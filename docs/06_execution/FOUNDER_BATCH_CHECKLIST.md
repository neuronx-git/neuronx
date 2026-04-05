# NeuronX — Founder Batch Task Checklist

**Purpose**: Complete all UI/billing/DNS tasks in one session (~2-3 hours).
**When**: After Claude completes all API-possible work.
**Date**: 2026-03-24

---

## Current Agency State (from API Audit)

| Item | Status | Count |
|------|--------|-------|
| Company name | `goldenphoenix1216@gmail.com` — **needs update to "NeuronX"** | - |
| Timezone | UTC — **needs update to America/Toronto** | - |
| Country | US — **needs update to CA** | - |
| Currency | USD — **needs update to CAD** | - |
| Logo/Favicon | Not set | - |
| Custom fields | 113 (41 NX + pre-existing) | OK |
| Tags | 89 (63 NX-prefixed) | OK |
| Workflows | 15/15 published | OK |
| Calendar | 1 (Immigration Consultations) | OK |
| Pipeline | 1 (9 stages — API can't list but exists in UI) | OK |
| Form | 1 (Immigration Inquiry V1 — ID: FNMmVXpfUvUypS0c4oQ3) | OK |
| Sub-accounts | 0 (Gold lab is the only location) | Expected |
| Snapshots | None created yet | Expected |
| SaaS Mode | Not activated (requires Stripe first) | Expected |
| Stripe | Not connected | Needs setup |
| Phone numbers | None provisioned via LC Phone | Needs setup |
| Email domain | Not configured | Needs setup |
| White-label | Not configured | Needs setup |

---

## SECTION 1: Agency Admin (~15 min)

### 1.1 Update Company Profile
Navigate: **Settings → Company** (Agency level, NOT sub-account)

- [ ] Change company name: `NeuronX`
- [ ] Set timezone: `America/Toronto (Eastern)`
- [ ] Set country: `Canada`
- [ ] Set currency: `CAD`
- [ ] Set business phone: `+1 (647) XXX-XXXX` (your NeuronX business number)
- [ ] Set business address: (your registered business address)
- [ ] Upload company logo (NeuronX logo — SVG or PNG, minimum 200x200px)
- [ ] Upload favicon (32x32 PNG or ICO)

### 1.2 Review Agency Settings
Navigate: **Settings → My Staff**

- [ ] Verify your admin account has full permissions
- [ ] Add any team members if applicable (or skip for now)

---

## SECTION 2: Stripe Connection (~15 min)

### 2.1 Create Stripe Account (if you don't have one)
1. Go to [stripe.com](https://stripe.com)
2. Sign up with your business email
3. Complete business verification (name, address, bank account)
4. Note: Stripe requires identity verification — have ID ready

### 2.2 Connect Stripe to GHL
Navigate: **Settings → Payments → Stripe**

1. [ ] Click "Connect with Stripe"
2. [ ] Log into your Stripe account
3. [ ] Authorize GHL to access your Stripe
4. [ ] Verify connection shows "Connected" in GHL

**Why**: Stripe must be connected before SaaS Mode can be activated.

---

## SECTION 3: Purchase Domain (~10 min)

### 3.1 Buy NeuronX Domain
**Recommended**: Use [Cloudflare Registrar](https://dash.cloudflare.com) (at-cost pricing, built-in CDN/DNS)

1. [ ] Purchase `neuronx.ai` (or `neuronx.ca` / `neuronx.com`)
2. [ ] Set up Cloudflare account (free tier) if using Cloudflare
3. [ ] Point domain nameservers to Cloudflare (if purchased elsewhere)
4. [ ] Verify domain resolves (may take 1-24 hours for DNS propagation)

**Share with Claude**: The exact domain you purchased (e.g., `neuronx.ai`)

---

## SECTION 4: Phone Numbers (~15 min)

### 4.1 Buy Agency Phone Number
Navigate: **Settings → Phone Numbers → Buy Number** (Agency level)

1. [ ] Search for a Canadian local number (647 or 416 area code for Toronto)
2. [ ] Purchase number (~$1.15/mo)
3. [ ] Note the number: `+1 (___) ___-____`

### 4.2 Buy VMC Phone Number
Navigate: **Sub-account: Visa Master Canada → Settings → Phone Numbers → Buy Number**

1. [ ] Search for Canadian number (647/416 area code)
2. [ ] Purchase number (~$1.15/mo)
3. [ ] Note the number: `+1 (___) ___-____`

**Share with Claude**: Both phone numbers — Claude will configure VAPI with the VMC number.

### 4.3 A2P 10DLC Registration (Required for SMS)
Navigate: **Settings → Phone Numbers → A2P Registration**

This is required by carriers for business SMS in US/Canada.

1. [ ] Select brand type: "Standard" (for businesses)
2. [ ] Enter legal company name
3. [ ] Enter EIN / Business Number (Canadian: BN)
4. [ ] Enter business address
5. [ ] Enter business vertical: "Professional Services"
6. [ ] Enter message sample: "Thank you for your inquiry with Visa Master Canada. We're reviewing your information and will reach out shortly. Reply STOP to opt out."
7. [ ] Submit registration (approval takes 1-5 business days)

**Note**: SMS workflows won't work until A2P is approved. Email workflows work immediately.

---

## SECTION 5: Email Services (~20 min)

### 5.1 Set Up Dedicated Email Domain
Navigate: **Settings → Email Services** (Agency level)

GHL uses Mailgun for email sending. You need to verify a sending domain.

1. [ ] Click "Add Domain" or "Connect Mailgun"
2. [ ] Enter sending domain: `mail.neuronx.ai` (or your domain variant)
3. [ ] GHL will display DNS records to add

### 5.2 Add DNS Records
In your DNS provider (Cloudflare), add these records:

| Type | Name | Value | Notes |
|------|------|-------|-------|
| TXT | `mail.neuronx.ai` | (GHL provides SPF record) | SPF verification |
| TXT | `mailo._domainkey.mail.neuronx.ai` | (GHL provides DKIM) | DKIM signing |
| CNAME | `email.mail.neuronx.ai` | `mailgun.org` | Tracking |

**Copy exact values from GHL** — they'll be displayed after step 5.1.

3. [ ] Add all DNS records in Cloudflare
4. [ ] Wait 5-30 min for propagation
5. [ ] Click "Verify" in GHL
6. [ ] Verify shows green checkmarks

### 5.3 Configure System Emails
Navigate: **Settings → Business Profile → General** (in sub-account)

1. [ ] Set "From Name": `Visa Master Canada` (for VMC sub-account)
2. [ ] Set "From Email": `info@visamastercanada.com` or `hello@mail.neuronx.ai`

---

## SECTION 6: White-Label Domains (~20 min)

### 6.1 Add DNS Records
In your DNS provider (Cloudflare), add these 5 CNAME records:

| Record | Type | Name | Target |
|--------|------|------|--------|
| App | CNAME | `app.neuronx.ai` | `msgsndr.com` |
| API | CNAME | `api.neuronx.ai` | `api-white-label.msgsndr.com` |
| Sites/Funnels | CNAME | `sites.neuronx.ai` | `sites-white-label.msgsndr.com` |
| Email | CNAME | `mail-link.neuronx.ai` | `email.msgsndr.com` |
| Client Portal | CNAME | `portal.neuronx.ai` | `msgsndr.com` |

**Important**: If using Cloudflare, set proxy status to "DNS only" (gray cloud) for these records.

1. [ ] Add all 5 CNAME records in Cloudflare
2. [ ] Wait 5-15 min for propagation

### 6.2 Configure in GHL
Navigate: **Settings → White Label** (Agency level)

1. [ ] Set App Domain: `app.neuronx.ai` → click Verify
2. [ ] Set API Domain: `api.neuronx.ai` → click Verify
3. [ ] Set Sites Domain: `sites.neuronx.ai` → click Verify
4. [ ] Set Email Link Domain: `mail-link.neuronx.ai` → click Verify
5. [ ] Set Client Portal Domain: `portal.neuronx.ai` → click Verify

### 6.3 White-Label Appearance
Navigate: **Settings → White Label → Appearance**

1. [ ] Upload NeuronX logo (header logo, 300x80px recommended)
2. [ ] Upload NeuronX favicon
3. [ ] Set primary color: `#E8380D` (NeuronX red) or your brand color
4. [ ] Set app name: `NeuronX`
5. [ ] Set support email: `support@neuronx.ai`
6. [ ] Set Terms of Service URL (can add later)
7. [ ] Set Privacy Policy URL (can add later)

### 6.4 Verify White-Label
1. [ ] Open `app.neuronx.ai` in an incognito browser
2. [ ] Verify NeuronX branding shows (no GHL/HighLevel logos)
3. [ ] Verify login page works

---

## SECTION 7: SaaS Mode Activation (~15 min)

**Prerequisites**: Stripe connected (Section 2), GHL SaaS Pro plan active.

### 7.1 Activate SaaS Mode
Navigate: **Settings → SaaS Configurator**

1. [ ] Click "Enable SaaS Mode" (if not already enabled)
2. [ ] Select your connected Stripe account

### 7.2 Create Pricing Plans
Navigate: **SaaS Configurator → Plans**

Create these 3 plans:

**Plan 1: NeuronX Starter**
- [ ] Price: $497 CAD/month
- [ ] Includes: Base snapshot, 1 pipeline, 1 calendar, 500 contacts
- [ ] Mark as default plan for new sub-accounts

**Plan 2: NeuronX Professional**
- [ ] Price: $997 CAD/month
- [ ] Includes: Everything in Starter + AI calling, advanced workflows, unlimited contacts

**Plan 3: NeuronX Enterprise**
- [ ] Price: $1,497 CAD/month
- [ ] Includes: Everything in Pro + dedicated support, custom integrations

**Note**: Pricing is a founder decision (OD-02). These are recommendations — adjust as you see fit.

---

## SECTION 8: Snapshot Creation (~5 min)

### 8.1 Create Gold Snapshot
Navigate: **Settings → Company → Snapshots** (Agency level)

1. [ ] Click "Create Snapshot"
2. [ ] Select source: `Visa Master Canada` (the Gold sub-account)
3. [ ] Name: `NeuronX Gold v1.0 — Immigration Intake`
4. [ ] Select what to include:
   - [x] Workflows (all 15)
   - [x] Custom Fields (all)
   - [x] Tags (all)
   - [x] Pipeline + Stages
   - [x] Calendar
   - [x] Forms
   - [x] Funnels (if any)
   - [x] Email templates
   - [x] Surveys
5. [ ] Click "Create Snapshot"
6. [ ] Wait for snapshot creation to complete (1-3 min)

### 8.2 Get Snapshot ID
1. [ ] Copy the snapshot ID from the snapshot list
2. [ ] Share with Claude: `Snapshot ID: _______________`

**Claude will use this to create new sub-accounts via API with the Gold config pre-loaded.**

---

## SECTION 9: Funnels (~30-60 min, collaborative)

### 9.1 Choose a Template

**DO NOT import the GHL Immigration Lawyer Playbook snapshot** — it would overwrite/duplicate our 15 custom workflows, pipeline, and fields.

**Use one of these instead** (funnel template ONLY, no snapshot):

- **GHL built-in template library** (FREE): Sites → Funnels → New → Template Library → "Book Appointment" or "Professional Services" category
- **GHLElite consulting template**: $67-97 (ghlelite.com) — modern, clean design
- **FunnelsFlex coaching template**: $49 (funnelsflex.io) — pre-customization included

Then paste VMC copy from `docs/06_execution/VMC_FUNNEL_COPY.md`.

1. [ ] Browse GHL template library or purchase a premium funnel template
2. [ ] Name the funnel: "VMC — Immigration Intake"

### 9.2 Customize (Claude provides all copy)
Claude will provide section-by-section copy and branding instructions for:
- Hero section (headline, subheadline, CTA)
- Trust bar (stats, credentials)
- Services section
- Testimonials
- FAQ
- Footer

1. [ ] Apply VMC branding (logo, colors: Primary Red #E8380D, Navy #0F172A)
2. [ ] Replace template text with Claude's copy
3. [ ] Connect GHL form (Immigration Inquiry V1) to the funnel
4. [ ] Set up Thank You page

### 9.3 Publish & Connect Domain
1. [ ] Connect custom domain: `intake.visamastercanada.com` (add CNAME in DNS)
2. [ ] Publish funnel
3. [ ] Test: submit form, verify WF-01 fires

---

## After Completing All Sections

**Tell Claude**:
1. NeuronX domain: `____________`
2. VMC phone number: `+1 (___) ___-____`
3. Agency phone number: `+1 (___) ___-____`
4. Snapshot ID: `____________`
5. Stripe connected: Yes/No
6. SaaS Mode active: Yes/No
7. White-label verified: Yes/No
8. Email domain verified: Yes/No

**Claude will then**:
- Create VMC sub-account via API with snapshot
- Configure VMC-specific details
- Update VAPI with new phone number
- Run full verification audit
- Update PROJECT_MEMORY.md

---

## Cost Summary

| Item | Cost | Frequency |
|------|------|-----------|
| GHL SaaS Pro | $497/mo | Monthly (already paying) |
| Domain (neuronx.ai) | ~$15/yr | Annual |
| Phone number (agency) | ~$1.15/mo | Monthly |
| Phone number (VMC) | ~$1.15/mo | Monthly |
| SMS usage | ~$0.0079/segment | Per use |
| Voice usage | ~$0.017/min | Per use |
| Email (Mailgun via GHL) | ~$0.80/1000 | Per use |
| Stripe fees | 2.9% + $0.30 | Per transaction |
| **Total new monthly** | **~$5-10/mo** | (on top of existing GHL plan) |
