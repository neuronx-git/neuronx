# BOOTSTRAP PROMPT — NeuronX Production Readiness Sprint

**Copy-paste this entire file as your first message to the next Claude Code session.**

---

## WHO YOU ARE

You are the AI development lead for NeuronX — an immigration consulting SaaS. You have full execution authority. Your job is to take this product from "works in sandbox" to "investor-demo ready with production data."

## MANDATORY STARTUP

```bash
cat PROJECT_MEMORY.md
cat neuronx-api/docs/E2E_FORM_FLOW.md
cat docs/06_execution/AGENT_OPERATING_MODEL.md
```

Read the memory files:
```
memory/project_neuronx_state.md        # Current build state
memory/feedback_agent_working_model.md  # Agent rules
memory/feedback_form_architecture.md    # Form lessons learned
memory/feedback_railway_deploy.md       # Railway deploy pitfalls
memory/feedback_typebot_api.md          # Typebot API gotchas
memory/reference_credentials.md         # ALL credentials
```

## INFRASTRUCTURE MAP

### Railway Project: Neuronx
| Service | URL | Purpose |
|---------|-----|---------|
| neuronx (API) | neuronx-production-62f9.up.railway.app | FastAPI orchestration brain |
| PostgreSQL | postgres.railway.internal | Cases, activities, sync_log, dependents |
| Metabase | metabase-production-1846.up.railway.app | Analytics dashboard |

**Railway CLI**: `railway link --project Neuronx && railway service neuronx`
**Deploy**: `cd neuronx-api && railway up --detach` (NOT git push — auto-deploy unreliable)
**startCommand**: `uvicorn main:app --host 0.0.0.0 --port 8000` (NO shell expansion)
**GitHub**: neuronx-git/neuronx, main branch, root: /neuronx-api

### Railway Project: Typebot
| Service | URL | Purpose |
|---------|-----|---------|
| Builder | builder-production-6784.up.railway.app | Form design + API |
| Viewer | viewer-production-366c.up.railway.app | Form rendering (iframe) |
| PostgreSQL | postgres.railway.internal | Typebot data |
| MinIO | minio.railway.internal | File uploads |

**Typebot API token**: SuUW5WiLi1IAjuja4Mdtlu16
**Typebot workspace**: cmnrfqc6z000034qx46joy6hf
**Typebot form ID**: cmnrfu934000334qxnlmsvw2u (publicId: vmc-onboarding)
**CRITICAL**: Typebot version must be "6" (not "6.1"). Viewer __ENV.js is baked into Docker image.

### Vercel: Website
| URL | Root Dir |
|-----|----------|
| www.neuronx.co | neuronx-web |
| /intake/vmc/onboarding | public/intake.html (static, forwards params to Typebot iframe) |

### GHL (GoHighLevel) — Sandbox
| Item | Value |
|------|-------|
| Location ID | FlRL82M0D6nclmKT7eXH |
| Company ID | 1H22jRUQWbxzaCaacZjO |
| API Base | https://services.leadconnectorhq.com |
| Token | tools/ghl-lab/.tokens.json (auto-refreshes on 401) |
| Pipeline | Dtj9nQVd3QjL7bAb3Aiw (NeuronX — Immigration Intake) |
| Calendar | To1U2KbcvJ0EAX0RGKHS |
| **SANDBOX LIMITS**: Email/SMS/phone BLOCKED. Max 2 sub-accounts. |

### VAPI (Voice AI)
| Item | Value |
|------|-------|
| API Key | cb69d6fc-baf7-4881-8bff-20c7df251437 |
| Phone | +16479315181 |
| Assistant | Wired to Railway webhook |

## E2E DATA FLOW (How Everything Connects)

```
PHASE 1: LEAD → RETAINER
═══════════════════════════
Prospect submits GHL form / visits website
  → GHL creates contact + adds to pipeline stage 1
  → VAPI outbound call within 5 min (R1-R5 readiness assessment)
  → POST /webhooks/voice → scores lead → updates GHL tags
  → Consultation booked via GHL calendar
  → RCIC consultation → retainer signed
  → POST /cases/initiate → case ID generated (NX-YYYYMMDD-XXXXXXXX)
  → GET /cases/onboarding-url/{contact_id} → unique form link generated

PHASE 2: CASE PROCESSING (Onboarding Form)
═══════════════════════════════════════════
Client opens unique link: /form/vmc/onboarding/{contact_id}
  → Server fetches GHL contact data → pre-fills form
  → Typebot conversational form:
    Welcome → Passport Upload (OCR) → Personal Info → Program Selection
    → Program-specific questions (8 branches) → Family → Background
    → Consent → Document Upload → Completion
  → Typebot webhook → POST /typebot/webhook
    → 96 fields synced to GHL custom fields
    → Tag: nx:case:docs_pending (triggers WF-CP-02)
    → Escalation: deportation/criminal → nx:escalation:rcic_review
  → RCIC reviews docs → forms prepared → submitted to IRCC
  → Case stages: onboarding → doc_collection → form_prep → submitted → processing → decision
```

## WHAT'S DONE (Don't Redo)

- 735 unit/integration tests — ALL PASS
- 41 E2E form flow tests — ALL PASS
- 96 webhook field mappings (all 8 programs, zero-gap)
- 13 IRCC form mappings
- 7 OCR document types (FastMRZ passport + Ollama Cloud vision)
- GHL token auto-refresh on 401
- Client-specific form URLs with GHL data pre-fill
- Typebot webhooks wired (passport OCR, doc OCR, submission)
- rememberUser enabled for multi-session
- Lighthouse: Perf 87, A11y 95, BP 96, SEO 100

## YOUR MISSION — IN THIS ORDER

### Sprint 1: Functional Product Testing (E2E User Journey)
NOT unit testing. Test the PRODUCT like a real user would.

**Phase 1 Testing (Lead → Retainer)**:
1. Create a test contact in GHL via API
2. Simulate VAPI call completion (POST /webhooks/voice with R1-R5 data)
3. Verify scoring tags applied correctly in GHL
4. Generate consultation booking link
5. Simulate retainer signed → POST /cases/initiate
6. Verify case ID generated, GHL fields updated, tags added

**Phase 2 Testing (Form → GHL Sync)**:
1. Generate client-specific form link via GET /cases/onboarding-url/{contact_id}
2. Open the form in browser — verify pre-fill works
3. Walk through the form: select Express Entry, fill all fields
4. Upload a test passport → verify OCR extraction works
5. Submit the form → verify webhook fires
6. Check GHL contact — verify all 96 fields synced correctly
7. Check tags: nx:case:docs_pending applied
8. Reopen same link — verify data persists (multi-session)

**VAPI Testing**:
1. Test VAPI assistant config via API (GET /assistant/{id})
2. Verify structured data plan (R1-R5 extraction schema)
3. Simulate end-of-call-report webhook with transcript
4. Verify scoring + GHL tag update

### Sprint 2: Production-Like Data + Dashboards
1. **Seed demo data**: Create 20-30 realistic contacts across all 8 programs
   - Mix of stages: new lead, assessment complete, docs pending, submitted, approved, refused
   - Use POST /demo/seed or create via GHL API
2. **Metabase dashboards**: Connect to metabase-production-1846.up.railway.app
   - Pipeline conversion funnel
   - Program distribution
   - Average processing time by program
   - Stuck leads (>14 days in same stage)
   - RCIC workload distribution
3. **Analytics endpoints**: Verify GET /analytics/pipeline and GET /analytics/stuck return data

### Sprint 3: Email Templates
1. Choose open-source email template system (recommend: MJML or React Email)
2. Create templates for ALL case processing workflows:
   - WF-CP-01: Welcome + onboarding link (retainer signed)
   - WF-CP-02: Document collection reminder (7-day, 14-day)
   - WF-CP-03: Documents complete confirmation
   - WF-CP-05: IRCC submission confirmation
   - WF-CP-06: Monthly processing update
   - WF-CP-07: Additional information request (RFI)
   - WF-CP-08: Decision notification (approved/refused)
   - WF-CP-09: Case closed + satisfaction survey
3. Store templates in config/email_templates/ or integrate with GHL email builder
4. Wire templates to GHL workflows via API

### Sprint 4: Final Verification + Investor Demo Readiness
1. Re-run all tests (unit + E2E + production)
2. Re-run Lighthouse on all pages
3. Verify all dashboards populated with demo data
4. Take screenshots of: form flow, GHL pipeline, Metabase dashboards, VAPI call log
5. Create investor demo script with realistic data
6. Update all documentation

## RULES FOR THIS SESSION

1. **One step at a time** — complete Sprint 1 before starting Sprint 2
2. **Update PROJECT_MEMORY.md after every sprint** — this is how state is preserved
3. **Commit after every meaningful change** — don't batch 10 changes
4. **Test what you build** — run tests after every code change
5. **Don't break what works** — 735 tests must keep passing
6. **Use `railway up --detach`** to deploy (not git push — auto-deploy is unreliable)
7. **Typebot version must be "6"** — viewer rejects "6.1"
8. **GHL sandbox limits**: email/SMS/phone BLOCKED. Config work is safe.
9. **Ollama Cloud is sole OCR provider** — no Anthropic fallback
10. **GHL token auto-refreshes** — don't worry about expiry

## KEY FILES

| What | Where |
|------|-------|
| API entry point | neuronx-api/main.py |
| All questions | neuronx-api/config/questionnaires.yaml |
| Programs + docs | neuronx-api/config/programs.yaml |
| IRCC form mappings | neuronx-api/config/ircc_field_mappings.yaml |
| Tenant config | neuronx-api/config/tenants.yaml |
| Email templates | neuronx-api/config/case_emails.yaml |
| Form serving | neuronx-api/app/routers/forms.py |
| Webhook handler | neuronx-api/app/routers/typebot.py |
| Case management | neuronx-api/app/routers/cases.py |
| OCR extraction | neuronx-api/app/routers/doc_extract.py |
| GHL client | neuronx-api/app/services/ghl_client.py |
| OCR service | neuronx-api/app/services/doc_ocr_service.py |
| E2E tests | neuronx-api/tests/test_e2e_form_flow.py |
| E2E flow doc | neuronx-api/docs/E2E_FORM_FLOW.md |
| Form template | neuronx-api/templates/form.html |
| Vercel intake | neuronx-web/public/intake.html |

## CREDENTIALS QUICK REFERENCE

```bash
# GHL token (auto-refreshes)
cat tools/ghl-lab/.tokens.json | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'][:20]+'...')"

# Typebot API
curl -s -H "Authorization: Bearer SuUW5WiLi1IAjuja4Mdtlu16" \
  "https://builder-production-6784.up.railway.app/api/v1/typebots?workspaceId=cmnrfqc6z000034qx46joy6hf"

# VAPI
curl -s -H "Authorization: Bearer cb69d6fc-baf7-4881-8bff-20c7df251437" \
  "https://api.vapi.ai/assistant"

# Railway
railway whoami  # Should show Ranjan Singh
railway link --project Neuronx && railway service neuronx  # Link API service
railway link --project Typebot && railway service viewer     # Link Typebot viewer

# Production health
curl -s https://neuronx-production-62f9.up.railway.app/health/deep | python3 -m json.tool
```
