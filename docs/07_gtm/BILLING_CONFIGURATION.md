# NeuronX — Billing Configuration Guide

**Version**: v1.0
**Date**: 2026-03-26
**Status**: CANONICAL — All agents must reference this for billing decisions
**Depends on**: PRICING_STRATEGY.md

---

## Platform Decision

| Component | Tool | Why |
|-----------|------|-----|
| **Subscription billing** | Stripe Billing | Industry leader, full self-service, AI dunning, 0.7% fee |
| **Payment collection** | Stripe Payment Links (no-code) | Zero development, instant setup |
| **Customer self-service** | Stripe Customer Portal (hosted) | Clients manage their own cards, upgrades, invoices |
| **Invoicing** | Stripe Invoicing (auto) | Auto-generated per billing cycle |
| **Failed payment recovery** | Stripe Smart Retries + Dunning emails | Recovers 56% of failed payments automatically |
| **CRM + provisioning** | GHL ($297 plan) + manual snapshot loading | 5 min/client, high-touch onboarding |

**NOT using**: GHL SaaS Mode (requires $497 plan). Will migrate to GHL SaaS Mode at client #8-10 if needed.

---

## Stripe Products to Create

### Product 1: NeuronX Essentials
```
Name: NeuronX Essentials
Description: Branded intake form, inquiry pipeline, lead dashboard, CRM,
             online booking, Google Calendar sync. For solo RCICs.
Price: $299 CAD / month (recurring)
Tax behavior: Exclusive (add tax on top)
Currency: CAD
Trial: 14-day free trial
```

### Product 2: NeuronX Professional
```
Name: NeuronX Professional
Description: Everything in Essentials + AI voice calls (50/mo), automated
             email + SMS sequences, missed call text-back, no-show rebooking,
             smart scheduling, Google Meet auto-link, reminder sequences.
             Includes dedicated onboarding call. For solo/duo firms.
Price: $599 CAD / month (recurring)
Tax behavior: Exclusive
Currency: CAD
Trial: 14-day free trial
Metadata: recommended=true
```

### Product 3: NeuronX Scale
```
Name: NeuronX Scale
Description: Everything in Professional + unlimited AI voice calls, AI briefings,
             stuck-lead detection, analytics reports, custom call scripts,
             multi-consultant support (up to 5), round-robin scheduling,
             lead assignment rules, team dashboard, priority support,
             quarterly strategy reviews. For established firms.
Price: $1,199 CAD / month (recurring)
Tax behavior: Exclusive
Currency: CAD
Trial: 14-day free trial
```

### Annual Pricing (Create After Month 3)
```
Essentials Annual: $2,990 CAD / year (save $598 = 2 months free)
Professional Annual: $5,990 CAD / year (save $1,198 = 2 months free)
Scale Annual: $11,990 CAD / year (save $2,398 = 2 months free)
```

---

## Stripe Setup Checklist (Week 4-5)

### Day 1: Account Setup
- [ ] Create Stripe account at stripe.com with ranjan@neuronx.co
- [ ] Complete business verification (government ID + Canadian bank account)
- [ ] Set business name: "NeuronX"
- [ ] Set statement descriptor: "NEURONX" (what appears on client credit card statements)
- [ ] Enable CAD as primary currency
- [ ] Connect Canadian bank account for payouts

### Day 2: Products & Prices
- [ ] Create Product: NeuronX Essentials ($299 CAD/mo)
- [ ] Create Product: NeuronX Professional ($599 CAD/mo)
- [ ] Create Product: NeuronX Scale ($1,199 CAD/mo)
- [ ] Enable 14-day free trial on all products
- [ ] Set billing cycle anchor to 1st of month (pro-rated first month)

### Day 3: Payment Links
- [ ] Generate Payment Link for Essentials
- [ ] Generate Payment Link for Professional
- [ ] Generate Payment Link for Scale
- [ ] Test each link with Stripe test mode
- [ ] Customize confirmation page (redirect to neuronx.co/welcome)

### Day 4: Customer Portal
- [ ] Enable Customer Portal in Stripe Dashboard → Settings → Billing → Customer Portal
- [ ] Configure allowed actions:
  - ✅ Update payment method
  - ✅ View invoices and receipts
  - ✅ Upgrade/downgrade subscription
  - ✅ Cancel subscription (with reason collection)
  - ✅ Update billing address
  - ❌ Pause subscription (not supported yet)
- [ ] Configure cancellation flow:
  - Collect cancellation reason (dropdown)
  - Offer retention coupon: 20% off for 3 months
  - Require cancellation confirmation
- [ ] Brand the portal:
  - Upload NeuronX logo
  - Set brand color (#2563EB or NeuronX primary)
  - Add business name and support email

### Day 5: Dunning & Recovery
- [ ] Enable Smart Retries (AI-powered retry scheduling)
- [ ] Set retry window: 1 month (4 retry attempts)
- [ ] Enable failed payment emails to customers
- [ ] Configure dunning email schedule:
  - Day 1: "Payment failed — please update your card"
  - Day 3: "Reminder: Your payment is still outstanding"
  - Day 7: "Final notice: Update payment to keep your NeuronX access"
- [ ] Set subscription cancellation after: 30 days of failed payment
- [ ] Enable "Send upcoming renewal reminders" (3 days before)

### Day 6: Tax Configuration
- [ ] Enable Stripe Tax (automatic Canadian tax calculation)
- [ ] Register for GST/HST collection (if applicable)
- [ ] Set tax reporting to Canadian format

---

## Client Onboarding Flow (Manual — $297 GHL Plan)

```
1. DEMO COMPLETED → Client says "I'm in"
   │
2. SEND PAYMENT LINK (via email)
   │  → Include: tier-specific Stripe Payment Link
   │  → Professional tier link is default recommendation
   │
3. CLIENT PAYS → Stripe processes payment
   │  → Stripe sends receipt automatically
   │  → You get notified (Stripe email + webhook)
   │
4. YOU PROVISION (within 24 hours)
   │  → GHL: Create new sub-account from snapshot (5 min)
   │  → GHL: Configure client branding (firm name, logo, colors)
   │  → GHL: Set up client calendar (availability, timezone)
   │  → GHL: Update form with client's firm details
   │  → VAPI: Create client-specific voice agent (or clone template)
   │  → Send welcome email with login credentials
   │
5. ONBOARDING CALL (within 48 hours)
   │  → 60-min Zoom/Meet call
   │  → Walk through dashboard, pipeline, calendar
   │  → Test intake form together
   │  → Set up Google Calendar sync
   │  → Answer questions
   │
6. GO LIVE
   │  → Enable form on client's website
   │  → First inquiry flows through NeuronX
   │  → Monitor for 7 days, adjust as needed
   │
7. ONGOING
   → Monthly check-in (Scale tier: quarterly strategy review)
   → Stripe handles renewals, invoicing, dunning automatically
   → Client self-manages billing via Stripe Customer Portal
```

---

## What Stripe Handles Automatically (Zero Work After Setup)

| Task | Stripe Feature | Your Effort |
|------|---------------|-------------|
| Monthly billing | Auto-charge on billing date | Zero |
| Invoice generation | Auto-generated per cycle | Zero |
| Receipt emails | Auto-sent after payment | Zero |
| Failed payment retries | Smart Retries (AI) | Zero |
| Failed payment emails | Dunning emails | Zero |
| Card expiration reminders | Auto-sent before expiry | Zero |
| Subscription upgrades | Customer Portal self-service | Zero |
| Subscription downgrades | Customer Portal self-service | Zero |
| Payment method updates | Customer Portal self-service | Zero |
| Tax calculation | Stripe Tax (if enabled) | Zero |
| Cancellation + reason | Customer Portal with retention coupon | Zero |
| Revenue reporting | Stripe Dashboard | Zero |
| Payout to your bank | Auto-deposited (2 business days) | Zero |

**Total ongoing billing work: ~0 hours/month.** Stripe runs everything.

---

## Key Metrics to Track (Stripe Dashboard)

| Metric | Where | Target |
|--------|-------|--------|
| MRR (Monthly Recurring Revenue) | Stripe Dashboard → Overview | Growing month-over-month |
| Churn rate | Stripe Dashboard → Subscriptions | <5% monthly |
| Failed payment recovery | Stripe Dashboard → Revenue Recovery | >50% |
| Average revenue per customer | MRR ÷ active subscriptions | Trending toward $599+ |
| Trial-to-paid conversion | Trial subscriptions → Active | >60% |

---

## Migration to GHL SaaS Mode (Future — Client #8-10)

When manual provisioning becomes painful (est. 8-10 clients):

1. Upgrade GHL plan from $297 → $497/mo
2. Configure SaaS Configurator with same 3 tiers
3. Connect Stripe to GHL SaaS Mode
4. Enable auto-provisioning from client snapshot
5. Migrate existing Stripe subscriptions to GHL billing OR keep Stripe direct
6. Enable rebilling with markup on SMS/email/AI usage

**Decision point**: At this stage, evaluate whether GHL SaaS Mode adds enough value vs keeping Stripe direct. Many agencies prefer Stripe direct for control and portability.

---

## Pricing Rules (All Agents Must Follow)

### Rule P1: No Discounting Below Floor
- Essentials: Never below $249/mo
- Professional: Never below $499/mo
- Scale: Never below $999/mo
- Exception: Pilot pricing for first 3 clients (founder approval required)

### Rule P2: Pilot Client Pricing
- First 3 clients may receive "Founding Member" pricing:
  - Professional at $399/mo for 6 months (then auto-increases to $599)
  - Must be documented in Stripe as coupon, not price change
  - Coupon code: FOUNDING-MEMBER-2026

### Rule P3: No Custom Plans
- Sell only the 3 defined tiers
- If client needs something custom → Scale tier + custom workflow modification
- Do NOT create one-off pricing for individual clients

### Rule P4: Price Increases
- Minimum 60 days notice for existing clients
- Grandfather existing clients for 6 months after any increase
- New clients get new pricing immediately

### Rule P5: Annual Billing
- Offer annual only after Month 3 (need monthly churn data first)
- Annual = 2 months free (16.7% discount)
- Annual payments are non-refundable after 30 days

---

## Sources
- [Stripe Billing](https://stripe.com/billing) — Subscription management
- [Stripe Customer Portal](https://docs.stripe.com/customer-management) — Self-service billing
- [Stripe Smart Retries](https://stripe.com/blog/billing-customer-portal) — AI-powered dunning
- [Stripe Payment Links](https://stripe.com/payments/payment-links) — No-code payment collection
- [Stripe Invoicing](https://stripe.com/invoicing) — Automated invoicing
