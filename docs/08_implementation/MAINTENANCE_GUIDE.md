# NeuronX Maintenance Guide

**For**: Ranjan (Founder) + future team members
**Purpose**: How to maintain and customize every part of NeuronX without AI agent help

---

## Architecture Overview

```
NeuronX = 4 independent services + GHL

1. NeuronX API (Railway)     — scoring, briefings, form serving, webhooks
2. Typebot (Railway)          — form builder + viewer (7 services)
3. Marketing Website (Vercel) — neuronx.co
4. GHL (GoHighLevel)          — CRM, pipelines, workflows, email/SMS
5. VAPI                       — AI voice calling
```

Each is independent. Changing one doesn't break the others.

---

## How to: Edit Form Questions

**Tool**: Typebot Builder
**URL**: https://builder-production-6784.up.railway.app
**Login**: goldenphoenix1216@gmail.com (magic link via email)

1. Open Builder → click "VMC Client Onboarding"
2. Edit any group/block (drag-and-drop, click to edit text)
3. Click **Publish** (top right)
4. Changes are LIVE immediately at `/form/vmc/onboarding`
5. No code changes needed. No deployment needed.

**What lives where:**
- Question text, choices, branching logic → **Typebot Builder** (edit here)
- Colors, bot name, avatar → **tenants.yaml** (edit in code)
- Rendering behavior → **templates/form.html** (edit in code)

---

## How to: Add a New Client

**Time**: 5 minutes
**No code needed** — just YAML config

1. Edit `neuronx-api/config/tenants.yaml`
2. Add a new block:
```yaml
  acme-immigration:
    name: "Acme Immigration Services"
    slug: "acme-immigration"
    ghl_location_id: "NEW_GHL_LOCATION_ID"
    typebot_viewer_url: "https://viewer-production-366c.up.railway.app"
    branding:
      primary: "#2563EB"      # Client's primary color
      accent: "#10B981"       # Client's accent color
      background: "#F8FAFC"
      text_on_primary: "#FFFFFF"
      text_on_accent: "#FFFFFF"
      input_border: "#E2E8F0"
      input_focus: "#2563EB"
      font: "Inter, -apple-system, sans-serif"
    bot_name: "Acme Immigration Assistant"
    bot_status: "Online"
    avatar_url: "/static/avatars/acme.png"
    favicon_url: "/static/favicon.png"
    forms:
      onboarding:
        typebot_id: "acme-onboarding"
        title: "Immigration Assessment"
```
3. Create the Typebot form in Builder (or duplicate VMC's)
4. Upload client avatar to `neuronx-api/static/avatars/`
5. Push to GitHub → Railway auto-deploys
6. Form live at: `/form/acme-immigration/onboarding`

---

## How to: Change Client Branding (Colors, Bot Name)

**File**: `neuronx-api/config/tenants.yaml`

Edit the tenant's `branding` section, push to GitHub. Changes deploy in ~90 seconds.

---

## How to: Change NeuronX Website Content

**Location**: `neuronx-web/src/components/`

| Page Section | File | What to Edit |
|-------------|------|-------------|
| Navigation | `navbar.tsx` | Links, CTA text |
| Hero | `hero.tsx` | Headline, subheadline, stats |
| Social Proof | `social-proof.tsx` | Client names/logos |
| Features | `features.tsx` | Feature cards (title, description, icon) |
| How It Works | `how-it-works.tsx` | 5-step descriptions |
| Pricing | `pricing.tsx` | Tier names, prices, feature lists |
| FAQ | `faq.tsx` | Questions and answers |
| CTA | `cta.tsx` | Bottom CTA text, booking link |
| Footer | `footer.tsx` | Company info, links |

After editing, push to GitHub. If deployed on Vercel, it auto-deploys.

---

## How to: Change Scoring Rules

**File**: `neuronx-api/config/scoring.yaml`
Push → auto-deploys in 90 seconds. No code changes.

## How to: Change Immigration Programs

**File**: `neuronx-api/config/programs.yaml`
Push → auto-deploys in 90 seconds.

## How to: Change Compliance Rules

**File**: `neuronx-api/config/trust.yaml`
Push → auto-deploys in 90 seconds.

---

## How to: Deploy

### NeuronX API (Railway)
```
git push origin main
# Railway auto-deploys in ~90 seconds
# Verify: curl https://neuronx-production-62f9.up.railway.app/health
```

### Marketing Website (Vercel)
```
cd neuronx-web
npx vercel --prod
# Or: push to main branch → Vercel auto-deploys
```

### Typebot Forms
```
# No deployment needed — edit in Builder, click Publish, done
```

---

## Single Source of Truth

| What | Source of Truth | NOT the source |
|------|---------------|---------------|
| Form questions & logic | Typebot Builder (Railway) | JSON backup files |
| Client branding | `config/tenants.yaml` | Hardcoded in code |
| Scoring rules | `config/scoring.yaml` | Python code |
| GHL workflows | GHL UI | Documentation |
| GHL contacts | GHL API | PostgreSQL (sync copy) |
| Website content | `neuronx-web/src/` | Docs |
| NeuronX brand | `docs/08_implementation/BRAND_GUIDE.md` | APP/branding-kit.ts |

---

## Key URLs

| Service | URL | Purpose |
|---------|-----|---------|
| NeuronX API | neuronx-production-62f9.up.railway.app | Backend API |
| Typebot Builder | builder-production-6784.up.railway.app | Edit forms |
| Typebot Viewer | viewer-production-366c.up.railway.app | Form API |
| VMC Form | neuronx-api-url/form/vmc/onboarding | Client form |
| Metabase | metabase-production-1846.up.railway.app | Analytics |
| GHL Dashboard | app.gohighlevel.com | CRM |
| GitHub | github.com/ranjan-expatready/neuronx | Code |

---

## Backup Strategy

| What | How | Frequency |
|------|-----|-----------|
| Typebot form JSON | `config/typebot_templates/vmc_onboarding_branching.json` | After major changes |
| GHL Snapshot | GHL Agency → Snapshots | Before upgrades |
| Code | GitHub (auto) | Every push |
| PostgreSQL | Railway auto-backups | Daily |
