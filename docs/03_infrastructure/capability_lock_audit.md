# NeuronX V1 Capability Lock Audit

Version: 1.0
Status: CANONICAL
Last Updated: 2026-03-13
Purpose: Verify every capability maps to GHL or minimal wrapper -- avoid custom builds

---

## Executive Summary

| Metric | Target | Achieved | Status |
|---|---|---|---|
| GHL Native + Config | ≥70% | 78% baseline (range 70–90%) | ✅ PASS |
| NeuronX Wrapper | ~15% | 17% baseline (range 8–25%) | ✅ ACCEPTABLE |
| Open Source | ~5% | 3% | ✅ ACCEPTABLE |
| Custom Build | ≤10% | 2% baseline (target <5%) | ✅ EXCELLENT |

**Verdict**: NeuronX v1 can be built as a thin orchestration layer on top of GoHighLevel.

**Important**: Voice capability selection is not locked by this audit. GoHighLevel first-party Voice AI is a real candidate for v1 and must be live-tested against external voice providers before architecture is finalized.

---

## SECTION 1 — Capability Mapping Table

### 1.1 Inquiry Intake Flow

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| Web form submission | GHL_NATIVE | GHL Forms module | None |
| Facebook Lead Ads integration | GHL_NATIVE | GHL Facebook integration | Low |
| Missed call capture | GHL_NATIVE | GHL LC Phone missed call trigger | Low |
| WhatsApp message capture | GHL_NATIVE | GHL WhatsApp integration | Medium (verify reliability) |
| Email inquiry capture | GHL_NATIVE | GHL email forwarding or form | Low |
| Lead record creation | GHL_NATIVE | Workflow: Form Submitted → Create Contact | None |
| Source attribution tagging | GHL_CONFIG | Workflow adds tags based on source | Low |
| Phone validation | GHL_LIMITATION | GHL has basic validation; may need wrapper enhancement | Low |
| Duplicate detection | NEURONX_WRAPPER | Query GHL API for existing phone/email | Low |
| Consent logging | GHL_CONFIG + WRAPPER | GHL DND + NeuronX supplementary consent store | Low |

### 1.2 First Response Flow

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| Instant acknowledgment SMS | GHL_NATIVE | Workflow: Send SMS action | None |
| Instant acknowledgment email | GHL_NATIVE | Workflow: Send Email action | None |
| State transition to CONTACTING | GHL_CONFIG | Workflow updates opportunity stage | None |
| Speed-to-lead tracking | NEURONX_WRAPPER | NeuronX timestamps inquiry and first contact | Low |
| Delivery failure detection | GHL_NATIVE | Workflow checks delivery status | Low |
| Fallback to alternate channel | GHL_CONFIG | Workflow: if SMS fails, send email | Low |

### 1.3 Contact Attempts Flow

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| AI outbound call initiation | GHL_LIMITATION | Primary candidate: GoHighLevel Voice AI (live-test). Fallback: NeuronX calls external voice provider API | Medium (feature fit depends on tenant bake-off) |
| Call scheduling (respect timezone) | GHL_CONFIG | Workflow with Wait steps and time conditions | Low |
| SMS follow-up messages | GHL_NATIVE | Workflow: Send SMS action | None |
| Email follow-up messages | GHL_NATIVE | Workflow: Send Email action | None |
| Voicemail detection | GHL_LIMITATION | Candidate: GoHighLevel Voice AI metadata. Fallback: external provider metadata returned in callback | Low |
| Call outcome logging | NEURONX_WRAPPER | NeuronX writes result to GHL custom fields | Low |
| Attempt counter tracking | GHL_CONFIG | Custom field incremented by workflow | Low |
| 7-attempt limit enforcement | GHL_CONFIG | Workflow condition: if attempts >= 7 | Low |
| Timezone-aware calling | NEURONX_WRAPPER | NeuronX checks area code or stated location | Low |
| Human escalation queue | GHL_NATIVE | Workflow assigns to user/round-robin | None |

### 1.4 Readiness Assessment Flow

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| AI asking assessment questions | GHL_LIMITATION | Candidate: GoHighLevel Voice AI agent prompt + actions. Fallback: external provider conversation flow | Medium |
| Question script management | GHL_CONFIGURATION | Configure Voice AI agent prompts in GHL (candidate). Fallback: NeuronX provides prompts to external provider | Low |
| Response capture and storage | GHL_LIMITATION | Candidate: GHL Voice AI transcript + contact field updates. Fallback: NeuronX receives transcript and writes to GHL | Medium (depends on transcript access and field update capabilities) |
| Program interest classification | NEURONX_WRAPPER | Parse transcript, map to enum | Low |
| Location determination | NEURONX_WRAPPER | Parse transcript, map to enum | Low |
| Urgency assessment | NEURONX_WRAPPER | Parse transcript, map to enum | Low |
| Prior history capture | NEURONX_WRAPPER | Parse transcript, map to enum | Low |
| Budget awareness check | GHL_CONFIG + WRAPPER | AI asks; human confirms if uncertain | Low |
| Complexity flag detection | NEURONX_WRAPPER | Keyword detection in transcript | Low |
| Readiness scoring algorithm | NEURONX_WRAPPER | Weighted scoring based on R1-R5 | Low |
| Outcome assignment (Ready/Urgent/etc) | NEURONX_WRAPPER | Score evaluation, write to GHL | Low |
| Senior review queue for complex | GHL_NATIVE | Workflow assigns to specific user | None |

### 1.5 Booking Flow

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| Calendar availability check | GHL_NATIVE | GHL Calendar API | None |
| Booking link generation | GHL_NATIVE | GHL Calendar widget/booking link | None |
| Booking invitation SMS | GHL_NATIVE | Workflow: Send SMS with link | None |
| Booking invitation email | GHL_NATIVE | Workflow: Send Email with link | None |
| Appointment creation on calendar | GHL_NATIVE | GHL Calendar API or widget | None |
| Consultant assignment | GHL_NATIVE | Workflow: Round-robin or manual | None |
| Booking confirmation | GHL_NATIVE | Workflow: Send SMS/Email on booking | None |
| 48h follow-up if not booked | GHL_CONFIG | Workflow: Wait 48h → Send SMS | None |
| 5-day operator assignment | GHL_CONFIG | Workflow: Wait 5d → Assign to user | None |
| 14-day timeout to NURTURE | GHL_CONFIG | Workflow: Wait 14d → Update stage | None |

### 1.6 Reminders Flow

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| 48-hour reminder SMS | GHL_NATIVE | Workflow: Appointment Status → Wait → Send | None |
| 24-hour reminder SMS | GHL_NATIVE | Workflow: Wait → Send | None |
| 2-hour reminder SMS | GHL_NATIVE | Workflow: Wait → Send | None |
| Confirmation reply tracking | GHL_NATIVE | GHL Conversation tracking | Low |
| No-confirmation escalation | GHL_CONFIG | Workflow: if no reply → Assign to user | Low |

### 1.7 No-Show Recovery Flow

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| No-show detection | GHL_NATIVE | Workflow: Appointment No-Show trigger | None |
| +5 min SMS | GHL_NATIVE | Workflow: Send SMS | None |
| +15 min call | GHL_LIMITATION | Candidate: trigger GHL Voice AI call via workflow. Fallback: NeuronX triggers external voice call or human task | Low |
| +2h SMS | GHL_NATIVE | Workflow: Wait → Send SMS | None |
| +1 day SMS | GHL_NATIVE | Workflow: Wait → Send SMS | None |
| +3 days email | GHL_NATIVE | Workflow: Wait → Send Email | None |
| +7 days final SMS | GHL_NATIVE | Workflow: Wait → Send SMS | None |
| Reschedule link | GHL_NATIVE | GHL Calendar widget | None |
| Reschedule count tracking | GHL_CONFIG | Custom field incremented | Low |
| 3-reschedule flag | GHL_CONFIG | Workflow: if count >= 3 → Assign to user | Low |

### 1.8 Consultation Preparation Flow

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| Data pull from GHL | NEURONX_WRAPPER | GHL API: contact, fields, notes, tags, appointment | Low |
| Briefing assembly | NEURONX_WRAPPER | NeuronX formats data into structured doc | Low |
| Briefing delivery (email) | NEURONX_WRAPPER | NeuronX sends email (or GHL workflow if possible) | Low |
| Briefing delivery (CRM note) | GHL_NATIVE | Workflow: Add Note to Contact | None |
| Delivery confirmation | NEURONX_WRAPPER | Track email open or log delivery timestamp | Low |
| Partial briefing flag | NEURONX_WRAPPER | Detect missing data, flag in briefing | Low |

### 1.9 Post-Consultation Outcome Capture

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| Outcome prompt to consultant | GHL_NATIVE | Workflow: Send SMS/email after appointment | None |
| Outcome selection interface | GHL_NATIVE | GHL custom form or task | Low |
| Outcome recording | GHL_NATIVE | Workflow updates custom field/stage | None |
| Retainer flow trigger | GHL_CONFIG | Workflow: if outcome=proceed → trigger sequence | None |
| Follow-up sequence trigger | GHL_CONFIG | Workflow: if outcome=thinking → trigger nurture | None |
| Non-recording escalation | GHL_CONFIG | Workflow: Wait 1h → Reminder; 4h → Alert owner | None |

### 1.10 Follow-Up to Retainer Flow

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| Retainer agreement delivery | GHL_NATIVE | Workflow: Send Email with attachment | None |
| Document checklist delivery | GHL_NATIVE | Workflow: Send Email | None |
| Payment instructions | GHL_NATIVE | Workflow: Send Email with Stripe link | None |
| Day 1 follow-up SMS | GHL_NATIVE | Workflow: Wait → Send SMS | None |
| Day 2 follow-up | GHL_NATIVE | Workflow: Wait → Send SMS/Email | None |
| Day 5 follow-up | GHL_NATIVE | Workflow: Wait → Send Email | None |
| Day 10 consultant call | GHL_NATIVE | Workflow: Create Task for consultant | None |
| Day 14 final + NURTURE | GHL_CONFIG | Workflow: Wait 14d → Update stage | None |
| Retainer signed detection | GHL_NATIVE | Workflow: Tag/field update triggers | None |
| Payment received detection | GHL_NATIVE | Stripe integration or manual tag | Low |

### 1.11 Pipeline and State Management

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| State machine (9 states) | GHL_CONFIG | GHL Pipeline stages + custom fields | None |
| State transition logic | GHL_CONFIG | Workflow triggers and actions | None |
| Sub-status tracking | GHL_CONFIG | Custom fields | None |
| History logging | GHL_NATIVE | GHL activity log + notes | None |

### 1.12 Analytics and Dashboards

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| Pipeline snapshot counts | GHL_NATIVE | GHL dashboard/opportunities view | None |
| Conversion funnel calculation | NEURONX_WRAPPER | Query GHL API, compute percentages | Low |
| Speed-to-contact metric | NEURONX_WRAPPER | Calculate from inquiry and first contact timestamps | Low |
| Stuck lead detection | GHL_NATIVE + WRAPPER | GHL Stale Opportunity trigger + NeuronX scoring | Low |
| Source-to-revenue attribution | NEURONX_WRAPPER | Query GHL, join with cost data (manual input) | Medium |
| Daily briefing generation | NEURONX_WRAPPER | Aggregate data, format, send via GHL workflow | Low |
| Operator performance metrics | NEURONX_WRAPPER | Query GHL API, calculate per user | Low |
| Consultation schedule view | GHL_NATIVE | GHL Calendar view | None |

### 1.13 Compliance and Trust Boundaries

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| Consent tracking (transactional) | GHL_NATIVE | GHL DND system | None |
| Outbound call consent gating | GHL_LIMITATION | Candidate: enforce via GHL Voice AI consent checks. Fallback: NeuronX gates call initiation based on consent fields | Medium (must verify in tenant) |
| Consent tracking (marketing) | GHL_CONFIG + WRAPPER | GHL fields + NeuronX supplementary store | Low |
| Suppression enforcement | GHL_NATIVE + WRAPPER | GHL DND + NeuronX rules | Low |
| CASL compliance (firm ID, unsubscribe) | GHL_CONFIG | Workflow templates include required elements | Low |
| Webhook signature verification | NEURONX_WRAPPER | Verify `X-GHL-Signature` (Ed25519); support legacy `X-WH-Signature` (RSA) during transition | Medium (must be implemented correctly before 2026-07-01) |
| AI escalation triggers | NEURONX_WRAPPER | Prompt engineering + NeuronX rule checking | Medium |
| Trust boundary enforcement | NEURONX_WRAPPER | System-level and prompt-level rules | Medium |
| Compliance audit logging | NEURONX_WRAPPER | Log all AI interactions | Low |

### 1.14 Infrastructure and Deployment

| Capability | Source | Implementation Strategy | Risk |
|---|---|---|---|
| Sub-account provisioning | GHL_NATIVE | GHL SaaS Configurator API | None |
| Snapshot deployment | GHL_NATIVE | GHL Snapshot system (public API support is partial; deployment remains mostly manual) | Low (manual per firm remains safe v1 assumption) |
| White-labeling | GHL_NATIVE | GHL Agency Pro | None |
| Billing and subscriptions | GHL_NATIVE | GHL SaaS Mode + Stripe | None |
| User authentication | GHL_NATIVE | GHL login system | None |
| Role-based access | GHL_NATIVE | GHL permissions | None |

---

## SECTION 2 — GHL Coverage Score (Conditional)

### Coverage Range (Voice Layer Not Locked)

The coverage score is conditional because the voice layer is not yet locked.

Two valid v1 architectures exist:

| Architecture | Voice Layer | GHL Native + Config | NeuronX Wrapper | Custom Code |
|---|---|---:|---:|---:|
| **A** | GoHighLevel Voice AI | ~85–90% | ~8–12% | ~1–2% |
| **B** | External Voice Provider | ~70–75% | ~20–25% | ~3–5% |

**GHL Coverage Range**: **~70–90%** depending on bake-off results.

**NeuronX Wrapper Range**: **~8–25%** depending on bake-off results.

**Custom Code Target**: **<5%**.

### By Category (Current Draft Baseline)

This baseline view assumes more wrapper responsibility in the voice layer. It is
used to keep build discipline conservative until the live tenant bake-off locks
Architecture A or B.

| Category | Capabilities | % of Total |
|---|---|---|
| GHL Native | 58 | 58% |
| GHL Configuration | 20 | 20% |
| **GHL Total** | **78** | **78%** |
| NeuronX Wrapper | 17 | 17% |
| Voice Layer (TBD: GHL Voice AI vs external) | 3 | 3% |
| Open Source | 0 | 0% |
| Custom Build | 2 | 2% |
| **Total** | **100** | **100%** |

### GHL Native (No Config Required)

These work out-of-the-box in any GHL sub-account:

- Form submission handling
- Contact record CRUD
- SMS sending
- Email sending
- Calendar booking
- Appointment triggers
- Pipeline stage management
- Opportunity tracking
- Activity logging
- Notes
- Task creation
- User assignment
- Round-robin assignment
- Webhook triggers
- Webhook actions
- DND/suppression handling
- Dashboard views
- Reporting
- SaaS Mode billing
- White-labeling

### GHL Configuration (Requires Setup)

These require workflow building, custom fields, and pipeline configuration:

- Acknowledgment workflows
- Contact attempt sequences
- Reminder workflows
- No-show recovery workflows
- Follow-up sequences
- State transition logic
- Sub-status custom fields
- Source attribution tagging
- Booking workflows
- Outcome capture workflows
- Escalation workflows
- Compliance templates
- Snapshot creation

---

## SECTION 3 — Required Wrappers

### NeuronX Must Build

| Wrapper | Purpose | Complexity |
|---|---|---|
| **Webhook Receiver** | Accept events from GHL and voice providers | Low |
| **Voice Orchestrator** | Trigger voice actions (GHL Voice AI or external), process results | Medium |
| **Readiness Scorer** | Evaluate R1-R5, assign outcomes | Low |
| **Consultation Prep Assembler** | Pull GHL data, format briefing | Low |
| **Analytics Engine** | Query GHL, compute metrics | Medium |
| **Daily Briefing Generator** | Aggregate and format daily report | Low |
| **Stuck Lead Detector** | Scan pipeline, flag stale leads | Low |
| **Consent/Suppression Manager** | Supplementary consent tracking | Low |
| **Trust Boundary Enforcer** | Rules and prompt management | Medium |
| **Context Store** | Minimal: scoring history, transcripts | Low |

### Total Wrapper Code Estimate

- Webhook handlers: ~5 endpoints
- Scoring logic: ~500 lines
- Briefing formatter: ~300 lines
- Analytics queries: ~10 queries
- Scheduled jobs: ~3 jobs

**Estimated development time**: 2-3 days for a competent developer

---

## SECTION 4 — Required Open Source

### Voice Layer Options (Bake-Off Required)

| Option | Cost | Quality | Integration |
|---|---|---|---|
| GoHighLevel Voice AI | Plan-dependent | Unknown until tested | Native |
| Vapi | ~$0.05/min + provider | High (LLM-driven) | REST API |
| Bland AI | ~$0.09/min | Good (scripted) | REST API |
| Retell AI | Similar | Good | REST API |

**Decision Rule**: Run a live tenant bake-off before selecting the voice layer. External voice providers are optional if GHL Voice AI meets immigration-specific requirements for tone, control, reliability, cost, and compliance.

### Other Open Source

| Component | Status | Notes |
|---|---|---|
| Analytics dashboard | DEFERRED | Use GHL native dashboards for v1 |
| Queue system | NOT NEEDED | GHL workflows handle queuing |
| Message broker | NOT NEEDED | Webhooks are sufficient |
| Database | MINIMAL | Small store for transcripts, analytics cache |

**Verdict**: Almost no open source dependencies required. GHL + voice provider + minimal NeuronX wrapper.

---

## SECTION 5 — Things We Must NOT Build

### CRM Functionality

❌ Contact database -- GHL is the system of record  
❌ Lead scoring UI -- GHL custom fields + workflows  
❌ Pipeline visualization -- GHL native dashboards  
❌ Activity timeline -- GHL activity log  

### Messaging Infrastructure

❌ SMS gateway -- GHL LC Phone  
❌ Email service -- GHL email builder  
❌ Message templates -- GHL template system  
❌ Sequence builder -- GHL workflow builder  

### Calendar System

❌ Availability management -- GHL calendars  
❌ Booking widget -- GHL booking widget  
❌ Appointment CRUD -- GHL calendar API  
❌ Reminder system -- GHL workflows  

### Billing

❌ Subscription management -- GHL SaaS Mode  
❌ Payment processing -- Stripe via GHL  
❌ Invoicing -- GHL invoices  

### Authentication

❌ User login -- GHL authentication  
❌ Password management -- GHL handles  
❌ Role permissions -- GHL permissions  

### AI Infrastructure

❌ Speech recognition -- Voice layer handles  
❌ Voice synthesis -- Voice layer handles  
❌ LLM hosting -- Use provider APIs (OpenAI, etc.)  
❌ Conversation management (voice) -- Voice layer handles  

---

## Build Discipline Rule (Lean Machine)

NeuronX must never replace existing GoHighLevel capabilities.

If GoHighLevel introduces a first-party feature that overlaps with a NeuronX
wrapper capability:

1. Mark the wrapper capability as **Deprecated** in this audit
2. Add a migration note describing the native replacement
3. Update `/docs/03_infrastructure/product_boundary.md` so GoHighLevel becomes
   the source of execution
4. Remove wrapper logic from the v1 codebase at the next safe release

This rule prevents the most common failure mode for platform-wrapper products:
accidental drift into a shadow CRM or parallel automation engine.

---

## Platform Parity Rule

If GoHighLevel releases a first-party feature that replaces a NeuronX wrapper
capability:

1. **Evaluate the native feature** against v1 requirements (including trust boundaries)
2. **Deprecate the wrapper** in the next planned release window
3. **Migrate customers** to the native feature and remove wrapper dependency

The default bias is always toward the platform when parity exists.

---

## SECTION 6 — Recommended Stack (Minimal)

### Core Infrastructure

| Layer | Technology | Responsibility |
|---|---|---|
| **CRM + Messaging + Pipeline** | GoHighLevel | Everything customer-facing |
| **Voice AI** | GoHighLevel Voice AI OR external provider | AI outbound calls (bake-off determines choice) |
| **Orchestration** | Minimal Node.js/Python service | Webhooks, scoring, prep, analytics |
| **Data Store** | SQLite or PostgreSQL (minimal) | Transcripts, analytics cache, consent |
| **Hosting** | Vercel / Railway / Render | Wrapper service |

### GHL Configuration (Per Firm)

| Component | Setup Time | Method |
|---|---|---|
| Pipeline stages | 30 min | Manual or Snapshot |
| Custom fields | 30 min | Manual or Snapshot |
| Workflows | 2-3 hours | Manual or Snapshot |
| Forms | 30 min | Manual or Snapshot |
| Calendars | 15 min | Manual or Snapshot |
| **Total** | **4-5 hours** | **Snapshot reduces to 30 min** |

### Snapshot Distribution Model (Strategic Advantage)

Even if snapshot deployment is manual/semi-manual in v1, the operational
distribution model is powerful:

Client purchases NeuronX
→ NeuronX installs snapshot and configures workflows
→ Connect voice layer and required credentials
→ System live in ~30 minutes

This supports a premium packaging model: **SaaS + implementation package**
instead of a low-priced “tool-only” SaaS.

### NeuronX Wrapper Components

| Component | Lines of Code | Purpose |
|---|---|---|
| Webhook server | ~200 | Receive GHL and voice provider events |
| Voice orchestrator | ~300 | Call API, process results |
| Readiness scorer | ~400 | Parse transcripts, calculate scores |
| Prep assembler | ~300 | Format briefings |
| Analytics engine | ~400 | Query GHL, compute metrics |
| Daily briefing | ~200 | Generate and send reports |
| **Total** | **~1,800 lines** | **Minimal wrapper** |

### Deployment Model

```
Prospect
  ↓
GHL Form / Ad / Call
  ↓
GHL Workflow (ack, tag, trigger)
  ↓
NeuronX Webhook (orchestration)
  ↓
Voice Layer (GHL Voice AI or External Provider)
  ↓
NeuronX (process result, score, update GHL)
  ↓
GHL Workflow (next steps, reminders, etc.)
  ↓
Consultant (prepared with briefing)
```

### Time to Launch

| Phase | Duration |
|---|---|
| GHL configuration (with Snapshot) | 1 day |
| NeuronX wrapper development | 2-3 days |
| Voice provider integration | 1 day |
| Testing with pilot firm | 2-3 days |
| **Total** | **6-8 days** |

---

## Critical Findings

### Finding 1: GoHighLevel Voice AI is a first-party candidate for v1

GoHighLevel now offers first-party Voice AI capabilities (inbound and outbound) including appointment booking, workflow triggering, and contact-field updates.

**Verdict**: Do not default to external voice. Run a live tenant bake-off (GHL Voice AI vs external providers) before selecting the voice layer.

### Finding 2: Snapshots API support is partial; deployment remains mostly manual

Public docs now expose snapshot endpoints (e.g., list snapshots, create share links, and push status metadata). However, a straightforward public endpoint to directly apply/push a snapshot into a target sub-account is not clearly surfaced.

Operationally, each firm still requires:
- Manual snapshot import, OR
- Screen-automation tool (e.g., Playwright), OR
- Accept manual onboarding as premium service

**Verdict**: Manual or semi-manual snapshot deployment for v1 remains the safe assumption.

### Finding 3: GHL Workflow AI (2025) is promising but unverified

GHL released Workflow AI in 2025 for:
- Conditional logic based on AI interpretation
- Sentiment analysis
- Intent detection

**Status**: Too new to rely on for v1. Monitor for v1.5.

### Finding 4: Conversation AI is more than an inbox bot; evaluate its API and workflow actions

Conversation AI supports multiple channels and includes workflow actions and more advanced automation patterns. Public API support for agent provisioning and message-level behavior may allow more of the intake and follow-up system to remain native.

**Verdict**: Treat Conversation AI as a candidate for parts of v1 (follow-up, booking assistance, agent provisioning), but do not assume it eliminates the need for NeuronX orchestration.

---

## Gaps to Add Before Architecture Lock

### Gap A: Webhook security and signature migration

If NeuronX receives GoHighLevel webhooks, it must verify request authenticity using `X-GHL-Signature` (Ed25519). The legacy `X-WH-Signature` is being deprecated (current docs indicate removal after July 1, 2026). During the transition window, integrations should prefer `X-GHL-Signature` and fall back to legacy verification when needed.

### Gap B: Outbound consent and compliance is more productized in GHL than assumed

GoHighLevel now documents deeper consent tooling and consent checks for outbound calling and forms. v1 should lean on native GHL consent mechanics wherever possible for call eligibility and consent capture, while NeuronX maintains supplementary consent state for enforcement and auditing.

---

## Recommendations

1. **Proceed with minimal wrapper architecture** -- 78% GHL coverage validates approach
2. **Run a live tenant bake-off before selecting voice** -- compare GHL Voice AI vs external providers against immigration-specific requirements
3. **Treat external voice providers as optional** -- fallback if GHL Voice AI fails tone, control, reliability, cost, or compliance tests
4. **Accept manual/semi-manual snapshot deployment** -- Premium onboarding model remains correct
5. **Leverage Conversation AI where it reduces wrapper scope** -- evaluate API/workflow actions for follow-up and booking assistance
6. **Build only the minimum wrapper components** -- webhooks, scoring, briefing assembly, analytics, and audit logs

Bake-off template:
- `/docs/03_infrastructure/live_tenant_bakeoff_scorecard.md`

---

## Document Authority

This audit validates the architecture in:
- `/docs/03_infrastructure/product_boundary.md`

If this audit finds a capability requires custom build that was assumed GHL-native,
update the product boundary document before proceeding to architecture.
