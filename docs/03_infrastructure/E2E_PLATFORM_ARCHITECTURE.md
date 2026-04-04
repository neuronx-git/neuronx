# NeuronX — E2E White-Label Platform Architecture

**Date**: 2026-04-01
**Status**: CANONICAL — Replaces OPEN_SOURCE_STACK.md as strategic vision doc
**Principle**: If NeuronX can't white-label it, NeuronX doesn't use it.

---

## The Vision

NeuronX is the **complete operating system** for immigration consulting firms.
Not just intake. Not just CRM. Everything from first inquiry to case resolution,
plus the firm's own HR, payroll, accounting, and team productivity.

**One login. One brand. One bill. Full white-label.**

---

## Architecture: Three Pillars (All White-Labelable)

```
┌──────────────────────────────────────────────────────────────────┐
│                    PILLAR 1: GHL (White-Labeled)                  │
│              "NeuronX CRM" — Client-Facing Platform               │
│                                                                    │
│  Intake Pipeline ──► Case Processing Pipeline ──► Nurture         │
│  Forms · Calendar · Client Portal · Workflows · Custom Objects    │
│  Email · SMS · Voice (VAPI) · Documents · Analytics               │
│                                                                    │
│  White-label: ✅ Complete (Agency Pro $497/mo)                     │
│  Client sees: "NeuronX" or firm's brand. Never "GoHighLevel".     │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                    PILLAR 2: ERPNext (White-Labeled)              │
│              "NeuronX Operations" — Back-Office Platform          │
│                                                                    │
│  HR · Payroll · Attendance · Leave · Accounting · Invoicing       │
│  Trust Accounting · Employee Lifecycle · Performance Reviews      │
│  Expense Tracking · Commission Calculation · Tax Compliance       │
│                                                                    │
│  White-label: ✅ (GPL, custom Frappe apps for branding)           │
│  Deploy: Frappe Cloud ($25/mo) or Railway Docker                  │
│  Pricing: NOT per-user — unlimited users at same cost             │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                  PILLAR 3: NeuronX Custom Layer                   │
│           FastAPI + Next.js + Metabase + Documenso                │
│                                                                    │
│  FastAPI: Scoring · Briefings · Trust · Analytics · Sync          │
│  Next.js: Marketing site · Unified portal · Sales scripts         │
│  Metabase: Embedded dashboards (pipeline, productivity, commn)    │
│  Documenso: E-signatures (retainers, engagement letters)          │
│  Docxtemplater: IRCC form generation + consultation packets       │
│                                                                    │
│  White-label: ✅ (all open source, self-hosted)                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Customer Lifecycle (E2E)

### Phase 1: INQUIRY → RETAINER (GHL + NeuronX API + VAPI)
```
Website form → AI call (5 min) → Score R1-R5 → Book consult → Briefing → Consultation → Retainer signed
```
**Status**: BUILT ✅ (15 workflows, scoring, briefings, templates)

### Phase 2: CASE PROCESSING (GHL — Second Pipeline)
```
Retainer signed → Doc collection → Form prep → IRCC submission → Status tracking → Decision → Case closed
```

**New GHL Pipeline: "Case Processing"**

| Stage | What Happens | Automation |
|-------|-------------|------------|
| DOC COLLECTION | Client uploads docs via portal | WF: checklist email + deadline reminders |
| FORM PREPARATION | RCIC reviews + preps IRCC forms | WF: task created for assigned RCIC |
| UNDER REVIEW | Internal QC before submission | WF: notify senior RCIC for review |
| SUBMITTED TO IRCC | Application filed | WF: log submission date, set follow-up |
| PROCESSING | Waiting for IRCC decision | WF: monthly status check reminders |
| ADDITIONAL INFO | IRCC requests more docs | WF: urgent alert + client notification |
| DECISION RECEIVED | Approval/refusal | WF: notify RCIC + client |
| CASE CLOSED | Final docs delivered | WF: satisfaction survey + review request |

**Custom fields for case tracking**:
- `ircc_receipt_number` — IRCC application number
- `ircc_submission_date` — when submitted
- `ircc_program_type` — Express Entry, Spousal, etc.
- `case_assigned_rcic` — assigned consultant
- `case_deadline_date` — next milestone date
- `case_status_notes` — latest status update
- `docs_outstanding` — pending document list

**GHL Custom Objects** (advanced): Treat each case as its own record with lifecycle, separate from the contact. One client can have multiple active cases (spousal + work permit).

### Phase 3: CLIENT PORTAL (GHL White-Label + Next.js Enhancement)

GHL client portal shows:
- Case status (which stage, what's next)
- Document upload area
- Appointment history
- Messages with RCIC
- Invoice status

Next.js portal adds:
- Metabase analytics dashboards (conversion rates, pipeline health)
- Document generation (download prep packets)
- IRCC form status tracker
- Multi-case view for clients with parallel applications

### Phase 4: FIRM OPERATIONS (ERPNext White-Labeled)

**Module**: HR & Employee Lifecycle
- Employee records (onboarding, contracts, emergency contacts)
- Attendance tracking (clock in/out, biometric integration)
- Leave management (request, approve, balance tracking)
- Performance reviews (quarterly, tied to case metrics)

**Module**: Payroll & Compensation
- Salary structures (base + commission + bonuses)
- Automated payslip generation (monthly)
- Tax calculations (Canadian CRA compliance)
- Commission calculation:
  ```
  Retainer signed (from GHL pipeline) → FastAPI syncs deal data to ERPNext
  Commission rules:
    Tier 1 ($0-5K retainer): 10%
    Tier 2 ($5K-15K): 12%
    Tier 3 ($15K+): 15%
    Speed bonus: +2% if closed within 7 days
  ERPNext auto-calculates → adds to payslip as variable component
  ```

**Module**: Accounting & Finance
- Trust account management (regulatory requirement for RCICs)
- Client invoicing (auto-generated from retainer terms)
- Expense tracking (firm operating costs)
- GST/HST calculations (Canadian tax)
- Financial reporting (P&L, balance sheet, cash flow)

**Module**: Work Assignment & Productivity
- Task management (synced from GHL workflows)
- Case-to-consultant assignment (skill-based routing)
- Workload dashboard (cases per RCIC, hours logged)
- Productivity metrics (cases closed, avg time to resolution)

---

## Sales Enablement (Baked Into Platform)

### What's Already Built
| Asset | Location | Status |
|-------|----------|--------|
| VAPI AI call scripts (R1-R5 assessment) | VAPI assistant config | ✅ Built |
| 11 email templates (inquiry→retainer) | `templates/themed/` | ✅ Built |
| 8 nurture emails (program-specific) | `templates/nurture/` | ✅ Built |
| 6 NX-WF sales workflows (selling NeuronX) | `templates/nx-sales/` | ✅ Drafted |
| Pre-consultation briefing (HTML) | FastAPI `/briefing/generate` | ✅ Built |
| Trust boundary rules (what AI can/can't say) | `trust_boundaries.md` | ✅ Built |

### What Needs Building (Sales Script System)

**Deliver via GHL + Next.js portal** (not a separate tool):

| Script Type | Delivery | Priority |
|-------------|----------|----------|
| **Inbound call script** (receptionist) | GHL custom page (staff-only) | P1 |
| **AI call script** (VAPI prompts) | VAPI assistant config | ✅ Done |
| **Follow-up call script** (human rep) | GHL custom page | P1 |
| **Consultation script** (RCIC guide) | Pre-consultation briefing | ✅ Done |
| **Retainer closing script** | GHL custom page | P1 |
| **Objection handling guide** | GHL custom page or Next.js | P1 |
| **No-show recovery script** | Email/SMS templates | ✅ Done |
| **Referral ask script** | GHL custom page | P2 |

**How it works in GHL**:
- Create "Sales Playbook" as a GHL Custom Menu page (staff portal)
- Scripts are organized by pipeline stage
- When rep opens a contact, they see the relevant script for that stage
- Scripts include: opening, discovery questions, value props, objection responses, close

---

## Complete E2E Feature Map

### For the Immigration Firm (Client of NeuronX)

| Need | Tool | White-Label? | Status |
|------|------|-------------|--------|
| Lead capture (forms, landing pages) | GHL | ✅ Yes | Built |
| AI calling (5-min response) | VAPI + GHL | ✅ Yes | Built |
| Lead scoring (R1-R5) | NeuronX API | ✅ Yes | Built |
| Consultation booking | GHL Calendar | ✅ Yes | Built |
| Pre-consult briefings | NeuronX API | ✅ Yes | Built |
| Email/SMS workflows (15 WFs) | GHL Workflows | ✅ Yes | Built |
| Nurture campaigns (8 programs) | GHL + Templates | ✅ Yes | Content ready |
| Case processing pipeline | GHL (Pipeline #2) | ✅ Yes | **Build next** |
| Document collection portal | GHL Client Portal | ✅ Yes | **Build next** |
| IRCC form generation | Docxtemplater | ✅ Yes | Week 2 |
| E-signatures (retainers) | Documenso | ✅ Yes | Week 5 |
| Pipeline analytics | Metabase (embedded) | ✅ Yes | Week 3 |
| Client status portal | Next.js + GHL | ✅ Yes | Week 4 |
| HR / Employee records | ERPNext | ✅ Yes | Phase 2 |
| Attendance tracking | ERPNext | ✅ Yes | Phase 2 |
| Payroll + commission | ERPNext | ✅ Yes | Phase 2 |
| Trust accounting | ERPNext | ✅ Yes | Phase 2 |
| Invoicing | ERPNext | ✅ Yes | Phase 2 |
| Sales scripts | GHL custom pages | ✅ Yes | P1 |
| Work assignment | GHL tasks + ERPNext | ✅ Yes | Week 3 |
| Productivity dashboards | Metabase | ✅ Yes | Week 3 |

### For NeuronX (The Company)

| Need | Tool | Status |
|------|------|--------|
| Selling NeuronX to firms | GHL (NX-WF-01→06) | Drafted |
| Demo booking | GHL Calendar | Ready |
| Trial management | GHL Pipeline | Build in production |
| Client onboarding | GHL Snapshot + Workflows | Ready |
| NeuronX team HR | ERPNext | Phase 2 |
| Revenue tracking | ERPNext + Metabase | Phase 2 |

---

## Deployment Map

| Service | Platform | Cost/mo | White-Label |
|---------|----------|---------|-------------|
| GHL (Agency Pro) | GHL Cloud | $497 | ✅ Complete |
| NeuronX API (FastAPI) | Railway | $5-20 | ✅ Your code |
| PostgreSQL | Railway add-on | Included | ✅ |
| ERPNext | Frappe Cloud | $25 | ✅ GPL + branding app |
| Metabase | Railway | $10-15 | ✅ Open source |
| Next.js (neuronx.co) | Vercel | $0-20 | ✅ Your code |
| Documenso (e-sign) | Railway | $0 | ✅ Open source |
| VAPI (voice AI) | VAPI Cloud | Usage-based | ✅ (behind NeuronX) |
| **Total** | | **~$550-580/mo** | **100% white-label** |

---

## IRCC Case Management (No Docketwise Needed)

Instead of paying for Docketwise ($200+/mo per firm), build case management directly in GHL:

**GHL Pipeline #2: Case Processing** (stages defined above)
**GHL Custom Fields**: IRCC receipt, program type, deadlines, assigned RCIC
**GHL Custom Objects**: Each case = independent record (multi-case per client)
**GHL Workflows**: Deadline reminders, status change notifications, escalations
**GHL Client Portal**: Client sees case status, uploads docs, messages RCIC
**Docxtemplater**: Generate IRCC form packages from templates (IMM 0008, checklists)

**What we can't do (and shouldn't try)**:
- Auto-fill IRCC web forms (this is what Docketwise/CaseEasy do)
- Direct e-filing to IRCC portal (requires IRCC API access, which doesn't exist publicly)

**What RCICs do manually** (will always be manual):
- Log into IRCC portal
- Copy data from NeuronX prep packet into IRCC forms
- Submit application
- Update NeuronX with receipt number

**Our job**: Give the RCIC everything they need in one place so submission takes 15 minutes, not 2 hours.

---

## Build Sequence

### Now (This Week)
- [x] FastAPI thin brain (27 tests)
- [x] 11 email templates
- [x] 8 nurture templates
- [x] 6 NX-WF sales drafts
- [ ] Deploy FastAPI to Railway
- [ ] Commit + push code to GitHub

### Week 2
- [ ] GHL Pipeline #2: Case Processing (stages + fields + workflows)
- [ ] Docxtemplater: retainer agreement + assessment report templates
- [ ] GHL → PostgreSQL data sync
- [ ] Sales scripts: inbound call + follow-up + retainer close + objections

### Week 3
- [ ] Metabase on Railway (pipeline + productivity dashboards)
- [ ] Next.js scaffold (marketing + portal)
- [ ] Work assignment logic (GHL round-robin + tasks)

### Week 4
- [ ] Client portal (Next.js + Metabase embeds)
- [ ] Full UAT: form → call → score → book → brief → retainer → case processing

### Week 5 (Production)
- [ ] Migrate to paid GHL account
- [ ] Documenso (e-signatures)
- [ ] Commission calculation in FastAPI
- [ ] Pilot customer onboarded

### Phase 2 (Month 2-3)
- [ ] ERPNext deployment (HR + Payroll + Accounting)
- [ ] ERPNext ↔ FastAPI sync (commission → payslip)
- [ ] Trust accounting setup
- [ ] Employee self-service portal
