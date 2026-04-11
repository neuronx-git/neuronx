# NeuronX Current Execution State

**Version**: 3.0
**Date**: 2026-04-04 (Updated end of session)
**Source of Truth**: This file + PROJECT_MEMORY.md + TEAM_LOG.md

---

## GHL Gold Build — COMPLETE (API-Verified + UI-Built 2026-04-04)

| Asset | Count | Status |
|-------|-------|--------|
| Custom Fields | 140 (incl. 20 case processing) | ✅ |
| Tags | 104 (77 nx-prefixed, 13 case processing, nx:not_ready added) | ✅ |
| Pipeline #1: Immigration Intake | 1 pipeline, 10 stages, colors + smart tags | ✅ |
| Pipeline #2: Case Processing | 1 pipeline, 9 stages, colors + smart tags | ✅ BUILT 2026-04-04 |
| NeuronX Sales Pipeline | 1 pipeline, 9 stages, colors | ✅ BUILT 2026-04-04 (NeuronX sub-account) |
| Workflows | 15 — all published | ✅ |
| WF-11 Nurture Branches | 9 branches (8 programs + default), dual triggers | ✅ BUILT 2026-04-04 |
| Calendars | 3 VMC + 1 NeuronX (Free Assessment, Paid Consult, Strategy, Product Demo) | ✅ |
| Forms | 1 (Immigration Inquiry V1) | ✅ |
| Email Templates | 11 (unified VMC theme) | ✅ |
| VAPI Voice Agent | 1 (wired to Railway, structuredDataPlan configured) | ✅ |

### Pipeline Smart Tags (2026-04-04)

**Intake Pipeline**:
- Stale (7+ days) — yellow — no activity in 7 days
- High Value — green — opportunity > $5,000
- Lost — red — stage = LOST
- Retained — green — stage = RETAINED
- New Lead (pre-built) — fresh leads ≤3 days
- Hot Deal (pre-built) — high-value this week
- Unassigned Deal (pre-built) — no owner

**Case Processing Pipeline**:
- Stale Case (14+ days) — orange — no activity 14 days
- Processing — stage = PROCESSING
- Approved — green — stage = DECISION RECEIVED
- New Case (pre-built) — ≤3 days old
- Unassigned (pre-built) — no owner

## NeuronX API — LIVE (Railway)

**URL**: `https://neuronx-production-62f9.up.railway.app`
**Tests**: 39/39 passing | **Endpoints**: 17
**Config-driven**: scoring.yaml, programs.yaml, trust.yaml (edit YAML → push → auto-deploy)

### VAPI Structured Data Extraction — CONFIGURED (2026-04-04)
- R1-R5 extracted as structured JSON after every call
- summaryPlan configured for compliance-safe summaries

## Case Processing — COMPLETE (Pipeline + 9 Workflows)

20 fields + 13 tags created via API. Pipeline #2 created in GHL UI (9 stages).
9 case processing workflows (WF-CP-01→09) ALL BUILT AND PUBLISHED ✅ (2026-04-05)

| Workflow | Trigger | Status |
|----------|---------|--------|
| WF-CP-01 | nx:retainer:signed | ✅ Published |
| WF-CP-02 | nx:case:docs_pending | ✅ Published |
| WF-CP-03 | nx:case:docs_complete | ✅ Published |
| WF-CP-04 | nx:case:under_review | ✅ Published |
| WF-CP-05 | nx:case:submitted | ✅ Published |
| WF-CP-06 | nx:case:processing | ✅ Published |
| WF-CP-07 | nx:case:rfi | ✅ Published |
| WF-CP-08 | nx:case:decision (IF/ELSE approved/refused) | ✅ Published |
| WF-CP-09 | nx:case:closed | ✅ Published |

## Content — ALL DONE

11 email templates, 8 nurture templates (now in WF-11 as inline content), 6 NX-WF drafts, 7 sales scripts.
.docx templates: retainer agreement + assessment report (neuronx-api/templates/).

## INFRASTRUCTURE — LIVE

| Service | URL | Status |
|---------|-----|--------|
| NeuronX API | neuronx-production-62f9.up.railway.app | ✅ 33+ endpoints, 78 tests |
| PostgreSQL | postgres.railway.internal | ✅ 6 tables, connected |
| Metabase | metabase-production-1846.up.railway.app | ✅ 5 dashboards, demo data seeded |
| Typebot Builder | builder-production-6784.up.railway.app | ✅ Form editor (16 groups, 30 vars) |
| Typebot Viewer | viewer-production-366c.up.railway.app | ⚠️ Blank page — web component not loading (API works, data OK) |

## Chrome Extension — BUILT (needs icons + deploy)

| File | Status |
|------|--------|
| manifest.json | ✅ Valid v3 |
| popup.html/js | ✅ Search fixed (was hardcoded) |
| content.js | ✅ XSS fixed (was innerHTML) |
| background.js | ✅ API routing |
| icons/ | ✅ 3 PNGs generated |

## AUDIT COMPLETED (2026-04-11)

- **Product Audit**: docs/06_execution/PRODUCT_AUDIT_2026_04_11.md (overall 7.1/10)
- **Competitor Analysis**: docs/06_execution/COMPETITOR_ANALYSIS_2026_04_11.md (6 competitors analyzed)
- **Form Migration Strategy**: docs/06_execution/TYPEBOT_MIGRATION_STRATEGY.md
- **Improvement Backlog**: 24 items across P0-P3 priorities

## NOT BUILT

Production GHL account ($97 upgrade), Documenso deployment, Next.js portal, daily briefing endpoint, operator work queue.
