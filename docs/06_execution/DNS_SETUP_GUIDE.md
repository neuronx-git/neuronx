# NeuronX — DNS & White-Label Setup Guide

## Prerequisites
- NeuronX domain purchased (e.g., `neuronx.ai`)
- DNS managed via Cloudflare (recommended) or your registrar

---

## Step 1: Add Domain to Cloudflare (if not already)

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Click "Add a Site"
3. Enter your domain (e.g., `neuronx.ai`)
4. Select Free plan
5. Cloudflare will scan existing DNS records
6. Update nameservers at your registrar to Cloudflare's nameservers
7. Wait for propagation (up to 24 hours, usually 15 min)

---

## Step 2: Add All Required DNS Records

In Cloudflare DNS management, add these records:

### White-Label Records (GHL)

| Type | Name | Target | Proxy | Purpose |
|------|------|--------|-------|---------|
| CNAME | `app` | `msgsndr.com` | DNS only (gray) | GHL app login |
| CNAME | `api` | `api-white-label.msgsndr.com` | DNS only (gray) | GHL API |
| CNAME | `sites` | `sites-white-label.msgsndr.com` | DNS only (gray) | Funnels & sites |
| CNAME | `portal` | `msgsndr.com` | DNS only (gray) | Client portal |
| CNAME | `mail-link` | `email.msgsndr.com` | DNS only (gray) | Email tracking links |

### Email Records (Mailgun via GHL)

GHL will provide exact values when you add the email domain in Settings → Email Services.
Typical records:

| Type | Name | Value | Proxy | Purpose |
|------|------|-------|-------|---------|
| TXT | `mail` | `v=spf1 include:mailgun.org ~all` | N/A | SPF |
| TXT | `mailo._domainkey.mail` | (long DKIM key — copy from GHL) | N/A | DKIM |
| CNAME | `email.mail` | `mailgun.org` | DNS only | Tracking |
| MX | `mail` | `mxa.mailgun.org` (priority 10) | N/A | Inbound (optional) |
| MX | `mail` | `mxb.mailgun.org` (priority 10) | N/A | Inbound (optional) |

### VMC Funnel Domain (if using custom domain for funnel)

| Type | Name | Target | Proxy |
|------|------|--------|-------|
| CNAME | `intake.visamastercanada.com` | `sites.neuronx.ai` | DNS only |

**Note**: The VMC funnel domain CNAME points to your white-label sites domain.

---

## Step 3: Verify in GHL

After adding DNS records:

1. **Settings → White Label → Custom Domains**
   - Enter each domain (app.neuronx.ai, api.neuronx.ai, etc.)
   - Click "Verify" for each
   - Green checkmark = success

2. **Settings → Email Services**
   - Click "Verify Domain"
   - All records should show verified

3. **Sites → Funnels → Custom Domains** (for funnel domain)
   - Add `intake.visamastercanada.com`
   - Verify

---

## Important Notes

- **Cloudflare Proxy**: Set ALL GHL CNAME records to "DNS only" (gray cloud icon). Orange cloud (proxied) will break GHL's SSL.
- **Propagation**: CNAME records typically propagate in 5-15 minutes. TXT records may take up to 1 hour.
- **SSL**: GHL automatically provisions SSL certificates for verified custom domains. No manual SSL setup needed.
- **TTL**: Use "Auto" TTL in Cloudflare (default).
