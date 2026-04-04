# NeuronX Team Log — Single Collaboration Surface

**Purpose**: The ONLY place for brainstorming, decisions, progress updates, questions, and review notes.
**Rule**: ALL coordination goes here. No random markdown files in project root or COCKPIT/.
**Format**: Newest entries at TOP. Include timestamp, actor, and category tag.

---

## Log Categories
- `[DECISION]` — A decision was made (include rationale)
- `[PROGRESS]` — Work completed (include evidence/IDs)
- `[BLOCKER]` — Something is blocking work (include owner and resolution path)
- `[QUESTION]` — Needs answer from another party
- `[ESCALATION]` — Requires founder input
- `[INSIGHT]` — New technical lesson learned
- `[UAT]` — Test result

---

## 2026-04-04 — Case Processing Pipeline Foundation + Production Wiring

**[PROGRESS]** — Claude | 2026-04-04

### Production API Live
- NeuronX API deployed to Railway: `https://neuronx-production-62f9.up.railway.app`
- All endpoints verified live: /health, /score/lead, /score/form, /documents/checklist
- VAPI `serverUrl` updated to Railway endpoint (was pointing to GHL webhook)

### Case Processing Pipeline — Fields + Tags Created
- **20 custom fields** created via GHL API (case_id, ircc_receipt_number, case_program_type, etc.)
- **13 tags** created via GHL API (nx:case:onboarding through nx:case:overdue)
- Full spec: `docs/06_execution/CASE_PROCESSING_PIPELINE.md`
- **Remaining (UI-only)**: Pipeline stage creation, workflow builder (9 WF-CP workflows)

### Document Generation — Live in Production
- `POST /documents/checklist` — 8 program-specific IRCC document checklists
- `POST /documents/assessment` — Assessment reports from GHL contact data
- 32 tests passing

### Sales Scripts — Complete
- 7 call scripts: `docs/02_operating_system/SALES_SCRIPTS.md`
- Covers: inbound, AI (VAPI), follow-up, pre-consult, consultation 5-phase, retainer close, referral

### E2E Architecture — Locked
- 100% white-label: GHL + ERPNext + FastAPI + Next.js + Metabase + Documenso
- No Docketwise, no Wagepoint, no non-white-labelable tools
- Full doc: `docs/03_infrastructure/E2E_PLATFORM_ARCHITECTURE.md`

---

## 2026-04-01 — Strategic Architecture Decisions + Full Build Session

**[DECISION]** — Ranjan + Claude | 2026-04-01

### Scoring: Multi-Source (VAPI + Form Fallback)
- Added `POST /score/form` endpoint — preliminary scoring from form data (R1-R3 only, max 48/100)
- VAPI call upgrades to full score (R1-R5, 0-100). If VAPI fails, form score becomes final.
- 27/27 tests passing.

### Deployment: Railway Confirmed
- Vercel rejected — serverless cold starts (30s+) will timeout webhooks
- Railway: always-on, no cold starts, $5-20/mo, native Python support

### Odoo: REJECTED
- Full ERP overlap with GHL (80%+), 2-4 week integration, maintenance burden
- No production-grade Canadian immigration module exists
- Violates Rule 8 (minimalist architecture)

### Open-Source Stack: Phased Approach (doc: `docs/03_infrastructure/OPEN_SOURCE_STACK.md`)
- **Phase 1**: Docxtemplater (doc gen), Metabase (analytics), Next.js (website + portal)
- **Phase 2**: Documenso (e-sign), Plausible (analytics)
- **Rejected**: Odoo, Nextcloud, n8n/Make, SuiteCRM

### Task 2.14: WF-11 Nurture Templates
- 8 program-specific templates generated: `tools/ghl-lab/templates/nurture/`
- Programs: Express Entry, Spousal, Work Permit, Study Permit, LMIA, PR Renewal, Citizenship, Visitor
- Founder implements in WF-11 workflow builder

### Block 2D: NX-WF Sales Workflows
- 6 workflow content drafts: `tools/ghl-lab/templates/nx-sales/NX-WF-CONTENT.md`
- NX-WF-01 (lead alert) through NX-WF-06 (win-back)
- Build in production account after sandbox migration

---

## 2026-04-01 — FastAPI Thin Brain: Production-Ready Build

**[PROGRESS]** — Claude | 2026-04-01

### NeuronX API (`neuronx-api/`) — Built & Tested

Took the scaffold from Mar 21 and built it into a working system:

**What was done:**
1. **GHL Client** — OAuth token auto-reads from `tools/ghl-lab/.tokens.json`, proper custom field format, all CRUD ops
2. **VAPI Webhook** — Full handler for all VAPI event types (function-call, end-of-call-report, status-update). Aligned with real VAPI payload structure
3. **Scoring Service** — 0-100 scale aligned with WF-04B thresholds (>=70 high, 40-69 med, <40 low). Produces correct `nx:score:high/med/low` tags
4. **Briefing Service** — Proper HTML email output with NeuronX theme, plain text fallback, R1-R5 table, flag alerts, compliance reminder
5. **Trust Service** — Escalation patterns + AI violation detection (unchanged, already solid)
6. **Tests** — 24/24 passing, 0 warnings. Covers scoring, trust, webhooks, function calls
7. **Deployment** — Dockerfile, Procfile, .env.example, DEPLOY.md (Railway/Render/Fly.io)

**Data flow:**
```
VAPI call ends → POST /webhooks/voice → extract R1-R5 → score → update GHL (fields + tags) → WF-04B routes
```

**Files changed**: `main.py`, `config.py`, `models/readiness.py`, `routers/webhooks.py`, `routers/scoring.py`, `services/ghl_client.py`, `services/scoring_service.py`, `services/briefing_service.py`

**New files**: `tests/test_webhooks.py`, `.env.example`, `Dockerfile`, `Procfile`, `.gitignore`, `DEPLOY.md`

**Remaining**: Deploy to Railway/Render (needs account setup) → set as VAPI serverUrl → integration test

---

## 2026-04-01 — Block 2B Complete: All 11 Email Templates Unified & Saved

**[PROGRESS]** — Claude + Ranjan | 2026-04-01

### Email Templates: Unified Theme Applied (All 11 ✅)

All 11 GHL email templates updated with unified NeuronX/VMC design theme:
- VMC Red `#E8380D` primary, Green `#16a34a` success, Dark `#1a1a1a` neutral
- Inter font, 600px card, 8px radius, consistent footer with unsubscribe link

**Templates saved by Ranjan in GHL UI (Marketing → Emails → Code view)**:

| # | GHL Template | File |
|---|---|---|
| 1 | VMC-inquiry-received | 01-inquiry-received.html |
| 2 | VMC-consultation-confirmed | 02-consultation-confirmed.html |
| 3 | VMC-consultation-reminder | 03-consultation-reminder.html |
| 4 | VMC-noshow-recovery | 04-noshow-recovery.html |
| 5 | VMC-retainer-proposal | 05-retainer-proposal.html |
| 6 | VMC-pipeda-acknowledgement | 06-pipeda-acknowledgement.html |
| 7 | VMC-monthly-nurture-base | 07-monthly-nurture.html |
| 8 | VMC-complex-case-alert | 08-complex-case-alert.html |
| 9 | VMC-pipeda-deletion-confirmation | 09-pipeda-deletion.html |
| 10 | VMC-retainer-followup-7day | 10-retainer-followup.html |
| 11 | VMC-winback-nurture-30day | 11-winback-nurture.html |

**HTML source**: `/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/templates/themed/`

**Pending (UI-only)**:
- Delete 4 archived test templates in GHL: `Marketing → Emails → Archived → delete`
- Task 2.14: WF-11 program-specific nurture branches (8 programs) — workflow builder UI

---

## 2026-03-23 — Web Architecture Decision

**[DECISION]** — Ranjan Singh + Claude | 2026-03-23

### Web Presence: Two-Layer Architecture LOCKED

After research into Framer API capabilities, top SaaS stacks, and NeuronX scalability requirements, the following architecture is now CANONICAL and documented in `docs/03_infrastructure/product_boundary.md` Section 9.

**Layer 1 — GHL Native (inside snapshot)**
- All intake/conversion assets: landing page, thank you page, appointment page, surveys
- Must stay in GHL to auto-deploy with snapshot — zero friction guarantee
- Rule: intake funnel triggers GHL automation → stays in GHL, always

**Layer 2 — Next.js + Tailwind + Framer Motion (outside snapshot)**
- Full marketing websites: home, services, team, blog, case studies
- Stack: `next@14`, `tailwindcss`, `framer-motion`, `shadcn/ui`, `sanity`, Vercel
- Claude builds 100% of code autonomously — no UI work for founder
- VMC site = master template — clone + customize per client in ~10 min
- Sanity CMS = clients edit own content, no webmaster dependency

**GHL Integration confirmed zero-friction:**
- GHL form iframe → WF-01 fires natively ✅
- GHL calendar iframe → WF-05 fires natively ✅

**White-label upsell unlocked:**
- Core NeuronX: $500–1,500/mo (GHL snapshot)
- Premium Website Add-On: +$300–500/mo (Next.js, Claude deploys per client)

**Why NOT Framer for client sites:**
- Framer has zero public API — Claude cannot control it programmatically
- Next.js = same stack as Vercel/Linear/Stripe = 10/10 quality
- Vercel CLI = fully automated deployment, $0 hosting

**Build order:**
1. Week 1: VMC intake funnel — GHL native (current)
2. Week 2: VMC full website — Next.js (master template)
3. Week 3: NeuronX marketing site — Next.js
4. Week 4+: Each client = template clone + deploy

---

## 2026-03-21 — Session Start

### [PROGRESS] 2026-03-21 — AI Agent: Startup Configuration Complete

**Actor**: AI Agent (Claude Code)
**Scope**: Project-wide agent rules + execution state setup

**Completed**:
- Rewrote `CLAUDE.md` v2.0 — NeuronX-focused agent operating system (replaced legacy governance OS)
- Created `COCKPIT/WORKSPACE/TEAM_LOG.md` (this file) — single collaboration surface
- Created `docs/06_execution/CURRENT_STATE.md` — granular execution state tracker
- Created `docs/06_execution/WEEK1_CHECKLIST.md` — day-by-day Week 1 tasks
- Created `neuronx-api/` — FastAPI thin brain scaffold (Week 4 build)
- Created `.env.example` — environment variable template
- Created `docs/07_agent_rules/AI_CODING_BEST_PRACTICES.md` — AI agent best practices
- Updated `docs/05_governance/open_decisions.md` — added recommendations for all 13 ODs
- Populated agent memory files at `~/.claude/projects/.../memory/`

**Audit Findings**:
- GHL Gold Build: 60% complete (WF-01 done, WF-02-11 blocked on Skyvern login)
- Vision, PRD, operating spec: WORLD-CLASS — no changes needed
- Trust boundaries: Solid — BINDING for all AI work
- `/APP/*` codebase: Reference only, NOT the MVP path
- Missing: neuronx-api/, .env.example, execution state docs, agent memory

**Next Action**: Founder to log into Skyvern session `pbs_506976117979052016` to unblock WF-02 to WF-11

---

### [DECISION] 2026-03-21 — OD-13 Recommended Resolution

**Actor**: AI Agent (Claude Code)
**Decision**: V1 Tech Boundary
**Recommendation**: **Option A — GHL + NeuronX thin wrapper (~1,800 lines Python/FastAPI)**
**Rationale**:
- Gets to market faster (days vs weeks of full backend setup)
- Lower risk (fewer moving parts)
- Aligns with configure-first principle
- `/APP/*` TypeScript monorepo can be salvaged selectively for v1.5+
**Status**: RECOMMENDED (awaiting founder confirmation)

---

### [DECISION] 2026-03-21 — OD-01 Recommended Path

**Actor**: AI Agent (Claude Code)
**Decision**: Voice Layer Selection
**Recommendation**: Run bake-off Week 3 per scorecard in `docs/03_infrastructure/live_tenant_bakeoff_scorecard.md`
**Current lean**: VAPI (function calling for structured R1-R5 extraction, tenant isolation)
**Rationale**: VAPI's function calling schema allows structured JSON data extraction from calls, critical for reliable readiness scoring without NLP post-processing
**Status**: UNRESOLVED — requires live bake-off + founder final decision

---

### [BLOCKER] 2026-03-21 — WF-02 to WF-11 Blocked

**Actor**: AI Agent
**Blocker**: Skyvern persistent browser session requires founder login
**Session URL**: https://app.skyvern.com/browser-session/pbs_506976117979052016
**Impact**: Cannot configure 10 workflows until unblocked
**ETA After Unblock**: 2-4 hours automated via Skyvern orchestrator
**Owner**: Founder
**Resolution**: Founder logs into Skyvern session (one-time, ~30 min)

---

### [ESCALATION] 2026-03-21 — Awaiting Founder Decisions

**Actor**: AI Agent
**Pending**:
1. **Skyvern login** — unblocks WF-02 to WF-11 (30 min, this week)
2. **OD-13 confirmation** — V1 tech boundary (choose Option A or B)
3. **OD-01 bake-off scheduling** — voice AI selection (schedule for Week 3)
4. **Pilot customer identification** — needed by Week 5 (2 candidates minimum)

---

## 2026-03-17 — Skyvern Automation Breakthrough

### [PROGRESS] 2026-03-17 — Skyvern Successfully Configured WF-01

**Actor**: Previous AI session
**Achievement**: Skyvern Cloud Visual LLM successfully automated WF-01 workflow configuration AND verified persistence after reload
**Impact**: UNLOCKED — complex GHL UI automation is now possible
**Rule Update**: AUTHENTICATED_UI_AUTOMATION_RULE now applies to all SaaS tools

---

## 2026-03-13 — Documentation Canon Finalized

### [PROGRESS] 2026-03-13 — Canonical Docs v3.0 Complete

**Actor**: Previous session (Trae AI)
**Completed**:
- `vision.md` v3.0 — CANONICAL
- `prd.md` v3.0 — CANONICAL
- All `/docs/*` production-ready

**Status**: No changes needed to canonical docs. Vision and PRD are world-class.

---

## TEMPLATE FOR NEW ENTRIES

```markdown
### [CATEGORY] YYYY-MM-DD — Short description

**Actor**: [AI Agent | Founder | Trae AI]
**Details**: ...
**Evidence**: [IDs, screenshots, links]
**Next Action**: ...
```

---

**Last Updated**: 2026-03-21
**Maintained By**: All agents — update after every meaningful action
