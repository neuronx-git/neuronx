# NeuronX Open Decisions Log

Version: 2.0
Status: ACTIVE
Last Updated: 2026-03-21
Rule: Decisions marked 🔴 CRITICAL must be resolved before building dependent features

---

## Unresolved Decisions

| # | Decision | Status | Priority | Owner | Dependency |
|---|----------|--------|----------|-------|------------|
| OD-01 | Voice layer selection | ✅ RESOLVED | CRITICAL | AI recommendation accepted | VAPI locked — structured data extraction, function calling, already wired to Railway |
| OD-02 | Pricing tiers and feature gating | 🟡 UNRESOLVED | PRE-PILOT | Founder | Sales/pitch deck |
| OD-02b | Commercial packaging | 🟡 UNRESOLVED | PRE-PILOT | Founder | Pricing model |
| OD-03 | Readiness scoring weights | 🟡 UNRESOLVED | WEEK 4 | Founder + domain expert | Scorer calibration |
| OD-04 | AI call script tone | 🟡 UNRESOLVED | WEEK 3 | Founder + pilot testing | Voice bake-off scripts |
| OD-05 | Snapshot deployment process | 🟡 UNRESOLVED | WEEK 2 | Technical eval | Onboarding speed |
| OD-06 | Consultation prep delivery | 🟡 UNRESOLVED | WEEK 4 | Founder + feedback | Briefing delivery |
| OD-07 | Analytics dashboard | ✅ RESOLVED | WEEK 4 | Technical eval | Metabase on Railway — confirmed 2026-04-04 |
| OD-08 | Onboarding model | 🟡 UNRESOLVED | PRE-PILOT | Founder | Scale planning |
| OD-09 | Existing codebase disposition | ✅ RECOMMENDED | RESOLVED | Technical eval | Build scope |
| OD-10 | AI transparency policy | 🟡 UNRESOLVED | WEEK 3 | Founder + legal | Call scripts |
| OD-11 | WhatsApp as v1 channel | ✅ DEFERRED | DEFERRED | — | v1.5 |
| OD-12 | Data hosting and residency | 🟡 UNRESOLVED | PRE-PILOT | Founder + legal | PIPEDA compliance |
| OD-13 | V1 tech boundary | ✅ RESOLVED | RESOLVED | Founder | Option A: GHL + thin FastAPI wrapper — confirmed by build |

---

## OD-01: Voice Layer Selection (CRITICAL — Week 3)

**Decision**: Which voice AI provider for outbound first-contact calls?

**Options**:
| Provider | Pros | Cons |
|----------|------|------|
| GHL Native Voice AI | Simplest, no external dependency, native GHL integration | Unknown structured data extraction capability, limited compliance controls |
| VAPI | Function calling (structured R1-R5 extraction), tenant isolation, proven API | External dependency, $150-225/mo |
| Bland AI | Competitive pricing, good quality | Less ecosystem support |
| Retell AI | Strong reliability | Less flexibility |

**AI Technical Recommendation**:
VAPI for structured data extraction via function calling. VAPI allows defining JSON schemas that the AI fills during the call — this means R1-R5 data is always structured, never requiring NLP post-processing.

**Evaluation Method**: Run bake-off per `docs/03_infrastructure/live_tenant_bakeoff_scorecard.md`

**Resolution Process**:
1. Week 3 Monday: Configure GHL Voice AI test agent
2. Week 3 Tuesday: Configure VAPI test agent
3. Week 3 Thursday: Founder reviews scorecards
4. Week 3 Thursday: Founder approves voice layer
5. Record resolution below

**Dependencies**: Voice integration (Phase 2), call scripts, webhook security

---

## OD-02: Pricing Tiers

**Decision**: How to structure NeuronX pricing

**AI Recommendation** (for founder consideration):

Flat pricing for v1 (one SKU, one price). Simpler to sell, simpler to deliver.

| Tier | Price | Rationale |
|------|-------|-----------|
| NeuronX Standard | $1,500 CAD/month | One firm, full product, white-glove setup |
| Pilot/Trial | Free for 30 days | First 50 leads or 30 days, whichever first |

Premium onboarding fee ($2,000-5,000 one-time) is viable given white-glove model.

**Resolution**: Founder decides pre-pilot (Week 5)

---

## OD-03: Readiness Scoring Weights

**Decision**: How to weight R1-R5 dimensions in readiness score

**Current Implementation** (neuronx-api/app/services/scoring_service.py):
- Each answered dimension: +2 points (max 10 for 5 dimensions)
- Urgency bonus: +1 for Urgent timeline
- Complexity penalty: -1 for prior refusal
- Budget penalty: -1 for budget-unaware

**Calibration Needed**: After 30 days of pilot data, adjust weights based on which dimensions best predict consult-to-retained conversion.

**Resolution**: Baseline weights approved for v1, refine in v1.5 with data

---

## OD-05: Snapshot Deployment Process

**Decision**: Manual vs automated snapshot install

**AI Assessment** (from project history):
- GHL snapshot API is unclear/limited
- Manual install tested and documented
- Manual install is acceptable for premium model (white-glove setup)

**Recommendation**: Manual install with documented playbook for v1. Build automation for v1.5 if volume demands.

**Resolution**: Test in Week 2, document process, resolve based on time measurement

---

## OD-06: Consultation Prep Delivery Method

**AI Recommendation**: Email to consultant + GHL contact note (both)
- Email: Consultant receives briefing 30 minutes before consultation in inbox
- GHL note: Permanent record, accessible from any device

**Implementation**: Already built in neuronx-api/app/services/briefing_service.py

**Resolution**: Confirm with first pilot consultant which delivery they prefer

---

## OD-07: Analytics Dashboard

**AI Recommendation**: Custom FastAPI endpoints for v1, GHL native dashboards as fallback

- Week 4: Build `/analytics/pipeline` and `/analytics/stuck` endpoints
- v1.5: Embed BI tool (Metabase or similar) if firm owners want richer views

**Resolution**: Build custom endpoints Week 4, validate with pilot customer

---

## OD-09: Existing Codebase Disposition

**RECOMMENDED RESOLUTION** (2026-03-21):

**Decision**: Option B — Reference Only

**Rationale**:
- `/APP/*` TypeScript monorepo (~90 packages) is overengineered for v1
- GHL-first approach with thin Python wrapper is faster to market
- Salvage `/APP/*` packages selectively for v1.5+ (billing, playbooks, decision engine)
- Clean start with neuronx-api/ FastAPI aligns with configure-first principle

**Status**: RECOMMENDED — Awaiting founder confirmation

---

## OD-10: AI Transparency Policy

**AI Recommendation**: Always identify as AI-assisted

Per CASL and trust boundary requirements, AI must be transparent.
Script: "Hi, I'm an AI assistant from [Firm Name]. I'm calling to help schedule your consultation."

**This also reduces legal risk** — impersonating a human in regulated context is higher liability.

**Resolution**: Include in call scripts for Week 3 bake-off

---

## OD-11: WhatsApp as v1 Channel

**DEFERRED** to v1.5.

GHL WhatsApp reliability requires verification. Not launch-critical.
Priority: Get voice AI calling working first.

---

## OD-13: V1 Tech Boundary

**RECOMMENDED RESOLUTION** (2026-03-21):

**Decision**: Option A — GHL + NeuronX Thin Orchestration Layer

**Rationale**:
- Faster to build (1-2 weeks vs 6+ weeks for full backend)
- Lower risk (fewer moving parts)
- Aligns with configure-first principle
- `/APP/*` codebase is reference-only — selective salvage in v1.5
- FastAPI thin brain (~1,800 lines) scaffold already created in `neuronx-api/`

**Implementation**:
- GHL: System of record (contacts, pipeline, workflows, SMS/email)
- VAPI: Voice AI execution (pending OD-01)
- NeuronX API (FastAPI): Webhook receiver + readiness scorer + briefing assembler + trust enforcer + analytics

**Status**: RECOMMENDED — Awaiting founder confirmation

---

## Decision Resolution Process

1. Owner investigates options
2. AI provides recommendation with rationale
3. Founder approves or modifies
4. Decision recorded in Resolved Decisions table below
5. Affected documents updated

---

## Resolved Decisions

| # | Decision | Resolution | Date | Rationale |
|---|----------|------------|------|-----------|
| OD-11 | WhatsApp v1 channel | DEFERRED to v1.5 | 2026-03-13 | Not launch-critical; verify GHL WhatsApp reliability first |
| OD-09 | Codebase disposition | Reference-only for v1. Salvage selectively for v1.5+ | 2026-03-21 (recommended) | GHL-first is faster to market; /APP/* overengineered for MVP |
| OD-01 | Voice layer selection | **VAPI** — function calling for R1-R5 extraction, serverUrl wired to Railway, structuredDataPlan configured | 2026-04-04 | GHL Voice AI lacks structured data extraction; VAPI already fully operational |
| OD-13 | V1 tech boundary | Option A: GHL + NeuronX thin wrapper (FastAPI) | 2026-03-21 (recommended) | Fastest path to first customer; configure-first principle |
| OD-07 | Analytics dashboard | Metabase on Railway, embedded in Next.js portal | 2026-04-04 | Metabase stays — intuitive for firm owners, "Powered by" fine for v1 |

---

**Version History**:
- v2.0 (2026-03-21): Added AI recommendations for all unresolved decisions. Marked OD-09 and OD-13 as recommended. Prioritized by week dependency.
- v1.0 (2026-03-13): Initial log

---

**Next Review**: After Week 3 voice bake-off (OD-01 resolution)
