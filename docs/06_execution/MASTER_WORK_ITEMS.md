# NeuronX — Master Work Items (Combined Audit)
# Last Updated: 2026-03-22 ET
# Source: Claude API Audit + GHL Built-In AI Audit (14-Section) — MERGED & VERIFIED

## Priority Legend
- P0 = BLOCKING — must fix before any testing
- P1 = CRITICAL — must fix before pilot customer
- P2 = IMPORTANT — must fix before $1M ARR push
- P3 = NICE TO HAVE — enhance when time allows

---

## P0 — BLOCKING (5 items)

| # | Item | Owner | Effort | Status | Notes |
|---|------|-------|--------|--------|-------|
| P0-01 | Set calendar availability hours (Mon-Fri 9-5 ET) | Claude API | 5 min | ✅ DONE | API: PUT /calendars/ |
| P0-02 | Fix form consent checkbox placeholder text ([BUSINESS NAME]) | **RANJAN** | 10 min | ✅ DONE | Visa Master Canada Immigration Services |
| P0-03 | Add welcome SMS to WF-01 | **RANJAN+Claude** | 10 min | ✅ DONE | Welcome SMS added to WF-01 |
| P0-04 | Fix form button text from "Button" to "Get Your Free Assessment" | **RANJAN** | 5 min | ✅ DONE | Form builder UI only |
| P0-05 | Run end-to-end UAT test (submit form → verify call → verify pipeline) | **RANJAN** | 30 min | ⏳ TODO | Needs real phone |

## P1 — CRITICAL (15 items)

| # | Item | Owner | Effort | Status | Notes |
|---|------|-------|--------|--------|-------|
| P1-01 | Add PROPOSAL SENT pipeline stage | **RANJAN** | 5 min | ✅ DONE | Added between CONSULT COMPLETED and RETAINED |
| P1-02 | Build WF-02 retry loop (6 attempts over 48h) | **RANJAN+Claude** | 2 hours | ✅ DONE | 6-attempt sequence, VAPI webhooks, If/Else exits, UNREACHABLE fallback — Published 2026-03-22 |
| P1-03 | Add nx:score:med handler workflow | **RANJAN+Claude** | 30 min | ✅ DONE | WF-12 published — CONTACTING stage, SMS+Email+Internal alert, nx:score:med:actioned tag — 2026-03-22 |
| P1-04 | Rename WF-03 to "Unreachable Handler" or clarify purpose | **RANJAN** | 5 min | ✅ DONE | Renamed to "WF-03 Contact Success Handler" |
| P1-05 | Create RCIC Outcome Capture Survey (triggers WF-07) | **RANJAN+Claude** | 30 min | ✅ DONE | 5-field survey: Outcome, Program, Retainer Amount, Notes, Follow-Up Date — Saved 2026-03-22 |
| P1-06 | Add Thank You page to intake funnel | **RANJAN** | 20 min | ✅ DONE | Custom HTML/CSS built with VMC brand kit |
| P1-07 | Delete 3 junk custom fields (152dv, 168z3, 1qpb + 17fpb) | Claude API | 5 min | ✅ DONE | 4 fields deleted |
| P1-08 | Add `retainer_amount` MONETARY custom field | Claude API | 5 min | ✅ DONE | ID: j38iWDDCLu8I0aEVQMJV |
| P1-09 | Add `lost_reason` SINGLE_OPTIONS custom field | Claude API | 5 min | ✅ DONE | ID: PRrN4EF8B6svJNbQHzYa |
| P1-10 | Add `consultation_outcome` SINGLE_OPTIONS custom field | Claude API | 5 min | ✅ DONE | Already existed |
| P1-11 | Fix VAPI transfer number from UAE (+971) to Canadian | Claude API | 5 min | ✅ DONE | Now +16479315181 |
| P1-12 | Add AI disclaimer checkbox to intake form | **RANJAN** | 15 min | ✅ DONE | Checkbox mapped to ai_disclaimer_shown, Required |
| P1-13 | Set calendar buffer times (10 min post-buffer) | Claude API | 5 min | ✅ DONE | slotBuffer=10 |
| P1-14 | Create at least 1 test user in GHL | **RANJAN** | 10 min | ✅ DONE | All 6 VMC team members created via PIT API — awaiting email activation |
| P1-15 | Freeze WF-04B at stable version before snapshot | **RANJAN** | 5 min | ✅ DONE | Renamed to [v14-STABLE] |

## P2 — IMPORTANT (15 items)

| # | Item | Owner | Effort | Status | Notes |
|---|------|-------|--------|--------|-------|
| P2-01 | Build NeuronX FastAPI thin brain | Claude | 3 days | ⏳ Week 4 | Scoring + briefings + analytics |
| P2-02 | Add R2/R4/R5/R6 readiness scoring fields | Claude API | 30 min | ✅ DONE | r2_education_level, r4_budget_readiness, r5_language_ability, r6_family_situation |
| P2-03 | Fix 7 field types (r1→MULTIPLE, spouse→CHECKBOX, etc.) | Claude API | 30 min | ✅ DONE | Delete+recreate approach |
| P2-04 | Add 6 compliance fields | Claude API | 30 min | ✅ DONE | ai_disclaimer_shown, consent_ip, consent_form_version, data_deletion_requested, conflict_check_cleared, ai_disclaimer_timestamp |
| P2-05 | Create GHL Snapshot v1.0 | **RANJAN** | 2 hours | ⏳ Week 2 | Agency-level feature |
| P2-06 | Update landing page content | **RANJAN** | 2 hours | ⏳ Week 2 | Funnel builder UI |
| P2-07 | Build 5 reporting dashboards | **RANJAN+Claude** | 2 hours | ⏳ TODO | Reporting UI |
| P2-08 | Build round-robin calendar for multi-RCIC firms | **RANJAN** | 30 min | ⏳ Week 5 | Requires 2+ users first |
| P2-09 | Create user role templates (Admin, RCIC, Sales, Receptionist) | **RANJAN** | 1 hour | ⏳ Week 5 | Team management UI |
| P2-10 | Build PIPEDA data deletion request workflow | **RANJAN+Claude** | 1 hour | ⏳ Week 4 | Workflow editor UI |
| P2-11 | Add "How did you hear about us?" to intake form | **RANJAN** | 5 min | ✅ DONE | Single dropdown, 6 options, query key: how_did_you_hear |
| P2-12 | Add source tracking tags (nx:source:*) | Claude API | 10 min | ✅ DONE | 5 source tags created |
| P2-13 | Add loss reason tags (nx:lost:*) | Claude API | 10 min | ✅ DONE | 4 loss tags created |
| P2-14 | Build program-specific nurture branches in WF-11 | **RANJAN+Claude** | 2 hours | ✅ DONE | 9 branches (8 programs + default), dual triggers, published — 2026-04-04 |
| P2-15 | Connect Stripe for paid consultation deposits | **RANJAN** | 30 min | ⏳ Week 5 | Stripe account + GHL payments |

## P3 — NICE TO HAVE (10 items)

| # | Item | Owner | Effort | Status | Notes |
|---|------|-------|--------|--------|-------|
| P3-01 | WhatsApp Business integration | **RANJAN** | 2-5 days | ⏳ | Meta Business verification needed |
| P3-02 | French language workflow variants | Claude | 2 days | ⏳ | System prompt + workflow clones |
| P3-03 | Multi-step intake form (3-page funnel) | **RANJAN+Claude** | 1 day | ⏳ | Funnel builder UI |
| P3-04 | NeuronX product website (B2B SaaS sales page) | **RANJAN** | 2 days | ⏳ | Website builder |
| P3-05 | Client trust portal via GHL Memberships | **RANJAN+Claude** | 2 days | ⏳ | Memberships feature |
| P3-06 | GHL Conversation AI bot for after-hours FAQ | Claude | 2 hours | ⏳ | Settings → Conversation AI |
| P3-07 | Daily productivity notification workflow for managers | **RANJAN+Claude** | 1 hour | ⏳ | Workflow editor UI |
| P3-08 | Voicemail drop integration in WF-02 | **RANJAN** | 1 hour | ⏳ | LC Phone feature |
| P3-09 | Speed-to-lead SLA breach alert workflow | **RANJAN+Claude** | 30 min | ⏳ | Workflow editor UI |
| P3-10 | White-label mobile app configuration | **RANJAN** | 1 day | ⏳ | GHL white-label app |

---

## COMPLETION SUMMARY

| Priority | Total | Done | Remaining |
|----------|-------|------|-----------|
| P0 | 5 | 4 | **1 (UAT test)** |
| P1 | 15 | 15 | **✅ ALL DONE** |
| P2 | 15 | 8 | **7 (mix of UI + production)** |
| P3 | 10 | 0 | **10 (post-pilot)** |
| **TOTAL** | **45** | **27** | **18** |

### API-Automated (Prior Sessions): 14/45
### UI-Only Completed (2026-03-22): 8 additional items (P0-03, P1-06 + 6 already reflected above)
### Future Code (Week 4+): 5 items (FastAPI, PIPEDA workflow, nurture branches, French, Conversation AI)
### Future Setup (Week 5+): 9 items (Stripe, Round-Robin, Roles, WhatsApp, etc.)

---

## CALENDAR GAPS (From GHL AI Audit — Section 4)

| Setting | Current | Target | Status |
|---------|---------|--------|--------|
| Open Hours | Mon-Fri 9-5 ET | Mon-Fri 9-5 ET | ✅ DONE |
| Slot Buffer | 10 min | 10 min | ✅ DONE |
| Slot Duration | 30 min | 30 min | ✅ Already correct |
| Payment Mode | Not Live | Live with $100 CAD deposit | ⏳ P2-15 (Stripe needed) |
| Calendar Groups | None | "Immigration Consultants" | ⏳ P2-08 (users needed first) |
| Type | Standard | Round-Robin | ⏳ P2-08 (users needed first) |
| Pre-qualification Gate | None | Only CONSULT READY can book | ⏳ P2 (trigger link approach) |

## WORKFLOW GAPS (From GHL AI Audit — Section 2)

| Gap | Status | Notes |
|-----|--------|-------|
| WF-01 no welcome SMS | ✅ DONE | Welcome SMS added 2026-03-22 |
| WF-02 single attempt (no retry loop) | ✅ DONE | 6-attempt retry loop published 2026-03-22 |
| No Unreachable Handler workflow | ⏳ P1-04 | Rename WF-03 or create new |
| No PROPOSAL SENT workflow | ✅ DONE | Stage added 2026-03-22 |
| No RCIC outcome survey | ⏳ P1-05 | Survey builder |
| WF-04B at v14 (high risk) | ✅ DONE | Frozen as [v14-STABLE] 2026-03-22 |
| No program-specific nurture branches | ⏳ P2-14 | Week 4 |
| No Win Tracking workflow (revenue calc) | ⏳ New | Need to add — WF-10 partially covers |
| No Loss Tracking workflow (feedback) | ⏳ New | Need to add — currently goes to NURTURE |

## FORM GAPS (From GHL AI Audit — Section 5)

| Gap | Status | Notes |
|-----|--------|-------|
| Consent text has [BUSINESS NAME] placeholder | ✅ DONE | Updated to "Visa Master Canada Immigration Services" |
| Button text is generic "Button" | ✅ DONE | Updated to "Get Your Free Assessment" |
| No AI disclaimer checkbox | ✅ DONE | Mapped to ai_disclaimer_shown, Required |
| No "How did you hear about us?" field | ✅ DONE | 6-option dropdown, query key: how_did_you_hear |
| No multi-step form | ⏳ P3-03 | Enhancement |
| No conditional logic (program-specific fields) | ⏳ P3 | Enhancement |

## FUNNEL GAPS (From GHL AI Audit — Section 6)

| Gap | Status | Notes |
|-----|--------|-------|
| No Thank You page | ✅ DONE | Custom HTML/CSS built with VMC brand kit 2026-03-22 |
| No custom domain | ⏳ Week 5 | Per-client setup |
| No SEO configuration | ⏳ P2-06 | Part of landing page update |
| No tracking pixels | ⏳ P2-06 | Part of landing page update |
| URL slug is internal naming | ⏳ P2-06 | Change to /start or /assessment |

## COMPLIANCE GAPS (From GHL AI Audit — Section 13)

| Gap | Status | Notes |
|-----|--------|-------|
| Compliance fields created | ✅ DONE | 6 fields via API |
| Compliance tags created | ✅ DONE | nx:casl:compliant, nx:do_not_contact, nx:ai_disclaimer_shown |
| CASL consent form text fix | ✅ DONE | Updated to "Visa Master Canada Immigration Services" |
| PIPEDA data deletion workflow | ⏳ P2-10 | Week 4 |
| Conflict check workflow | ⏳ P2 | Week 4 |
| AI disclosure in form | ✅ DONE | Checkbox added, mapped to ai_disclaimer_shown |

## TAG NAMING CLEANUP (For Week 4 API Build)

| Currently Used | Planned/Standard | Action |
|---------------|-----------------|--------|
| nx:appointment:noshow | Keep as-is | Consistent with nx: prefix |
| nx:consult:done | Keep as-is | Consistent |
| nx:contacting:attempt1 | Keep as-is | Matches attempt2-6 |

## SNAPSHOT DEPLOYMENT CHECKLIST (Per New Client)

### Pre-Deployment
- [ ] Firm name, address, RCIC name, registration number
- [ ] Custom domain (if applicable)
- [ ] Stripe account credentials
- [ ] Google Workspace email (for SMTP)
- [ ] RCIC availability hours + timezone

### During Deployment (Target: 3 hours)
- [ ] Install snapshot
- [ ] Create sub-account with firm branding
- [ ] Assign phone number (LC Phone)
- [ ] Configure email sending domain + DNS
- [ ] Create RCIC user accounts
- [ ] Add users to round-robin calendar
- [ ] Set calendar availability hours
- [ ] Configure VAPI tenant API key
- [ ] Update WF-04B webhook URL for tenant
- [ ] Test: Submit test inquiry → Confirm WF-01 fires
- [ ] Test: Complete VAPI call → Confirm fields update
- [ ] Test: Book consultation → Confirm WF-05 fires

### Post-Deployment
- [ ] Send RCIC training video (Loom)
- [ ] Schedule 30-min onboarding call
- [ ] Add to NeuronX support channel
- [ ] Set monitoring alert if no leads in 14 days
