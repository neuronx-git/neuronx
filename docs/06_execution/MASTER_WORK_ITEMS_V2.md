# NeuronX — Master Work Items (V2 — Complete E2E Gold Class)

**Version**: v2.0
**Date**: 2026-03-26
**Status**: CANONICAL — Single source of truth for all execution
**Overall Progress**: 150/268 items done (56%) → Target: 268/268

---

## PROGRESS DASHBOARD

```
PHASE 0: SANDBOX BUILD          ████████████░░░░░░░░ 56%  (150/268)
  ├── Tier 1: Agency             ██░░░░░░░░░░░░░░░░░░ 26%  (17/65)
  ├── Tier 2: NeuronX Sub       ██████████████░░░░░░ 72%  (132/184)
  ├── Tier 3: VMC Pilot          █░░░░░░░░░░░░░░░░░░░  5%  (1/19)
  ├── Tier 4: FastAPI Brain      ░░░░░░░░░░░░░░░░░░░░  0%  (0/18)
  ├── Tier 5: Open Source Stack  ░░░░░░░░░░░░░░░░░░░░  0%  (0/12)
  └── Tier 6: GTM & Launch       ██░░░░░░░░░░░░░░░░░░ 15%  (3/20)

PHASE 1: PRODUCTION (Week 5)    ░░░░░░░░░░░░░░░░░░░░  0%  (0/25)
PHASE 2: FIRST CUSTOMER (Wk 6) ░░░░░░░░░░░░░░░░░░░░  0%  (0/12)
```

---

## EXECUTION ORDER (Most Logical Sequence)

### 🔴 BLOCK 1: IMMEDIATE (Today — Mar 26)
*Must do before anything else. All sandbox-safe.*

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 1.1 | **CREATE SNAPSHOT** of NeuronX sub-account | UI | 5 min | ✅ DONE (2026-03-26) |
| 1.2 | Add phone +16479395000 to My Staff profile | UI | 2 min | ⬜ TODO |
| 1.3 | Configure Notification Settings (My Staff tab) — enable email + in-app for new leads, bookings, form submissions | UI | 10 min | ⬜ TODO |
| 1.4 | Set Reply & Forward Settings — forwarding: ranjan@neuronx.co, reply: ranjan@neuronx.co, forward-to-assigned: ON | UI | 5 min | ⬜ TODO |
| 1.5 | Set Call & Voicemail Settings (My Staff tab) — voicemail greeting, call forwarding to +16479395000 | UI | 5 min | ⬜ TODO |

---

### 🟡 BLOCK 2: GHL SUB-ACCOUNT COMPLETION (Week 1 — Mar 27-Apr 1)
*Complete all remaining NeuronX sub-account configuration. Sandbox-safe.*

#### 2A: Forms & Funnel Polish

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 2.1 | Update landing page headline: "Turn Every Inquiry Into a Consultation" | UI (Funnel Builder) | 15 min | ⬜ TODO |
| 2.2 | Add programs section to landing page (8 immigration programs with icons) | UI | 30 min | ⬜ TODO |
| 2.3 | Add trust signals section (CICC regulated, PIPEDA compliant, years of experience) | UI | 20 min | ⬜ TODO |
| 2.4 | Add testimonials/social proof section (template — client fills in their own) | UI | 20 min | ⬜ TODO |
| 2.5 | Add SEO meta tags to funnel pages | UI | 10 min | ⬜ TODO |
| 2.6 | Add Google Analytics / Facebook Pixel tracking code placeholders | UI | 10 min | ⬜ TODO |
| 2.7 | Mobile-responsive check on all funnel pages | UI | 15 min | ⬜ TODO |
| 2.8 | Fix favicon (NeuronX icon) | UI | 5 min | ⬜ TODO |

#### 2B: Email & SMS Templates (Drafts — Can't Test Sending)

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 2.9 | Create Assessment SMS variants (R1-R5 specific follow-ups) | UI (Marketing → Templates) | 30 min | ⬜ TODO |
| 2.10 | Create Complex Case Alert email (for RCIC when nx:human_escalation tagged) | UI | 15 min | ⬜ TODO |
| 2.11 | Create PIPEDA Data Deletion Confirmation email | UI | 15 min | ⬜ TODO |
| 2.12 | Create Proposal/Retainer Follow-up email (7-day after proposal sent) | UI | 15 min | ⬜ TODO |
| 2.13 | Create Win-Back Nurture email (for lost leads, 30-day re-engagement) | UI | 15 min | ⬜ TODO |

#### 2C: Workflow Refinements

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 2.14 | WF-11: Add program-specific nurture branches (8 programs × different content) | UI (Workflow Builder) | 2 hrs | ⬜ TODO |
| 2.15 | WF-13: Test PIPEDA deletion workflow logic (triggers, conditions) | UI | 30 min | ⬜ TODO |
| 2.16 | Review all 13 workflows — verify tag triggers, conditions, stage moves are correct | UI | 1 hr | ⬜ TODO |
| 2.17 | Document all workflow trigger→action maps in a reference sheet | Doc | 30 min | ⬜ TODO |

#### 2D: NeuronX Sales Workflows (For YOUR Sales Pipeline)

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 2.18 | NX-WF-01: New Lead Alert — trigger on contact created, tag nx:lead:new, notify founder, create opportunity | UI | 20 min | ⬜ TODO |
| 2.19 | NX-WF-02: Demo Booked — trigger on calendar event, tag nx:demo:scheduled, move pipeline | UI | 20 min | ⬜ TODO |
| 2.20 | NX-WF-03: Demo Completed Follow-up — trigger 1 day post-demo, draft follow-up (no send) | UI | 20 min | ⬜ TODO |
| 2.21 | NX-WF-04: Proposal Sent Tracker — trigger on field update, tag nx:proposal:sent, move stage | UI | 15 min | ⬜ TODO |
| 2.22 | NX-WF-05: Deal Won — trigger on tag nx:deal:won, move stage, create onboarding task | UI | 15 min | ⬜ TODO |
| 2.23 | NX-WF-06: Deal Lost — trigger on tag nx:deal:lost, move stage, add to win-back | UI | 15 min | ⬜ TODO |

#### 2E: Pipeline & Custom Values

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 2.24 | Verify NeuronX Sales Pipeline stages match pricing tiers (Essentials/Professional/Scale) | UI | 10 min | ⬜ TODO |
| 2.25 | Add Custom Values for email templates: {{business.name}}, {{business.phone}}, {{calendar.link}} | API | 15 min | ⬜ TODO |

---

### 🟢 BLOCK 3: FastAPI THIN BRAIN (Week 2 — Apr 2-8)
*Local development. Zero GHL dependency. This is the intelligence layer.*

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 3.1 | Project scaffold: FastAPI + Python 3.11 + poetry/pip + project structure | Code | 30 min | ⬜ TODO |
| 3.2 | `GET /health` — Service health check endpoint | Code | 15 min | ⬜ TODO |
| 3.3 | `POST /webhooks/ghl` — GHL form submission + appointment event receiver | Code | 2 hrs | ⬜ TODO |
| 3.4 | `POST /webhooks/voice` — VAPI end-of-call report handler (transcript, structured data) | Code | 2 hrs | ⬜ TODO |
| 3.5 | `POST /score/lead` — Readiness scorer (R1-R5 → outcome + score + tags) | Code | 3 hrs | ⬜ TODO |
| 3.6 | `POST /briefing/generate` — Pre-consultation briefing generator (OpenAI GPT-4o) | Code | 3 hrs | ⬜ TODO |
| 3.7 | `POST /trust/check` — Trust boundary enforcer (scan transcript for violations) | Code | 2 hrs | ⬜ TODO |
| 3.8 | `GET /analytics/pipeline` — Conversion funnel metrics (N-day window) | Code | 2 hrs | ⬜ TODO |
| 3.9 | `GET /analytics/stuck` — Stuck leads detection (leads in stage > threshold days) | Code | 1 hr | ⬜ TODO |
| 3.10 | `GET /analytics/dashboard` — Daily summary for firm owner | Code | 1 hr | ⬜ TODO |
| 3.11 | GHL API client module (contacts, tags, opportunities, custom fields CRUD) | Code | 2 hrs | ⬜ TODO |
| 3.12 | VAPI API client module (call initiation, assistant management) | Code | 1 hr | ⬜ TODO |
| 3.13 | Unit tests for scoring engine (all R1-R5 combinations) | Code | 2 hrs | ⬜ TODO |
| 3.14 | Unit tests for trust boundary checker | Code | 1 hr | ⬜ TODO |
| 3.15 | Integration test: GHL webhook → score → tag update → pipeline move | Code | 2 hrs | ⬜ TODO |
| 3.16 | Docker containerization (Dockerfile + docker-compose) | Code | 30 min | ⬜ TODO |
| 3.17 | Deploy to Railway (free tier) or Render | Deploy | 30 min | ⬜ TODO |
| 3.18 | API documentation (auto-generated via FastAPI /docs) | Code | Free (built-in) | ⬜ TODO |

---

### 🔵 BLOCK 4: OPEN SOURCE ENHANCEMENT STACK (Week 2-3)
*Free tools that make NeuronX premium. Each adds value without adding cost.*

| # | Tool | What It Does | Integration | Time | Priority |
|---|------|-------------|-------------|------|----------|
| 4.1 | **[Metabase](https://www.metabase.com/)** (open source) | Client-facing analytics dashboard — show firm owners their pipeline metrics, conversion rates, lead sources in beautiful charts | FastAPI feeds data → PostgreSQL → Metabase reads it. Embed dashboards via iframe in GHL custom menu link or client portal. Free self-hosted on Railway. | 4 hrs | P1 — HIGH VALUE |
| 4.2 | **[Documenso](https://documenso.com/)** (open source) | Digital retainer/engagement letter signing — after consultation outcome = "proceed", auto-send retainer for e-signature | FastAPI triggers → Documenso API creates signing request → webhook on completion → GHL tag update. Self-hosted free. | 3 hrs | P1 — DIFFERENTIATOR |
| 4.3 | **[Nextcloud](https://nextcloud.com/)** (open source) | Secure document portal — clients upload passports, bank statements, education docs. RCIC reviews in one place | Self-hosted. Create per-client folders. Share links via GHL email templates. PIPEDA-compliant when self-hosted in Canada. | 3 hrs | P2 — Phase 2 |
| 4.4 | **[Cal.com](https://cal.com/)** (open source) | Advanced scheduling — if GHL calendar limitations appear (round-robin edge cases, collective booking, payments) | Native integration: Cal.com webhook → GHL contact update. Free self-hosted. Only add IF GHL calendar proves insufficient. | 2 hrs | P3 — IF NEEDED |
| 4.5 | **[n8n](https://n8n.io/)** (open source) | Workflow automation middleware — connect VAPI → FastAPI → GHL → Documenso → Metabase in complex multi-step flows | Self-hosted on Railway. Has native GHL node. Use ONLY for complex orchestration that FastAPI can't handle natively. | 3 hrs | P2 — ONLY IF NEEDED |
| 4.6 | **[Chatwoot](https://www.chatwoot.com/)** (open source) | Live chat widget on client websites — capture leads who don't want to fill forms, route to GHL as contacts | Embed on landing page. Webhook → GHL contact creation. Alternative to GHL's built-in chat (which is decent). | 2 hrs | P3 — Phase 2 |
| 4.7 | **[Plausible](https://plausible.io/)** (open source) | Privacy-friendly website analytics — track landing page visits, form submissions, conversion rates without Google dependency | Drop-in script on funnel/landing pages. Self-hosted free. PIPEDA-friendly (no cookies). | 1 hr | P2 — NICE TOUCH |
| 4.8 | **NeuronX Client Portal** (custom, using Next.js) | Branded portal at portal.neuronx.co where firm owners see their dashboard, manage settings, view invoices | Next.js + Stripe Customer Portal embed + Metabase embed + GHL API for contact/pipeline data. Hosted on Vercel (free). | 8 hrs | P1 — Week 4 |
| 4.9 | **[Docxtemplater](https://docxtemplater.com/)** (open source) | Auto-generate consultation prep packets, engagement letters, retainer agreements from templates | Integrate into FastAPI briefing endpoint. Template → merge GHL contact data → output PDF. | 2 hrs | P1 — HIGH VALUE |
| 4.10 | **neuronx.co Marketing Website** (Next.js + Tailwind) | Professional marketing site with pricing page, features, demo booking, blog | Next.js on Vercel (free). Stripe Payment Links on pricing page. Cal embedded for demo booking. | 12 hrs | P1 — Week 3-4 |
| 4.11 | **[Umami](https://umami.is/)** (open source) | Alternative to Plausible — simpler, self-hosted web analytics | Drop-in script. Self-hosted on Railway/Vercel. | 1 hr | P3 — OPTIONAL |
| 4.12 | **[Papermerge](https://www.papermerge.com/)** (open source) | Document management with OCR — scan uploaded immigration docs, extract text for searchability | Advanced feature for Phase 2. OCR on passport scans, education transcripts. | 4 hrs | P3 — Phase 2 |

#### Open Source Stack Architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT-FACING                         │
├──────────┬──────────┬──────────┬───────────────────────┤
│ neuronx  │ Client   │ Landing  │ Firm Owner            │
│ .co      │ Portal   │ Pages    │ Dashboard             │
│ (Next.js)│ (Next.js)│ (GHL)    │ (Metabase embed)      │
├──────────┴──────────┴──────────┴───────────────────────┤
│                    MIDDLEWARE                            │
├──────────┬──────────┬──────────┬───────────────────────┤
│ FastAPI  │ VAPI     │ Stripe   │ Documenso             │
│ (brain)  │ (voice)  │ (billing)│ (e-sign)              │
├──────────┴──────────┴──────────┴───────────────────────┤
│                    SYSTEM OF RECORD                      │
├──────────┬──────────┬──────────┬───────────────────────┤
│ GHL CRM  │ Google   │ Plausible│ PostgreSQL            │
│ (pipeline│ Workspace│ (privacy │ (analytics            │
│  contacts│ (email)  │  analytics│  data store)          │
│  workflow)│         │  )       │                       │
└──────────┴──────────┴──────────┴───────────────────────┘
```

---

### 🟣 BLOCK 5: VOICE AI (Week 3 — Apr 9-15)
*OD-01 Resolution + VAPI Refinement*

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 5.1 | Voice AI bake-off: GHL Voice AI vs VAPI — test both on same 5 scenarios | Test | 3 hrs | ⬜ TODO |
| 5.2 | Score bake-off results (latency, accuracy, naturalness, cost, compliance) | Analysis | 1 hr | ⬜ TODO |
| 5.3 | **OD-01 DECISION**: Lock voice provider (Founder final call) | Decision | — | ⬜ TODO |
| 5.4 | Refine VAPI agent prompts (R1-R5 question flow, escalation triggers) | VAPI Config | 2 hrs | ⬜ TODO |
| 5.5 | Configure VAPI structured data extraction (post-call JSON → R1-R5 fields) | VAPI Config | 1 hr | ⬜ TODO |
| 5.6 | Configure VAPI serverUrl → FastAPI production endpoint | VAPI Config | 15 min | ⬜ TODO |
| 5.7 | Test VAPI → FastAPI → GHL end-to-end flow (call → score → tag → pipeline) | Integration | 2 hrs | ⬜ TODO |
| 5.8 | Create VAPI per-client isolation strategy (per-assistant vs per-account) | Architecture | 1 hr | ⬜ TODO |

---

### 🟤 BLOCK 6: GTM & SALES PREP (Week 3-4 — Apr 9-22)
*Get ready to sell before production account exists.*

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 6.1 | GTM Strategy document — complete research + write | Doc | 3 hrs | ⬜ TODO |
| 6.2 | Competitive analysis deep-dive (CaseEasy, Docketwise, Officio, Visto, Clio, Lawmatics) | Research | 2 hrs | ✅ DONE (partial) |
| 6.3 | Pricing strategy finalized ($299/$599/$1,199) | Decision | — | ✅ DONE |
| 6.4 | Billing configuration documented (Stripe direct) | Doc | — | ✅ DONE |
| 6.5 | Create sales deck / pitch presentation (10 slides) | Doc/Design | 3 hrs | ⬜ TODO |
| 6.6 | Create demo video script (3-minute product walkthrough) | Doc | 1 hr | ⬜ TODO |
| 6.7 | Identify 10 warm pilot prospects (Canadian RCICs — LinkedIn, CAPIC, CICC directory) | Research | 2 hrs | ⬜ TODO |
| 6.8 | Create outreach email templates (3 variants: cold, warm, referral) | Doc | 1 hr | ⬜ TODO |
| 6.9 | Create onboarding playbook v1 (step-by-step client setup guide) | Doc | 2 hrs | ⬜ TODO |
| 6.10 | Create client training video outline (what to show on onboarding call) | Doc | 1 hr | ⬜ TODO |
| 6.11 | Design NeuronX logo properly (fix spacing between Neuron and X) | Design | 1 hr | ⬜ TODO |
| 6.12 | Prepare ROI calculator spreadsheet (input: inquiries/month → output: extra retainers) | Spreadsheet | 1 hr | ⬜ TODO |
| 6.13 | Create case study template (for pilot customer results) | Doc | 30 min | ⬜ TODO |
| 6.14 | Research CAPIC conference dates + CICC events for networking | Research | 30 min | ⬜ TODO |
| 6.15 | Set up LinkedIn company page for NeuronX | Social | 30 min | ⬜ TODO |
| 6.16 | Write 3 LinkedIn posts (launch announcement, problem statement, solution preview) | Content | 1 hr | ⬜ TODO |
| 6.17 | Search for GHL free trial affiliate link (30 days) | Research | 30 min | ⬜ TODO |

---

### ⚪ BLOCK 7: PRODUCTION LAUNCH (Week 5 — Apr 23-29)
*Switch from sandbox to paid account. Everything blocked above gets unblocked.*

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 7.1 | Sign up GHL $297/mo (use 30-day trial link) | Account | 15 min | ⬜ DEFERRED |
| 7.2 | Complete Stripe verification (business docs + Canadian bank) | Account | 30 min | ⬜ DEFERRED |
| 7.3 | Import production snapshot into new agency | UI | 15 min | ⬜ DEFERRED |
| 7.4 | Create NeuronX sub-account from snapshot | UI | 10 min | ⬜ DEFERRED |
| 7.5 | Re-authorize OAuth Marketplace app (new tokens) | API | 15 min | ⬜ DEFERRED |
| 7.6 | Transfer/re-point neuronx.co DNS to production | DNS | 30 min | ⬜ DEFERRED |
| 7.7 | Configure whitelabel domain (app.neuronx.co) | UI | 15 min | ⬜ DEFERRED |
| 7.8 | Re-configure Mailgun (mg.neuronx.co) | UI | 15 min | ⬜ DEFERRED |
| 7.9 | Connect Google Workspace (ranjan@neuronx.co) | UI | 10 min | ⬜ DEFERRED |
| 7.10 | Buy Toronto phone number (416/647) | UI | 5 min | ⬜ DEFERRED |
| 7.11 | Register A2P 10DLC | UI | 30 min | ⬜ DEFERRED |
| 7.12 | Send test email from Conversations | Test | 5 min | ⬜ DEFERRED |
| 7.13 | Send test SMS | Test | 5 min | ⬜ DEFERRED |
| 7.14 | Test outbound VAPI call (end-to-end) | Test | 15 min | ⬜ DEFERRED |
| 7.15 | Set up Stripe Products (Essentials $299, Professional $599, Scale $1,199) | Stripe | 30 min | ⬜ DEFERRED |
| 7.16 | Generate Stripe Payment Links (3 tiers) | Stripe | 15 min | ⬜ DEFERRED |
| 7.17 | Configure Stripe Customer Portal | Stripe | 30 min | ⬜ DEFERRED |
| 7.18 | Configure Stripe dunning emails | Stripe | 15 min | ⬜ DEFERRED |
| 7.19 | UAT-01: Happy path (form → call → booking → briefing → retainer) | Test | 30 min | ⬜ DEFERRED |
| 7.20 | UAT-02: Complex case (refusal → human escalation) | Test | 20 min | ⬜ DEFERRED |
| 7.21 | UAT-03: No-show → automated follow-up | Test | 20 min | ⬜ DEFERRED |
| 7.22 | UAT-04: Disqualified lead → proper exit | Test | 15 min | ⬜ DEFERRED |
| 7.23 | Create VMC pilot sub-account from client snapshot | UI | 15 min | ⬜ DEFERRED |
| 7.24 | Configure VMC branding (logo, colors, firm details) | UI | 1 hr | ⬜ DEFERRED |
| 7.25 | Final snapshot (production-ready, all UAT passed) | UI | 10 min | ⬜ DEFERRED |

---

### ⭐ BLOCK 8: FIRST CUSTOMER (Week 6 — Apr 30-May 6)

| # | Task | Type | Time | Status |
|---|------|------|------|--------|
| 8.1 | Pilot customer identified and committed (from Block 6 outreach) | Sales | — | ⬜ DEFERRED |
| 8.2 | Send Stripe Payment Link to pilot | Sales | 5 min | ⬜ DEFERRED |
| 8.3 | Deploy pilot sub-account from snapshot | UI | 15 min | ⬜ DEFERRED |
| 8.4 | Customize branding for pilot firm | UI | 1 hr | ⬜ DEFERRED |
| 8.5 | Conduct onboarding call (60 min) | Meeting | 60 min | ⬜ DEFERRED |
| 8.6 | Embed intake form on pilot's website | Code | 30 min | ⬜ DEFERRED |
| 8.7 | First inquiry submitted via NeuronX | Milestone | — | ⬜ DEFERRED |
| 8.8 | First AI call executed | Milestone | — | ⬜ DEFERRED |
| 8.9 | First consultation booked automatically | Milestone | — | ⬜ DEFERRED |
| 8.10 | First retainer signed post-consultation | Milestone | — | ⬜ DEFERRED |
| 8.11 | Collect NPS/feedback from pilot | Survey | 15 min | ⬜ DEFERRED |
| 8.12 | Create case study from pilot results | Doc | 1 hr | ⬜ DEFERRED |

---

## WHAT'S ALREADY DONE (Completed Items)

### Tier 2: NeuronX Sub-Account — 72% Complete
- ✅ 98 Custom Fields created via API
- ✅ 76 Tags (51 NX-prefixed) created via API
- ✅ 9-Stage Pipeline (NeuronX — Immigration Intake) created in UI
- ✅ Calendar (NeuronX Product Demo) — round_robin, Mon-Fri 9-5 ET, 10min buffer, Google Meet
- ✅ Immigration Inquiry Form V1 — all fields, consent, AI disclaimer
- ✅ Thank You Page — VMC brand kit
- ✅ Landing Page / Funnel V1 — basic structure (needs content polish)
- ✅ 13 Workflows (WF-01 through WF-13) — ALL PUBLISHED & VERIFIED
- ✅ 15/20 Email & SMS templates created
- ✅ VAPI Voice Agent configured (GPT-4o + ElevenLabs)
- ✅ OAuth Marketplace App authorized (21 scopes)
- ✅ Google Calendar 2-way sync connected
- ✅ Business Profile completed (today)
- ✅ Google Workspace (ranjan@neuronx.co) active with aliases
- ✅ Mailgun sending domain (mg.neuronx.co) verified
- ✅ Domain purchased (neuronx.co)
- ✅ 6 VMC team members created via API

### Tier 6: GTM — 15% Complete
- ✅ Pricing strategy finalized ($299/$599/$1,199)
- ✅ Billing configuration documented (Stripe direct)
- ✅ Competitor analysis (partial)

---

## TOTAL WORK REMAINING

| Block | Items | Est. Hours | When |
|-------|-------|-----------|------|
| Block 1: Immediate | 5 | 0.5 hr | Today |
| Block 2: GHL Completion | 25 | 8 hrs | Week 1 |
| Block 3: FastAPI Brain | 18 | 25 hrs | Week 2 |
| Block 4: Open Source Stack | 12 | 45 hrs | Week 2-4 |
| Block 5: Voice AI | 8 | 10 hrs | Week 3 |
| Block 6: GTM & Sales | 17 | 18 hrs | Week 3-4 |
| Block 7: Production Launch | 25 | 8 hrs | Week 5 |
| Block 8: First Customer | 12 | 5 hrs | Week 6 |
| **TOTAL** | **122 remaining** | **~120 hrs** | **6 weeks** |

---

## OPEN SOURCE VALUE-ADD SUMMARY

| Tool | What It Adds | Client Perception | Cost | Priority |
|------|-------------|-------------------|------|----------|
| **Metabase** | "Look at your conversion dashboard" | 🔥 WOW factor — firms love seeing their numbers | $0 (self-hosted) | P1 |
| **Documenso** | "Sign your retainer digitally right now" | 🔥 Modern, seamless — closes deals faster | $0 (self-hosted) | P1 |
| **Docxtemplater** | "Here's your consultation prep packet, auto-generated" | 🔥 Professional — RCIC feels prepared | $0 (MIT license) | P1 |
| **Next.js Website** | "Visit neuronx.co — see our pricing, book a demo" | 🔥 Credibility — proves you're a real company | $0 (Vercel free) | P1 |
| **Plausible** | "Here's how your landing page is performing" | 👍 Nice touch — privacy-friendly analytics | $0 (self-hosted) | P2 |
| **Nextcloud** | "Upload your documents securely here" | 👍 Trust — PIPEDA-compliant document handling | $0 (self-hosted) | P2 |
| **n8n** | Complex workflow orchestration | 🔧 Internal tool — clients don't see this | $0 (self-hosted) | P3 |
| **Cal.com** | Advanced scheduling if GHL calendar fails | 🔧 Backup only | $0 (self-hosted) | P3 |
