# NeuronX — Bootstrap Document Map

**Version**: 1.0
**Date**: 2026-04-04
**Purpose**: Complete inventory of all project docs. Read this + startup sequence to bootstrap any new session.

---

## MANDATORY STARTUP (Every Session)

| # | File | What You Learn |
|---|------|----------------|
| 1 | `PROJECT_MEMORY.md` | What's done, what's next, session summaries, blockers |
| 2 | `COCKPIT/WORKSPACE/TEAM_LOG.md` | Decisions made, what changed |
| 3 | `docs/05_governance/open_decisions.md` | Unresolved decisions (OD-01 through OD-13) |
| 4 | `docs/06_execution/CURRENT_STATE.md` | Granular build status |
| 5 | `docs/08_implementation/MASTER_IMPLEMENTATION_PLAN.md` | $1M rollout plan + sandbox rules |
| 6 | `memory/project_neuronx_state.md` | Latest build state (auto-memory) |
| 7 | `memory/feedback_agent_working_model.md` | Agent rules + API patterns |

---

## PRODUCT CANON (Source of Truth — Higher doc wins)

| Priority | File | What It Governs |
|----------|------|-----------------|
| 1 | `docs/04_compliance/trust_boundaries.md` | **OVERRIDES ALL** — what AI may/must not do |
| 2 | `docs/01_product/vision.md` | Product direction, target market, philosophy |
| 3 | `docs/01_product/prd.md` | Requirements, API contracts, onboarding spec |
| 4 | `docs/02_operating_system/operating_spec.md` | State machine, workflow logic, business rules |
| 5 | `docs/02_operating_system/ghl_configuration_blueprint.md` | GHL field/tag/workflow/form specification |
| 6 | `docs/03_infrastructure/product_boundary.md` | What goes in GHL vs custom code |

---

## EXECUTION & TRACKING

| File | What It Tracks |
|------|---------------|
| `docs/06_execution/CURRENT_STATE.md` | Granular build status (pipelines, workflows, API, content) |
| `docs/06_execution/MASTER_WORK_ITEMS.md` | All 45 work items with P0-P3 priority + status (27/45 done) |
| `docs/06_execution/MASTER_WORK_ITEMS_V2.md` | Updated work items (use alongside V1) |
| `docs/06_execution/WEEK1_CHECKLIST.md` | Day-by-day Week 1 tasks |
| `docs/06_execution/WORKFLOW_REFERENCE.md` | All 15 workflows: trigger→action→tag→stage maps |
| `docs/06_execution/CASE_PROCESSING_PIPELINE.md` | Pipeline #2 spec: 9 stages, 9 workflows, handoff logic |
| `docs/06_execution/COMPREHENSIVE_GAP_ANALYSIS.md` | Full gap analysis |
| `docs/06_execution/FOUNDER_BATCH_CHECKLIST.md` | Tasks requiring founder (manual/billing/2FA) |
| `docs/06_execution/SYSTEM_EMAIL_TEMPLATES.md` | Email template specs |
| `docs/06_execution/VMC_FUNNEL_COPY.md` | Marketing copy for VMC landing page |
| `docs/06_execution/DNS_SETUP_GUIDE.md` | DNS config for vmc.neuronx.co |

---

## INFRASTRUCTURE & ARCHITECTURE

| File | What It Covers |
|------|---------------|
| `docs/03_infrastructure/E2E_PLATFORM_ARCHITECTURE.md` | End-to-end technical architecture |
| `docs/03_infrastructure/PLATFORM_RESPONSIBILITY_MATRIX.md` | What lives where (GHL vs API vs VAPI vs open source) |
| `docs/03_infrastructure/OPEN_SOURCE_STACK.md` | Metabase, Documenso, Next.js, ERPNext decisions |
| `docs/03_infrastructure/ghl_capability_map.md` | GHL platform capabilities |
| `docs/03_infrastructure/capability_lock_audit.md` | GHL capability validation |
| `docs/03_infrastructure/ghl_execution_memory.md` | GHL API gotchas + proven patterns |
| `docs/03_infrastructure/live_tenant_bakeoff_scorecard.md` | Voice AI bake-off framework |
| `docs/03_infrastructure/browser_operator_architecture.md` | Skyvern/Playwright automation |
| `docs/03_infrastructure/manual_config_guide.md` | Manual GHL config steps |

---

## GTM & PRICING

| File | What It Covers |
|------|---------------|
| `docs/07_gtm/PRICING_STRATEGY.md` | 3 tiers: $299/$599/$1,199 CAD (OD-02 resolved) |
| `docs/07_gtm/BILLING_CONFIGURATION.md` | Stripe billing setup |
| `docs/08_gtm/GTM_STRATEGY.md` | Go-to-market plan |
| `docs/08_gtm/LEGALTECH_GTM_RESEARCH.md` | Legal tech market research |
| `docs/02_operating_system/sales_playbook.md` | Sales process + scripts |
| `docs/02_operating_system/SALES_SCRIPTS.md` | 7 sales call/email scripts |

---

## NEURONX API (FastAPI — Railway)

| File | What It Is |
|------|-----------|
| `neuronx-api/main.py` | FastAPI app entry — 17 endpoints |
| `neuronx-api/config/scoring.yaml` | Scoring rules (edit YAML → auto-deploy) |
| `neuronx-api/config/programs.yaml` | 8 immigration programs + IRCC forms |
| `neuronx-api/config/trust.yaml` | Trust/compliance rules |
| `neuronx-api/app/routers/` | webhooks, scoring, briefings, trust, documents, cases, analytics |
| `neuronx-api/app/services/` | ghl_client, scoring, briefing, case, analytics, trust, webhook_security |
| `neuronx-api/templates/` | .docx templates (retainer, assessment) |
| `neuronx-api/tests/` | 39 tests (scoring, trust, webhooks, documents, cases) |
| `neuronx-api/DEPLOY.md` | Railway deployment guide |
| `neuronx-api/Dockerfile` | Docker config |

---

## GHL LAB TOOLS

| File | What It Does |
|------|-------------|
| `tools/ghl-lab/src/ghlProvisioner.ts` | GHL API provisioner (fields, tags, calendars) |
| `tools/ghl-lab/src/ghlOauth.ts` | OAuth token management |
| `tools/ghl-lab/src/ghlV2.ts` | GHL V2 API client |
| `tools/ghl-lab/.tokens.json` | OAuth tokens (gitignored) |
| `tools/ghl-lab/.private-integration-token` | PIT token for users API (gitignored) |
| `tools/ghl-lab/templates/TEMPLATE_REGISTRY.md` | Template-to-workflow mapping |
| `tools/ghl-lab/templates/themed/` | 11 VMC-themed email HTML files |
| `tools/ghl-lab/templates/nurture/` | 8 program-specific nurture HTML files |
| `tools/ghl-lab/templates/nx-sales/` | NeuronX sales workflow content |

---

## AGENT MEMORY (Cross-Session Persistence)

| File | Type | What It Stores |
|------|------|---------------|
| `memory/MEMORY.md` | Index | Pointer to all memory files |
| `memory/user_ranjan_profile.md` | user | Founder profile, preferences |
| `memory/project_neuronx_state.md` | project | Current build state snapshot |
| `memory/feedback_coding_style.md` | feedback | Configure-first, minimalist, ship fast |
| `memory/feedback_agent_behavior.md` | feedback | State awareness, escalation, docs |
| `memory/feedback_agent_working_model.md` | feedback | Autonomous execution, API-first, GHL+VAPI SME |
| `memory/feedback_ghl_workflow_builder.md` | feedback | GHL AI lessons — build manually, avoid cascading |
| `memory/feedback_navigation_help.md` | feedback | Ask Ranjan for GHL navigation when stuck |
| `memory/feedback_agent_startup.md` | feedback | Mandatory startup protocol |
| `memory/project_architecture.md` | project | Architecture decisions |
| `memory/project_tag_registry.md` | project | Tag registry — who adds, who listens |
| `memory/reference_credentials.md` | reference | Where credentials live |

---

## STATE & TRACKING

| File | What It Is |
|------|-----------|
| `STATE/STATUS_LEDGER.md` | Status tracking ledger |
| `STATE/LAST_KNOWN_STATE.md` | Latest known system state |
| `COCKPIT/WORKSPACE/TEAM_LOG.md` | Decisions + collaboration log |
| `BACKLOG/000-backlog-master.md` | Master backlog |

---

## REFERENCE ONLY (Do Not Build From)

| Directory | What It Is |
|-----------|-----------|
| `/APP/*` | TypeScript monorepo — v1 reference only (OD-09/OD-13 resolved) |
| `/archive/*` | Historical docs — `/docs/` is authoritative |
| `/FOUNDATION/*` | Legacy governance docs (deleted from git, in archive) |
| `/GOVERNANCE/*` | Legacy governance (deleted from git) |
| `/AGENTS/*` | Legacy agent prompts (deleted from git) |

---

## COMPLETE WORK ITEM STATUS (Updated 2026-04-04)

### Tier 1: MVP — First Paying Customer

| # | Item | Status |
|---|------|--------|
| 1 | Pipeline #1: Immigration Intake (10 stages) | ✅ DONE + colors + 7 smart tags |
| 2 | Pipeline #2: Case Processing (9 stages) | ✅ DONE (2026-04-04) + colors + 5 smart tags |
| 3 | 15 Workflows (WF-01→WF-13) — all published | ✅ DONE |
| 4 | WF-11: 9 program nurture branches | ✅ DONE (2026-04-04) — dual triggers, inline email content |
| 5 | Custom Fields (140) | ✅ DONE |
| 6 | Tags (104, 77 nx-prefixed) | ✅ DONE |
| 7 | Form: Immigration Inquiry (V1) | ✅ DONE |
| 8 | Calendars (3 VMC + 1 NeuronX) | ✅ DONE |
| 9 | FastAPI on Railway (17 endpoints, 39 tests) | ✅ LIVE |
| 10 | VAPI Voice Agent (wired to Railway) | ✅ DONE |
| 11 | VAPI structuredDataPlan (R1-R5 extraction) | ✅ DONE (2026-04-04) |
| 12 | 11 email templates (VMC theme) | ✅ DONE |
| 13 | Config-driven YAML (scoring, programs, trust) | ✅ DONE (2026-04-04) |
| 14 | .docx templates (retainer + assessment) | ✅ DONE (2026-04-04) |
| 15 | 7 sales scripts | ✅ DONE |
| 16 | Document checklists (8 programs) | ✅ DONE |
| 17 | NeuronX Sales Pipeline (NeuronX sub-account) | ✅ DONE (2026-04-04) |
| 18 | Production GHL account | ❌ NOT DONE — sandbox |
| 19 | E2E UAT | ❌ NOT DONE — needs production |
| 20 | Snapshot v2 | ⏳ PENDING — take after this session |

### Tier 2: Essential (Within 2 Weeks of Pilot)

| # | Item | Status |
|---|------|--------|
| 21 | 9 Case Processing Workflows (WF-CP-01→09) | ❌ Specs written, GHL UI needed |
| 22 | Client Onboarding Questionnaire form | ❌ GHL UI |
| 23 | Document Upload form / Client Portal | ❌ GHL UI |
| 24 | Consultation Outcome form | ❌ GHL UI |
| 25 | Client Satisfaction Survey | ❌ GHL UI |
| 26 | NX-WF sales workflows (selling NeuronX) | ❌ Content drafted, production needed |
| 27 | Metabase analytics | ❌ Railway deploy |
| 28 | GHL → PostgreSQL data sync | ❌ Needed for Metabase |

### Tier 3: Important (Month 2-3)

| # | Item | Status |
|---|------|--------|
| 29 | Next.js marketing site (neuronx.co) | ❌ |
| 30 | Client portal (Next.js + Metabase embeds) | ❌ |
| 31 | Documenso e-signatures | ❌ |
| 32 | Commission calculation | ❌ |
| 33 | RCIC work queue / assignment | ❌ |

### Tier 4: Scale (Month 4-6)

| # | Item | Status |
|---|------|--------|
| 34 | ERPNext (HR/Payroll/Accounting) | ❌ |
| 35 | Multi-tenant snapshot automation | ❌ |
| 36 | IRCC form auto-fill | ❌ |
| 37 | Plausible analytics | ❌ |

---

## KEEP UPDATED

After every session, update these files:
1. `PROJECT_MEMORY.md` — add session summary
2. `docs/06_execution/CURRENT_STATE.md` — update build status
3. `memory/project_neuronx_state.md` — update memory snapshot
4. `docs/06_execution/MASTER_WORK_ITEMS.md` — mark items done
5. `docs/05_governance/open_decisions.md` — record any resolved ODs
