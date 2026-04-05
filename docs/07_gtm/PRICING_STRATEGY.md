# NeuronX — Pricing Strategy

**Version**: v1.0
**Date**: 2026-03-26
**Status**: APPROVED (Pending Founder Final Sign-Off)
**Decision**: OD-02 RESOLVED — 3-tier pricing

---

## Pricing Tiers

| Tier | Price (CAD/mo) | Target | Expected Mix |
|------|---------------|--------|-------------|
| **Essentials** | $299 | Solo RCIC, starting out | 20% of clients |
| **Professional** | $599 | Solo/duo firm, ready to automate | 70% of clients |
| **Scale** | $1,199 | 3-5 consultant firms | 10% of clients |

## Feature Matrix

### Essentials ($299/mo)
**Intake & Pipeline:**
- Branded intake form (web)
- 9-stage inquiry pipeline
- Lead dashboard + contact CRM
- Manual follow-up reminders

**Booking:**
- Online calendar booking
- Confirmation emails
- Google Calendar 2-way sync

**Support:** Email support + setup guide
**Includes:** 0 SMS, 1,000 emails/mo, 1 consultant

### Professional ($599/mo) — MOST POPULAR
Everything in Essentials, plus:

**AI Voice & Automation:**
- AI voice calls to new inquiries (up to 50/mo)
- Automated email + SMS follow-up sequences
- Missed call text-back
- No-show rebooking automation

**Booking+:**
- Smart scheduling with buffer times
- Google Meet auto-link
- Reminder sequence (email + SMS, 24h + 1h)

**Support:** Dedicated onboarding call (60 min) + chat support (24h SLA)
**Includes:** 250 SMS/mo, 3,000 emails/mo, 1-2 consultants

### Scale ($1,199/mo)
Everything in Professional, plus:

**AI & Intelligence:**
- AI voice calls — UNLIMITED
- AI-generated pre-consultation briefings
- Stuck-lead detection + auto-re-engagement
- Monthly conversion analytics report
- Custom AI call scripts

**Multi-Consultant:**
- Up to 5 RCICs with individual calendars + round-robin
- Lead assignment rules
- Team performance dashboard
- Per-consultant pipeline view

**Premium Support:** Priority (4hr response) + quarterly strategy review + custom workflow modifications + dedicated account manager
**Includes:** 1,000 SMS/mo, 5,000 emails/mo, up to 5 consultants

---

## Pricing Rationale

### Competitive Positioning
- NeuronX is NOT competing with case management tools (CaseEasy $99-199, Docketwise $79-129)
- NeuronX competes in the intake/sales automation category
- Comparable: Lawmatics $300-500, Smith.ai $210-600, HubSpot $800-1,200
- NeuronX pricing sits in the middle of this range

### Affordability Test
| Tier | Target Revenue | % of Revenue | Industry Benchmark |
|------|---------------|-------------|-------------------|
| $299 Essentials | $10,500-17,500/mo | 1.7-2.8% | ✅ Below 3% = easy sell |
| $599 Professional | $17,500-52,500/mo | 1.1-3.4% | ✅ Within 1-3% sweet spot |
| $1,199 Scale | $52,500-105,000/mo | 1.1-2.3% | ✅ Well within comfort zone |

### Psychology
- 3 tiers proven to convert 27-40% better than single tier (ConversionXL, ProfitWell)
- Middle tier ($599) is the target — anchored by $299 below and $1,199 above
- $299 entry prevents sticker shock; $1,199 makes $599 feel like great value
- Professional tier has disproportionate value (AI calling alone worth $500+/mo)

### ROI Story
Without NeuronX: ~15 consultations/month from 100 inquiries (40% response rate, delayed follow-up)
With NeuronX: ~35 consultations/month from 100 inquiries (100% contact rate within 5 minutes)
Extra revenue: ~$48,000/month from additional retainers
NeuronX cost: $599/month = 80x ROI

---

## Revenue Projections

| Milestone | Clients | Weighted MRR | ARR | Timeline |
|-----------|---------|-------------|-----|----------|
| First client | 1 | $599 | $7K | Week 6 |
| Breakeven | 1 | $599 | $7K | Week 6 |
| 5 clients | 5 | $2,995 | $36K | Month 3 |
| 10 clients | 10 | $5,990 | $72K | Month 6 |
| 25 clients | 25 | $14,975 | $180K | Month 9 |
| 50 clients | 50 | $29,950 | $359K | Month 12 |
| 100 clients | 100 | $59,900 | $719K | Month 16 |
| $1M ARR | ~140 | $83,860 | $1M | Month 20 |

Note: Assumes 70% Professional ($599), 20% Essentials ($299), 10% Scale ($1,199) = $599 weighted avg.

---

## Implementation (GHL $297 Plan)

Since we're on the GHL $297 plan (no SaaS Mode), billing is handled via Stripe directly:

1. Create 3 Products in Stripe Dashboard (Essentials, Professional, Scale)
2. Create recurring Prices in CAD
3. Generate Payment Links for each tier
4. Embed on neuronx.co pricing page
5. Manual sub-account provisioning via snapshot (5 min/client)
6. Upgrade to GHL $497 at client #8-10 for automated provisioning

---

## Future Pricing Evolution

### Phase 1 (Month 1-6): Launch Pricing
- 3 tiers as defined above
- Focus on selling Professional tier
- Collect usage data and client feedback

### Phase 2 (Month 7-12): Optimization
- Adjust tier boundaries based on actual usage
- Consider annual pricing (2 months free)
- Consider per-lead or per-call usage pricing
- Add-on marketplace (custom integrations, additional consultants)

### Phase 3 (Month 13-18): Expansion
- Enterprise tier ($2,497+) for firms with 10+ consultants
- Partner/white-label tier for immigration agencies managing multiple brands
- Volume discounts for multi-location firms

---

## Sources
- CaseEasy Pricing: https://caseeasy.ca/Home/Pricing
- Docketwise Pricing: https://www.docketwise.com/pricing/
- SaaS Pricing Research: https://www.saastock.com/blog/the-saas-pricing-trap-when-too-many-tiers-kill-conversions/
- Vertical SaaS Pricing: https://www.getmonetizely.com/articles/vertical-specific-saas-pricing-why-industry-context-matters
- RCIC Income Data: https://www.glassdoor.ca/Salaries/immigration-consultant-salary-SRCH_KO0,22.htm
- Immigration Fees: https://cipcanada.com/price-guide-how-much-do-immigration-consultants-charge-in-canada/
