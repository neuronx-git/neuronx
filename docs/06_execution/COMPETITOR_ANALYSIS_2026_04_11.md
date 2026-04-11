# NeuronX Competitive Analysis — 2026-04-11

---

## COMPETITIVE POSITIONING MATRIX

| Feature | NeuronX | VisaFlo | Visto AI | CaseEasy | Docketwise | Filevine | INSZoom |
|---------|---------|---------|----------|----------|------------|----------|---------|
| **INTAKE & SALES** | | | | | | | |
| AI Voice Calling (Outbound) | **YES** | No | No | No | No | No | No |
| 5-Min Auto-Response SLA | **YES** | No | No | No | No | No | No |
| Sales Readiness Scoring (R1-R5) | **YES** | No | No | Eligibility only | No | No | No |
| Pre-Consultation Briefing | **YES** | No | No | No | No | No | No |
| Sales Pipeline (Inquiry→Retainer) | **9 stages** | No | No | No | No | No | No |
| Multi-Channel Contact Sequences | **7-step** | No | No | No | No | No | No |
| Stuck-Lead Detection | **YES** | No | No | No | No | No | No |
| Trust Boundary Enforcement | **YES** | No | No | No | No | No | No |
| **CASE MANAGEMENT** | | | | | | | |
| Post-Retainer Case Tracking | Basic | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** |
| IRCC Form Auto-Fill | Chrome ext | **YES** | **YES** | **YES** | **YES** | **YES** | No |
| Document Management | GHL Portal | Basic | Basic | **YES** | **YES** | **YES** | **YES** |
| Client Portal | GHL | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** |
| **AI CAPABILITIES** | | | | | | | |
| AI Eligibility Assessment | No (by design) | No | **YES** | **YES** | **YES** | **YES** | No |
| AI Form Auto-Fill | Data sheets | No | **YES** | **YES** | **YES** | **YES** | No |
| AI Call Summaries | **YES** (VAPI) | No | No | No | No | No | No |
| AI Compliance Checking | **YES** | No | No | No | No | No | No |
| **ANALYTICS** | | | | | | | |
| Pipeline/Funnel Analytics | **YES** (Metabase) | Basic | Basic | Basic | Basic | **YES** | **YES** |
| IRCC Processing Time Tracking | **YES** | No | **YES** | **YES** | No | No | **YES** |
| **INFRASTRUCTURE** | | | | | | | |
| CRM (Built-in) | GHL | No | No | **YES** | No | **YES** | No |
| Billing/Invoicing | Stripe | No | No | **YES** | No | **YES** | No |
| Multi-Language | v2 | No | No | No | **14 langs** | **170 langs** | No |

---

## PRICING COMPARISON

| Product | Entry | Mid | Premium | Model | Currency |
|---------|-------|-----|---------|-------|----------|
| **NeuronX** | $299 | $599 | $1,199 | Per-firm | CAD |
| CaseEasy | $99 | $149 | $199 | Per-firm | CAD |
| VisaFlo | ~$129 | ? | ? | Per-firm | CAD |
| Visto AI | $199 | $449 | $999 | Per-firm | USD |
| Docketwise | $69/user | $99/user | $119/user | Per-user | USD |
| Filevine | ~$39-65/user | ~$79/user | Custom | Per-user | USD |
| INSZoom | $50/user | $100/user | $180/user | Per-user | USD |

**5-person firm comparison**: NeuronX $299 vs CaseEasy $99 vs Docketwise $495 vs INSZoom $500

---

## FEATURES COMPETITORS HAVE THAT WE DON'T

| Feature | Who Has It | Priority for NeuronX |
|---------|-----------|---------------------|
| IRCC form auto-fill (in-browser) | Visto, CaseEasy, Docketwise, Filevine, VisaFlo | **P1** — Chrome ext exists, needs polish |
| AI eligibility scoring | CaseEasy, Visto, Docketwise, Filevine | **NOT DOING** — trust boundary (we score sales readiness, not eligibility) |
| Dedicated client portal (branded) | CaseEasy, Visto, Docketwise, Filevine, INSZoom | **P2** — Next.js portal planned |
| Document management (upload/organize) | CaseEasy, Docketwise, Filevine, INSZoom | **P2** — GHL Portal for v1 |
| Billing/invoicing | CaseEasy, Filevine | **P3** — Stripe direct for v1 |
| Multi-language questionnaires | Docketwise (14), Filevine (170) | **P3** — v2 consideration |
| IRCC form change monitoring | Visto | **P2** — Could build with canada.ca scraper |
| Case timeline/Gantt view | CaseEasy, Filevine | **P3** — Time-in-stage analytics cover this |
| CRS score calculator | Visto, CaseEasy | **NOT DOING** — eligibility tool, not sales tool |

---

## NEURONX DIFFERENTIATORS (Features We Have That Nobody Else Does)

1. **AI Voice Calling** — 0/6 competitors have automated outbound voice calls
2. **5-Minute Response SLA** — Only NeuronX auto-contacts prospects within minutes
3. **Sales Readiness Scoring** — R1-R5 dimensions are unique (competitors score eligibility, we score buyability)
4. **Pre-Consultation Briefings** — Auto-generated RCIC prep docs are unique
5. **Full Sales Funnel Automation** — 9-stage pipeline with 24 automated workflows
6. **Stuck-Lead Detection** — No competitor identifies neglected pipeline leads
7. **AI Trust Boundary Enforcement** — Documented compliance controls for AI interactions
8. **Config-Driven Architecture** — Edit YAML, push, auto-deploy in 90 seconds

---

## STRATEGIC POSITIONING

> **"NeuronX gets you clients. CaseEasy/Visto/VisaFlo help you serve them."**

NeuronX owns the **pre-retention funnel** that every competitor ignores. All competitors focus on post-retainer case management. NeuronX and case management tools are **complementary**, not competing.

**Biggest Risk**: CaseEasy adding sales automation features (500+ firms in Canada, $99/mo entry)
**Biggest Opportunity**: IRCC form auto-fill Chrome extension (matches competitor feature, saves RCIC 2-3 hours/case)
**Price Justification**: NeuronX drives revenue (new retainers). Case management is a cost center. One additional retained client ($3K-$5K) pays for 6+ months of NeuronX.
