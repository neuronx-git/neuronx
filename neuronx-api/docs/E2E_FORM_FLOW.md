# NeuronX Immigration Intake Form — E2E Flow

**Last Updated**: 2026-04-16  
**Status**: Production-ready (pending: production GHL account, RCIC license)

## Architecture Overview

```
Client receives unique link (via GHL workflow email)
  |
  v
www.neuronx.co/intake/vmc/onboarding?contact_id=abc123
  |
  v  [Vercel proxy → forwards params]
neuronx-api /form/vmc/onboarding?contact_id=abc123
  |
  v  [form.html JS forwards params to iframe]
Typebot Viewer: vmc-onboarding?contact_id=abc123
  |
  v  [isInputPrefillEnabled=true → auto-fills from URL params]
Client sees pre-filled form → fills remaining → uploads docs → submits
  |
  v  [Typebot webhook fires]
POST /typebot/webhook {contact_id, answers, resultId}
  |
  v  [96 field mapping → GHL custom fields]
GHL Contact updated → tag: nx:case:docs_pending → WF-CP-02 triggers
```

## URL Patterns

| URL | Purpose |
|-----|---------|
| `/form/vmc/onboarding` | Shared URL (no pre-fill, new contacts) |
| `/form/vmc/onboarding/{contact_id}` | Client-specific (server fetches GHL, pre-fills) |
| `/form/vmc/onboarding?contact_id=X&full_name=Y` | Query param pre-fill (used by GHL workflow) |
| `/intake/vmc/onboarding?contact_id=X` | Vercel proxy (www.neuronx.co) |

## Form Groups (16)

| # | Group | Blocks | Purpose |
|---|-------|--------|---------|
| 1 | Welcome | 4 | Greeting + Get Started |
| 2 | Program Selection | 2 | 8 program choices |
| 3 | Name | 6 | Passport upload + OCR + full name |
| 4 | Personal Info | 8 | Country, passport#, email, DOB, phone |
| 5-12 | Program Branches | 6-17 | Express Entry / Spousal / Work / Study / LMIA / PR / Citizenship / Visitor |
| 13 | Family | 4 | Spouse, dependents |
| 14 | Background | 5 | Criminal, refusal, deportation, medical, countries lived |
| 15 | Document Upload | 5 | Supporting docs + additional docs |
| 16 | Complete | 5 | Webhook + thank you |

## Questionnaire Coverage (24 common + program-specific)

| Program | Common | Specific | Total | Tier |
|---------|--------|----------|-------|------|
| Express Entry | 24 | 19 | 43 | P0 |
| Spousal Sponsorship | 24 | 15 | 39 | P0 |
| Work Permit | 24 | 13 | 37 | P0 |
| Study Permit | 24 | 12 | 36 | P1 |
| LMIA | 24 | 7 | 31 | P2 |
| PR Renewal | 24 | 5 | 29 | P2 |
| Citizenship | 24 | 7 | 31 | P2 |
| Visitor Visa | 24 | 12 | 36 | P2 |

## Common Questions (24)

**Personal Info (6)**: full_name, date_of_birth, country_of_citizenship, current_country, passport_number, passport_expiry  
**Contact (2)**: email, phone  
**Family (6)**: marital_status, has_spouse_on_application, spouse_full_name, spouse_date_of_birth, spouse_citizenship, has_dependents, num_dependents, dependent_names_dobs  
**Background (6)**: criminal_history, previous_refusal, previous_refusal_details, medical_conditions, deportation_history, countries_lived  
**Consent (2)**: consent_true_information, consent_representation

## Data Flow: GHL → Form → GHL

### Phase 1: Link Generation
```
GET /cases/onboarding-url/{contact_id}
  → Fetches GHL contact (name, email, phone, program_interest)
  → Returns URL with pre-fill params + contact_id
  → GHL workflow sends link to client
```

### Phase 2: Form Pre-fill
```
Client opens link → /form/vmc/onboarding?contact_id=X&full_name=Y
  → form.html JS: iframe.src = viewer_url + window.location.search
  → Typebot reads URL params → pre-fills matching variables
  → Client sees name, email, program already filled
```

### Phase 3: Form Submission
```
Typebot webhook → POST /typebot/webhook
  → Identifies contact by contact_id (or email/phone fallback)
  → Maps 96 Typebot answers → GHL custom fields
  → Adds tag: nx:case:docs_pending
  → Escalation: deportation/criminal → nx:escalation:rcic_review
  → Dedup: same resultId rejected on retry
```

### Phase 4: Multi-Session
```
Client reopens same link
  → /form/vmc/onboarding/{contact_id} re-fetches GHL data
  → Form pre-fills with LATEST data (GHL is source of truth)
  → No duplication — same contact_id, same record
  → rememberUser: Typebot also stores session in browser
```

## OCR Auto-Population

| Document | Method | Fields Extracted |
|----------|--------|-----------------|
| Passport | FastMRZ (free) → Ollama Cloud fallback | full_name, date_of_birth, passport_number, passport_expiry, nationality, sex |
| IELTS/CELPIP | Ollama Cloud (Gemini Flash) | listening, reading, writing, speaking, overall, test_date |
| ECA | Ollama Cloud | credential_level, canadian_equivalent, reference_number |
| Employment Letter | Ollama Cloud | employer_name, job_title, noc_code, start_date, salary |
| Marriage Certificate | Ollama Cloud | spouse names, marriage_date, jurisdiction |
| Bank Statement | Ollama Cloud | balance, currency, institution |
| Police Clearance | Ollama Cloud | applicant_name, country, result |

## IRCC Form Mappings (13 forms)

| Form | Programs | Fields |
|------|----------|--------|
| IMM 0008 | EE, SS, WP | 12 |
| IMM 5669 | EE, SS | 6 |
| IMM 5406 | EE, SS | 5 |
| IMM 5476 | EE, SS, WP | 3 |
| IMM 1344 | SS | 7 |
| IMM 5532 | SS | 5 |
| IMM 1295 | WP | 8 |
| IMM 5710 | WP | 6 |
| IMM 1294 | Study | 12 |
| IMM 5707 | Study, Visitor | 5 |
| IMM 5644 | PR Renewal | 8 |
| CIT 0002 | Citizenship | 10 |
| IMM 5257 | Visitor | 11 |

## Webhook Field Mapping (96 fields)

See `app/routers/typebot.py` lines 104-194 for the complete mapping.

## Typebot Configuration

| Setting | Value |
|---------|-------|
| isInputPrefillEnabled | true |
| isBrandingEnabled | false |
| rememberUser | enabled (session) |
| Webhook b_pp_ocr | /extract/from-url (passport OCR) |
| Webhook b_doc_ocr | /extract/from-url (doc OCR) |
| Webhook b_wh1 | /typebot/webhook (final submission) |

## Key Files

| File | Purpose |
|------|---------|
| `config/questionnaires.yaml` | All questions (24 common + program-specific) |
| `config/programs.yaml` | Document checklists, processing times |
| `config/ircc_field_mappings.yaml` | IRCC form field → questionnaire field mapping |
| `config/tenants.yaml` | Multi-tenant branding + form config |
| `app/routers/forms.py` | Form serving (shared + client-specific) |
| `app/routers/typebot.py` | Webhook handler (96 field mapping + escalation) |
| `app/routers/cases.py` | Onboarding URL generation + case management |
| `app/routers/doc_extract.py` | OCR extraction + GHL sync |
| `app/services/ghl_client.py` | GHL API + token auto-refresh |
| `app/services/doc_ocr_service.py` | FastMRZ + Ollama Cloud OCR |
| `templates/form.html` | Form HTML (iframe + param forwarding) |
| `tests/test_e2e_form_flow.py` | 41 E2E tests |

## Remaining for Pilot

1. **Production GHL account** ($297/mo) — email/SMS/phone workflows
2. **RCIC license number** — R000000 placeholder in ircc_field_mappings.yaml
3. **Typebot Builder sync** — update form blocks to match new questionnaire fields
