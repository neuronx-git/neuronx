"""
Database models for NeuronX analytics and case processing.

These tables mirror GHL data for:
1. Metabase analytics dashboards
2. Case processing persistence
3. Document signature tracking
4. Activity audit trail

GHL remains the source of truth. These tables are populated via:
- Webhook events (real-time activity tracking)
- Daily full sync (consistency guarantee)
"""

from datetime import datetime, timezone
from sqlalchemy import (
    String, Text, Integer, Float, DateTime, Boolean,
    JSON, ForeignKey, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from app.database import Base


class Contact(Base):
    """Mirror of GHL contact — synced for Metabase queries."""
    __tablename__ = "contacts"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)  # GHL contact ID
    first_name: Mapped[str] = mapped_column(String(100), default="")
    last_name: Mapped[str] = mapped_column(String(100), default="")
    email: Mapped[str] = mapped_column(String(255), default="")
    phone: Mapped[str] = mapped_column(String(50), default="")
    tags: Mapped[list] = mapped_column(ARRAY(String), default=list)
    source: Mapped[str] = mapped_column(String(100), default="")
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict)

    # Scoring
    readiness_score: Mapped[int] = mapped_column(Integer, default=0)
    readiness_outcome: Mapped[str] = mapped_column(String(50), default="")
    program_interest: Mapped[str] = mapped_column(String(100), default="")

    # Timestamps
    ghl_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    opportunities: Mapped[list["Opportunity"]] = relationship(back_populates="contact")
    cases: Mapped[list["Case"]] = relationship(back_populates="contact")
    activities: Mapped[list["Activity"]] = relationship(back_populates="contact")
    signatures: Mapped[list["Signature"]] = relationship(back_populates="contact")

    __table_args__ = (
        Index("ix_contacts_email", "email"),
        Index("ix_contacts_program", "program_interest"),
        Index("ix_contacts_score", "readiness_score"),
    )


class Opportunity(Base):
    """Mirror of GHL pipeline opportunity — for funnel analytics."""
    __tablename__ = "opportunities"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)  # GHL opportunity ID
    contact_id: Mapped[str] = mapped_column(String(50), ForeignKey("contacts.id"))
    pipeline_id: Mapped[str] = mapped_column(String(50))
    pipeline_name: Mapped[str] = mapped_column(String(100), default="")
    stage_id: Mapped[str] = mapped_column(String(50), default="")
    stage_name: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(String(20), default="open")  # open, won, lost, abandoned
    monetary_value: Mapped[float] = mapped_column(Float, default=0.0)
    assigned_to: Mapped[str] = mapped_column(String(100), default="")

    ghl_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    ghl_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    contact: Mapped["Contact"] = relationship(back_populates="opportunities")

    __table_args__ = (
        Index("ix_opp_pipeline", "pipeline_id"),
        Index("ix_opp_stage", "stage_name"),
        Index("ix_opp_status", "status"),
    )


class User(Base):
    """Team member / RCIC — synced from GHL users API.

    Source of truth: GHL /users/ endpoint. We maintain a local mirror so we
    can:
      * enforce referential integrity on Case.assigned_rcic_id (no typos)
      * compute reliable per-user analytics / leaderboards
      * implement access control in upcoming auth work
    The `id` column == GHL user id (same string, no surrogate).
    """
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)  # GHL user ID
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), default="")
    last_name: Mapped[str] = mapped_column(String(100), default="")
    full_name: Mapped[str] = mapped_column(String(200), default="")  # "First Last" — precomputed for grouping
    phone: Mapped[str] = mapped_column(String(50), default="")

    # Role values: managing_partner, senior_rcic, junior_rcic, csm, sdr, ops, intake, admin, user
    role: Mapped[str] = mapped_column(String(30), default="user")
    rcic_license: Mapped[str] = mapped_column(String(20), default="")  # "R123456" — empty for non-RCIC
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    max_concurrent_cases: Mapped[int] = mapped_column(Integer, default=30)
    hire_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Explicit GHL mirror (same as id but clearer for joins/debugging)
    ghl_user_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    cases: Mapped[list["Case"]] = relationship(back_populates="assigned_user")

    __table_args__ = (
        Index("ix_user_role", "role"),
        Index("ix_user_active", "is_active"),
    )


class Case(Base):
    """Case processing record — post-retainer lifecycle tracking."""
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[str] = mapped_column(String(50), unique=True)  # NX-20260404-ABCDEF
    contact_id: Mapped[str] = mapped_column(String(50), ForeignKey("contacts.id"))
    program_type: Mapped[str] = mapped_column(String(100))

    # ── Assignment (Blocker #2 migration) ───────────────────────────────────
    # Preferred: FK to users.id. Nullable during backfill period.
    assigned_rcic_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("users.id"), nullable=True, index=True
    )
    # Denormalized display name — kept for backwards compatibility with
    # code/views that still read the string column. DEPRECATED: prefer the
    # FK join via `assigned_user.full_name`. Do not drop until all consumers
    # migrate.
    assigned_rcic_name: Mapped[str] = mapped_column(String(100), default="Unassigned")

    stage: Mapped[str] = mapped_column(String(50), default="onboarding")
    complexity: Mapped[str] = mapped_column(String(20), default="Standard")

    # IRCC tracking
    ircc_receipt_number: Mapped[str] = mapped_column(String(50), default="")
    ircc_submission_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    ircc_decision: Mapped[str] = mapped_column(String(20), default="Pending")
    ircc_decision_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Document tracking
    docs_required: Mapped[int] = mapped_column(Integer, default=0)
    docs_received: Mapped[int] = mapped_column(Integer, default=0)

    # Value
    retainer_value: Mapped[float] = mapped_column(Float, default=0.0)

    # Dates
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    closed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    doc_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    contact: Mapped["Contact"] = relationship(back_populates="cases")
    assigned_user: Mapped["User"] = relationship(back_populates="cases", lazy="selectin")

    __table_args__ = (
        Index("ix_case_stage", "stage"),
        Index("ix_case_program", "program_type"),
        Index("ix_case_rcic_name", "assigned_rcic_name"),
    )

    # ── Backwards-compat shim ───────────────────────────────────────────────
    # A lot of older code (and seed scripts) still pass/read `assigned_rcic`
    # as a plain string. We expose it as an alias of `assigned_rcic_name`,
    # and accept it in the constructor for legacy callers.
    def __init__(self, **kwargs):
        legacy = kwargs.pop("assigned_rcic", None)
        if legacy is not None and "assigned_rcic_name" not in kwargs:
            kwargs["assigned_rcic_name"] = legacy
        super().__init__(**kwargs)

    @property
    def assigned_rcic(self) -> str:
        return self.assigned_rcic_name or "Unassigned"

    @assigned_rcic.setter
    def assigned_rcic(self, value: str) -> None:
        self.assigned_rcic_name = value or "Unassigned"


class Activity(Base):
    """Activity audit trail — every webhook event + case stage change."""
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contact_id: Mapped[str] = mapped_column(String(50), ForeignKey("contacts.id"))
    activity_type: Mapped[str] = mapped_column(String(50))  # form_submitted, call_completed, tag_added, stage_changed, etc.
    detail: Mapped[str] = mapped_column(Text, default="")
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    contact: Mapped["Contact"] = relationship(back_populates="activities")

    __table_args__ = (
        Index("ix_activity_type", "activity_type"),
        Index("ix_activity_created", "created_at"),
    )


class Signature(Base):
    """Documenso e-signature tracking."""
    __tablename__ = "signatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contact_id: Mapped[str] = mapped_column(String(50), ForeignKey("contacts.id"))
    document_type: Mapped[str] = mapped_column(String(50))  # retainer, assessment, consent
    documenso_document_id: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, sent, viewed, signed, declined
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    signer_email: Mapped[str] = mapped_column(String(255), default="")

    contact: Mapped["Contact"] = relationship(back_populates="signatures")

    __table_args__ = (
        Index("ix_sig_status", "status"),
        Index("ix_sig_documenso", "documenso_document_id"),
    )


class Dependent(Base):
    """Dependent/family member linked to a case — wrapper-authoritative."""
    __tablename__ = "dependents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[str] = mapped_column(String(50), ForeignKey("cases.case_id"))
    contact_id: Mapped[str] = mapped_column(String(50), ForeignKey("contacts.id"))
    full_name: Mapped[str] = mapped_column(String(200))
    relationship: Mapped[str] = mapped_column(String(50))  # spouse, child, parent
    date_of_birth: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    passport_number: Mapped[str] = mapped_column(String(50), default="")
    passport_expiry: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    docs_status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, partial, complete
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        Index("ix_dep_case", "case_id"),
        Index("ix_dep_contact", "contact_id"),
    )


class ProcessedWebhook(Base):
    """Idempotency tracking — prevents duplicate webhook processing."""
    __tablename__ = "processed_webhooks"

    webhook_id: Mapped[str] = mapped_column(String(200), primary_key=True)
    source: Mapped[str] = mapped_column(String(20))  # ghl, vapi, typebot, documenso
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    response_status: Mapped[int] = mapped_column(Integer, default=200)

    __table_args__ = (
        Index("ix_pw_source", "source", "processed_at"),
    )


class DeadLetterQueue(Base):
    """Failed webhook retry queue — for manual review and retry."""
    __tablename__ = "dead_letter_queue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(20))  # ghl, vapi, typebot, documenso
    webhook_id: Mapped[str] = mapped_column(String(200), default="")
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    error_message: Mapped[str] = mapped_column(Text, default="")
    attempt_count: Mapped[int] = mapped_column(Integer, default=1)
    first_failed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    last_attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, retrying, resolved, abandoned

    __table_args__ = (
        Index("ix_dlq_status", "status"),
        Index("ix_dlq_source", "source"),
    )


class SyncLog(Base):
    """Tracks sync state for GHL → PostgreSQL data sync."""
    __tablename__ = "sync_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entity_type: Mapped[str] = mapped_column(String(50))  # contacts, opportunities
    last_sync_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    records_synced: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="completed")  # running, completed, failed
    error_message: Mapped[str] = mapped_column(Text, default="")
