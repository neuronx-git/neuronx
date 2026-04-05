# NeuronX Productization Roadmap

## Mission
Take NeuronX from validated lab system to market-ready vertical SaaS product for Canadian immigration consultants.

---

## Phase 1: Pre-Launch Hardening (Week 1-2)

### Objectives
- Polish Gold v1.0 snapshot to "wow" standard.
- Create all sales enablement materials.
- Validate pricing and packaging.

### Tasks
1. **Execute High-ROI Improvements** (`HIGH_ROI_IMPLEMENTATION_REPORT.md`).
   - Add testimonials (placeholders → real after first 3 customers).
   - Add team section.
   - Add success stats.
   - Change CTA copy.
2. **Founder Obtains**:
   - CICC badge file.
   - 3 real testimonials from beta testers (if available).
   - Professional headshot for "Team" section.
3. **Create Sales Materials**:
   - 1-page overview PDF.
   - ROI calculator (Google Sheet).
   - Demo script (Loom video).
4. **Finalize Pricing**:
   - Validate $497 / $797 / Custom tiers with 3 target customers.
5. **Create Onboarding Playbook** (from `WORLD_CLASS_GAP_MASTERPLAN.md`).

**Deliverables**:
- Polished Gold v1.0 snapshot.
- Sales deck.
- Demo video.
- Onboarding playbook v1.0.

---

## Phase 2: SaaS Site Launch (Week 3-4)

### Objectives
- Launch consultant-facing marketing site.
- Enable inbound lead capture.

### Tasks
1. **Build SaaS Site** (`NEURONX_SAAS_SITE_BLUEPRINT.md`).
   - Platform: Webflow or GHL Sites.
   - Domain: `neuronx.ai`.
2. **Set Up Demo Environment**:
   - Create "Demo" GHL sub-account with sample data.
   - Record 10-min Loom walkthrough.
3. **Enable Payments**:
   - Stripe integration for Starter tier ($497/mo).
   - Manual invoicing for Enterprise (for now).
4. **Launch**:
   - Soft launch to warm network (email list, LinkedIn).
   - No paid ads yet.

**Deliverables**:
- Live SaaS site.
- Demo environment.
- Payment flow.

---

## Phase 3: First 10 Customers (Month 2-3)

### Objectives
- Acquire 10 paying customers.
- Validate product-market fit.
- Refine onboarding.

### Go-to-Market Strategy
1. **Warm Outreach**:
   - Founder's network (RCICs, immigration lawyers).
   - LinkedIn direct outreach (personalized, not spammy).
   - Immigration consultant Facebook groups.
2. **Content Marketing**:
   - Write 3 blog posts: "How to 10X Your Immigration Firm's Response Time", "The #1 Reason Immigration Leads Don't Convert", "Why GHL is Perfect for Immigration Firms".
   - Post in CICC forums (if allowed).
3. **Referral Program**:
   - "Refer a firm, get 1 month free."

### Success Metrics
- 10 paid customers.
- < 20% churn in first 90 days.
- Average NPS > 40.

### Feedback Loop
- Monthly customer call (first 10 only).
- Collect: What's working? What's confusing? What's missing?
- Update onboarding playbook based on feedback.

**Deliverables**:
- 10 customers live.
- Onboarding playbook v2.0 (refined).
- Case study from Customer #1.

---

## Phase 4: Snapshot Iteration (Month 4)

### Objectives
- Create Gold v1.1 snapshot based on customer feedback.
- Fix any GHL-native gaps discovered.

### Tasks
1. **Review Customer Feedback**:
   - Identify top 5 pain points.
   - Identify top 5 feature requests.
2. **Prioritize GHL-Native Fixes**:
   - Only implement if no custom code required.
   - Examples: New workflow triggers, additional SMS templates, calendar tweaks.
3. **Update Gold Snapshot**:
   - Apply fixes to Gold tenant.
   - Create `NeuronX Gold v1.1 — 2026-04-XX` snapshot.
4. **Push Update to Existing Customers**:
   - Manual process for v1 (acceptable for 10 customers).

**Deliverables**:
- Gold v1.1 snapshot.
- Updated documentation.

---

## Phase 5: NeuronX Thin Brain (Month 5-6)

### Objectives
- Build lightweight orchestration layer ONLY IF GHL gaps are proven.

### Decision Criteria
Build NeuronX wrapper layer ONLY if:
1. Customers explicitly request features GHL cannot do natively.
2. Revenue justifies engineering investment ($10K+ MRR minimum).
3. No GHL native workaround exists.

### Candidate Features (Post-PMF Only)
1. **AI Voice Integration** (OD-01): Orchestrate Vapi/Bland/Retell.
2. **Readiness Scoring Engine**: Calculate R1-R6 scores from AI call transcripts.
3. **Consultation Briefing Assembly**: Pull GHL data + format + email to consultant.
4. **Advanced Analytics**: Funnel metrics beyond GHL native dashboards.

### Architecture (If Built)
- Webhook receiver (GHL events).
- Webhook sender (push to GHL).
- Stateless where possible.
- Small persistent store (analytics cache, transcripts, audit log).
- Deploy on Railway/Render/Fly.io.

**Deliverables** (Only if justified):
- NeuronX orchestration service v0.1.
- Webhook integration doc.

---

## Phase 6: Scale to 50 Customers (Month 7-12)

### Objectives
- Grow to 50 customers.
- Automate onboarding where possible.
- Hire first support/onboarding specialist.

### Marketing
- Paid ads (Google, Facebook, LinkedIn).
- Content SEO ("immigration CRM", "RCIC software").
- Partnerships with CICC, immigration lawyer associations.

### Operations
- Hire part-time onboarding specialist.
- SOP for snapshot installation.
- Build Slack community for customers.

**Deliverables**:
- 50 customers.
- Onboarding specialist hired.
- Slack community active.

---

## Success Metrics (12-Month Horizon)

| Metric | Target |
| :--- | :--- |
| **Customers** | 50 |
| **MRR** | $30K USD |
| **Churn** | < 10% monthly |
| **NPS** | > 50 |
| **Time to Value** | < 48 hours (from signup to first lead) |
| **Support Tickets per Customer** | < 2/month |

---

## What NOT to Build (v1)

Per `WORLD_CLASS_GAP_MASTERPLAN.md`:
1. AI Voice Layer (until OD-01 resolved + demand proven).
2. Multi-language support.
3. Mobile app.
4. White-label SaaS dashboard.
5. A/B testing framework.
6. Case management integration.
7. Multi-vertical expansion.
8. Enterprise features (50+ staff).
9. Self-serve signup (premium onboarding required for v1).
10. Custom code unless GHL gap is proven critical.

---

## Founder Time Allocation (First 6 Months)

| Activity | % Time |
| :--- | :--- |
| **Sales / Demos** | 40% |
| **Customer Success** | 30% |
| **Product** (roadmap, feedback) | 20% |
| **Operations** (onboarding, docs) | 10% |

**Key Decision**: Do NOT write code in Months 1-3. Focus on sales + customer success. Only after PMF should engineering begin.

---

## Risk Mitigation

| Risk | Mitigation |
| :--- | :--- |
| **GHL changes pricing/features** | Diversify: plan multi-CRM support for v2. |
| **Competitors emerge** | Speed to market. Vertical focus. Superior onboarding. |
| **Customers churn early** | Onboarding excellence. Monthly check-ins. Fast support. |
| **Founder burnout** | Hire onboarding specialist by Month 4. |
| **Regulatory changes** | Trust boundaries enforce compliance by design. |

---

## Final Verdict

**NeuronX is ready for market with 62/100 product readiness.**

The system works. The automation is solid. The snapshot is repeatable.

What's missing is **packaging, positioning, and customer onboarding**—all solvable with founder effort, not engineering.

**Next Action**: Execute Phase 1 (Pre-Launch Hardening) immediately.
