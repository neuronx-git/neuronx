# NeuronX Product Vision

Version: 3.0
Status: CANONICAL
Last Updated: 2026-03-13
Authority: Founder

---

## 1. What NeuronX Is

NeuronX is an AI-assisted sales and intake operating system for immigration
consulting firms. It sits as an orchestration and intelligence layer on top of
GoHighLevel, which serves as the mandatory CRM and automation infrastructure.

NeuronX manages the pre-retention pipeline: the sequence of events from the
moment a prospect inquires about immigration services to the moment they sign
a retainer agreement and become a paying client.

NeuronX is not a CRM. It is not a case management system. It is not a voice
provider. It is the operational brain that ensures every inquiry is responded to
quickly, every prospect is assessed consistently, every consultation is
prepared with context, and every follow-up happens on time.

**Canon Decision**: NeuronX is a vertical product for immigration consulting.
It is not a horizontal agency tool. It is not a generic GHL wrapper.

---

## 2. Who NeuronX Serves

### Primary Users

| User | Role | Core Need |
|---|---|---|
| Firm Owner / Principal RCIC | Strategy, high-value consultations, business health | Pipeline visibility, conversion metrics, ROI on marketing spend |
| Intake Coordinator | Responds to inquiries, qualifies, books consultations | Speed, consistency, clear work queue, scripts |
| Consultant / RCIC / Lawyer | Delivers consultations, converts to retainer | Preparation, context, qualified prospects only |

### Secondary Users

| User | Role | Core Need |
|---|---|---|
| Prospective Client | Seeking immigration help | Fast response, clarity, professionalism, trust |

**Canon Decision**: Primary market is Canada. Primary customers are RCIC firms,
immigration law firms, and boutique immigration consultancies with 2-15 staff.

---

## 3. The Problem

Immigration consulting is a high-ticket, trust-dependent, consultation-based
business. Average engagement values range from $1,000 to $5,000+ CAD. Firms
spend significant budgets on lead generation.

The operational reality for most firms:

- Inquiries wait hours or days for a first response
- Readiness assessment is inconsistent -- depends on who answers and when
- Follow-up after initial contact is manual and unreliable
- Consultants enter meetings with little or no preparation
- Firm owners lack visibility into pipeline health and conversion rates
- No-shows, cold leads, and undecided outcomes have no recovery process

The result: firms lose a substantial share of potential revenue to operational
inefficiency in the pre-retention funnel.

**Canon Decision**: NeuronX solves the inquiry-to-retainer lifecycle.
Post-retention case management, document preparation, and government application
filing are explicitly out of scope.

---

## 4. The Solution

NeuronX provides:

1. **Speed-to-Lead Response** -- AI-assisted outbound contact within minutes of
   an inquiry, via the firm's chosen voice AI provider
2. **Structured Readiness Assessment** -- Consistent assessment logic with
   immigration-relevant dimensions, executed by AI with human escalation
3. **Appointment Orchestration** -- Automated booking, reminders, no-show
   recovery, and rescheduling
4. **Consultation Preparation** -- AI-assembled briefings delivered to the
   consultant before every meeting
5. **Follow-Up Automation** -- Persistent, multi-channel sequences for every
   stage of the pipeline
6. **Pipeline Intelligence** -- Conversion funnel analytics, operator metrics,
   lead source attribution, and stuck-lead detection
7. **Regulatory Guardrails** -- Hard boundaries ensuring AI never provides
   immigration advice, assesses legal eligibility, or replaces licensed judgment

**Canon Decision**: GoHighLevel is the mandatory infrastructure. NeuronX builds
only what GHL cannot handle natively: AI calling orchestration, readiness
intelligence, consultation preparation, AI context memory, advanced analytics,
and immigration-specific domain logic.

---

## 5. Product Principles

1. **Configure-first, code-last.** Use GoHighLevel natively wherever possible.
   Only build wrapper logic where GHL is insufficient.
2. **Every feature must map to revenue impact or cost reduction.** No vanity
   features. No technical indulgence.
3. **AI augments humans. AI does not replace licensed judgment.** AI handles
   speed, consistency, and preparation. Humans handle advice, assessment,
   and complex decisions.
4. **Immigration-specific, not generic.** Pipeline stages, readiness criteria,
   scripts, and metrics are designed for immigration consulting. Generic
   patterns are rejected.
5. **Premium experience for the prospect.** The person seeking immigration help
   is anxious and spending significant money on their family's future. Every
   touchpoint must be fast, clear, professional, and respectful.
6. **Measurability over intuition.** Firm owners must be able to see exactly
   where the pipeline leaks, which operators perform, and which lead sources
   convert.
7. **Regulatory discipline is non-negotiable.** Trust boundaries are hard
   constraints, not suggestions.

**Canon Decision**: These principles govern all product decisions.
A feature that violates a principle is rejected regardless of demand.

---

## 6. What NeuronX Is NOT

- NOT a CRM (GoHighLevel is the CRM)
- NOT a case management system (Docketwise, INSZoom, etc. serve that need)
- NOT a voice provider (NeuronX orchestrates calls via third-party providers)
- NOT an immigration knowledge base or eligibility assessor
- NOT a document management system
- NOT a multi-vertical platform in v1 (immigration only)
- NOT a multi-CRM platform in v1 (GoHighLevel only)
- NOT a self-serve, zero-touch product (premium onboarding is expected)

---

## 7. Business Model

Premium vertical SaaS subscription.

| Aspect | Decision |
|---|---|
| Pricing model | Monthly subscription, per-firm (not per-seat) |
| Target range | $500-$1,500 CAD per month |
| Pricing anchor | Value created: one additional retained client pays for months of subscription |
| Billing infrastructure | GoHighLevel SaaS Mode + Stripe |

**Assumption**: v1 is delivered as a premium implementation package, not a self-serve tool.
This may include a one-time onboarding and configuration service in addition to the monthly subscription.

**Assumption**: Pricing tiers and exact feature gating are open decisions
to be finalized based on early customer feedback.

---

## 8. Timeline Boundaries

| Milestone | Scope |
|---|---|
| v1 (Launch) | Core pipeline: speed-to-lead, readiness assessment, booking, consultation prep, follow-up, basic analytics. Canada only. |
| v1.5 (Post-launch iteration) | Refined analytics, operator scorecards, improved AI scripts, customer feedback integration |
| v2 (Expansion) | Advanced AI memory, multi-language support, potential expansion to adjacent verticals (legal, financial advisory) |

**Open Decision**: Exact launch date is not specified in canon. Timelines are
set by the build plan, not the vision document.

---

## 9. Success Definition

### North Star Metric
**Consultation-to-Retained Conversion Rate** for firms using NeuronX.

### Supporting Metrics
- Speed-to-first-contact (target: < 5 minutes for AI-handled inquiries)
- Lead-to-booked conversion rate
- Consultation show rate
- Pipeline stage velocity (average days per stage)
- Firm owner time-in-system per day (target: < 15 minutes for oversight)

---

## 10. Canon Governance

This document is the governing product vision for NeuronX.

- Changes require founder approval
- Version history is maintained
- All product decisions must be traceable to this canon or the PRD
- Contradictions between this document and other artifacts: this document wins
