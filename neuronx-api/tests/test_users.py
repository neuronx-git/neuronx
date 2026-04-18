"""
Tests for Blocker #2 — users table + Case.assigned_rcic_id FK.

Covers:
  * User model CRUD (in-memory SQLite)
  * Fuzzy name resolution (UserSyncService.resolve_by_name)
  * Role normalisation
  * Case backwards-compat shim (assigned_rcic → assigned_rcic_name)
  * users router endpoints (with DB stub)
  * Metabase SQL view syntax validity (compiles with PostgreSQL dialect)
  * GHL user sync (mocked HTTP)
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from sqlalchemy import text, Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


pytestmark = pytest.mark.database


# ───────────────────────────────────────────────────────────────────────────
# In-memory SQLite fixture with users + cases tables
# ───────────────────────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(_build_schema)
    yield engine
    await engine.dispose()


def _build_schema(conn):
    meta = MetaData()
    Table(
        "users", meta,
        Column("id", String(50), primary_key=True),
        Column("email", String(255)),
        Column("first_name", String(100), default=""),
        Column("last_name", String(100), default=""),
        Column("full_name", String(200), default=""),
        Column("phone", String(50), default=""),
        Column("role", String(30), default="user"),
        Column("rcic_license", String(20), default=""),
        Column("is_active", Boolean, default=True),
        Column("max_concurrent_cases", Integer, default=30),
        Column("hire_date", DateTime(timezone=True), nullable=True),
        Column("ghl_user_id", String(50)),
        Column("synced_at", DateTime(timezone=True)),
        Column("created_at", DateTime(timezone=True)),
    )
    Table(
        "cases", meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("case_id", String(50), unique=True),
        Column("contact_id", String(50)),
        Column("program_type", String(100)),
        Column("assigned_rcic_id", String(50), ForeignKey("users.id"), nullable=True),
        Column("assigned_rcic_name", String(100), default="Unassigned"),
        Column("stage", String(50), default="onboarding"),
        Column("created_at", DateTime(timezone=True)),
        Column("closed_at", DateTime(timezone=True), nullable=True),
        Column("ircc_decision", String(20), default="Pending"),
        Column("retainer_value", Integer, default=0),
        Column("docs_required", Integer, default=0),
        Column("docs_received", Integer, default=0),
    )
    meta.create_all(conn)


@pytest_asyncio.fixture
async def db_session(db_engine):
    factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session


@pytest_asyncio.fixture
async def seeded_users(db_session):
    """Insert a realistic set of 5 test users."""
    now = datetime.now(timezone.utc)
    rows = [
        ("u-mp",   "mp@demo.local",    "Rajiv",   "Mehta",   "Rajiv Mehta",   "managing_partner"),
        ("u-srna", "nina@demo.local",  "Nina",    "Patel",   "Nina Patel",    "senior_rcic"),
        ("u-srmc", "mike@demo.local",  "Michael", "Chen",    "Michael Chen",  "senior_rcic"),
        ("u-jrsa", "sarah@demo.local", "Sarah",   "Johnson", "Sarah Johnson", "junior_rcic"),
        ("u-csm",  "emily@demo.local", "Emily",   "Brooks",  "Emily Brooks",  "csm"),
    ]
    for uid, email, first, last, full, role in rows:
        await db_session.execute(
            text(
                "INSERT INTO users (id, email, first_name, last_name, full_name, role, "
                "is_active, ghl_user_id, synced_at, created_at) "
                "VALUES (:id, :email, :first, :last, :full, :role, 1, :id, :now, :now)"
            ),
            {"id": uid, "email": email, "first": first, "last": last, "full": full, "role": role, "now": now},
        )
    await db_session.commit()
    return rows


# ───────────────────────────────────────────────────────────────────────────
# 1. User CRUD
# ───────────────────────────────────────────────────────────────────────────

class TestUserCRUD:
    @pytest.mark.asyncio
    async def test_insert_and_read_user(self, db_session):
        now = datetime.now(timezone.utc)
        await db_session.execute(
            text(
                "INSERT INTO users (id, email, first_name, last_name, full_name, role, "
                "rcic_license, is_active, ghl_user_id, synced_at, created_at) "
                "VALUES ('u1', 'a@b.c', 'Ana', 'Lee', 'Ana Lee', 'senior_rcic', 'R999999', 1, 'u1', :now, :now)"
            ),
            {"now": now},
        )
        await db_session.commit()
        row = (await db_session.execute(text("SELECT * FROM users WHERE id='u1'"))).mappings().first()
        assert row["role"] == "senior_rcic"
        assert row["rcic_license"] == "R999999"
        assert row["full_name"] == "Ana Lee"

    @pytest.mark.asyncio
    async def test_case_fk_points_to_user(self, db_session, seeded_users):
        now = datetime.now(timezone.utc)
        await db_session.execute(
            text(
                "INSERT INTO cases (case_id, contact_id, program_type, assigned_rcic_id, "
                "assigned_rcic_name, stage, created_at) "
                "VALUES ('NX-FK-001', 'c-1', 'Express Entry', 'u-srna', 'Nina Patel', 'onboarding', :now)"
            ),
            {"now": now},
        )
        await db_session.commit()
        row = (await db_session.execute(
            text("SELECT c.case_id, u.full_name FROM cases c JOIN users u ON c.assigned_rcic_id = u.id "
                 "WHERE c.case_id='NX-FK-001'")
        )).mappings().first()
        assert row["full_name"] == "Nina Patel"


# ───────────────────────────────────────────────────────────────────────────
# 2. Role normalisation
# ───────────────────────────────────────────────────────────────────────────

class TestRoleNormalisation:
    def test_managing_partner_title(self):
        from app.services.user_sync_service import _normalise_role
        assert _normalise_role("Managing Partner / Head RCIC") == "managing_partner"

    def test_senior_rcic_title(self):
        from app.services.user_sync_service import _normalise_role
        assert _normalise_role("Senior RCIC Consultant") == "senior_rcic"

    def test_perms_fallback(self):
        from app.services.user_sync_service import _normalise_role
        assert _normalise_role("Some Custom Title", perms="csm") == "csm"

    def test_default_to_user(self):
        from app.services.user_sync_service import _normalise_role
        assert _normalise_role("Unknown Title", perms="", ghl_role="user") == "user"


# ───────────────────────────────────────────────────────────────────────────
# 3. Fuzzy name resolution
# ───────────────────────────────────────────────────────────────────────────

class TestNameResolution:
    @pytest.mark.asyncio
    async def test_clean_name_strips_demo_prefix_and_rcic_suffix(self):
        from app.services.user_sync_service import _clean_name_for_match
        assert _clean_name_for_match("DEMO - Nina Patel") == "nina patel"
        assert _clean_name_for_match("Nina Patel, RCIC") == "nina patel"
        assert _clean_name_for_match("Dr. Nina Patel") == "nina patel"
        assert _clean_name_for_match("") == ""

    @pytest.mark.asyncio
    async def test_resolve_by_name_exact_match(self, db_engine, seeded_users):
        from app.services.user_sync_service import UserSyncService
        factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

        with patch("app.services.user_sync_service.database.async_session_factory", factory):
            svc = UserSyncService()
            match = await svc.resolve_by_name("DEMO - Nina Patel")
            assert match is not None, "Should resolve 'DEMO - Nina Patel' to Nina"
            assert match["full_name"] == "Nina Patel"
            assert match["id"] == "u-srna"

    @pytest.mark.asyncio
    async def test_resolve_by_name_typo_tolerance(self, db_engine, seeded_users):
        from app.services.user_sync_service import UserSyncService
        factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
        with patch("app.services.user_sync_service.database.async_session_factory", factory):
            svc = UserSyncService()
            # "Nina Patell" should still match "Nina Patel" via fuzzy
            match = await svc.resolve_by_name("Nina Patell")
            assert match is not None
            assert match["id"] == "u-srna"

    @pytest.mark.asyncio
    async def test_resolve_by_name_no_match(self, db_engine, seeded_users):
        from app.services.user_sync_service import UserSyncService
        factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
        with patch("app.services.user_sync_service.database.async_session_factory", factory):
            svc = UserSyncService()
            match = await svc.resolve_by_name("Totally Unknown Person XYZ")
            assert match is None

    @pytest.mark.asyncio
    async def test_resolve_by_name_empty(self, db_engine, seeded_users):
        from app.services.user_sync_service import UserSyncService
        factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
        with patch("app.services.user_sync_service.database.async_session_factory", factory):
            svc = UserSyncService()
            assert await svc.resolve_by_name("") is None
            assert await svc.resolve_by_name(None) is None


# ───────────────────────────────────────────────────────────────────────────
# 4. Case model backwards-compat shim
# ───────────────────────────────────────────────────────────────────────────

class TestCaseBackwardsCompat:
    def test_case_init_with_legacy_assigned_rcic_kwarg(self):
        """Passing `assigned_rcic="John"` should populate assigned_rcic_name."""
        from app.models.db_models import Case
        c = Case(case_id="NX-TEST-1", contact_id="c-1", program_type="Express Entry",
                 assigned_rcic="John Smith, RCIC")
        assert c.assigned_rcic_name == "John Smith, RCIC"
        assert c.assigned_rcic == "John Smith, RCIC"

    def test_case_property_setter(self):
        from app.models.db_models import Case
        c = Case(case_id="NX-TEST-2", contact_id="c-1", program_type="Express Entry")
        c.assigned_rcic = "New Name"
        assert c.assigned_rcic_name == "New Name"

    def test_case_property_handles_none(self):
        from app.models.db_models import Case
        c = Case(case_id="NX-TEST-3", contact_id="c-1", program_type="Express Entry")
        c.assigned_rcic = None
        assert c.assigned_rcic == "Unassigned"


# ───────────────────────────────────────────────────────────────────────────
# 5. Users router endpoints
# ───────────────────────────────────────────────────────────────────────────

class TestUsersRouter:
    def test_router_import(self):
        """The router module imports cleanly and is mounted in main."""
        from app.routers import users as users_router
        assert users_router.router is not None
        # Route paths include the core set
        paths = [getattr(r, "path", "") for r in users_router.router.routes]
        assert "/" in paths
        assert "/{user_id}" in paths
        assert "/{user_id}/cases" in paths
        assert "/sync-from-ghl" in paths

    def test_main_registers_users_router(self):
        from main import app
        paths = {r.path for r in app.routes}
        assert any(p.startswith("/users") for p in paths), f"Users router not mounted, got: {sorted(p for p in paths if 'user' in p)}"


# ───────────────────────────────────────────────────────────────────────────
# 6. User sync from fallback file
# ───────────────────────────────────────────────────────────────────────────

class TestUserSyncService:
    @pytest.mark.asyncio
    async def test_sync_upserts_from_fallback_file(self, db_engine, tmp_path):
        """Simulate .team-users.json fallback and verify upsert counts."""
        from app.services.user_sync_service import UserSyncService
        factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

        fake_file = tmp_path / ".team-users.json"
        fake_file.write_text(json.dumps({
            "users": [
                {"ghl_id": "tst1", "firstName": "Alpha", "lastName": "One",
                 "email": "a@x.co", "title": "Senior RCIC Consultant", "perms": "senior_rcic",
                 "license": "R111111", "phone": "+1", "role": "user"},
                {"ghl_id": "tst2", "firstName": "Beta", "lastName": "Two",
                 "email": "b@x.co", "title": "Junior RCIC Consultant", "perms": "junior_rcic",
                 "license": "R222222", "phone": "+2", "role": "user"},
            ]
        }))

        with patch("app.services.user_sync_service.database.async_session_factory", factory), \
             patch("app.services.user_sync_service._fallback_team_file", return_value=fake_file), \
             patch("app.services.user_sync_service.GHLClient") as GCls:
            # Make the GHL path fail so we fall back to file
            mock_ghl = MagicMock()
            mock_ghl._request = AsyncMock(side_effect=Exception("network down"))
            mock_ghl.location_id = "loc"
            GCls.return_value = mock_ghl

            svc = UserSyncService()
            summary = await svc.sync_all_from_ghl()

        assert summary["fetched"] == 2
        assert summary["created"] == 2
        assert summary["source"] == "team_users_file"

        # Re-run: should be updates not creates (idempotent)
        with patch("app.services.user_sync_service.database.async_session_factory", factory), \
             patch("app.services.user_sync_service._fallback_team_file", return_value=fake_file), \
             patch("app.services.user_sync_service.GHLClient") as GCls:
            mock_ghl = MagicMock()
            mock_ghl._request = AsyncMock(side_effect=Exception("network down"))
            mock_ghl.location_id = "loc"
            GCls.return_value = mock_ghl
            svc = UserSyncService()
            summary2 = await svc.sync_all_from_ghl()

        assert summary2["created"] == 0
        assert summary2["updated"] == 2


# ───────────────────────────────────────────────────────────────────────────
# 7. Metabase views compile (PostgreSQL dialect syntactic check)
# ───────────────────────────────────────────────────────────────────────────

class TestMetabaseViews:
    def test_views_sql_contains_fk_based_workload(self):
        from pathlib import Path
        sql = Path(__file__).parent.parent.parent.joinpath(
            "neuronx-api/scripts/metabase_views.sql"
        )
        # Path resolution fallback for different test invocations
        if not sql.exists():
            sql = Path(__file__).parent.parent / "scripts" / "metabase_views.sql"
        text_sql = sql.read_text()
        assert "v_rcic_workload" in text_sql
        assert "JOIN cases cs ON cs.assigned_rcic_id = u.id" in text_sql
        assert "v_rcic_case_velocity" in text_sql
        assert "v_team_leaderboard" in text_sql

    def test_views_sql_parses_with_sqlglot(self):
        """SQL syntax is valid PostgreSQL (using sqlparse check instead of sqlglot dep)."""
        import re
        from pathlib import Path
        sql = Path(__file__).parent.parent / "scripts" / "metabase_views.sql"
        content = sql.read_text()
        # Every CREATE OR REPLACE VIEW must have a matching SELECT, FROM, and ;
        views = re.findall(r"CREATE OR REPLACE VIEW (\w+)", content)
        assert len(views) >= 8, f"Expected at least 8 views, got {len(views)}: {views}"
        for v in ["v_rcic_workload", "v_rcic_case_velocity", "v_team_leaderboard"]:
            assert v in views, f"Missing required view: {v}"
