# GoHighLevel Capability Map for NeuronX

Version: 1.0
Status: CANONICAL
Last Updated: 2026-03-13

---

## Classification

Each capability is classified into one of four tiers:
- **GHL Native**: Configure in GoHighLevel, do not build
- **NeuronX Orchestration**: Wrapper/orchestration logic on top of GHL
- **Domain Logic**: Immigration-specific product logic
- **Needs Verification**: Must be tested in live GHL tenant before build

---

## GHL Native (Configure, Don't Build)

| # | Capability | GHL Feature | API | Notes |
|---|---|---|---|---|
| 1 | Contact CRUD | Contacts | V2 API | Verified |
| 2 | Custom fields | Contact fields | V2 API | Verified |
| 3 | Tags and segmentation | Tags + Smart Lists | V2 API | Verified |
| 4 | Notes and activity log | Contact notes | V2 API | Verified |
| 5 | Pipeline creation and stages | Pipelines | V2 API | Verified |
| 6 | Opportunity CRUD and movement | Opportunities | V2 API | Verified |
| 7 | Workflow automation (40+ triggers) | Workflows | Via webhook/API | Verified |
| 8 | Calendar booking | Calendars | V2 API | Verified |
| 9 | Appointment reminders | Workflow: Appt Status | Via workflow | Verified |
| 10 | No-show detection | Workflow: Appt No-Show | Via workflow | Verified |
| 11 | SMS 2-way messaging | Conversations | V2 API | Verified |
| 12 | Email sending and sequences | Email builder | V2 API | Verified |
| 13 | Forms and surveys | Forms module | Via workflow | Verified |
| 14 | Outbound webhooks | Workflow action | Documented | Verified |
| 15 | Inbound webhooks | Workflow trigger | Documented | Verified |
| 16 | Custom webhooks (GET/POST/PUT/DELETE) | Workflow action | With auth | Verified |
| 17 | Lead assignment (round-robin) | Workflow action | Native | Verified |
| 18 | Sub-account provisioning | SaaS Configurator | API | Verified |
| 19 | Billing (Stripe) | SaaS Mode | Stripe Connect | Verified |
| 20 | White-labeling | Agency Pro | Native | Verified |
| 21 | Stale opportunity detection | Workflow trigger | Native | Verified |
| 22 | Pipeline stage change trigger | Workflow trigger | Native | Verified |

## NeuronX Orchestration (Build Wrapper Logic)

| # | Capability | Why GHL Insufficient | NeuronX Role |
|---|---|---|---|
| 23 | AI outbound calling | No native AI voice calling | Orchestrate call via voice provider, inject CRM context, write back result |
| 24 | Call outcome processing | Voice provider results need interpretation | Parse callback, map to GHL fields, move pipeline |
| 25 | Readiness scoring | GHL if/else too basic for multi-factor scoring | Configurable scoring engine with weighted criteria |
| 26 | Consultation prep assembly | Data exists but not assembled | Pull, aggregate, format, deliver briefing |
| 27 | AI context memory | No conversation state persistence | Maintain context store across interactions |
| 28 | Operator work queue | Pipeline shows leads but no prioritization | Score by urgency + value + staleness |
| 29 | Conversion funnel analytics | Basic native reporting | Stage-by-stage calculations, source attribution |
| 30 | Daily owner briefing | No aggregation capability | Generate and deliver summary |
| 31 | Stuck-lead detection (intelligent) | Basic stale trigger only | Context-aware alerting |

## Domain-Specific Logic (Immigration-Specific Build)

| # | Capability | Why Immigration-Specific |
|---|---|---|
| 32 | Immigration readiness dimensions | Program type, refusal history, document readiness |
| 33 | Consultation prep templates | Structured briefings per program type |
| 34 | AI call scripts | Tone, sensitivity, regulatory language |
| 35 | Pipeline stage definitions | Immigration sales cycle stages |
| 36 | Metric definitions | "Consult-to-retainer rate" not "close rate" |
| 37 | Regulatory guardrails | Hard rules preventing AI from crossing into regulated territory |

## Needs Live Verification

| # | Capability | Concern | Action Required |
|---|---|---|---|
| 38 | Snapshot deployment | Documented as UI-only, no API | Verify workaround options in live tenant |
| 39 | Conversation AI (built-in chatbot) | Quality and configurability unknown | Test in live tenant |
| 40 | WhatsApp integration | Real-world reliability unknown | Test deliverability, latency, limits |
| 41 | Calendar widget customization | Branding/field depth unknown | Test in live tenant |
| 42 | API rate limits under load | Documented 100/10s, 200K/day | Test with production-like patterns |
| 43 | Form builder flexibility | Custom field layout/logic unknown | Test immigration-specific forms |

---

## GHL API Reference

| Aspect | Detail |
|---|---|
| Authentication | OAuth 2.0 (public apps) or Private Integration Tokens |
| Burst limit | 100 requests / 10 seconds / app / location |
| Daily limit | 200,000 requests / day / app / location |
| Webhook rate | 100 requests / minute / company (outbound) |
| Version | V2 (V1 end-of-support) |
