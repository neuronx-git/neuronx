# NeuronX — Platform Responsibility Matrix

**Date**: 2026-04-04
**Purpose**: Single source of truth for what lives where, who owns it, and how to change it.

---

## Platform Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  CUSTOMER FACING                         INTERNAL / BACK-OFFICE    │
│                                                                     │
│  GHL (White-Labeled)    NeuronX API      ERPNext        Metabase   │
│  "The CRM + Portal"    "The Brain"      "The Office"   "The Dash" │
│                                                                     │
│  Next.js + Vercel       VAPI             Documenso      Plausible  │
│  "The Website"         "The Voice"      "The Signer"   "The Stats"│
└─────────────────────────────────────────────────────────────────────┘
```

---

## MASTER MATRIX: What Lives Where

### 1. GHL (GoHighLevel) — White-Labeled CRM + Automation Engine

**Role**: System of record. All contacts, pipelines, workflows, forms, calendars, client portal.
**Cost**: $497/mo (Agency Pro with SaaS Mode + white-label)
**White-label**: Complete — client never sees "GoHighLevel"
**How to change**: GHL Admin UI (point-and-click)

| Capability | What GHL Does | Config Location | Status |
|-----------|---------------|-----------------|--------|
| **Contact Management** | Store all prospect + client records | GHL → Contacts | ✅ Live |
| **Intake Pipeline** (10 stages) | Track inquiry → retainer | GHL → Opportunities → Pipeline #1 | ✅ Live |
| **Case Processing Pipeline** (9 stages) | Track retainer → case closed | GHL → Opportunities → Pipeline #2 | ❌ UI needed |
| **Custom Fields** (140) | Store all structured data (R1-R5, IRCC, case) | GHL → Settings → Custom Fields | ✅ Live |
| **Tags** (103) | Trigger workflows, categorize contacts | GHL → Settings → Tags | ✅ Live |
| **Workflows** (15 intake) | Automated sequences: SMS, email, tasks, routing | GHL → Automation → Workflows | ✅ Live |
| **Workflows** (9 case processing) | Doc reminders, IRCC submission, decision routing | GHL → Automation → Workflows | ❌ UI needed |
| **Forms** (1 intake) | Lead capture: Immigration Inquiry V1 | GHL → Sites → Forms | ✅ Live |
| **Forms** (3 more needed) | Onboarding questionnaire, outcome, satisfaction | GHL → Sites → Forms | ❌ UI needed |
| **Calendars** (3) | Free assessment, paid consult, complex strategy | GHL → Calendars | ✅ Live |
| **Email Templates** (11) | Themed VMC emails for all touchpoints | GHL → Marketing → Emails | ✅ Live |
| **Client Portal** | Client sees case status, uploads docs, messages RCIC | GHL → Sites → Client Portal | ❌ Configure |
| **SMS/Email Sending** | Actual message delivery | GHL native (blocked in sandbox) | ❌ Production only |
| **Phone Numbers** | Inbound/outbound calling | GHL → Phone System | ❌ Production only |
| **Landing Pages** | Lead capture funnels | GHL → Sites → Funnels | ✅ Exists |
| **Reporting** (basic) | Pipeline overview, contact stats | GHL → Reporting | ✅ Native |
| **SaaS Mode** | Auto-provision client sub-accounts + billing | GHL → SaaS Configurator | ❌ Production only |
| **Snapshots** | Clone entire setup for new clients | GHL → Settings → Snapshots | ⚠️ Create before migrate |

**GHL Does NOT Do**:
- Scoring/intelligence (→ NeuronX API)
- Voice AI calls (→ VAPI)
- Deep analytics (→ Metabase)
- HR/Payroll (→ ERPNext)
- E-signatures (→ Documenso)
- IRCC form generation (→ Docxtemplater)
- Marketing website (→ Next.js)

---

### 2. NeuronX API (FastAPI on Railway) — Intelligence + Orchestration Layer

**Role**: The brain. Scoring, briefings, trust enforcement, case management, analytics, config.
**Cost**: $5-20/mo (Railway)
**White-label**: Your code — 100% owned
**How to change**: Edit YAML configs (no-code) or Python code (developer)

| Capability | What NeuronX API Does | Endpoint | Config File | Status |
|-----------|----------------------|----------|-------------|--------|
| **Lead Scoring (VAPI)** | Score R1-R5 from AI call data (0-100) | `POST /score/lead` | `config/scoring.yaml` | ✅ Live |
| **Lead Scoring (Form)** | Preliminary score from form only (R1-R3) | `POST /score/form` | `config/scoring.yaml` | ✅ Live |
| **VAPI Webhook Handler** | Process all VAPI events (calls, transcripts) | `POST /webhooks/voice` | Python code | ✅ Live |
| **GHL Webhook Handler** | Process GHL events (forms, appointments, tags) | `POST /webhooks/ghl` | Python code | ✅ Live |
| **Pre-Consult Briefing** | Generate HTML briefing from GHL contact data | `POST /briefing/generate` | Python code | ✅ Live |
| **Trust Enforcement** | Scan transcripts for compliance violations | `POST /trust/check` | `config/trust.yaml` | ✅ Live |
| **Document Checklist** | Program-specific IRCC doc requirements | `POST /documents/checklist` | `config/programs.yaml` | ✅ Live |
| **Assessment Report** | Structured report from GHL contact data | `POST /documents/assessment` | Python code | ✅ Live |
| **Case Initiation** | Start case after retainer (set fields, tags, deadlines) | `POST /cases/initiate` | `config/programs.yaml` | ✅ Live |
| **Case Stage Update** | Move case through processing stages | `POST /cases/stage` | Python code | ✅ Live |
| **IRCC Submission** | Record submission with receipt number | `POST /cases/submission` | Python code | ✅ Live |
| **IRCC Decision** | Record decision (approved/refused) | `POST /cases/decision` | Python code | ✅ Live |
| **IRCC Forms Lookup** | Get required forms for top 3 programs | `GET /cases/forms/{program}` | `config/programs.yaml` | ✅ Live |
| **Processing Timeline** | Estimated IRCC processing time | `GET /cases/timeline/{program}` | `config/programs.yaml` | ✅ Live |
| **Pipeline Analytics** | Funnel metrics from GHL data | `GET /analytics/pipeline` | Python code | ✅ Live |
| **Stuck Leads** | Detect contacts stuck in a stage | `GET /analytics/stuck` | Python code | ✅ Live |
| **Daily Dashboard** | Summary metrics for firm owner | `GET /analytics/dashboard` | Python code | ✅ Live |
| **Config Reload** | Hot-reload YAML configs without redeploy | `POST /admin/reload-config` | — | ✅ Live |

**NeuronX API Does NOT Do**:
- Store contacts (→ GHL)
- Send emails/SMS (→ GHL)
- Make phone calls (→ VAPI)
- Display dashboards (→ Metabase)
- Handle payroll (→ ERPNext)
- Sign documents (→ Documenso)

---

### 3. VAPI — Voice AI Layer

**Role**: Make and receive phone calls. Structured data extraction from conversations.
**Cost**: Usage-based (~$0.05-0.15/min)
**White-label**: Caller hears firm's brand, never "VAPI"
**How to change**: VAPI Dashboard → Assistants

| Capability | What VAPI Does | Config Location | Status |
|-----------|---------------|-----------------|--------|
| **Outbound AI Calls** | Call prospects within 5 min of inquiry | VAPI Dashboard → Assistants | ✅ Configured |
| **R1-R5 Assessment** | Collect readiness data during call | VAPI → analysisPlan | ✅ Configured |
| **Transcript + Summary** | Post-call analysis sent to NeuronX API | VAPI → serverUrl | ✅ Wired to Railway |
| **Function Calling** | collect_readiness_data, book_consultation, transfer_to_human | VAPI → Tools | ✅ Configured |
| **Compliance Guardrails** | System prompt prevents AI from assessing eligibility | VAPI → System Prompt | ✅ Configured |

**VAPI Does NOT Do**:
- Store data (→ sends to NeuronX API which writes to GHL)
- Score leads (→ NeuronX API)
- Send follow-up SMS/email (→ GHL workflows)

---

### 4. ERPNext (Frappe) — Back-Office Operations (Phase 2)

**Role**: HR, payroll, accounting, trust accounting for the immigration firm.
**Cost**: $25/mo (Frappe Cloud) — unlimited users
**White-label**: Yes (GPL + custom Frappe branding app)
**How to change**: ERPNext Admin UI

| Capability | What ERPNext Does | Module | Status |
|-----------|------------------|--------|--------|
| **Employee Records** | Onboarding, contracts, emergency contacts | HR | ❌ Phase 2 |
| **Attendance** | Clock in/out, biometric, mobile | HR → Attendance | ❌ Phase 2 |
| **Leave Management** | Request, approve, balance tracking | HR → Leave | ❌ Phase 2 |
| **Payroll** | Salary structures, payslips, tax calc | Payroll | ❌ Phase 2 |
| **Sales Commission** | Auto-calc from GHL retainer data → payslip | Payroll (variable) | ❌ Phase 2 |
| **Trust Accounting** | Segregated client funds (RCIC regulatory) | Accounting | ❌ Phase 2 |
| **Invoicing** | Auto-generate from retainer terms | Accounting | ❌ Phase 2 |
| **Expense Tracking** | Firm operating costs | Accounting | ❌ Phase 2 |
| **Performance Reviews** | Quarterly reviews tied to case metrics | HR → Appraisal | ❌ Phase 2 |

**ERPNext Does NOT Do**:
- CRM / pipeline (→ GHL)
- Client-facing communication (→ GHL)
- Voice calls (→ VAPI)
- Lead scoring (→ NeuronX API)

---

### 5. Metabase — Analytics Dashboards (Phase 1)

**Role**: Visual dashboards embedded in client portal. Deep analytics GHL can't do.
**Cost**: $10-15/mo (Railway Docker) — free OSS
**White-label**: Yes (embedded via JWT, shows your brand)
**How to change**: Metabase Admin → Questions/Dashboards

| Dashboard | What It Shows | Data Source | Status |
|-----------|--------------|-------------|--------|
| **Pipeline Funnel** | Conversion rates by stage | GHL → PostgreSQL | ❌ Week 3 |
| **Speed-to-Lead** | Avg time from inquiry to first contact | GHL → PostgreSQL | ❌ Week 3 |
| **Consultant Performance** | Bookings, show rate, conversion by RCIC | GHL → PostgreSQL | ❌ Week 3 |
| **Source Attribution** | Which lead sources convert best | GHL → PostgreSQL | ❌ Week 3 |
| **Commission Report** | Monthly commission by rep | GHL → PostgreSQL | ❌ Week 5 |
| **Case Processing** | Avg time per stage, bottlenecks | GHL → PostgreSQL | ❌ Phase 2 |

---

### 6. Next.js + Vercel — Website + Enhanced Client Portal (Phase 1)

**Role**: Marketing website (neuronx.co) + enhanced client portal beyond GHL's native portal.
**Cost**: $0-20/mo (Vercel free tier)
**White-label**: Your code — 100% owned
**How to change**: Code + push to GitHub

| Page | What It Does | Status |
|------|-------------|--------|
| `/` | Marketing homepage (features, pricing, testimonials) | ❌ Week 3 |
| `/demo` | Demo booking (embeds GHL calendar) | ❌ Week 3 |
| `/login` | Client portal login (magic link) | ❌ Week 4 |
| `/dashboard` | Client portal (Metabase embeds + case status) | ❌ Week 4 |
| `/documents` | Document upload/download + generated packets | ❌ Week 4 |
| `/blog` | SEO content (immigration updates) | ❌ Future |

---

### 7. Documenso — E-Signatures (Phase 2)

**Role**: Digital retainer signing. Replaces manual PDF signing.
**Cost**: $0 (self-hosted Railway Docker)
**White-label**: Yes (open source, fully brandable)

| Capability | What It Does | Status |
|-----------|-------------|--------|
| **Retainer Signing** | Client signs retainer digitally after consultation | ❌ Week 5 |
| **Webhook Callback** | Notify NeuronX API when signed → update GHL | ❌ Week 5 |
| **Audit Trail** | Legally compliant signing record | ❌ Week 5 |

---

### 8. Docxtemplater — Document Generation (In NeuronX API)

**Role**: Generate .docx files from templates with GHL contact data.
**Cost**: $0 (Python library: `docxtpl`)
**White-label**: N/A — generates files, not a UI

| Template | What It Generates | Status |
|----------|------------------|--------|
| **Retainer Agreement** | Fees, scope, terms from contact data | ❌ Week 2 |
| **Consultation Prep Packet** | Briefing + checklist for RCIC | ❌ Week 2 |
| **Assessment Report** | R1-R5 results + recommendation (JSON exists, .docx not) | ❌ Week 2 |
| **Engagement Letter** | Formal offer | ❌ Week 3 |

---

## CROSS-PLATFORM DATA FLOW

```
LEAD INQUIRY
  │
  ▼
GHL Form (captures name, program, location, timeline)
  │
  ├──► GHL WF-01 (instant ack SMS/email)
  ├──► NeuronX API /score/form (preliminary score)
  └──► GHL WF-02 → VAPI outbound call
                      │
                      ▼
              VAPI collects R1-R5
                      │
                      ▼
              NeuronX API /webhooks/voice
                      │
                      ├──► /trust/check (compliance scan)
                      ├──► /score/lead (full 0-100 score)
                      └──► GHL contact updated (fields + tags)
                              │
                              ▼
                      GHL WF-04B routes by score:
                        ≥70 → WF-04 → booking invite
                        40-69 → WF-12 → operator review
                        <40 → WF-11 → nurture
                              │
                              ▼
                      GHL Calendar → booking
                              │
                              ▼
              NeuronX API /briefing/generate
                      │
                      ▼
              RCIC conducts consultation (GHL WF-07 outcome capture)
                      │
                      ▼
              GHL WF-08 routes outcome:
                proceed → WF-09 → retainer follow-up
                follow-up → WF-10 → nurture
                declined → LOST
                              │
                              ▼
              Documenso signs retainer (Phase 2)
                      │
                      ▼
              NeuronX API /cases/initiate
                      │
                      ├──► GHL Pipeline #2 (case processing)
                      ├──► /documents/checklist (program-specific)
                      └──► /cases/forms/{program} (IRCC forms)
                              │
                              ▼
              Case processing through Pipeline #2 stages
              (RCIC manually preps + submits to IRCC)
                              │
                              ▼
              NeuronX API /cases/submission (receipt number)
                              │
                              ▼
              NeuronX API /cases/decision (approved/refused)
                              │
                              ▼
              GHL WF-CP-09 → close case → survey → referral ask

ANALYTICS (runs across all stages):
  GHL data → PostgreSQL (nightly sync) → Metabase dashboards
  Embedded in Next.js client portal

HR/OPERATIONS (Phase 2):
  ERPNext ← commission data from NeuronX API
  ERPNext → payslips, attendance, accounting
```

---

## CONFIGURATION GUIDE: Where to Change What

| I want to change... | Go to... | Type |
|---------------------|----------|------|
| Scoring thresholds (70/40) | `config/scoring.yaml` → `thresholds` | YAML edit → push |
| Add a complexity keyword | `config/scoring.yaml` → `complexity_keywords` | YAML edit → push |
| Change scoring points per dimension | `config/scoring.yaml` → `dimension_base_points` | YAML edit → push |
| Add an IRCC form to a program | `config/programs.yaml` → `ircc_forms` | YAML edit → push |
| Add a document to a checklist | `config/programs.yaml` → `required_documents` | YAML edit → push |
| Change processing time estimate | `config/programs.yaml` → `processing_months` | YAML edit → push |
| Add a new immigration program | `config/programs.yaml` → add new program block | YAML edit → push |
| Add an escalation trigger | `config/trust.yaml` → `escalation_triggers` | YAML edit → push |
| Change a workflow | GHL → Automation → Workflows → select → edit | GHL UI |
| Change an email template | GHL → Marketing → Emails → select → edit | GHL UI |
| Change calendar availability | GHL → Calendars → select → edit hours | GHL UI |
| Change pipeline stages | GHL → Opportunities → Pipeline → edit | GHL UI |
| Add a custom field | GHL → Settings → Custom Fields → Add | GHL UI |
| Change VAPI voice/prompts | VAPI Dashboard → Assistants → edit | VAPI UI |
| Change website content | `neuronx-website/` code → push to GitHub | Vercel auto-deploy |
| Change analytics dashboards | Metabase Admin → edit question/dashboard | Metabase UI |

---

## COST SUMMARY

| Platform | What | Monthly | Annual |
|----------|------|---------|--------|
| GHL Agency Pro | CRM + White-label + SaaS Mode | $497 | $5,964 |
| Railway (FastAPI) | API hosting | $10 | $120 |
| Railway (PostgreSQL) | Database | Included | — |
| Railway (Metabase) | Analytics | $15 | $180 |
| Vercel (Next.js) | Website + portal | $0 | $0 |
| VAPI | Voice AI | ~$50 usage | ~$600 |
| Frappe Cloud (ERPNext) | HR/Payroll/Accounting | $25 | $300 |
| Railway (Documenso) | E-signatures | $0 | $0 |
| **TOTAL** | | **~$597/mo** | **~$7,164/yr** |

**Revenue needed to break even**: 1 client at $599/mo Professional tier.
**At 10 clients**: $5,990 revenue vs $597 cost = **90% gross margin**.
