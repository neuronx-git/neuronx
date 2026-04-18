"""
One-off migration — backfill Case.assigned_rcic_id from the legacy string.

Usage:

    export DATABASE_URL=postgresql://...
    # 1. Apply the schema migration first:
    psql $DATABASE_URL < scripts/migrations/001_users_table_and_case_fk.sql
    # 2. Run this script (idempotent — safe to re-run):
    python scripts/migrate_rcic_strings_to_fks.py

Steps the script performs:
  1. Sync users from GHL (or fallback .team-users.json).
  2. For every `cases` row with a non-empty `assigned_rcic_name` and NULL
     `assigned_rcic_id`, fuzzy-match the string against the users table and
     set the FK.
  3. Print counts + list of unresolved names for manual review.

Exit code:
  0 if every case was linked or intentionally skipped
  1 if at least one case could not be resolved (unresolved names are
    printed so an operator can fix them manually)
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("migrate_rcic")


async def main() -> int:
    from app.database import init_db, is_db_configured, async_session_factory
    from app import database as db_module

    if not is_db_configured():
        log.error("DATABASE_URL not set — aborting")
        return 2

    await init_db()
    sf = db_module.async_session_factory
    assert sf is not None

    # Lazy imports — rely on env being set and DB initialised
    from sqlalchemy import select, update
    from app.models.db_models import Case, User
    from app.services.user_sync_service import UserSyncService

    # ── 1. Sync users ──────────────────────────────────────────────────────
    log.info("Syncing users from GHL …")
    svc = UserSyncService()
    summary = await svc.sync_all_from_ghl()
    log.info("User sync: %s", summary)

    # ── 2. Iterate cases needing backfill ──────────────────────────────────
    async with sf() as session:
        result = await session.execute(
            select(Case).where(Case.assigned_rcic_id.is_(None))
        )
        cases = result.scalars().all()

    log.info("Found %d cases without assigned_rcic_id", len(cases))

    resolved = 0
    skipped_blank = 0
    unresolved: list[tuple[str, str]] = []
    cache: dict[str, str | None] = {}

    for case in cases:
        name = (case.assigned_rcic_name or "").strip()
        if not name or name.lower() == "unassigned":
            skipped_blank += 1
            continue

        if name in cache:
            uid = cache[name]
        else:
            match = await svc.resolve_by_name(name)
            uid = match["id"] if match else None
            cache[name] = uid

        if not uid:
            unresolved.append((case.case_id, name))
            continue

        async with sf() as session:
            await session.execute(
                update(Case)
                .where(Case.case_id == case.case_id)
                .values(assigned_rcic_id=uid)
            )
            await session.commit()
        resolved += 1

    # ── 3. Report ──────────────────────────────────────────────────────────
    log.info("=" * 60)
    log.info("Backfill complete:")
    log.info("  Resolved:  %d", resolved)
    log.info("  Skipped (blank/unassigned): %d", skipped_blank)
    log.info("  Unresolved: %d", len(unresolved))
    if unresolved:
        log.warning("Unresolved case → rcic_name pairs (fix manually):")
        for cid, name in unresolved[:50]:
            log.warning("  %s  ←  %r", cid, name)
        log.warning("… add the missing person to GHL, re-run sync, then re-run this script.")
        return 1

    log.info("Verify with: SELECT COUNT(*) FROM cases WHERE assigned_rcic_id IS NULL;  -- expect 0 (or == skipped_blank)")
    return 0


if __name__ == "__main__":
    rc = asyncio.run(main())
    sys.exit(rc)
