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

## Case Processing — PIPELINE BUILT, WORKFLOWS PENDING

20 fields + 13 tags created via API. Pipeline #2 created in GHL UI (9 stages).
9 case processing workflows (WF-CP-01→09) NOT yet built (specs at docs/06_execution/CASE_PROCESSING_PIPELINE.md).

## Content — ALL DONE

11 email templates, 8 nurture templates (now in WF-11 as inline content), 6 NX-WF drafts, 7 sales scripts.
.docx templates: retainer agreement + assessment report (neuronx-api/templates/).

## NOT BUILT

WF-CP workflows (case processing), additional forms (onboarding, outcome, satisfaction), production account, Metabase, Next.js, ERPNext.
