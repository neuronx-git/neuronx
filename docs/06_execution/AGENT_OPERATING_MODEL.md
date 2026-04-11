# NeuronX — Agent Operating Model

**Version**: 1.0
**Date**: 2026-04-05
**Purpose**: How AI agents must operate on NeuronX across sessions. Every session reads this.

---

## MANDATORY SESSION START PROTOCOL

Every new session MUST run these steps before doing ANY work:

```
1. Read PROJECT_MEMORY.md                          # Session summaries, what's done
2. Read memory/project_neuronx_state.md            # Current build state
3. Read memory/project_architecture_decisions.md   # ALL locked decisions (CRITICAL)
4. Read memory/feedback_agent_working_model.md     # API patterns, auth methods
5. Read memory/feedback_typebot_api.md             # Typebot API mastery (CRITICAL)
6. Read memory/feedback_ghl_workflow_builder.md    # GHL UI lessons
7. Read docs/06_execution/CURRENT_STATE.md         # Build status
8. Read docs/06_execution/BOOTSTRAP_DOCUMENT_MAP.md # File inventory
9. Read docs/05_governance/open_decisions.md       # Resolved decisions
10. Read this file (AGENT_OPERATING_MODEL.md)      # Operating rules
```

## MANDATORY SESSION END PROTOCOL

Before ending ANY session:

```
1. Update PROJECT_MEMORY.md with session summary
2. Update docs/06_execution/CURRENT_STATE.md with build changes
3. Update memory/project_neuronx_state.md with state snapshot
4. Update memory/project_architecture_decisions.md if any decisions made
5. Update docs/06_execution/MASTER_WORK_ITEMS.md with completed items
6. Commit ALL changes to git with descriptive message
7. Push to GitHub (Railway auto-deploys NeuronX API)
8. Confirm 0 uncommitted changes
```

## RULES FOR EVERY SESSION

### Rule 1: Verify Before Building
Always check current state via API or docs before creating/modifying anything.
Never assume — verify.

### Rule 2: Update Docs After Every Task
After completing any significant task, update the relevant doc immediately.
Don't batch doc updates — do them inline.

### Rule 3: Test Before Committing
Run `python3 -m pytest tests/ -q` before every commit.
Never commit broken tests.

### Rule 4: Save Credentials Securely
- GHL OAuth: `tools/ghl-lab/.tokens.json` (gitignored)
- GHL PIT: `tools/ghl-lab/.private-integration-token` (gitignored)
- All other credentials: `.env` files (gitignored)
- Reference credentials in memory: `memory/reference_credentials.md`

### Rule 5: Config-Driven Changes
Business rules live in YAML configs, not Python code:
- `config/scoring.yaml` — scoring weights
- `config/programs.yaml` — immigration programs + IRCC forms
- `config/trust.yaml` — compliance rules
- `config/questionnaires.yaml` — form questions
- `config/ircc_field_mappings.yaml` — PDF field mappings
- `config/case_emails.yaml` — email templates

### Rule 6: API-First Execution
Use GHL API before UI. Use Typebot API before visual builder.
Only escalate to UI when API is insufficient.

### Rule 7: Document Learnings Permanently
When discovering a platform limitation, API quirk, or workaround:
1. Add to the relevant memory file
2. Include the exact error + fix
3. Future sessions must not repeat the same mistakes

---

## PLATFORM CREDENTIALS REFERENCE

### GHL (GoHighLevel)
- **Location ID**: FlRL82M0D6nclmKT7eXH (sandbox — changes with paid plan)
- **Company ID**: 1H22jRUQWbxzaCaacZjO
- **OAuth Token**: `tools/ghl-lab/.tokens.json` (auto-refreshes)
- **PIT Token**: `tools/ghl-lab/.private-integration-token`
- **API Base**: https://services.leadconnectorhq.com
- **API Version Header**: 2021-07-28

### Railway (NeuronX Project)
- **NeuronX API**: neuronx-production-62f9.up.railway.app
- **PostgreSQL**: postgres.railway.internal:5432 (internal only)
- **Metabase**: metabase-production-1846.up.railway.app
- **Metabase Login**: ranjan@neuronx.co / NeuronX2026!Secure
- **DATABASE_URL**: set via Railway env var

### Railway (Typebot Project — "spirited-victory")
- **Builder**: builder-production-6784.up.railway.app
- **Viewer**: viewer-production-366c.up.railway.app
- **API Token**: JdIqSp4Lzb97R1CwTLIj2ug3
- **Workspace ID**: cmnrfqc6z000034qx46joy6hf
- **Form ID**: cmnrfu934000334qxnlmsvw2u
- **Public URL**: viewer-production-366c.up.railway.app/vmc-onboarding
- **Admin Login**: goldenphoenix1216@gmail.com (magic link via Resend)
- **DB Credentials**: postgres:ZyIoHSqdvFKKDaqzpVWvMUFefcTyYvkD@postgres.railway.internal:5432/railway
- **ENCRYPTION_SECRET**: SBuKnjywor0jvwdLRItOIPOOhOvKYQ8j

### Typebot Cloud (Secondary — sandbox/testing)
- **Workspace ID**: cmnr4aq4x000004if16bzq8w9
- **API Token**: uo6Cd2K68cU6asEYNYBpiGio
- **API Base**: https://app.typebot.com/api/v1

### VAPI
- **API Key**: cb69d6fc-baf7-4881-8bff-20c7df251437
- **Assistant ID**: 289a9701-9199-4d03-9416-49d18bec2f69
- **Phone Number ID**: ea133993-7c18-4437-88a6-fa7a2d15efbe

### Resend (SMTP for Typebot)
- **API Key**: re_7TZ64bNp_Mfq5Cyrnbsjg7h4ELsPnG7TM
- **SMTP Host**: smtp.resend.com
- **SMTP Username**: resend
- **Send from**: onboarding@resend.dev (free tier — verify domain for custom)

### GitHub
- **Repo**: ranjan-expatready/neuronx
- **Typebot Fork**: ranjan-expatready/typebot.io (has Prisma fix PRs)

---

## KNOWN ISSUES & FIXES (Permanent Reference)

### Typebot Blank Page Fix
**Problem**: Published Typebot form shows blank white page
**Root Cause**: Start event missing `outgoingEdgeId`
**Fix**: PATCH the events array to include outgoingEdgeId matching the start edge
```json
{"events": [{"id": "evt_id", "outgoingEdgeId": "e_start", "type": "start", "graphCoordinates": {"x":0,"y":0}}]}
```

### Typebot Railway DATABASE_URL Fix
**Problem**: Prisma 7 can't resolve Railway reference variables
**Fix**: Hardcode DATABASE_URL as plain `postgresql://` string on Builder + Viewer
Do NOT use `${{Postgres.DATABASE_URL}}`

### GHL Workflow Builder — Build Manually
**Problem**: GHL AI creates cascading duplicate branches
**Fix**: Build IF/ELSE manually. Never use GHL AI for >4 branches.

### GHL Forms API — Read Only
**Problem**: Cannot create forms via API
**Fix**: Build in GHL Form Builder UI, or use Typebot instead

### Typebot PATCH Destroys Other Groups
**Problem**: PATCH with `groups: [only_one_group]` replaces ALL groups, not just the one specified
**Fix**: Always include ALL groups in the PATCH payload when updating any group. Never PATCH with a partial groups array.
**Root Cause**: The groups field is a full replacement, not a merge. Sending 1 group deletes the other 15.
**Prevention**: Before PATCHing groups, GET the full typebot, modify the specific group in the full array, then PATCH the complete array.

### Typebot Viewer Blank Page (Railway) — SOLVED
**Problem**: Self-hosted Typebot viewer (Railway) shows blank page. CDN embed script throws cookie domain errors.
**Root Cause (1)**: Railway viewer's React SSR fails to hydrate `<typebot-standard>` web component — `customElements.get('typebot-standard')` returns undefined
**Root Cause (2)**: CDN embed script (`@typebot.io/js`) hardcodes `typebot.com` cookie domain, throws `CookieStore` error on non-typebot.com hosts
**Solution**: Custom lightweight renderer at `/static/vmc-onboarding.html` that calls the viewer's sendMessage API directly
- Uses `POST /api/v1/sendMessage` with `startParams` and `sessionId` tracking
- Renders text bubbles, images, choice buttons, text/email inputs
- VMC-branded chat UI (navy header, avatar, animated messages)
- Hosted on NeuronX API (Railway auto-deploys)
**Verification**: `python3 -c "import requests; r=requests.post('https://viewer-production-366c.up.railway.app/api/v1/sendMessage',json={'startParams':{'typebot':'vmc-onboarding'}}); print(len(r.json()['messages']),'messages')"` → should return 3 messages
**Live URL**: `https://neuronx-production-62f9.up.railway.app/form/vmc/onboarding` (multi-tenant route)
**Old static URL**: DELETED (2026-04-11) — was `/static/vmc-onboarding.html`, superseded by multi-tenant architecture
**Form Backup**: `neuronx-api/config/typebot_templates/vmc_onboarding_branching.json` (16 groups, 30 vars, 23 edges)
**Typebot Cloud**: DELETED (2026-04-11) — duplicate removed, self-hosted is the only source of truth

### Chrome Extension Client Search
**Problem**: popup.js was calling wrong endpoint (POST /documents/checklist) with hardcoded demo clients
**Fix**: Updated to call GET /clients/search?q=query. Applied 2026-04-11.

---

## WHAT TO DO IN THE NEXT SESSION

Priority order:
1. **Push code to GitHub** → syncs Railway with client endpoint fixes
2. **Fix Typebot viewer** → redeploy Railway viewer service, check logs
3. **Upgrade GHL** → $97 plan unlocks email/SMS/phone
4. **Set GHL_ACCESS_TOKEN on Railway** → fixes /briefing/generate and /clients/search
5. **Run E2E UAT** → full lifecycle test (form → call → booking → briefing)
6. **Take Snapshot v3** → final Gold Build backup
7. **Review improvement backlog** → docs/06_execution/PRODUCT_AUDIT_2026_04_11.md
