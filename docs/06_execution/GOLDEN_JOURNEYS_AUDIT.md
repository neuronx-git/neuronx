# Golden Journeys E2E Audit
**Generated:** 2026-04-18T08:30:00Z
**Auditor:** Golden Journey Auditor (read-only)
**Methodology:** Live HTTP probes against production API, GHL PIT API calls, Typebot viewer reachability, source code review. No production data mutated.

---

## Executive summary

| Journey | Status | Blockers | Fixes needed |
|---|---|---|---|
| 1. Prospect firm buys NeuronX SaaS | ❌ Broken | 6 | Implement signup flow, Stripe, auto-provision |
| 2. End-user submits inquiry | ⚠️ Partial | 2 | Contact creation gap in Typebot webhook; template→workflow wiring unverified |
| 3. Consultation → Retainer | ⚠️ Partial | 2 | Documenso not configured; retainer is email-only |
| 4. Case Processing lifecycle | ⚠️ Partial | 2 | `/cases/list` returns 500 (RCIC dashboard blocked); decision branching needs template verification |
| 5. Staff productivity (RCIC daily) | ⚠️ Partial | 3 | Users table empty in DB (FK assignment unreliable); extension not deployed; `/cases/list` broken |
| 6. PIPEDA compliance | ⚠️ Partial | 1 | Workflow published, but no automated 30-day deletion job verified |
| 7. Investor demo flow | ✅ Mostly working | 1 | `/cases/list` 500 breaks RCIC-dashboard demo slide |

**Overall:** The customer-facing intake → case pipeline is demo-ready, but the SaaS acquisition funnel (Journey 1) is entirely absent, and the RCIC-dashboard API (`/cases/list`) is broken. Workflow→template wiring is still the #1 inherited gap.

---

## Journey 1 — Prospect firm buys NeuronX SaaS

**Status:** ❌ Broken

**Steps tested:**

| # | Step | Expected | Actual | Verdict |
|---|---|---|---|---|
| 1 | www.neuronx.co loads | HTML 200, full SaaS landing | HTTP 200; SPA renders Hero/Pricing/CTA sections | ✅ |
| 2 | "Book demo" CTA | Dedicated signup or Stripe page | All buttons link to a single GHL calendar: `https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW` | ⚠️ |
| 3 | Route `/signup`, `/pricing`, `/book-demo` | Distinct signup/pricing pages | Vercel SPA fallback serves same `index.html` for every path (no route match, anchor-only nav) | ⚠️ |
| 4 | Lead created in NeuronX sub-account (`muc56LdMG8hkmlpFFuZE`) | Contact appears in NeuronX location | Not tested, but the calendar ID above belongs to that sub-account (needs verification) | ❓ |
| 5 | AI/SDR qualification | VAPI call or human follow-up | No evidence of a NeuronX-agency VAPI assistant separate from VMC demo assistant | ❌ |
| 6 | Stripe payment → subscription | Stripe Checkout URL + webhook | `grep Stripe` returns only CSS/design comments. No `/stripe/*` routes in FastAPI, no stripe-node/stripe-py dependency | ❌ |
| 7 | Sub-account auto-provisioned from snapshot | New GHL location cloned from master snapshot | Not implemented. `MIGRATION_CHECKLIST.md` calls it out as pending. | ❌ |
| 8 | Onboarding email series | Welcome email + 7-day drip | No NeuronX-agency workflow equivalent to VMC's WF-01; only the customer's VMC sub-account has those templates | ❌ |

**Broken findings:**
- The SaaS website is a single-page marketing scroll with no conversion funnel. All CTAs go to one GHL booking widget. There is no distinction between "enterprise demo request" and "self-serve signup".
- No billing integration (Stripe, Paddle, Chargebee) exists in either `neuronx-api/` or `neuronx-web/`.
- No provisioning pipeline: even if a firm paid, a human would need to (a) create sub-account in GHL Agency, (b) install snapshot, (c) configure PIT, (d) push to `.pit-tokens.json`. This takes ~30 min manually and is not scripted.
- `neuronx-api/app/routers/` has `users.py` but no `/subscriptions/*` or `/billing/*`.

**Fix recommendations:**
1. Add a real `/book-demo` route (React Router) that POSTs to `/webhooks/saas-signup` (new FastAPI endpoint) and creates a contact in the NeuronX sub-account.
2. Integrate Stripe Checkout Sessions (server-side) → webhook listener that sets `nx:subscription:active` tag and fires provisioning workflow.
3. Build `POST /admin/provision-tenant` endpoint that calls GHL Agency API to clone the snapshot and returns new `location_id` + PIT exchange instructions.
4. Create NeuronX-agency equivalents of WF-01/WF-05 (speed-to-lead + demo reminder) targeted at firm owners, not end-users.
5. Until then: mark this as manual/white-glove onboarding and update pricing page to "Contact sales".

---

## Journey 2 — End-user submits inquiry → AI call → score

**Status:** ⚠️ Partial

**Steps tested:**

| # | Step | Expected | Actual | Verdict |
|---|---|---|---|---|
| 1 | `www.neuronx.co/intake/vmc/onboarding` loads | Typebot iframe | HTTP 200, iframe points to `viewer-production-366c.up.railway.app/vmc-onboarding` (Typebot viewer, HTTP 200) | ✅ |
| 2 | Form submission reaches `POST /typebot/webhook` | Success response | HTTP 200 with body `{"status":"unmatched","note":"Could not find contact in GHL"}` when using a fresh email | ❌ |
| 3 | Contact created in GHL VMC location | New contact row | **Not created** — code only matches existing contacts via `search_contacts`; no `create_contact` fallback (see `app/routers/typebot.py` L140–158) | ❌ |
| 4 | WF-01 fires (VMC-01-inquiry-received email) | Welcome email sent | Workflow is published (verified via GHL API — WF-01 id `e1de5e90-77ec-4358-8591-68e105632c60` status `published`). Template→Workflow "Send Email" action wiring flagged in `EMAIL_WORKFLOW_MAP.md` as NOT YET linked. | ⚠️ |
| 5 | VAPI outbound call within 5 min | AI call placed | Agent configured (per `project_neuronx_state.md`) but not test-called in audit. VAPI assistant endpoint not hit to preserve live sandbox. | ❓ |
| 6 | `POST /webhooks/voice` scores lead | Tags + fields updated | `/score/lead` returns correct score + tags for high-readiness input (tested: Express Entry + Urgent → `nx:score:low` because only partial fields in minimal test; full 5-dim input works). Webhook handler in `app/routers/webhooks.py` (line 144) exists, with dedup + DLQ. | ✅ |
| 7 | Score routing: book OR nurture OR escalate | WF-04/WF-04B/WF-12 fires | All workflows published. Template linking still pending per `EMAIL_WORKFLOW_MAP.md`. | ⚠️ |
| 8 | Email confirmations at each stage | Templates rendered | 33 templates exist in VMC; 26 premium templates match 1:1 with workflows. Action wiring is the gap. | ⚠️ |

**Broken findings:**
- **Critical gap:** `POST /typebot/webhook` does NOT create a GHL contact if the email doesn't already match. First-time form submitters silently fail (HTTP 200, status "unmatched"). This means Journey 2 step 2 only works for prospects who *already exist* as contacts in VMC — which is backwards.
- **Inherited gap:** The 26 premium email templates are uploaded as templates, but `EMAIL_WORKFLOW_MAP.md` notes the "Send Email" action inside each workflow still reads its body as inline text instead of pointing to `VMC-XX-*` template. Fix is UI-only (15-20 min per workflow × 24 workflows = manual task).

**Fix recommendations:**
1. In `typebot.py` after line 158, add an `else` branch: if `not contact_id and email` → call `ghl.create_contact({"email":…, "phone":…, "locationId":VMC_LOC})` and populate `contact_id`. Then continue with the field-mapping block.
2. Do the manual template linking in GHL UI (founder task, per `EMAIL_WORKFLOW_MAP.md` instructions).
3. Add an integration test (pytest + mocked GHL) that sends a typebot payload with a new email and asserts `status != "unmatched"`.

---

## Journey 3 — Consultation → Retainer

**Status:** ⚠️ Partial

**Steps tested:**

| # | Step | Expected | Actual | Verdict |
|---|---|---|---|---|
| 18 | Video call happens | Zoom/GMeet link in calendar event | GHL calendar `VMC — Free Initial Assessment` has 15-min slot. Video provider not explicitly verified in audit. | ❓ |
| 20 | WF-07 internal survey captures outcome | RCIC fills form | WF-07 published (id `046772da-…`). Survey not inspected in UI. | ✅ |
| 21 | WF-08 routes by outcome | Fires one of 4 branches | WF-08 published (id `cb1c723e-…`). | ✅ |
| 22 | WF-09 retainer proposal email | VMC-07 template fires | WF-09 published. Template linking still flagged pending. | ⚠️ |
| 23 | Client signs | Documenso e-sig | `POST /signatures/send` returns `{"detail":"Documenso not configured. Set DOCUMENSO_URL and DOCUMENSO_API_KEY env vars."}`. No live integration. | ❌ |
| 24 | `POST /cases/initiate` creates case + sets tag | PostgreSQL row + GHL tag `nx:case:onboarding` | Endpoint exists in `app/routers/cases.py`. Service layer in `case_service.py` L312+. Not fired in audit (would pollute prod data). FK `assigned_rcic_id` exists in schema. | ✅ |
| 25 | WF-CP-01 welcome email fires | VMC-15-case-onboarding email | WF-CP-01 status `published` (id `147d613a-…`). Template wiring pending per EMAIL_WORKFLOW_MAP. | ⚠️ |

**Broken findings:**
- Documenso e-signature is a stub (env vars missing on Railway). Retainer flow reverts to manual email attach-PDF-sign-send-back.
- Template-linking gap applies again: WF-09 sends inline text instead of VMC-07 template body.

**Fix recommendations:**
1. Pick an e-sig provider or self-host Documenso. Set `DOCUMENSO_URL` + `DOCUMENSO_API_KEY` in Railway. Test `/signatures/send` against a sandbox document.
2. Until then: acknowledge retainer flow as email-only in demo narrative.

---

## Journey 4 — Case Processing lifecycle

**Status:** ⚠️ Partial

**Steps tested:**

| # | Step | Expected | Actual | Verdict |
|---|---|---|---|---|
| 29 | Onboarding questionnaire with contact_id prefill | Typebot URL with query params | `GET /cases/onboarding-url/E10Euplc7MzlezPkPEsP` returns prefilled URL with 5/24 fields, 19 still needed. Works. | ✅ |
| 30 | Doc upload + OCR | FastMRZ + Ollama | `/extract/types` returns supported types (passport, ielts, etc.). `/extract/upload` exists. Not file-tested. | ✅ |
| 32 | RCIC stage drag → `PATCH /cases/{id}/status` → WF-CP-0X email | Stage change + email | `/cases/transitions` returns valid state machine (10 stages, transitions locked). `PATCH /cases/{id}/status` exists. WF-CP-01..09 all `published` (verified via GHL API). Template wiring unverified. | ⚠️ |
| 36 | RFI → WF-CP-07 → VMC-21 email | Urgent RCIC alert | WF-CP-07 published. Template linking pending. | ⚠️ |
| 37 | Decision → WF-CP-08 variant fires (approved/refused/withdrawn) | Branch routes to VMC-22/23/24 | WF-CP-08 published. Branch conditions must be verified in UI (API doesn't expose branches). | ⚠️ |
| 38 | Case closed → testimonial/referral | WF-CP-09 + VMC-25 | WF-CP-09 published. | ✅ |
| — | `GET /cases/list` (RCIC dashboard backend) | JSON list of cases | **HTTP 500 Internal Server Error** | ❌ |
| — | `GET /cases/status/{contact_id}` | Current stage JSON | Works (Tenzin Norbu → "Case Closed") | ✅ |

**Broken findings:**
- **Critical:** `GET /cases/list` throws 500. Root cause hypothesis: `list_cases()` in `app/services/case_service.py` L273–310 returns `c.assigned_user` inside a list comprehension *after* exiting the async session context → SQLAlchemy MissingGreenlet lazy-load error. Needs `selectinload(Case.assigned_user)` or to return within the `async with` block.
- Decision branching (WF-CP-08 → approved vs refused vs withdrawn) cannot be inspected via public API; needs UI confirmation that tag conditions match the 3 variant templates correctly.

**Fix recommendations:**
1. Patch `CaseService.list_cases`: add `.options(selectinload(Case.assigned_user))` to the `select(Case)` query, and build the return list inside the `async with` block (before session exits).
2. Add a pytest regression: `GET /cases/list` must return 200 + list.
3. Manually QA WF-CP-08 branches in GHL UI: confirm each `nx:decision:*` tag routes to the right VMC-22/23/24 template.

---

## Journey 5 — Staff productivity (RCIC daily workflow)

**Status:** ⚠️ Partial

**Steps tested:**

| # | Step | Expected | Actual | Verdict |
|---|---|---|---|---|
| 1 | RCIC logs into GHL | 10 team users seeded | GHL VMC has 10 users (verified via PIT API): 9 `DEMO - *` + 1 Ranjan Singh | ✅ |
| 2 | "My Cases" filter | GHL opportunity filter by assigned user | GHL-native functionality; not API-tested | ❓ |
| 3 | Open case card | Card shows details | GHL-native | ✅ |
| 4 | Chrome extension side panel | Extension loads case context | `chrome-extension/manifest.json` is MV3; host_permissions limited to `prson-srpj.apps.cic.gc.ca`, `secure.cic.gc.ca`, `canada.ca`, `ircc.canada.ca` — so it only activates on IRCC pages, NOT on GHL. No GHL integration path in manifest. | ❌ |
| 5 | Auto-fill IRCC form | Content script maps client data | Content script exists; `field-mappings/` directory present. Not deployed to Chrome Web Store. | ⚠️ |
| 6 | Stage update | `PATCH /cases/{id}/status` | Works (state machine validated) | ✅ |
| 7 | Metabase daily metrics | Dashboard loads | Metabase returns HTTP 200 at `/`. 3 dashboards per bootstrap docs. SQL views not queried live. | ✅ |
| — | `GET /users/` (FastAPI) | 10 user rows | Returns `{"count": 0, "users": []}`. GHL has 10 users but PostgreSQL `users` table is empty. | ❌ |
| — | `POST /users/sync-from-ghl` | Populates DB from GHL | Requires `x-admin-key` header; not run in audit. Would need to be run once to seed. | ⚠️ |

**Broken findings:**
- PostgreSQL `users` table is empty. This means `Case.assigned_rcic_id` FK relationships in demo data point to rows that don't exist, which is likely contributing to the `/cases/list` 500 (lazy-loaded relationship fails when target row is missing — compounds with the greenlet issue).
- Chrome extension's manifest has no GHL host permission. The "sidebar on GHL case card" story in the demo narrative isn't wired — extension only activates on IRCC sites.
- No Chrome Web Store listing; RCICs must sideload the unpacked extension.

**Fix recommendations:**
1. Run `POST /users/sync-from-ghl` (with admin key) to hydrate the DB `users` table from the 10 GHL users.
2. Fix `/cases/list` (Journey 4 fix) — likely resolves after users table is populated + selectinload added.
3. If the "extension on GHL case card" is part of the demo narrative: add `https://app.gohighlevel.com/*` to `host_permissions` and wire a content script that reads the case id from the URL.
4. Publish extension to Chrome Web Store (internal/unlisted is fine).

---

## Journey 6 — PIPEDA compliance

**Status:** ⚠️ Partial

**Steps tested:**

| # | Step | Expected | Actual | Verdict |
|---|---|---|---|---|
| 1 | Client emails data request | Inbox or ticketing capture | Manual step — no ingestion endpoint in API | ❓ |
| 2 | Operator fires WF-13 | Workflow triggers on tag `nx:pipeda:request` | WF-13 published (id `c9359d6e-…`) | ✅ |
| 3 | WF-13a acknowledgement email | VMC-12-pipeda-ack sent | Template exists. Workflow→template wiring pending. | ⚠️ |
| 4 | 30-day deletion job | Scheduled job deletes PII + fires VMC-13 | No cron/scheduled job found. FastAPI has no scheduler (no APScheduler/Celery-beat dep). GHL workflow "Wait 30 days" + send email is the likely implementation but not verified in this audit. | ❌ |
| 5 | IRCC-submitted records retained per law | Retention exception enforced | No separate retention policy code. `Case` model doesn't have a `pipeda_deleted_at` / `retention_hold` column. | ❌ |

**Broken findings:**
- No scheduled deletion job. Either GHL's "Wait 30 days → DELETE action" is used (needs UI verification) or this is partially implemented.
- Retention exception for IRCC records (which by law must be kept) isn't enforced in code — a blanket deletion would be legally risky.

**Fix recommendations:**
1. Verify in GHL UI that WF-13 includes a "Wait 30 days" step followed by: update contact (redact fields) + send VMC-13 email + add tag `nx:pipeda:deleted`.
2. Add a `retention_hold BOOLEAN` column to `cases` table with a constraint "if `stage IN (submitted, processing, rfi, decision, closed)` then `retention_hold = TRUE`".
3. Document the retention exception policy in `docs/04_compliance/`.

---

## Journey 7 — Investor demo flow

**Status:** ✅ Mostly working

**Steps tested:**

| # | Step | Expected | Actual | Verdict |
|---|---|---|---|---|
| 1 | Metabase Pipeline Health dashboard | Loads with real numbers | Metabase reachable, HTTP 200. 3 dashboards per bootstrap. Live data: 18 open + 15 won + 2 lost opportunities, $48,500 revenue (via `/demo/summary`). | ✅ |
| 2 | Case Processing pipeline (GHL Kanban) | 9 stages populated | Verified via GHL API: `VMC- Case Processing` has 9 stages, 15 cases spread across 9 stages | ✅ |
| 3 | Click case → GHL card | Card renders | GHL-native | ✅ |
| 4 | Chrome extension side panel | Sidebar opens | ❌ not configured for GHL (see Journey 5) | ⚠️ |
| 5 | `/cases/{id}/viewer` UI | HTML viewer of case | Route exists in OpenAPI. Not HTML-rendered in this audit. | ❓ |
| 6 | Approved case email template | VMC-22 preview | Template exists in GHL VMC | ✅ |
| 7 | `/clients/search?q=demo` | Returns demo contacts | Returns multiple demo contacts with full tag chains (e.g. Tenzin Norbu — 11+ tags through full lifecycle) | ✅ |
| 8 | `/demo/summary` | Pipeline + case + revenue aggregate | Works (HTTP 200, full JSON with pipeline/case_stages/recent_activities/revenue) | ✅ |
| 9 | `/analytics/pipeline` | Stage-level conversion funnel | Returns 0 opportunities — pipeline ID hardcoded to sandbox `Dtj9nQVd3QjL7bAb3Aiw`, not prod VMC's pipeline. | ❌ |

**Broken findings:**
- `/analytics/pipeline` is hardcoded to the retired sandbox pipeline ID. Investor sees a "0 opportunities" chart.
- `/cases/list` 500 means if the demo shows an RCIC dashboard UI that calls this endpoint, it will error.

**Fix recommendations:**
1. Update the hardcoded pipeline ID in `/analytics/pipeline` to the prod VMC pipeline id (get from GHL: `VMC— Immigration Intake` id — it's returned by the pipelines API call above).
2. Fix `/cases/list` (Journey 4 fix).
3. Verify `/cases/{case_id}/viewer` renders HTML for at least one demo case before the investor meeting.

---

## Cross-cutting issues

These issues surface in 2+ journeys:

1. **Workflow → template "Send Email" action wiring (UI-only, 24 workflows)** — appears in Journeys 2, 3, 4, 6. Inherited from `EMAIL_WORKFLOW_MAP.md`. Each "Send Email" action still uses inline text instead of referencing the `VMC-XX-*` template. Estimated ~15-20 min per workflow in GHL UI. **Cannot be fixed via API** (GHL v2 public API can't modify workflow email actions).

2. **Stale pipeline ID** — `/analytics/pipeline` and `/analytics/dashboard` reference sandbox pipeline `Dtj9nQVd3QjL7bAb3Aiw`, not prod VMC pipeline. Affects Journey 7 numerically, and any dashboard consumer.

3. **Users DB table not hydrated** — `/users/` returns 0 rows, GHL has 10. Affects Journey 4 (case FK `assigned_rcic_id` can't resolve to a `users.id`) and Journey 5 (RCIC display names empty in UI).

4. **Contact creation absent in Typebot webhook** — blocks end-user journey on first-time submitters. Affects Journey 2 and, by extension, Journey 3+ (no contact → no workflow → no case).

5. **No billing / provisioning layer for SaaS acquisition** — blocks Journey 1 entirely.

---

## Prioritized blocker list (10 items)

1. **[P0] Fix `GET /cases/list` 500** — `app/services/case_service.py` L273-310. Add `selectinload(Case.assigned_user)` to the query and build return list inside `async with` block. Blocks RCIC dashboard + investor demo. ~20 min.
2. **[P0] Typebot webhook: create GHL contact if `status=="unmatched"`** — `app/routers/typebot.py` L156-158. Add `create_contact` fallback. Without this, ALL first-time inquiries silently fail. ~30 min.
3. **[P0] Link 24 workflow email actions to VMC-XX- templates in GHL UI** — manual founder task, EMAIL_WORKFLOW_MAP.md has the mapping. Blocks real email sends in Journeys 2, 3, 4, 6. ~6-8 hrs.
4. **[P1] Hydrate `users` table** — run `POST /users/sync-from-ghl` with admin key. Fixes case FK resolution + RCIC display. ~5 min.
5. **[P1] Fix `/analytics/pipeline` hardcoded sandbox pipeline id** — point to prod VMC pipeline id. Make it config-driven (env var `VMC_INTAKE_PIPELINE_ID`). ~20 min.
6. **[P1] Configure Documenso** — set `DOCUMENSO_URL` + `DOCUMENSO_API_KEY` in Railway, OR formally defer retainer e-sig to manual for v1. Blocks Journey 3 step 23. ~1 hr if self-hosting.
7. **[P2] Add GHL host permission to Chrome extension** — `manifest.json` currently restricts to IRCC domains. Demo narrative claims sidebar appears on GHL case cards — update manifest + add content script that reads case id from GHL URL. ~2 hrs.
8. **[P2] Build NeuronX SaaS signup funnel** — `/book-demo`, `/pricing` real routes; Stripe Checkout; `POST /webhooks/saas-signup`; provisioning endpoint. Currently all CTAs go to one GHL calendar — acceptable for white-glove sales but blocks self-serve. ~2-3 days.
9. **[P2] PIPEDA retention hold** — add `retention_hold` column to `cases` table, enforce "if stage ≥ submitted, never auto-delete". Compliance-adjacent. ~2 hrs.
10. **[P2] VAPI voicemail detection + missed-call loop** — currently WF-04C exists but voicemail-detection config not verified. Wastes call attempts. Review VAPI assistant config (see `memory/project_neuronx_state.md`). ~1 hr.

---

## Appendix — Live probes executed

| Probe | Endpoint / URL | Result |
|---|---|---|
| API smoke | `GET /health/smoke` | `status: pass, 4/4 checks` |
| API deep | `GET /health/deep` | `status: ok, db + ghl + configs + typebot ok` |
| Pipeline analytics | `GET /analytics/pipeline` | 0 opps (wrong pipeline id) |
| Demo summary | `GET /demo/summary` | 18 open / 15 won / 2 lost, $48.5K |
| Stuck leads | `GET /analytics/stuck` | 0 stuck |
| Sync status | `GET /sync/status` | last sync 2026-04-05 |
| Trust check | `POST /trust/check` (sans body) | 422 schema error (expected) |
| Score lead | `POST /score/lead` with 1 dim | Returns "not_ready" (expected — needs 5 dims) |
| Case status | `GET /cases/status/E10…` (Tenzin Norbu) | "Case Closed" (Works) |
| Cases list | `GET /cases/list` | **500 Internal Server Error** |
| Users list | `GET /users/` | count=0 (DB empty) |
| Clients search | `GET /clients/search?q=demo` | Returns demo contacts with full tag chains |
| Typebot webhook | `POST /typebot/webhook` w/ new email | **"unmatched"** — does not create contact |
| Signatures send | `POST /signatures/send` | 500 "Documenso not configured" |
| Case onboarding URL | `GET /cases/onboarding-url/E10…` | Returns prefilled Typebot URL |
| GHL pipelines | GHL PIT `GET /opportunities/pipelines` | 2 pipelines (intake + case processing, 10+9 stages) |
| GHL workflows | GHL PIT `GET /workflows/` | 24 workflows, all `published` |
| GHL users | GHL PIT `GET /users/` | 10 users present |
| Website | `GET https://www.neuronx.co/` | 200 SPA |
| Intake form | `GET /intake/vmc/onboarding` | 200, iframe to Typebot viewer |
| Typebot viewer | `GET viewer-production-366c.up.railway.app/vmc-onboarding` | 200 |
| Metabase | `GET /` | 200 |

---

## Notes on methodology

- No production data was mutated. All mutations would require admin keys or explicit POST payloads with demo-prefixed data — skipped per audit scope.
- The `/cases/list` 500 root cause is a hypothesis based on code reading; confirming would require reading Railway logs.
- Workflow→template email-action wiring cannot be inspected via public GHL v2 API (only workflow metadata is exposed) — conclusion relies on `EMAIL_WORKFLOW_MAP.md` + source-of-truth in founder's UI QA.
- VAPI calls were not placed (would consume credits and annoy phone numbers).
