# NeuronX V1 Product Boundary

Version: 1.0
Status: CANONICAL
Last Updated: 2026-03-13
Authority: Founder
Purpose: Define exact system boundaries between GHL, NeuronX, and external providers

---

## 1. What NeuronX IS in V1

NeuronX in v1 is a **small orchestration service** that sits between GoHighLevel
and external providers (voice AI, email delivery). It is NOT a full application
backend. It is NOT a standalone product.

NeuronX v1 is:

- A webhook receiver (receives events from GHL and voice providers)
- A webhook sender (pushes data back to GHL via API)
- A scoring engine (evaluates readiness dimensions, assigns outcomes)
- A content assembler (pulls CRM data, assembles consultation briefings)
- A scheduling engine (triggers timed actions: follow-ups, reminders, alerts)
- An analytics calculator (computes funnel metrics from GHL pipeline data)
- A rules enforcer (applies business rules, trust boundaries, consent logic)

NeuronX v1 has:

- A small persistent data store (for context memory, analytics cache, audit log)
- An API layer (receives webhooks, serves dashboard data)
- A scheduled job runner (daily briefings, stuck-lead detection, nurture triggers)

NeuronX v1 does NOT have:

- A user-facing CRM (GHL is the CRM)
- A messaging system (GHL sends SMS/email)
- A calendar system (GHL manages calendars)
- A form builder (GHL provides forms)
- A billing system (GHL SaaS Mode + Stripe)
- A voice calling platform (voice execution is handled by GoHighLevel Voice AI or an external provider)

---

## 2. What NeuronX is NOT in V1

| Not This | Why | Where This Lives |
|---|---|---|
| CRM | Configure-first principle | GoHighLevel |
| Messaging platform | GHL handles SMS, email, WhatsApp | GoHighLevel |
| Calendar/booking system | GHL calendars are sufficient | GoHighLevel |
| Form builder | GHL forms with custom fields | GoHighLevel |
| Voice calling platform | Voice execution is provider-managed | GoHighLevel Voice AI OR external provider |
| Billing system | SaaS Mode handles subscriptions | GoHighLevel + Stripe |
| Case management system | Post-retention, out of scope | Docketwise / INSZoom / etc. |
| Document management | Out of scope | External tools |
| Full application backend | Over-engineered for v1 needs | Deferred to v2 if needed |
| Mobile app | Web-responsive is sufficient | Deferred |
| AI model host | Use provider APIs | Voice AI provider + LLM API |

---

## 3. What Runs Inside GoHighLevel

GHL is the **system of record** for lead data and the **execution engine** for
messaging and workflow automation.

### Workflow Responsibility Split (Anti-Overengineering)

#### Layer 1 — GoHighLevel Workflows (Execution Layer)

GoHighLevel workflows handle:
- Lead capture and contact creation
- Acknowledgment messaging
- Pipeline stage movement
- Appointment booking and calendars
- Reminders
- SMS/email sequences
- Task creation and assignment
- Most timing logic (Wait steps)

#### Layer 2 — NeuronX Orchestration (Intelligence Layer)

NeuronX handles:
- Voice layer orchestration and outcome normalization (GHL Voice AI or external)
- Readiness scoring and classification
- Consultation briefing assembly
- Stuck-lead detection beyond basic triggers
- Funnel analytics and reporting
- Trust boundary enforcement and compliance auditing

**Rule**: If a capability can be implemented safely as a GHL workflow, it must live in Layer 1.

### GHL Owns

| Domain | What GHL Manages | How NeuronX Interacts |
|---|---|---|
| **Contact records** | All lead data: name, phone, email, custom fields, tags, notes | NeuronX reads via API, writes back via API |
| **Pipeline and opportunities** | Stage definitions, stage movements, opportunity values | NeuronX triggers stage changes via API |
| **Workflows** | All trigger-action automation: form submission -> ack, appointment -> reminder, tag -> sequence | NeuronX triggers workflows by adding tags or updating fields |
| **Calendars** | Consultant availability, booking widgets, appointments | NeuronX reads appointments via API for prep timing |
| **Messaging** | SMS sending, email sending, templates, sequences | GHL sends all messages. NeuronX does not send messages directly. |
| **Forms** | Intake forms, survey forms | Form submissions trigger GHL workflows -> webhook to NeuronX |
| **Sub-accounts** | Per-firm tenant isolation | NeuronX provisions via SaaS Configurator API |
| **Billing** | Subscription management, payment collection | GHL SaaS Mode + Stripe. NeuronX does not handle payments. |
| **DND/Compliance** | Built-in opt-out handling for phone/SMS | GHL enforces. NeuronX maintains supplementary consent records. |

### GHL Does NOT Own

| Domain | Why | Who Owns |
|---|---|---|
| Voice layer selection and orchestration | Depends on v1 bake-off result | NeuronX governs choice; execution is GHL Voice AI or external provider |
| Readiness scoring logic | GHL if/else is too simple | NeuronX scoring engine |
| Consultation briefing content | GHL cannot assemble and format data | NeuronX content assembler |
| Pipeline analytics | GHL reporting is basic | NeuronX analytics engine |
| Trust boundary enforcement | GHL has no concept of regulatory guardrails | NeuronX rules engine |
| AI conversation context | GHL does not persist AI state | NeuronX context store |

---

## 4. What Runs Inside NeuronX

NeuronX is a **stateless-where-possible, lightweight orchestration service**.

### Core Components

| Component | Purpose | Inputs | Outputs |
|---|---|---|---|
| **Webhook Receiver** | Accept events from GHL and voice layer | GHL webhook (form submission, appointment, stage change). Voice layer callback/event (call ended, transcript/summary). | Internal event processing |
| **Voice Orchestrator** | Trigger voice actions and process results | New lead event. Lead CRM data from GHL. | Candidate A: trigger GHL Voice AI via native mechanisms. Candidate B: call external voice provider API. Write outcomes back to GHL. |
| **Readiness Scorer** | Evaluate lead readiness for consultation | Readiness dimension data from call or form | Readiness outcome (Ready/Urgent/Complex/Not Ready/Disqualified). Written to GHL custom fields. |
| **Consultation Prep Engine** | Assemble pre-consultation briefing | All lead data from GHL (contact, fields, notes, tags, appointment) | Structured briefing document. Delivered via email and/or GHL note. |
| **Analytics Engine** | Calculate pipeline metrics | GHL pipeline data (via API queries) | Dashboard data. Daily briefing. Stuck-lead alerts. |
| **Rules Engine** | Enforce business rules and trust boundaries | All events and data | Rule outcomes: escalation triggers, suppression actions, speed alerts |
| **Scheduled Jobs** | Time-based triggers | Clock + pipeline state | Daily briefings, stuck-lead scans, nurture triggers |
| **Context Store** | Persist AI conversation state (v1.5 scope, minimal in v1) | Call transcripts, interaction summaries | Context injection for subsequent interactions |

### Data NeuronX Stores

NeuronX maintains a **small, supplementary data store**. GHL remains the system
of record for all lead data.

| Data | Why NeuronX Stores It | Why Not in GHL |
|---|---|---|
| Analytics cache | Pre-computed metrics for dashboard performance | GHL has no custom analytics store |
| Voice transcripts / summaries | Voice layer returns data that needs processing and auditability | Can also be written to GHL notes, but NeuronX may require raw data for scoring and compliance review |
| Readiness scoring history | Audit trail of how scores were computed | GHL custom fields store the outcome, but not the computation |
| Consent/suppression records | Supplementary to GHL DND, needed for NeuronX-specific rules | GHL DND is binary; NeuronX needs reason, method, timestamp |
| Scheduled job state | Track which jobs have run, pending actions | GHL workflows handle some; NeuronX handles the rest |
| Compliance audit log | Record of all AI interactions for compliance review | GHL does not have a compliance-specific audit log |

---

## 5. External Providers

### Voice Layer (Open Decision OD-01)

| Aspect | Specification |
|---|---|
| Role | Execute AI outbound calls (and potentially inbound). Return call outcome and transcript/summary. |
| Options | GoHighLevel Voice AI (first-party) OR external provider (Vapi/Bland/Retell/etc.) |
| Integration pattern (external) | NeuronX calls provider API to initiate call. Provider calls NeuronX webhook when call ends with result. |
| Integration pattern (GHL Voice AI) | GHL handles call execution natively. NeuronX consumes resulting state changes/fields/notes via API and/or webhooks. |
| NeuronX responsibility | Own decision and governance of voice layer, enforce trust boundaries, normalize outcomes into GHL fields, maintain audit trail. |
| Voice layer responsibility | Call execution, voice synthesis, speech recognition, conversation management. |
| Failure mode | Voice layer unavailable: route leads to human operator queue. No data loss; v1 remains operational via GHL workflows. |

### Email Delivery

| Aspect | Specification |
|---|---|
| Role | Deliver consultation briefings when sent from NeuronX (not GHL workflow) |
| Integration pattern | NeuronX uses email API (provider TBD: could be GHL's own email API, SendGrid, or similar) |
| Scope | Only for NeuronX-originated emails (briefings, daily reports). All prospect-facing email goes through GHL. |
| Failure mode | Email fails: fallback to GHL contact note + SMS alert |

### SMS Delivery

| Aspect | Specification |
|---|---|
| Role | All prospect-facing SMS |
| Integration pattern | All SMS sent through GHL. NeuronX triggers SMS by adding tags or updating fields that fire GHL workflows. |
| Scope | NeuronX never sends SMS directly. GHL is the SMS gateway. |
| Failure mode | GHL SMS fails: NeuronX detects via API check, flags for operator. |

---

## 6. Data Ownership Boundaries

### Data Authority Rule (Prevent Shadow CRM)

#### Source of Truth Hierarchy

1. **GoHighLevel** (system of record)
2. **External providers** (raw artifacts such as voice transcripts/summaries)
3. **NeuronX derived data** (scores, classifications, analytics)

#### NeuronX Must Never Be Authoritative For

- Contacts and contact fields (identity, phone, email)
- Conversation threads (SMS/email inbox history)
- Pipeline stages and opportunity records
- Appointment records and calendar availability

#### NeuronX May Store (Limited)

- Derived intelligence (readiness outcomes, flags, scoring history)
- Temporary orchestration state (retry queues, idempotency keys)
- Analytics cache (precomputed funnels and dashboards)
- Compliance audit log (AI interaction record, signature verification results)

This rule avoids the #1 platform-wrapper failure mode: accidental creation of a
shadow CRM that diverges from GoHighLevel.

| Data Domain | System of Record | Read Access | Write Access |
|---|---|---|---|
| Lead contact info | GHL | NeuronX (API) | GHL (forms, manual). NeuronX (API updates). |
| Pipeline state | GHL | NeuronX (API) | GHL (workflows). NeuronX (API stage changes). |
| Custom fields (readiness, flags) | GHL | NeuronX (API) | NeuronX (API). GHL (workflows). |
| Tags | GHL | NeuronX (API) | Both (NeuronX adds tags to trigger GHL workflows) |
| Notes | GHL | NeuronX (API) | Both |
| Appointments | GHL | NeuronX (API) | GHL (booking widget, workflows). NeuronX (API if needed). |
| Messages (SMS/email content) | GHL | NeuronX (API, limited) | GHL only. NeuronX does not compose prospect-facing messages. |
| AI call transcripts | Voice layer | NeuronX (copy) | Voice layer emits transcript/summary. NeuronX stores copy for scoring/audit and mirrors summary to GHL notes. |
| Readiness scores | GHL (outcome) + NeuronX (computation) | Both | NeuronX writes outcome to GHL. NeuronX stores computation details. |
| Analytics / metrics | NeuronX | NeuronX only | NeuronX (computed from GHL data) |
| Consent records | GHL (DND) + NeuronX (supplementary) | Both | GHL manages DND. NeuronX manages detailed consent/suppression. |
| Billing / subscription | GHL (Stripe) | Neither (Stripe dashboard) | GHL SaaS Mode |

### Data Conflict Resolution

If GHL and NeuronX have conflicting data for the same lead:
- **GHL wins** for contact info, pipeline state, appointments, and messages
- **NeuronX wins** for readiness scores, analytics, AI transcripts, and consent details
- **Neither overwrites the other silently** -- conflicts are logged and flagged for review

For clarity:
- **GHL remains authoritative** even when NeuronX temporarily caches data.
- **External provider artifacts** (e.g., transcripts) are treated as evidence and may be mirrored into GHL notes.
- **NeuronX stores only derived intelligence** and must be safe to wipe without losing the firm’s operational system.

---

## 7. Failure Isolation Boundaries

### Principle

Failure in one system must not cascade into total system failure. GHL and
NeuronX must be able to operate independently in degraded mode.

### Failure Scenarios

| Failed System | Impact on GHL | Impact on NeuronX | Impact on Firm |
|---|---|---|---|
| **NeuronX down** | GHL continues: ack SMS sent, reminders fire, booking works, pipeline visible | AI calling stops. Prep not generated. Analytics stale. | Operators work from GHL dashboard directly. No AI speed-to-lead. No briefings. Manual operation. |
| **GHL down** | All CRM, messaging, booking stopped | NeuronX cannot read/write CRM data. Queues operations. | Firm cannot operate intake pipeline. Emergency: manual tracking until restored. |
| **Voice layer down (GHL Voice AI or external)** | If GHL Voice AI down: voice degraded within GHL. If external down: no impact on GHL core. | AI calls fail. NeuronX routes to human queue. | Human operators handle calls. Speed-to-lead degrades. |
| **NeuronX + voice layer down** | GHL continues normally | Both AI systems offline | GHL handles ack, reminders, booking. Humans handle calls and prep. Degraded but functional. |
| **GHL + NeuronX down** | Full outage | Full outage | Firm uses phone and email manually until restored. |

### Design Rule

NeuronX must NEVER be a single point of failure for critical firm operations.
GHL must always be able to function for: lead capture, messaging, booking,
reminders, and pipeline visibility -- even if NeuronX is completely offline.

NeuronX adds value (AI speed, scoring, prep, analytics) but the firm's
core intake operation must survive NeuronX downtime.

---

## 8. Deployment Model

### V1 Deployment Architecture (Architecture-Neutral Description)

| Component | Deployment | Notes |
|---|---|---|
| GHL | SaaS (managed by HighLevel) | No deployment responsibility for NeuronX |
| NeuronX orchestrator | Single deployed service | Receives webhooks, processes events, calls APIs |
| NeuronX data store | Managed database | Small footprint: analytics, transcripts, audit log, consent |
| NeuronX scheduled jobs | Part of orchestrator or separate worker | Daily briefings, stuck-lead scans, nurture triggers |
| Voice AI provider | SaaS (managed by provider) | No deployment responsibility for NeuronX |

### Deployment Requirements

| Requirement | Specification |
|---|---|
| Availability | NeuronX must be available during business hours (8 AM - 10 PM firm local time) minimum. 24/7 preferred for AI speed-to-lead. |
| Latency | Webhook processing: < 5 seconds from receipt to action. API calls to GHL: within rate limits. |
| Scalability | v1 must support 1-10 firms with up to 500 inquiries/month each (5,000 inquiries/month total). |
| Recovery | If NeuronX fails, queued events must be retried on recovery. No data loss. |
| Monitoring | Health check endpoint. Alert on: downtime, high error rate, webhook processing delay. |
| Logging | All webhook events, API calls, scoring decisions, and trust boundary checks logged. |

---

## Webhook Security Boundary

NeuronX must verify authenticity of all incoming GoHighLevel webhooks.

- Prefer verification using `X-GHL-Signature` (Ed25519)
- Support fallback verification using legacy `X-WH-Signature` (RSA) during the transition window
- Do not process a webhook if signature verification fails
- Reject replay attacks using webhook `timestamp` and unique `webhookId` (when present in payload)
- Apply a maximum clock-skew window (configurable) and reject stale deliveries
- Log verification failures with webhook ID and timestamp

This is mandatory for v1 because the legacy signature header is being deprecated and will be removed after the transition period.

### What This Is NOT

This is not an architecture document. It does not specify:
- Programming language
- Framework
- Cloud provider
- Database technology
- Deployment tooling

Those decisions are made in the architecture phase, governed by this boundary document.

---

---

## 9. Web Presence Architecture (CANONICAL — 2026-03-23)

### The Two-Layer Web Strategy

NeuronX serves two distinct web contexts. Each has a different builder, owner, and purpose.

---

### Layer 1 — GHL Native (Inside Snapshot)

**What lives here**: All conversion/intake assets that must auto-deploy with every client snapshot install.

| Asset | Builder | Why GHL |
|-------|---------|---------|
| Intake landing page (lead capture) | GHL Funnel Builder | In snapshot → deploys in <30 min per client |
| Thank You page (post-form confirmation) | GHL Funnel Builder | Triggers WF-01 natively |
| Appointment booking page | GHL Calendar Widget | Native calendar integration |
| Surveys (RCIC outcome, post-consult) | GHL Survey Builder | Maps to GHL custom fields natively |
| All 15 workflows | GHL Workflow Builder | Core automation — snapshot only |

**Rule**: If an asset is part of the intake/conversion funnel OR triggers GHL automation, it MUST live in GHL. Non-negotiable.

---

### Layer 2 — Next.js + Tailwind + Framer Motion (Outside Snapshot)

**What lives here**: Full marketing website, SEO pages, blog. Deployed per-client via Vercel CLI.

**Tech stack** (same stack used by Vercel, Linear, Stripe):
```
next@14+ (App Router, RSC)
tailwindcss@3+
framer-motion@11+ (npm animation library — NOT Framer the builder)
shadcn/ui (component primitives)
sanity (CMS — allows client to edit content without code)
Deployed: Vercel CLI (vercel deploy --prod --token $VERCEL_TOKEN)
```

| Asset | Builder | Why Next.js |
|-------|---------|------------|
| Full marketing website (home, services, team, about) | Next.js | 10/10 design quality, 95+ Lighthouse, SEO |
| Blog / immigration guides | Next.js + Sanity CMS | SEO traffic, content marketing |
| Case studies | Next.js | Trust-building, conversion |
| NeuronX SaaS marketing site | Next.js | Product demo, pricing, B2B conversion |

**Rule**: Full marketing websites live in Next.js. Claude builds 100% of the code autonomously. Deployed to Vercel free tier. Client edits content via Sanity Studio (no code required).

---

### GHL Integration — Zero Friction Guarantee

Next.js sites integrate with GHL via two mechanisms that have been confirmed to work with zero friction:

| Integration | Method | Status |
|-------------|--------|--------|
| Lead capture form | GHL form iframe embed | ✅ Confirmed working |
| Calendar booking | GHL calendar widget iframe embed | ✅ Confirmed working |
| Chat widget | GHL JS snippet in `<head>` | ✅ Confirmed working |
| Form → WF-01 trigger | Native (form submission triggers GHL workflow) | ✅ Confirmed working |
| Tracking pixels | Script tags in Next.js `layout.tsx` | ✅ Confirmed working |

**What does NOT transfer to Next.js** (must stay in GHL):
- GHL native funnel conversion analytics
- GHL A/B testing
- GHL payments and memberships
- Snapshot deployment

---

### White-Label Template Business Model

This architecture enables a premium upsell tier for NeuronX clients:

```
NeuronX Core ($500–1,500 CAD/mo):
  → GHL snapshot (all 15 workflows, pipeline, calendar, forms)
  → AI intake VAPI calling
  → Full CRM automation

NeuronX Premium Website Add-On (+$300–500 CAD/mo):
  → Full Next.js marketing website (6-8 pages)
  → VMC template customized: logo, colors, team, RCIC#, GHL form ID, calendar URL
  → Claude deploys autonomously per client (~10 min via Vercel CLI)
  → Sanity CMS so client edits content independently
  → SEO optimized, mobile-perfect, 95+ Lighthouse
```

**Deployment automation** (Claude runs this per new client):
```bash
# 1. Copy base VMC template
# 2. Update client config (name, colors, logo, GHL form ID, calendar URL)
# 3. Deploy:
vercel deploy --prod --token $VERCEL_TOKEN --yes
vercel domains add clientdomain.com --token $VERCEL_TOKEN
# Result: Live in ~10 minutes per client. Zero UI work.
```

---

### Build Order

| Phase | Asset | When |
|-------|-------|------|
| Week 1 (now) | VMC intake funnel — GHL native (in snapshot) | Current |
| Week 2 | VMC full marketing website — Next.js (first template) | After snapshot |
| Week 3 | NeuronX marketing website — Next.js | Before outreach |
| Week 4+ | Each new client website — Next.js clone + customize | Per client onboarding |

---

## Document Authority

This document defines the boundaries that the architecture must respect.

Any architecture decision that violates these boundaries requires founder approval
and an update to this document before implementation.

---

## 6. Web Presence Architecture (Added 2026-03-23 — CANONICAL)

**Decision**: Hybrid approach — GHL native for conversion/intake, Next.js for marketing.

### Layer 1 — GHL Native (inside every snapshot — auto-deploys)
```
✅ Intake landing page (form capture → WF-01 → VAPI)
✅ Thank You page (post-form confirmation)
✅ Appointment booking page (calendar embed)
✅ All surveys (RCIC outcome, readiness)
✅ All 15 workflows
✅ Email/SMS templates
```
Rule: ANY page that captures a GHL form submission MUST be in GHL native.
Reason: Forms trigger workflows. External pages break native GHL funnel analytics and snapshot portability.

### Layer 2 — Next.js + Tailwind + Vercel (per-client deployment)
```
✅ Full marketing website (home, services, team, about, blog)
✅ SEO-optimized program pages (Express Entry, Spousal, etc.)
✅ Trust-building content (testimonials, case studies)
✅ NeuronX SaaS marketing site (neuronxai.com)
```
Rule: Full websites with blog/SEO/branding go in Next.js, deployed to Vercel.
Reason: GHL page builder cannot produce 10/10 design quality or proper SEO.

### Layer 3 — Sanity CMS (optional, premium tier)
```
✅ Client content editing without code
✅ Blog management
✅ Team/credentials updates
```

### GHL Integration on Next.js Pages
```
GHL Form → embed via iframe (✅ works, triggers workflows)
GHL Calendar → embed via iframe (✅ works, triggers WF-05)
GHL Chat Widget → embed via script tag (✅ works)
GHL Analytics → does NOT work on external pages (❌ use GA4 instead)
GHL A/B Testing → does NOT work on external pages (❌ use Vercel experiments)
```

### Per-Client Deployment Process (Claude executes autonomously)
```
1. Clone Next.js base template
2. Update client config (name, colors, logo, RCIC#, GHL form ID, calendar URL)
3. vercel deploy --prod
4. vercel domains add clientdomain.com
Total time per client: ~10 minutes, zero human effort
```

### Upsell Model
```
NeuronX Core ($500-1,500/mo): GHL snapshot only
NeuronX Premium (+$300-500/mo): Full Next.js website + Sanity CMS
```

### Figma Policy
Figma is NOT used. Claude goes directly from brief → production code.
Reason: Claude is both designer and developer — Figma is a redundant handoff layer.

### Brand Kit (Applied to ALL client-facing assets)
VMC Brand Kit is the reference implementation for all future clients:
- Primary: client's primary brand color
- Dark: #0F172A (universal dark — same across all clients)
- Background: #F9FAFB (universal light bg — same across all clients)
- Font: Inter (universal — same across all clients)
- Only primary/secondary colors change per client

