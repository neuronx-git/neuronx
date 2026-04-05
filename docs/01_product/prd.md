# NeuronX Product Requirements Document

Version: 3.1
Status: CANONICAL
Last Updated: 2026-03-21
Authority: Founder
Companion: vision.md v3.0
Implementation Blueprint: /docs/02_operating_system/operating_spec.md
Changes v3.1: Added Section 12 (API Contract), Section 13 (Onboarding Process), Section 14 (Build Sequence). Updated Document Authority table.

---

## 1. Product Goals

G1: Enable immigration consulting firms to make AI-assisted first contact
    with every inquiry within 5 minutes.

G2: Provide structured, immigration-relevant readiness assessment that is
    consistent across all operators and AI interactions.

G3: Automate consultation booking, reminders, and no-show recovery so that
    assessed leads reliably reach a consultant.

G4: Deliver AI-assembled consultation preparation briefings so that
    consultants enter every meeting with full prospect context.

G5: Ensure persistent follow-up across the full pipeline so that no lead
    is lost to inaction.

G6: Give firm owners real-time visibility into pipeline health, conversion
    rates, and operator performance.

G7: Enforce trust boundaries so that AI never provides immigration advice,
    assesses legal eligibility, or makes promises about outcomes.

---

## 2. Users

### 2.1 Firm Owner / Principal Consultant

- **Responsibilities**: Business strategy, high-value consultations, marketing
  decisions, team management
- **Uses NeuronX for**: Pipeline dashboards, conversion analytics, lead source
  ROI, operator performance, daily briefings
- **Success looks like**: "I open one dashboard and know exactly how my firm
  is performing, without asking anyone."

### 2.2 Intake Coordinator

- **Responsibilities**: Responding to inquiries, assessing leads, booking
  consultations, managing follow-up
- **Uses NeuronX for**: Work queue, lead context cards, readiness assessment
  workflows, booking tools, follow-up task management
- **Success looks like**: "I know exactly who to call next, what to say, and
  how to book them -- without hunting through spreadsheets."

### 2.3 Consultant / RCIC / Immigration Lawyer

- **Responsibilities**: Delivering consultations, converting to retainer,
  case assessment
- **Uses NeuronX for**: Pre-consultation briefings, outcome recording,
  calendar overview
- **Success looks like**: "I walk into every consultation already knowing the
  prospect's situation, questions, and urgency."

### 2.4 Prospective Client (End User)

- **Responsibilities**: Seeking immigration services
- **Interacts with**: Intake forms, AI calls, SMS/email communications,
  booking pages, consultation experience
- **Success looks like**: "They called me back within minutes, asked the right
  questions, and booked me with the right consultant. I didn't have to repeat
  myself."

---

## 3. Ideal Customer Profile (ICP)

| Dimension | Specification |
|---|---|
| Industry | Immigration consulting |
| Geography | Canada (v1) |
| Firm type | RCIC firms, immigration law firms, boutique consultancies |
| Firm size | 2-15 staff |
| Monthly inquiries | 50-500 |
| Annual revenue | $300K-$5M CAD |
| Current tech | Spreadsheets, WhatsApp, Calendly, sometimes GHL or basic CRM |
| Key pain | Slow response, missed follow-ups, unprepared consultations, no pipeline visibility |
| Willingness to pay | $500-$1,500/month for a system that demonstrably increases retained clients |

### Exclusions (v1)
- Solo practitioners handling < 20 inquiries/month (insufficient volume for ROI)
- Large enterprise firms with 50+ staff (require custom solutions)
- Firms outside Canada (regulatory context differs)
- Non-immigration consulting firms

---

## 4. Core Workflows (Summary)

Detailed workflow specifications, state machine, data model, rules engine,
and failure modes are defined in the operating specification:
`/docs/02_operating_system/operating_spec.md`

The following workflows are implemented in v1:

| ID | Workflow | Purpose |
|---|---|---|
| WF-01 | Inquiry Intake | Capture inquiry, create lead, tag source |
| WF-02 | First Response | Instant acknowledgment, initiate contact |
| WF-03 | Contact Attempts | 7-step multi-channel contact sequence |
| WF-04 | Readiness Assessment | Structured assessment with 6 dimensions |
| WF-05 | Booking | Calendar booking with follow-up |
| WF-06 | Reminders | 4-touch reminder sequence before consultation |
| WF-07 | No-Show Recovery | 6-step recovery sequence |
| WF-08 | Consultation Prep | AI-assembled briefing delivered to consultant |
| WF-09 | Outcome Capture | Post-consultation outcome recording and routing |
| WF-10 | Follow-Up to Retainer | Retainer delivery and conversion follow-up |

---

## 5. Functional Capabilities

### 5.1 Handled Natively by GoHighLevel (Configure, Don't Build)

- FC-GHL-01: Contact record management (CRUD, custom fields, tags)
- FC-GHL-02: Pipeline and opportunity tracking (stages, movements)
- FC-GHL-03: Workflow automation (triggers, conditions, actions, waits)
- FC-GHL-04: Calendar booking (availability, widget, reminders)
- FC-GHL-05: SMS and email messaging (sending, sequences, templates)
- FC-GHL-06: Forms and surveys (intake forms)
- FC-GHL-07: Webhook integration (inbound and outbound)
- FC-GHL-08: Lead assignment (round-robin or manual)
- FC-GHL-09: Sub-account provisioning (SaaS Mode)
- FC-GHL-10: Billing (Stripe via SaaS Mode)
- FC-GHL-11: White-labeling (Agency Pro)
- FC-GHL-12: Basic reporting (native GHL dashboards)

### 5.2 Handled by NeuronX Orchestration Layer

- FC-NX-01: AI outbound calling orchestration
- FC-NX-02: Call outcome processing and CRM update
- FC-NX-03: Readiness scoring engine
- FC-NX-04: Consultation preparation assembly
- FC-NX-05: AI context memory
- FC-NX-06: Operator work queue prioritization
- FC-NX-07: Pipeline analytics engine
- FC-NX-08: Daily briefing generation
- FC-NX-09: Stuck-lead detection and alerting
- FC-NX-10: Regulatory guardrail enforcement

### 5.3 Handled by Domain-Specific Logic

- FC-DS-01: Immigration-specific readiness dimensions
- FC-DS-02: Immigration consultation prep templates
- FC-DS-03: Immigration-appropriate AI call scripts
- FC-DS-04: Immigration-specific pipeline stage definitions
- FC-DS-05: Immigration-specific metric definitions

Full capability classification: `/docs/03_infrastructure/ghl_capability_map.md`

---

## 6. Non-Goals (v1)

| Non-Goal | Rationale |
|---|---|
| Case management (post-retention) | Served by Docketwise, INSZoom, Cerenade, etc. |
| Document collection and management | Post-retention scope |
| Government application preparation | Regulated activity, out of scope |
| Immigration eligibility assessment | Regulated, AI must not perform |
| Multi-language support | v2 consideration |
| Multi-CRM support | GoHighLevel only in v1 |
| Marketplace or template store | Premature |
| Self-serve zero-touch onboarding | Premium product requires guided setup |
| Mobile native app | Web-first; mobile-responsive is sufficient |
| Integration with case management software | v2 consideration |

---

## 7. Trust Boundaries (Summary)

Full trust boundary specification: `/docs/04_compliance/trust_boundaries.md`

**AI May**: Greet, ask factual questions, gather information, schedule
consultations, send reminders, prepare briefings, escalate to humans.

**AI Must NOT**: Assess eligibility, recommend pathways, interpret law,
promise outcomes, impersonate licensed professionals, handle payment.

**Mandatory Escalation**: Eligibility questions, deportation/removal mentions,
emotional distress, minor involved, explicit human request, low AI confidence.

---

## 8. Success Metrics

### Primary Metric
**Consultation-to-Retained Conversion Rate**

### Pipeline Metrics

| Metric | v1 Target |
|---|---|
| Speed-to-first-contact | < 5 min (AI-handled) |
| Contact rate | > 75% |
| Readiness assessment rate | > 90% of contacted leads |
| Booking rate | > 55% of assessed leads |
| Show rate | > 80% |
| Consult-to-retained rate | Baseline, then improve |

### Operational Metrics

| Metric | Purpose |
|---|---|
| Operator contacts per day | Workload and productivity |
| Pipeline stage velocity | Bottleneck identification |
| Stuck leads count | Neglect detection |
| No-show rate and recovery rate | Reminder effectiveness |

### Business Metrics

| Metric | Purpose |
|---|---|
| Revenue per lead | Pipeline efficiency |
| Lead source ROI | Marketing spend optimization |
| Time to retained | Sales cycle efficiency |

**Assumption**: v1 establishes measurement capability. Targets beyond
speed-to-contact are set after 90 days of live data.

---

## 9. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| AI call quality insufficient for trust-sensitive immigration context | High | Rigorous prompt engineering, mandatory human escalation, pilot testing |
| GoHighLevel API limitations discovered during integration | High | GHL Capability Map requires live verification; fallback plans per feature |
| Regulatory objection from CICC regarding AI in immigration intake | Medium | Trust boundaries exceed regulatory requirements; AI gathers info only |
| Low adoption due to firm tech aversion | Medium | Premium onboarding, guided setup, not self-serve |
| Voice provider pricing or reliability issues | Medium | Provider choice open; architecture supports swap |
| Prospect negative reaction to AI calling | Medium | AI identifies as AI-assisted; immediate human handoff on request |
| Snapshot deployment requires manual setup (no API) | Medium | Manual setup per firm in v1 |
| Existing codebase technical debt | Medium | Codebase is reference only; disposition is open decision |

---

## 10. Launch Scope (v1)

| ID | Capability | Category |
|---|---|---|
| V1-01 | GHL sub-account with immigration pipeline, forms, calendars, workflows | GHL Config |
| V1-02 | Intake form with immigration-relevant fields | GHL Config |
| V1-03 | Speed-to-lead AI calling | NeuronX Orchestration |
| V1-04 | Readiness scoring (program, urgency, location, budget, history) | NeuronX Logic |
| V1-05 | Automated booking with reminders and no-show recovery | GHL + NeuronX |
| V1-06 | Consultation preparation briefing | NeuronX Logic |
| V1-07 | Post-consultation outcome capture and follow-up | GHL + NeuronX |
| V1-08 | Pipeline dashboard with conversion funnel | NeuronX Analytics |
| V1-09 | Daily briefing for firm owner | NeuronX Logic |
| V1-10 | Trust boundary enforcement | NeuronX Logic |
| V1-11 | Repeatable onboarding process | Operations |

---

## 11. Deferred Scope

| ID | Capability | Deferred To | Rationale |
|---|---|---|---|
| D-01 | Operator scorecards | v1.5 | Requires 30+ days of data |
| D-02 | Lead source attribution (automated) | v1.5 | Requires marketing cost integration |
| D-03 | AI context memory across interactions | v1.5 | Not launch-critical |
| D-04 | Multi-language support | v2 | English-first |
| D-05 | Case management integration | v2 | Post-retention scope |
| D-06 | Self-serve onboarding | v2+ | Premium model in v1 |
| D-07 | WhatsApp automation | v1.5 | GHL WhatsApp reliability unverified |
| D-08 | Adjacent vertical expansion | v2+ | Immigration-first |
| D-09 | Mobile native app | v2+ | Web-responsive sufficient |
| D-10 | Consultant performance comparison | v1.5 | Politically sensitive |

---

## 12. NeuronX API Contract (v1)

The following API endpoints are required for v1 launch. Implementation: `neuronx-api/`.

| Endpoint | Method | Purpose | Week |
|----------|--------|---------|------|
| `/health` | GET | Service health check | Week 4 |
| `/webhooks/ghl` | POST | GHL form + appointment events | Week 4 |
| `/webhooks/voice` | POST | VAPI end-of-call transcript + results | Week 4 |
| `/score/lead` | POST | R1-R5 readiness scoring → outcome + GHL fields | Week 4 |
| `/briefing/generate` | POST | Pre-consultation briefing → email + GHL note | Week 4 |
| `/trust/check` | POST | Trust boundary audit of AI transcript | Week 4 |
| `/analytics/pipeline` | GET | Conversion funnel metrics (N-day window) | Week 4 |
| `/analytics/stuck` | GET | Leads stuck in stage > threshold days | Week 4 |
| `/analytics/dashboard` | GET | Daily summary for firm owner | Week 4 |

**Webhook Security**: GHL webhooks use Ed25519 signatures. Validate `X-GHL-Signature` header.
**Deployment**: Railway or Render (free/starter tier, <$50/month).

---

## 13. Onboarding Process (v1)

Per-firm onboarding is founder-led and white-glove for v1. Estimated time: 2-4 hours per firm.

### Step 1: Sub-Account Provisioning
- Create GHL sub-account in Agency view
- Install NeuronX snapshot ("NeuronX Immigration Intake v1.0")
- Verify all 11 workflows, pipeline, form, calendar imported correctly

### Step 2: Firm Branding
- Update landing page with firm name, logo, colors, team photos
- Update RCIC number and credentials
- Customize message template signatures with firm contact info
- List programs offered (Express Entry, Spousal, etc.)

### Step 3: Voice AI Configuration
- GHL Voice AI: Configure in sub-account settings
- VAPI: Create sub-account, link firm's phone number, set consultant email for call notifications
- Test call: Submit form → verify AI calls within 5 minutes

### Step 4: NeuronX API Configuration
- Set `GHL_LOCATION_ID` for firm's sub-account
- Set `consultant_email` for briefing delivery
- Deploy/configure webhook endpoints
- Test end-to-end: form → voice call → readiness scored → briefing delivered

### Step 5: Team Training
- Intake coordinator: Work queue, lead management, manual tagging
- Consultants: Briefing delivery, outcome recording, retainer sending
- Firm owner: Pipeline dashboard, stuck lead review

### Step 6: Go-Live Checklist
- [ ] Landing page accessible and form submitting
- [ ] AI call triggers within 5 minutes of form submission
- [ ] Readiness data captured in GHL custom fields
- [ ] Consultation booking flow tested
- [ ] Pre-consultation briefing delivered to consultant
- [ ] Retainer follow-up sequence active
- [ ] Trust boundary enforcer active (compliance log writing)
- [ ] Firm team trained and confident

---

## 14. Build Sequence (6-Week Implementation Plan)

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 1 | M1 — Gold Complete | 11 workflows + 4 UAT scenarios passed |
| 2 | M2 — Snapshot Proven | Snapshot installs in <30 min, UAT-01 re-passed |
| 3 | M3 — Voice Locked | OD-01 resolved, bake-off avg ≥ 4.0/5.0 |
| 4 | M4 — Orchestration Live | End-to-end: form → call → GHL update → briefing |
| 5–6 | M5 — Pilot Deployed | First retainer via NeuronX, $18K ARR |

**Detailed plan**: `.trae/documents/6_WEEK_ROADMAP.md`

---

## Document Authority

| Document | Governs | Authority |
|---|---|---|
| `/docs/01_product/vision.md` | Product direction, principles, boundaries | Highest -- wins all conflicts |
| `/docs/01_product/prd.md` (this file) | Requirements, capabilities, scope | Second -- implements vision |
| `/docs/02_operating_system/operating_spec.md` | Operational detail: states, flows, rules, data | Third -- implements PRD |
| `/docs/02_operating_system/sales_playbook.md` | Human operational guide | Reference for NeuronX behavior |
| `/docs/03_infrastructure/ghl_capability_map.md` | GHL capability classification | Reference for build decisions |
| `/docs/04_compliance/trust_boundaries.md` | Regulatory and AI constraints | Binding -- overrides all feature requests |
| `/docs/05_governance/open_decisions.md` | Unresolved decisions | Active -- must be resolved before build |
| `/docs/06_execution/CURRENT_STATE.md` | Live build status, IDs, blockers | Agent reference -- updated after every task |
| `/neuronx-api/` | FastAPI thin brain implementation | Implement per Section 12 API contract |
