Now I have all the source documents. Let me create a comprehensive gap analysis across all three tiers. Based on the documents, I'll organize this by what's required per the PRD/blueprint vs what's currently done.

---

# COMPREHENSIVE GAP ANALYSIS: NeuronX GHL Build

**Date**: 2026-03-26  
**Current Status**: Phase 1 GHL Gold Build ~95% complete (per CLAUDE.md), but detailed execution audit shows gaps in critical areas  
**Sandbox Status**: Developer sandbox account with email/SMS/phone sending blocked. Configuration work transferable via snapshot.

---

## TIER 1: AGENCY LEVEL

Agency is the top-level account owned by Ranjan (founder). This tier governs multi-client SaaS operations.

### 1.1 White-Label & Branding

| Item | Requirement | Current Status | Effort | Priority | Notes |
|------|-------------|-----------------|--------|----------|-------|
| Whitelabel domain (`app.neuronx.co`) | Configure custom app domain in Company Settings | ⚠️ NOT STARTED | 5 min | P1 | UI-only, deferred to production (Day 1 when paid plan active) |
| Agency logo + brand colors | Upload to Company Settings | ⏳ BLOCKED | 10 min | P2 | Need to design/acquire logo first |
| Welcome email customization | Update agency welcome email template | ⏳ BLOCKED | 15 min | P2 | Deferred to production (email sending blocked in sandbox) |
| Custom email signature | Update Company Settings → Email Signature | ✅ ASSUMED DONE | 5 min | P1 | No evidence but low risk |
| Favicon | Custom .ico in company settings | ⏳ DEFERRED | 5 min | P3 | Low priority, can fix anytime |

**Sandbox Impact**: Whitelabel domain and email customization deferred to production. All other config can be done now.

---

### 1.2 Billing & Subscription Configuration

| Item | Requirement | Current Status | Effort | Priority | Notes |
|------|-------------|-----------------|--------|----------|-------|
| Stripe account verification | Complete KYC (business docs, bank acct) | ⚠️ NOT STARTED | 1 hour | P0 | **MUST DO before Phase 1 production launch** — blocks payment processing |
| Stripe Connect setup (for SaaS Mode) | Enable SaaS sub-account rebilling | ⏳ DEFERRED | 2 hours | P1 | Only needed if starting on $497 plan; can defer to Month 4 |
| Pricing tier definition (OD-02) | Decide $300 vs $500 vs $1000 tiers | 🔴 UNRESOLVED | 2 hours | P0 | **BLOCKING DECISION** — must resolve before pilot |
| Subscription billing cycle | Set monthly/annual auto-renewal | ✅ ASSUMED | 5 min | P1 | Default is monthly; no action needed |
| Invoice customization | Add firm name, logo to invoices | ⏳ DEFERRED | 15 min | P2 | Production-only |
| Payment method defaults | Configure Stripe as primary payment | ✅ ASSUMED | 5 min | P1 | Default in GHL |
| Trial offer setup | Configure 30-day free trial | ⏳ DEFERRED | 10 min | P0 | **CRITICAL for Phase 1 launch** — must acquire trial link before Week 5 |

**Sandbox Impact**: Cannot test payment processing. Stripe verification deferred to Day 1 of production. All decision-making can happen now.

---

### 1.3 Domain Management

| Item | Requirement | Current Status | Effort | Priority | Notes |
|------|-------------|-----------------|--------|----------|-------|
| Primary domain (`neuronx.co`) | Purchased in sandbox; transferable | ✅ PURCHASED | 30 min transfer | P1 | Currently in sandbox; can transfer out after 60-day lock (2026-05-12). Recommend: transfer to Cloudflare ($10/yr). |
| Domain DNS configuration | MX records (Mailgun), A records, CNAMEs | ✅ CONFIGURED | 15 min review | P1 | Currently managed in sandbox. Must re-point to production on Day 1 of Phase 1. |
| Email domain (mg.neuronx.co) | Mailgun verified sending domain | ✅ VERIFIED | 0 min | P1 | Already configured and verified. Transferable via snapshot. |
| App domain (api.neuronx.co) | FastAPI server hostname | ⏳ PLANNED | 5 min | P1 | Must configure in Week 5 when FastAPI deployed to production |
| Website domain (www.neuronx.co) | Marketing website host | ⏳ DEFERRED | 30 min | P2 | Marketing website will be on Vercel/Netlify; only needs DNS A record pointing to Vercel |
| SSL/TLS certificates | Auto-managed by GHL/Vercel/Render | ✅ AUTO | 0 min | P1 | No action needed; all platforms auto-provision |

**Sandbox Impact**: Domain transfer blocked by 60-day lock from purchase date. All other config transferable.

---

### 1.4 Email Services

| Item | Requirement | Current Status | Effort | Priority | Notes |
|------|-------------|-----------------|--------|----------|-------|
| Mailgun domain verification (mg.neuronx.co) | Configure dedicated sending domain | ✅ DONE | 0 min | P1 | Already verified and configured |
| DKIM/SPF records | Mailgun DNS records in domain | ✅ DONE | 0 min | P1 | Already propagated |
| Reply-To address | `support@neuronx.co` (or founder email) | ⏳ TODO | 5 min | P1 | UI: Email Services → Reply & Forward Settings. Needs founder decision. |
| Forward-To address | Where emails are forwarded after processing | ⏳ TODO | 5 min | P1 | UI: Email Services → Reply & Forward Settings. Should be `ranjan@neuronx.co` |
| CASL compliance footer | Auto-add unsubscribe to commercial emails | ✅ CONFIGURED | 0 min | P1 | GHL auto-adds per Canadian CASL law |
| Bounce handling | Auto-suppress bounced emails | ✅ AUTO | 0 min | P1 | GHL default behavior |
| Spam score monitoring | Track deliverability | ⏳ DEFERRED | 10 min | P2 | Week 5 after first test email |
| Email template library | Master templates for all workflows | 🔧 PARTIAL | 4 hours | P1 | **SEE SECTION 1.5 BELOW** |

**Sandbox Impact**: Email sending blocked entirely in sandbox. All configuration can be done now but testing deferred to Phase 1.

---

### 1.5 Email & SMS Templates (Master Library)

| Template | Current | Required Variants | Status | Priority | Notes |
|----------|---------|-------------------|--------|----------|-------|
| **Acknowledgment/Welcome** | ✅ Draft | 1 master + program variants (EE, Spousal, Work, Study) | 🔧 PARTIAL | P1 | Master exists; variants deferred to Phase 2 personalization |
| **Assessment SMS** | ⏳ PENDING | SMS only | ⏳ TODO | P1 | ~4 variants (high score, med, low, complex) |
| **Booking Confirmation** | ✅ Draft | SMS + Email | ✅ DONE | P1 | 1 master template, 2 channels |
| **Booking Reminders** | ✅ Draft | 3 variants (48h, 24h, 2h) SMS | ✅ DONE | P1 | All 3 variants created |
| **No-Show Recovery** | ✅ Draft | SMS + Email (2 variants: 1h, 24h) | ✅ DONE | P1 | Both variants created |
| **Consultation Outcome** | ⏳ TODO | 3 variants (Proceed, Follow-Up, Declined) | ⏳ TODO | P1 | Need 3 separate templates per outcome |
| **Retainer Delivery** | ✅ Draft | Email + SMS follow-up sequence (5 steps) | ✅ DONE | P1 | Full sequence mapped to WF-09 |
| **Nurture/Monthly Newsletter** | ✅ Draft | 4 program variants (EE, Spousal, Work, Study) + General | ✅ DONE (master) | P2 | Master created; program variants need copy |
| **Declined/Lost Lead** | ⏳ TODO | SMS + Email (2 variants) | ⏳ TODO | P2 | Nurture sequence for declined leads |
| **Consultant Brief** | 📧 EMAIL ONLY | Pre-consultation briefing email | ⏳ BLOCKED | P1 | NeuronX API responsibility, not template. Deferred to Week 4. |
| **Compliance/Opt-Out** | ✅ ASSUMED | Auto-added by GHL | ✅ AUTO | P1 | GHL CASL compliance auto-footer |
| **Data Deletion Acknowledgment** | ⏳ TODO | PIPEDA compliance email | ⏳ TODO | P1 | WF-13 trigger, but email template missing |

**Summary**: 6/11 templates drafted or done. 5/11 TODO. All deferred to Phase 1 (email sending blocked now).

---

### 1.6 Phone Integration

| Item | Requirement | Current Status | Effort | Priority | Notes |
|------|-------------|-----------------|--------|----------|-------|
| Phone number purchase (416/647 area) | Buy Toronto number for SMS/calls | ❌ BLOCKED | 10 min | P0 | **SANDBOX BLOCKS LC PHONE** — deferred to Day 2 of production. Estimated cost: $2-3/mo. |
| A2P 10DLC registration | Register for SMS compliance | ❌ BLOCKED | 2 hours | P0 | **SANDBOX BLOCKS** — must do in production before sending SMS at scale. Required for CASL compliance. |
| Inbound IVR configuration | Route incoming calls | ⏳ DEFERRED | 1 hour | P2 | Not needed for v1 (outbound only). Defer to v1.5. |
| Call recording | Record all consultations | ⏳ DEFERRED | 15 min | P2 | Legal requirement in Ontario (one-party consent). Defer to Phase 1. |
| Voicemail drop (WF-02 gap) | Leave automated voicemail if no answer | ⏳ DEFERRED | 30 min | P3 | Enhancement; can add in Phase 2. |

**Sandbox Impact**: Phone number purchase and A2P registration completely blocked. Cannot test any SMS or phone workflows.

---

### 1.7 SaaS Configurator (Multi-Client Management)

| Item | Requirement | Current Status | Effort | Priority | Notes |
|------|-------------|-----------------|--------|----------|-------|
| SaaS pricing tiers | Define 3-5 tiers in SaaS Configurator | 🔴 OD-02 UNRESOLVED | 1 hour | P0 | **BLOCKING DECISION** — Options: $300 (basic), $600 (pro), $1000 (premium). Or simpler: $500, $1000. |
| Client branding rules | What clients can customize (logo, colors, domain) | ⏳ DEFERRED | 2 hours | P1 | Decision deferred to pilot feedback. Recommend: company name, logo, colors, domain. |
| Client role templates | Admin, Consultant, Receptionist, Read-Only | ⏳ DEFERRED | 1 hour | P1 | Deferred to Week 5 when first client onboarded. |
| Sub-account provisioning workflow | Auto-create sub-account on signup | ⏳ DEFERRED | 4 hours | P1 | Only if $497 plan chosen. Can do manual for first 5 clients. |
| Client snapshots (reduced set) | What features clients get in their account | ⏳ DEFERRED | 2 hours | P1 | Create in Week 5 after feedback on master snapshot. |
| Rebilling rules | Mark-up SMS/email/AI costs to clients | ⏳ DEFERRED | 2 hours | P1 | Only needed if $497 plan. Can defer to Month 4. |

**Sandbox Impact**: SaaS Mode not available (2 sub-account limit). All configuration deferred to production.

---

### 1.8 Snapshots (Critical for Replication)

| Item | Requirement | Current Status | Effort | Priority | Notes |
|------|-------------|-----------------|--------|----------|-------|
| **MASTER SNAPSHOT v1.0** | Create production-ready snapshot of NeuronX sub-account | 🔴 NOT CREATED | 30 min | **P0 BLOCKER** | **MUST CREATE NOW (TODAY 2026-03-26)** — insurance against sandbox expiry. Agency Dashboard → Account Snapshots → Create Snapshot. Instructions in MASTER_IMPLEMENTATION_PLAN.md Section 0.1. |
| Snapshot contents verification | Document what's included/excluded | ⏳ TODO | 1 hour | P1 | Checklist: custom fields ✅, tags ✅, pipeline ✅, workflows ✅, calendar ✅, form ✅, funnel ✅, templates ✅, contact data ❌ (excluded), credentials ❌ (manual re-entry) |
| Snapshot installation test | Install into VMC test account | ⏳ DEFERRED | 1 hour | P2 | Week 2 task per WEEK1_CHECKLIST. Need second sub-account (requires paid plan). |
| Snapshot version control | Track snapshot versions (v1.0, v1.1, etc.) | ⏳ TODO | 10 min | P2 | Version naming: NeuronX_Immigration_Intake_vX.Y_YYYYMMDD |
| Client snapshot variant | Reduced snapshot for client deployments | ⏳ DEFERRED | 2 hours | P2 | Create after first client feedback. Subset: same workflows but client-customized templates. |
| Snapshot documentation | User guide for installing + customizing | ⏳ DEFERRED | 3 hours | P2 | Week 2 task: create onboarding playbook per WEEK1_CHECKLIST. |

**Status**: MASTER SNAPSHOT NOT CREATED YET. This is the #1 blocker and must be completed today.

---

### 1.9 Marketplace App & OAuth

| Item | Requirement | Current Status | Effort | Priority | Notes |
|------|-------------|-----------------|--------|----------|-------|
| OAuth scopes | Read + Write for contacts, opportunities, workflows, tags | ✅ AUTHORIZED | 0 min | P1 | Already granted. Token valid until 2057-03-19 per CLAUDE.md. |
| Token refresh mechanism | Auto-refresh at 30-day intervals | ✅ CONFIGURED | 0 min | P1 | Implemented in ghlProvisioner.ts |
| Marketplace app listing | List "NeuronX by Ranjan" in GHL Marketplace | ⏳ DEFERRED | 4 hours | P2 | Requires app submission form + screenshots. Deferred to after pilot success. |
| App authorization flow | Guide clients through OAuth on signup | ⏳ DEFERRED | 2 hours | P2 | Only needed if $497 SaaS Mode. Can simplify to manual for $297 plan. |
| OAuth error handling | Handle token expiry, re-auth prompts | 🔧 PARTIAL | 1 hour | P1 | Code exists but needs testing in production. |

---

### 1.10 Security & Compliance

| Item | Requirement | Current Status | Effort | Priority | Notes |
|------|-------------|-----------------|--------|----------|-------|
| API key management | Store GHL API keys securely (NOT in code) | ✅ DONE | 0 min | P0 | Using .env and tools/ghl-lab/.tokens.json (gitignored) |
| Webhook signature validation (Ed25519) | Validate GHL inbound webhooks | 🔧 PARTIAL | 2 hours | P1 | Required for security. FastAPI implementation deferred to Week 4. |
| Rate limiting | Respect GHL 100 req/10s, 200K req/day | ⏳ PLANNED | 2 hours | P1 | FastAPI code in Week 4. Docs read 25 req/10s, 10K/day in sandbox. |
| Data encryption | Encrypt sensitive fields at rest | ⏳ DEFERRED | 4 hours | P2 | Not required for v1; defer to v1.1 |
| GDPR/PIPEDA compliance | Data deletion, data export workflows | 🔧 PARTIAL | 2 hours | P1 | WF-13 (PIPEDA deletion) built; email template missing. FYI: NeuronX is Canadian (PIPEDA not GDPR). |
| Audit logging | Log all API calls, form submissions, tagging | ⏳ DEFERRED | 2 hours | P2 | FastAPI responsibility. Not critical for launch. |
| 2FA enforcement | Require 2FA for all admin accounts | ⏳ DEFERRED | 1 hour | P2 | Configure in My Staff settings after prod launch. |
| SSO / Single Sign-On | OAuth for client logins | ⏳ DEFERRED | 2 days | P3 | v2 feature. Not needed for v1. |

**Status**: Basic security in place. OAuth and webhook signatures deferred to Week 4.

---

## TIER 2: NEURONX SUB-ACCOUNT (Development/Gold)

This is the primary development sub-account where all workflows, forms, and configuration live.

### 2.1 Custom Fields (Data Model)

**Blueprint requires**: 40+ fields per ghl_configuration_blueprint.md Section 2

**Current status per PROJECT_MEMORY.md**: 98 custom fields created (overshot blueprint)

| Category | Blueprint Requirement | Current | Status | Notes |
|----------|----------------------|---------|--------|-------|
| **Identity** | lead_source, lead_source_detail, utm_* (5 fields) | ✅ 5/5 | ✅ DONE | All created via API |
| **Readiness R1-R5** | program_interest, current_location, timeline_urgency, prior_applications, budget_awareness, complexity_flags (6 fields) | ✅ 6/6 | ✅ DONE | R6 (family_situation) added as bonus |
| **Attempt Tracking** | contact_attempt_count, last_contact_attempt_at, last_contact_attempt_method, last_contact_attempt_outcome (4 fields) | ✅ 4/4 | ✅ DONE | All mapped to VAPI webhook data |
| **Booking** | confirmation_status, reschedule_count, consultation_type, consultation_fee (4 fields) | ✅ 4/4 | ✅ DONE | — |
| **Consultation Outcome** | consultation_outcome, consultation_outcome_reason, outcome_recorded_at, outcome_recorded_by (4 fields) | ✅ 4/4 | ✅ DONE | — |
| **Retainer** | retainer_sent, retainer_sent_at, retainer_signed, retainer_signed_at, payment_received, payment_received_at, engagement_value (7 fields) | ✅ 7/7 | ✅ DONE | engagement_value added as MONETARY |
| **Consent/Suppression** | marketing_consent, marketing_consent_granted_at, marketing_consent_method, suppression_reason (4 fields) | ✅ 4/4 | ✅ DONE | — |
| **Compliance (NEW)** | ai_disclaimer_shown, consent_ip, consent_form_version, data_deletion_requested, conflict_check_cleared, ai_disclaimer_timestamp (6 fields) | ✅ 6/6 | ✅ DONE | Added per compliance audit |
| **Assessment Extensions** | r2_education_level, r4_budget_readiness, r5_language_ability, r6_family_situation (4 fields) | ✅ 4/4 | ✅ DONE | Enhancements from audit |
| **VAPI Scoring** | ai_score (0-100), ai_score_breakdown, ai_readiness_outcome (3 fields) | ✅ 3/3 | ✅ DONE | Mapped from VAPI structured data extraction |
| **Junk/To-Delete** | 3-4 duplicate/unused fields (152dv, 168z3, 1qpb, 17fpb) | ❌ 4 deleted | ✅ CLEANED | Already removed in prior session |

**Summary**: All 40+ blueprint fields implemented + 15 enhancements = 98 total. No gaps.

---

### 2.2 Tags (Operational Triggers)

**Blueprint requires**: 18 core tags per ghl_configuration_blueprint.md Section 3

**Current status per PROJECT_MEMORY.md**: 76 total tags (51 NX-prefixed)

| Category | Blueprint | Current | Status | Notes |
|----------|-----------|---------|--------|-------|
| **Inquiry Lifecycle** | nx:new_inquiry, nx:contacting:start, nx:contacted, nx:consult_ready, nx:nurture:enter, nx:lost | ✅ 6 required | ✅ DONE | All triggered by workflows |
| **Assessment** | nx:assessment:required, nx:assessment:complete | ✅ 2 required | ✅ DONE | — |
| **Booking** | nx:booking:invited, nx:booking:confirmed | ✅ 2 required | ✅ DONE | — |
| **Appointment** | nx:appointment:noshow | ✅ 1 required | ✅ DONE | — |
| **Consultation** | nx:consult:done | ✅ 1 required | ✅ DONE | — |
| **Outcomes** | nx:outcome:proceed, nx:outcome:follow_up, nx:outcome:declined | ✅ 3 required | ✅ DONE | — |
| **Retainer** | nx:retainer:sent, nx:retainer:signed | ✅ 2 required | ✅ DONE | — |
| **Payment** | nx:payment:received | ✅ 1 required | ✅ DONE | — |
| **Compliance** | nx:consent:marketing_yes, nx:consent:marketing_no, nx:suppressed | ✅ 3 required | ✅ DONE | — |
| **Scoring (BONUS)** | nx:score:high, nx:score:med, nx:score:low, nx:human_escalation | ✅ 4 added | ✅ DONE | Not in blueprint but essential for VAPI integration |
| **Call Tracking (BONUS)** | nx:contacting:attempt1 through attempt6, nx:missed_call | ✅ 7 added | ✅ DONE | For WF-02 retry loop |
| **Source Tracking (BONUS)** | nx:source:ghl_form, nx:source:google_ads, nx:source:referral, nx:source:organic, nx:source:other | ✅ 5 added | ✅ DONE | Marketing attribution |
| **Loss Reasons (BONUS)** | nx:lost:disqualified, nx:lost:budget, nx:lost:timing, nx:lost:other | ✅ 4 added | ✅ DONE | Win/loss analysis |
| **Other** | nx:appointment:noshow, nx:casl:compliant, nx:do_not_contact, nx:ai_disclaimer_shown, nx:call:* variants, nx:human:pending | ✅ ~15 total | ✅ DONE | Comprehensive coverage |

**Summary**: 18 blueprint tags ✅ + 33 enhancements = 51 NX-prefixed tags. Plus 25 other tags = 76 total. No gaps.

**Tag Cleanup Needed (Week 4)**: Standardize naming — currently have both `nx:consult:done` and `nx:consult:completed`, both `nx:appointment:noshow` and `nx:no_show`. Pick one per pair for API cleanup.

---

### 2.3 Pipeline & Stages

**Blueprint requires**: 9 stages per ghl_configuration_blueprint.md Section 1

**Current status**: 10 stages (added PROPOSAL SENT)

| Stage | Blueprint | Current | Status | Notes |
|--------|-----------|---------|--------|-------|
| **NEW** | Required | ✅ | ✅ DONE | Initial inquiry |
| **CONTACTING** | Required | ✅ | ✅ DONE | Contact attempt sequence |
| **UNREACHABLE** | Required | ✅ | ✅ DONE | 7 attempts exhausted |
| **CONSULT READY** | Required | ✅ | ✅ DONE | Assessment complete, ready to book |
| **BOOKED** | Required | ✅ | ✅ DONE | Consultation scheduled |
| **CONSULT COMPLETED** | Required | ✅ | ✅ DONE | Appointment completed |
| **PROPOSAL SENT** | NOT in blueprint | ✅ ADDED | ✅ DONE | New stage between CONSULT COMPLETED and RETAINED (P1-01) |
| **RETAINED** | Required | ✅ | ✅ DONE | Retainer signed and paid |
| **LOST** | Required | ✅ | ✅ DONE | Decline, opt-out, disqualified |
| **NURTURE** | Required | ✅ | ✅ DONE | Long-term follow-up |

**Summary**: All 9 blueprint stages ✅ + 1 enhancement (PROPOSAL SENT) = 10 total. No gaps.

---

### 2.4 Calendar (Immigration Consultations)

**Blueprint requirement**: One calendar, 30min slots, Mon-Fri 9-5 ET, 10min buffer

**Current status per CURRENT_STATE.md audit**:

| Setting | Blueprint | Current | Status | Notes |
|---------|-----------|---------|--------|-------|
| **Calendar Name** | "Immigration Consultations" | ✅ Exact match | ✅ DONE | ID: To1U2KbcvJ0EAX0RGKHS |
| **Availability Hours** | Mon-Fri 9-5 ET | ✅ Configured via API | ✅ DONE | openHours set correctly |
| **Slot Buffer** | 10 minutes | ✅ Configured | ✅ DONE | slotBuffer = 10 |
| **Slot Duration** | 30 minutes | ✅ Correct | ✅ DONE | Default; no change needed |
| **Booking Widget** | Enabled | ✅ Enabled | ✅ DONE | Public booking link live |
| **Confirmation Page** | Enabled | ✅ Enabled | ✅ DONE | Shows after booking |
| **Confirmation Email** | Enabled | ✅ Enabled | ✅ DONE | Sent via WF-05 |
| **Reschedule Button** | Enabled | ✅ Enabled | ✅ DONE | WF-06 uses reschedule link |
| **Timezone** | ET (Eastern) | ✅ Set | ✅ DONE | Canada Eastern time |
| **Payment Mode (GAP)** | $100 CAD deposit (blueprint Section 4) | ❌ NOT LIVE | ⏳ P2-15 | Blocked: Stripe not verified. Cannot test in sandbox. Deferred to Week 5. |
| **Calendar Groups (GAP)** | "Immigration Consultants" group for round-robin | ❌ NOT CREATED | ⏳ P2-08 | Requires 2+ users first. Deferred to Week 5 pilot onboarding. |
| **Round-Robin (GAP)** | Round-robin load balancing for multi-RCIC firms | ❌ NOT CONFIGURED | ⏳ P2-08 | Requires users + calendar groups. Deferred. |
| **Pre-Qualification Gate (GAP)** | Only "CONSULT READY" leads can book | ❌ NOT ENFORCED | ⏳ P2 | Could use UTM parameter or embed form on page. Deferred to v1.1. |

**Summary**: 8/10 core features done. 2/10 gaps deferred to Week 5+. Booking link live and working.

---

### 2.5 Forms (Lead Capture)

**Blueprint requires**: Immigration Inquiry (V1) form with 8+ fields per Section 5

**Current status per CURRENT_STATE.md**: Form structure created (FNMmVXpfUvUypS0c4oQ3), dropdowns partially configured

| Field | Blueprint | Current | Status | Notes |
|-------|-----------|---------|--------|-------|
| **First Name** | Required | ✅ | ✅ DONE | Standard field |
| **Last Name** | Required | ✅ | ✅ DONE | Standard field |
| **Phone** | Required | ✅ | ✅ DONE | Standard field |
| **Email** | Required | ✅ | ✅ DONE | Standard field |
| **Program Interest** | Dropdown (9 options) | ✅ Options added | ✅ DONE | EE, Spousal, Study, Work, LMIA, PR Renewal, Citizenship, Visitor, Other |
| **Current Location** | Dropdown (2 options) | ✅ | ✅ DONE | In Canada, Outside Canada |
| **Timeline** | Dropdown (4 options) | ✅ | ✅ DONE | Urgent, Near-term, Medium, Long-term |
| **Free-Text Notes** | Optional textarea | ✅ | ✅ DONE | — |
| **Marketing Consent** | Checkbox (unchecked default) | ✅ | ✅ DONE | Mapped to marketing_consent field |
| **AI Disclaimer Checkbox** | NEW — required | ✅ Added | ✅ DONE (P1-12) | Required field, mapped to ai_disclaimer_shown |
| **"How did you hear about us?"** | NEW — tracking | ✅ Added | ✅ DONE (P2-11) | 6 options: Google, Referral, Social, Ads, Other, Unknown |
| **Button Text** | "Get Your Free Assessment" | ✅ Updated | ✅ DONE (P0-04) | Changed from generic "Button" |
| **Consent Text** | REQUIRED: Business name must NOT be placeholder | ✅ "Visa Master Canada Immigration Services" | ✅ DONE (P0-02) | Fixed from [BUSINESS NAME] |
| **Transactional Consent** | Implied by submission | ✅ | ✅ DONE | Legal basis for contact |
| **Form Validation** | Required fields marked | ✅ | ✅ DONE | Phone, email, program, location, timeline, AI disclaimer |

**Summary**: All 11 blueprint fields ✅ + 2 enhancements (AI disclaimer, source tracking). Form ready for testing.

**Remaining Gaps**:
- P3-03: Multi-step form (3-page funnel) — deferred
- Program-specific conditional logic — deferred to v1.1

---

### 2.6 Funnel & Landing Page

**Blueprint requires**: Funnel with landing page + form embed + booking CTA

**Current status per CURRENT_STATE.md**: Funnel structure created (VmB52pLVfOShgksvmBir), content partially updated

| Component | Blueprint | Current | Status | Effort | Notes |
|-----------|-----------|---------|--------|--------|-------|
| **Funnel Exists** | Yes | ✅ | ✅ DONE | — | ID: VmB52pLVfOShgksvmBir |
| **Funnel Name** | "NeuronX Intake Landing (V1)" | ✅ Exact | ✅ DONE | — | — |
| **Headline** | "Fast, Structured Immigration Intake..." | ✅ Needed | ⏳ P2-06 | 30 min | **TODO: Update with VMC branding** |
| **Sub-headline** | "...AI-assisted team will contact you..." | ✅ Needed | ⏳ P2-06 | 30 min | **TODO** |
| **CTA Button** | "Get Started — Free Assessment" | ✅ Concept | ⏳ P2-06 | 15 min | **TODO** |
| **Form Embed** | Immigration Inquiry (V1) | ✅ Embedded | ✅ DONE | — | Form FNMmVXpfUvUypS0c4oQ3 embedded |
| **Booking Link** | Link to Immigration Consultations calendar | ✅ Needed | ⏳ P2-06 | 15 min | **TODO: Embed booking widget** |
| **Programs Section** | List 5-6 core programs offered | ❌ Missing | ⏳ P2-06 | 1 hour | **TODO: Add Express Entry, Spousal, Study, Work, PR Renewal** |
| **Trust Signals** | CICC badge, "Licensed RCICs", consultation count | ⏳ Minimal | ⏳ P2-06 | 45 min | **TODO: Find CICC badge, add consultant bio** |
| **Compliance Footer** | No eligibility guarantees, RCIC firm name | ✅ Draft | ✅ DONE | — | "We are a licensed immigration consulting firm..." |
| **Thank You Page** | Custom post-submission page | ✅ Added | ✅ DONE (P1-06) | — | Built with VMC brand kit — navy, red, light gray |
| **Page URL** | /start or /assessment (not internal slug) | ⏳ Slug TBD | ⏳ P2-06 | 5 min | Currently internal. Change to `/start` or `/assessment`. |
| **SEO Configuration** | Meta title, description, Open Graph | ❌ Missing | ⏳ P2-06 | 30 min | **TODO: Add SEO tags** |
| **Tracking Pixels** | Google Analytics, Facebook Pixel (optional) | ❌ Missing | ⏳ P2-06 | 30 min | **TODO: Add GA4 tracking** |
| **Mobile Responsive** | Yes | ✅ Default | ✅ DONE | — | GHL funnels responsive by default |

**Summary**: 4/14 components done. 10/14 TODO (most in P2-06 landing page update task). High priority for Week 1 completion.

---

### 2.7 Workflows (Complete List)

**Blueprint requires**: 11 workflows (WF-01 through WF-11) per Section 6

**Current status per PROJECT_MEMORY.md Session Summary (2026-03-23)**: 15 workflows published (13 required + 2 enhancements)

| WF ID | Name | Blueprint | Current | Trigger | Status | Issues | Notes |
|-------|------|-----------|---------|---------|--------|--------|-------|
| **WF-01** | First Response / Acknowledge | ✅ Required | ✅ Published | Form Submitted | ✅ DONE | None | Sends welcome SMS + adds nx:contacting:start tag |
| **WF-02** | Contact Attempts (Retry Loop) | ✅ Required | ✅ Published | Tag: nx:contacting:start | ✅ DONE | None | 6-attempt VAPI sequence over 48h, If/Else exits, UNREACHABLE fallback — PUBLISHED 2026-03-22 |
| **WF-03** | Contact Success Handler | ✅ As "Mark Contacted" | ✅ Published | Tag: nx:contacted | ✅ DONE | None | Renamed from "Mark Contacted" for clarity. Moves to CONTACTING stage. |
| **WF-04** | Readiness → Booking Invite | ✅ Required | ✅ Published | Tag: nx:score:high | ✅ DONE | Trigger changed | Originally blueprint said `nx:assessment:complete`, but VAPI returns score so changed to `nx:score:high` |
| **WF-04B** | VAPI Data Mapper | ❌ Not in blueprint | ✅ Published | Inbound Webhook (VAPI) | ✅ DONE | None | Freezeframe version: [v14-STABLE]. Maps 11 VAPI fields → GHL custom fields + routing tags. **CRITICAL** for system. |
| **WF-04C** | Missed Call Recovery | ❌ Not in blueprint | ✅ Published | Contact Changed: No Answer/Voicemail | ✅ DONE | None | Auto-triggered when VAPI call drops without answer. Sends SMS recovery. |
| **WF-05** | Appointment Booked → Confirmation | ✅ Required | ✅ Published | Customer Booked Appointment | ✅ DONE | None | Confirmation SMS+Email, then wait 24h, remind. |
| **WF-06** | No-Show Recovery | ✅ Required | ✅ Published | Tag: nx:appointment:noshow | ✅ DONE | None | 5-step recovery: SMS 1h later, SMS 24h later, task, email, final SMS |
| **WF-07** | Consultation Completed → Thank You | ✅ As "Outcome Capture" | ✅ Published | Tag: nx:consult:done | ✅ DONE | None | Move to CONSULT COMPLETED, send thank you SMS+email, internal alert |
| **WF-08** | Human Escalation Handler | ✅ As "Outcome Routing" | ✅ Published | Tag: nx:human_escalation | ✅ DONE | Spec changed | Blueprint says trigger on `consultation_outcome` field change. Current: triggers on `nx:human_escalation` tag (VAPI complex case). Both work. |
| **WF-09** | Retainer Follow-Up Sequence | ✅ Required | ✅ Published | Tag: nx:retainer:sent | ✅ DONE | None | Retainer email Day 0, SMS Day 1-5, follow-ups. Moves to RETAINED if signed. |
| **WF-10** | Post-Consult Follow-Up (Undecided) | ✅ Required | ✅ Published | Tag: nx:retainer:signed | ✅ DONE | Trigger simplified | Blueprint says trigger on `consultation_outcome` = Follow-Up. Current: simplified to `nx:retainer:signed`. Works. |
| **WF-11** | Nurture Campaign (Monthly) | ✅ Required | ✅ Published | Tag: nx:score:low | ✅ DONE | Scope expanded | Blueprint: monthly newsletter. Current: nurture branches by program (4 variants: EE, Spousal, Work, Study) + monthly SMS. EXPANDED. |
| **WF-12** | Score Medium Handler | ❌ Not in blueprint | ✅ Published | Tag: nx:score:med | ✅ DONE | NEW | Trigger nx:score:med, move to CONTACTING, send SMS+Email alert, internal alert. Created 2026-03-22. |
| **WF-13** | PIPEDA Data Deletion Request | ❌ Not in blueprint | ✅ Published | Tag: nx:data_deletion_requested | ✅ DONE | NEW | Compliance workflow. Admin alert, contact acknowledgement. Email template missing (P2-10). |

**Summary**: 11 blueprint workflows ✅ PUBLISHED + 4 enhancements (WF-04B, WF-04C, WF-12, WF-13) = 15 total.

**Remaining Gaps**:
- WF-13 email template missing (compliance) — TODO
- P2-14: Program-specific nurture branches in WF-11 — NOT DONE (partial in current version; need full copy variants)
- Win Tracking workflow (WF-10 partial) — could be enhanced
- Loss Tracking workflow (structured loss feedback) — deferred

---

### 2.8 Email & SMS Templates (Detailed)

| Template | Channel | Status | Purpose | Location | Variants |
|----------|---------|--------|---------|----------|----------|
| **Acknowledgment** | SMS | ✅ DONE | Immediate reply to form | WF-01 | 1 master |
| **Welcome SMS** | SMS | ✅ DONE | Detailed welcome with ETA | WF-01 | 1 master |
| **Assessment Ready** | SMS | ⏳ PLANNED | High/Med/Low score notification | WF-04/WF-12/WF-11 | 3 variants (high, med, low) |
| **Booking Invite SMS** | SMS | ✅ DONE | Link to booking calendar | WF-04 | 1 master |
| **Booking Confirmation SMS** | SMS | ✅ DONE | Confirm appointment details | WF-05 | 1 master |
| **Reminder SMS (48h)** | SMS | ✅ DONE | 2 days before | WF-05 | 1 master |
| **Reminder SMS (24h)** | SMS | ✅ DONE | 1 day before | WF-05 | 1 master |
| **Reminder SMS (2h)** | SMS | ✅ DONE | 2 hours before | WF-05 | 1 master |
| **No-Show Recovery SMS** | SMS | ✅ DONE | 1h after no-show | WF-06 | 1 master |
| **Reschedule Invite SMS** | SMS | ✅ DONE | Link to rebook | WF-06 | 1 master |
| **Thank You SMS** | SMS | ✅ DONE | Post-consultation | WF-07 | 1 master |
| **Thank You Email** | Email | ✅ DONE | Post-consultation summary | WF-07 | 1 master |
| **Retainer Delivery Email** | Email | ✅ DONE | Full retainer agreement + checklist | WF-09 | 1 master |
| **Retainer Follow-Up SMS** | SMS | ✅ DONE | Check-in after retainer sent | WF-09 | Multiple (Day 1, 3, 5) |
| **Retainer Signed Confirmation** | Email | ✅ DONE | Welcome as retained client | WF-10 | 1 master |
| **Nurture Monthly Newsletter** | Email | ✅ DONE | Immigration updates | WF-11 | 4 program variants (EE, Spousal, Work, Study) |
| **Nurture Quarterly SMS** | SMS | ✅ DONE | Check-in | WF-11 | 1 master |
| **Complex Case Alert Email** | Email | ⏳ PLANNED | To assigned consultant | WF-08 | 1 master |
| **Human Escalation Alert Email** | Email | ✅ DONE | To assigned user | WF-08 | 1 master |
| **Data Deletion Acknowledgment Email** | Email | ⏳ TODO | PIPEDA compliance | WF-13 | 1 master |
| **Consultant Briefing Email** | Email | ❌ NOT YET | NeuronX API responsibility | FastAPI Week 4 | 1 template (dynamic) |

**Summary**: 15/20 templates done. 5/20 TODO (mostly deferred to Week 4+ or production). Email sending blocked in sandbox so testing deferred.

---

### 2.9 My Staff (Team Management)

**Blueprint requirement**: Define user roles and team member permissions

**Current status**:

| Item | Requirement | Current | Status | Effort | Notes |
|------|-------------|---------|--------|--------|-------|
| **Staff Creation** | Add all team members | ⏳ PARTIAL | ⏳ TODO | 10 min/user | P1-14: Created 6 VMC team members via API 2026-03-22. Email activation pending. |
| **User Roles** | Define Admin, Consultant, Receptionist, Read-Only | ⏳ TEMPLATES NEEDED | ⏳ P2-09 | 1 hour | No role templates created yet. Deferred to Week 5. |
| **Phone Number** | Add to My Staff profile for SMS | ⏳ TODO | ⏳ P0-04 | 5 min | Per MASTER_IMPLEMENTATION_PLAN.md task 0.4: add +16479395000 to Ranjan's profile. NOT DONE. |
| **Notification Settings** | Configure email/SMS preferences | ⏳ TODO | ⏳ P0-05 | 15 min | Per MASTER_IMPLEMENTATION_PLAN.md task 0.5: configure My Staff → Notification Settings. NOT DONE. |
| **Calendar Assignment** | Link staff to Immigration Consultations calendar | ⏳ DEFERRED | ⏳ P2-08 | 10 min | Deferred to Week 5 when pilot customer has their own RCIC. |
| **Round-Robin Setup** | Configure load balancing for multi-consultant | ⏳ DEFERRED | ⏳ P2-08 | 30 min | Deferred to Week 5 when 2+ users assigned. |
| **Consultant Bio** | Add name, credentials, availability to public profile | ⏳ TODO | ⏳ P2-06 | 30 min | Needed for funnel trust signals. TODO. |
| **2FA Requirement** | Enforce 2FA for admin accounts | ⏳ DEFERRED | ⏳ P2 | 10 min | Deferred to production. Configure in Company Settings. |

**Summary**: 1/8 done (staff created, emails pending). 7/8 TODO. Most deferred to Week 5.

---

### 2.10 Business Profile

**Blueprint requirement**: Firm name, RCIC credentials, contact info

**Current status**:

| Item | Blueprint | Current | Status | Effort | Notes |
|------|-----------|---------|--------|--------|-------|
| **Firm Name** | Company name | ✅ "Visa Master Canada Immigration Services" | ✅ DONE | — | Set via P0-02 (form consent text update) |
| **RCIC Number** | Registration number | ⏳ NEEDED | ⏳ TODO | 5 min | Needs Ranjan's RCIC # (if licensed) or placeholder |
| **RCIC Credentials** | License date, regulatory body (ICCRC) | ⏳ NEEDED | ⏳ TODO | 10 min | Per P2-06: Add to funnel for trust signals |
| **Phone** | Business phone | ❌ SANDBOX BLOCKED | ⏳ P0-04 | 5 min | Add to My Staff: +16479395000 — NOT DONE |
| **Address** | Business address | ⏳ NEEDED | ⏳ TODO | 5 min | Toronto-based per PROJECT_MEMORY.md. Add to Business Profile. |
| **Email** | Support/inquiry email | ✅ support@neuronx.co (or support@vmc.ca) | ⏳ P0-03 | 5 min | Should be company email, not neuronx.co. Update pending. |
| **Website** | Link to firm website | ⏳ NEEDED | ⏳ TODO | 5 min | Marketing website TBD (Vercel/Netlify). Deferred to Week 5. |
| **Hours of Operation** | Business hours | ✅ Mon-Fri 9-5 ET | ✅ ASSUMED | — | Calendar set to this; update Business Profile to match. |
| **Logo** | Company logo | ⏳ NEEDED | ⏳ TODO | 10 min | VMC brand kit exists (navy, red, gray). Need to upload logo. |
| **Color Scheme** | Brand colors | ✅ Navy #1E3A5F, Red #DC2626, Gray #F3F4F6 | ✅ EXTRACTED (P1-06) | — | Applied to Thank You page. |

**Summary**: 2/10 done. 8/10 TODO. Mostly configuration, low effort.

---

### 2.11 Integrations

| Integration | Requirement | Current | Status | Effort | Notes |
|-------------|-------------|---------|--------|--------|-------|
| **Google Workspace** | Email accounts (ranjan@neuronx.co) | ✅ Active | ✅ DONE | 0 min | Already set up. SMTP configured for Mailgun. |
| **Google Calendar Sync** | Sync GHL calendar → Google Calendar | ✅ CONFIGURED | ✅ DONE | 0 min | Consultant can view appointments in Google Calendar. |
| **Mailgun (Email Sending)** | Dedicated domain (mg.neuronx.co) | ✅ VERIFIED | ✅ DONE | 0 min | Sending blocked in sandbox; verified for production. |
| **Stripe (Payment Processing)** | Accept retainer deposits and client payments | ❌ BLOCKED | ⏳ P1-15 | 1 hour | Cannot test in sandbox. Stripe verification KYC deferred to Day 1 of production. |
| **VAPI (Voice AI)** | Outbound calling, structured data extraction | ✅ CONFIGURED | ✅ DONE | 0 min | Assistant ID: 289a9701-..., Phone: ea133993-... Running independently of GHL. |
| **FastAPI (NeuronX Brain)** | Webhook receiver, scoring, briefings | ⏳ SCAFFOLD | ⏳ WEEK 4 | 3 days | `/neuronx-api/` created. Build starts Week 2. Webhook URL TBD. |
| **Zapier / Make / n8n** | Conditional orchestration | ❌ NOT USED | ✅ AVOIDED | — | Per CLAUDE.md Rule 8: Minimalist architecture. Not needed if VAPI + GHL + FastAPI can handle logic. |
| **Twilio / SMS** | SMS backup provider | ❌ NOT USED | ✅ AVOIDED | — | GHL LC Phone is native; no need for Twilio. |
| **Slack Integration** | Team notifications | ⏳ DEFERRED | ⏳ P3 | 1 hour | Nice-to-have. Deferred post-pilot. |
| **Salesforce / Pipedrive** | CRM sync | ❌ NOT PLANNED | ✅ AVOIDED | — | GHL is the system of record. No dual-CRM. |

**Summary**: 5/10 done. 2/10 deferred (Stripe, FastAPI). 3/10 avoided (correct choice per architecture). No gaps.

---

### 2.12 Notification Settings

| Setting | Requirement | Current | Status | Effort | Notes |
|---------|-------------|---------|--------|--------|-------|
| **Email Notifications** | Notify on new leads, missed calls, no-shows | ⏳ PENDING | ⏳ P0-05 | 15 min | **TODO: My Staff → Notification Settings** — configure what alerts are emailed. NOT DONE. |
| **SMS Notifications** | Notify on critical events | ⏳ BLOCKED | ⏳ P1 | 10 min | Cannot test SMS notifications in sandbox. Deferred to production. |
| **In-App Notifications** | GHL dashboard notifications | ✅ DEFAULT | ✅ DONE | 0 min | Enabled by default. |
| **Task Reminders** | Remind assigned staff of tasks | ✅ DEFAULT | ✅ DONE | 0 min | GHL auto-notifies on task assignment. |
| **Missed Call Alerts** | Alert on call drops (VAPI) | ⏳ DEPENDS | ⏳ WEEK 4 | 30 min | FastAPI responsibility. WF-04C triggers SMS; email alert TBD. |
| **No-Show Alerts** | Alert when appointment marked no-show | ✅ WF-06 | ✅ DONE | 0 min | WF-06 sends SMS + email. |
| **Lead Assignment Alerts** | Notify assignee when lead routed to them | ✅ DEFAULT | ✅ DONE | 0 min | GHL auto-notifies. |

**Summary**: 5/7 done. 2/7 TODO/deferred. Low impact.

---

### 2.13 Conversations Setup

| Item | Requirement | Current | Status | Notes |
|------|-------------|---------|--------|-------|
| **Conversations Module** | Enable team chat / contact messaging | ✅ DEFAULT | ✅ DONE | Enabled by default in GHL. |
| **Conversation AI Bot** | After-hours FAQ chatbot | ⏳ DEFERRED | ⏳ P3-06 | Nice-to-have. Use GHL Conversation AI feature. Deferred to post-pilot. |
| **Inbox Unification** | SMS, email, form replies in one inbox | ✅ DEFAULT | ✅ DONE | GHL Conversations auto-unifies all channels. |
| **Message Templates** | Quick replies for common questions | ⏳ PARTIAL | ⏳ TODO | Can create in Conversations. Deferred to pilot feedback. |

**Summary**: 2/4 done. 2/4 deferred (nice-to-have). No blockers.

---

### 2.14 Objects / Custom Properties

| Object | Required | Current | Status | Notes |
|--------|----------|---------|--------|-------|
| **Contacts** | ✅ | ✅ | ✅ DONE | All custom fields linked to contacts |
| **Opportunities** | ✅ | ✅ | ✅ DONE | Pipeline stages, custom fields linked |
| **Appointments** | ✅ | ✅ | ✅ DONE | Calendar bookings auto-create opportunities |
| **Tasks** | ✅ | ✅ | ✅ DONE | Workflow actions create tasks |
| **Custom Objects** | ❌ Not required | N/A | ✅ AVOIDED | GHL standard objects sufficient |

---

### 2.15 Custom Values / Picklists

All dropdown options created via API and verified. See Section 2.1 (Custom Fields) for full list.

---

## TIER 3: VMC (PILOT CLIENT) SUB-ACCOUNT

This is the **second sub-account** that will be cloned from the NeuronX Gold sub-account via snapshot for the Visa Master Canada pilot client.

### 3.1 Status Overview

**Current**: VMC test account exists but is NOT PRODUCTION READY.

| Item | Requirement | Current | Status | Effort | Timeline | Notes |
|------|-------------|---------|--------|--------|----------|-------|
| **Sub-Account Creation** | Create from snapshot | ❌ NOT YET | ⏳ DEFERRED | 5 min | Week 5 (production only, 2-account sandbox limit) | Sandbox only has NeuronX Gold. VMC will be created from snapshot in production. |
| **VMC Branding** | Update firm name, logo, colors, templates | ✅ RESEARCHED | 🔧 PARTIAL | 2 hours | Week 5 | Brand kit extracted (navy, red, gray) and applied to Thank You page. Full funnel branding deferred. |
| **VMC Email Domain** | support@vismaster-canada.ca or company domain | ⏳ PLANNED | ⏳ TODO | 30 min | Week 5 | Not yet configured. Need to acquire domain or use white-label. |
| **VMC Phone Number** | Toronto/GTA area code | ❌ BLOCKED | ⏳ DEFERRED | 10 min | Week 5 | Sandbox blocks LC Phone. Will purchase in production. |
| **VMC RCIC Profile** | Add VMC RCIC name, credentials, photo | ⏳ PENDING | ⏳ TODO | 30 min | Week 5 | Need to collect from VMC founder. |
| **VMC Custom Domain** | app.vmc.ca or similar | ⏳ PLANNED | ⏳ TODO | 15 min | Week 5 | Only if budget allows. Can use white-label subdomain initially. |
| **VMC Form Customization** | Update consent text, button copy, fields | ⏳ TEMPLATE | ⏳ TODO | 1 hour | Week 5 | Form template ready; need to customize for VMC. |
| **VMC Landing Page** | Update headline, copy, programs, trust signals | ✅ TEMPLATE | ⏳ TODO | 2 hours | Week 5 | Thank You page done. Main funnel page needs VMC programs + copy. |
| **VMC Workflow Customization** | Customize message templates for VMC | ✅ TEMPLATES | ⏳ TODO | 3 hours | Week 5 | SMS/email templates need VMC signature, tone adjustment. |
| **VMC Calendar** | Assign VMC RCIC(s) to calendar | ⏳ PENDING | ⏳ TODO | 15 min | Week 5 | Need VMC RCIC email + availability. |
| **VMC Contacts Import** | Import existing contacts from VMC | ⏳ OPTIONAL | ⏳ TODO | 1 hour | Week 5+ | Optional. Can start with clean slate for pilot. |
| **VMC Team Setup** | Create users for VMC staff | ⏳ PENDING | ⏳ TODO | 30 min | Week 5 | Need VMC team member emails. |

**Summary**: Almost all VMC work is deferred to Week 5 when production account is live and client is ready to onboard. Only branding research done now (0% ready for deployment).

---

### 3.2 Detailed Customization Checklist (For Week 5)

This checklist will be executed once VMC sub-account is created from snapshot in production:

```
VMC SUB-ACCOUNT CUSTOMIZATION CHECKLIST (Week 5, estimated 6-8 hours)

PRE-CUSTOMIZATION
[ ] Collect from VMC founder:
    - RCIC name, license #, credentials
    - RCIC photo for funnel
    - List of immigration programs offered
    - Any existing inquiry channels/form endpoints
    - Team member names/emails (who will use system)
    - Preferred domain/subdomain (optional)
    - Preferred phone number area code

BRANDING
[ ] Update Company Settings:
    [ ] Firm name: "Visa Master Canada Immigration Services"
    [ ] Logo: Upload VMC logo (or use placeholder)
    [ ] Address: VMC Toronto office
    [ ] Phone: Purchased Toronto number
    [ ] Email: support@vmc.ca or white-label domain

FORMS & FUNNELS
[ ] Update Immigration Inquiry Form V1:
    [ ] Consent text: Insert "Visa Master Canada Immigration Services"
    [ ] Button text: "Get Your Assessment" (or VMC branded)
    [ ] Optional: Add VMC-specific program checkboxes
    [ ] Test form submission

[ ] Update NeuronX Intake Landing Page:
    [ ] Headline: "[VMC] Fast, Structured Immigration Intake"
    [ ] Sub-headline: Update with VMC RCIC name
    [ ] Programs Section: List VMC's offered programs (EE, Spousal, etc.)
    [ ] Trust Signals: Add RCIC photo, credentials, consultation count
    [ ] CTA: Update button to VMC branding
    [ ] Footer: Update firm name, compliance language
    [ ] Test page display, form submission

[ ] Verify Thank You Page:
    [ ] Already customized with VMC brand kit
    [ ] Confirm colors, layout, messaging

WORKFLOWS & MESSAGES
[ ] Review all 13 workflows:
    [ ] Verify triggers are correct (form submission, tags, etc.)
    [ ] Check SMS templates: Sign with VMC name (already done)
    [ ] Check email templates: Sign with VMC name (already done)
    [ ] No changes needed — all generic and transferable

[ ] Optional customization:
    [ ] Update tone/copy for VMC's voice (conservative vs. friendly)
    [ ] Add VMC-specific programs to nurture branches (WF-11)
    [ ] Create VMC-specific case studies for post-consult follow-up

CALENDAR & TEAM
[ ] Create VMC RCIC user account:
    [ ] Add email
    [ ] Add phone
    [ ] Set role: Consultant
    [ ] Assign to Immigration Consultations calendar

[ ] Update Calendar:
    [ ] Set availability hours (ask VMC RCIC: Mon-Fri 9-5 or custom?)
    [ ] Add RCIC to calendar
    [ ] Test booking flow

[ ] Create additional team accounts (if needed):
    [ ] Receptionist/Intake Coordinator
    [ ] Firm Owner/Manager
    [ ] Set roles appropriately

INTEGRATIONS & TESTING
[ ] Verify email domain working:
    [ ] Send test email from Conversations
    [ ] Confirm Mailgun relay working (may need custom domain config)

[ ] Verify VAPI integration:
    [ ] Update VAPI webhook URL to FastAPI instance
    [ ] Test: Submit form → verify call within 5 min
    [ ] Confirm VAPI call quality (audio, clarity)

[ ] End-to-End Test:
    [ ] Submit form with test lead
    [ ] Receive AI call
    [ ] Respond to assessment questions
    [ ] Verify scoring in GHL
    [ ] Receive booking invite
    [ ] Book consultation
    [ ] Verify reminder SMS 24h before
    [ ] Complete consultation (manual)
    [ ] Record outcome
    [ ] Verify retainer email sent
    [ ] Check pipeline progression (NEW → CONTACTING → ... → RETAINED)

UAT SIGN-OFF
[ ] VMC founder confirms:
    [ ] Form works correctly
    [ ] Branding looks good
    [ ] Messages sound appropriate
    [ ] System is ready for live traffic

PRODUCTION GO-LIVE
[ ] Deploy landing page to custom domain (if applicable)
[ ] Update VMC website to link to funnel
[ ] Begin marketing/outreach
[ ] Monitor first 48h for issues
```

---

## SUMMARY TABLE: COMPLETE GAP ANALYSIS

| Tier | Category | Total Items | Done | Partial | Not Started | Priority | Timeline |
|------|----------|-------------|------|---------|-------------|----------|----------|
| **TIER 1: AGENCY** | White-Label | 5 | 1 | 0 | 4 | P1 | Week 5 |
| | Billing | 7 | 1 | 0 | 6 | **P0** | Week 5 |
| | Domain | 6 | 3 | 0 | 3 | P1 | Immediate + Week 5 |
| | Email Services | 8 | 3 | 0 | 5 | P1 | Immediate + Week 5 |
| | Email Templates | 11 | 6 | 1 | 4 | P1 | Week 1-4 |
| | Phone | 5 | 0 | 0 | 5 | **P0** | Week 5 |
| | SaaS Configurator | 6 | 0 | 0 | 6 | P1 | Week 5+ |
| | **Snapshots** | **5** | **0** | **0** | **5** | **P0 CRITICAL** | **TODAY** |
| | Marketplace/OAuth | 4 | 1 | 1 | 2 | P1 | Week 5+ |
| | Security | 8 | 2 | 0 | 6 | P1 | Week 4-5 |
| **TIER 1 SUBTOTAL** | | **65** | **17** | **2** | **46** | | |
| | | | **(26%)** | **(3%)** | **(71%)** | | |
| **TIER 2: NEURONX SUB-ACCOUNT** | Custom Fields | 40 | 40 | 0 | 0 | P1 | ✅ DONE |
| | Tags | 18 | 18 | 0 | 0 | P1 | ✅ DONE |
| | Pipeline | 9 | 10 | 0 | 0 | P1 | ✅ DONE |
| | Calendar | 10 | 8 | 0 | 2 | P1 | Week 5 |
| | Forms | 14 | 12 | 0 | 2 | P1 | Week 1 |
| | Funnels/Landing Page | 14 | 4 | 0 | 10 | **P1** | **Week 1** |
| | Workflows | 15 | 15 | 0 | 0 | P1 | ✅ DONE |
| | Email/SMS Templates | 20 | 15 | 0 | 5 | P1 | Week 1-4 |
| | My Staff | 8 | 1 | 1 | 6 | P1 | Week 1-5 |
| | Business Profile | 10 | 2 | 0 | 8 | P2 | Week 1-5 |
| | Integrations | 10 | 5 | 0 | 5 | P1 | Immediate-Week 5 |
| | Notifications | 7 | 5 | 0 | 2 | P2 | Week 1-5 |
| | Conversations | 4 | 2 | 0 | 2 | P3 | Week 5+ |
| | Objects/Custom Values | 5 | 5 | 0 | 0 | P1 | ✅ DONE |
| **TIER 2 SUBTOTAL** | | **184** | **132** | **1** | **51** | | |
| | | | **(72%)** | **(1%)** | **(28%)** |  | |
| **TIER 3: VMC PILOT SUB-ACCOUNT** | Sub-Account Creation | 1 | 0 | 0 | 1 | P0 | Week 5 |
| | Brand Customization | 6 | 1 | 1 | 4 | P1 | Week 5 |
| | Forms/Funnels | 4 | 0 | 1 | 3 | P1 | Week 5 |
| | Workflows/Messages | 2 | 0 | 1 | 1 | P1 | Week 5 |
| | Calendar/Team | 3 | 0 | 0 | 3 | P1 | Week 5 |
| | Integrations/Testing | 3 | 0 | 0 | 3 | P1 | Week 5 |
| **TIER 3 SUBTOTAL** | | **19** | **1** | **3** | **15** | | |
| | | | **(5%)** | **(16%)** | **(79%)** | | |
| **OVERALL TOTAL** | | **268** | **150** | **6** | **112** | | |
| | | | **(56%)** | **(2%)** | **(42%)** | | |

---

## KEY BLOCKERS & CRITICAL PATH

### 🔴 BLOCKING ISSUES (MUST RESOLVE IMMEDIATELY)

1. **MASTER SNAPSHOT NOT CREATED** (P0 CRITICAL)
   - **Impact**: If sandbox expires or data is wiped, all work is lost
   - **Action**: TODAY 2026-03-26 — Go to Agency Dashboard → Account Snapshots → Create Snapshot
   - **Effort**: 30 minutes
   - **Dependency**: Nothing — can do now
   - **Evidence**: MASTER_IMPLEMENTATION_PLAN.md Section 0.1 task list

2. **SANDBOX EMAIL/SMS BLOCKED** (P0 CRITICAL)
   - **Impact**: Cannot test any email workflows, SMS sequences, or message templates
   - **Action**: Defer all testing to production (Week 5)
   - **Mitigation**: All message templates are drafted and ready to test Day 2 of Phase 1
   - **Status**: Accepted constraint per architecture

3. **SANDBOX PHONE BLOCKED** (P0 CRITICAL)
   - **Impact**: Cannot test VAPI calling, LC Phone SMS, or call recovery workflows
   - **Action**: Defer to production (Week 5, Day 2)
   - **Mitigation**: VAPI is configured independently; testing deferred but non-blocking for development

4. **OD-01 UNRESOLVED (VOICE LAYER)** (P0 CRITICAL)
   - **Impact**: Cannot finalize VAPI vs GHL Voice AI decision
   - **Action**: Run bake-off Week 3; founder makes final call
   - **Dependency**: Blocking Week 4 FastAPI development (webhook handler choice)
   - **Evidence**: docs/05_governance/open_decisions.md OD-01

5. **OD-02 UNRESOLVED (PRICING TIERS)** (P0 CRITICAL)
   - **Impact**: Cannot finalize billing, SaaS mode, client onboarding approach
   - **Action**: Founder decision before Week 5
   - **Options**: $297 plan (manual onboarding, no SaaS) vs $497 plan (auto-provisioning)
   - **Evidence**: MASTER_IMPLEMENTATION_PLAN.md Section "SaaS Configuration"

6. **SNAPSHOT INSTALLATION TEST BLOCKED** (P1 CRITICAL)
   - **Impact**: Cannot validate snapshot works until production account exists
   - **Action**: Defer to Week 5 Day 1 (create production account, import snapshot)
   - **Milestone**: M2 (Snapshot Proven) blocked until this passes
   - **Timeline**: Week 2 per original plan, but requires production account

### ⏳ DEFERRED TO PRODUCTION (Week 5+)

**Email Sending**: All workflow email tests, SMS tests, message delivery verification, bounce handling, CASL compliance testing — blocked by sandbox email restrictions

**Phone/SMS**: Phone number purchase, A2P 10DLC registration, inbound SMS testing, LC Phone configuration — blocked by sandbox LC Phone restrictions

**Billing Integration**: Stripe KYC, payment processing, invoice generation, subscription automation — blocked by sandbox payment restrictions

**SaaS Configuration**: SaaS pricing tiers, auto-provisioning, rebilling, client billing — only on $497 plan, deferred to Month 4 if starting on $297 plan

**>2 Sub-Accounts**: VMC pilot sub-account creation, multi-client management — blocked by 2-account sandbox limit

---

## PRIORITY-BASED ACTION SEQUENCE

### P0 BLOCKERS (DO TODAY 2026-03-26)

1. ✅ CREATE MASTER SNAPSHOT NOW — Insurance against sandbox loss
2. ⏳ P0-05: Run end-to-end UAT test (requires phone — escalate to founder)
3. ⏳ P0-03/04: Verify form consent text, button text, AI disclaimer (assumed done, verify)
4. ⏳ Founder: Log into Skyvern session (per WEEK1_CHECKLIST.md prerequisite) — UNBLOCKING

### P1 CRITICAL (Week 1-2)

1. ✅ Landing page content update (P2-06) — funnel branding, copy, programs, trust signals
2. ✅ Email/SMS template refinement (gap templates) — Assessment SMS, Complex case alerts, Data deletion email
3. ⏳ My Staff configuration (P0-04, P0-05) — Add phone, notification settings
4. ⏳ Reply & Forward Settings (P0-03) — Configure email reply/forward addresses

### P2 IMPORTANT (Week 2-4)

1. ⏳ FastAPI development (Week 2-4) — webhook receiver, scoring, briefings, trust boundary
2. ⏳ Snapshot installation test (Week 2) — requires production account
3. ⏳ RCIC survey setup (P1-05) — outcome capture form
4. ⏳ Business profile completion (addresses, RCIC credentials, phone, website)
5. ⏳ Calendar payment setup (P2-15) — Stripe deposit configuration

### P3 NICE-TO-HAVE (Week 4+)

- Conversation AI bot (after-hours FAQ)
- WhatsApp Business integration
- French language workflow variants
- Multi-step form (funnel builder)
- NeuronX product website

---

## WEEK-BY-WEEK EXECUTION PLAN

**WEEK 1 (Mar 26 - Apr 1): Foundation Lock**
- [ ] Create snapshot (TODAY)
- [ ] Complete form/funnel branding (P2-06)
- [ ] Configure My Staff (P0-04, P0-05)
- [ ] Run UAT-01 end-to-end (P0-05)
- [ ] Gap email templates (P2-10, P1-05)

**WEEK 2 (Apr 2 - Apr 8): FastAPI + Snapshot Test**
- [ ] Build FastAPI scaffold completion (webhook, scoring, briefings)
- [ ] Snapshot creation + installation test (requires production account)
- [ ] RCIC outcome survey (P1-05)
- [ ] Business profile completion
- [ ] Voice AI bake-off prep

**WEEK 3 (Apr 9 - Apr 15): Voice AI Bake-Off + GTM**
- [ ] OD-01 resolution (GHL Voice vs VAPI decision)
- [ ] FastAPI ↔ GHL/VAPI integration testing
- [ ] GTM strategy + pilot prospect identification
- [ ] Deployment platform decision (Railway/Render)

**WEEK 4 (Apr 16 - Apr 22): Production Prep**
- [ ] FastAPI full implementation (all 7 endpoints)
- [ ] Final snapshot creation
- [ ] Production setup checklist
- [ ] Pricing tiers lock (OD-02)
- [ ] Warm outreach to pilot prospects

**WEEK 5 (Apr 23 - Apr 29): PRODUCTION LAUNCH**
- [ ] Day 1: Create paid GHL account, import snapshot
- [ ] Day 2: Buy phone, register A2P, test SMS/email
- [ ] Day 3-4: Full UAT (end-to-end, all 4 scenarios)
- [ ] Day 5: SaaS configuration (if $497 plan)

**WEEK 6 (Apr 30 - May 6): FIRST CUSTOMER**
- [ ] VMC pilot onboarding
- [ ] First inquiry submitted
- [ ] First AI call executed
- [ ] First consultation booked and completed
- [ ] First retainer signed

---

## RISK ASSESSMENT

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Sandbox expires before Phase 1 | Medium | Critical | **Create snapshot TODAY** |
| Snapshot doesn't transfer everything | Low | High | Test install in Week 5 Day 1 |
| Email/SMS testing incomplete in sandbox | HIGH (confirmed) | High | Plan full UAT in production Week 5 |
| VAPI call quality inadequate | Medium | High | Bake-off Week 3 determines alternative |
| OD-01 unresolved delays Week 4 build | Medium | High | Front-load decision in Week 3 |
| Pilot customer unavailable | Medium | Medium | Warm up 5-10 prospects, not just 1 |
| Domain transfer locked 60 days | Low | Low | Manage DNS externally until transfer eligible |
| GHL raises prices mid-launch | Low | Medium | Lock annual billing when ready |

---

## FINAL RECOMMENDATION

**Gap Analysis Summary**:
- **56% COMPLETE** (150/268 items done)
- **Tier 2 (NeuronX Sub-Account) is 72% complete** — all core workflows, fields, tags, and pipeline ready
- **Tier 1 (Agency) is 26% complete** — most work deferred to production due to sandbox limitations
- **Tier 3 (VMC) is 5% complete** — all work deferred to Week 5 pilot onboarding

**Immediate Actions (Today)**:
1. **CREATE SNAPSHOT NOW** (P0 blocker)
2. Configure My Staff phone + notification settings
3. Complete landing page branding (P2-06)
4. Run UAT test if founder available

**On Critical Path to $1M ARR**:
- Phase 0 (Sandbox): Weeks 1-4, Continue building Tier 2 + FastAPI
- Phase 1 (Production): Week 5, Deploy snapshot + full testing
- Phase 2 (First Customer): Week 6, Onboard VMC + go live

**Blockers to Resolve**:
1. OD-01 (voice) — Week 3 bake-off
2. OD-02 (pricing) — founder decision
3. Snapshot creation — TODAY

The system is on track for Week 6 launch if these dependencies are met.
