-- Metabase Dashboard SQL Views
-- Run against NeuronX PostgreSQL to create materialized views for dashboards.
-- These views power 3 Metabase dashboards: Pipeline Health, Case Status, Activity Timeline.
--
-- Usage: psql $DATABASE_URL < scripts/metabase_views.sql
-- Or via API: POST /admin/install-views (requires X-Admin-Key header)

-- ═══════════════════════════════════════════════════════════════════════════
-- DASHBOARD 1: PIPELINE HEALTH
-- ═══════════════════════════════════════════════════════════════════════════

-- View: Intake pipeline funnel
CREATE OR REPLACE VIEW v_pipeline_funnel AS
SELECT
    o.stage_name,
    o.status,
    COUNT(*) AS count,
    COALESCE(SUM(o.monetary_value), 0) AS total_value,
    ROUND(AVG(o.monetary_value)::numeric, 2) AS avg_value
FROM opportunities o
GROUP BY o.stage_name, o.status
ORDER BY count DESC;

-- View: Lead source performance
CREATE OR REPLACE VIEW v_lead_sources AS
SELECT
    c.source,
    COUNT(*) AS total_leads,
    SUM(CASE WHEN c.readiness_score >= 70 THEN 1 ELSE 0 END) AS high_score_leads,
    ROUND(AVG(c.readiness_score)::numeric, 1) AS avg_score,
    SUM(CASE WHEN 'nx:retainer:signed' = ANY(c.tags) THEN 1 ELSE 0 END) AS converted
FROM contacts c
WHERE c.source != ''
GROUP BY c.source
ORDER BY total_leads DESC;

-- View: Conversion funnel (inquiry → booking → retainer)
CREATE OR REPLACE VIEW v_conversion_funnel AS
SELECT
    'Inquiries' AS stage,
    1 AS stage_order,
    COUNT(*) AS count
FROM contacts
UNION ALL
SELECT
    'Scored High (70+)',
    2,
    COUNT(*)
FROM contacts WHERE readiness_score >= 70
UNION ALL
SELECT
    'Consultations Booked',
    3,
    COUNT(*)
FROM activities WHERE activity_type = 'appointment_booked'
UNION ALL
SELECT
    'Retainers Signed',
    4,
    COUNT(*)
FROM activities WHERE activity_type = 'retainer_signed'
UNION ALL
SELECT
    'Cases Active',
    5,
    COUNT(*)
FROM cases WHERE stage != 'closed'
ORDER BY stage_order;

-- ═══════════════════════════════════════════════════════════════════════════
-- DASHBOARD 2: CASE STATUS
-- ═══════════════════════════════════════════════════════════════════════════

-- View: Case stage distribution
-- Grouped by user FK (typo-safe); still exposes the display name for legacy reports.
CREATE OR REPLACE VIEW v_case_stages AS
SELECT
    cs.stage,
    cs.program_type,
    cs.assigned_rcic_id,
    COALESCE(u.full_name, cs.assigned_rcic_name) AS assigned_rcic,
    COUNT(*) AS count,
    COALESCE(SUM(cs.retainer_value), 0) AS total_value,
    ROUND(AVG(EXTRACT(EPOCH FROM (COALESCE(cs.closed_at, NOW()) - cs.created_at)) / 86400)::numeric, 1) AS avg_days_in_pipeline
FROM cases cs
LEFT JOIN users u ON u.id = cs.assigned_rcic_id
GROUP BY cs.stage, cs.program_type, cs.assigned_rcic_id, u.full_name, cs.assigned_rcic_name
ORDER BY count DESC;

-- View: RCIC workload — FK-joined (no more typo-broken groupings)
CREATE OR REPLACE VIEW v_rcic_workload AS
SELECT
    u.id AS user_id,
    u.full_name AS assigned_rcic,
    u.role,
    u.is_active,
    COUNT(cs.*) FILTER (WHERE cs.stage != 'closed') AS active_cases,
    COUNT(cs.*) FILTER (WHERE cs.stage = 'closed' AND cs.ircc_decision = 'Approved') AS approved,
    COUNT(cs.*) FILTER (WHERE cs.stage = 'closed' AND cs.ircc_decision = 'Refused') AS refused,
    COUNT(cs.*) FILTER (WHERE cs.stage = 'closed') AS total_closed,
    COALESCE(SUM(cs.retainer_value), 0) AS total_revenue,
    ROUND(AVG(cs.docs_received::float / NULLIF(cs.docs_required, 0) * 100)::numeric, 1) AS avg_doc_completeness
FROM users u
LEFT JOIN cases cs ON cs.assigned_rcic_id = u.id
WHERE u.is_active = TRUE
GROUP BY u.id, u.full_name, u.role, u.is_active
ORDER BY active_cases DESC NULLS LAST;

-- View: Per-RCIC case velocity — avg days between stage transitions for CLOSED cases
CREATE OR REPLACE VIEW v_rcic_case_velocity AS
SELECT
    u.id AS user_id,
    u.full_name AS assigned_rcic,
    u.role,
    COUNT(cs.*) FILTER (WHERE cs.stage = 'closed') AS closed_cases,
    ROUND(
        AVG(EXTRACT(EPOCH FROM (cs.closed_at - cs.created_at)) / 86400)
        FILTER (WHERE cs.stage = 'closed')::numeric, 1
    ) AS avg_days_to_close,
    ROUND(
        AVG(EXTRACT(EPOCH FROM (cs.ircc_submission_date - cs.created_at)) / 86400)
        FILTER (WHERE cs.ircc_submission_date IS NOT NULL)::numeric, 1
    ) AS avg_days_to_submission
FROM users u
LEFT JOIN cases cs ON cs.assigned_rcic_id = u.id
WHERE u.is_active = TRUE
GROUP BY u.id, u.full_name, u.role
ORDER BY avg_days_to_close NULLS LAST;

-- View: Monthly team leaderboard — approvals + revenue per RCIC
CREATE OR REPLACE VIEW v_team_leaderboard AS
SELECT
    DATE_TRUNC('month', cs.closed_at) AS month,
    u.id AS user_id,
    u.full_name AS assigned_rcic,
    u.role,
    COUNT(cs.*) AS cases_closed,
    COUNT(cs.*) FILTER (WHERE cs.ircc_decision = 'Approved') AS approvals,
    COUNT(cs.*) FILTER (WHERE cs.ircc_decision = 'Refused')  AS refusals,
    CASE WHEN COUNT(cs.*) FILTER (WHERE cs.ircc_decision IN ('Approved', 'Refused')) > 0
        THEN ROUND(
            (COUNT(cs.*) FILTER (WHERE cs.ircc_decision = 'Approved')::numeric /
             COUNT(cs.*) FILTER (WHERE cs.ircc_decision IN ('Approved', 'Refused')) * 100), 1
        )
        ELSE NULL
    END AS approval_rate_pct,
    COALESCE(SUM(cs.retainer_value), 0) AS revenue
FROM users u
JOIN cases cs ON cs.assigned_rcic_id = u.id
WHERE cs.closed_at IS NOT NULL
GROUP BY DATE_TRUNC('month', cs.closed_at), u.id, u.full_name, u.role
ORDER BY month DESC, revenue DESC;

-- View: Document collection progress
CREATE OR REPLACE VIEW v_doc_progress AS
SELECT
    cs.case_id,
    c.first_name || ' ' || c.last_name AS client_name,
    cs.program_type,
    COALESCE(u.full_name, cs.assigned_rcic_name) AS assigned_rcic,
    cs.assigned_rcic_id,
    cs.docs_required,
    cs.docs_received,
    CASE WHEN cs.docs_required > 0
        THEN ROUND((cs.docs_received::float / cs.docs_required * 100)::numeric, 0)
        ELSE 0
    END AS pct_complete,
    cs.doc_deadline,
    cs.stage
FROM cases cs
JOIN contacts c ON cs.contact_id = c.id
LEFT JOIN users u ON u.id = cs.assigned_rcic_id
WHERE cs.stage NOT IN ('closed', 'decision')
ORDER BY pct_complete ASC;

-- View: Revenue summary
CREATE OR REPLACE VIEW v_revenue AS
SELECT
    cs.program_type,
    COUNT(*) AS case_count,
    COALESCE(SUM(cs.retainer_value), 0) AS total_revenue,
    ROUND(AVG(cs.retainer_value)::numeric, 2) AS avg_retainer,
    COUNT(*) FILTER (WHERE cs.ircc_decision = 'Approved') AS approved,
    COUNT(*) FILTER (WHERE cs.ircc_decision = 'Refused') AS refused,
    CASE WHEN COUNT(*) FILTER (WHERE cs.ircc_decision IN ('Approved', 'Refused')) > 0
        THEN ROUND(
            (COUNT(*) FILTER (WHERE cs.ircc_decision = 'Approved')::numeric /
            COUNT(*) FILTER (WHERE cs.ircc_decision IN ('Approved', 'Refused')) * 100), 1
        )
        ELSE NULL
    END AS approval_rate_pct
FROM cases cs
GROUP BY cs.program_type
ORDER BY total_revenue DESC;

-- ═══════════════════════════════════════════════════════════════════════════
-- DASHBOARD 3: ACTIVITY TIMELINE
-- ═══════════════════════════════════════════════════════════════════════════

-- View: Daily activity volume
CREATE OR REPLACE VIEW v_daily_activity AS
SELECT
    DATE(a.created_at) AS activity_date,
    a.activity_type,
    COUNT(*) AS count
FROM activities a
GROUP BY DATE(a.created_at), a.activity_type
ORDER BY activity_date DESC, count DESC;

-- View: Recent activities (last 30 days, enriched with contact name)
CREATE OR REPLACE VIEW v_recent_activities AS
SELECT
    a.id,
    a.created_at,
    a.activity_type,
    a.detail,
    c.first_name || ' ' || c.last_name AS client_name,
    c.program_interest,
    a.metadata_json
FROM activities a
JOIN contacts c ON a.contact_id = c.id
WHERE a.created_at > NOW() - INTERVAL '30 days'
ORDER BY a.created_at DESC;

-- View: Case stage transition timeline (from metadata)
CREATE OR REPLACE VIEW v_stage_transitions AS
SELECT
    a.created_at AS transition_date,
    a.metadata_json->>'case_id' AS case_id,
    a.metadata_json->>'old_stage' AS from_stage,
    a.metadata_json->>'new_stage' AS to_stage,
    a.metadata_json->>'updated_by' AS updated_by,
    c.first_name || ' ' || c.last_name AS client_name
FROM activities a
JOIN contacts c ON a.contact_id = c.id
WHERE a.activity_type = 'stage_changed'
ORDER BY a.created_at DESC;
