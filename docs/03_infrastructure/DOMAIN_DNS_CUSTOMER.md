# Customer Domain Onboarding Playbook

**Version**: 1.0
**Status**: CANONICAL
**Owner**: Infra / Ops
**Last Updated**: 2026-04-18
**Scope**: How to give a newly-subscribed immigration firm a branded domain footprint on NeuronX.

---

## TL;DR — Tier Summary

| Tier | Customer Domain | Setup Time | Who Does DNS | What Is Branded |
|------|-----------------|------------|--------------|-----------------|
| **0** | None — use NeuronX defaults | **0 min** | Nobody | `www.neuronx.co/intake/{slug}/onboarding` (no firm branding) |
| **1** | Free subdomain on `neuronx-clients.co` | **5 min** (all on our side) | NeuronX | `{firm}.neuronx-clients.co` (partial brand — NeuronX visible) |
| **2** | Firm-owned domain, CNAME only | **30 min config + 15 min–24 h DNS propagation + up to 48 h DKIM** | Firm's IT with our exact records | Full firm brand (`apply.firmname.ca`, `cases.firmname.ca`, `mg.firmname.ca`) |
| **3** | Firm-owned domain, root redirect + full white-label | **60–90 min + 48 h DKIM + up to 72 h SSL warm-up** | Firm's IT | Full white-label including funnel on root domain |

**Default recommendation for new firms: Tier 2.** Tier 1 is a fallback for firms with no domain yet. Tier 3 is a paid add-on.

---

## Section 1 — Current NeuronX Domain Architecture

### 1.1 Authoritative DNS state (verified live 2026-04-18)

Verified via `dig +short`:

| Record | Value | Verified | Source |
|--------|-------|----------|--------|
| `neuronx.co` A | `216.198.79.1` | ✅ live | Vercel anycast |
| `www.neuronx.co` CNAME | `cname.vercel-dns.com.` | ✅ live | Vercel |
| `mg.neuronx.co` MX (10) | `mxa.mailgun.org.` | ✅ live | LeadConnector/Mailgun shared MX |
| `mg.neuronx.co` MX (10) | `mxb.mailgun.org.` | ✅ live | LeadConnector/Mailgun shared MX |
| `mg.neuronx.co` TXT (SPF) | `v=spf1 include:spf.leadconnectorhq.com include:mailgun.org ~all` | ✅ live | LeadConnector + Mailgun |
| `_dmarc.neuronx.co` TXT | `v=DMARC1; p=none; rua=mailto:dmarc@neuronx.co; sp=quarantine; fo=1` | ✅ live | DMARC monitoring only |

From PROJECT_MEMORY.md "GHL DNS Records (neuronx.co — Internal Domain)" table (not re-verified live in this session):

| Record | Value | Purpose |
|--------|-------|---------|
| `forms.neuronx.co` CNAME | `neuronx-production-62f9.up.railway.app` | Railway custom domain (SSL pending; use Vercel proxy instead) |
| `vmc.neuronx.co` CNAME | `sites.ludicrous.cloud` | GHL white-label funnel for VMC demo |
| `api.neuronx.co` CNAME | `brand.ludicrous.cloud` | GHL API white-label |
| `app.neuronx.co` CNAME | `whitelabel.ludicrous.cloud` | GHL admin white-label |

> **Operator must re-verify:** run `dig +short forms.neuronx.co`, `dig +short vmc.neuronx.co`, `dig +short api.neuronx.co`, `dig +short app.neuronx.co` if you need ground truth. The DNS-audit bash calls for these hosts were denied in the session where this doc was drafted; values above come from `PROJECT_MEMORY.md:160-169`.

### 1.2 Routing diagram

```
                              ┌───────────────────────┐
                              │  Cloudflare DNS for   │
                              │      neuronx.co       │
                              └───────────┬───────────┘
                                          │
            ┌─────────────┬───────────────┼────────────────┬──────────────┐
            │             │               │                │              │
        neuronx.co   www.neuronx.co   forms.neuronx.co  vmc/api/app   mg.neuronx.co
            │             │               │                │              │
        (A 216.198.79.1)  │               │                │              │
        Vercel ──────────►│               │                │              │
                         Vercel ────────► │                │              │
                                          │                │              │
                          (also used by Vercel proxy to    │              │
                           /intake/vmc/onboarding)         │              │
                                                           │              │
                                          Railway ◄────────┘              │
                                     (neuronx-api  FastAPI)               │
                                          ▼                               │
                                   /form/vmc/onboarding ──► Typebot Viewer│
                                                                          │
                                          GHL white-label ◄───────────────┘
                                     (ludicrous.cloud edge)
                                                                          │
                                                                 LeadConnector/Mailgun
                                                                    (SMTP sender)
```

### 1.3 Shared vs VMC-specific

| Subdomain | Scope | Notes |
|-----------|-------|-------|
| `neuronx.co` / `www.neuronx.co` | **Agency (shared)** | Marketing site; serves intake for VMC via Vercel proxy |
| `mg.neuronx.co` | **Agency (shared)** | Only email sender today — all firms relay through it at Tier 0/1 |
| `forms.neuronx.co` | **Agency (shared)** | Points to Railway; currently unused by end-users (Vercel proxy is preferred) |
| `vmc.neuronx.co` | **VMC-specific demo** | GHL funnel for VMC demo location (`vb8iWAwoLi2uT3s5v1OW`) |
| `api.neuronx.co` / `app.neuronx.co` | **Agency (shared) white-label** | GHL admin + API custom host; identical across all sub-accounts |

**Key implication:** today, everything except `vmc.*` is agency-shared. Per-firm branding is achieved by pointing the **firm's domain** at our agency infra — not by creating per-firm subdomains under `neuronx.co`.

---

## Section 2 — Customer Firm's Domain Needs

### Scenario A — Firm already owns a domain (e.g., `maplecrestimmigration.ca`)

This is the happy path. We add CNAME/MX/TXT records on their zone so their branded URLs resolve to our infrastructure.

**Minimum branded surface for Tier 2:**

| Branded URL | Points To | Purpose |
|-------------|-----------|---------|
| `apply.maplecrestimmigration.ca` | `viewer-production-366c.up.railway.app` | Typebot-viewer-served intake form |
| `cases.maplecrestimmigration.ca` | `neuronx-production-62f9.up.railway.app` | Case viewer `/cases/{id}/viewer` |
| `mg.maplecrestimmigration.ca` | Mailgun MX + SPF + DKIM TXT | Email sender domain (per-firm) |
| `hire.maplecrestimmigration.ca` | `sites.ludicrous.cloud` (GHL) | GHL funnel for retainer/booking |

**Propagation time:** 5–60 minutes for CNAME (Cloudflare is ~1–5 min in practice). DKIM verification in GHL: up to 48 h worst case, usually 15 min – 4 h.

**Verification steps:**

```bash
# Run from firm's IT workstation or from NeuronX side after DNS push
dig +short apply.maplecrestimmigration.ca
# Expected: viewer-production-366c.up.railway.app (CNAME chain)

dig +short cases.maplecrestimmigration.ca
# Expected: neuronx-production-62f9.up.railway.app

dig +short mg.maplecrestimmigration.ca MX
# Expected: mxa.mailgun.org, mxb.mailgun.org (priority 10)

dig +short mg.maplecrestimmigration.ca TXT
# Expected: v=spf1 include:spf.leadconnectorhq.com include:mailgun.org ~all

dig +short mailo._domainkey.mg.maplecrestimmigration.ca TXT
# Expected: DKIM public key provided by GHL on domain add
```

**Failure modes if DNS is misconfigured:**

| Misconfig | Symptom | Fix |
|-----------|---------|-----|
| CNAME target typo | Form URL 404/SSL error | Correct CNAME, wait 5–15 min |
| Cloudflare proxy ON (orange cloud) for Railway CNAME | Railway-issued SSL fails; users see CF edge cert mismatch | Set to "DNS only" (grey cloud) |
| Missing SPF on `mg` | Outbound emails marked spam / hard-bounced at Gmail | Add TXT `v=spf1 include:spf.leadconnectorhq.com include:mailgun.org ~all` |
| DKIM not published | GHL shows "Verification pending" indefinitely | Paste DKIM TXT exactly as GHL provides (quotes + length) |
| DMARC too strict (`p=reject`) before DKIM verifies | Legit outbound mail rejected | Start with `p=none`; tighten to `p=quarantine` only after 14 days of clean DMARC reports |

### Scenario B — Firm doesn't own a domain

**Recommended default: Tier 1** — provide `{firm-slug}.neuronx-clients.co` on a NeuronX-owned domain we pre-register.

**Action:** register `neuronx-clients.co` (separate from `neuronx.co` so agency marketing stays clean) on Cloudflare. Pre-provision a wildcard CNAME so we can add firms via API without touching DNS per-firm.

```
# On neuronx-clients.co zone (one-time setup)
CNAME  *                viewer-production-366c.up.railway.app   DNS only  Auto TTL
# Wildcard — every {anything}.neuronx-clients.co resolves here
```

Then a new firm gets `maplecrest.neuronx-clients.co` with zero DNS work. Cases and email still fall back to `cases.neuronx.co` / `mg.neuronx.co` (shared) until they upgrade to Tier 2.

**Fallback: recommend they buy a domain.** .ca domains via Cloudflare Registrar ~$10 CAD/yr. Script the ask in onboarding email. Most firms prefer this.

---

## Section 3 — GHL Custom Domain Setup (Funnels, Calendars)

GHL supports customer-branded:
- **Funnels** (landing / hire-us / thank-you pages)
- **Calendar booking pages** (`calendar.firmname.ca/intro-call`)
- **Email sender** (see Section 4)

GHL does **not** support custom domains for:
- Forms (but we don't use GHL forms — we use Typebot)
- Workflows (internal)
- Admin login (agency-wide white-label only)

### 3.1 Adding a custom domain to a GHL sub-account

**UI path** (no API — GHL custom domain add is UI-only, verified in `docs/03_infrastructure/ghl_capability_map.md`):

1. Agency view → pick sub-account (e.g., Maplecrest) → **Settings → Domains**.
2. Click **Add Domain**.
3. Enter: `hire.maplecrestimmigration.ca` (or `book.`, `apply.` — any subdomain the firm will use for a funnel).
4. GHL shows the CNAME target — typically `sites.ludicrous.cloud` for our white-labeled agency (agency white-label host from PROJECT_MEMORY).
5. Firm's DNS admin adds:
   ```
   Type   Name    Content                  TTL    Proxy
   CNAME  hire    sites.ludicrous.cloud    Auto   DNS only
   ```
6. Back in GHL: click **Verify** → typically 1–5 min.
7. Assign a funnel to that domain: Funnels → Settings → **Domain** → pick `hire.maplecrestimmigration.ca`.

### 3.2 SSL cert provisioning

Automatic via GHL (Let's Encrypt under the hood). Requires:
- CNAME must be live before you click Verify (otherwise cert request fails and is rate-limited — wait 1 h between retries).
- Cloudflare proxy **must be off** ("DNS only" grey cloud). If proxy is on, GHL can't issue the cert because CF intercepts ACME HTTP-01 challenge.

### 3.3 Path-based routing on the firm's root domain

**Question:** can `maplecrestimmigration.ca/hire-us` go to GHL while `maplecrestimmigration.ca/about` stays on their WordPress?

**Answer: not natively.** A domain is owned by one host. Three workarounds:

| Workaround | Difficulty | Recommendation |
|------------|-----------|----------------|
| Subdomain (`hire.firm.ca`) instead | Trivial | **Default — do this.** |
| Cloudflare Worker or Page Rule with path-based reverse proxy | Medium | Only if firm insists on root-domain path |
| Move firm's marketing site fully to GHL | Hard | Only if firm wants us to own their whole web presence |

**Our policy:** we offer **subdomains only**. If they want `maplecrestimmigration.ca/hire-us` on the root, they add a Cloudflare Worker themselves (out of our support scope) or redirect to `hire.maplecrestimmigration.ca`.

---

## Section 4 — Email Sender Domain Per Firm

### 4.1 Tiers

| Tier | Sender | Firm sees | Inbox sees (From) | Our cost |
|------|--------|-----------|-------------------|----------|
| 1 shared | `mg.neuronx.co` (our agency) | "via neuronx.co" footer in Gmail | `noreply@mg.neuronx.co` on behalf of firm | Zero — uses existing SPF/DKIM |
| 2 custom | `mg.firmname.ca` | Clean Gmail — no "via" | `noreply@mg.firmname.ca` | 1 hour of DNS work with firm |

Tier 1 is fine for the first 2 weeks while the firm gets DNS set up. Don't send >500 emails/day/firm on shared — Gmail starts to group them.

### 4.2 Step-by-step: Tier 2 custom email sender

**Prerequisites:** firm has a GHL sub-account and access to their DNS provider (ideally Cloudflare).

**Step 1 — GHL sub-account → Settings → Email Services → Dedicated Domain**

1. Enter `mg.firmname.ca`.
2. GHL returns **5 DNS records**:

| # | Type | Name | Value (example — GHL will give exact values) |
|---|------|------|----------------------------------------------|
| 1 | MX | `mg` | `10 mxa.mailgun.org` |
| 2 | MX | `mg` | `10 mxb.mailgun.org` |
| 3 | TXT | `mg` | `v=spf1 include:spf.leadconnectorhq.com include:mailgun.org ~all` |
| 4 | TXT | `mailo._domainkey.mg` | `k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...` *(GHL provides full key)* |
| 5 | CNAME | `email.mg` | `mailgun.org` *(tracking pixel and bounce webhooks)* |

**Step 2 — Firm's DNS admin adds records**

Exact Cloudflare UI sequence:
1. Log in to Cloudflare → select `firmname.ca` zone → **DNS → Records → Add record**.
2. For each row above, paste exactly. **Proxy status: DNS only** (grey cloud) for all 5 records. TTL: Auto.
3. Save.

**Step 3 — Verify in GHL**

- Wait 10–15 min (Cloudflare is fast).
- GHL → Domains → click **Verify** next to `mg.firmname.ca`.
- Expected flags: SPF ✅, DKIM ✅, MX ✅.
- If DKIM is ❌ after 30 min: re-check TXT record value — common failure is Cloudflare auto-wrapping the key at 255 chars (GHL expects exact TXT string).

**Step 4 — Register on Gmail Postmaster Tools (strongly recommended)**

1. `https://postmaster.google.com/` → Add Domain → `mg.firmname.ca`.
2. Add TXT verification record in Cloudflare (Postmaster provides).
3. Wait 24–48 h for first reputation data.
4. Monitor weekly during first month. Target: Domain reputation = High, Spam rate < 0.1%.

**Step 5 — DMARC (after 14 days of clean sending)**

Start with monitoring only:
```
Type  Name     Value
TXT   _dmarc   v=DMARC1; p=none; rua=mailto:dmarc@firmname.ca; fo=1
```

After 14 days of zero DMARC failures in the `rua` reports, tighten to:
```
TXT   _dmarc   v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc@firmname.ca
```

Never jump straight to `p=reject` — one misconfig and legit mail bounces for 24–48 h.

---

## Section 5 — Typebot Form → Custom Domain

### 5.1 Current flow (VMC today)

```
User → www.neuronx.co/intake/vmc/onboarding
        │
        ▼  (Vercel rewrite rule)
    Railway FastAPI /form/vmc/onboarding
        │
        ▼  (server returns HTML with Typebot iframe embed)
    viewer-production-366c.up.railway.app  (Typebot Viewer)
```

### 5.2 Options for per-firm branded form URL

| Option | Example | Effort | Maintenance | Verdict |
|--------|---------|--------|-------------|---------|
| **A. Per-firm Vercel proxy** | `apply.firm.ca` → Vercel project per firm with rewrites | High — new Vercel project per firm | Bad — 50 firms = 50 projects | ❌ Reject |
| **B. GHL funnel with Typebot iframe** | `hire.firm.ca` → GHL funnel with `<iframe src=viewer...>` | Medium | Good — GHL manages SSL | ⚠️ Works but loses Typebot features (prefill via URL params gets awkward across iframe boundary) |
| **C. Separate Vercel deploy per firm** | Copy whole `neuronx-web` per firm | Very high | Terrible | ❌ Reject |
| **D. Railway CNAME with path-based routing** | `apply.firm.ca` CNAME → `viewer-production-366c.up.railway.app`; FastAPI serves `/intake/{firm_slug}/onboarding`; Typebot Viewer manages SSL | Low — one CNAME per firm | Excellent — slug-based routing already exists in `/form/{tenant}/{slug}` | ✅ **Recommended** |

### 5.3 Recommended: Option D

**Why:** we already have multi-tenant routing in FastAPI (`/form/{tenant}/{slug}` per `PROJECT_MEMORY.md:117`). Typebot Viewer on Railway issues its own Let's Encrypt cert for any CNAME pointed at it. Zero new infra.

**One catch:** `viewer-production-366c.up.railway.app` is Typebot's viewer, not our FastAPI. Two sub-options:

- **D1 (preferred):** Point firm's CNAME at **Typebot Viewer** and embed via Typebot's native domain support. Each firm gets a separate Typebot instance (copy of the VMC bot) with `publicId = {firm-slug}-onboarding`. Typebot natively supports custom domain per bot.
- **D2:** Point firm's CNAME at **our FastAPI** (`neuronx-production-62f9.up.railway.app`). FastAPI resolves the Host header to a tenant, returns the right HTML template with Typebot iframe. More control, but we manage SSL + edge.

**Recommendation: start with D1** (simpler, Typebot handles SSL). Migrate to D2 only if we need server-side logic before showing the form (e.g., pre-auth, feature-gating).

### 5.4 Migration steps (current VMC → Option D1 blueprint)

1. In Typebot Builder: duplicate `vmc-onboarding` → rename `{firm-slug}-onboarding`.
2. Typebot Viewer → Settings → **Custom Domain** → enter `apply.firm.ca`.
3. Firm adds DNS:
   ```
   CNAME  apply   viewer-production-366c.up.railway.app   DNS only
   ```
4. Wait 5–15 min → Typebot auto-issues SSL.
5. Webhooks: ensure each bot's webhook → `neuronx-production-62f9.up.railway.app/typebot/webhook` carries `tenant_slug` so FastAPI routes to the right GHL sub-account.
6. Update firm's onboarding email with `https://apply.firm.ca`.

---

## Section 6 — Case Viewer URL Per Firm

Today: `neuronx-production-62f9.up.railway.app/cases/{id}/viewer`.

| Option | Pro | Con | Verdict |
|--------|-----|-----|---------|
| **A. `cases.firm.ca` → CNAME → our Railway** | Full brand, clean URL; Railway auto-issues SSL per CNAME | FastAPI must resolve Host → tenant (small code change) | ✅ **Recommended for Tier 2** |
| **B. GHL funnel embeds iframe of our viewer** | No DNS work by firm | Iframe feels hacky; mobile scroll issues; can't deep-link `?highlight=doc123` | ⚠️ Emergency fallback |
| **C. Keep raw Railway URL** | Zero work | Looks unprofessional; clients screenshot URL and it confuses them | ⚠️ Tier 0/1 only |

### 6.1 Implementation for Option A

1. Firm adds:
   ```
   CNAME  cases   neuronx-production-62f9.up.railway.app   DNS only
   ```
2. Railway dashboard → `neuronx-api` service → **Settings → Domains → Custom Domain** → add `cases.firm.ca` → Railway gives a verification TXT (one-time).
3. Firm adds the verification TXT. Railway auto-issues SSL in ~5 min.
4. FastAPI middleware: if `request.headers["host"]` is `cases.firm.ca`, set `tenant_slug=firm-slug` in request state. Existing `/cases/{id}/viewer` renders with firm branding (logo/color from `config/tenants.yaml`).

**Code change needed** (out of scope for this doc — see `neuronx-api/middleware/tenant_resolver.py` task): add host→tenant map. Keep as YAML so ops can edit without deploy.

---

## Section 7 — Onboarding Automation (Runbook)

**Trigger:** Stripe webhook `checkout.session.completed` for NeuronX subscription product.

**End state:** firm has a working GHL sub-account, Twilio number, custom domain, and first automated "you're live" email has been sent.

### 7.1 Runbook steps

| # | Step | Automated? | Owner | Detail |
|---|------|-----------|-------|--------|
| 1 | Stripe webhook → FastAPI `/webhooks/stripe` | ✅ Auto | FastAPI | Parses firm metadata (name, domain, contact email) |
| 2 | Create GHL sub-account | ✅ Auto | FastAPI → GHL SaaS API | `POST /locations` with agency PIT; returns new `location_id` |
| 3 | Install snapshot | ⚠️ Semi | FastAPI → GHL | Snapshot install API if ready; else operator triggers manually |
| 4 | Assign Twilio phone number | ✅ Auto | FastAPI → GHL LC Phone API | Searches local area code, purchases number, assigns to sub-account |
| 5 | Generate DNS setup email | ✅ Auto | FastAPI | Renders `templates/dns_setup_email.md` with exact records (Section 8 template) |
| 6 | Send DNS setup email | ✅ Auto | FastAPI → SMTP | Use Postmark transactional (not GHL — firm isn't set up yet) |
| 7 | Wait for firm's DNS | ⏳ Poll | FastAPI cron | Every 15 min: `dig` firm's `apply.` and `mg.` subdomains |
| 8 | Verify DKIM in GHL | ✅ Auto | FastAPI → GHL Domain Verify API | When DKIM TXT visible, POST verify |
| 9 | Activate email sender | ✅ Auto | FastAPI | Sets `from_email = noreply@mg.firm.ca` in tenant config |
| 10 | Send "you're live" email | ✅ Auto | FastAPI → GHL email (now using firm's own sender) | Includes their branded form URL |
| 11 | Escalate if DNS not added in 48 h | ✅ Auto | FastAPI | Slack alert to ops; email firm with reminder |
| 12 | Manual: training call booked | ❌ Manual | Sales/CS | Calendly link in welcome email |

### 7.2 Cron job spec (DNS verifier)

```python
# neuronx-api/jobs/dns_verifier.py  — runs every 15 min
# For each tenant with status="awaiting_dns":
#   1. dns.resolver.resolve(f"apply.{tenant.domain}", "CNAME")
#   2. Check target matches expected viewer host
#   3. dns.resolver.resolve(f"mg.{tenant.domain}", "MX")
#   4. If MX matches mailgun → trigger GHL DKIM verify endpoint
#   5. On full pass, transition tenant.status → "active"
#   6. Write activity row to PostgreSQL
```

Escalation ladder:
- 24 h no DNS → gentle email
- 48 h no DNS → Slack alert + phone call from CS
- 7 days no DNS → pause billing, hand to sales

---

## Section 8 — DNS Record Templates (Copy-Paste for Customer)

### 8.1 Full Tier 2 template (Cloudflare-style)

Give this table to the firm's IT/admin as-is. Every row has a purpose column so they know **why**, reducing support tickets.

```
Type  | Name                  | Content                                             | TTL  | Proxy     | Purpose
------|-----------------------|-----------------------------------------------------|------|-----------|---------------------------------------------
CNAME | apply                 | viewer-production-366c.up.railway.app               | Auto | DNS only  | Typebot-hosted intake form (branded)
CNAME | cases                 | neuronx-production-62f9.up.railway.app              | Auto | DNS only  | Case viewer (PostgreSQL-backed)
CNAME | hire                  | sites.ludicrous.cloud                               | Auto | DNS only  | GHL funnel (retainer + booking)
MX    | mg                    | mxa.mailgun.org (priority 10)                       | Auto | N/A       | Email receive (bounce handling)
MX    | mg                    | mxb.mailgun.org (priority 10)                       | Auto | N/A       | Email receive (redundant MX)
TXT   | mg                    | v=spf1 include:spf.leadconnectorhq.com include:mailgun.org ~all | Auto | DNS only  | SPF — authorizes GHL + Mailgun to send from mg.firm.ca
TXT   | mailo._domainkey.mg   | (GHL provides on domain add — paste exactly)        | Auto | DNS only  | DKIM — cryptographic signature for outbound mail
CNAME | email.mg              | mailgun.org                                         | Auto | DNS only  | Open/click tracking + bounce webhooks
TXT   | _dmarc                | v=DMARC1; p=none; rua=mailto:dmarc@firm.ca; fo=1    | Auto | DNS only  | DMARC in monitoring mode (upgrade after 14 days)
```

**After 14 days of clean DMARC reports**, upgrade the `_dmarc` record:
```
TXT   | _dmarc                | v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc@firm.ca
```

### 8.2 Record-by-record explainer (for the firm's IT)

- **`apply` CNAME** — Typebot Viewer hosts the form. Typebot auto-issues SSL for any CNAME pointing at it. Must be "DNS only" (not Cloudflare-proxied) or cert issuance fails.
- **`cases` CNAME** — Our FastAPI resolves the Host header to your tenant and renders case viewer. Railway auto-issues SSL.
- **`hire` CNAME** — GHL-hosted funnel for retainer signing, booking, thank-you page. GHL issues SSL after click-Verify.
- **`mg` MX x2** — Mailgun's two MX servers. Priority 10 on both = equal preference (round-robin). Without these, bounces and unsubscribes don't reach us.
- **`mg` SPF TXT** — Says "GoHighLevel and Mailgun are allowed to send email claiming to be from `mg.firm.ca`." Without this, Gmail marks outbound mail as spoofing.
- **`mailo._domainkey.mg` DKIM TXT** — Public key. GHL/Mailgun signs outbound mail with the matching private key. Receivers verify the signature. Without this, Gmail shows a yellow "unverified sender" warning.
- **`email.mg` CNAME** — Mailgun's link-wrapping host for open/click tracking and bounce webhooks. Required for analytics.
- **`_dmarc` TXT** — Policy for what to do with email that fails SPF+DKIM. `p=none` = just monitor (safe default).

### 8.3 Registrar-specific notes

| Registrar / DNS | Gotcha |
|-----------------|--------|
| Cloudflare | Wildcard proxy is orange by default — **toggle off** for Railway/Typebot CNAMEs |
| GoDaddy | TXT records auto-add trailing dot — usually fine but check DKIM verification |
| Namecheap (BasicDNS) | MX priority field is separate from value — enter `10` in priority, `mxa.mailgun.org` in value |
| Google Domains (now Squarespace) | DKIM TXT > 255 chars gets split into chunks — concatenate in DNS provider, not in the record |
| Route 53 | Values auto-quoted for TXT — don't add extra quotes |

---

## Section 9 — Migration & Rollback

### 9.1 Firm leaves (churn) — remove custom domain

**Goal:** stop serving their branded URLs cleanly within 24 h of cancellation, without breaking in-flight client interactions.

1. **Day 0 (cancellation):** Set tenant `status=cancelled` in `config/tenants.yaml`. FastAPI returns 410 Gone + explainer page for new requests on `apply.firm.ca` and `cases.firm.ca`.
2. **Day 0–7:** Send farewell email from `mg.firm.ca` with: "download your case data, export cadence, our service ends on [Day 30]".
3. **Day 30:** Ask firm to remove the CNAMEs from their DNS. If they don't:
   - Remove their custom domain from Railway + Typebot dashboards (Railway will stop serving certs — subdomain returns SSL error, which is fine because cancelled firm).
   - Remove from GHL domain list (sub-account still exists in suspended state for 90 days per GHL retention).
4. **Day 90:** Hard-delete sub-account via GHL API. Data export file (SQL dump + JSON blobs) delivered to firm via secure link.

### 9.2 Firm rebrands / changes primary domain

Example: Maplecrest rebrands to Apex Immigration → `apeximmigration.ca`.

1. Add new CNAMEs on new domain (Section 8 template).
2. Verify new domain works end-to-end (test submission on `apply.apeximmigration.ca`).
3. Set up 301 redirects on old domain: `apply.maplecrestimmigration.ca` → `apply.apeximmigration.ca` (either at Cloudflare Page Rule or via a Railway middleware that reads the tenant config `legacy_hosts: [maplecrest...]`).
4. Keep old sender `mg.maplecrestimmigration.ca` active for 90 days so reply-to threads survive.
5. Switch default sender in GHL to `mg.apeximmigration.ca` at Day 7.
6. Remove old domain records at Day 90.

### 9.3 What breaks if a DNS record is deleted accidentally

| Record deleted | Effect | Time to notice | Recovery |
|---------------|--------|----------------|----------|
| `apply` CNAME | New form submissions fail — `SSL_ERROR` or `NXDOMAIN` in browser | Minutes (user complaints) | Re-add CNAME; cert issues in ~5 min |
| `cases` CNAME | Clients can't view their case portal | Minutes | Re-add CNAME; SSL in ~5 min |
| `mg` MX | Email bounces stop flowing back — GHL shows "delivered" but real bounces are silent | Hours (inbox warnings on firm's end) | Re-add MX; propagation 5–60 min |
| `mg` SPF TXT | Outbound mail marked spam at Gmail — open rate craters within hours | 2–24 h (analytics dip) | Re-add SPF; Gmail reputation recovers in 24–48 h |
| DKIM TXT | Same as SPF, plus "unverified sender" warning | Hours | Re-add DKIM; propagation 5 min – 4 h |
| `hire` CNAME (GHL funnel) | Booking/retainer pages dead | Minutes | Re-add CNAME; re-verify in GHL (manual click) |
| `_dmarc` TXT | Quiet monitoring gap — no functional impact unless you were at `p=quarantine/reject` | Days | Re-add |

### 9.4 Rollback checklist (keep with each tenant in `config/tenants.yaml`)

```yaml
maplecrest:
  primary_domain: maplecrestimmigration.ca
  branded_hosts:
    form: apply.maplecrestimmigration.ca
    cases: cases.maplecrestimmigration.ca
    funnel: hire.maplecrestimmigration.ca
    sender: mg.maplecrestimmigration.ca
  rollback:
    form_fallback: www.neuronx.co/intake/maplecrest/onboarding  # Tier 0 fallback
    cases_fallback: neuronx-production-62f9.up.railway.app/cases/{id}/viewer
    sender_fallback: mg.neuronx.co
  created_at: 2026-04-18
  status: active  # active | awaiting_dns | cancelled | suspended
```

If anything breaks, flip `branded_hosts` → `rollback.*_fallback` in tenant config. FastAPI + email send both pick up new config within one request cycle (YAML hot-reload or restart).

---

## Appendix A — Quick Reference: Time Budgets

| Activity | Time | Blocker |
|----------|------|---------|
| Add CNAME in Cloudflare | 1–2 min | Firm's DNS admin access |
| Cloudflare DNS propagation | 1–5 min | DNS TTL |
| Non-Cloudflare DNS propagation | 15 min – 1 h | DNS TTL on firm's provider |
| Railway SSL issuance | 3–10 min | CNAME must be live first |
| Typebot Viewer SSL issuance | 3–10 min | Same |
| GHL funnel SSL issuance | 3–10 min | Same; Cloudflare proxy must be OFF |
| GHL DKIM verification | 15 min – 48 h | DNS propagation + GHL poll interval |
| Gmail Postmaster Tools data | 24–72 h | Google's own cadence |
| DMARC first aggregate report | 24 h | Google's cadence |

## Appendix B — Emergency Contacts

| Scenario | First escalation |
|----------|------------------|
| DNS changes not propagating after 4 h | Firm's registrar support |
| Railway SSL stuck "pending" | Railway Discord `#help` |
| GHL DKIM stuck "pending" | GHL support ticket + retry via agency UI |
| Typebot custom domain broken | Typebot GitHub issues or ops rotates CNAME off/on |
| Gmail-wide deliverability drop | Check Google Postmaster Tools; pause sending; contact Mailgun support |

---

## Appendix C — Glossary

- **SPF (Sender Policy Framework)** — DNS TXT record listing authorized senders for a domain.
- **DKIM (DomainKeys Identified Mail)** — Cryptographic signature on outbound mail; public key in DNS.
- **DMARC (Domain-based Message Authentication)** — Policy layered on top of SPF + DKIM telling receivers what to do with failures.
- **CNAME** — DNS alias: "this hostname points at that hostname."
- **MX** — Mail exchanger: where mail for this domain is delivered.
- **PIT (Private Integration Token)** — GHL's non-OAuth API token, location-scoped.
- **Tier 0/1/2/3** — NeuronX branding levels (see top of doc).
- **"DNS only" (Cloudflare grey cloud)** — CF serves DNS but doesn't proxy traffic; required for origins (Railway, Typebot, GHL) that issue their own SSL.

---

**End of playbook.**
**Owner to refresh quarterly.** Re-verify Section 1.1 DNS records with `dig` before publishing any update. Contact infra owner before changing Tier semantics.
