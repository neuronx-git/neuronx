# 🚀 NeuronX Production Readiness — Master PM Document

**Last updated:** 2026-04-18 (after 4-agent parallel research)
**Owner:** PM lead (Claude) + founder (Ranjan)
**Status:** v0.5.0 live + 2 P0 fixes deployed. Investor-demo-ready. Pilot-customer-ready pending 5 blockers.

---

## 📊 One-Page Summary

### What's done (green)
- ✅ Production GHL live: VMC + NeuronX agency + 9-person firm team + 3 shared calendars + 140 fields + 120 tags
- ✅ 26 premium email templates uploaded + renamed to workflow names (WF-01…WF-CP-09)
- ✅ Email stack production-grade: SPF/DKIM/DMARC/Postmaster all verified on `mg.neuronx.co`
- ✅ Case lifecycle API: 10-stage state machine, users FK, Metabase views
- ✅ Case documents viewer UI at `/cases/{id}/viewer` (one-link RCIC view)
- ✅ Demo dataset: 35 contacts, 15 cases, $48.5K simulated revenue
- ✅ Metabase: 3 dashboards + 10 SQL views populated
- ✅ 788+ tests (+ 42 new from users FK + viewer UI)
- ✅ Just-fixed P0 bugs: `/cases/list` 500, typebot webhook drop (commit `4462ef6`)

### What's blocking pilot customer (red)
1. **Documents storage layer** — Typebot uploads are OCR'd then lost (no SeaweedFS/S3 wired)
2. **Workflow email text** → template linking (24 workflows use inline text, not our 26 premium templates)
3. **Stripe verification** — "unverified" warning; need public pages + incorporation docs
4. **No SaaS signup funnel** on neuronx.co (Journey 1 fully broken)
5. **VAPI PIPEDA disclosure** missing in `firstMessage` (compliance gap)

---

## 🎯 4-Agent Research Synthesis

### 🔴 Agent B — Golden Journeys Audit
**Doc:** `docs/06_execution/GOLDEN_JOURNEYS_AUDIT.md`
**Verdict:** 7 journeys tested. 1 broken (❌ J1 SaaS signup), 5 partial (⚠️), 1 mostly-working (✅ J7 investor demo).

| Journey | Health | Top blocker |
|---|---|---|
| J1 SaaS signup (firm buys NeuronX) | ❌ | No funnel, no Stripe, no auto-provisioning |
| J2 End-user inquiry | ⚠️ | Typebot webhook dropped new contacts (✅ now fixed) |
| J3 Consult → Retainer | ⚠️ | Documenso not wired |
| J4 Case processing | ⚠️ | `/cases/list` 500 (✅ now fixed) |
| J5 RCIC daily | ⚠️ | users table empty (run `POST /users/sync-from-ghl`), Chrome ext not on GHL domain |
| J6 PIPEDA compliance | ⚠️ | No 30-day deletion job |
| J7 Investor demo | ✅ | Analytics has stale sandbox pipeline ID |

### 📞 Agent C — Telephony Setup
**Doc:** `docs/03_infrastructure/TELEPHONY_SETUP.md` (505 lines)
**Decisions:**
- **Winner:** GHL LC Phone (one Canadian local DID per firm). Import same DID into VAPI via BYOC for AI intake.
- **Current VAPI numbers:** `+1 647-931-5181` (keep, primary VMC), `+1 447-766-9795` (retire, no production role).
- **Compliance blocker:** CA carriers block unregistered A2P SMS in 2026. Register VMC brand: $4 sole-prop or $44 standard + $15/campaign + $1.50-10/mo.
- **VAPI `firstMessage` missing PIPEDA disclosure** — fix this week.
- **50-firm unit economics:** COGS $31/firm/mo, revenue $50/firm, 38% gross margin.

### 💰 Agent D — Stripe + SaaS Pricing
**Doc:** `docs/03_infrastructure/STRIPE_SAAS_PRICING.md` (520 lines)
**Pricing revision:**
| Tier | Old | New | Why |
|---|---|---|---|
| Starter | $500 | **$497/mo** | $997 SaaS anchor psychology |
| Growth | $1,000 | **$997/mo** | Below Clio Essentials, AI voice edge |
| Scale | $1,500 | **$1,997/mo** | Industry norm |
| Enterprise | — | **$2,997+ custom** | — |
| Setup fee | — | **$1,500 one-time** | Waived on annual G/S |
| Annual discount | — | **17% (2 months free)** | — |
| Trial | — | **14 days Starter only, no CC** | Demo-gate G/S |

**Stripe blockers before selling:**
1. Publish `/pricing`, `/terms`, `/privacy`, `/refund-policy` on neuronx.co — Stripe reviews site
2. Submit: Articles of Incorporation + CRA Business Number + void cheque + photo ID
3. Register GST/HST voluntarily NOW (reclaim input tax credits on Railway/GHL/VAPI)
4. Upgrade to GHL SaaS Pro ($497/mo agency level) for rebilling with markup
5. Generate Agency-level API key (not PIT) for `/saas-api/public-api/*`

**COGS realistic margins:** Starter 69% ✅, Growth 49% (60-65% realized), Scale 36% (improves with stickiness).

### 🌐 Agent E — Domain + DNS Customer Onboarding
**Doc:** `docs/03_infrastructure/DOMAIN_DNS_CUSTOMER.md` (537 lines)
**4-tier domain model:**
- **Tier 0** (0 min): Firm uses our shared `mg.neuronx.co` sender + `forms.neuronx.co/{firm-slug}`
- **Tier 1** (5 min): Wildcard `{firm-slug}.neuronx-clients.co` — zero DNS on firm's side (requires we buy this domain)
- **Tier 2** (30 min config + 48h DKIM): Firm's own `mg.firmdomain.ca` + `forms.firmdomain.ca`
- **Tier 3** (60-90 min + 72h SSL): Full white-label including case viewer `cases.firmdomain.ca`

**Key recommendations:**
- **Subdomains only, not root-path routing** — avoids per-firm Cloudflare Workers
- **Typebot per-firm bot** (Option D1) with CNAME from `apply.firmdomain.ca`
- **Case viewer** (Option A): `cases.firmdomain.ca` → Railway CNAME with Host→tenant middleware
- **Buy domain:** `neuronx-clients.co` for Tier 1 wildcard hosting
- **DMARC upgrade path:** `p=none` → `p=quarantine` after 14 days of clean reports

---

## 🎯 Prioritized Action List (PM-curated)

### 🔴 P0 — This week (investor-demo blockers)
| # | Action | Owner | Est | Blocker for |
|---|---|---|---|---|
| 1 | Verify P0 bugs deployed (`/cases/list`, typebot fallback) | Me | 5 min | Journey 2, 4, 5 |
| 2 | Run `POST /users/sync-from-ghl` to populate users table | Me | 2 min | Journey 5, Metabase |
| 3 | Add PIPEDA disclosure to VAPI `firstMessage` | Founder | 10 min UI | Compliance |
| 4 | Fix stale analytics pipeline ID in `/analytics/pipeline` | Me | 15 min | Journey 7 demo |
| 5 | Extract workflow email text via Claude-in-Chrome | Me + founder | 20 min | Path to blocker #6 |
| 6 | Rebuild 26 templates with founder's actual text + VMC logo | Me | 1 hr | Workflow emails |
| 7 | Link 26 templates → 24 GHL workflow Send Email actions | Me + founder via Chrome | 30 min | Email delivery |

### 🟡 P1 — Next 2 weeks (pilot-customer ready)
| # | Action | Owner | Est | Source |
|---|---|---|---|---|
| 8 | Build documents table + SeaweedFS container on Railway | Dev | 1 day | Agent B + prior audit |
| 9 | Publish `/pricing`, `/terms`, `/privacy`, `/refund-policy` on neuronx.co | Me + founder | 3 hr | Agent D (Stripe gate) |
| 10 | Submit Stripe verification docs | Founder | 30 min + 2-5 biz days | Agent D |
| 11 | Register GST/HST voluntarily | Founder | 1 hr + 2 weeks | Agent D |
| 12 | A2P 10DLC brand registration for VMC | Founder | 30 min + 1-2 weeks | Agent C |
| 13 | Integrate Docuseal container for retainer e-sig | Dev | 4 hr | OSS research |
| 14 | Build SaaS signup funnel on neuronx.co | Me | 1 day | Journey 1 |
| 15 | Buy `neuronx-clients.co` domain for Tier 1 wildcard | Founder | 5 min | Agent E |

### 🟢 P2 — Month 2 (scale enablers)
| # | Action | Owner | Est |
|---|---|---|---|
| 16 | PIPEDA 30-day deletion job (APScheduler) | Dev | 2 hr |
| 17 | Paperless-ngx container for OCR archive | Dev | 3 hr |
| 18 | Chrome extension auth + published to web store | Dev | 1 day |
| 19 | Family sponsorship upsell workflow | Dev | 2 hr |
| 20 | Upgrade DMARC `p=none` → `p=quarantine` | Founder | 5 min (after 14d) |
| 21 | Microsoft SNDS registration | Founder | 5 min |

---

## 📁 All Agent Outputs (for next session)

| File | Purpose | Lines |
|---|---|---|
| `docs/06_execution/GOLDEN_JOURNEYS_AUDIT.md` | 7-journey E2E audit with fix recs | ~400 |
| `docs/03_infrastructure/TELEPHONY_SETUP.md` | Phone + SMS buying/compliance playbook | 505 |
| `docs/03_infrastructure/STRIPE_SAAS_PRICING.md` | Stripe setup, pricing, tiers, margins | 520 |
| `docs/03_infrastructure/DOMAIN_DNS_CUSTOMER.md` | 4-tier domain playbook + runbook | 537 |
| `docs/03_infrastructure/OSS_BPM_RESEARCH.md` | Prior: open-source tool recommendations | 190 |
| `docs/06_execution/CASE_LIFECYCLE_AUDIT.md` | Prior: documents layer blockers | ~280 |
| `docs/06_execution/MANUAL_BUILD_CASE_PROCESSING.md` | Prior: (already executed) UI build guide | ~200 |
| `docs/06_execution/USER_JOURNEY_GAPS.md` | Prior: 42-step customer journey audit | ~300 |

**Total research output this session: ~2,900 lines of actionable documentation.**

---

## ✅ Definition of "investor demo ready"

Checkpoint test (run after P0 items 1-7 done):
1. Open Metabase Pipeline Health dashboard → shows $48.5K demo revenue, 11 cases across stages
2. Open GHL VMC Case Processing pipeline → drag a case card one stage → email fires with premium template
3. Open a case's viewer URL → shows timeline + doc grid + checklist
4. Send a test email from GHL → lands in Gmail Primary inbox, SPF/DKIM/DMARC all pass in headers
5. Submit test form on www.neuronx.co → receive VAPI AI call within 5 min → get confirmation email

If all 5 pass, we're demo-ready.

## ✅ Definition of "first paying customer ready"

Adds on top of demo-ready:
6. Stripe live + verified + connected to GHL SaaS Configurator
7. `/pricing` page public with "Start 14-day trial" button → Stripe checkout → auto-provisions sub-account
8. A2P 10DLC registered for SMS
9. At least one working document upload → retrieved by RCIC flow (blocker #8 delivered)
10. Docuseal wired for retainer e-sig

Target: 2-3 weeks from today.
