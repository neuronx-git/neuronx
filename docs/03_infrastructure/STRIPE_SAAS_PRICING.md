# NeuronX — Stripe + SaaS Pricing & Billing Architecture

**Version**: v1.0
**Date**: 2026-04-18
**Status**: CANONICAL (founder decision required on final tier prices before Stripe live)
**Owner**: Founder (Ranjan Singh)
**Purpose**: Complete billing + pricing + subscription architecture for NeuronX SaaS (immigration consulting firms)

---

## TL;DR — Founder Decisions (Ship These Numbers)

| Tier        | **List Price (CAD/mo)** | Annual (save 17%)   | RCIC Seats | AI Minutes | SMS   | Positioning                  |
|-------------|-------------------------|---------------------|------------|------------|-------|------------------------------|
| **Starter** | **$497**                | $4,970/yr ($414/mo) | 2          | 300        | 1,000 | Solo RCIC / 2-person firm    |
| **Growth**  | **$997**                | $9,970/yr ($831/mo) | 5          | 1,000      | 3,500 | **MOST POPULAR** — 3–5 RCICs |
| **Scale**   | **$1,997**              | $19,970/yr ($1,664/mo) | 10     | 2,500      | 8,000 | 6–10 RCICs / multi-office    |
| **Enterprise** | **Custom (from $2,997)** | Annual only      | Unlimited  | Custom     | Custom | 10+ RCICs, white-label       |

**Setup fee**: $1,500 CAD one-time (waived on annual Growth/Scale, non-negotiable for Starter)
**Trial**: **14 days, no credit card required** for Starter only; **sales-assisted demo** required for Growth+
**Overages**: $0.25/min AI, $0.05/SMS, $15/extra seat — hard cap at 150% of plan, then throttle

### Why these numbers (not $500/$1000/$1500)

Your original $500/$1000/$1500 pricing was **too round, too cheap, and left margin on the table**. The numbers above are psychologically tuned ($997 is the universal SaaS anchor) and sit **well below** Clio ($89-$159/user × 5 users = **$445-$795/mo**) and MyCase ($89-$109/user × 5 = **$445-$545/mo**) **per-seat economics** while offering **AI voice + outbound intake** those tools don't. You price above them because you **replace** them (CRM + intake + voice + booking in one system) and their per-seat math gets ugly at 5-10 seats.

**Concrete rationale**:
- A 5-RCIC firm on Clio Essentials pays $445/mo for CRM alone. Our Growth ($997) includes CRM + AI voice + intake pipeline + 1,000 AI minutes. That's ~2x the price for ~5x the scope.
- Target firm bills $150-$300/hr × 20-30 billable hours/week/RCIC = $150K-$450K/RCIC/year. $997/mo is **<0.5% of revenue** for a 5-RCIC firm. Easy sell.
- VAPI blended cost is ~$0.25-$0.33/min all-in (not $0.09 — that figure excludes telephony + LLM). At 1,000 included minutes, our COGS is **~$250/mo on Growth**, leaving ~60% gross margin after GHL + Railway + support.

**Do not launch at $500/$1000/$1500.** Raise to the numbers above.

---

## Section 1: Pricing Strategy — Competitive Benchmarking

### 1.1 Competitive Landscape (April 2026 pricing)

| Product                | Model         | Price/Seat/mo     | 5-User Cost | 10-User Cost | AI Voice? | Immigration-Specific? |
|------------------------|---------------|-------------------|-------------|--------------|-----------|-----------------------|
| **Clio Manage EasyStart** | per-seat   | $49               | $245        | $490         | No        | No                    |
| **Clio Manage Essentials** | per-seat  | $89               | $445        | $890         | No        | No                    |
| **Clio Manage Advanced**   | per-seat  | $129              | $645        | $1,290       | No        | No                    |
| **Clio Manage Complete**   | per-seat  | $159              | $795        | $1,590       | No        | No                    |
| **MyCase Basic**          | per-seat   | $39 (annual)      | $195        | $390         | No        | No                    |
| **MyCase Pro**            | per-seat   | $89 (annual)      | $445        | $890         | No        | No                    |
| **MyCase Advanced**       | per-seat   | $109 (annual)     | $545        | $1,090       | No        | No                    |
| **INSZoom** (Mitratech)   | custom     | ~$100-$150 est.   | $500-$750   | $1,000-$1,500| No        | Yes (enterprise)      |
| **Officio**               | flat tiers | $99-$299 (est.)   | $99-$299    | $99-$299     | No        | Yes (Canadian)        |
| **RCIC Suite / Immicase** | flat tiers | $79-$199 (est.)   | $79-$199    | $79-$199     | No        | Yes (Canadian)        |
| **Case Status**           | per-firm   | ~$99+             | ~$99+       | ~$99+        | No        | Yes (comms only)      |
| **NeuronX Starter**       | flat + usage | n/a             | **$497**    | n/a          | **Yes**   | **Yes**               |
| **NeuronX Growth**        | flat + usage | n/a             | **$997**    | n/a          | **Yes**   | **Yes**               |
| **NeuronX Scale**         | flat + usage | n/a             | n/a         | **$1,997**   | **Yes**   | **Yes**               |

**Key insight**: Canadian-specific competitors (Officio, RCIC Suite, Immicase) charge flat tiers, not per-seat. Clio/MyCase dominate but are **US-centric and per-seat**, which punishes firms with paralegals. NeuronX wins on (a) AI voice intake nobody else has, (b) flat pricing with generous seat counts, (c) Canadian-first compliance (PIPEDA, RCIC workflows).

### 1.2 Pricing Philosophy

- **Flat tiers, not per-seat.** Per-seat punishes firms for adding paralegals/admins. Our seats are generous because we don't want seat count to be a friction point.
- **Usage overages, not feature gates, for the obvious stuff.** AI minutes and SMS are metered. Everything else is flat.
- **Gates that drive tier upgrades**:
  - Starter: 1 sub-account, no white-label, no Metabase.
  - Growth: 1 sub-account, basic white-label (logo + colors), Metabase read-only.
  - Scale: up to 3 sub-accounts (multi-office), full white-label (custom domain), Metabase with custom dashboards, Chrome extension, priority support.
  - Enterprise: everything + SSO + dedicated CSM + SOC 2 attestation on request.
- **14-day no-CC trial on Starter only.** Research (Ordway Labs, 2026) shows 14-day structured trials convert at ~44% when paired with Day 3 + Day 7 check-ins. 30-day trials underperform.
- **Demo-required for Growth+.** These are the real ACV drivers. Don't let them self-serve without a pitch.

### 1.3 JSON Pricing Table (Load into GHL SaaS Configurator)

```json
{
  "currency": "CAD",
  "billing_cycles": ["monthly", "annual"],
  "annual_discount_pct": 17,
  "plans": [
    {
      "id": "nx-starter",
      "name": "Starter",
      "price_monthly": 497,
      "price_annual": 4970,
      "stripe_price_id_monthly": "price_TBD_starter_month",
      "stripe_price_id_annual": "price_TBD_starter_year",
      "trial_days": 14,
      "trial_requires_cc": false,
      "features": {
        "rcic_seats": 2,
        "contacts_max": 2500,
        "ai_minutes_included": 300,
        "sms_included": 1000,
        "workflows": ["WF-01","WF-02","WF-03","WF-04","WF-05"],
        "sub_accounts": 1,
        "white_label": false,
        "metabase_access": false,
        "chrome_extension": false,
        "doc_storage_gb": 5,
        "esign_count": 10,
        "support_level": "email_48h",
        "snapshot_id": "snap_starter_v1"
      },
      "overage": { "ai_min": 0.25, "sms": 0.05, "seat": 15 }
    },
    {
      "id": "nx-growth",
      "name": "Growth",
      "price_monthly": 997,
      "price_annual": 9970,
      "stripe_price_id_monthly": "price_TBD_growth_month",
      "stripe_price_id_annual": "price_TBD_growth_year",
      "trial_days": 0,
      "trial_requires_cc": true,
      "most_popular": true,
      "features": {
        "rcic_seats": 5,
        "contacts_max": 10000,
        "ai_minutes_included": 1000,
        "sms_included": 3500,
        "workflows": "all_standard",
        "sub_accounts": 1,
        "white_label": "basic",
        "metabase_access": "readonly",
        "chrome_extension": true,
        "doc_storage_gb": 25,
        "esign_count": 50,
        "support_level": "email_24h_slack_shared",
        "snapshot_id": "snap_growth_v1"
      },
      "overage": { "ai_min": 0.22, "sms": 0.04, "seat": 12 }
    },
    {
      "id": "nx-scale",
      "name": "Scale",
      "price_monthly": 1997,
      "price_annual": 19970,
      "stripe_price_id_monthly": "price_TBD_scale_month",
      "stripe_price_id_annual": "price_TBD_scale_year",
      "trial_days": 0,
      "trial_requires_cc": true,
      "features": {
        "rcic_seats": 10,
        "contacts_max": 30000,
        "ai_minutes_included": 2500,
        "sms_included": 8000,
        "workflows": "all_plus_custom",
        "sub_accounts": 3,
        "white_label": "full_custom_domain",
        "metabase_access": "full_custom_dashboards",
        "chrome_extension": true,
        "doc_storage_gb": 100,
        "esign_count": 250,
        "support_level": "slack_priority_4h",
        "snapshot_id": "snap_scale_v1"
      },
      "overage": { "ai_min": 0.20, "sms": 0.035, "seat": 10 }
    },
    {
      "id": "nx-enterprise",
      "name": "Enterprise",
      "price_monthly": null,
      "price_annual": null,
      "custom": true,
      "starting_at_monthly": 2997,
      "features": {
        "rcic_seats": "unlimited",
        "contacts_max": "unlimited",
        "ai_minutes_included": "custom",
        "sms_included": "custom",
        "workflows": "all_plus_bespoke",
        "sub_accounts": "unlimited",
        "white_label": "full_plus_sso",
        "metabase_access": "full_plus_bespoke",
        "chrome_extension": true,
        "doc_storage_gb": "unlimited",
        "esign_count": "unlimited",
        "support_level": "dedicated_csm_1h",
        "snapshot_id": "snap_enterprise_custom"
      }
    }
  ],
  "setup_fee": {
    "amount": 1500,
    "currency": "CAD",
    "waived_on": ["annual_growth", "annual_scale", "enterprise"]
  }
}
```

---

## Section 2: GHL SaaS Configurator Setup

### 2.1 Current State (as of 2026-04-18)

Based on the PIT token context (`tools/ghl-lab/.pit-tokens.json`) and `tools/ghl-lab/src/setup_neuronx_saas.py`:

- **NeuronX agency**: `qKxHWhSxcGxcW3YycTui`
- **NeuronX sales sub-account**: `muc56LdMG8hkmlpFFuZE` (this is where WE sell FROM)
- **VMC sub-account**: `FlRL82M0D6nclmKT7eXH` (this is the CUSTOMER DEMO — not for billing)
- **Custom fields + tags in NeuronX sub-account**: 23 fields + 24 tags configured (per `setup_neuronx_saas.py`)
- **Pipeline "NeuronX Sales"**: Must be created via UI (pipeline API scope missing)

**What is NOT yet configured in SaaS Configurator**:
1. Stripe connection (shows "unverified" — see Section 3)
2. SaaS pricing plans (0 created)
3. Snapshots assigned to tiers (snapshots exist in VMC but not wired to plans)
4. Auto-provisioning rules
5. White-label / branding per tier
6. Trial conversion workflow

The `saas-api/public-api/locations` 403 error the user saw is expected: that endpoint requires an **Agency-level** API key (not location PIT). The Agency API key is issued from Agency Settings → API Keys and is what SaaS Configurator uses internally.

### 2.2 Step-by-Step Setup (GHL UI — ~3-4 hours)

**Prerequisite**: Stripe must be verified first (see Section 3). Configurator will accept settings but cannot charge until Stripe is live.

#### Step 1: Connect Stripe (Agency Level)
1. Navigate: `https://app.gohighlevel.com/settings/company-billing` → **Payments → Stripe Connect**
2. Click **Connect Stripe Account**
3. Complete Stripe OAuth (logs into Stripe, authorizes GHL platform)
4. Verify status changes from "unverified" to "verified" (requires Section 3 steps completed)

#### Step 2: Open SaaS Configurator
1. Agency Dashboard → **SaaS Mode** (left sidebar, under "Agency")
2. First time: click **Enable SaaS Mode** → accept terms
3. Tab: **Plans** → **+ Create Plan**

#### Step 3: Create Plan — Starter
Fields to fill in GHL UI:
- **Plan Name**: `NeuronX Starter`
- **Plan Description**: `AI intake for solo RCICs and 2-person firms`
- **Stripe Product**: Create new → `NeuronX Starter`
- **Monthly Price**: `$497 CAD`
- **Annual Price**: `$4,970 CAD` (toggle annual)
- **Trial Days**: `14`
- **Trial Requires CC**: `OFF`
- **Snapshot to Assign**: `snap_starter_v1` (upload first if not exists)
- **Rebilling - SMS**: Markup `$0.05/SMS` (our COGS via LC Phone ~$0.02)
- **Rebilling - Email**: Markup to $0.002/email (cost $0.00068)
- **Rebilling - AI Workflow**: Markup 2x on workflow AI actions
- **Rebilling - Voice (LC Phone)**: $0.10/min outbound (cost $0.04)
- **Feature Caps**:
  - Sub-accounts: 1
  - Users: 2
  - Contacts: 2,500
- **White-label**: OFF (shows "Powered by NeuronX")

#### Step 4: Create Plan — Growth (repeat structure)
- Name: `NeuronX Growth`
- Monthly: `$997 CAD` / Annual: `$9,970 CAD`
- Trial: `0 days, CC required` (demo-gated)
- Snapshot: `snap_growth_v1`
- Caps: 1 sub-account, 5 users, 10,000 contacts
- White-label: Basic (logo + colors, subdomain)
- Metabase: Read-only dashboard URL embedded

#### Step 5: Create Plan — Scale
- Name: `NeuronX Scale`
- Monthly: `$1,997 CAD` / Annual: `$19,970 CAD`
- Trial: `0 days, CC required`
- Snapshot: `snap_scale_v1`
- Caps: 3 sub-accounts, 10 users, 30,000 contacts
- White-label: Full (custom domain)
- Metabase: Full access

#### Step 6: Enterprise
- Create as **"Contact Sales" plan** (no Stripe price)
- Sales books call → manual Stripe invoice via Stripe Billing (not Configurator)

#### Step 7: Configure Auto-Provisioning
SaaS Configurator → **Settings → Sub-Account Creation**:
- Snapshot deploy: **automatic on payment success**
- User invite: send welcome email + temp password
- Phone number: auto-assign from agency pool (Starter: local; Growth+: toll-free)
- Custom domain DNS instructions: auto-email (Scale+)

#### Step 8: Test with $1 plan
Create a test plan at $1/mo, buy it yourself with a test card, verify:
1. Stripe charge succeeds
2. Sub-account auto-created with snapshot
3. Welcome email delivered
4. GHL login works for test customer
5. Cancel → sub-account paused (not deleted) after 7 days

---

## Section 3: Stripe Setup (Canada)

### 3.1 Resolving the "Unverified" Warning

The warning "The Stripe account connected to this agency is unverified and cannot collect payments" means Stripe's KYC (Know Your Customer) has not been completed. To resolve:

#### Required Documents for NeuronX (Canadian Incorporated Business)

1. **Business registration**:
   - Articles of Incorporation (federal: Corporations Canada) OR provincial (e.g., Ontario Ministry)
   - Business Number (BN) from CRA (9-digit, e.g., `123456789RC0001`)
   - If sole prop: Master Business Licence (Ontario) or provincial equivalent

2. **Banking**:
   - Canadian business bank account (Stripe Canada only deposits to CAD Canadian accounts)
   - Void cheque OR bank letter showing institution/transit/account numbers
   - Account must be in the registered business name

3. **Representative identity (you, Ranjan)**:
   - Government-issued photo ID (passport or Canadian driver's license)
   - SIN (last 4 digits; Stripe encrypts)
   - Home address (must match ID)
   - DOB
   - Signed declaration of beneficial ownership (auto-generated by Stripe)

4. **Business details**:
   - Full legal business name matching Articles of Incorporation
   - Business address (physical — P.O. Box not accepted)
   - Website URL (must be live; Stripe reviews it)
   - Product description: "SaaS platform for immigration consulting firms" (avoid vague language)
   - Expected monthly volume: **$10,000 CAD** initially (don't under-estimate; triggers re-review)
   - Average transaction: `$997 CAD`

5. **For SaaS specifically**:
   - Refund policy URL (see Section 3.4)
   - Terms of Service URL
   - Privacy Policy URL (PIPEDA-compliant)
   - Subscription cancellation process explained

#### Steps to Verify
1. Log into Stripe Dashboard → **Settings → Business Settings → Account details**
2. Click any yellow/red banner prompting verification
3. Upload docs in this order: business registration → banking → representative ID
4. Stripe review: **typically 1-3 business days**; up to 7 if flagged
5. Once verified, return to GHL → SaaS Configurator → Stripe tab → refresh connection

**If rejected**: Most common cause is website mismatch (Stripe visits your site and can't find pricing/TOS/refund policy). Fix: ensure `neuronx.ai` (or whatever domain) has public `/pricing`, `/terms`, `/privacy`, `/refund-policy` pages **before** submitting.

### 3.2 Canadian Tax Setup (HST/GST)

**Registration trigger**: NeuronX MUST register for GST/HST once gross Canadian revenue exceeds **$30,000 CAD in any rolling 12-month period** (per Stripe docs / CRA).

**Recommended**: Register **before** first sale. Voluntary registration benefits:
- Can claim input tax credits (reclaim GST paid on your costs — Railway, GHL, VAPI, OpenAI)
- Required anyway if you hit $30K in month 1 (Growth × 4 customers = $4K MRR = on pace for $48K)

**Steps**:
1. CRA Business Registration Online (BRO): https://www.canada.ca/en/services/taxes/business-number.html
2. Get GST/HST registration number (format: `123456789 RT0001`)
3. In Stripe: Dashboard → **Tax → Registrations → Add Canada → GST/HST**
4. Enter registration number
5. Enable **Stripe Tax** (auto-calculates GST/HST by customer province at checkout)

**Rates to apply** (Stripe Tax handles automatically, but for reference):
| Province                | Rate  | Type    |
|-------------------------|-------|---------|
| Ontario                 | 13%   | HST     |
| BC                      | 5%+7% | GST+PST |
| Alberta                 | 5%    | GST     |
| Quebec                  | 5%+9.975% | GST+QST |
| Nova Scotia             | 15%   | HST     |
| New Brunswick           | 15%   | HST     |
| PEI                     | 15%   | HST     |
| Newfoundland            | 15%   | HST     |
| Manitoba                | 5%+7% | GST+PST |
| Saskatchewan            | 5%+6% | GST+PST |

**For US customers** (if any): no GST/HST. Stripe Tax will also handle US state sales tax via Stripe Tax registrations (register in states you hit economic nexus — typically $100K or 200 transactions; you won't hit this for years).

**For non-Canadian/non-US customers**: B2B digital SaaS generally zero-rated when customer is GST/HST-registered business outside Canada. Collect customer's business tax ID via checkout.

**Filing**: Stripe Tax produces reports; file quarterly via CRA My Business Account.

### 3.3 Subscription Model in Stripe

**Use Stripe Billing (not one-time Charges)**.

- **Products** (one per tier): `NeuronX Starter`, `NeuronX Growth`, `NeuronX Scale`
- **Prices** per Product: one monthly, one annual (4 Prices if you do multi-currency later)
- **Subscription schedule**: standard monthly/annual, auto-renew
- **Trial**: set `trial_period_days` at Price level (Starter only)
- **Proration**: enabled (upgrades bill immediately prorated; downgrades take effect next cycle)
- **Usage overages**: use **Metered Prices** for AI minutes + SMS
  - Create metered Price: `ai_minute_overage` @ $0.25/unit
  - FastAPI reports usage via `/v1/subscription_items/:id/usage_records` daily
  - Billed at end of cycle

### 3.4 Failed Payment Handling (Dunning)

Configure in Stripe Dashboard → **Billing → Subscriptions → Retry Settings**:

- **Smart Retries**: ON (Stripe ML picks optimal retry times; +7% recovery vs fixed)
- **Retry schedule**: 1d, 3d, 5d, 7d (4 attempts over 7 days)
- **Email notifications**:
  - Day 0 (fail): "Payment failed — update card" (include magic link)
  - Day 3: reminder + offer to call
  - Day 7: "Final notice — account will be suspended in 24h"
- **After 7 days failed**:
  - GHL sub-account → **paused** (read-only; no new leads, no outbound)
  - After 30 days: sub-account → **archived** (data retained 90 days, then deleted per PIPEDA)
- **Webhook**: `invoice.payment_failed` → FastAPI → tags contact with `nx-saas:customer:churning`

### 3.5 Refund Policy (Post on Website Before Stripe Review)

**NeuronX Refund Policy — Recommended Language**:

> - **14-day money-back guarantee** for new Starter subscribers only. Contact support within 14 days of initial charge for full refund.
> - **Growth and Scale plans**: Non-refundable after initial charge. If you cancel mid-cycle, service continues through paid period; no partial refunds.
> - **Annual plans**: Non-refundable after 30 days. Within first 30 days, refund minus $500 setup fee.
> - **Enterprise**: Per contract.
> - **Exceptions**: Service outages >24 hours = prorated credit. Billing errors = full correction.

### 3.6 Subscription vs One-Time Charges

| Item               | Stripe Mechanism             |
|--------------------|------------------------------|
| Monthly/annual plan | Subscription (recurring)   |
| Setup fee ($1,500) | One-time Invoice Item added to first subscription invoice |
| AI minute overages | Metered Subscription Item   |
| SMS overages       | Metered Subscription Item   |
| Custom onboarding (Enterprise) | Separate Invoice   |
| Add-on (extra seat, extra snapshot) | Subscription Item (quantity-based) |

---

## Section 4: Feature Matrix by Tier

| Feature                          | Starter $497 | Growth $997 | Scale $1,997 | Enterprise |
|----------------------------------|--------------|-------------|--------------|------------|
| **Contacts/month**               | 2,500        | 10,000      | 30,000       | Unlimited  |
| **AI Call Minutes/mo (VAPI)**    | 300          | 1,000       | 2,500        | Custom     |
| **SMS/mo**                       | 1,000        | 3,500       | 8,000        | Custom     |
| **Emails/mo**                    | 10,000       | 50,000      | 150,000      | Unlimited  |
| **Workflows enabled**            | 5 core (WF-01 to WF-05) | All standard | All + custom workflows | All + bespoke |
| **Sub-accounts**                 | 1            | 1           | 3 (multi-office) | Unlimited |
| **RCIC Seats (users)**           | 2            | 5           | 10           | Unlimited  |
| **White-label branding**         | No (NeuronX logo) | Logo + colors | Full custom domain | Full + SSO |
| **Metabase analytics**           | No           | Read-only dashboards | Custom dashboards | Full + bespoke |
| **Chrome extension**             | No           | Yes         | Yes          | Yes        |
| **Document storage**             | 5 GB         | 25 GB       | 100 GB       | Unlimited  |
| **E-signatures (Docuseal)**      | 10/mo        | 50/mo       | 250/mo       | Unlimited  |
| **Support level**                | Email (48h)  | Email 24h + shared Slack | Priority Slack (4h) | Dedicated CSM (1h) |
| **Onboarding**                   | Self-serve + 30-min kickoff | 1-hr kickoff + setup | 3-hr guided + data migration | White-glove + SOC 2 attestation |
| **SLA**                          | 99.0%        | 99.5%       | 99.9%        | 99.95%     |
| **SSO (SAML/OIDC)**              | No           | No          | Add-on $200/mo | Included |
| **API access**                   | No           | Read        | Read + Write | Full       |
| **Data export**                  | CSV          | CSV + JSON  | CSV + JSON + webhook | All + scheduled |
| **Setup fee**                    | $1,500 (non-waivable) | $1,500 (waived on annual) | $1,500 (waived on annual) | Included |

### Gate Logic (Why These Lines)

- **AI minutes**: 300/mo = ~60 outbound calls at 5 min avg. A solo RCIC does ~100 inquiries/mo — Starter will overage. That's intentional (creates upgrade pressure).
- **Sub-accounts**: Most firms are single-office. Multi-office (Scale+) is a clear expansion signal.
- **White-label**: Basic is enough for SMB. Full custom domain is what enterprise firms ask for.
- **Metabase**: Biggest feature gate. Firms obsess over pipeline analytics; gating analytics to Growth+ forces upgrades.
- **Chrome extension**: For RCICs who want to grab prospect info from LinkedIn → NeuronX. High retention feature, gate to Growth+.

---

## Section 5: Self-Serve vs Sales-Led Strategy

### Recommendation: **Hybrid (tier-gated)**

| Tier       | Motion                           | Why                                                                 |
|------------|----------------------------------|---------------------------------------------------------------------|
| Starter    | **Pure self-serve** (website → Stripe → instant provision) | Low ACV, solo RCICs want fast. 14-day free trial does the selling. |
| Growth     | **Sales-assisted** (demo required, then self-checkout link) | $12K ACV — worth a 30-min demo. Reduce churn from mis-fit buyers. |
| Scale      | **Sales-led** (demo + ROI call + contract)     | $24K ACV — requires alignment with firm's operations. |
| Enterprise | **Full sales cycle** (multi-stakeholder, legal review) | Custom pricing, SOC 2, data migration. |

### Self-serve flow (Starter)
1. Visit `neuronx.ai/pricing`
2. Click "Start Free Trial" on Starter card
3. Signup form: name, email, firm name, phone (no CC)
4. → Stripe Checkout in trial mode (CC optional, skip button prominent)
5. → Auto-provision sub-account (GHL API)
6. → Welcome email with login + 5-min Loom walkthrough
7. Day 3: Check-in email "How's your first week?"
8. Day 7: "Unlock more — here's how paying customers use NeuronX"
9. Day 12: "2 days left in trial — add card to keep your data"
10. Day 14: Trial ends → if CC added, convert; if not, account paused (30-day data hold)

### Sales-led flow (Growth/Scale)
1. "Book Demo" button on pricing page
2. Calendly-style booking (use GHL calendar)
3. 30-min Zoom demo with founder
4. Post-demo: Stripe payment link (GHL Smart List)
5. On payment: same auto-provision flow
6. Week 1: 1-hour kickoff call
7. Week 2: data migration assistance (if from Clio/MyCase)
8. Week 4: success check-in

---

## Section 6: Post-Purchase Onboarding Flow

### 6.1 Automated Sequence (triggered by `checkout.session.completed` Stripe webhook → FastAPI → GHL)

**T+0 (payment success)**:
1. FastAPI receives `checkout.session.completed` webhook
2. FastAPI calls GHL SaaS API: create sub-account, apply snapshot (Starter/Growth/Scale)
3. FastAPI creates admin user in new sub-account, emails credentials
4. FastAPI assigns phone number from agency pool
5. FastAPI creates GHL opportunity in NeuronX Sales pipeline → move to "PAID CUSTOMER" stage
6. FastAPI sends welcome email (see template below)

**T+0 (email template)**:
```
Subject: Welcome to NeuronX — your account is ready

Hi [First Name],

Your NeuronX account for [Firm Name] is live.

[LOGIN URL with one-click magic link]

Credentials:
  Login: https://app.[tenant].neuronx.ai
  Email: [admin email]
  Temp password: [auto-generated, forced reset on login]

What's included in your [Plan Name] plan:
  - [X] AI call minutes/mo
  - [Y] SMS/mo
  - [Z] RCIC seats
  - Dedicated phone number: [+1 XXX XXX XXXX]

Next step (5 min):
  1. Log in and set your password
  2. Add your logo and brand colors
  3. Submit your first test inquiry via the intake form

Need help?
  - Starter: support@neuronx.ai (48h response)
  - Growth/Scale: your shared Slack channel (invite coming separately)

Your 1-hour kickoff call is booked for [Date/Time]:
  [Zoom link]

- Ranjan
Founder, NeuronX
```

**T+1 day**: GHL workflow `NX-SAAS-ONBOARD-01` triggers → sends "Quick setup video" email
**T+3 days**: Check-in — "Ran into anything? Reply to this email"
**T+7 days**: Usage report — "You've used X min of Y — here's how top firms ramp up"
**T+14 days**: Success milestone — "Here's what your pipeline looks like"
**T+30 days**: Upsell trigger if usage >80% of AI minutes → "Consider Growth"

### 6.2 Data Migration (Scale+ only; optional paid add-on $1,500 for Growth)

Supported source systems:
- Clio Manage (CSV export → mapping script)
- MyCase (CSV export)
- HubSpot (API sync)
- Officio / RCIC Suite (manual CSV)
- Spreadsheets (template provided)

Turnaround: 5 business days. Data validated before go-live.

### 6.3 Phone Number Provisioning

- **Starter**: Local number from firm's area code (random). Via LC Phone.
- **Growth**: Local + option for vanity (+$15 one-time).
- **Scale**: Toll-free included (one 1-8XX number). Local numbers for each sub-account.
- **Enterprise**: Number porting supported (bring your own).

### 6.4 Kickoff Call Agenda (Growth+)

1. Confirm firm's intake process (what happens today?)
2. Map their workflow to NeuronX (which WF-01-WF-CP-09 fit their practice?)
3. Upload logo + brand colors
4. Configure AI voice persona (name, tone, handoff rules)
5. Set business hours (for VAPI outbound windows)
6. Test one inquiry end-to-end
7. Hand off to Slack channel

---

## Section 7: Billing Mechanics

### 7.1 Invoice Generation

- **Monthly**: Auto-generated by Stripe on subscription anniversary. Emailed as PDF.
- **Annual**: Same, annually. Offer option to pay via EFT (for >$10K invoices) — reduces Stripe fees.
- **Custom line items**: Setup fee on first invoice only. Overages on cycle-end invoice.
- **Invoice customization**: Brand Stripe invoices with NeuronX logo (Stripe Dashboard → Settings → Branding).

### 7.2 Trial Period Policy

- **Starter**: 14 days, no CC. Auto-converts to paid IF CC added during trial. No conversion = paused.
- **Growth/Scale**: No free trial. Instead: **30-day money-back guarantee on annual plans only** (non-refundable on monthly).
- **Enterprise**: Proof-of-concept (POC) pilot, typically 60 days, contracted.

### 7.3 Upgrades / Downgrades / Cancellations

**Upgrades** (e.g., Starter → Growth):
- Effective immediately
- Stripe prorates: charge difference for remaining cycle on next invoice
- Sub-account gets upgraded snapshot applied (additive — no data loss)

**Downgrades** (e.g., Scale → Growth):
- Effective at next billing cycle (not immediate — prevents abuse)
- Customer keeps full access through current period
- Warning if usage exceeds lower tier limits — prompted to stay or accept overages

**Cancellations**:
- Self-serve cancel button in customer portal (Stripe-hosted)
- Cancel at period end (default) — keep access until paid period ends
- Immediate cancel = no refund (unless within 14-day guarantee)
- Exit survey (GHL form): reason + NPS — feeds `saas_churn_reason` custom field

### 7.4 Usage Overage Fees

Overages are billed on the invoice after the cycle where they occurred. Caps prevent runaway bills:

- **Soft cap** at 100% of included: warning email
- **Hard cap** at 150%: throttle (new AI calls disabled, SMS queued)
- Customer can click "Lift cap" in portal → acknowledges additional charges

Per-unit overage rates (see JSON in Section 1.3):
- AI min: $0.25 (Starter) / $0.22 (Growth) / $0.20 (Scale) — 15-20% premium over COGS
- SMS: $0.05 / $0.04 / $0.035
- Extra seat: $15 / $12 / $10

### 7.5 Tax Handling (Canadian + US)

- **Enable Stripe Tax** (flat $0.50/txn fee; worth it for auto-calc)
- **Canadian customers**: Stripe auto-determines province from billing address → applies HST/GST/PST
- **US customers**: Stripe Tax checks nexus; initially no US tax charged (below threshold)
- **Invoices show**: subtotal, tax line with rate, total
- **Tax reports**: Export monthly from Stripe Tax → give to accountant

---

## Section 8: Cost-to-Serve & Gross Margin

### 8.1 COGS per Customer (CAD/month, estimated at 2026-04 costs)

| Cost Item                        | Starter | Growth  | Scale   | Notes                              |
|----------------------------------|---------|---------|---------|------------------------------------|
| GHL sub-account (agency SaaS Pro covers) | $0   | $0   | $0 (up to 3) | SaaS Pro plan is $497/mo at agency level — amortized across all customers |
| Railway hosting (FastAPI)        | $8      | $15     | $25     | Per-tenant resources               |
| VAPI (AI minutes @ $0.25/min blended) | $75  | $250    | $625    | Included minutes × blended         |
| Twilio / LC Phone (SMS @ $0.015) | $15     | $52     | $120    | Included SMS × LC Phone cost       |
| LC Email (emails @ $0.0007)      | $7      | $35     | $105    | Included emails × cost             |
| OpenAI API (scoring, briefings)  | $10     | $30     | $70     | ~$0.04/lead × contacts             |
| Metabase (hosted Starter Pro)    | $0      | $5      | $10     | Shared across customers; negligible per |
| Docuseal (e-sign)                | $2      | $10     | $50     | $0.20/envelope                     |
| Storage (S3 / Railway volumes)   | $1      | $3      | $10     |                                    |
| Support labor (human, avg)       | $20     | $75     | $200    | 15 min/mo Starter, 45 min Growth, 2h Scale |
| Stripe fees (2.9% + $0.30)       | $14     | $29     | $58     | On gross revenue                   |
| GST/HST pass-through (net)       | $0      | $0      | $0      | Collected & remitted, neutral      |
| **Total COGS**                   | **$152**| **$504**| **$1,273** |                                 |
| **Plan Price**                   | $497    | $997    | $1,997  |                                    |
| **Gross Profit**                 | **$345**| **$493**| **$724** |                                   |
| **Gross Margin**                 | **69%** | **49%** | **36%** |                                    |

### 8.2 Margin Analysis

**Starter margin is healthiest (69%)** because the included AI/SMS allocations are conservative. This is correct — Starter customers are price-sensitive and will upgrade when they hit caps. Don't cut Starter minutes further; 300 is already tight.

**Growth margin (49%) is concerning** if firms actually use their full 1,000 AI minutes. Reality: average usage across SaaS trials is 40-60% of allocation. Expected realized margin: **~60-65%** once you account for under-utilization.

**Scale margin (36%) is low** on paper but masks:
1. 3 sub-accounts means 3× the configuration stickiness — churn is lower.
2. Scale customers rarely max out minutes (they have human intake teams too).
3. Enterprise expansion often comes from Scale firms first — effective LTV is higher.

### 8.3 Recommended Adjustments After 10 Customers

Re-evaluate COGS after first 10 paying customers. Likely tweaks:
- If AI usage >70% across base: raise Growth to $1,197 or reduce included minutes to 800.
- If SMS usage <30%: don't cut, keep as perceived-value filler.
- If support labor >estimates: invest in better self-serve docs before hiring.

### 8.4 CAC Targets

- **Starter**: CAC <$250 (self-serve; paid ads + content)
- **Growth**: CAC <$1,500 (founder-led sales for first 20; then SDR)
- **Scale**: CAC <$4,000 (founder-led, longer cycle)
- **Enterprise**: CAC <$15,000 (consultative)

LTV/CAC target: >3x across all tiers.

### 8.5 Payback Period

| Tier   | Monthly GP | Setup Fee | CAC     | Payback        |
|--------|-----------|-----------|---------|----------------|
| Starter| $345      | $1,500    | $250    | **Immediate** (setup covers CAC) |
| Growth | $493      | $1,500    | $1,500  | **~0 months** (setup covers CAC, first mo profit) |
| Scale  | $724      | $1,500    | $4,000  | **~3.5 months** |

---

## Section 9: Implementation Checklist (What Ranjan Does Next)

**Week 1 (this week)**:
- [ ] Gather Stripe verification docs (Articles, BN, void cheque, photo ID) — 2 hours
- [ ] Publish `/pricing`, `/terms`, `/privacy`, `/refund-policy` on `neuronx.ai` — 4 hours
- [ ] Register for GST/HST via CRA BRO (don't wait; saves Q4 pain) — 30 min
- [ ] Submit Stripe verification — 20 min upload, 1-3 day wait

**Week 2**:
- [ ] Enable Stripe Tax, add Canada GST/HST registration number
- [ ] Create 3 Stripe Products (Starter/Growth/Scale) with monthly + annual Prices
- [ ] In GHL: connect verified Stripe, enable SaaS Mode
- [ ] Create 3 SaaS plans in Configurator with feature caps + snapshots
- [ ] Test with $1 plan (real card, real provisioning)

**Week 3**:
- [ ] Build sub-account snapshots (`snap_starter_v1`, `snap_growth_v1`, `snap_scale_v1`) — differ by workflow set
- [ ] Wire FastAPI webhook receiver for `checkout.session.completed` → auto-provision
- [ ] Build welcome email templates in GHL
- [ ] Set up customer portal URL (Stripe-hosted self-serve)

**Week 4**:
- [ ] Soft launch to 3 warm prospects (charge $497 Starter)
- [ ] Measure: time to first value, first overage hit, support tickets
- [ ] Adjust tiers if any disaster signals

---

## Section 10: Open Questions for Founder

1. **Final tier prices**: confirm $497/$997/$1,997 or push to $597/$1,197/$2,497? (Recommendation: launch at $497/$997/$1,997. Raise by 20% after 10 customers; grandfather early adopters.)
2. **Annual discount**: 17% (2 months free) or 25%? (Recommend 17% — preserves margin while incentivizing commitment.)
3. **Setup fee**: $1,500 confirmed? Some competitors don't charge. Recommendation: keep it for Starter (selects for serious buyers), waive on annual Growth/Scale.
4. **Trial on Growth**: offer 14-day POC for $100 instead of free trial? (Recommend skipping free trial on Growth; demo-gate instead.)
5. **White-label on Starter**: currently OFF. Some competitors include. Keep OFF — biggest upgrade driver to Growth.
6. **Metabase gating**: Read-only on Growth is generous. Consider gating all Metabase to Scale? (Recommend: keep Growth read-only — retention feature.)
7. **Bring-your-own-Stripe** for Scale+ (let customer receive their client payments through their own Stripe via GHL SaaS Configurator rebilling)? Likely yes for Scale+ — makes them stickier.

---

## Appendix A: Stripe Webhook Events to Handle in FastAPI

| Event                             | Action                                                  |
|-----------------------------------|---------------------------------------------------------|
| `checkout.session.completed`      | Provision sub-account, send welcome, create opportunity |
| `customer.subscription.created`   | Tag contact `nx-saas:customer:paying`                   |
| `customer.subscription.updated`   | Sync plan tier → GHL custom field `saas_plan`           |
| `customer.subscription.deleted`   | Pause sub-account after 7d, archive after 30d           |
| `invoice.payment_succeeded`       | Log payment, extend access                              |
| `invoice.payment_failed`          | Dunning sequence → tag `nx-saas:customer:churning`      |
| `invoice.upcoming`                | 7d-before heads-up if overages detected                 |
| `customer.subscription.trial_will_end` | 3d-before trial conversion email              |

## Appendix B: Competitor Positioning Cheat Sheet (for sales calls)

**vs Clio Manage**: "Clio is great for case management after you've won the client. NeuronX wins you the client — AI voice intake within 5 minutes of form submission. Clio has no voice. Plus we're flat-priced so your paralegals don't cost extra."

**vs MyCase**: "MyCase is per-seat and US-focused. For a 5-person Canadian firm you're paying $545/mo for MyCase Advanced and getting no intake automation. NeuronX Growth is $997 all-in with AI voice + intake + CRM."

**vs Officio / RCIC Suite**: "Those are great case management tools built by Canadians for Canadians — but they stop at case management. NeuronX handles the top of the funnel they don't touch: inbound inquiries, AI qualification, booking, retainer delivery. Use us together."

**vs INSZoom**: "INSZoom is enterprise-grade and priced for 50+ person firms. For a 5-10 RCIC practice it's overkill and overpriced. NeuronX is purpose-built for your scale."

---

**Sources**:
- [GoHighLevel SaaS Mode Setup Guide](https://help.gohighlevel.com/support/solutions/articles/48001184920-saas-mode-full-setup-guide-faq)
- [GoHighLevel Pricing 2026](https://www.highlevel.ai/pricing-explained.html)
- [HighLevel Rebilling, Reselling, and Wallets Explained](https://help.gohighlevel.com/support/solutions/articles/155000002095-rebilling-reselling-and-wallets-explained)
- [How to Import Stripe Products into SaaS Configurator](https://help.gohighlevel.com/support/solutions/articles/155000006287-how-to-import-stripe-products-into-saas-configurator)
- [Clio Legal Software Plans & Pricing](https://www.clio.com/pricing/)
- [MyCase Pricing 2026](https://mycasepricing.com/)
- [Vapi AI Pricing: True Cost Breakdown in 2026 (Zeeg)](https://zeeg.me/en/blog/post/vapi-ai-pricing)
- [Voice AI Cost Per Minute (Klariqo)](https://klariqo.com/blog/voice-ai-cost-per-minute/)
- [Stripe Canada: Verification Requirements](https://support.stripe.com/questions/verification-requirements-canada)
- [Stripe GST Tax in Canada: Rates, Rules, and Registration](https://stripe.com/resources/more/gst-in-canada)
- [Stripe Tax: Canada](https://docs.stripe.com/tax/supported-countries/canada)
- [SaaS Pricing Strategy Guide 2026 (NxCode)](https://www.nxcode.io/resources/news/saas-pricing-strategy-guide-2026)
- [SaaS Free Trial Length Conversion (Ordway Labs)](https://ordwaylabs.com/blog/saas-free-trial-length-conversion/)
- [B2B SaaS Conversion Benchmarks 2026 (Pixelswithin)](https://pixelswithin.com/b2b-saas-conversion-benchmarks-2026/)
- [Top 12 Immigration Case Management Software 2026](https://thelegalpractice.com/tools/best-immigration-case-management-software/)
