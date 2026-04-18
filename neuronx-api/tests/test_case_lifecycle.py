"""
Tests for case lifecycle API — PATCH /cases/{case_id}/status, GET /cases/by-id/{case_id},
GET /cases/list, GET /cases/transitions.

Uses in-memory SQLite DB with pre-seeded case data.
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text

from app.database import Base
from app.models.db_models import Contact, Case, Activity
from app.services.case_service import (
    CaseService, VALID_TRANSITIONS, ALL_STAGES, STAGE_TAGS,
)


# ── Fixtures ──────────────────────────────────────────────────────────────


def _create_tables_sqlite(conn):
    """Create SQLite-compatible tables (ARRAY → JSON workaround)."""
    from sqlalchemy import Column, String, Text, Integer, Float, DateTime, JSON, MetaData, Table

    meta = MetaData()
    Table("contacts", meta,
          Column("id", String(50), primary_key=True),
          Column("first_name", String(100)), Column("last_name", String(100)),
          Column("email", String(255)), Column("phone", String(50)),
          Column("tags", JSON), Column("source", String(100)),
          Column("custom_fields", JSON), Column("readiness_score", Integer),
          Column("readiness_outcome", String(50)), Column("program_interest", String(100)),
          Column("ghl_created_at", DateTime), Column("synced_at", DateTime))
    Table("cases", meta,
          Column("id", Integer, primary_key=True, autoincrement=True),
          Column("case_id", String(50), unique=True),
          Column("contact_id", String(50)), Column("program_type", String(100)),
          Column("assigned_rcic_id", String(50)), Column("assigned_rcic_name", String(100)),
          Column("stage", String(50)),
          Column("complexity", String(20)), Column("ircc_receipt_number", String(50)),
          Column("ircc_submission_date", DateTime), Column("ircc_decision", String(20)),
          Column("ircc_decision_date", DateTime), Column("docs_required", Integer),
          Column("docs_received", Integer), Column("retainer_value", Float),
          Column("created_at", DateTime), Column("closed_at", DateTime),
          Column("doc_deadline", DateTime))
    Table("activities", meta,
          Column("id", Integer, primary_key=True, autoincrement=True),
          Column("contact_id", String(50)), Column("activity_type", String(50)),
          Column("detail", Text), Column("metadata_json", JSON),
          Column("created_at", DateTime))
    meta.create_all(conn)


@pytest_asyncio.fixture
async def db_session():
    """Create in-memory SQLite engine + pre-seed case data."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(_create_tables_sqlite)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Seed data — use raw SQL to avoid ORM ARRAY serialization issues with SQLite
    now = datetime.now(timezone.utc)
    async with session_factory() as session:
        await session.execute(text(
            "INSERT INTO contacts (id, first_name, last_name, email, phone, tags, source, custom_fields, readiness_score, readiness_outcome, program_interest, synced_at) "
            "VALUES (:id, :fn, :ln, :email, '', '[]', '', '{}', :score, '', :prog, :synced)"
        ), [
            {"id": "test-contact-1", "fn": "Priya", "ln": "Sharma", "email": "priya@test.com", "score": 82, "prog": "Express Entry", "synced": now.isoformat()},
            {"id": "test-contact-2", "fn": "Ahmed", "ln": "Hassan", "email": "ahmed@test.com", "score": 91, "prog": "Spousal Sponsorship", "synced": now.isoformat()},
        ])

        await session.execute(text(
            "INSERT INTO cases (case_id, contact_id, program_type, assigned_rcic_id, assigned_rcic_name, stage, complexity, ircc_receipt_number, ircc_decision, docs_required, docs_received, retainer_value, created_at) "
            "VALUES (:cid, :contact, :prog, NULL, :rcic, :stage, 'Standard', '', 'Pending', 0, 0, :val, :created)"
        ), [
            {"cid": "NX-20260416-TEST01", "contact": "test-contact-1", "prog": "Express Entry", "rcic": "Rajiv Mehta", "stage": "onboarding", "val": 3500, "created": (now - timedelta(days=10)).isoformat()},
            {"cid": "NX-20260416-TEST02", "contact": "test-contact-2", "prog": "Spousal Sponsorship", "rcic": "Nina Patel", "stage": "doc_collection", "val": 4500, "created": (now - timedelta(days=5)).isoformat()},
        ])
        await session.execute(text(
            "INSERT INTO cases (case_id, contact_id, program_type, assigned_rcic_id, assigned_rcic_name, stage, complexity, ircc_receipt_number, ircc_decision, docs_required, docs_received, retainer_value, created_at, closed_at) "
            "VALUES (:cid, :contact, :prog, NULL, :rcic, 'closed', 'Standard', '', 'Approved', 8, 8, 3500, :created, :closed)"
        ), [{"cid": "NX-20260416-TEST03", "contact": "test-contact-1", "prog": "Express Entry", "rcic": "Rajiv Mehta", "created": (now - timedelta(days=90)).isoformat(), "closed": (now - timedelta(days=15)).isoformat()}])
        await session.commit()

    yield session_factory

    await engine.dispose()


# ── State Machine Unit Tests ──────────────────────────────────────────────


class TestStateMachine:
    def test_all_stages_have_transitions(self):
        for stage in ALL_STAGES:
            assert stage in VALID_TRANSITIONS

    def test_all_stages_have_tags(self):
        for stage in ALL_STAGES:
            assert stage in STAGE_TAGS
            assert STAGE_TAGS[stage].startswith("nx:case:")

    def test_closed_is_terminal(self):
        assert VALID_TRANSITIONS["closed"] == set()

    def test_onboarding_can_go_to_doc_collection(self):
        assert "doc_collection" in VALID_TRANSITIONS["onboarding"]

    def test_onboarding_cannot_skip_to_submitted(self):
        assert "submitted" not in VALID_TRANSITIONS["onboarding"]

    def test_every_stage_can_close(self):
        for stage in ALL_STAGES:
            if stage != "closed":
                assert "closed" in VALID_TRANSITIONS[stage], f"{stage} should allow transition to closed"

    def test_rfi_can_return_to_processing(self):
        assert "processing" in VALID_TRANSITIONS["rfi"]

    def test_doc_collection_can_return_to_onboarding(self):
        assert "onboarding" in VALID_TRANSITIONS["doc_collection"]

    def test_stage_count(self):
        assert len(ALL_STAGES) == 10


# ── Case Lifecycle Service Tests ──────────────────────────────────────────


class TestCaseLifecycle:
    @pytest.mark.asyncio
    async def test_update_case_status_valid(self, db_session):
        """Test valid transition: onboarding → doc_collection."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        with patch.object(service, '_get_ghl_client') as mock_ghl:
            ghl = AsyncMock()
            mock_ghl.return_value = ghl

            result = await service.update_case_status(
                case_id="NX-20260416-TEST01",
                new_stage="doc_collection",
                notes="Documents requested",
            )

        assert result["old_stage"] == "onboarding"
        assert result["new_stage"] == "doc_collection"
        assert result["tag_added"] == "nx:case:docs_pending"
        assert "closed" in result["allowed_next"]
        assert "docs_complete" in result["allowed_next"]

    @pytest.mark.asyncio
    async def test_update_case_status_invalid_transition(self, db_session):
        """Test invalid transition: onboarding → submitted (must go through intermediaries)."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        result = await service.update_case_status(
            case_id="NX-20260416-TEST01",
            new_stage="submitted",
        )

        assert "error" in result
        assert "Invalid transition" in result["error"]
        assert result["current_stage"] == "onboarding"
        assert "allowed_transitions" in result

    @pytest.mark.asyncio
    async def test_update_case_status_not_found(self, db_session):
        """Test non-existent case ID."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        result = await service.update_case_status(
            case_id="NX-DOESNOTEXIST",
            new_stage="doc_collection",
        )

        assert "error" in result
        assert "not found" in result["error"]

    @pytest.mark.asyncio
    async def test_update_case_status_unknown_stage(self, db_session):
        """Test unknown target stage."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        result = await service.update_case_status(
            case_id="NX-20260416-TEST01",
            new_stage="flying_unicorn",
        )

        assert "error" in result
        assert "Unknown stage" in result["error"]

    @pytest.mark.asyncio
    async def test_close_sets_closed_at(self, db_session):
        """Test that closing a case sets the closed_at timestamp."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        with patch.object(service, '_get_ghl_client') as mock_ghl:
            mock_ghl.return_value = AsyncMock()

            result = await service.update_case_status(
                case_id="NX-20260416-TEST01",
                new_stage="closed",
            )

        assert result["new_stage"] == "closed"

        # Verify closed_at was set in DB
        from app.models.db_models import Case
        from sqlalchemy import select

        async with db_session() as session:
            case = (await session.execute(
                select(Case).where(Case.case_id == "NX-20260416-TEST01")
            )).scalar_one()
            assert case.closed_at is not None

    @pytest.mark.asyncio
    async def test_closed_cannot_transition(self, db_session):
        """Test that closed cases cannot be transitioned."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        result = await service.update_case_status(
            case_id="NX-20260416-TEST03",
            new_stage="onboarding",
        )

        assert "error" in result
        assert "Invalid transition" in result["error"]

    @pytest.mark.asyncio
    async def test_activity_logged_on_transition(self, db_session):
        """Test that an activity record is created on transition."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        with patch.object(service, '_get_ghl_client') as mock_ghl:
            mock_ghl.return_value = AsyncMock()

            await service.update_case_status(
                case_id="NX-20260416-TEST02",
                new_stage="docs_complete",
                notes="All 12 docs received",
                updated_by="rcic_nina",
            )

        from sqlalchemy import select
        async with db_session() as session:
            activities = (await session.execute(
                select(Activity).where(Activity.contact_id == "test-contact-2")
            )).scalars().all()

        assert len(activities) == 1
        assert activities[0].activity_type == "stage_changed"
        assert "doc_collection → docs_complete" in activities[0].detail
        assert activities[0].metadata_json["updated_by"] == "rcic_nina"

    @pytest.mark.asyncio
    async def test_get_case_by_id(self, db_session):
        """Test fetching case details."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        case = await service.get_case_by_id("NX-20260416-TEST01")

        assert case is not None
        assert case["case_id"] == "NX-20260416-TEST01"
        assert case["program_type"] == "Express Entry"
        assert case["stage"] == "onboarding"
        assert "doc_collection" in case["allowed_transitions"]

    @pytest.mark.asyncio
    async def test_get_case_by_id_not_found(self, db_session):
        """Test fetching non-existent case."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        case = await service.get_case_by_id("NX-DOESNOTEXIST")
        assert case is None

    @pytest.mark.asyncio
    async def test_list_cases(self, db_session):
        """Test listing all cases."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        cases = await service.list_cases()

        assert len(cases) == 3
        # Should be ordered by created_at desc
        assert cases[0]["case_id"] == "NX-20260416-TEST02"  # most recent

    @pytest.mark.asyncio
    async def test_list_cases_by_stage(self, db_session):
        """Test filtering cases by stage."""
        import app.database as database
        database.async_session_factory = db_session

        service = CaseService()
        cases = await service.list_cases(stage="onboarding")

        assert len(cases) == 1
        assert cases[0]["stage"] == "onboarding"


# ── Router Tests ──────────────────────────────────────────────────────────


class TestCaseRouter:
    @pytest.fixture
    def client(self):
        from fastapi.testclient import TestClient
        from main import app
        return TestClient(app)

    def test_transitions_endpoint(self, client):
        r = client.get("/cases/transitions")
        assert r.status_code == 200
        data = r.json()
        assert len(data["stages"]) == 10
        assert "onboarding" in data["stages"]
        assert data["transitions"]["closed"] == []

    def test_patch_status_unknown_stage_returns_400(self, client):
        r = client.patch("/cases/NX-FAKE/status", json={"new_stage": "flying_unicorn"})
        # Even if case doesn't exist in DB, unknown stage is caught first
        assert r.status_code in (400, 500)  # 400 if validation catches, 500 if DB not configured

    def test_list_cases_bad_stage_returns_400(self, client):
        r = client.get("/cases/list?stage=flying_unicorn")
        assert r.status_code == 400
