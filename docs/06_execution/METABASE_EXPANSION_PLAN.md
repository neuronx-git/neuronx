# Metabase Expansion Plan — Staff Performance + Case Analytics

**Status:** 10 views live across 3 dashboards. Plan: add 8 new views + 2 new dashboards for staff performance + case document analytics.

## Current state (10 views, 3 dashboards)

**Dashboard 1: Pipeline Health** (id 8)
- v_pipeline_funnel
- v_lead_sources
- v_conversion_funnel

**Dashboard 2: Case Status** (id 9)
- v_case_stages
- v_rcic_workload
- v_doc_progress
- v_revenue

**Dashboard 3: Activity Timeline** (id 10)
- v_daily_activity
- v_recent_activities
- v_stage_transitions

## Proposed additions (8 new views + 2 dashboards)

### Dashboard 4: Staff Performance (NEW)

| View | Purpose | Unblocked by |
|---|---|---|
| `v_rcic_case_velocity` | Avg days each RCIC spends per stage | Current data (activities.metadata_json has updated_by) |
| `v_rcic_revenue_trend` | Monthly revenue per RCIC (line chart) | `v_rcic_workload` — extend with time dim |
| `v_rcic_approval_rate` | Approval rate per RCIC | Already available via `v_rcic_workload` |
| `v_rcic_utilization` | Active cases per RCIC vs capacity (needs `users` table with `max_concurrent_cases`) | **BLOCKED** — requires `users` table FK migration |
| `v_rcic_sla_breaches` | Cases where doc_deadline exceeded per RCIC | Current data |
| `v_team_leaderboard` | Monthly top performer (revenue + approval + speed) | Requires `users` table |

### Dashboard 5: Case Document Analytics (NEW — blocked until `documents` table exists)

| View | Purpose |
|---|---|
| `v_doc_checklist_progress` | Per case: received/required with document types listed |
| `v_missing_documents_by_stage` | Aggregate: what's blocking cases at each stage |
| `v_doc_upload_velocity` | Upload volume over time, trend by program |

### Example SQL (ready to execute after `users` + `documents` tables exist)

```sql
-- v_rcic_case_velocity
CREATE OR REPLACE VIEW v_rcic_case_velocity AS
SELECT
    (metadata_json ->> 'updated_by') AS rcic,
    (metadata_json ->> 'old_stage') AS from_stage,
    (metadata_json ->> 'new_stage') AS to_stage,
    COUNT(*) AS transitions,
    ROUND(AVG(EXTRACT(EPOCH FROM (
        created_at - LAG(created_at) OVER (
            PARTITION BY metadata_json->>'case_id' ORDER BY created_at
        )
    )) / 86400)::numeric, 1) AS avg_days_in_prev_stage
FROM activities
WHERE activity_type = 'stage_changed'
GROUP BY rcic, from_stage, to_stage;

-- v_rcic_sla_breaches
CREATE OR REPLACE VIEW v_rcic_sla_breaches AS
SELECT
    assigned_rcic,
    COUNT(*) FILTER (WHERE doc_deadline < NOW() AND docs_received < docs_required) AS active_breaches,
    COUNT(*) FILTER (WHERE doc_deadline < NOW() AND docs_received >= docs_required) AS breached_but_recovered,
    ROUND(AVG(docs_received::float / NULLIF(docs_required, 0) * 100), 1) AS avg_doc_completeness
FROM cases
WHERE stage NOT IN ('closed', 'decision')
GROUP BY assigned_rcic;

-- v_team_leaderboard (monthly)
CREATE OR REPLACE VIEW v_team_leaderboard AS
WITH monthly_stats AS (
    SELECT
        assigned_rcic,
        DATE_TRUNC('month', closed_at) AS month,
        COUNT(*) FILTER (WHERE ircc_decision = 'Approved') AS approved,
        COUNT(*) FILTER (WHERE ircc_decision = 'Refused') AS refused,
        COALESCE(SUM(retainer_value), 0) AS revenue,
        ROUND(AVG(EXTRACT(EPOCH FROM (closed_at - created_at)) / 86400)::numeric, 1) AS avg_days_to_close
    FROM cases
    WHERE closed_at IS NOT NULL
    GROUP BY assigned_rcic, DATE_TRUNC('month', closed_at)
)
SELECT
    month, assigned_rcic, approved, refused, revenue, avg_days_to_close,
    ROUND(100.0 * approved::numeric / NULLIF(approved + refused, 0), 1) AS approval_rate_pct,
    RANK() OVER (PARTITION BY month ORDER BY revenue DESC) AS rev_rank,
    RANK() OVER (PARTITION BY month ORDER BY approved DESC, avg_days_to_close ASC) AS perf_rank
FROM monthly_stats;
```

## Deployment

Once tables exist:
1. Add SQL to `neuronx-api/scripts/metabase_views.sql` (10 existing + 8 new = 18 total)
2. Run: `curl -X POST https://neuronx-production-62f9.up.railway.app/admin/install-views -H "X-Admin-Key: ..."`
3. Run `neuronx-api/scripts/setup_metabase.py` to create Dashboard 4 & 5 with cards
4. Verify: visit Metabase dashboard/11 and /12
