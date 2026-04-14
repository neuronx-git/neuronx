# NeuronX Feature Status — Working vs Non-Working

**Date**: 2026-04-14 (Updated)
**API Version**: v0.4.0
**Tests**: 700 core + 13 GHL live + 31 VAPI live = 744 total | 92.54% coverage | 0 failures
**UAT**: 6/6 scenarios PASS against production Railway

---

## WORKING FEATURES (Tested + Verified)

### Core API Infrastructure
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Health check | `GET /health` | 5 | 100% | WORKING |
| Deep health (all deps) | `GET /health/deep` | 7 | 100% | WORKING |
| Config hot-reload | `POST /admin/reload-config` | 5 | 100% | WORKING |
| OpenAPI spec | `GET /openapi.json` | 8 | 100% | WORKING |
| Root endpoint | `GET /` | 3 | 100% | WORKING |

### Webhook Processing (Inbound Events)
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| GHL webhook receiver | `POST /webhooks/ghl` | 15+ | 94% | WORKING |
| VAPI voice webhook | `POST /webhooks/voice` | 20+ | 94% | WORKING |
| Typebot form webhook | `POST /typebot/webhook` | 8 | 92% | WORKING |
| Signature webhook | `POST /signatures/webhook` | 6 | 91% | WORKING |
| Ed25519 signature verify | (internal) | 6 | 90% | WORKING |
| HMAC-SHA256 verify | (internal) | 5 | 90% | WORKING |
| Webhook deduplication | (internal) | 4 | 94% | WORKING |
| Dead letter queue | (internal) | 3 | 94% | WORKING |

### Lead Scoring (R1-R5 Assessment)
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Full R1-R5 scoring | `POST /score/lead` | 97+ | 99% | WORKING |
| Form preliminary score | `POST /score/form` | 7 | 93% | WORKING |
| Score → GHL tag mapping | (internal) | 30+ | 99% | WORKING |
| Complexity keyword detection | (internal) | 15+ | 99% | WORKING |
| All 5 outcomes (standard/urgent/complex/not_ready/disqualified) | (internal) | 20+ | 99% | WORKING |

### Trust Boundary Enforcement
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Transcript compliance check | `POST /trust/check` | 46+ | 93% | WORKING |
| 6 escalation trigger categories | (internal) | 12+ | 93% | WORKING |
| 3 AI violation categories | (internal) | 9+ | 93% | WORKING |
| Compliance audit logging | (internal) | 4 | 92% | WORKING |

### Document OCR Extraction
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Upload + extract | `POST /extract/upload` | 12+ | 100% | WORKING |
| Upload + sync to GHL | `POST /extract/upload-and-sync` | 4 | 100% | WORKING |
| Supported types listing | `GET /extract/types` | 3 | 100% | WORKING |
| Passport MRZ (FastMRZ) | (internal) | 6 | 98% | WORKING |
| Claude vision OCR (7 doc types) | (internal) | 8 | 98% | WORKING |
| File dedup cache (SHA-256) | (internal) | 3 | 100% | WORKING |

### Multi-Tenant Forms
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Branded form serving | `GET /form/{tenant}/{slug}` | 13 | 100% | WORKING |
| Form listing per tenant | `GET /form/{tenant}` | 3 | 100% | WORKING |
| Tenant branding injection | (internal) | 5 | 100% | WORKING |

### Case Management
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Case initiation | `POST /cases/initiate` | 6 | 93% | WORKING |
| Case stage update | `POST /cases/stage` | 4 | 93% | WORKING |
| Case status check | `GET /cases/status/{id}` | 3 | 93% | WORKING |
| Dependents CRUD | `POST/GET/PUT/DELETE /dependents/` | 8 | 100% | WORKING |
| Case ID generation (NX-YYYYMMDD-xxx) | (internal) | 3 | 95% | WORKING |

### Consultation Prep
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Briefing generation | `POST /briefing/generate` | 6 | 100% | WORKING |
| Pre-consult assembly | (internal) | 8 | 100% | WORKING |

### Analytics & Pipeline
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Dashboard metrics | `GET /analytics/dashboard` | 4 | 100% | WORKING |
| Pipeline view | `GET /analytics/pipeline` | 3 | 100% | WORKING |
| Stuck leads | `GET /analytics/stuck` | 3 | 100% | WORKING |

### Document Generation
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Assessment report | `POST /documents/assessment` | 4 | 94% | WORKING |
| Checklist generation | `POST /documents/checklist` | 3 | 94% | WORKING |
| IRCC form auto-fill | `POST /documents/ircc-fill` | 11 | 79% | WORKING |
| IRCC field discovery | `GET /documents/ircc-fields/{key}` | 5 | 79% | WORKING |
| IRCC forms listing | `GET /documents/ircc-forms/{prog}` | 4 | 79% | WORKING |

### Data Sync
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Full GHL sync | `POST /sync/full` | 5 | 64% | WORKING |
| Sync status | `GET /sync/status` | 4 | 64% | WORKING |

### Demo / Seeding
| Feature | Endpoint | Tests | Coverage | Status |
|---------|----------|-------|----------|--------|
| Seed demo contacts | `POST /demo/seed` | 5 | 100% | WORKING |
| Clear demo data | `POST /demo/clear` | 3 | 100% | WORKING |

### Configuration System (YAML-driven)
| Config File | Purpose | Tests | Status |
|-------------|---------|-------|--------|
| scoring.yaml | R1-R5 weights, thresholds | 26+ | WORKING |
| trust.yaml | Escalation triggers, violations | 20+ | WORKING |
| programs.yaml | 8 immigration programs | 5 | WORKING |
| questionnaires.yaml | 68 questions across programs | 4 | WORKING |
| ircc_field_mappings.yaml | PDF field mappings | 6 | WORKING |
| tenants.yaml | Multi-tenant branding | 8 | WORKING |
| case_emails.yaml | Email templates | 2 | WORKING |

### Database Models (PostgreSQL)
| Model | Purpose | Tests | Status |
|-------|---------|-------|--------|
| Contact | GHL contact mirror | 4 | WORKING |
| Opportunity | Pipeline tracking | 2 | WORKING |
| Case | Post-retainer lifecycle | 5 | WORKING |
| Activity | Audit trail | 3 | WORKING |
| Signature | E-signature tracking | 2 | WORKING |
| Dependent | Family members | 3 | WORKING |
| ProcessedWebhook | Idempotency | 4 | WORKING |
| DeadLetterQueue | Failed webhook retry | 3 | WORKING |
| SyncLog | Sync state | 2 | WORKING |

---

## WORKING BUT WITH CAVEATS

| Feature | Status | Caveat |
|---------|--------|--------|
| GHL API integration | WORKING (mocked) | Real GHL calls blocked by sandbox rate limits (25/10s). All tested via mocks. Contract tests validate payload shapes. |
| VAPI voice integration | WORKING (mocked) | Real VAPI calls cost money. All tested via mocked webhook payloads. |
| Claude OCR extraction | WORKING (mocked) | Real Claude API costs credits. Tested via mocks + Promptfoo weekly eval (4 test cases). |
| E-signature (Documenso) | WORKING (mocked) | Documenso calls mocked. Real Documenso instance on Railway not tested in CI. |
| Typebot form generation | WORKING (mocked) | Typebot API calls mocked. Real Typebot integration tested manually only. |
| IRCC PDF auto-fill | WORKING (partial) | PDFs that are encrypted get HTML data sheet fallback. Works for 5/12 fillable PDFs, 4 encrypted use data sheet. |
| Webhook signature verification | WORKING (disabled in dev) | VERIFY_WEBHOOKS=false in test/dev. Tests verify both enabled/disabled paths. |

---

## NOT WORKING / BLOCKED

| Feature | Reason | Workaround | Unblock Condition |
|---------|--------|------------|-------------------|
| **GHL email sending** | Developer sandbox blocks email | None — emails silently fail | Production GHL account ($297/mo) |
| **GHL SMS sending** | Developer sandbox blocks SMS | None | Production GHL account |
| **GHL phone calls** | Developer sandbox blocks calls | None | Production GHL account |
| **Typebot file upload** | S3_ENDPOINT misconfigured on Railway | Upload disabled; passport OCR uses URL input | Fix S3_ENDPOINT to use RAILWAY_PRIVATE_DOMAIN |
| **GHL workflow triggers** | UI-only, no API to trigger | Manual verification only | PERMANENT — GHL architecture limitation |
| **Alembic migrations** | No migration files created yet | Tables created via init_db() | Write first migration when schema changes |
| **Real E2E with live APIs** | Sandbox + costs block live testing | Full mock coverage (92.5%) | Production accounts + test budget |
| **Client portal** | Not built — not needed for pilot | RCICs use GHL directly | Post-pilot phase |
| **WhatsApp integration** | Not built | Not needed for pilot | Post-pilot |
| **Chrome extension store** | Not published | Extension works locally | Chrome Web Store submission |
| **Case email delivery** | Templates defined but not wired | case_emails.yaml ready, no send path | Wire email templates to GHL send_email |

---

## COVERAGE BY MODULE

```
92.54% OVERALL (693 tests)

100%  config.py, config_loader.py, db_models.py, analytics.py, briefings.py,
      demo.py, dependents.py, doc_extract.py, forms.py, trust.py,
      briefing_service.py

99%   scoring_service.py, ghl_client.py
98%   doc_ocr_service.py, analytics_service.py
97%   readiness.py, clients.py
95%   case_service.py
94%   webhooks.py, documents.py, document_service.py
93%   cases.py, scoring.py, trust_service.py, documenso_client.py
92%   sync_service.py, typebot.py, compliance_log.py
91%   signatures.py
90%   webhook_security.py
79%   ircc_form_service.py (PDF auto-fill)
72%   typebot_service.py (complex Typebot API)
64%   sync.py (needs real DB session)
38%   database.py (connection init — only runs in Railway)
```

---

## PERFORMANCE CHARACTERISTICS (k6 scripts ready)

| Scenario | Script | Thresholds |
|----------|--------|------------|
| API smoke | `tests/k6/smoke.js` | p95 < 500ms, <1% errors |
| Webhook burst (50 concurrent) | `tests/k6/webhook_burst.js` | p95 < 1000ms, <5% errors |
| Scoring throughput (100 VU) | `tests/k6/scoring_throughput.js` | p95 < 200ms, <1% errors |

---

## CI/CD STATUS

| Pipeline | Trigger | Status |
|----------|---------|--------|
| `ci-api.yml` | Push/PR to neuronx-api/** | READY (not yet pushed to GitHub) |
| `ci-web.yml` | Push/PR to neuronx-web/** | READY (not yet pushed to GitHub) |
| `nightly.yml` | Daily 6:17 AM UTC | READY (smoke + perf + weekly LLM eval) |

---

## SUMMARY COUNTS

| Metric | Count |
|--------|-------|
| Total tests | **693** |
| Tests passing | **693 (100%)** |
| Tests failing | **0** |
| Line coverage | **92.54%** |
| API endpoints tested | **55/57** (96%) |
| Database models tested | **9/9** (100%) |
| Config files tested | **7/7** (100%) |
| External integrations mocked | **5/5** (GHL, VAPI, Claude, Documenso, Typebot) |
| Contract fixtures | **6** JSON payload shapes |
| CI pipelines | **3** (api, web, nightly) |
| k6 perf scripts | **3** (smoke, burst, throughput) |
| Promptfoo eval cases | **4** (passport, IELTS x2, edge case) |
