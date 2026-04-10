# NeuronX — Project Memory (Compact)

## Canon (Authority)

- `/docs/*` is authoritative; `/archive/*` is reference only.
- `docs/04_compliance/trust_boundaries.md` overrides all implementation choices.

## Current MVP Strategy

- Build Phase 1 entirely inside GoHighLevel (GHL) using the blueprint.
- Create one Gold GHL sub-account.
- Create Snapshot from Gold.
- Install snapshot into another sub-account.
- Run UAT and record evidence.
- Only after proven GHL gaps: implement NeuronX thin brain (webhooks + scoring + briefings + analytics).

## ⚠️ SANDBOX DISCOVERY (2026-03-26)

**CRITICAL**: The GHL agency is a **DEVELOPER SANDBOX** account, not a paid production account.
- Agency shows "Agency Pro — 100% discount applied forever" — this is how GHL labels sandbox
- Error confirmed: "Only 2 locations are allowed for this company, as this is a sandbox agency"
- Email sending blocked: "Email sending is blocked for sandbox agencies"
- Stripe unverified banner on Agency Dashboard
- LC Phone 500 errors traced to same root cause

**Impact**: All configuration work is SAFE and transferable via Snapshot. VAPI, FastAPI, Google Workspace are independent platforms unaffected by sandbox.

**Strategy**: Continue building in sandbox (Phase 0, Weeks 1-4), then migrate via snapshot to paid account ($297/mo with 30-day trial) in Week 5. See `docs/08_implementation/MASTER_IMPLEMENTATION_PLAN.md`.

**Deferred to Production**: Email sending, SMS, phone number purchase, A2P registration, SaaS mode, >2 sub-accounts, client billing.

**Snapshot Created**: 2026-03-26 ✅ (insurance backup of all Gold Build work)

**Pricing Decided (OD-02 RESOLVED)**: 3 tiers — Essentials $299, Professional $599, Scale $1,199 CAD/month. Billing via Stripe direct (not GHL SaaS Mode). See `docs/07_gtm/PRICING_STRATEGY.md` and `docs/07_gtm/BILLING_CONFIGURATION.md`.

**Open Source Enhancement Stack (Implement in logical order)**:
- Metabase (analytics dashboard) — P1
- Documenso (e-signatures for retainers) — P1
- Docxtemplater (auto-generate consultation prep packets) — P1
- Next.js + Vercel (neuronx.co website + client portal) — P1
- Plausible/Umami (privacy-friendly analytics) — P2
- Nextcloud (secure document portal) — P2

### Active Sub-Accounts (Sandbox — Max 2)
1. **NeuronX** (oZN1j4944EaIvXoI8rRA) — Main development account
2. **VMC Test** — Pilot client test account

## Architecture Direction (v1)

- GHL = system of record + workflow execution.
- NeuronX = orchestration/intelligence layer only.
- Prefer GHL native features first; use APIs only where durable.
- Use UI automation only where API is insufficient.
- Do not use `/APP/*` as the MVP build path (reference only).
- **Minimalist Architecture Rule**: The default architecture for v1 must be the most minimal viable setup (e.g., GHL + Vapi directly). Do not introduce third-party orchestration layers (Make.com, n8n) unless a concrete blocker is proven that the native platforms cannot solve cleanly.

## Open Decisions (must be resolved with evidence)

- OD-01 Voice layer selection (run live tenant bake-off).
- OD-05 Snapshot deployment process (manual vs partial automation).
- ~~OD-07 Analytics approach~~ → **RESOLVED** (2026-04-01): Metabase (open source) on Railway, embedded in Next.js client portal. See `docs/03_infrastructure/OPEN_SOURCE_STACK.md`.

See: `docs/05_governance/open_decisions.md`.

## FastAPI Thin Brain (2026-04-01)

**Status**: Built, tested (27/27), deployment-ready.
**Location**: `neuronx-api/`
**Deploy to**: Railway ($5-20/mo)

### Endpoints
| Endpoint | What | Status |
|----------|------|--------|
| `POST /webhooks/ghl` | GHL events (form, appointment, tags) | ✅ |
| `POST /webhooks/voice` | VAPI events (function-call, end-of-call, status) | ✅ |
| `POST /score/lead` | Full R1-R5 scoring (0-100, WF-04B aligned) | ✅ |
| `POST /score/form` | Preliminary form-based scoring (R1-R3 fallback) | ✅ |
| `POST /briefing/generate` | Pre-consultation briefing (HTML + plain text) | ✅ |
| `POST /trust/check` | Transcript compliance scan | ✅ |
| `GET /analytics/pipeline` | Funnel metrics (stubbed, Week 4) | ⚪ |
| `GET /analytics/stuck` | Stuck lead detection (stubbed, Week 4) | ⚪ |

### Open-Source Stack Decision (2026-04-01)
- **Odoo**: REJECTED (overlap with GHL, maintenance burden)
- **Approved Phase 1**: Docxtemplater, Metabase, Next.js+Vercel
- **Approved Phase 2**: Documenso, Plausible
- **Full doc**: `docs/03_infrastructure/OPEN_SOURCE_STACK.md`

### Block 2B: Email Templates (2026-04-01)
- 11/11 themed templates saved in GHL UI ✅
- Source: `tools/ghl-lab/templates/themed/`

### Task 2.14: Program Nurture Templates (2026-04-01)
- 8/8 program-specific nurture emails generated ✅
- Source: `tools/ghl-lab/templates/nurture/`
- Founder implements in WF-11 builder

### Block 2D: NeuronX Sales Workflows (2026-04-01)
- 6/6 NX-WF content drafts generated ✅
- Source: `tools/ghl-lab/templates/nx-sales/NX-WF-CONTENT.md`
- Build in production account post-sandbox

## Platform Mastery & Capability Storage
- **GHL**: System of record. Pipelines, workflows, smart lists, and payments are native.
- **Vapi**: Voice layer. Handles state machines, strict UPL guardrails, and structured JSON data extraction (via function calling). SaaS scaling is achieved via the Vapi Sub-Account API.
- **Make/n8n**: Orchestration layer. Catches Vapi end-of-call webhooks, parses JSON, and updates GHL Custom Fields. Also responsible for passing data to OpenAI for "Pre-Consultation Briefings".
- **Skyvern**: Authenticated UI automation layer. Used to provision and configure the above platforms when APIs are gated by billing or lack parity.

- Phase 1 Gold Build: **Blocks 1-6 COMPLETE** (structure created)
- Marketplace OAuth install flow is in use for sub-account access
- Current Gold lab sub-account:
  - Name: `NeuronX Test Lab`
  - Location ID: `FlRL82M0D6nclmKT7eXH`

### Live Artifacts (Gold Sub-Account)

| Artifact | ID | Method |
|---|---|---|
| Custom Fields (41) | various | API |
| Tags (21) | various | API |
| Pipeline: NeuronX — Immigration Intake | `Dtj9nQVd3QjL7bAb3Aiw` | Playwright |
| Calendar: Immigration Consultations | `To1U2KbcvJ0EAX0RGKHS` | API |
| Form: Immigration Inquiry (V1) | `FNMmVXpfUvUypS0c4oQ3` | Playwright |
| Funnel: NeuronX Intake Landing (V1) | `VmB52pLVfOShgksvmBir` | Playwright |
| Funnel Step: Immigration Inquiry | `a607c93d-9b58-4c8c-931b-19aca87aed9a` | Playwright |
| Workflows: WF-01 through WF-11 | see execution memory | Playwright |

### Automation Ceiling — UNLOCKED 2026-03-17

> **UPDATE:** Skyvern Cloud (Visual LLM) successfully automated workflow configuration and persistence verification on 2026-03-17.
> The previous "LOCKED" decision is now superseded by the Skyvern success.

**What automation CAN do (via Skyvern):**
- Navigate complex UI (Workflows, Builders)
- Configure Triggers and Actions
- Persist changes (Save/Publish)
- Verify persistence after reload

### AUTHENTICATED_UI_AUTOMATION_RULE (Permanent SaaS Rule)
Do not treat external SaaS tools (Vapi, ElevenLabs, Make, n8n, Twilio, etc.) as "manual by default."
GHL authenticated UI automation worked successfully via persisted session/state (Skyvern and Playwright). This pattern **MUST** be reused for all similar SaaS tools before declaring a task manual.

**The SaaS Automation Checklist:**
1. Is there a login session already available?
2. Can cookies/auth state be saved?
3. Can Skyvern reuse that session?
4. Can we automate after login?
*Only escalate to the founder if blocked by: unavailable credentials, 2FA/CAPTCHA, billing/payment confirmation, or legal/identity verification.*

### Skyvern Execution Mode (Active 2026-03-17)

Switched execution from Browser-Use (credits blocked) to **Skyvern Cloud**:
- **SDK**: `@skyvern/client` (using direct API fetch due to SDK issues)
- **Session**: Persistent session `pbs_506976117979052016`
- **Orchestrator**: `tools/ghl-lab/src/skyvern/skyvernOrchestrator.ts`
- **Skills**: `tools/ghl-lab/src/skills/workflowSkills.ts`

**Current Status:**
- **WF-01**: Configured & Verified (Trigger: Form Submitted, Action: SMS).
- **Next**: WF-02 through WF-11.

### Execution Knowledge

See: `docs/03_infrastructure/ghl_execution_memory.md`

Note: `README.md` still states "Build Status: Not started". Treat this as outdated.

## Agent Setup Completed (2026-03-21)

**Session**: AI Agent setup + audit + gap-fill
**What was done**:
- CLAUDE.md v2.0 — Complete rewrite as NeuronX agent OS (replaces legacy governance)
- COCKPIT/WORKSPACE/TEAM_LOG.md — Single collaboration surface created
- docs/06_execution/CURRENT_STATE.md — Granular build status tracker
- docs/06_execution/WEEK1_CHECKLIST.md — Day-by-day Week 1 tasks with Skyvern commands
- docs/07_agent_rules/AI_CODING_BEST_PRACTICES.md — AI agent behavior standards
- neuronx-api/ — FastAPI scaffold: webhook, scoring, briefing, trust, analytics endpoints
- neuronx-api/tests/ — Tests for scoring (5 cases) and trust boundary (6 cases)
- .env.example — All environment variables documented
- docs/05_governance/open_decisions.md v2.0 — AI recommendations for all 13 ODs
- docs/01_product/prd.md v3.1 — Added API contract, onboarding spec, build sequence
- .gitignore — Added neuronx-api/ and compliance log exclusions
- ~/.claude/.../memory/ — 6 agent memory files (user, project, feedback, reference)

## GHL Workflow Build — COMPLETE (2026-03-21)

**Session**: Ranjan (founder) as hands, Claude as brain — field-by-field guided configuration

### Workflow Status (All Published ✅)

| Workflow | ID | Status | Trigger | Key Actions |
|----------|-----|--------|---------|-------------|
| WF-01 | 99ce0aa7-... | Published ✅ | Form Submitted | SMS + adds nx:contacting:start |
| WF-02 | 43ecd109-... | Published ✅ | Tag: nx:contacting:start | 6-attempt retry loop over 48h → VAPI webhooks → If/Else exits → UNREACHABLE fallback |
| WF-03 | fb1215b4-... | Published ✅ | Tag: nx:contacted | Move to CONTACTING stage |
| WF-04 | 838f7c38-... | Published ✅ | Tag: nx:score:high | Move to CONSULT READY → SMS invite → nx:booking:invited |
| WF-04B | cc52cbeb-... | Published ✅ | Inbound Webhook (VAPI) | Map 11 fields → tags → Human Escalation Check → Lead Score Router |
| WF-04C | 5a1b58a3-... | Published ✅ | Contact Changed: No Answer/Voicemail | Wait → SMS recovery → nx:missed_call |
| WF-05 | 9af911d1-... | Published ✅ | Customer Booked Appointment | Confirmation SMS+Email → Wait 24h → Reminder SMS+Email |
| WF-06 | 5d0c1920-... | Published ✅ | Tag: nx:appointment:noshow | No-Show SMS+Email → Move to NURTURE |
| WF-07 | 83177830-... | Published ✅ | Tag: nx:consult:done | Move to CONSULT COMPLETED → Thank You SMS+Email → Internal Alert |
| WF-08 | (see GHL) | Published ✅ | Tag: nx:human_escalation | Email alert to Assigned User → nx:human:pending |
| WF-09 | 93b39b76-... | Published ✅ | Tag: nx:retainer:sent | Retainer Email → Wait 2d → Follow-Up SMS+Email |
| WF-10 | 25046474-... | Published ✅ | Tag: nx:retainer:signed | Move to RETAINED → Welcome SMS+Email |
| WF-11 | 7e0a17f4-... | Published ✅ | Tag: nx:score:low | Move to NURTURE → Nurture Email → Wait 30d → Monthly SMS |

### Tag Registry (Manually Added vs Auto)

| Tag | Added By | Triggers |
|-----|----------|---------|
| nx:contacting:start | WF-01 (auto) | WF-02 |
| nx:contacted | WF-04B (auto) | WF-03 |
| nx:contacting:attempt1 | WF-02 (auto) | - |
| nx:score:high | WF-04B (auto) | WF-04 |
| nx:score:med | WF-04B (auto) | - |
| nx:score:low | WF-04B (auto) | WF-11 |
| nx:human_escalation | WF-04B (auto) | WF-08 |
| nx:missed_call | WF-04C (auto) | - |
| nx:booking:invited | WF-04 (auto) | - |
| nx:appointment:noshow | Consultant (manual) | WF-06 |
| nx:consult:done | Consultant (manual) | WF-07 |
| nx:human:pending | WF-08 (auto) | - |
| nx:retainer:sent | Consultant (manual) | WF-09 |
| nx:retainer:signed | Consultant (manual) | WF-10 |

### VAPI Configuration
- Assistant ID: `289a9701-9199-4d03-9416-49d18bec2f69`
- Phone Number ID: `ea133993-7c18-4437-88a6-fa7a2d15efbe`
- Lead score scale: 0-100 (High ≥70, Medium ≥40, Low <40)
- WF-02 triggers outbound call via Custom Webhook → POST https://api.vapi.ai/call

### Tag Naming Notes (for Week 4 API cleanup)
- nx:consult:done (used) vs nx:consult:completed (planned) — standardize in API build
- nx:appointment:noshow (used) vs nx:no_show (planned) — standardize in API build

## Session Summary — 2026-04-04

### Completed This Session

| Item | What Was Done |
|------|--------------|
| Pipeline #2 (VMC) | Case Processing pipeline created — 9 stages (ONBOARDING → CASE CLOSED) with background tint colors + 5 smart tags ✅ |
| Pipeline #1 Smart Tags (VMC) | Intake pipeline colors + 7 smart tags (Stale 7d, High Value, Lost, Retained, New Lead, Hot Deal, Unassigned) ✅ |
| NeuronX Sales Pipeline | Created in NeuronX sub-account — 9 stages (Prospect → Active Client) with colors ✅ |
| WF-11 Gold Rebuild | Completely rebuilt from scratch manually — 9 flat parallel branches (Express Entry, Spousal, Work Permit, Study, LMIA, PR Renewal, Citizenship, Visitor Visa, Default) ✅ |
| WF-11 Dual Triggers | nx:score:low + nx:not_ready (new tag created) ✅ |
| WF-11 Email Content | All 9 branches have targeted program-specific email text with booking links, written inline (not templates) ✅ |
| WF-11 Published | Saved + Published ✅ |
| VAPI structuredDataPlan | R1-R5 JSON extraction configured — was MISSING before this session ✅ |
| VAPI summaryPlan | Compliance-safe summary configured ✅ |
| FastAPI Case Processing | Case management endpoints deployed to Railway (create, get, update, list, forms, timeline) ✅ |
| Config-Driven YAML | scoring.yaml, programs.yaml, trust.yaml — edit YAML, push, auto-deploy ✅ |
| .docx Templates | Retainer agreement + assessment report templates created (neuronx-api/templates/) ✅ |
| Platform Responsibility Matrix | docs/03_infrastructure/PLATFORM_RESPONSIBILITY_MATRIX.md — what lives where ✅ |
| Case Processing Architecture | docs/06_execution/CASE_PROCESSING_PIPELINE.md — E2E spec for Pipeline #2 ✅ |
| Tag nx:not_ready | Created in GHL for WF-11 trigger ✅ |

### Key Decisions Made (2026-04-04)
- **Metabase STAYS** — "Powered by Metabase" is fine for v1; Superset rejected (too technical for firm owners)
- **Managed everything** — Railway + Frappe Cloud + Vercel. Zero self-hosted servers. ~$600/mo total.
- **Case Processing = stage-based**, not program-based. 9 workflows for all programs. Program-specific content injected by API.
- **80/20 on IRCC forms**: Top 3 programs (Express Entry, Spousal, Work Permit) = 80% revenue → 19 forms mapped. Other 5 programs = manual.
- **GHL AI limitations confirmed**: Can't edit IF/ELSE conditions, creates duplicate cascading branches. Manual workflow building is more reliable.

### GHL AI Workflow Builder Lessons (2026-04-04)
- GHL AI creates cascading IF/ELSE (not parallel) — looks messy but functionally correct
- GHL AI cannot edit existing IF/ELSE segment conditions (temporarily disabled feature)
- GHL AI often creates duplicate Level 2/3 branches — delete manually from bottom up
- Best results: one focused prompt at a time, ≤4 branches per prompt
- "End Workflow" goals cause save errors if multiple exist — remove all goals, workflows stop naturally
- **Best approach**: Build branches MANUALLY (click + → If/Else → add 8 conditions). Then add email+wait per branch. Total: ~30 min vs hours of AI prompt wrestling.

### Current Status (2026-04-04)
- **15/15 Workflows PUBLISHED** ✅ (WF-11 rebuilt with 9 branches)
- **2 Pipelines in VMC** ✅ (Intake 10 stages + Case Processing 9 stages)
- **1 Pipeline in NeuronX** ✅ (Sales Pipeline 9 stages)
- **FastAPI**: 39/39 tests, 17 endpoints, config-driven YAML, LIVE on Railway
- **VAPI**: structuredDataPlan + summaryPlan configured
- **All API-capable work COMPLETE** — remaining work is GHL UI or production account

## Session Summary — 2026-04-05

### Completed This Session (Massive)

| Item | What Was Done |
|------|--------------|
| OD-01 RESOLVED | VAPI locked as voice provider (GHL Voice AI rejected) ✅ |
| Smart Questionnaire API | GET /cases/questionnaire/{program} — 8 programs with conditional fields ✅ |
| Case Emails Config | 11 case processing email templates in case_emails.yaml ✅ |
| PostgreSQL on Railway | 6 tables (contacts, opportunities, cases, activities, signatures, sync_log) ✅ |
| GHL → PostgreSQL Sync | POST /sync/full + GET /sync/status — dual sync (webhook + daily) ✅ |
| Documenso Integration | POST /signatures/send, /webhook, GET /status — retainer e-signing ✅ |
| IRCC Form Auto-Fill | POST /documents/ircc-fill + field mappings YAML — pypdf PDF filling ✅ |
| Document Service | docxtpl wrapper for retainer + assessment .docx generation ✅ |
| Metabase Deployed | Railway, connected to PostgreSQL, 5 unique-value dashboards ✅ |
| Demo Data | POST /demo/seed — 12 contacts, 8 cases, 28 activities for presentations ✅ |
| Government Sources | docs/09_domain_knowledge/GOVERNMENT_SOURCES.md — 50+ canada.ca URLs ✅ |
| WF-CP-01 through WF-CP-09 | ALL 9 case processing workflows built and published in GHL ✅ |
| Architecture Decisions | memory/project_architecture_decisions.md — permanent decision record ✅ |
| Bootstrap Doc Map | docs/06_execution/BOOTSTRAP_DOCUMENT_MAP.md — 100+ files inventoried ✅ |
| Metabase Cleanup | Removed 4 GHL-duplicate cards, added 4 unique immigration analytics ✅ |
| Tests | 59/59 passing (up from 43) ✅ |

### Key Decisions Made (2026-04-05)
- OD-01: VAPI locked (structured data extraction, already wired)
- Metabase: unique-value analytics ONLY (IRCC rates, time-in-stage, RCIC workload)
- GHL forms: conditional logic v2 supports dynamic fields (no Next.js for forms)
- Multi-tenant: GHL location_id = tenant_id, $297 plan, add column when firm #2 joins
- Case assignment: manual for v1 (round-robin Phase 2)
- Document collection: GHL Portal + email reply fallback

### Current Status (2026-04-05)
- **24/24 Workflows PUBLISHED** (15 intake + 9 case processing) ✅
- **29 API endpoints, 59 tests** ✅
- **3 Railway services** (NeuronX API + PostgreSQL + Metabase) ✅
- **ALL API-capable work COMPLETE**
- **ALL case processing workflows COMPLETE**

## Session Summary — 2026-04-05 (Massive Session)

### Infrastructure Deployed
- PostgreSQL on Railway (6 tables, connected to NeuronX API) ✅
- Metabase on Railway (5 unique dashboards, demo data seeded) ✅
- Typebot self-hosted on Railway (7 services, all features free) ✅
- Typebot form: 16 groups, 55 blocks, 8 program branches, file upload, webhook ✅

### Key Builds
- 9 case processing workflows (WF-CP-01→09) — all published in GHL ✅
- Chrome Extension (NeuronX RCIC Assistant) — IRCC portal auto-fill ✅
- 5 new client API endpoints (form-data, data-sheet, validate, copy-paste, search) ✅
- Typebot API mastery — discovered correct JSON format (items at block level, outgoingEdgeId on events)
- IRCC PDFs downloaded (IMM 0008, 5406, 5476, 5669) — IMM 5476 auto-fill tested ✅
- Government source citations (50+ canada.ca URLs) ✅
- GHL → PostgreSQL sync service ✅
- Documenso e-signature integration code ✅
- IRCC form auto-fill service (pypdf) ✅
- Demo data seeding endpoint ✅

### Key Decisions
- OD-01 RESOLVED: VAPI locked as voice provider
- Typebot wins over Formbricks (conversational UX, mid-flow API, FSL license)
- Typebot self-hosted > Cloud (all features free, $15/mo Railway)
- GHL replacement: NOT RECOMMENDED (no open-source covers >55%)
- GHL $97 plan sufficient for 2-3 customers (not $297)
- IRCC forms: mostly web-only now, generate Data Sheets for copy-paste
- Chrome extension: IRCC portal auto-fill (same approach as VisaFlo, Visto)

### Critical Typebot Learnings
- Start event MUST have outgoingEdgeId (root cause of blank page)
- items at block level for choice input (NOT inside options)
- PATCH groups + events separately (not together)
- Hardcode DATABASE_URL on Railway (not reference variables)
- Self-hosted deployment: Railway template → hardcode DB URL → works

### Stats
- Tests: 78/78 passing
- API endpoints: 33+
- GHL workflows: 24 published
- Typebot form: 16 groups, 55 blocks, 8 programs
- Railway services: 10 (NeuronX project: 3, Typebot project: 7)

### What's Next
1. **Upgrade GHL to $97 plan** → unlocks email/SMS/phone
2. **Install Chrome extension** → test on IRCC pages
3. **E2E UAT** → full lifecycle test
4. **Detailed product audit** → gaps, improvements, competitor analysis
5. **Take GHL Snapshot v3**

---

## Next Expected Milestone

**IMMEDIATE**: Verify WF-01 adds nx:contacting:start tag to complete the chain

1. **WF-01 verification**: Confirm trigger chain is complete
2. **End-to-end UAT**: Submit test form → verify full flow fires
3. **VAPI structured data**: Update assistant analysisSchema with 0-100 lead score
4. **Form Dropdowns**: Configure form options (see WEEK1_CHECKLIST.md)
5. **Landing Page**: Edit content (see WEEK1_CHECKLIST.md)
6. **Snapshot**: Create GHL snapshot (Week 2)
7. **UAT**: Run 4 scenarios (see WEEK1_CHECKLIST.md)
8. **M1**: Gold Complete milestone

**See detailed plan**: docs/06_execution/WEEK1_CHECKLIST.md

## Session Summary — 2026-03-23

### Completed This Session (8 items)

| Item | What Was Done |
|------|--------------|
| WF-02 | 6-attempt VAPI contact sequence built — retry loop over 48h, all If/Else exits, UNREACHABLE fallback — PUBLISHED ✅ |
| WF-12 | Score Med Handler — trigger nx:score:med, move to CONTACTING, SMS + Email + Internal Alert — PUBLISHED ✅ |
| WF-13 | PIPEDA Data Deletion Request — trigger tag, admin alert, contact acknowledgement email — PUBLISHED ✅ |
| P1-05 | RCIC Consultation Outcome Survey — 5 fields (outcome, program, retainer amount, notes, follow-up date) — PUBLISHED ✅ |
| P2-10 | WF-13 PIPEDA workflow complete — DONE ✅ |
| P2-14 | WF-11 nurture branches — 4 program-specific emails (EE, Spousal, Work, Study) + General — PUBLISHED ✅ |
| VAPI | System prompt updated — now branded as "Visa Master Canada" throughout ✅ |
| Tags | 86 total tags — 2 missing tags created (nx:call:attempt_1, nx:call:attempt_4) ✅ |

### Current Status (2026-03-23)
- **15/15 Workflows PUBLISHED** ✅
- **P0**: 4/5 done — only UAT test (P0-05) remaining
- **P1**: 15/15 COMPLETE ✅
- **P2**: 3/4 done — P2-06 (landing page) + P2-07 (dashboards) remaining
- **GHL Gold Build: ~99% complete**
- **Next**: P2-06 Landing Page VMC branding → P2-07 Dashboards → UAT → M1 GOLD COMPLETE

---

## Session Summary — 2026-03-22

**Pilot Client Confirmed**: Visa Master Canada (VMC) — immigration firm, Toronto
**Brand Kit Extracted**: Navy #1E3A5F | Red #DC2626 | Light Gray #F3F4F6

### Completed This Session (9 items)

| Item | What Was Done |
|------|--------------|
| P0-02 | Form consent placeholder text → "Visa Master Canada Immigration Services" |
| P0-03 | Welcome SMS added to WF-01 |
| P0-04 | Form button text → "Get Your Free Assessment" |
| P1-01 | PROPOSAL SENT pipeline stage added (between CONSULT COMPLETED and RETAINED) — pipeline now has 10 stages |
| P1-04 | WF-03 renamed to "WF-03 Contact Success Handler" |
| P1-06 | Thank You page built — custom HTML/CSS with VMC brand kit |
| P1-12 | AI disclaimer checkbox added to form — mapped to `ai_disclaimer_shown`, Required |
| P1-15 | WF-04B frozen — renamed to [v14-STABLE] before snapshot |
| P2-11 | "How did you hear about us?" dropdown added — 6 options, query key: `how_did_you_hear` |

**Calendar Booking URL confirmed**: https://api.leadconnectorhq.com/widget/booking/immigration-consultations

### Phase 1 Status After This Session
- MASTER_WORK_ITEMS: 22/45 DONE (was 14/45)
- P0 blockers resolved: 4/5 (only UAT test remaining)
- P1 critical items: 11/15 done
- **Next unblocked action**: Run UAT end-to-end test (P0-05) — needs real phone

---

## Session Summary — 2026-03-30

### Completed This Session

| Item | What Was Done |
|------|--------------|
| VMC Funnel | AI-generated immigration intake landing page built + published to `vmc.neuronx.co` ✅ |
| Funnel Domain | CNAME `vmc.neuronx.co → sites.ludicrous.cloud` verified + connected ✅ |
| Funnel Design | VMC brand (Red #E8380D, Inter font), 9-card 3×3 programs grid, form embedded inline ✅ |
| Nav links | All nav links connected (Book Consult → calendar, CTA → form scroll) ✅ |
| Old Users Deleted | 6 @visamastercanada.com users deleted (Ranjan, Alexandra, Priya, James, Sarah, Michael) ✅ |
| NeuronX Staff | 2 users created: Ranjan Singh (ranjan@neuronx.co, agency owner) + Alexandra Wong (team@neuronx.co, admin) ✅ |
| VMC Staff | 3 users created: Rajiv Mehta (rcic@neuronx.co, admin), Nina Patel (intake@neuronx.co, user), David Park (sales@neuronx.co, user) ✅ |
| VMC Calendars | 3 round_robin calendars correctly configured: Free Initial Assessment (15min, RCIC+Intake), Paid Consultation (30min, RCIC+Sales), Strategy Session Complex (60min, RCIC only, autoConfirm OFF) ✅ |
| NeuronX Calendars | Fixed: deleted 2 wrong "VMC —" calendars, renamed remaining → "NeuronX — Product Demo" (30min, FREE, round_robin, autoConfirm ON) ✅ |
| Block 2B Templates | 4 email templates created via API (2.10-2.13) + 5 SMS variants drafted (2.9) ✅ |
| Template HTML | Full HTML bodies saved to `tools/ghl-lab/templates/` for email builder import ✅ |
| Template Registry | `tools/ghl-lab/templates/TEMPLATE_REGISTRY.md` — complete mapping of all 11 templates to workflows ✅ |
| Template Metadata | All 11 templates PATCHED with subject lines, from name/email, preview text via API ✅ |
| Template Theme | Unified NeuronX/VMC themed HTML saved to `tools/ghl-lab/templates/themed/` (11 files) — needs UI import ⏳ |
| Test Templates | 4 test templates archived via API ✅ |
| Block 2C: WF Audit | All 15 workflows verified published via API, 64 nx: tags, 10 pipeline stages ✅ |
| Block 2C: WF Reference | `docs/06_execution/WORKFLOW_REFERENCE.md` — full trigger→action→tag→stage maps for all 15 WFs ✅ |
| Block 2C: PIPEDA Test | WF-13 tested via API — tag trigger fires, adds nx:pipeda:deletion_in_progress + nx:pipeda:acknowledged ✅ |
| PIT Token | New PIT token saved: `.private-integration-token` ✅ |

### VMC Staff (FlRL82M0D6nclmKT7eXH)
| ID | Name | Email | Role | assignedDataOnly |
|----|------|-------|------|-----------------|
| 6lpXO6Om18TVifpEl3Hj | Rajiv Mehta | rcic@neuronx.co | admin | No |
| VNzHAuGCGIE39c1T3qQP | Nina Patel | intake@neuronx.co | user | No |
| KUZ8AW403wRvdoUlqZIs | David Park | sales@neuronx.co | user | No |

### NeuronX Staff (oZN1j4944EaIvXoI8rRA)
| ID | Name | Email | Role |
|----|------|-------|------|
| (agency-owner) | Ranjan Singh | ranjan@neuronx.co | admin |
| QvXEGGAguPesgAasxAsA | Alexandra Wong | team@neuronx.co | admin |

### VMC Calendar Booking URLs (FINAL — 2026-03-30)
| Calendar | ID | Duration | Price | Auto-Confirm | Booking URL |
|----------|----|----------|-------|--------------|-------------|
| VMC — Free Initial Assessment | To1U2KbcvJ0EAX0RGKHS | 15 min | FREE | ✅ Yes | https://api.leadconnectorhq.com/widget/booking/To1U2KbcvJ0EAX0RGKHS |
| VMC — Paid Consultation | bHYTHjSMXjuKULrawXNM | 30 min | $200 CAD | ✅ Yes | https://api.leadconnectorhq.com/widget/booking/bHYTHjSMXjuKULrawXNM |
| VMC — Strategy Session (Complex) | y9X7TRnrWXMBplrkdMvm | 60 min | TBD | ❌ No (manual) | https://api.leadconnectorhq.com/widget/booking/y9X7TRnrWXMBplrkdMvm |

### NeuronX Calendar Booking URLs (FINAL — 2026-03-30)
| Calendar | ID | Duration | Price | Auto-Confirm | Booking URL |
|----------|----|----------|-------|--------------|-------------|
| NeuronX — Product Demo | clvODWkfByOZnzeqyPPW | 30 min | FREE | ✅ Yes | https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW |

### Google Workspace Aliases (all @neuronx.co → ranjan@neuronx.co)
- **NeuronX**: hello, team, support, billing
- **Client template (pilot)**: rcic, intake, sales

### Next Steps (Priority Order)
1. **Snapshot update** → take new snapshot of VMC after all changes ← NEXT
2. **Block 2B** → 5 email/SMS templates for workflows
3. **Block 2C/2D** → remaining workflow refinements + NeuronX sales workflows
4. **vmc.neuronx.co nav** → update "Book Consult" link to Free Initial Assessment URL (15min calendar)

---

## Combined Audit Complete (2026-03-21)

**Source**: Claude API Audit + GHL Built-in AI 14-Section Audit
**Master Work Items**: `docs/06_execution/MASTER_WORK_ITEMS.md`

### Critical Discovery: Calendar has ZERO availability hours
- `openHours: {}` — nobody can book consultations
- MUST FIX before any testing

### Audit Scores (GHL AI):
- Pipeline: 7/10 (missing PROPOSAL SENT stage)
- Workflows: 8/10 (13 built, gaps in retry logic)
- Custom Fields: 7.5/10 (R2/R4/R5/R6 missing, 3 junk fields)
- Tags: 9/10 (excellent taxonomy)
- Calendar: 5/10 (no availability, no buffers, no gate)
- Forms: 4/10 (1 form, placeholder text, no survey)
- Funnels: 3/10 (1 page, no TY page)
- Compliance: 6/10 (consent exists, AI disclaimer missing)

### P0 Fixes Remaining:
1. Set calendar availability hours
2. Fix form consent placeholder text
3. Add welcome SMS to WF-01
4. Fix form button text
5. Run E2E UAT test

