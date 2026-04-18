-- ════════════════════════════════════════════════════════════════════════════
-- Migration 001 — Users table + Case.assigned_rcic FK
-- Blocker #2 from GO_LIVE_ACTION_PLAN.md
-- ----------------------------------------------------------------------------
-- Replaces the typo-fragile `cases.assigned_rcic VARCHAR(100)` with a proper
-- foreign key to a `users` table synced from GHL.
--
-- SAFE TO RE-RUN: all statements use IF NOT EXISTS / IF EXISTS.
-- DOES NOT DROP the legacy string column — it is renamed to `assigned_rcic_name`
-- and kept as a denormalized display field for backwards compatibility.
--
-- Run order:
--   1. psql $DATABASE_URL < scripts/migrations/001_users_table_and_case_fk.sql
--   2. python scripts/migrate_rcic_strings_to_fks.py    # backfill FKs
--   3. Verify: SELECT COUNT(*) FROM cases WHERE assigned_rcic_id IS NULL;  -- expect 0
-- ════════════════════════════════════════════════════════════════════════════

BEGIN;

-- ── 1. users table ──────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id                    VARCHAR(50)  PRIMARY KEY,                -- GHL user ID
    email                 VARCHAR(255) NOT NULL,
    first_name            VARCHAR(100) NOT NULL DEFAULT '',
    last_name             VARCHAR(100) NOT NULL DEFAULT '',
    full_name             VARCHAR(200) NOT NULL DEFAULT '',
    phone                 VARCHAR(50)  NOT NULL DEFAULT '',
    role                  VARCHAR(30)  NOT NULL DEFAULT 'user',
    rcic_license          VARCHAR(20)  NOT NULL DEFAULT '',
    is_active             BOOLEAN      NOT NULL DEFAULT TRUE,
    max_concurrent_cases  INTEGER      NOT NULL DEFAULT 30,
    hire_date             TIMESTAMPTZ,
    ghl_user_id           VARCHAR(50)  NOT NULL,
    synced_at             TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_at            TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email       ON users (email);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_ghl_user_id ON users (ghl_user_id);
CREATE        INDEX IF NOT EXISTS ix_user_role         ON users (role);
CREATE        INDEX IF NOT EXISTS ix_user_active       ON users (is_active);

-- ── 2. cases: rename legacy column, add FK column ──────────────────────────
-- Rename only if the old column still exists and the new one does not.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'cases' AND column_name = 'assigned_rcic'
    ) AND NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'cases' AND column_name = 'assigned_rcic_name'
    ) THEN
        ALTER TABLE cases RENAME COLUMN assigned_rcic TO assigned_rcic_name;
    END IF;
END $$;

-- Ensure the denormalized name column exists even for fresh databases.
ALTER TABLE cases
    ADD COLUMN IF NOT EXISTS assigned_rcic_name VARCHAR(100) NOT NULL DEFAULT 'Unassigned';

-- New FK column — nullable during backfill window.
ALTER TABLE cases
    ADD COLUMN IF NOT EXISTS assigned_rcic_id VARCHAR(50);

-- Attach FK constraint idempotently.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints
        WHERE table_name = 'cases' AND constraint_name = 'fk_cases_assigned_rcic_id'
    ) THEN
        ALTER TABLE cases
            ADD CONSTRAINT fk_cases_assigned_rcic_id
            FOREIGN KEY (assigned_rcic_id) REFERENCES users (id)
            ON DELETE SET NULL;
    END IF;
END $$;

-- Indexes on the new / renamed columns.
CREATE INDEX IF NOT EXISTS ix_cases_assigned_rcic_id   ON cases (assigned_rcic_id);
CREATE INDEX IF NOT EXISTS ix_case_rcic_name           ON cases (assigned_rcic_name);

-- Drop the stale index on the pre-rename column if it still lingers.
DROP INDEX IF EXISTS ix_case_rcic;

COMMIT;

-- ── Post-migration sanity check (run manually) ─────────────────────────────
--   SELECT COUNT(*) AS users_count FROM users;
--   SELECT COUNT(*) FILTER (WHERE assigned_rcic_id IS NULL) AS unlinked_cases,
--          COUNT(*) FILTER (WHERE assigned_rcic_id IS NOT NULL) AS linked_cases
--   FROM cases;
