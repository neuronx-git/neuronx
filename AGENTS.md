# NeuronX — Agent Operating Map (Repo Root)

## What NeuronX Is (v1)

NeuronX is an AI-assisted sales + intake operating system for Canadian immigration consulting firms.

In v1, GoHighLevel (GHL) is the mandatory system of record and execution engine.
NeuronX is a thin orchestration/intelligence layer that is built only after GHL gaps are proven.

## Project Stage (Truth)

- Canon is defined and authoritative in `/docs/*`.
- MVP build path is **GHL-first**:
  1) Build Gold sub-account in GHL
  2) Snapshot Gold
  3) Install snapshot into another sub-account
  4) Run UAT and capture proof

`/APP/*` exists but is **reference only** for MVP execution unless explicitly promoted later.

## Roles and Responsibilities

- Trae agent: execution owner (plans, drives, validates, reports)
- Playwright/UI operator: performs GHL UI actions when API is insufficient
- Founder: only login/2FA/CAPTCHA/sensitive approvals + high-level product vision clarification

## Non-Negotiable Policies

- **Authority**: `/docs/04_compliance/trust_boundaries.md` overrides all.
- **No shadow CRM**: do not duplicate system-of-record outside GHL.
- **Configure-first**: use GHL native features wherever possible.
- **No Phase 1 custom code**: Phase 1 is a GHL-only working product.
- **Secrets**: never paste tokens/keys/secrets into chat/logs/repo; use OS keychain.
- **AUTHENTICATED_UI_AUTOMATION_RULE**: Do not treat SaaS tools (Vapi, Make, etc.) as "manual by default". Always attempt authenticated UI automation via persisted Skyvern/Playwright sessions first. Only escalate if blocked by missing credentials, 2FA, or billing constraints.
- **MINIMALIST_ARCHITECTURE_RULE**: Prefer the most minimal architecture first (e.g., direct GHL <-> Vapi webhooks). Do not introduce orchestration layers (Make/n8n) unless a concrete blocker is proven.

## Platform Mastery Knowledge
- **GHL**: System of record.
- **Vapi**: Voice AI execution. Data extraction via Function Calling. Scaled via Sub-Accounts.
- **Make/n8n**: Webhook catcher. Routes Vapi JSON payload to GHL Custom Fields.
- **Skyvern**: Headless UI automation for platform configurations where APIs fail or require billing overrides.

1. `README.md`
2. `AGENTS.md`
3. `PROJECT_MEMORY.md`
4. Canon docs:
   - `/docs/01_product/vision.md`
   - `/docs/01_product/prd.md`
   - `/docs/02_operating_system/operating_spec.md`
   - `/docs/02_operating_system/sales_playbook.md`
   - `/docs/02_operating_system/ghl_configuration_blueprint.md`
   - `/docs/03_infrastructure/product_boundary.md`
   - `/docs/03_infrastructure/capability_lock_audit.md`
   - `/docs/03_infrastructure/live_tenant_bakeoff_scorecard.md`
   - `/docs/04_compliance/trust_boundaries.md`
   - `/docs/05_governance/open_decisions.md`

## Execution Order (Gold Build)

Follow `/docs/02_operating_system/ghl_configuration_blueprint.md` exactly:

1. Custom fields and tags
2. Pipeline stages
3. Consultation calendar
4. Lead capture form
5. Landing page/funnel
6. Workflows and message templates
7. Snapshot → install → UAT

## Where Tools Live

- GHL lab helpers and UAT template: `/tools/ghl-lab/`
- UAT report template: `/tools/ghl-lab/UAT_REPORT_TEMPLATE.md`
- GHL execution memory: `/docs/03_infrastructure/ghl_execution_memory.md`
- Playwright auth state: `/tools/ghl-lab/.ghl-auth-state.json` (gitignored)
- OAuth tokens: `/tools/ghl-lab/.tokens.json` (gitignored)

## GHL Automation Patterns (Proven)

### API-capable operations
- Custom fields (CRUD) — `POST /locations/{id}/customFields`
- Tags (CRUD) — `POST /locations/{id}/tags`
- Calendars (CRUD) — `POST /calendars/` (trailing slash required)
- Contacts, Opportunities — full API support
- Pipeline read — `GET /opportunities/pipelines`

### UI-only operations (Playwright required)
- Pipeline creation (API returns errors for stage creation)
- Form builder (iframe: `leadgen-apps-form-survey-builder.leadconnectorhq.com`)
- Funnel/website builder (heavy SPA page editor)
- Workflow creation and configuration (iframe: `client-app-automation-workflows.leadconnectorhq.com`)

### Reliable Playwright patterns
- `chromium.launch({ headless: false })` + `storageState` from saved auth
- Wait 15-20s after navigation for GHL SPA to render
- Iframe detection: `page.frames().find(f => f.url().includes(...))`
- Form field drag: `frame.locator('.gui__builder-card').filter({ hasText: '...' }).first().dragTo(target)`
- Workflow name: click h1 with `{ force: true }`, then `Cmd+A` + type
- Always press Escape after entering workflow editor (modal overlay blocks clicks)

