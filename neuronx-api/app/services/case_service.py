"""
Case Processing Service

Handles post-retainer case lifecycle:
  Onboarding → Doc Collection → Form Prep → Review → Submit → Processing → Decision → Closed

Integrates with GHL Pipeline #2 (Case Processing) via tags + custom fields.
Program-aware: content (checklists, timelines, forms) loaded from config/programs.yaml.

Architecture: PostgreSQL is authoritative for case lifecycle data.
GHL gets a sync of case status for workflow triggers + operator visibility.
"""

import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional

from app.services.ghl_client import GHLClient
from app.utils.compliance_log import log_event
from app.config_loader import load_yaml_config

logger = logging.getLogger("neuronx.cases")

# ── Case Stage State Machine ─────────────────────────────────────────────
# Defines valid transitions. Key = current stage, Value = set of allowed next stages.
VALID_TRANSITIONS: dict[str, set[str]] = {
    "onboarding":      {"doc_collection", "closed"},
    "doc_collection":  {"docs_complete", "onboarding", "closed"},
    "docs_complete":   {"form_prep", "doc_collection", "closed"},
    "form_prep":       {"under_review", "doc_collection", "closed"},
    "under_review":    {"submitted", "form_prep", "closed"},
    "submitted":       {"processing", "closed"},
    "processing":      {"rfi", "decision", "closed"},
    "rfi":             {"processing", "submitted", "closed"},
    "decision":        {"closed"},
    "closed":          set(),  # terminal state
}

STAGE_TAGS: dict[str, str] = {
    "onboarding":      "nx:case:onboarding",
    "doc_collection":  "nx:case:docs_pending",
    "docs_complete":   "nx:case:docs_complete",
    "form_prep":       "nx:case:form_prep",
    "under_review":    "nx:case:under_review",
    "submitted":       "nx:case:submitted",
    "processing":      "nx:case:processing",
    "rfi":             "nx:case:rfi",
    "decision":        "nx:case:decision",
    "closed":          "nx:case:closed",
}

ALL_STAGES = list(STAGE_TAGS.keys())


def _load_programs_config() -> dict:
    """Load program definitions from YAML — single source of truth."""
    try:
        cfg = load_yaml_config("programs")
        return cfg.get("programs", {})
    except Exception as e:
        logger.warning("Failed to load programs config: %s — using empty defaults", e)
        return {}


def _get_processing_times(program_type: str) -> dict:
    """Get processing time estimate from config."""
    programs = _load_programs_config()
    for name, prog in programs.items():
        if name.lower() == program_type.lower():
            return prog.get("processing_months", {"min": 3, "max": 12, "avg": 6})
    return {"min": 3, "max": 12, "avg": 6}


def _get_ircc_forms(program_type: str) -> list:
    """Get required IRCC forms from config."""
    programs = _load_programs_config()
    for name, prog in programs.items():
        if name.lower() == program_type.lower():
            return prog.get("ircc_forms", [])
    return []


def _generate_case_id() -> str:
    """Generate collision-safe case ID: NX-YYYYMMDD-XXXXXXXX (UUID-based)."""
    now = datetime.now(tz=timezone.utc)
    unique = uuid.uuid4().hex[:8].upper()
    return f"NX-{now.strftime('%Y%m%d')}-{unique}"


class CaseService:
    """Manages case processing lifecycle and program-specific content."""

    def get_ircc_forms(self, program_type: str) -> list:
        """Get required IRCC forms for a program type from config."""
        return _get_ircc_forms(program_type)

    def get_processing_estimate(self, program_type: str) -> dict:
        """Get processing time estimate for a program type from config."""
        return _get_processing_times(program_type)

    def _get_ghl_client(self) -> GHLClient:
        return GHLClient()

    # ── PATCH /cases/{case_id}/status ─────────────────────────────────

    async def update_case_status(
        self,
        case_id: str,
        new_stage: str,
        notes: Optional[str] = None,
        updated_by: str = "system",
    ) -> dict:
        """
        Transition a case to a new stage with full validation + persistence.

        1. Validate transition via state machine
        2. Update PostgreSQL case record
        3. Sync GHL tags + custom fields
        4. Log activity + compliance event
        """
        from app import database

        if new_stage not in ALL_STAGES:
            return {"error": f"Unknown stage '{new_stage}'. Valid: {ALL_STAGES}"}

        # ── 1) Load case from PostgreSQL ──
        if not database.async_session_factory:
            return {"error": "Database not configured"}

        from app.models.db_models import Case, Activity
        from sqlalchemy import select

        async with database.async_session_factory() as session:
            result = await session.execute(
                select(Case).where(Case.case_id == case_id)
            )
            case = result.scalar_one_or_none()

            if not case:
                return {"error": f"Case '{case_id}' not found"}

            old_stage = case.stage

            # ── 2) Validate transition ──
            allowed = VALID_TRANSITIONS.get(old_stage, set())
            if new_stage not in allowed:
                return {
                    "error": f"Invalid transition: {old_stage} → {new_stage}",
                    "current_stage": old_stage,
                    "allowed_transitions": sorted(allowed),
                }

            # ── 3) Update PostgreSQL ──
            case.stage = new_stage
            now = datetime.now(tz=timezone.utc)

            if new_stage == "closed":
                case.closed_at = now

            # Record activity
            activity = Activity(
                contact_id=case.contact_id,
                activity_type="stage_changed",
                detail=f"{old_stage} → {new_stage}" + (f" | {notes}" if notes else ""),
                metadata_json={
                    "case_id": case_id,
                    "old_stage": old_stage,
                    "new_stage": new_stage,
                    "updated_by": updated_by,
                },
            )
            session.add(activity)
            await session.commit()

        # ── 4) Sync to GHL ──
        tag = STAGE_TAGS.get(new_stage)
        contact_id = case.contact_id
        try:
            ghl = self._get_ghl_client()
            if tag:
                await ghl.add_tag(contact_id, tag)
            if notes:
                await ghl.update_custom_fields(contact_id, {"case_status_notes": notes})
                await ghl.add_note(contact_id, f"[CASE UPDATE] {old_stage} → {new_stage}\n{notes}")
        except Exception as e:
            logger.warning("GHL sync failed for case %s: %s (DB updated OK)", case_id, e)

        # ── 5) Compliance log ──
        log_event("case_stage_update", {
            "case_id": case_id,
            "contact_id": contact_id,
            "old_stage": old_stage,
            "new_stage": new_stage,
            "updated_by": updated_by,
        })

        logger.info("Case %s transitioned: %s → %s", case_id, old_stage, new_stage)

        return {
            "case_id": case_id,
            "contact_id": contact_id,
            "old_stage": old_stage,
            "new_stage": new_stage,
            "tag_added": tag,
            "allowed_next": sorted(VALID_TRANSITIONS.get(new_stage, set())),
        }

    async def get_case_by_id(self, case_id: str) -> Optional[dict]:
        """Fetch a single case from PostgreSQL by case_id."""
        from app import database
        if not database.async_session_factory:
            return None

        from app.models.db_models import Case
        from sqlalchemy import select

        async with database.async_session_factory() as session:
            result = await session.execute(
                select(Case).where(Case.case_id == case_id)
            )
            case = result.scalar_one_or_none()
            if not case:
                return None

            return {
                "case_id": case.case_id,
                "contact_id": case.contact_id,
                "program_type": case.program_type,
                "assigned_rcic": case.assigned_rcic,
                "stage": case.stage,
                "complexity": case.complexity,
                "ircc_receipt_number": case.ircc_receipt_number,
                "ircc_decision": case.ircc_decision,
                "docs_required": case.docs_required,
                "docs_received": case.docs_received,
                "retainer_value": case.retainer_value,
                "created_at": case.created_at.isoformat() if case.created_at else None,
                "closed_at": case.closed_at.isoformat() if case.closed_at else None,
                "doc_deadline": case.doc_deadline.isoformat() if case.doc_deadline else None,
                "allowed_transitions": sorted(VALID_TRANSITIONS.get(case.stage, set())),
            }

    async def list_cases(self, stage: Optional[str] = None, limit: int = 50) -> list[dict]:
        """List cases, optionally filtered by stage."""
        from app import database
        if not database.async_session_factory:
            return []

        from app.models.db_models import Case
        from sqlalchemy import select

        async with database.async_session_factory() as session:
            q = select(Case).order_by(Case.created_at.desc()).limit(limit)
            if stage:
                q = q.where(Case.stage == stage)
            result = await session.execute(q)
            cases = result.scalars().all()

            return [
                {
                    "case_id": c.case_id,
                    "contact_id": c.contact_id,
                    "program_type": c.program_type,
                    "assigned_rcic": c.assigned_rcic,
                    "stage": c.stage,
                    "retainer_value": c.retainer_value,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                }
                for c in cases
            ]

    async def initiate_case(self, contact_id: str, program_type: str, assigned_rcic: str) -> dict:
        """
        Start a new case after retainer is signed.
        1. Persists case to PostgreSQL (authoritative for case lifecycle)
        2. Syncs to GHL (custom fields + tags + note)
        3. Logs activity + compliance event
        """
        # Validate program_type against config
        programs = _load_programs_config()
        valid_programs = [name.lower() for name in programs.keys()]
        if program_type.lower() not in valid_programs:
            return {"error": f"Unknown program_type '{program_type}'. Valid: {list(programs.keys())}"}

        ghl = GHLClient()
        now = datetime.now(tz=timezone.utc)

        # Generate collision-safe case ID
        case_id = _generate_case_id()

        # Set doc collection deadline (14 days)
        deadline = now + timedelta(days=14)

        # Get processing time estimate from config
        proc_time = _get_processing_times(program_type)

        # Get required doc count from config
        forms = _get_ircc_forms(program_type)
        docs_required = len([f for f in forms if f.get("required", False)])

        # ── 1) Persist to PostgreSQL ──
        from app import database
        if database.async_session_factory:
            from app.models.db_models import Case, Activity
            try:
                async with database.async_session_factory() as session:
                    case = Case(
                        case_id=case_id,
                        contact_id=contact_id,
                        program_type=program_type,
                        assigned_rcic=assigned_rcic,
                        stage="onboarding",
                        complexity="Standard",
                        ircc_decision="Pending",
                        docs_required=docs_required,
                        docs_received=0,
                        retainer_value=0.0,
                        doc_deadline=deadline,
                    )
                    session.add(case)

                    activity = Activity(
                        contact_id=contact_id,
                        activity_type="case_initiated",
                        detail=f"Case {case_id} created — {program_type} — RCIC: {assigned_rcic}",
                        metadata_json={
                            "case_id": case_id,
                            "program_type": program_type,
                            "assigned_rcic": assigned_rcic,
                        },
                    )
                    session.add(activity)
                    await session.commit()
                    logger.info("Case %s persisted to PostgreSQL", case_id)
            except Exception as e:
                logger.error("Failed to persist case %s to DB: %s (continuing with GHL)", case_id, e)

        # ── 2) Sync to GHL ──
        try:
            await ghl.update_custom_fields(contact_id, {
                "case_id": case_id,
                "case_program_type": program_type,
                "case_assigned_rcic": assigned_rcic,
                "case_assigned_at": now.strftime("%Y-%m-%d"),
                "case_deadline_date": deadline.strftime("%Y-%m-%d"),
                "case_deadline_type": "Doc Collection",
                "case_complexity": "Standard",
                "ircc_decision": "Pending",
            })

            await ghl.add_tags(contact_id, ["nx:case:onboarding", "nx:case:docs_pending"])

            contact = await ghl.get_contact(contact_id)
            name = f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip()

            await ghl.add_note(contact_id, (
                f"CASE INITIATED — {case_id}\n"
                f"{'=' * 40}\n"
                f"Program: {program_type}\n"
                f"Assigned RCIC: {assigned_rcic}\n"
                f"Document deadline: {deadline.strftime('%Y-%m-%d')}\n"
                f"Estimated processing: {proc_time['min']}-{proc_time['max']} months\n"
                f"{'=' * 40}\n"
                f"Generated by NeuronX at {now.strftime('%Y-%m-%d %H:%M')} UTC"
            ))
        except Exception as e:
            logger.warning("GHL sync failed for case %s: %s (DB record exists)", case_id, e)

        # ── 3) Compliance log ──
        log_event("case_initiated", {
            "case_id": case_id,
            "contact_id": contact_id,
            "program_type": program_type,
            "assigned_rcic": assigned_rcic,
        })

        return {
            "case_id": case_id,
            "contact_id": contact_id,
            "program_type": program_type,
            "assigned_rcic": assigned_rcic,
            "doc_deadline": deadline.isoformat(),
            "estimated_processing_months": proc_time,
            "ircc_forms": forms,
            "docs_required": docs_required,
            "status": "onboarding",
            "allowed_transitions": sorted(VALID_TRANSITIONS["onboarding"]),
        }

    async def update_stage(self, contact_id: str, new_stage: str, notes: Optional[str] = None) -> dict:
        """Update case stage via tag management."""
        ghl = GHLClient()

        # Map stage to tag
        stage_tags = {
            "onboarding": "nx:case:onboarding",
            "doc_collection": "nx:case:docs_pending",
            "docs_complete": "nx:case:docs_complete",
            "form_prep": "nx:case:form_prep",
            "under_review": "nx:case:under_review",
            "submitted": "nx:case:submitted",
            "processing": "nx:case:processing",
            "rfi": "nx:case:rfi",
            "decision": "nx:case:decision",
            "closed": "nx:case:closed",
        }

        tag = stage_tags.get(new_stage)
        if not tag:
            return {"error": f"Unknown stage: {new_stage}"}

        await ghl.add_tag(contact_id, tag)

        if notes:
            await ghl.update_custom_fields(contact_id, {"case_status_notes": notes})
            await ghl.add_note(contact_id, f"[CASE UPDATE] Stage: {new_stage}\n{notes}")

        log_event("case_stage_update", {
            "contact_id": contact_id,
            "new_stage": new_stage,
            "tag": tag,
        })

        return {"contact_id": contact_id, "stage": new_stage, "tag_added": tag}

    async def record_submission(self, contact_id: str, receipt_number: str, submission_date: Optional[str] = None) -> dict:
        """Record IRCC submission with receipt number."""
        ghl = GHLClient()
        now = datetime.now(tz=timezone.utc)

        sub_date = submission_date or now.strftime("%Y-%m-%d")

        await ghl.update_custom_fields(contact_id, {
            "ircc_receipt_number": receipt_number,
            "ircc_submission_date": sub_date,
            "case_deadline_date": (now + timedelta(days=30)).strftime("%Y-%m-%d"),
            "case_deadline_type": "IRCC Response",
        })

        await ghl.add_tag(contact_id, "nx:case:submitted")
        await ghl.add_note(contact_id, (
            f"[IRCC SUBMITTED]\n"
            f"Receipt #: {receipt_number}\n"
            f"Date: {sub_date}\n"
            f"Next milestone: IRCC response (est. 30 days)"
        ))

        log_event("ircc_submission", {
            "contact_id": contact_id,
            "receipt_number": receipt_number,
            "submission_date": sub_date,
        })

        return {"contact_id": contact_id, "receipt_number": receipt_number, "status": "submitted"}

    async def record_decision(self, contact_id: str, decision: str, decision_date: Optional[str] = None, notes: Optional[str] = None) -> dict:
        """Record IRCC decision (approved/refused/withdrawn/returned)."""
        valid_decisions = ["Approved", "Refused", "Withdrawn", "Returned", "Pending"]
        if decision not in valid_decisions:
            return {"error": f"Invalid decision: {decision}. Must be one of: {valid_decisions}"}

        ghl = GHLClient()
        now = datetime.now(tz=timezone.utc)
        dec_date = decision_date or now.strftime("%Y-%m-%d")

        await ghl.update_custom_fields(contact_id, {
            "ircc_decision": decision,
            "ircc_decision_date": dec_date,
            "case_status_notes": notes or f"IRCC decision: {decision}",
        })

        await ghl.add_tag(contact_id, "nx:case:decision")
        await ghl.add_note(contact_id, (
            f"[IRCC DECISION] {decision}\n"
            f"Date: {dec_date}\n"
            f"{notes or ''}"
        ))

        log_event("ircc_decision", {
            "contact_id": contact_id,
            "decision": decision,
            "decision_date": dec_date,
        })

        return {"contact_id": contact_id, "decision": decision, "status": "decision_recorded"}
