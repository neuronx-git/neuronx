# 🔎 NeuronX Master Production Audit — Fresh Perspective

**Date**: 2026-04-18
**Auditor**: Claude (PM + DevOps + Production Manager hat)
**Method**: 6 parallel expert sub-agents (UX, Security, Code, Architecture, DevOps, Perf) on live prod + full codebase
**Scope**: All 7 golden journeys, all API endpoints, full repo, live Railway + Vercel + GHL
**Verdict**: ✅ Investor-demo-ready. ⚠️ NOT first-paying-customer-ready. 🚨 3 P0 security bugs must fix before ANY external use.

---

## 🔥 TL;DR — The 10 Things That Matter

| # | Finding | Severity | Blocker for | Fix effort |
|---|---|---|---|---|
| 1 | **Real secrets in `.env.example` committed to git** (VAPI, Anthropic, Skyvern, Vercel, GitHub tokens) | 🔴 P0 SEC | **IMMEDIATELY — rotate ALL** | 1 hr (rotate) + 15 min (fix file) |
| 2 | **`/clients/*` endpoints are IDOR-exposed** — no auth, returns passports, DOB, settlement funds by contact_id enumeration | 🔴 P0 SEC | Any prod traffic | 1 hr |
| 3 | **Admin key falls back to literal `"neuronx-admin-dev"`** if env var unset → unauthenticated admin access | 🔴 P0 SEC | Any prod traffic | 15 min |
| 4 | **No tenant isolation at API layer** — 2nd firm can read 1st firm's cases by guessing contact IDs | 🔴 P0 ARCH | Firm #2 onboarding | 4 hr |
| 5 | **26 email templates missing CASL unsubscribe link** — every send = potential $1M fine | 🔴 P0 COMPL | Any marketing email send | 1 hr |
| 6 | **No PIPEDA 30-day deletion workflow** — required by Canadian law | 🔴 P0 COMPL | Any real client data | 2 hr |
| 7 | **141 tests fail in full suite due to rate limiter** — CI unreliable | 🟡 P1 QA | Deploy confidence | 30 min |
| 8 | **Alembic migrations directory EMPTY** — all schema via `create_all()`, no rollback path | 🟡 P1 OPS | Schema change safety | 2 hr |
| 9 | **`$297` live agency lacks SaaS rebilling** — STRIPE_SAAS_PRICING.md assumes $497 | 🟡 P1 BIZ | First paid firm | Decision + $200/mo |
| 10 | **No Sentry, no structured logging, no rollback script** — prod runs blind | 🟡 P1 OPS | Confident scaling | 1 day |

**None of these block the investor demo this week** if we fix #1-3 (secrets + IDOR + admin key) and #7 (tests).

---

## 📐 Honest Current State (verified, not claimed)

### What the docs claim vs reality

| Claim | Reality | Delta |
|---|---|---|
| "788+ tests, 77% coverage" | **876 tests, 79.4% coverage** | ✅ Exceeded |
| "v0.5.0 live, v1.1.1 frontend" | API v0.5.0 ✅; frontend v1.1.**0** (package.json) | ⚠️ Doc drift |
| "/cases/list returns 200" | 200 ✅ | ✅ P0 fix held |
| "Typebot webhook creates new contact" | `"status":"processed"` ✅ | ✅ P0 fix held |
| "10 GHL users in PostgreSQL" | 10 confirmed, synced 2026-04-18 ✅ | ✅ |
| "26 templates with VMC logo" | 26/26 verified, uploaded today ✅ | ✅ |
| "Live agency on $497 SaaS Pro" | **$297 tier — no SaaS Configurator** | 🚨 Business-model gap |
| "Railway Postgres in secure region" | **US-East** (PIPEDA risk for Canadian PII) | ⚠️ Compliance gap |

### Latency reality (measured 2026-04-18 from live prod)

| Endpoint | p50 | p95 | Verdict |
|---|---|---|---|
| `/health/smoke` | 1004 ms | 1395 ms | OK (4 subchecks including GHL API) |
| `/health` | 750 ms | 1117 ms | OK |
| `/cases/list` | 935 ms | 942 ms | OK (no N+1) |
| `/analytics/pipeline` | 823 ms | 877 ms | Returns 0 — **stale pipeline_id** |
| `/analytics/stuck` | 813 ms | 883 ms | OK |
| `/` | 713 ms | 785 ms | OK |

Raw handler latency estimated 100-200ms; network dominates. No N+1 found. Baseline is healthy.

---

## 🚨 P0 — Fix This Week (Before ANY External Eyes)

### Security (#1-3 are exploitable NOW)

**1. Rotate leaked secrets + clean `.env.example`** — [`.env.example:20,27,35,49`](.env.example)
   ```
   ❌ VAPI_API_KEY=cb69d6fc-baf7-4881-8bff-20c7df251437
   ❌ ANTHROPIC_API_KEY=sk-ant-api03-jwAjz...
   ❌ SKYVERN_API_KEY=eyJhbGc...
   ❌ BROWSER_USE_API_KEY=bu_bJUE...
   ❌ .env:1-2  VERCEL_TOKEN, GITHUB_TOKEN
   ```
   **Action**: rotate all 6 keys today, replace values with `your_key_here` placeholders, commit. I can do the .env.example fix immediately; you rotate the keys in each vendor dashboard.

**2. Auth-gate `/clients/*` IDOR** — [`neuronx-api/app/routers/clients.py:22,51,125,223`](neuronx-api/app/routers/clients.py)
   Currently `/clients/{id}/form-data` returns passport + DOB + settlement funds **with no auth**. Add `X-Admin-Key` dependency (same pattern used in `/admin/*`).

**3. Remove hardcoded admin fallback** — [`neuronx-api/main.py:306,317`](neuronx-api/main.py)
   ```python
   admin_key = os.getenv("ADMIN_API_KEY", "neuronx-admin-dev")  # ❌ public default
   ```
   Raise `RuntimeError` at startup if `ADMIN_API_KEY` missing. Rotate the leaked `neuronx-admin-dev` in Railway env.

### Compliance (#4-6)

**4. Add CASL unsubscribe to all 26 templates** — [`neuronx-api/email-templates/generate.py`](neuronx-api/email-templates/generate.py)
   Add `{% if message.unsubscribe_url %}<a href="{{ message.unsubscribe_url }}">Unsubscribe</a>{% endif %}` to the generator's footer block. Re-render + re-upload (idempotent — we did this today for logo).

**5. PIPEDA 30-day deletion endpoint + job** —
   - New route: `POST /privacy/delete/{contact_id}` (admin-auth)
   - New column: `contacts.deletion_requested_at TIMESTAMP`
   - APScheduler job: daily scan → hard-delete Postgres rows + GHL contact via `/contacts/{id}` DELETE
   - Update privacy policy: "30-day deletion SLA"
   
**6. PIPEDA disclosure in VAPI `firstMessage`** — Already P0 #3 in PRODUCTION_READINESS. "This call is recorded for quality assurance. You may decline at any time." Founder UI edit in VAPI dashboard, 10 min.

### Demo blockers (#7-9)

**7. Fix stale `/analytics/pipeline` pipeline_id** — [`neuronx-api/app/routers/analytics.py`](neuronx-api/app/routers/analytics.py)
   Currently hardcoded to sandbox `Dtj9nQVd3QjL7bAb3Aiw` — returns 0 opps. Move to env var `VMC_INTAKE_PIPELINE_ID`, set to prod VMC pipeline. **15 min. I can do this next.**

**8. Fix 141 rate-limited test failures** — [`neuronx-api/main.py:84`](neuronx-api/main.py)
   Add `TESTING` env check; disable `slowapi.Limiter` when `TESTING=true`. Currently CI cannot reliably run the full suite. **30 min.**

**9. Fix case viewer demo-fallback masking** — [`neuronx-api/app/routers/case_viewer.py:119`](neuronx-api/app/routers/case_viewer.py)
   Non-existent case IDs return fake Priya Sharma data instead of 404. Add `?mode=demo` query param; without it return 404. **15 min.**

---

## 🟡 P1 — Next 2 Weeks (Pilot-Customer Blockers)

### Business model reality check ($297 vs $497)

**The pricing doc `STRIPE_SAAS_PRICING.md` assumes GHL $497 SaaS Pro for rebilling-with-markup. You're on $297.** This means:

| What you CAN do on $297 | What you CANNOT do on $297 |
|---|---|
| ✅ Create sub-accounts for firms | ❌ GHL SaaS Configurator (rebill Stripe at markup) |
| ✅ Install snapshot programmatically | ❌ "Stripe → GHL → Firm Sub-Account" auto-provisioning |
| ✅ Run unlimited workflows per location | ❌ Per-firm Stripe metering via GHL |
| ✅ Send emails via Mailgun (your own) | ❌ Native GHL "Rebilling Wallet" to firms |

**Two paths forward** (pick one; don't hedge):

- **Path A (recommended for pilot 1-3 customers): Stripe direct, no GHL Configurator.**
  - Founder bills customers directly via Stripe ($497/$997/$1997 tiers)
  - Manual (or code-automated) GHL sub-account provisioning via API
  - Upgrade to $497 only when 3+ paying firms justify the ~$200/mo difference
  - Unblocks: first customer signs this month; no $200/mo spend without revenue

- **Path B: Upgrade to $497 now.**
  - ~$200/mo extra ongoing cost
  - Unlocks GHL-native SaaS Configurator (auto-provisioning on Stripe success)
  - Risk: you pay ongoing before revenue lands
  - Unblocks: smoother onboarding from day 1

**My recommendation: Path A.** Founder-led sales for first 3 customers anyway; SaaS Configurator is an optimization, not a foundation. Upgrade when firm #3 lands.

### Architecture (must land before firm #2)

**10. Tenant isolation at API layer** — highest-leverage architectural fix.
   - Add `ghl_location_id` column + index to `contacts`, `cases`, `activities`, `users`
   - Extract `tenant_id` from request header (or PIT-based auth)
   - Wrap mutating endpoints: `SELECT … WHERE id = ? AND ghl_location_id = ?`
   - Return 403 on mismatch
   - Effort: 4-6 hours. Blocks firm #2 onboarding. See Architecture Audit §1 for evidence.

**11. Documents storage layer** (P1 #8 from PRODUCTION_READINESS still holding):
   - SeaweedFS container on Railway (or S3) for raw PDFs
   - `documents` table (id, contact_id, case_id, path, sha256, uploaded_at)
   - Presigned download URLs for RCIC access
   - Currently: Typebot uploads → OCR → lost. No retrieval path.

**12. Async webhook processing** — VAPI end-of-call webhook calls GHL 5× synchronously (trust check → score → 5 GHL calls). At scale this timeouts.
   - Add `asyncio.Queue` (no new infra; Redis optional later)
   - Webhooks enqueue + 202 immediately
   - Background worker drains; DLQ for failures
   - Effort: 4-6 hours. Blocks firm #10+ reliability.

### DevOps (must land before pilot)

**13. Sentry error tracking** — 2 hr. Currently production 500s are silent.
**14. Structured JSON logging + correlation IDs** — 4 hr. Essential for debugging across FastAPI → GHL → Postgres.
**15. Initial Alembic migration + CI gate** — 2 hr. Currently `metadata.create_all()` runs on startup with zero versioning. Any schema change is untracked + unrollback-able.
**16. Staging environment on Railway** — 2 hr. Currently prod IS the canary.
**17. GitHub branch protection** — 30 min. Currently direct-to-main possible.
**18. `rollback.sh`** — 1.5 hr. Founder has no one-command revert.
**19. Slack/email alert on nightly smoke test failure** — 1 hr.

### Compliance deep cuts

**20. Consent capture** — Add `consent_basis` + `consent_timestamp` to contact intake. CASL & PIPEDA require audit trail.
**21. Data residency** — verify Railway Postgres region. If US-East, migrate to Canadian region (ca-central-1 equivalent) OR document in privacy policy.
**22. Webhook signature verification: remove feature flag** — [`app/services/webhook_security.py:30`](neuronx-api/app/services/webhook_security.py). Currently `VERIFY_WEBHOOKS=false` bypasses Ed25519/HMAC check entirely. Make mandatory; fail startup if secret missing.
**23. Rotate `ADMIN_API_KEY`, `.tokens.json`, PITs** — quarterly cadence, documented.

### UX (pilot polish)

**24. Add `/terms` and `/privacy` real pages** — currently SPA returns index.html → hidden 404. Blocks Stripe verification + legal exposure.
**25. Differentiate website CTAs** — every button goes to same GHL calendar. Book-demo vs self-serve-trial need distinct routes.
**26. Case viewer: strict 404 for missing cases** — don't fall back to fake demo data when real case ID misses.

---

## 🟢 P2 — Month 2 (Scale Enablers)

- God objects: `case_service.py` (572 LOC), `doc_ocr_service.py` (468), `typebot.py` (429), `webhooks.py` (393) → split per §Refactor below
- Pydantic `extra = "forbid"` on all request models
- DB indexes: `activities(activity_type, created_at)`, `cases(contact_id, stage)`, `processed_webhooks(source, processed_at)` — Perf Audit §quick wins
- Connection pool: `pool_size=5 → 20, max_overflow=10 → 20` at [`app/database.py:45`](neuronx-api/app/database.py)
- GHL contact cache (in-memory LRU, 5-min TTL) in [`ghl_client.py`](neuronx-api/app/services/ghl_client.py)
- Static assets: `cache-control: public, max-age=2592000` for `/static/*`
- Frontend version bump: [`neuronx-web/package.json`](neuronx-web/package.json) `1.1.0 → 1.1.1`
- Dependabot: `.github/dependabot.yml` for Python + Node
- Docker base image pin by digest
- Rate limiter by auth tier (public 20/min, webhook exempt-if-signed, admin 200/min)
- Feature flag system (simple DB-backed, not LaunchDarkly)
- Compliance log file mode `0o600` + rotation

---

## 🏗️ Architectural Recommendations (Ranked)

### ✅ Keep doing

- **GHL as SoT for contacts/pipeline/calendar, Postgres for cases/activities** — clean boundary, well-evidenced in code
- **YAML-config-driven scoring/programs/tenants** — adding a program is a 10-line yaml change
- **Minimalist stack (no n8n, Temporal, Paperless-ngx)** — 876 tests prove Python is enough
- **Idempotency table + DLQ** — correct, working
- **Typebot config-driven multi-tenancy** — `/form/{slug}/onboarding` + `tenants.yaml` scales cleanly

### ⚠️ Revisit before firm #10

- **Shared GHL token** — single `.tokens.json` = 50 firms lose API access if one gets revoked. Move to per-firm PITs (you already have `.pit-tokens.json` pattern; extend it)
- **Email templates in GHL location (not per-firm)** — 26 templates in VMC. Second firm: reuse or duplicate? Neither scales well. Move to `email_templates/{firm_slug}/` + sync on provisioning
- **Single uvicorn process** — no HA. Run 2-4 workers behind Railway LB
- **Railway Postgres connection limit** — at $30/mo tier, ~30 connections. We'd exhaust at 10 firms with current pool settings

### 🚨 Change now (blocks growth)

- **Tenant isolation** — see P0 #10 above
- **PIPEDA deletion job** — see P0 #6 above
- **Webhook signature enforcement** — see P1 #22 above

### ❌ Things NOT to build

1. **Own CRM replacing GHL** — 6 months engineering, 0 revenue, 500k firms already on GHL
2. **Per-firm Typebot instances** — already multi-tenant via config; spawning 50 instances = 50× cost, no upside
3. **Zendesk-style ticket system** — GHL email + Slack is free
4. **Custom BI (Superset, Metric)** — Metabase is 90% of what's needed; defer to Scale tier
5. **Self-hosted k8s / docker compose** — Railway at $50-80/mo is 0.1% of revenue; staying managed until 100 firms

### 🧪 Refactor candidates (when you have 2-hour slots)

| File | Current LOC | Split into |
|---|---|---|
| `app/services/case_service.py` | 572 | `case_state_machine.py` + `case_timeline.py` + `case_checklist.py` |
| `app/services/doc_ocr_service.py` | 468 | `ocr_extraction.py` + `ocr_sync.py` + `field_extractor.py` |
| `app/routers/typebot.py` | 429 | `typebot_field_mapper.py` + `typebot_contact_resolver.py` |
| `app/routers/webhooks.py` | 393 | `webhook_dispatcher.py` + `lead_scorer_webhook.py` + `payment_webhook.py` |
| `app/routers/clients.py` | 417 | extract `ircc_form_mapper.py` |

---

## 💰 Cost at 50-Firm Scale (corrected for $297 plan)

| Component | Monthly | At 50 firms |
|---|---|---|
| GHL Agency ($297 plan OR $497) | $297 / $497 | same — shared |
| Railway FastAPI | $15 | ~$50 with 2-4 workers |
| Railway Postgres (need to upgrade from hobby) | $12 → $30 | $30 |
| Railway Typebot (builder + viewer) | $14-28 | $28 |
| Railway Metabase | $7-12 | $12 |
| Vercel (hobby → Pro at scale) | $0 → $20 | $20 |
| **VAPI (biggest variable)** | $0.25/min | **$6,250** (2000 min/firm/mo × 50) |
| Ollama Cloud OCR | $0.01/call | $500 |
| Stripe fees (2.9%) | — | $1,305 |
| **Total COGS** | | **~$8,490 ($297) or $8,690 ($497)** |

**Revenue at 50 firms (10 Starter × $497, 30 Growth × $997, 10 Scale × $1,997) = $54,850/mo**

**Gross margin: 84.5% on $297 plan, 84.2% on $497 plan.** The $200/mo upgrade cost is noise at scale. **Real lever is VAPI volume pricing — lock <$0.20/min before hitting 10 firms.**

---

## 📋 Specific Recommendations Matrix

### Do this week (P0, in priority order)
```
[ ] 1. Rotate VAPI, Anthropic, Skyvern, Vercel, GitHub tokens (you — vendor dashboards)
[ ] 2. Clean .env.example to placeholders (me — 15 min)
[ ] 3. Add X-Admin-Key to /clients/* (me — 1 hr)
[ ] 4. Remove admin-key fallback, set in Railway env (me — 15 min)
[ ] 5. Fix stale pipeline_id in /analytics/pipeline (me — 15 min)
[ ] 6. Disable rate limiter in TESTING mode (me — 30 min)
[ ] 7. Fix case viewer demo-fallback (me — 15 min)
[ ] 8. Add CASL unsubscribe to template generator + re-upload 26 (me — 1 hr)
[ ] 9. Link 26 templates to 24 workflows (you — WORKFLOW_TEMPLATE_LINKING.md, 30 min)
[ ] 10. Add PIPEDA disclosure to VAPI firstMessage (you — VAPI UI, 10 min)
```

### Do next 2 weeks (P1, in priority order)
```
[ ] 11. Tenant isolation (ghl_location_id scoping) — 4-6 hr
[ ] 12. PIPEDA deletion endpoint + APScheduler job — 2 hr
[ ] 13. Sentry + JSON logging + correlation IDs — 6 hr
[ ] 14. Alembic initial migration + CI gate — 3 hr
[ ] 15. Staging environment on Railway — 2 hr
[ ] 16. rollback.sh + branch protection — 2 hr
[ ] 17. Documents layer (SeaweedFS + documents table) — 1 day
[ ] 18. /terms, /privacy real pages — 2 hr
[ ] 19. Webhook signature enforcement (remove feature flag) — 1 hr
[ ] 20. Consent capture on form intake — 2 hr
[ ] 21. Decide Path A (Stripe direct) vs Path B (upgrade $497) — you
```

### Do month 2 (P2)
```
[ ] 22-30. God-object refactor, indexes, pool tuning, cache layer, feature flags, Dependabot, frontend version bump, etc.
```

---

## 🎯 Definition of Ready (updated)

### ✅ Investor demo ready — conditional on P0 #1-9
- Rotate secrets + close IDOR + fix admin fallback → ZERO prod exposure
- Fix stale pipeline_id → Metabase pipeline chart shows data
- Tests pass in CI → deploy confidence
- 26 templates linked to workflows → email demo works

### ⚠️ First paying customer ready — P0 complete + these P1s
- Tenant isolation (#11)
- PIPEDA deletion (#12)
- Sentry + logging (#13)
- Migrations + staging + rollback (#14-16)
- Documents layer (#17)
- Legal pages (#18)
- Stripe path A or B chosen (#21)

### 📊 Scale-ready (10+ firms)
- Refactored god objects
- Connection pool tuned
- Async webhook queue
- Per-firm PITs
- CDN/cache headers
- Load-tested at 5x

---

## 🔗 Source reports (for deep dives)

Each sub-agent's full report is in chat history above. Key sections referenced throughout this synthesis:

- **UX Audit** — 7 journey reverification + new UX bugs
- **Security Audit** — 14 findings, 5 P0, 9 P1/P2
- **Code Audit** — 876 tests actual, 79.4% cov, top refactor candidates
- **Architecture Audit** — tenant isolation deep dive, cost modelling, anti-recommendations
- **DevOps Audit** — Sentry/Alembic/staging gaps, 90-day action plan
- **Performance Audit** — measured latencies, indexes, scale bombs at 5x/10x/50x

---

**Next session start: work the P0 list top-down. I'll execute #2-8 autonomously; you handle #1 (vendor key rotations), #9 (workflow linking), #10 (VAPI UI).**
