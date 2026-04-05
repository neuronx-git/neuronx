# NeuronX — $1M ARR Master Implementation Plan

**Version**: v1.0
**Date**: 2026-03-26
**Author**: AI Development Lead + Founder
**Status**: CANONICAL — All agents MUST read this at session start

---

## SITUATION ASSESSMENT (As of 2026-03-26)

### What We Have (Assets Built)
| Asset | Status | Location | Transferable? |
|-------|--------|----------|---------------|
| 98 Custom Fields | ✅ Created via API | GHL sandbox sub-account | ✅ Via Snapshot |
| 76 Tags (51 NX-prefixed) | ✅ Created via API | GHL sandbox sub-account | ✅ Via Snapshot |
| 9-Stage Pipeline | ✅ Created in UI | GHL sandbox sub-account | ✅ Via Snapshot |
| Calendar (Product Demo) | ✅ Configured via API | GHL sandbox sub-account | ✅ Via Snapshot |
| Inquiry Form V1 | ✅ Built in UI | GHL sandbox sub-account | ✅ Via Snapshot |
| Landing Page/Funnel V1 | ✅ Built in UI | GHL sandbox sub-account | ✅ Via Snapshot |
| 13 Workflows (WF-01→WF-11) | ✅ Published & Verified | GHL sandbox sub-account | ✅ Via Snapshot |
| VAPI Voice Agent | ✅ Configured | VAPI cloud (separate) | ✅ Independent |
| OAuth Marketplace App | ✅ Authorized | GHL Marketplace | ⚠️ Re-auth needed |
| Google Workspace (neuronx.co) | ✅ Active | Google Admin | ✅ Independent |
| Mailgun sending domain | ✅ mg.neuronx.co verified | GHL/Mailgun | ✅ Re-configure |
| Domain: neuronx.co | ✅ DNS managed in GHL | GHL Domain Purchase | ⚠️ Transfer needed |
| VMC Brand Kit + Templates | ✅ 7 email templates | GHL sandbox sub-account | ✅ Via Snapshot |
| PRD, Operating Spec, Trust Boundaries | ✅ Complete | /docs/ directory | ✅ Git repo |
| GHL Configuration Blueprint | ✅ Complete | /docs/ directory | ✅ Git repo |
| API Tooling (ghlProvisioner) | ✅ Working | /tools/ghl-lab/ | ✅ Git repo |
| FastAPI scaffold | ✅ Created (empty) | /neuronx-api/ | ✅ Git repo |

### What's Blocked by Sandbox
| Capability | Blocked? | Impact |
|------------|----------|--------|
| Email sending (all channels) | ❌ BLOCKED | Cannot test workflows, nurture sequences, email templates |
| LC Phone / SMS | ❌ BLOCKED | Cannot buy phone numbers, test voice/SMS flows |
| More than 2 sub-accounts | ❌ BLOCKED | Cannot onboard clients, cannot create test client accounts |
| SaaS Mode (client billing) | ❌ BLOCKED | Cannot auto-provision or bill clients |
| A2P 10DLC registration | ❌ BLOCKED | Cannot send compliant SMS at scale |
| Production API rate limits | ⚠️ REDUCED | 25 req/10s vs production limits |
| Data persistence guarantee | ⚠️ TEMPORARY | Sandbox data may be wiped; 6-month expiry |

### What Works in Sandbox (Continue Building)
| Capability | Works? | What to Do |
|------------|--------|-----------|
| Custom fields/tags (API) | ✅ YES | Continue refining |
| Pipeline stages (UI) | ✅ YES | Complete, refine |
| Calendar configuration (API) | ✅ YES | Done |
| Form/funnel builder (UI) | ✅ YES | Continue iterating |
| Workflow builder (UI) | ✅ YES | Refine triggers, test logic (no email/SMS send) |
| VAPI configuration | ✅ YES | Separate platform, independent |
| Snapshot creation | ✅ YES | CREATE NOW — protects all work |
| FastAPI development | ✅ YES | Build locally, no GHL dependency |
| Google Calendar sync | ✅ YES | Already connected |
| Contact creation (API) | ✅ YES | For testing pipeline flows |

---

## STRATEGIC DECISION: Sandbox-First Development

### The Mentor Strategy

**Principle**: Maximize sandbox value → minimize paid-plan burn rate → launch with confidence.

**Why this works**:
1. GHL snapshots are the official migration tool — everything transfers cleanly
2. VAPI, FastAPI, Google Workspace are independent of GHL billing
3. The only things that require a paid plan are: email/SMS sending, phone numbers, SaaS billing, and >2 sub-accounts
4. Every hour of development in sandbox = $0. Every hour on paid plan = $16.50/day ($497/30)

### The Timeline

```
PHASE 0: SANDBOX BUILD (Weeks 1-4) — $0/month GHL cost
├── Complete all configuration that doesn't require email/SMS/phone
├── Build FastAPI thin brain locally
├── Develop VAPI voice agent fully
├── Create production-ready snapshot
├── Research & lock GTM strategy
├── Identify & warm up pilot customer
└── Prepare onboarding playbook

PHASE 1: PRODUCTION LAUNCH (Week 5) — Start $297 or $497/month
├── Sign up via 30-day affiliate trial link
├── Import snapshot into production agency
├── Verify Stripe immediately
├── Buy phone number, register A2P
├── Send first test email
├── Full UAT (end-to-end)
└── If $297 plan: no SaaS mode, manual client onboarding
    If $497 plan: full SaaS mode, automated provisioning

PHASE 2: FIRST CUSTOMER (Week 6) — Revenue starts
├── Pilot customer onboarded
├── First consultation booked via NeuronX
├── First retainer signed
└── $1,500/month ARR begins
```

---

## PHASE 0: SANDBOX BUILD (Weeks 1-4)

### Week 1 (Mar 26 - Apr 1): Foundation Lock

| # | Task | Type | Can Do in Sandbox? | Owner |
|---|------|------|--------------------|-------|
| 0.1 | **CREATE SNAPSHOT NOW** | UI | ✅ | Founder |
| 0.2 | Resolve OD-13 (V1 tech boundary) → Lock Option A | Decision | ✅ | Founder |
| 0.3 | Complete Reply & Forward Settings (forwarding address, reply address) | UI | ✅ | Founder |
| 0.4 | Add phone to My Staff profile (+16479395000) | UI | ✅ | Founder |
| 0.5 | Configure Notification Settings (My Staff tab) | UI | ✅ | Founder |
| 0.6 | Fix form consent text | UI | ✅ | Founder |
| 0.7 | Add PROPOSAL SENT pipeline stage | UI | ✅ | Founder |
| 0.8 | Build Thank You page for form submission | UI | ✅ | Founder |
| 0.9 | Create RCIC survey template | UI | ✅ | Founder |
| 0.10 | Review & refine all 13 workflows (logic only, skip email/SMS actions) | UI | ✅ | AI + Founder |

### Week 2 (Apr 2 - Apr 8): FastAPI + Voice AI

| # | Task | Type | Can Do in Sandbox? | Owner |
|---|------|------|--------------------|-------|
| 0.11 | Build FastAPI webhook receiver (`/webhooks/ghl`) | Code | ✅ Local | AI |
| 0.12 | Build readiness scorer (`/score/lead`) | Code | ✅ Local | AI |
| 0.13 | Build consultation briefing generator (`/briefing/generate`) | Code | ✅ Local | AI |
| 0.14 | Build trust boundary enforcer (`/trust/check`) | Code | ✅ Local | AI |
| 0.15 | Build VAPI webhook handler (`/webhooks/voice`) | Code | ✅ Local | AI |
| 0.16 | Voice AI bake-off prep: GHL Voice AI vs VAPI comparison doc | Research | ✅ | AI |
| 0.17 | VAPI agent refinement (prompts, structured data extraction) | VAPI API | ✅ VAPI Cloud | AI |
| 0.18 | Design end-to-end data flow diagram | Doc | ✅ | AI |

### Week 3 (Apr 9 - Apr 15): Integration + GTM

| # | Task | Type | Can Do in Sandbox? | Owner |
|---|------|------|--------------------|-------|
| 0.19 | Voice AI bake-off execution (OD-01) | Test | ⚠️ Partial (VAPI yes, GHL voice no) | Founder decides |
| 0.20 | FastAPI ↔ GHL API integration testing (contacts, tags, opportunities) | Code + API | ✅ | AI |
| 0.21 | FastAPI ↔ VAPI integration testing | Code + API | ✅ | AI |
| 0.22 | Deploy FastAPI to Railway/Render (free tier) | Deploy | ✅ | AI |
| 0.23 | GTM Strategy document — complete research + write | Doc | ✅ | AI |
| 0.24 | Identify 5-10 warm pilot prospects (Canadian RCICs) | Research | ✅ | Founder |
| 0.25 | Begin warm outreach to pilot prospects | Manual | ✅ | Founder |
| 0.26 | Create onboarding playbook v1 | Doc | ✅ | AI |

### Week 4 (Apr 16 - Apr 22): Production Prep

| # | Task | Type | Can Do in Sandbox? | Owner |
|---|------|------|--------------------|-------|
| 0.27 | Create FINAL production snapshot (captures all Week 1-3 work) | UI | ✅ | Founder |
| 0.28 | Document snapshot contents checklist | Doc | ✅ | AI |
| 0.29 | Prepare production setup checklist (what to do Day 1 on paid plan) | Doc | ✅ | AI |
| 0.30 | Prepare Stripe verification documents | Prep | ✅ | Founder |
| 0.31 | Lock pricing tiers (OD-02) | Decision | ✅ | Founder |
| 0.32 | Lock deployment platform (OD-08) | Decision | ✅ | AI recommends |
| 0.33 | Secure 30-day free trial link (affiliate or direct from GHL) | Research | ✅ | Founder |
| 0.34 | Design client onboarding email sequence (drafts, not sent) | Doc | ✅ | AI |

---

## PHASE 1: PRODUCTION LAUNCH (Week 5)

### Day 1: Account Setup
| # | Task | Notes |
|---|------|-------|
| 1.1 | Sign up for GHL paid plan (use 30-day trial link) | $297/mo or $497/mo |
| 1.2 | Complete Stripe verification IMMEDIATELY | Business docs + bank account |
| 1.3 | Import production snapshot into new agency | Agency Dashboard → Account Snapshots → Import |
| 1.4 | Create NeuronX sub-account from snapshot | All config auto-deploys |
| 1.5 | Re-authorize OAuth Marketplace app | New tokens for new location |
| 1.6 | Transfer domain (neuronx.co) from sandbox → production | Use Domain Transfer-Out, then Transfer-In |
| 1.7 | Configure whitelabel domain (app.neuronx.co) | Company Settings → Whitelabel |
| 1.8 | Re-configure Mailgun (mg.neuronx.co) | Email Services → Dedicated Domain |
| 1.9 | Connect Google Workspace (ranjan@neuronx.co) | Integrations → Google |

### Day 2: Communication Channels
| # | Task | Notes |
|---|------|-------|
| 1.10 | Buy Toronto phone number (416/647) | Phone System → Buy Number |
| 1.11 | Register A2P 10DLC | Phone System → A2P Registration |
| 1.12 | Send test email from Conversations | Verify Mailgun working |
| 1.13 | Send test SMS | Verify LC Phone working |
| 1.14 | Update VAPI serverUrl to production FastAPI endpoint | VAPI Dashboard |
| 1.15 | Test outbound VAPI call | End-to-end voice test |

### Day 3-4: UAT
| # | Task | Notes |
|---|------|-------|
| 1.16 | UAT-01: Happy path (form → call → booking → briefing → retainer) | Full end-to-end |
| 1.17 | UAT-02: Complex case (refusal history → human escalation) | Trust boundary test |
| 1.18 | UAT-03: No-show → automated follow-up sequence | Workflow test |
| 1.19 | UAT-04: Disqualified lead → proper tagging + exit | Edge case |

### Day 5: SaaS Configuration (if on $497 plan)
| # | Task | Notes |
|---|------|-------|
| 1.20 | Configure SaaS pricing tiers in SaaS Configurator | Based on OD-02 decision |
| 1.21 | Create client snapshot (what clients get) | Subset of NeuronX snapshot |
| 1.22 | Set up Stripe Connect for client billing | SaaS Mode → Billing |
| 1.23 | Test client signup flow | Self-service or manual |
| 1.24 | Create VMC pilot sub-account from client snapshot | First real client deployment |

---

## PHASE 2: FIRST CUSTOMER (Week 6)

| # | Task | Notes |
|---|------|-------|
| 2.1 | Pilot customer identified and committed | From Week 3-4 outreach |
| 2.2 | Deploy VMC (or other pilot) sub-account | Snapshot-based deployment |
| 2.3 | Conduct onboarding call + training | Use onboarding playbook |
| 2.4 | First inquiry submitted via NeuronX form | Live traffic |
| 2.5 | First AI call executed | VAPI voice agent live |
| 2.6 | First consultation booked automatically | Calendar integration live |
| 2.7 | First retainer signed post-consultation | Revenue milestone |
| 2.8 | Collect NPS/feedback from pilot | Iterate product |

---

## DOMAIN STRATEGY

### neuronx.co — Current Situation
- **Purchased inside GHL sandbox** ($28.60 from wallet)
- **DNS managed in GHL** (Mailgun MX records, Google Workspace MX, CNAME for verification)
- **Can be transferred out** via GHL Domain Transfer-Out feature (after 60 days from purchase)

### Domain Migration Options

| Option | How | Risk | Recommendation |
|--------|-----|------|----------------|
| **A: Transfer domain out to Cloudflare** | GHL → Domain Transfer-Out → Cloudflare ($0 renewal) | 60-day lock period | ✅ RECOMMENDED for long-term |
| **B: Transfer with sub-account** | Transfer entire sub-account to new agency → domain moves with it | Domain assigned by old agency removed | ⚠️ Partial — needs re-config |
| **C: Re-purchase on new account** | Buy neuronx.co again on paid account | ❌ Can't — already owned | Not possible |
| **D: Keep in sandbox, point DNS externally** | Use sandbox as DNS manager only | Sandbox expires in 6 months | ⚠️ Temporary only |

### Recommended Path
1. **Now**: Keep domain in sandbox (it works for DNS management)
2. **Day 60+**: Transfer out to Cloudflare (free DNS, $10/yr renewal)
3. **Production account**: Point neuronx.co DNS records to new GHL setup
4. **Website hosting**: Use Cloudflare Pages, Vercel, or Netlify (free tier) — GHL not needed for marketing website

### Can You Use neuronx.co Outside GHL?
**YES.** The domain is yours. You can:
- Host a marketing website on Vercel/Netlify (A/CNAME records)
- Run email through Google Workspace (MX records already set)
- Point app.neuronx.co to GHL whitelabel (CNAME)
- Point api.neuronx.co to your FastAPI server (A record)
- Use mg.neuronx.co for Mailgun (already configured)

---

## PRICING & BILLING DECISION (RESOLVED 2026-03-26)

### GHL Plan: $297/mo (Agency Unlimited) — DECIDED
Upgrade to $497 at client #8-10 when manual provisioning becomes painful.

### Client Pricing: 3 Tiers — DECIDED
| Tier | Price (CAD/mo) | Target |
|------|---------------|--------|
| Essentials | $299 | Solo RCIC starting out |
| Professional | $599 | Solo/duo firm (70% of clients) |
| Scale | $1,199 | 3-5 consultant firms |

### Billing Platform: Stripe Billing Direct — DECIDED
Full details: `docs/07_gtm/BILLING_CONFIGURATION.md`
Full pricing rationale: `docs/07_gtm/PRICING_STRATEGY.md`

### Previous Analysis (archived)
#### Option A: Start at $297/mo (Agency Unlimited)
```
Pros:
+ $200/mo cheaper
+ Unlimited sub-accounts
+ Full white-label branding
+ Everything except SaaS auto-provisioning

Cons:
- No SaaS Mode (manual client onboarding)
- No automated client billing
- No rebilling (SMS/email usage)
- No branded mobile app
- Must manually create sub-accounts + load snapshots

Best if: You want to minimize burn while manually onboarding first 5-10 clients
```

### Option B: Start at $497/mo (Agency Pro / SaaS Mode)
```
Pros:
+ Full SaaS Mode — automated sign-up → sub-account creation
+ Automated client billing via Stripe
+ Rebilling (markup on SMS/email/AI usage)
+ Branded mobile app
+ Scalable from Day 1

Cons:
- $200/mo more expensive
- SaaS features not needed until you have 5+ clients
- Overkill for pilot phase

Best if: You want full automation from Day 1 and expect to onboard clients quickly
```

### Recommendation: Start at $297, upgrade at client #5
- **Months 1-3**: $297/mo — manually onboard first 3-5 clients via snapshot
- **Month 4+**: Upgrade to $497/mo when manual onboarding becomes a bottleneck
- **Savings**: $600 over first 3 months
- **Annual billing**: $237/mo ($297 × 0.8) = save $720/year vs monthly

---

## OPEN SOURCE GAP FILLERS

### Where Open Source Can Help (Without Replacing GHL)

| Gap | Open Source Solution | Why |
|-----|---------------------|-----|
| **Marketing website** | Next.js + Vercel (free) | GHL funnels are limited; real website needed for credibility |
| **Analytics dashboard** | Metabase (self-hosted, free) | Client-facing analytics beyond GHL reporting |
| **Document generation** | Docxtemplater or Puppeteer | Auto-generate retainer agreements, engagement letters |
| **Knowledge base** | Docusaurus or GitBook (free) | Client help center, onboarding guides |
| **CRM backup/export** | Custom scripts + PostgreSQL | Data sovereignty, backup GHL contacts/deals |

### What NOT to Replace with Open Source
- **CRM/Pipeline**: GHL is the system of record. Don't duplicate.
- **Workflow automation**: GHL workflows are the core. Don't build a second engine.
- **Email/SMS sending**: GHL/Mailgun/LC Phone. Don't add Twilio/SendGrid separately.
- **Calendar/booking**: GHL calendars. Don't add Calendly.

---

## FINANCIAL MODEL

### Cost Structure (Monthly)
| Item | Sandbox Phase | Production ($297) | Production ($497) |
|------|---------------|-------------------|--------------------|
| GHL | $0 | $297 | $497 |
| Google Workspace | $7.20 CAD | $7.20 CAD | $7.20 CAD |
| VAPI (usage) | $0 (no calls) | ~$20 (est.) | ~$20 (est.) |
| FastAPI hosting | $0 (local) | $0-7 (Railway free) | $0-7 |
| Domain renewal | $0 (pre-paid) | $0 | $0 |
| Phone number | $0 (blocked) | ~$3/mo | ~$3/mo |
| **Total** | **~$7 CAD/mo** | **~$334/mo** | **~$534/mo** |

### Revenue Targets
| Milestone | Clients | MRR | ARR | When |
|-----------|---------|-----|-----|------|
| First client | 1 | $1,500 | $18K | Week 6 |
| Breakeven ($297 plan) | 1 | $1,500 | $18K | Week 6 |
| 5 clients | 5 | $7,500 | $90K | Month 3 |
| 10 clients | 10 | $15,000 | $180K | Month 6 |
| 25 clients | 25 | $37,500 | $450K | Month 12 |
| 50 clients | 50 | $75,000 | $900K | Month 18 |
| $1M ARR | 56 | $83,000 | $1M | Month 18-20 |

---

## DEFERRED ITEMS (Cannot Do in Sandbox)

These items are explicitly deferred to Phase 1 (production account):

| Item | Why Deferred | When to Do |
|------|-------------|-----------|
| Email sending test | Sandbox blocks all email | Day 1 of production |
| SMS sending test | Sandbox blocks LC Phone | Day 2 of production |
| Phone number purchase (416/647) | LC Phone blocked | Day 2 of production |
| A2P 10DLC registration | Requires production phone | Day 2 of production |
| SaaS Mode configuration | Requires $497 plan | Month 3-4 (or Day 5 if starting on $497) |
| Client billing setup | Requires Stripe verification | Day 1 of production |
| 3rd sub-account creation | 2 sub-account limit | Day 1 of production |
| Production email from Conversations | Requires verified Stripe + paid plan | Day 2 of production |
| Whitelabel domain (app.neuronx.co) | Need to re-configure on new account | Day 1 of production |
| Favicon fix | Can do in sandbox but low priority | Week 5 |

---

## RISK REGISTER

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Sandbox expires before Phase 1 | Low (6 months from creation) | High | Create snapshot immediately |
| Snapshot doesn't capture everything | Low | Medium | Document what's NOT in snapshot (credentials, API keys, DNS) |
| Domain transfer delay (60-day lock) | Medium | Low | Start transfer early; use manual DNS in interim |
| GHL raises prices | Low | Medium | Lock annual billing when ready |
| Pilot customer says no | Medium | High | Warm up 5-10 prospects, not just 1 |
| VAPI costs higher than expected | Low | Low | Per-minute pricing, start small |
| Sandbox data wiped unexpectedly | Low | High | **Snapshot is the insurance — CREATE NOW** |

---

## AGENT RULES (MANDATORY — All AI Agents Must Follow)

### Rule S1: Sandbox Awareness
Every session MUST check: "Am I operating on a sandbox or production account?" Read this document first. If sandbox: do NOT attempt email, SMS, phone, or >2 sub-account operations. They will fail silently or with errors.

### Rule S2: Snapshot Before Changes
Before any destructive changes or major refactoring, verify a recent snapshot exists. If not, prompt the founder to create one.

### Rule S3: Deferred Task Tracking
Any task that cannot be completed in sandbox MUST be logged in the DEFERRED ITEMS table above with: reason, when to do it, and any dependencies.

### Rule S4: Cost Awareness
No paid services or subscriptions without founder approval. Free tiers only for hosting, CI/CD, analytics. The $7.20 CAD/month Google Workspace is the only approved recurring cost until production launch.

### Rule S5: Production Readiness Focus
Every coding task should be production-ready — not "sandbox-grade." Write tests, handle errors, log properly. When we flip to production, the code should just work.

### Rule S6: State File Updates
After every session, update:
1. `PROJECT_MEMORY.md` — what was done
2. `docs/06_execution/CURRENT_STATE.md` — execution state
3. `docs/08_implementation/MASTER_IMPLEMENTATION_PLAN.md` — check off completed items

---

## IMMEDIATE NEXT ACTIONS (Today, 2026-03-26)

1. **🔴 CREATE SNAPSHOT** — Agency Dashboard → Account Snapshots → Create. This is the #1 priority.
2. **Configure Notification Settings** — My Staff → Notification Settings tab
3. **Add phone to My Staff** — +16479395000
4. **Set Reply & Forward Settings** — Email Services → Reply & Forward Settings
5. **Start FastAPI development** — `/neuronx-api/` scaffold ready

---

## Sources

- [GHL Sandbox Account Docs](https://marketplace.gohighlevel.com/docs/oauth/SandboxAccount)
- [GHL Sandbox PIT Docs](https://marketplace.gohighlevel.com/docs/oauth/SandboxPIT)
- [GHL Snapshot Overview](https://help.gohighlevel.com/support/solutions/articles/48000982511-snapshots-overview)
- [GHL Sub-Account Transfer Guide](https://help.gohighlevel.com/support/solutions/articles/155000002031-sub-account-transfer-guide)
- [GHL Domain Transfer-Out](https://ideas.gohighlevel.com/changelog/domain-transfer-out)
- [GHL Pricing 2026](https://www.gohighlevel.com/pricing)
- [GHL SaaS Mode Guide](https://ghl-services-playbooks-automation-crm-marketing.ghost.io/gohighlevel-saas-setup-pricing-guide-for-agencies/)
- [GHL Free Trial Options](https://www.automatethejourney.com/blog/gohighlevel-free-trial-2026)
