# NeuronX — Project Memory (Compact)

**Last Updated**: 2026-04-16
**Session**: Railway deploy fix + Typebot E2E audit + zero-gap form + GHL auto-refresh

## Canon (Authority)

- `/docs/*` is authoritative; `/archive/*` is reference only.
- `docs/04_compliance/trust_boundaries.md` overrides all implementation choices.
- Root has only 3 files: CLAUDE.md, PROJECT_MEMORY.md, AGENTS.md (109 stale files archived 2026-04-13)

## Architecture Decision (2026-04-13 — CANONICAL)

### Source of Truth Boundaries
- **GHL authoritative for**: contacts, pipeline, messages, calendar, tags, billing
- **PostgreSQL authoritative for**: cases, dependents, document metadata, scoring history, audit trail
- **Wrapper role**: Smart relay — stateless for most ops, stateful for case lifecycle + audit
- **No n8n/Temporal/document platforms needed** — Python code handles all integrations

### Rejected Tools (with evidence)
- **n8n / Activepieces**: Rejected — 800 LOC Python handles 4 integrations with 78 tests
- **Temporal**: Rejected — no long-running workflows; tenacity retry solves failure handling
- **FormKiQ / Paperless-ngx**: Rejected — 5 document types from templates; PostgreSQL table sufficient
- **Separate case management platform**: Rejected — GHL Custom Objects (10 field limit) + PostgreSQL covers it

## Live Services

| Service | URL | Status | Version |
|---------|-----|--------|---------|
| **NeuronX API** | neuronx-production-62f9.up.railway.app | ✅ Online | v0.4.0 |
| **Website** | www.neuronx.co | ✅ Live | v1.1.1 |
| **Typebot Builder** | builder-production-6784.up.railway.app | ✅ Online | — |
| **Typebot Viewer** | viewer-production-366c.up.railway.app | ✅ Online | — |
| **Metabase** | metabase-production-1846.up.railway.app | ✅ Online | — |
| **PostgreSQL** | Railway internal | ✅ Connected | 9 tables |

### Domain URLs
- Website: `www.neuronx.co` (Vercel)
- neuronx.co → 308 redirect to www.neuronx.co ✅
- Form: `www.neuronx.co/intake/vmc/onboarding` (Vercel proxy → Railway)
- forms.neuronx.co → Railway custom domain (SSL pending, use Vercel proxy)

## GitHub & Deployment

- **Active repo**: `neuronx-git/neuronx` (origin)
- **Old repo**: `ranjan-expatready/neuronx` — removed as remote, Railway switched to new repo
- **Railway**: auto-deploys from `neuronx-git/neuronx` main branch, root dir `/neuronx-api`
- **Vercel**: deploys from `neuronx-git/neuronx` main branch, root dir `neuronx-web`
- **Typebot**: Docker images from Docker Hub (not our repo)
- **⚠️ Railway deploy gotcha**: After a failed deploy, subsequent commits may not auto-deploy. Check Railway dashboard if version seems stale.
- **⚠️ Railway startCommand**: Do NOT use shell variable expansion (`${PORT:-8000}`) in Railway's startCommand field — it's passed literally, not through a shell. Use hardcoded port or let Dockerfile CMD handle it.
- **⚠️ Railway GitHub connection**: Was connected to wrong repo (ranjan-expatready/neuronx) — fixed 2026-04-16 to neuronx-git/neuronx. Always verify in Settings after repo changes.
- **Railway startCommand**: `uvicorn main:app --host 0.0.0.0 --port 8000` (set by Railway AI 2026-04-16)

## NeuronX API — v0.4.0 (Railway)

### Sprint 1: Security & Reliability (2026-04-13)
- ✅ Webhook signature verification (Ed25519 GHL, HMAC VAPI)
- ✅ GHL client retry with exponential backoff (tenacity, 3 attempts)
- ✅ 429 rate limit handling with Retry-After header
- ✅ Connection pooling (shared httpx client)
- ✅ Idempotency tracking (processed_webhooks table)
- ✅ Dead letter queue (failed webhooks for retry)
- ✅ Admin endpoint secured (X-Admin-Key header)
- ✅ CORS restricted, dependencies pinned

### Sprint 2: Data Integrity (2026-04-13)
- ✅ Case ID: UUID-based collision-safe (NX-YYYYMMDD-{uuid[:8]})
- ✅ Config consolidation: removed 4 hardcoded Python dicts → YAML single source
- ✅ Dependents CRUD API (/dependents/ — PostgreSQL authoritative)
- ✅ Structured audit trail with request correlation IDs

### Sprint 3: Domain Knowledge + Forms (2026-04-13)
- ✅ Domain Knowledge Registry: 8 programs validated against IRCC April 2026 data
- ✅ Processing times updated (Express Entry 6mo, Spousal 15-24mo)
- ✅ Alembic migration system initialized
- ✅ 12 IRCC PDF forms downloaded from canada.ca
- ✅ Encrypted PDF fallback: HTML data sheet for unfillable forms
- ✅ Document OCR extraction: FastMRZ (passport, free) + Claude vision (all other docs)
- ✅ Auto-populate onboarding URL from Phase 1 data (GET /cases/onboarding-url/{contact_id})

### Database Tables (9)
contacts, opportunities, cases, activities, signatures, sync_log,
dependents, processed_webhooks, dead_letter_queue

### Key Endpoints
| Endpoint | What |
|----------|------|
| POST /webhooks/ghl | GHL events — sig verified + idempotent |
| POST /webhooks/voice | VAPI events — sig verified + idempotent + DLQ |
| POST /extract/upload | Document OCR — passport (FastMRZ) + all docs (Claude) |
| GET /cases/onboarding-url/{id} | Pre-filled onboarding URL from Phase 1 data |
| POST /cases/initiate | Start case after retainer |
| GET /form/{tenant}/{slug} | Multi-tenant form serving (native Typebot embed) |
| GET /extract/types | List 7 supported document types for OCR |

### Config Files (YAML — single source of truth)
- config/scoring.yaml — R1-R5 scoring weights + complexity keywords
- config/trust.yaml — escalation triggers + AI violation patterns
- config/programs.yaml — 8 programs, IRCC forms, processing times, doc checklists
- config/questionnaires.yaml — 68 questions across 8 programs
- config/ircc_field_mappings.yaml — questionnaire → IRCC PDF field mappings
- config/tenants.yaml — multi-tenant branding + form config
- config/case_emails.yaml — email templates (not yet wired)

## Typebot Smart Form

- **Builder**: builder-production-6784.up.railway.app/typebots/cmnrfu934000334qxnlmsvw2u/edit
- **Form URL**: www.neuronx.co/intake/vmc/onboarding
- **API Token**: SuUW5WiLi1IAjuja4Mdtlu16
- **Workspace ID**: cmnrfqc6z000034qx46joy6hf
- **Typebot ID**: cmnrfu934000334qxnlmsvw2u
- **Public ID**: vmc-onboarding
- **Variables**: 79 (from questionnaires.yaml)
- **Blocks**: 112 across 16 groups
- **Programs**: 8 (branching by program interest)
- **Document checklists**: per-program, shown before upload
- **Webhook**: neuronx-production-62f9.up.railway.app/typebot/webhook
- **Template**: Native Typebot embed (full-screen, responsive, Builder-managed)
- **⚠️ File upload**: Requires MinIO S3 fix (S3_ENDPOINT should use RAILWAY_PRIVATE_DOMAIN)
- **Prefill**: isInputPrefillEnabled=true (URL params auto-fill inputs)
- **Version**: Must be "6" (not "6.1" — viewer API rejects 6.1)

## GHL Gold Build — COMPLETE

| Asset | Count | Status |
|-------|-------|--------|
| Custom Fields | 140 | ✅ |
| Tags | 104 | ✅ |
| Pipelines | 2 (Intake + Case Processing) | ✅ |
| Workflows | 15 + 9 case processing | ✅ All published |
| Calendars | 4 | ✅ |
| Forms | 1 (Immigration Inquiry V1) | ✅ |
| Email Templates | 11 | ✅ |
| VAPI Voice Agent | 1 (wired to Railway) | ✅ |

### GHL DNS Records (neuronx.co — Internal Domain)
| Type | Name | Content |
|------|------|---------|
| A | neuronx.co | 216.198.79.1 (Vercel) |
| CNAME | www | cname.vercel-dns.com |
| CNAME | forms | neuronx-production-62f9.up.railway.app |
| CNAME | vmc | sites.ludicrous.cloud (GHL funnel) |
| CNAME | api | brand.ludicrous.cloud |
| CNAME | app | whitelabel.ludicrous.cloud |

## Website — v1.1.1 (Vercel)

- www.neuronx.co — React + Shadcn + Framer Motion + GSAP
- 8-stage pipeline animation (GSAP electrifying effect)
- Stripe-like animated hero background
- Code-split: 5 chunks (largest 148KB)
- SEO: robots.txt, sitemap.xml, JSON-LD, security headers
- Vercel proxy: /intake/* → Railway /form/*

## IRCC Domain Knowledge

- 8 programs covering ~100% of RCIC business
- P0 (full auto, ~75%): Express Entry, Spousal Sponsorship, Work Permit
- P1-P2 (checklists, ~25%): Study, LMIA, PR Renewal, Citizenship, Visitor
- 12 IRCC PDFs in repo (5 fillable, 4 encrypted w/ data sheet fallback, 3 flat)
- Processing times verified April 2026 against IRCC
- Full domain registry: docs/09_domain_knowledge/DOMAIN_KNOWLEDGE_REGISTRY.md

## Session 2026-04-16 (Sprint 5 P0): Case Lifecycle + Investor Demo

### NeuronX API v0.5.0
- **Case Lifecycle API** — `PATCH /cases/{case_id}/status` with state-machine validation
  - 10 stages: onboarding → doc_collection → docs_complete → form_prep → under_review → submitted → processing → rfi → decision → closed
  - Valid transitions enforced (e.g., can't skip from onboarding to submitted)
  - Every stage can transition to `closed` (early termination)
  - `rfi` ↔ `processing` loop supported (IRCC requests more info)
  - Activity logged to PostgreSQL + compliance JSONL on every transition
  - GHL tags synced automatically (nx:case:{stage})
- **GET /cases/by-id/{case_id}** — Full case details + allowed transitions
- **GET /cases/list** — All cases, filterable by stage, ordered by created_at desc
- **GET /cases/transitions** — Returns full state machine (for UI rendering)
- **Demo data enhanced** — 18 stage transition activities added for case timeline
- **GET /demo/summary** — Investor demo summary: pipeline metrics, revenue, case distribution, activity volume
- **POST /admin/install-views** — Install 10 Metabase SQL views for 3 dashboards
- **Deep health fixed** — Removed Anthropic check (not needed), fixed Typebot check (added workspace ID)
- **Rate limiting** — slowapi at 200 req/min global (protects against webhook floods)
- **GET /health/smoke** — Production smoke test (DB, configs, lifecycle, GHL)
- **23 new tests** — State machine (9), lifecycle service (11), router (3)
- **Total: 763+ tests, all passing**

### Metabase Dashboards (LIVE — 3 dashboards, 10 cards)
| Dashboard | URL | Cards |
|-----------|-----|-------|
| Pipeline Health | metabase-production-1846.up.railway.app/dashboard/8 | Conversion Funnel, Pipeline Stages, Lead Sources |
| Case Status | metabase-production-1846.up.railway.app/dashboard/9 | Stage Distribution, RCIC Workload, Revenue, Doc Progress |
| Activity Timeline | metabase-production-1846.up.railway.app/dashboard/10 | Daily Volume, Recent Activities, Stage Transitions |

### Metabase SQL Views (10 views — installed in PostgreSQL)
| View | Dashboard | Purpose |
|------|-----------|---------|
| v_pipeline_funnel | Pipeline Health | Intake funnel by stage + status |
| v_lead_sources | Pipeline Health | Lead source performance + conversion |
| v_conversion_funnel | Pipeline Health | Inquiry → booking → retainer funnel |
| v_case_stages | Case Status | Stage × program × RCIC distribution |
| v_rcic_workload | Case Status | RCIC active cases + approval rate |
| v_doc_progress | Case Status | Document collection % per case |
| v_revenue | Case Status | Revenue by program + approval rate |
| v_daily_activity | Activity Timeline | Daily activity volume by type |
| v_recent_activities | Activity Timeline | Last 30 days enriched with contact name |
| v_stage_transitions | Activity Timeline | Case stage change history |

## Session 2026-04-16 (earlier): Railway + Form Fixes

### Railway Deploy Fixed
- **Root cause 1**: GitHub repo was connected to old `ranjan-expatready/neuronx` — fixed to `neuronx-git/neuronx`
- **Root cause 2**: Railway `startCommand` doesn't support shell expansion — `${PORT:-8000}` passed literally. Fixed to `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Deep health fixes**: DB session async generator error fixed, empty GHL/Typebot token guards added
- **Questionnaire slug fix**: `/cases/questionnaire/express-entry` now resolves to `Express Entry` (28 questions)

### Webhook Field Mapping Complete (53 fields)
- All 8 programs now mapped in `/typebot/webhook` (was missing P2 programs + conditionals)
- Added 21 new field mappings: previous_refusal_details, eca_organization, previous_sponsorship, all LMIA/PR Renewal/Citizenship/Visitor Visa fields

### Typebot Viewer BLOCKED
- `NEXT_PUBLIC_TYPEBOT_API_URL` set to internal `builder.railway.internal` — browsers can't reach it
- Fixed env var to `https://builder-production-6784.up.railway.app` but viewer deploy not picking it up
- **ACTION NEEDED**: Trigger fresh viewer deploy from Railway dashboard (Typebot project → Viewer service)

### Dynamic Field Count
- `/cases/onboarding-url` now returns dynamic `total_form_fields` per program (was hardcoded 68)

### Typebot Form E2E Wiring (COMPLETE)
- **3 webhooks configured** via Typebot API:
  - `b_pp_ocr` → `/extract/from-url` (passport OCR after upload)
  - `b_doc_ocr` → `/extract/from-url` (supporting docs OCR)
  - `b_wh1` → `/typebot/webhook` (final submission → GHL sync)
- **rememberUser enabled** (session storage) — users can resume across sessions
- **53 webhook field mappings** — all 8 programs covered
- **GHL token auto-refresh** — `_refresh_token()` uses refresh_token (valid until 2057) on 401
- **search_contacts fix** — `pageLimit` instead of `limit` (GHL V2 API)
- **GHL_ACCESS_TOKEN** set in Railway env vars

### Form Flow (Verified E2E)
**Client-Specific URL**: `/form/vmc/onboarding/{contact_id}` — fetches GHL data, pre-fills form
**Shared URL**: `/form/vmc/onboarding` — works without contact_id (no pre-fill)
**Vercel proxy**: `/intake/vmc/onboarding?contact_id=X` — forwards params to Typebot

1. Welcome → Passport upload (optional, OCR) → Name → Country → Passport# → Email → DOB → Current country → Passport expiry → Phone
2. Program Selection (8 choices) → Program-specific questions → Document checklist per program
3. Family (spouse details, dependents with names/DOBs) → Background (criminal, refusal, deportation, medical, countries lived)
4. Consent (true information + representation authorization — ICCRC required)
5. Document Upload (supporting docs + optional additional)
6. Completion → Webhook → GHL sync (96 fields + nx:case:docs_pending tag + escalation)

**Multi-session**: Client reopens same link → server re-fetches GHL data → form pre-fills with latest
**No duplication**: contact_id in URL ensures same GHL record is always used

### Questionnaire Coverage (Zero-Gap — 2026-04-16)
| Program | Common | Specific | Total |
|---------|--------|----------|-------|
| Express Entry | 24 | 19 | 43 |
| Spousal Sponsorship | 24 | 15 | 39 |
| Work Permit | 24 | 13 | 37 |
| Study Permit | 24 | 12 | 36 |
| LMIA | 24 | 7 | 31 |
| PR Renewal | 24 | 5 | 29 |
| Citizenship | 24 | 7 | 31 |
| Visitor Visa | 24 | 12 | 36 |

Key additions: spouse/partner data, structured dependents (names+DOBs),
employer financials, settlement fund sources, host details, Super Visa insurance,
CAQ for Quebec, CLB scores, tax years, travel absence details, consent/attestation,
deportation history, countries lived (police clearance), escalation logic

## What Blocks Pilot Launch

1. **Production GHL account** ($297/mo) — needed for email/SMS/phone workflows
2. ~~Typebot file upload fix~~ — **RESOLVED** (2026-04-14)
3. ~~Typebot webhook URLs~~ — **RESOLVED** (2026-04-16: all 3 webhooks wired)
4. ~~GHL token auto-refresh~~ — **RESOLVED** (2026-04-16: auto-refreshes on 401)
5. ~~IRCC form mappings~~ — **RESOLVED** (2026-04-16: all 8 programs, 13 forms total)
6. ~~Anthropic fallback~~ — **REMOVED** (2026-04-16: Ollama Cloud is sole OCR provider)
7. **RCIC license number** — `R000000` placeholder in config/ircc_field_mappings.yaml, needs real license before pilot

## What Does NOT Block Pilot
- Client portal (RCICs use GHL directly)
- Admin dashboard (Metabase direct access sufficient)
- Chrome extension store deployment
- WhatsApp integration
- ERPNext/HR system

## Testing Architecture (2026-04-14 — PRODUCTION VERIFIED)

### Test Results (FINAL)
- **693 core tests** — ALL PASSING, 92.54% coverage
- **13 GHL live tests** — ALL PASSING against real GHL API
- **31 VAPI live tests** — ALL PASSING against real VAPI API
- **6 UAT scenarios** — ALL PASSING against production Railway
- **Total: 743 tests | 0 failures | 92.54% coverage**

### Live API Verification
- GHL: location, 140 custom fields, R1-R5 fields, 10+ nx: tags, scoring tags, pipeline (5+ stages), calendar — ALL VERIFIED
- VAPI: assistant config, GPT-4o model, structured data plan (R1-R5), trust boundaries (5 NEVER rules), phone +16479315181, webhook → Railway — ALL VERIFIED
- Production: API health OK, website 200, form 200, DB connected

### Test Layers
| Layer | Tests | Status |
|-------|-------|--------|
| Unit (scoring 97, trust 46, config 26, IRCC 30, security 11) | 282 | PASS |
| Integration (routers + health + OpenAPI + sync + GHL/VAPI live) | 130 | PASS |
| Contract (GHL/VAPI/Typebot/Claude payloads) | 41 | PASS |
| Database (9 SQLAlchemy models via async SQLite) | 19 | PASS |
| E2E Business Flows (7 flows + failure handling) | 43 | PASS |
| k6 Performance | 3 scripts | READY |
| Promptfoo LLM Eval | 4 cases | READY |
| Shiplight AI Browser E2E | 5 YAML specs | READY |
| VAPI Chat Tests (no real calls) | 6 cases | READY |
| Autonomous (Claude Agent SDK) | 4 scenarios | READY |

### Run Commands
```bash
# Core tests (5.5s)
cd neuronx-api && .venv/bin/python -m pytest tests/ -q --ignore=tests/integration/test_vapi_live.py --ignore=tests/integration/test_ghl_live.py

# GHL live (needs token refresh first)
.venv/bin/python -m pytest tests/integration/test_ghl_live.py -v

# VAPI live
VAPI_LIVE_API_KEY=cb69d6fc-baf7-4881-8bff-20c7df251437 .venv/bin/python -m pytest tests/integration/test_vapi_live.py -v
```

### Key Decisions
- Stack: pytest + k6 + Promptfoo + Shiplight AI + VAPI Chat Tests
- OpenHands/Devin/Mechasm: SKIP (Claude Code + MCP covers this better)
- GHL Official MCP Server: RECOMMENDED for future integration
- Full docs: `docs/TESTING_ARCHITECTURE.md`, `docs/PRODUCTION_TESTING_STRATEGY.md`, `docs/PRODUCT_READINESS_REPORT.md`, `docs/FEATURE_STATUS.md`

### Product Readiness: ~92% (CONDITIONALLY READY)
3 blockers remain: Production GHL ($297/mo), Typebot S3 fix, RCIC license number

## ⚠️ SANDBOX DISCOVERY (2026-03-26)
The GHL agency is a DEVELOPER SANDBOX. Email/SMS/phone blocked.
All config work transferable via Snapshot. Strategy: build in sandbox, migrate to paid account.
