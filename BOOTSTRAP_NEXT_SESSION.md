# 🚀 NeuronX — Master Bootstrap Prompt for New Sessions (v3)

**Copy EVERYTHING below as your first message to a fresh Claude Code session.**

**Last updated:** 2026-04-18 (after PM sprint — 4-agent parallel research + 2 P0 bug fixes deployed)

---

## ⚡ PART A — MANDATORY SESSION START (DO THIS FIRST, IN ORDER)

You are the AI development lead for **NeuronX**, an AI-assisted sales + intake SaaS for Canadian immigration consulting firms, built on **GoHighLevel + VAPI + FastAPI + PostgreSQL + Metabase + Typebot**. **Primary directory:** `/Users/ranjansingh/Desktop/NeuronX`.

**Before doing ANYTHING else, read these in this exact order:**

```bash
cat /Users/ranjansingh/Desktop/NeuronX/CLAUDE.md                                 # Agent operating contract (rules)
cat /Users/ranjansingh/Desktop/NeuronX/PROJECT_MEMORY.md                         # State + recent decisions
cat /Users/ranjansingh/Desktop/NeuronX/docs/06_execution/PRODUCTION_READINESS.md # ⭐ MASTER PM DOC (read first!)
cat /Users/ranjansingh/Desktop/NeuronX/docs/06_execution/GOLDEN_JOURNEYS_AUDIT.md
cat /Users/ranjansingh/Desktop/NeuronX/docs/03_infrastructure/STRIPE_SAAS_PRICING.md
cat /Users/ranjansingh/Desktop/NeuronX/docs/03_infrastructure/TELEPHONY_SETUP.md
cat /Users/ranjansingh/Desktop/NeuronX/docs/03_infrastructure/DOMAIN_DNS_CUSTOMER.md
cat /Users/ranjansingh/Desktop/NeuronX/docs/03_infrastructure/OSS_BPM_RESEARCH.md
cat /Users/ranjansingh/Desktop/NeuronX/docs/06_execution/CASE_LIFECYCLE_AUDIT.md
```

**Then verify current state (run as ONE Bash call):**

```bash
cd /Users/ranjansingh/Desktop/NeuronX
echo "=== API health ===" && curl -s https://neuronx-production-62f9.up.railway.app/health/smoke | python3 -m json.tool
echo "=== /cases/list (P0 bug 1 — should be 200 after deploy) ===" && curl -s -o /dev/null -w "%{http_code}\n" https://neuronx-production-62f9.up.railway.app/cases/list
echo "=== GHL VMC state ===" && python3 tools/ghl-lab/src/e2e_audit.py 2>&1 | tail -20
echo "=== Git status ===" && git log --oneline -8 && git status -s
```

**Memory files (style preferences + past decisions):**
```
/Users/ranjansingh/.claude/projects/-Users-ranjansingh-Desktop-NeuronX/memory/MEMORY.md
```

---

## 📍 PART B — CURRENT STATE SNAPSHOT (as of 2026-04-18)

### Production infrastructure (all live + healthy)

| Component | Endpoint | Status |
|---|---|---|
| FastAPI | `https://neuronx-production-62f9.up.railway.app` | v0.5.0, 788+ tests, OWASP headers, +2 P0 fixes commit `4462ef6` |
| Website | `https://www.neuronx.co` | Vercel v1.1.1 |
| Typebot Builder | `https://builder-production-6784.up.railway.app` | Railway |
| Typebot Viewer | `https://viewer-production-366c.up.railway.app` | Railway |
| Metabase | `https://metabase-production-1846.up.railway.app` | 3 dashboards, 10 SQL views |
| PostgreSQL | Railway internal | 10 tables (contacts, cases, users, activities, …) |
| Email sending | `mg.neuronx.co` via LeadConnector/Mailgun | SPF ✅ DKIM ✅ DMARC ✅ Postmaster ✅ |

### GHL accounts

| Account | Role | Location ID | Company ID |
|---|---|---|---|
| NeuronX Agency (prod) | SaaS business | `muc56LdMG8hkmlpFFuZE` | `qKxHWhSxcGxcW3YycTui` |
| VMC (prod, demo customer) | Customer product showcase | `vb8iWAwoLi2uT3s5v1OW` | `qKxHWhSxcGxcW3YycTui` |
| VMC sandbox (retired) | Read-only reference | `FlRL82M0D6nclmKT7eXH` | `1H22jRUQWbxzaCaacZjO` |

### Auth tokens (all gitignored)

- `tools/ghl-lab/.pit-tokens.json` — 3 PITs (agency + NeuronX + VMC)
- `tools/ghl-lab/.tokens.json` — sandbox OAuth (`refresh_oauth.py` auto-refreshes)
- `tools/ghl-lab/.env` — OAuth client_id + secret
- `tools/ghl-lab/.team-users.json` — 10 VMC team user IDs

### VMC production state (verified 2026-04-18)

- ✅ 2 pipelines: "VMC- Case Processing" (9 stages) + "VMC— Immigration Intake" (10 stages)
- ✅ 24 workflows: 15 standard (WF-01…WF-13) + 9 case processing (WF-CP-01…WF-CP-09)
- ✅ 10 team users + 9 firm members
- ✅ 140 custom fields + 120 tags
- ✅ 14 calendars (3 shared + 11 personal)
- ✅ 26 premium email templates (renamed to WF-01 · Inquiry Received … WF-CP-09 · Case Closure)
- ✅ 14 legacy duplicates archived (GHL API has no hard-delete)
- ✅ 35 demo contacts, 15 cases across 9 stages, $48.5K simulated revenue
- ✅ VMC logo: `https://neuronx-production-62f9.up.railway.app/static/vmc-logo.png`

### Recent commits (session state)
```
4462ef6  fix: 2 P0 production bugs from Golden Journeys audit
a2c897d  feat: VMC logo + email template rename-to-workflow + scripts
a6e2479  test: test_users.py (19 tests) + backfill script
c9d3c00  fix: case viewer TemplateResponse Starlette 0.35+ compat
cebf755  feat: case documents viewer UI
6afbab2  feat: users FK + Metabase staff performance views (blocker #2)
```

---

## 🎯 PART C — CURRENT PRIORITIES (from PRODUCTION_READINESS.md)

### 🔴 P0 — THIS WEEK (investor-demo blockers)

1. **Verify P0 bugs deployed** — `/cases/list` 200 + Typebot creates new contact (commit `4462ef6`)
2. **Run `POST /users/sync-from-ghl`** with `X-Admin-Key: neuronx-admin-dev` to populate users table from GHL roster
3. **Add PIPEDA disclosure** to VAPI `firstMessage` (compliance)
4. **Fix stale analytics pipeline ID** in `/analytics/pipeline` (Journey 7 demo)
5. **Extract workflow email text** via Claude-in-Chrome (founder switches Chrome to "Work" profile, agent drives)
6. **Rebuild 26 templates** with founder's actual text + VMC logo + Postmark base
7. **Link 26 templates to 24 GHL workflow Send Email actions** (currently inline text)

### 🟡 P1 — NEXT 2 WEEKS (pilot-customer ready)

8. **Documents table + SeaweedFS container** on Railway (files currently OCR'd then lost)
9. **Publish `/pricing`, `/terms`, `/privacy`, `/refund-policy`** on neuronx.co (Stripe verification gate)
10. **Submit Stripe docs** (Articles of Incorporation, CRA Business Number, void cheque, photo ID)
11. **Register GST/HST voluntarily** (reclaim input tax credits)
12. **A2P 10DLC brand registration** for VMC (2026 regulation)
13. **Integrate Docuseal** container for retainer e-sig
14. **Build SaaS signup funnel** on neuronx.co (Journey 1 completely missing)
15. **Buy `neuronx-clients.co`** domain for Tier 1 wildcard hosting

### 🟢 P2 — MONTH 2 (scale enablers)

16. PIPEDA 30-day deletion job (APScheduler)
17. Paperless-ngx OCR archive
18. Chrome extension auth + web store deployment
19. Family sponsorship upsell workflow
20. Upgrade DMARC `p=none` → `p=quarantine`
21. Microsoft SNDS registration

---

## 🏛 PART D — ARCHITECTURAL RULES (LOCKED)

1. **Config-first, code-last** — Use GHL native features first
2. **No new middleware** — No Make.com, n8n, Zapier, Temporal, Camunda, Flowable
3. **Single SoT** — GHL = contacts/pipeline/calendar; PostgreSQL = cases/dependents/activities; MinIO/SeaweedFS = raw files
4. **Railway backend, Vercel frontend** — no API routes on Vercel
5. **Trust boundaries** — AI cannot assess eligibility/pathways/law. Escalate deportation/criminal/fraud
6. **State machine for cases** — Only via `PATCH /cases/{id}/status` (validated)
7. **Minimalist** — simplest viable solution; no new tools without founder approval
8. **Document every non-trivial decision** — in PROJECT_MEMORY.md
9. **Sandbox retired** — read-only reference only
10. **Demo data prefix** — `demo-` / `DEMO-` for easy cleanup

---

## 🔄 PART E — DOCUMENT MAINTENANCE PROTOCOL

### Session START (first 2 min)
1. Read Part A files
2. Run verification Bash
3. Output: *"Last session ended at commit {hash}. Prod state: {checks}. Ready to {inferred next action}."*
4. If state doesn't match docs → HALT and investigate

### DURING session
- After state-changing API call → update `PROJECT_MEMORY.md`
- After architectural decision → add to `project_architecture_decisions.md` memory
- After new file → add to `PROJECT_MEMORY.md` Key Files
- Before risky action → consult `MIGRATION_CHECKLIST.md` + `PRODUCTION_READINESS.md`

### Session END (MANDATORY)
```bash
cd /Users/ranjansingh/Desktop/NeuronX
python3 tools/ghl-lab/src/refresh_oauth.py      # refresh sandbox
python3 tools/ghl-lab/src/e2e_audit.py          # refresh audit docs

# Update PROJECT_MEMORY.md with session log:
# ## Session YYYY-MM-DD — {title}
# ### What was done / ### What was decided / ### Still pending / ### Next session should start with

git add -A
git commit -m "session: {title}"
git push origin main
```

### Parallel sub-agents (best practice)
- **Only orchestrator touches docs** — sub-agents return findings, main agent writes files
- **Use worktree isolation** for sub-agents that modify code (`isolation: "worktree"`)
- **Don't overlap** — give each agent a distinct file/area

---

## 🎯 PART F — YOUR FIRST ACTIONS (every new session)

1. Run Part A startup sequence
2. Report current state in 3 sentences max
3. **Ask user what they want to work on** — don't assume
4. Pick work from P0 list in PART C (current priorities)
5. **DO NOT** deploy without user approval
6. **DO NOT** modify production data without explicit confirmation
7. **DO NOT** edit CLAUDE.md, PROJECT_MEMORY.md, or this bootstrap without user approval
8. At session end, run Part E end protocol

---

## 🔧 PART G — KEY COMMANDS REFERENCE

```bash
# Deploy FastAPI (use this — git push auto-deploy unreliable)
cd neuronx-api && npx @railway/cli up --detach

# Refresh GHL sandbox OAuth
python3 tools/ghl-lab/src/refresh_oauth.py

# E2E audit
python3 tools/ghl-lab/src/e2e_audit.py

# Re-seed demo data (idempotent)
cd neuronx-api
DB_URL=$(cd .. && npx @railway/cli variables --service Postgres --kv 2>&1 | grep '^DATABASE_PUBLIC_URL=' | cut -d= -f2-)
DATABASE_URL="$DB_URL" .venv/bin/python scripts/seed_premium_demo.py

# Test suite
.venv/bin/python -m pytest tests/ -q --ignore=tests/integration/test_vapi_live.py --ignore=tests/integration/test_ghl_live.py

# Sync GHL users → PostgreSQL (run once; idempotent)
curl -X POST https://neuronx-production-62f9.up.railway.app/users/sync-from-ghl \
     -H "X-Admin-Key: neuronx-admin-dev"

# Email templates: regenerate + re-upload after edits
python3 neuronx-api/email-templates/generate.py
python3 neuronx-api/email-templates/reupload_with_logo.py

# Cleanup + rename templates (idempotent)
python3 neuronx-api/email-templates/cleanup_and_rename.py
```

---

## 🌐 PART H — URLS FOR HUMAN TASKS

| Task | URL |
|---|---|
| VMC workflows | https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflows |
| VMC pipelines | https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/opportunities |
| VMC email templates | https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/emails/email-builder |
| VMC SMTP settings | https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/settings/email_services |
| NeuronX agency settings | https://app.gohighlevel.com/settings (switch to agency view) |
| Metabase dashboards | https://metabase-production-1846.up.railway.app/collection/5 |
| Cloudflare DNS | https://dash.cloudflare.com (zone: neuronx.co) |
| Google Postmaster | https://postmaster.google.com/u/0/ |
| Railway API project | https://railway.app/project/801e7d68-04b5-4137-a5bb-bc1406a4c0d9 |
| Stripe dashboard | https://dashboard.stripe.com (verification pending) |

---

## 🧪 PART I — WORKFLOW TEXT EXTRACTION & DYNAMIC EMAIL (important context)

### What IS readable via GHL API (✅)

- **List of workflows** — `GET /workflows/?locationId={loc}` returns all 24 workflows with id, name, status (published/draft), version, createdAt, updatedAt. This is how we verified VMC has 24 workflows.
- **Email templates** — `GET /emails/builder?locationId={loc}` lists all templates with id, name, subject, previewUrl (Firebase-hosted HTML), archived status. `PATCH /emails/builder/{id}` supports rename + archive + body-update. `POST /emails/builder` creates.
- **Template HTML body** — `previewUrl` returns the final rendered HTML from Firebase Storage (works without auth).
- **Contacts, tags, custom fields, pipelines, calendars, users** — all CRUD via public v2 API.

### What is NOT readable via GHL API (❌)

**Workflow internals — actions, triggers, if/else branches, Send Email body text, Send SMS text, tasks, wait steps, filters.**

Confirmed via exhaustive probe across:
- OAuth token, VMC PIT, Agency PIT (all 3 Bearer auth types)
- Hosts: `services.leadconnectorhq.com` (v2 public), `rest.gohighlevel.com` (v1 legacy), `backend.leadconnectorhq.com` (CRM backend), `app.gohighlevel.com/api/*` (UI's internal — returns 401, requires browser session cookies not Bearer tokens)
- Endpoints tried: `/workflows/{id}`, `/workflows/{id}/actions`, `/workflows/{id}/steps`, `/workflows/{id}/nodes`, `/workflows/{id}/details`, `/workflows/{id}/config`, `/workflows/{id}/triggers`, `/locations/{loc}/workflows/{id}`, `/v1/workflows/{id}`, `/workflows/v2/{id}` — ALL return 404

**Why:** GHL deliberately gates workflow internals. The only way to read/modify workflow actions is:
- GHL UI (with your browser session)
- Claude-in-Chrome tool automating UI clicks with your logged-in session

### How GHL dynamic email text (merge tags) works

GHL supports Handlebars-style merge tags in email body + subject + preview. They get substituted at send time with the triggering contact's data.

**Merge tag categories:**

| Category | Examples | Source |
|---|---|---|
| **Contact** | `{{contact.first_name}}`, `{{contact.last_name}}`, `{{contact.full_name}}`, `{{contact.email}}`, `{{contact.phone}}`, `{{contact.id}}`, `{{contact.tags}}` | Contact record |
| **Custom fields** | `{{contact.ai_program_interest}}`, `{{contact.case_id}}`, `{{contact.ircc_receipt_number}}` | Contact's custom fields (VMC has 140 of these) |
| **Appointment** | `{{appointment.start_date}}`, `{{appointment.start_time}}`, `{{appointment.meeting_url}}`, `{{appointment.reschedule_url}}`, `{{appointment.assigned_user_name}}`, `{{appointment.ics_url}}` | When email fires from WF-05, WF-06 |
| **Location/firm** | `{{location.name}}`, `{{location.address}}`, `{{location.phone}}`, `{{location.website}}` | Sub-account settings |
| **User (RCIC)** | `{{user.name}}`, `{{user.email}}`, `{{user.phone}}` | The GHL user triggering or assigned |
| **Message** | `{{message.unsubscribe_url}}` | CASL compliance — must be present |
| **Opportunity** | `{{opportunity.monetary_value}}`, `{{opportunity.pipeline_stage}}` | If workflow is triggered by opportunity event |

**Our 26 premium templates already use these tags** — see `neuronx-api/email-templates/rendered/*.html` and `manifest.json`.

### The workflow → template linking problem

**Current state:** 24 workflows each have a "Send Email" action where the body is **inline text** (written directly in the action config) OR **template reference** (selects a VMC-* or WF-* template from Email Builder).

**Founder reported** all 24 workflows currently use **inline text**, not template references. To switch to premium templates:

1. Open each workflow in GHL UI
2. Find each Send Email action
3. Change from "Compose" to "Use Template"
4. Select the corresponding premium template by name (WF-01 · Inquiry Received, etc.)
5. Save + publish

**Mapping doc:** `docs/06_execution/EMAIL_WORKFLOW_MAP.md` has the full table.

### 3 paths to extract workflow inline text (so we can preserve voice when building premium HTML)

- **Path A (recommended):** Claude-in-Chrome scraping. ~20 min. User switches Chrome to NeuronX-agency profile, I drive click-through-all-24-workflows automation.
- **Path B:** User manually pastes inline text from each workflow's Send Email action into chat.
- **Path C:** Skip extraction — regenerate templates using AI best-practice copywriting based on workflow name + purpose inferred from the email map. Fast (5 min) but less personalized.

When resuming session, ask user to confirm. If Path A:
1. Switch Chrome to profile logged into NeuronX agency
2. Open https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflows
3. Say "go" → agent uses `mcp__Claude_in_Chrome__*` tools.

### Template naming convention (for right-place linking)

All 26 templates are already renamed to match workflow identifiers for easy dropdown selection:

```
WF-01 · Inquiry Received (Welcome)             →  used by WF-01 Instant Lead Capture
WF-02 · Outreach Attempt (Missed AI Call)      →  used by WF-02 Contact Attempt Sequence
WF-04 · Invite to Book Consultation            →  used by WF-04 Readiness Complete
WF-04B · Complex Case Alert (Internal)         →  used by WF-04B AI Call Receiver
WF-04C · Missed AI Call Recovery               →  used by WF-04C Missed Call Recovery
WF-05a · Booking Confirmed                     →  used by WF-05 Appointment Reminders (immediate)
WF-05b · Consultation Reminder (Day Before)    →  used by WF-05 Appointment Reminders (day-before)
WF-06 · No-Show Recovery                       →  used by WF-06 No-Show Recovery
WF-09a · Retainer Proposal                     →  used by WF-09 Retainer Follow-Up
WF-09b · Retainer Follow-Up                    →  used by WF-09 Retainer Follow-Up (3-day nudge)
WF-11a · Monthly Nurture                       →  used by WF-11 Nurture Campaign
WF-11b · Win-Back Nurture                      →  used by WF-11 Nurture Campaign (inactive)
WF-12 · Medium Score Nurture                   →  used by WF-12 Score Med Handler
WF-13a · PIPEDA Acknowledgement                →  used by WF-13 PIPEDA Data Deletion
WF-13b · PIPEDA Data Deleted                   →  used by WF-13 PIPEDA Data Deletion (confirmation)
WF-CP-01 · Case Onboarding (Welcome)           →  WF-CP-01 Client Onboarding
WF-CP-02 · Document Collection Reminder        →  WF-CP-02 Document Collection Reminders
WF-CP-03 · Form Preparation Started            →  WF-CP-03 Form Preparation
WF-CP-04 · Internal Review in Progress         →  WF-CP-04 Internal Review
WF-CP-05 · Submitted to IRCC                   →  WF-CP-05 IRCC Submission
WF-CP-06 · Monthly Status Update               →  WF-CP-06 Processing Status Checks
WF-CP-07 · IRCC Additional Info (RFI)          →  WF-CP-07 Additional Info
WF-CP-08a · Decision Approved 🎉                →  WF-CP-08 Decision Received (approved branch)
WF-CP-08b · Decision Refused                   →  WF-CP-08 Decision Received (refused branch)
WF-CP-08c · Decision Withdrawn                 →  WF-CP-08 Decision Received (withdrawn branch)
WF-CP-09 · Case Closure                        →  WF-CP-09 Case Closure
```

When you open a GHL workflow's Send Email action and click "Use Template", typing "WF-" in the search box filters to exactly the right templates — no guessing.

---

## 📊 PART J — DEFINITION OF DONE

### Investor-demo ready (2-3 days from today)
Checkpoint test (run after P0 items 1-7):
1. Metabase Pipeline Health dashboard shows $48.5K demo revenue, 11+ cases
2. Drag a case card in GHL → email fires with premium template
3. Open `/cases/{case_id}/viewer` → timeline + docs + checklist render
4. Send test email → lands in Gmail Primary, SPF/DKIM/DMARC pass
5. Submit form on www.neuronx.co → receive VAPI AI call within 5 min

### First paying customer ready (2-3 weeks from today)
All of above + P1 items 8-15:
6. Stripe live + verified + connected to GHL SaaS Configurator
7. `/pricing` page with Stripe checkout → auto-provisions sub-account
8. A2P 10DLC registered
9. Doc upload → retrieved by RCIC flow (documents table + SeaweedFS)
10. Docuseal wired for retainer e-sig

---

## 🏁 STATUS SNAPSHOT (if resuming mid-sprint)

**Last active work:** Email template management. 26 renamed to WF-* in GHL. VMC logo downloaded + deployed to Railway static. Generator updated to embed logo. Pending: get workflow email text (Path A), rebuild templates with text + logo, re-upload.

**Last commit on main:** `4462ef6` — 2 P0 bug fixes (`/cases/list` 500 + Typebot webhook fallback).

**Deploy state:** Railway auto-deploy triggered after push to main + explicit `railway up --detach`. Verify `/cases/list` returns 200 before declaring fixes live.

**Session research output (~2,900 lines):**
- PRODUCTION_READINESS.md (master PM doc)
- GOLDEN_JOURNEYS_AUDIT.md (Agent B — 7 journeys)
- TELEPHONY_SETUP.md (Agent C — 505 lines)
- STRIPE_SAAS_PRICING.md (Agent D — 520 lines, pricing revised to $497/$997/$1997)
- DOMAIN_DNS_CUSTOMER.md (Agent E — 537 lines, 4-tier model)
- OSS_BPM_RESEARCH.md (prior — Docuseal + Paperless-ngx + SeaweedFS)
- CASE_LIFECYCLE_AUDIT.md (prior — documents storage blockers)

---

**This bootstrap is current as of 2026-04-18 post-PM-sprint. Session agent: begin with Part A now.**
