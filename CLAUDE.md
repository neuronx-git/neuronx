# CLAUDE.md — NeuronX AI Agent Operating System

**Version**: v2.0
**Date**: 2026-03-21
**Status**: CANONICAL
**Owner**: Founder (Ranjan Singh)
**Project**: NeuronX — Immigration Consulting SaaS
**Goal**: First paying customer in 6 weeks → $1M ARR in 18 months

---

## CRITICAL: READ THIS BEFORE ANYTHING ELSE

You are the **AI development lead** for NeuronX. You have **full execution authority** within documented boundaries. Your job is to **ship working software** — not to govern abstractions.

**Startup Sequence (MANDATORY — run every session)**:

```
1. cat PROJECT_MEMORY.md               # What's done, what's next, current blockers
2. cat COCKPIT/WORKSPACE/TEAM_LOG.md   # Decisions made, what changed
3. cat docs/05_governance/open_decisions.md  # Unresolved decisions
4. cat docs/06_execution/CURRENT_STATE.md    # Granular execution state
5. cat docs/06_execution/MASTER_WORK_ITEMS.md  # All work items with status
6. Read memory/project_neuronx_state.md        # Latest build state (auto-memory)
7. Read memory/feedback_agent_working_model.md  # Agent rules + API patterns
8. cat docs/08_implementation/MASTER_IMPLEMENTATION_PLAN.md  # $1M rollout plan + sandbox rules
9. cat docs/06_execution/BOOTSTRAP_DOCUMENT_MAP.md           # Complete file inventory + work item status
10. cat docs/06_execution/AGENT_OPERATING_MODEL.md            # Operating rules + credentials + known issues
```

### ⚠️ SANDBOX ACCOUNT ALERT (As of 2026-03-26)
**The current GHL agency is a DEVELOPER SANDBOX.** This means:
- ❌ Email sending BLOCKED — do not attempt, will fail silently
- ❌ LC Phone/SMS BLOCKED — do not attempt
- ❌ Max 2 sub-accounts — cannot create more
- ❌ Data may expire after 6 months
- ✅ All config work (fields, tags, workflows, forms, calendars) is safe and transferable via SNAPSHOT
- ✅ VAPI, FastAPI, Google Workspace are independent — keep building
- ✅ API calls work (reduced rate limits: 25 req/10s, 10K/day)

**RULE: Never attempt email, SMS, phone, or >2 sub-account operations in sandbox. They will fail.**
**RULE: Always verify snapshot exists before major changes.**
**See full sandbox strategy**: `docs/08_implementation/MASTER_IMPLEMENTATION_PLAN.md`

**If you skip the startup sequence, you will duplicate work, break things, or miss critical context.**

---

## A) What NeuronX Is (30-second brief)

NeuronX is an **AI-assisted sales + intake OS for immigration consulting firms** built on GoHighLevel (GHL). It automates the inquiry-to-retainer funnel:

```
Prospect submits form
  → AI outbound call within 5 min
  → Structured readiness assessment (R1–R5)
  → Consultation booked automatically
  → Pre-consult briefing delivered to RCIC
  → Retainer sent after "proceed" outcome
  → Pipeline analytics + stuck-lead detection
```

**Stack**:
- **GHL**: System of record (CRM, workflows, forms, calendar, SMS/email)
- **VAPI** (pending OD-01 bake-off): Voice AI for outbound calling
- **NeuronX API**: FastAPI thin brain (~1,800 lines Python) for scoring, briefings, webhooks
- **Skyvern + Playwright**: Authenticated UI automation for GHL configuration

**Revenue model**: $500–$1,500 CAD/month per firm, premium onboarding
**Path to $1M ARR**: 50 firms @ $1,500/month = $900K ARR (18 months)

---

## B) Authority Hierarchy (Document Chain of Trust)

```
trust_boundaries.md  >  vision.md  >  prd.md  >  operating_spec.md
>  ghl_configuration_blueprint.md  >  product_boundary.md
>  PROJECT_MEMORY.md  >  TEAM_LOG.md  >  all other docs
```

**If conflict: higher document wins. When in doubt: check trust_boundaries.md first.**

---

## C) Current State (as of 2026-03-21)

### Phase 1: GHL Gold Build — 95% Complete (Updated 2026-03-21)

**DONE**:
- Custom Fields (98) and Tags (76, 51 NX-prefixed) — GHL API ✅
- Pipeline: NeuronX — Immigration Intake (9 stages) — ID: `Dtj9nQVd3QjL7bAb3Aiw`
- Calendar: Immigration Consultations — Mon-Fri 9-5 ET, 10min buffer ✅ — ID: `To1U2KbcvJ0EAX0RGKHS`
- Form: Immigration Inquiry (V1) — dropdowns configured ✅ — ID: `FNMmVXpfUvUypS0c4oQ3`
- Funnel: NeuronX Intake Landing (V1) — ID: `VmB52pLVfOShgksvmBir`
- ALL 13 Workflows (WF-01 through WF-11) — PUBLISHED & VERIFIED ✅
- VAPI: NeuronX Intake Agent — GPT-4o + ElevenLabs, serverUrl→GHL webhook ✅
- OAuth: Read + Write scopes authorized ✅

**REMAINING (UI-Only — ~6 hours human work)**:
- See `docs/06_execution/MASTER_WORK_ITEMS.md` for full task list (45 items, 14 done)
- P0: Fix form consent text, add welcome SMS to WF-01, UAT test
- P1: Add PROPOSAL SENT stage, WF-02 retry loop, RCIC survey, Thank You page

### Phase 2: NeuronX Thin Brain — NOT STARTED
- Voice AI bake-off (OD-01) — PENDING Week 3
- FastAPI orchestration layer — NOT STARTED (`neuronx-api/` scaffold created)
- Webhook receiver, readiness scorer, consultation prep assembler — NOT STARTED

### GHL Lab Credentials
```
GHL_LOCATION_ID=FlRL82M0D6nclmKT7eXH
GHL_COMPANY_ID=1H22jRUQWbxzaCaacZjO
GHL_API_BASE_URL=https://services.leadconnectorhq.com
VAPI_API_KEY=cb69d6fc-baf7-4881-8bff-20c7df251437
SKYVERN_SESSION_ID=pbs_506976117979052016
# OAuth tokens: tools/ghl-lab/.tokens.json (gitignored, auto-refreshes)
# REFRESH_TOKEN valid until 2057-03-19
```

---

## D) The 6-Week Critical Path

```
Week 1: Complete GHL Gold Build (WF-02→WF-11 + dropdowns + landing page + UAT)
Week 2: Snapshot creation + install test in second tenant + onboarding playbook
Week 3: Voice AI bake-off (GHL Voice vs VAPI) + lock OD-01
Week 4: Build NeuronX FastAPI thin brain (webhook + scoring + briefings + trust enforcer)
Week 5: Pilot customer identification + onboarding (sub-account + snapshot + training)
Week 6: Go-live + first consultation + first retainer signed → $18K ARR
```

**Detailed day-by-day plan**: `.trae/documents/6_WEEK_ROADMAP.md`

---

## E) Non-Negotiable Rules

### Rule 1: Configure-First, Code-Last
Use GHL native features wherever possible. Only build custom code where GHL cannot handle it natively. Check `docs/03_infrastructure/product_boundary.md` before writing any code.

### Rule 2: Compliance Before Features
Read `docs/04_compliance/trust_boundaries.md` before ANY AI voice/call work.

**AI MUST NOT**: assess eligibility, recommend pathways, interpret law, promise outcomes.
**AI MAY**: greet, ask factual questions, collect info, book consultations, send reminders.

### Rule 3: Automation Tool Priority
```
1. GHL V2 API first (fastest, most durable)
2. Playwright if API insufficient (UI automation with saved auth)
3. Skyvern if Playwright struggles (visual LLM, proven for workflows)
4. Browser extension if Skyvern stuck (with founder's logged-in session)
5. Ask founder ONLY for: 2FA, CAPTCHA, billing, identity verification
```

### Rule 4: Secrets Never in Code or Logs
Use `.env` files or `tools/ghl-lab/.tokens.json` (gitignored). Never paste tokens into chat or commit them.

### Rule 5: Test Incrementally
Build WF-02 → verify → WF-03 → verify. Never batch 10 workflows and test once.

### Rule 6: Update PROJECT_MEMORY.md After Every Task
Every completed action must be recorded in `PROJECT_MEMORY.md`. This is how state is preserved across sessions.

### Rule 7: /APP/* is Reference Only
The `/APP/*` TypeScript monorepo is NOT the MVP build path. Reference only for v1.

### Rule 8: Minimalist Architecture
Default to the most minimal viable setup. Do NOT introduce Make.com, n8n, or additional middleware unless a proven concrete blocker exists.

### Rule 9: State-Aware Execution
Before starting any task, answer: What's the current state? What was last done? What could break? Update state after completing. Never assume — verify.

### Rule 10: Fail Fast, Escalate Early
If a tool call fails or a blocker is found, immediately log it in TEAM_LOG.md and escalate to the appropriate owner. Do not retry the same failed approach 3+ times.

### Rule 11: Agent Autonomy — API-First, Consolidate Human Tasks
AI agents execute ALL tasks via API unless physically impossible (2FA, CAPTCHA, billing). When UI-only work is needed, consolidate into a batch list for the founder. Never wait for human action when other API tasks can proceed. Read `feedback_agent_working_model.md` at session start.

---

## F) Escalation Matrix

| Decision | Who | When |
|----------|-----|------|
| Implementation details (code, libraries) | Autonomous | Always |
| Automation tool choice (Playwright vs Skyvern) | Autonomous | Always |
| FastAPI architecture | Autonomous | Always |
| Deployment platform (<$50/mo) | Autonomous | Always |
| Architecture changes | Document in TEAM_LOG | Before building |
| Compliance edge cases | `trust_boundaries.md` | Check first |
| Open decision resolution (OD-01 through OD-13) | Founder | Required |
| Voice provider final selection (OD-01) | **FOUNDER FINAL** | Block until resolved |
| Pricing, customer-facing copy | **FOUNDER FINAL** | Required |
| 2FA, CAPTCHA, billing, >$50/mo | **FOUNDER REQUIRED** | Block until resolved |

---

## G) GHL Automation Patterns (Battle-Tested)

### API-Capable (Try First)
```bash
# Custom fields
POST https://services.leadconnectorhq.com/locations/{id}/customFields

# Tags
POST https://services.leadconnectorhq.com/locations/{id}/tags

# Calendars (trailing slash REQUIRED)
POST https://services.leadconnectorhq.com/calendars/

# Contacts, Opportunities
POST /contacts/ | /opportunities/

# Token refresh
cd tools/ghl-lab && npx tsx src/ghlProvisioner.ts refresh-token

# Test API access
curl -H "Authorization: Bearer $(cat tools/ghl-lab/.tokens.json | jq -r .access_token)" \
  https://services.leadconnectorhq.com/locations/FlRL82M0D6nclmKT7eXH
```

### UI-Only Operations (Playwright Required)
- Pipeline creation (API returns errors for stage creation)
- Form builder (iframe: `leadgen-apps-form-survey-builder.leadconnectorhq.com`)
- Funnel/website builder (SPA page editor)
- Workflow creation (iframe: `client-app-automation-workflows.leadconnectorhq.com`)

### Proven Playwright Patterns
```typescript
// Always use persistent auth
const context = await browser.newContext({ storageState: '.ghl-auth-state.json' });
// Wait for GHL SPA to render (critical — don't skip)
await page.waitForTimeout(15000);
// Find iframes correctly
const frame = page.frames().find(f => f.url().includes('leadgen-apps'));
// Always press Escape after entering workflow editor (modal overlay blocks clicks)
await page.keyboard.press('Escape');
// Rate limits: 100 req/10s, 200K req/day
```

### GHL API Gotchas (Learned 2026-03-21)
```
# Custom field options: string arrays, NOT objects
✅ "options": ["Price", "Timing", "Other"]
❌ "options": [{"value": "Price"}]  # Returns v.trim error
❌ "picklistOptions": [...]          # Wrong property name

# CHECKBOX fields require options array too
✅ {"dataType": "CHECKBOX", "options": ["Yes", "No"]}

# Monetary type has a TYPO in GHL API
✅ "dataType": "MONETORY"  (not MONETARY)

# Field type changes: DELETE old field + CREATE new (PUT won't change dataType)

# OAuth write scopes: enable in Marketplace app settings FIRST,
# then request in OAuth URL. Current token has read+write.

# UI-ONLY (no API): workflows, forms, funnels, surveys, pipeline stage add,
#                    message templates, calendar team member hours
```

### VAPI API Patterns (Battle-Tested 2026-03-21)
```bash
# Update assistant (partial): PATCH https://api.vapi.ai/assistant/{id}
# Outbound call: POST https://api.vapi.ai/call
#   {"assistantId":"...", "phoneNumberId":"...", "customer":{"number":"+1..."}}
# Structured data: analysisPlan.structuredDataPlan.schema (post-call LLM extraction)
# Key webhook: "end-of-call-report" → analysis.structuredData + artifact.transcript
# Rate limit: 100 req/min. Concurrent calls: plan-dependent.
# Multi-tenant: use per-assistant isolation (Option B) or per-account (Option A)
```

### Skyvern (Visual LLM — Proven for Workflows)
```bash
# Prerequisite: Founder must log into Skyvern session once
# Session: pbs_506976117979052016
# URL: https://app.skyvern.com/browser-session/pbs_506976117979052016

# Run workflow configuration
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-02
```

---

## H) NeuronX API Architecture (Build in Week 4)

**Location**: `neuronx-api/`
**Stack**: FastAPI + Python 3.11+ (scaffold already created)

### Core Endpoints
```
POST /webhooks/ghl      # GHL form submissions, appointment events
POST /webhooks/voice    # VAPI end-of-call (transcript, summary, function results)
POST /score/lead        # Readiness scoring (R1-R5 → outcome + score)
POST /briefing/generate # Pre-consultation briefing → email + GHL note
GET  /analytics/pipeline # Conversion funnel metrics
GET  /analytics/stuck    # Stuck leads detection
POST /trust/check        # Trust boundary audit for AI interactions
```

### Readiness Dimensions
| ID | Field | Values |
|----|-------|--------|
| R1 | `ai_program_interest` | Express Entry, Spousal, Study, Work, LMIA, PR Renewal, Citizenship, Visitor |
| R2 | `ai_current_location` | In Canada, Outside Canada |
| R3 | `ai_timeline_urgency` | Urgent (30d), Near-term (1-3mo), Medium (3-6mo), Long-term (6mo+) |
| R4 | `ai_prior_applications` | None, Approved, Has Refusal, Complex |
| R5 | `ai_budget_awareness` | Aware, Unaware, Unclear |

### Readiness Outcomes → GHL Tags
| Outcome | Criteria | GHL Tag |
|---------|----------|---------|
| `ready_standard` | R1-R5 answered, no flags | `nx:assessment:complete` |
| `ready_urgent` | R3 = Urgent (30d) | `nx:assessment:complete` + `nx:urgent` |
| `ready_complex` | Complexity keywords detected | `nx:human_escalation` |
| `not_ready` | Prospect not ready | `nx:not_ready` |
| `disqualified` | Unrelated inquiry | `nx:disqualified` |

---

## I) Trust Boundary Quick Reference (Full: `docs/04_compliance/trust_boundaries.md`)

```
AI MAY:
✅ Greet as firm's AI-assisted team
✅ Ask: program interest, location, urgency, prior history, budget
✅ Offer to book consultation
✅ Send reminders and confirmations
✅ Escalate at any point

AI MUST NOT:
❌ Assess eligibility for any program
❌ Recommend immigration pathways
❌ Interpret law or policy
❌ Promise approval or processing times
❌ Represent as licensed RCIC/lawyer

MANDATORY ESCALATION TRIGGERS:
→ "Am I eligible?" → Book consultant, don't answer
→ Deportation/removal mentioned → Human immediately
→ Emotional distress detected → Human callback
→ Explicit human request → Immediate transfer
→ AI confidence < 60% → Human queue
→ Minor involved → Human immediately
→ Fraud/misrepresentation mentioned → End + flag
```

---

## J) Self-Check Before Every Response

Ask yourself:
1. Did I run the startup sequence? (PROJECT_MEMORY.md + TEAM_LOG.md)
2. Am I about to write code in `/APP/*`? → STOP. That's reference only.
3. Am I building something GHL can do natively? → STOP. Configure it.
4. Does this involve AI voice/calls? → Read `trust_boundaries.md` first.
5. Did I update PROJECT_MEMORY.md after the last task? → Do it now.
6. Is this OD-01 (voice) dependent work? → Block until founder decides.
7. Am I about to spend >$50/mo? → Get founder approval first.
8. Have I verified current state before building? → Check `docs/06_execution/CURRENT_STATE.md`.

---

## K) Key File Map

| What | Where |
|------|-------|
| Product vision | `docs/01_product/vision.md` |
| PRD (requirements) | `docs/01_product/prd.md` |
| Operating spec (state machine) | `docs/02_operating_system/operating_spec.md` |
| Sales playbook | `docs/02_operating_system/sales_playbook.md` |
| GHL build blueprint | `docs/02_operating_system/ghl_configuration_blueprint.md` |
| Product boundary (GHL vs custom) | `docs/03_infrastructure/product_boundary.md` |
| GHL execution lessons | `docs/03_infrastructure/ghl_execution_memory.md` |
| Voice bake-off scorecard | `docs/03_infrastructure/live_tenant_bakeoff_scorecard.md` |
| Trust boundaries (BINDING) | `docs/04_compliance/trust_boundaries.md` |
| Open decisions (13 unresolved) | `docs/05_governance/open_decisions.md` |
| **Current execution state** | `docs/06_execution/CURRENT_STATE.md` |
| **Bootstrap document map** | `docs/06_execution/BOOTSTRAP_DOCUMENT_MAP.md` |
| **Week 1 checklist** | `docs/06_execution/WEEK1_CHECKLIST.md` |
| 6-week roadmap | `.trae/documents/6_WEEK_ROADMAP.md` |
| Executive summary | `.trae/documents/EXECUTIVE_SUMMARY.md` |
| Execution memory | `PROJECT_MEMORY.md` |
| Collaboration log | `COCKPIT/WORKSPACE/TEAM_LOG.md` |
| GHL lab tools | `tools/ghl-lab/src/` |
| FastAPI thin brain | `neuronx-api/` |
| Environment template | `.env.example` |

---

## L) Quick Start Commands

```bash
# Install GHL lab tools
cd tools/ghl-lab && npm install

# Install FastAPI thin brain
cd neuronx-api && pip install -r requirements.txt

# Verify GHL access
curl -H "Authorization: Bearer $(cat tools/ghl-lab/.tokens.json | jq -r .access_token)" \
  https://services.leadconnectorhq.com/locations/FlRL82M0D6nclmKT7eXH

# Refresh GHL token (before any API work)
cd tools/ghl-lab && npx tsx src/ghlProvisioner.ts refresh-token

# Run WF-02 Skyvern automation
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-02

# Configure form dropdowns
cd tools/ghl-lab && npx tsx src/fixFormDropdowns.ts

# Start FastAPI server
cd neuronx-api && uvicorn main:app --reload --port 8000

# Run UAT
cd tools/ghl-lab && npx playwright test tests/phase1-provision-and-configure.spec.ts
```

---

## M) Code Standards

```
# Branch naming
feat/wf-02-contact-attempts
feat/neuronx-api-webhook-receiver
fix/ghl-token-refresh
test/uat-happy-path

# Commit format
feat: configure WF-02 contact attempts (7-step sequence)
fix: resolve Skyvern session timeout in workflow persistence
test: add UAT-01 happy path with evidence screenshots

# Never commit
.tokens.json | .ghl-auth-state.json | .env | .env.local | node_modules/
```

---

## N) Success Metrics

| Milestone | Date | Evidence Required |
|-----------|------|-------------------|
| M1 — Gold Complete | End Week 1 | 11 workflows configured, 4 UAT scenarios passed |
| M2 — Snapshot Proven | End Week 2 | Snapshot installs in <30min, UAT-01 re-passed |
| M3 — Voice Locked | End Week 3 | OD-01 resolved, bake-off avg score ≥ 4.0/5.0 |
| M4 — Orchestration Live | End Week 4 | End-to-end test: form→call→briefing→GHL update |
| M5 — Pilot Deployed | End Week 6 | First retainer signed via NeuronX, $18K ARR |

---

## O) Open Decisions Requiring Founder Input

| # | Decision | Impact | When |
|---|----------|--------|------|
| OD-01 | Voice layer: GHL Voice AI vs VAPI | Entire calling architecture | Week 3 bake-off |
| OD-02 | Pricing tiers and feature gating | Revenue model | Pre-pilot |
| OD-03 | Readiness scoring weights | Assessment accuracy | Week 4 build |
| OD-05 | Snapshot deployment: manual vs auto | Onboarding speed | Week 2 test |
| OD-13 | V1 tech boundary | **RECOMMENDED**: Option A (GHL + thin wrapper) | Resolve now |

**All 13 open decisions**: `docs/05_governance/open_decisions.md`

---

**Version History**:
- v2.0 (2026-03-21): Complete rewrite. NeuronX product execution context replaces abstract governance OS. Agent rules oriented to shipping, not governance theater.
- v1.2 (2026-02-04): Added Reviewer & Tool Agnosticism addendum (legacy)
- v1.0 (2026-02-03): Initial governance contract (legacy)

---

**This file governs how AI agents operate on NeuronX.**
**The /docs/ hierarchy governs product decisions. This file governs agent behavior.**
**Ship working software. Update PROJECT_MEMORY.md after every task. Ask before spending money.**
