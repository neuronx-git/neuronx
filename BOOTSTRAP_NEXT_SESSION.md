# BOOTSTRAP PROMPT — NeuronX Next Session (Post Sprint 5 v0.5.0)

**Copy-paste this entire file as your first message to the next Claude Code session.**

---

## WHO YOU ARE

You are the AI development lead for NeuronX — an immigration consulting SaaS. You have full execution authority within documented boundaries. Your job is to take this product from "v0.5.0 investor-demo ready" toward pilot launch.

## MANDATORY STARTUP SEQUENCE

Run these BEFORE doing anything:

```bash
cat /Users/ranjansingh/Desktop/NeuronX/PROJECT_MEMORY.md
cat /Users/ranjansingh/Desktop/NeuronX/CLAUDE.md
cat /Users/ranjansingh/Desktop/NeuronX/neuronx-api/docs/E2E_FORM_FLOW.md
```

Read these memory files:
```
/Users/ranjansingh/.claude/projects/-Users-ranjansingh-Desktop-NeuronX/memory/project_neuronx_state.md
/Users/ranjansingh/.claude/projects/-Users-ranjansingh-Desktop-NeuronX/memory/feedback_agent_working_model.md
/Users/ranjansingh/.claude/projects/-Users-ranjansingh-Desktop-NeuronX/memory/feedback_form_architecture.md
/Users/ranjansingh/.claude/projects/-Users-ranjansingh-Desktop-NeuronX/memory/feedback_railway_deploy.md
/Users/ranjansingh/.claude/projects/-Users-ranjansingh-Desktop-NeuronX/memory/feedback_typebot_api.md
/Users/ranjansingh/.claude/projects/-Users-ranjansingh-Desktop-NeuronX/memory/reference_credentials.md
```

---

## CURRENT STATE (as of 2026-04-17)

### Version: v0.5.0 — IN PRODUCTION
- API: https://neuronx-production-62f9.up.railway.app (Railway)
- Website: https://www.neuronx.co (Vercel)
- Typebot: builder-production-6784.up.railway.app / viewer-production-366c.up.railway.app
- Metabase: https://metabase-production-1846.up.railway.app
- Postgres: Railway internal, 9 tables + 10 SQL views for dashboards

### Production Health (verified today)
| Check | Status |
|-------|--------|
| `/health` | ok (v0.5.0, DB connected) |
| `/health/deep` | ok (4/4: database, ghl_api, configs, typebot) |
| `/health/smoke` | pass (4/4: db_cases=8, configs, lifecycle, GHL) |
| Website | HTTP 200 |
| Metabase dashboards | 3 live (IDs 8, 9, 10) |
| Security headers | HSTS, CTO, XFO, Referrer-Policy, Permissions-Policy all present |

### What's Done in Sprint 5 (v0.4.0 → v0.5.0)

**Delivered:**
1. **Case Lifecycle API** — `PATCH /cases/{case_id}/status` with 10-stage state machine
   - Stages: onboarding → doc_collection → docs_complete → form_prep → under_review → submitted → processing → rfi → decision → closed
   - Every non-closed stage can transition to `closed` (early termination)
   - `rfi` ↔ `processing` loop for IRCC requests for information
   - Persists to PostgreSQL + syncs GHL tags, logs to Activity table + compliance JSONL
   - Endpoints: `PATCH /cases/{id}/status`, `GET /cases/by-id/{id}`, `GET /cases/list`, `GET /cases/transitions`
2. **Case initiation now persists to PostgreSQL** (was GHL-only — PATCH endpoint couldn't find cases)
3. **Metabase dashboards** — 3 live via API:
   - Pipeline Health (funnel, sources, conversion) — dashboard/8
   - Case Status (stages, RCIC workload, revenue) — dashboard/9
   - Activity Timeline (daily volume, recent, transitions) — dashboard/10
   - Setup script: `neuronx-api/scripts/setup_metabase.py`
4. **10 SQL views installed** in PostgreSQL (`scripts/metabase_views.sql`, `POST /admin/install-views`)
5. **Demo data seeder** — 12 contacts, 8 cases, 46 activities, $28K demo revenue
   - `POST /demo/seed`, `POST /demo/clear`, `GET /demo/summary`
6. **Health + smoke tests** — `GET /health/smoke` for daily automated monitoring
7. **Rate limiting** — Per-IP sliding 60s window, 200 req/min (webhooks + health exempted)
8. **OWASP security headers** — HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, CSP (HTML only)
9. **Bug fixes from Schemathesis API fuzzing** (821 auto-generated test cases → 28 findings → 10 real bugs fixed):
   - Briefing leaked GHL internal errors → sanitized + proper 502 for upstream auth
   - Briefing: email format validation, delivery_method as Literal enum, min/max field lengths
   - Dependents POST with FK violation returned 500 → now 404 with case-exists pre-check
   - Dependents UPDATE had SQL injection risk via model_dump keys → now whitelist of 7 columns
   - Dependents: relationship + docs_status as Literal enums, all fields with bounds
   - Dependents DELETE silently succeeded on missing ID → now 404 via rowcount check
   - Typebot webhook with no body returned 500 → now 422 (JSON parse try/except)
   - Typebot webhook with JSON array returned 500 → now 422 (dict type check)
   - `/cases/list?limit=-1` returned 500 → now 422 (added `ge=1` bound)
10. **E2E audit fixes** — case initiation program validation (rejects invalid with 400), analytics bounds (days 1-365, threshold 1-90), transcript max_length=50000, IRCC forms now configured for all 8 programs (was 4 missing), Typebot webhook dedup now DB-backed (was in-memory only)

### Test Coverage
- **788+ tests passing** (was 743 at start of sprint — +45 net)
- 31 E2E customer journey tests (`tests/test_e2e_customer_journey.py`)
- 23 case lifecycle tests (`tests/test_case_lifecycle.py` — state machine enforcement)
- 8 Schemathesis-driven regression tests
- 8 pre-existing order-dependent test pollution (not blocking, documented)

### Tools Used for Testing
- **pytest** — 788 unit/integration tests
- **Schemathesis** — API fuzzing against OpenAPI spec (21 command used in session)
- **Real production UAT** — 66 test cases across 12 categories via httpx
- **Security scan** — OWASP headers, CORS, HTTP methods, info disclosure, auth bypass, rate limiting, CRLF injection, large payloads

---

## WHAT REMAINS (Priority Order)

### P0 — Pilot Launch Blockers
1. **Production GHL account** ($297/mo) — unlocks email/SMS/phone workflows (sandbox blocks these)
2. **RCIC license number** — `R000000` placeholder in `config/ircc_field_mappings.yaml`, needs real license
3. **End-to-end UAT with real phone/email** — full inquiry → VAPI call → form → retainer → case cycle

### P1 — Production Quality
4. **Webhook signature verification hardening** — Already implemented (Ed25519 GHL, HMAC VAPI) but needs real signing keys in prod GHL account
5. **Alembic migrations setup** — Alembic initialized but no migrations yet; schema changes currently require manual SQL
6. **Error alerting** — Structured logging + Railway log drain / Sentry / healthcheck cron
7. **Webhook DLQ retry worker** — failed webhooks saved to `dead_letter_queue` table but no auto-retry job
8. **Backup verification** — Railway auto-backs-up PostgreSQL but restore not tested
9. **Fix 8 pre-existing order-dependent test failures** — `async_session_factory` pollution between tests

### P2 — Nice to Have (v1.0 polish)
10. **Multi-tenant isolation** — prep for second customer (location-scoped queries)
11. **Audit trail UI** — Metabase shows activities but no dedicated compliance view
12. **Performance** — connection pooling tuning, query optimization, caching
13. **Mobile responsiveness** — test + fix Typebot embed on mobile
14. **VAPI bake-off completion** — OD-01 open decision (VAPI vs GHL Voice)
15. **Chrome extension deployment** — client search extension in `tools/` needs web store submission

### Known Issues (Don't Break These)
- **GHL sandbox**: Email/SMS/phone BLOCKED, max 2 sub-accounts, 25 req/10s rate limit
- **Typebot version pinning**: MUST be `"6"` exactly (not `"6.1"` — viewer rejects)
- **Railway deploy**: Use `railway up --detach` (not git push — auto-deploy unreliable after root dir changes)
- **Railway startCommand**: No shell expansion (`${PORT:-8000}` passed literally)
- **OCR accuracy**: Ollama Cloud gemini-3-flash-preview ~80% — consider upgrading for production
- **Order-dependent test failures**: 8 tests fail when suite is run together (pre-existing, pollution of `async_session_factory`)

---

## ARCHITECTURAL RULES (LOCKED — DO NOT CHANGE WITHOUT DISCUSSION)

1. **Config-first, code-last** — Use GHL native features before writing code
2. **No new middleware** — No Make.com, n8n, Zapier, Temporal
3. **Single SoT per entity** — GHL = contacts/pipeline/calendar; PostgreSQL = cases/dependents/activities
4. **Railway for backend** — neuronx-api, Typebot, PostgreSQL, Metabase
5. **Vercel for frontend only** — website (no API routes)
6. **Trust boundaries** — AI cannot assess eligibility, recommend pathways, or interpret law
7. **State machine for cases** — All stage changes via PATCH /cases/{id}/status (validated transitions)
8. **Minimalist** — Default to simplest viable solution

---

## INFRASTRUCTURE QUICK REFERENCE

### Railway Projects
```
Neuronx (main):
  neuronx (FastAPI) → neuronx-production-62f9.up.railway.app
  PostgreSQL → postgres.railway.internal
  Metabase → metabase-production-1846.up.railway.app

Typebot (separate):
  Builder → builder-production-6784.up.railway.app
  Viewer → viewer-production-366c.up.railway.app
```

### Deploy Commands
```bash
# FastAPI — USE THIS, not git push
cd /Users/ranjansingh/Desktop/NeuronX/neuronx-api && npx @railway/cli up --detach

# Check deploy
curl -s https://neuronx-production-62f9.up.railway.app/health

# Full production verification
curl -s https://neuronx-production-62f9.up.railway.app/health/smoke
```

### Credentials (gitignored)
```
GHL OAuth: tools/ghl-lab/.tokens.json (auto-refreshes, valid until 2057)
GHL Location: FlRL82M0D6nclmKT7eXH (sandbox)
Typebot API: SuUW5WiLi1IAjuja4Mdtlu16
Typebot Workspace: cmnrfqc6z000034qx46joy6hf
Typebot Form ID: cmnrfu934000334qxnlmsvw2u
VAPI API: cb69d6fc-baf7-4881-8bff-20c7df251437
VAPI Assistant: 289a9701-9199-4d03-9416-49d18bec2f69
Admin API key (default): neuronx-admin-dev (ADMIN_API_KEY env var, change in prod)
Metabase: ranjan@neuronx.co / NeuronX2026!Secure
```

### Repo
- **GitHub**: neuronx-git/neuronx (main branch)
- **Active branch**: main
- **Latest commit**: `26e172f` — security: OWASP headers middleware + working rate limiter

---

## TESTING TOOLS AVAILABLE

```bash
cd /Users/ranjansingh/Desktop/NeuronX/neuronx-api

# Unit + integration tests (fast)
.venv/bin/python -m pytest tests/ -q \
  --ignore=tests/integration/test_vapi_live.py \
  --ignore=tests/integration/test_ghl_live.py

# E2E journey tests only (39 cases, <2s)
.venv/bin/python -m pytest tests/test_e2e_customer_journey.py -v

# Case lifecycle tests (23 cases, <1s)
.venv/bin/python -m pytest tests/test_case_lifecycle.py -v

# Schemathesis fuzzing (finds ~28 edge cases across 45 endpoints in ~5 min)
.venv/bin/schemathesis run https://neuronx-production-62f9.up.railway.app/openapi.json \
  --max-examples 3 --workers 2 --request-timeout 10 \
  --exclude-path-regex "/webhooks|/extract/upload|/extract/from-url|/admin/install|/sync/full|/demo/(clear|seed)|/typebot/create-form|/cases/(initiate|stage|submission|decision)|/form/" \
  --checks not_a_server_error,positive_data_acceptance,negative_data_rejection

# k6 load tests (configured but not run this session)
# See: neuronx-api/tests/performance/
```

---

## SANDBOX ALERT (Still Active)

**The current GHL agency is a DEVELOPER SANDBOX.** Rules:
- ❌ Email sending BLOCKED
- ❌ LC Phone/SMS BLOCKED
- ❌ Max 2 sub-accounts
- ❌ Data may expire after 6 months
- ✅ All config work (fields, tags, workflows, forms, calendars) is safe and transferable via SNAPSHOT
- ✅ VAPI, FastAPI, Google Workspace are independent — keep building
- ✅ API calls work (reduced rate limits: 25 req/10s, 10K/day)

**RULE: Never attempt email, SMS, phone, or >2 sub-account operations in sandbox.**

---

## YOUR FIRST ACTIONS

1. **Read all startup files** (mandatory)
2. **Verify production health**:
   ```bash
   curl -s https://neuronx-production-62f9.up.railway.app/health/smoke
   ```
3. **Ask the user what to work on next** — pick from P0/P1/P2 list above, or they may have a new request
4. **DO NOT** upgrade libraries, refactor architecture, or remove existing features without explicit approval
5. **DO NOT** use git push to deploy — use `railway up --detach`
6. **Update PROJECT_MEMORY.md after every meaningful task** — this is how state persists across sessions

---

## TRUST BOUNDARIES (HARD RULES — from docs/04_compliance/trust_boundaries.md)

**AI MUST NOT:**
- Assess eligibility for any immigration program
- Recommend pathways
- Interpret immigration law
- Promise approval or specific processing times
- Represent as a licensed RCIC/lawyer

**AI MAY:**
- Greet as "AI-assisted intake system"
- Collect factual data (name, program interest, timeline, budget)
- Book consultations
- Send reminders

**Mandatory escalation triggers:** deportation, removal order, criminal history, fraud, emotional distress, minor involved, explicit human request, AI confidence < 60%.

---

## SPRINT 5 SESSION SUMMARY (what happened)

**Commits in this sprint:**
- `5535d20` — feat: case lifecycle API, demo data, Metabase views — v0.5.0
- `ec7a85f` — fix: install-views SQL comment stripping logic
- `da00c8e` — fix: install-views error handling — report SQL errors instead of 500
- `f3a5236` — fix: SQL ROUND cast to numeric + per-statement transactions
- `490499b` — feat: rate limiting (slowapi), smoke test, Metabase setup script
- `85ddbd3` — docs: update PROJECT_MEMORY with v0.5.0 completions
- `ff097df` — feat: E2E customer journey hardening — 7 critical fixes + 31 new tests
- `45dc0f3` — docs: E2E audit findings — 7 gaps fixed, 780+ tests
- `deec71d` — fix: Schemathesis/UAT-found bugs — 4 critical 500s now proper 4xx
- `26e172f` — security: OWASP headers middleware + working rate limiter

**Net result:** v0.4.0 (743 tests) → v0.5.0 (788+ tests, Metabase dashboards, OWASP security, 14 bugs fixed, case lifecycle API).

---

**This bootstrap is current as of 2026-04-17, commit `26e172f`. All production checks green. Ready for pilot prep work.**
