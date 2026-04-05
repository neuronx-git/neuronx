# NeuronX Repo Rules (Project-Level)

These rules apply to every Trae agent/session working in this repository.

## Authority (SSOT)

1. `/docs/04_compliance/trust_boundaries.md` overrides everything.
2. `/docs/01_product/vision.md`
3. `/docs/01_product/prd.md`
4. `/docs/02_operating_system/operating_spec.md`
5. `/docs/02_operating_system/sales_playbook.md`
6. `/docs/03_infrastructure/*`
7. `/docs/05_governance/open_decisions.md`

Non-authoritative:
- `/archive/*` is reference only. If it conflicts with `/docs`, `/docs` wins.
- `/APP/*` is reference only for MVP execution unless explicitly promoted in `/docs/05_governance/open_decisions.md`.

## Working Model (MVP Execution Strategy)

1. Build the entire Phase 1 system inside GoHighLevel (GHL) first.
2. Use one sub-account as the Gold environment.
3. Convert Gold → Snapshot.
4. Install Snapshot into a second lab sub-account.
5. Run UAT end-to-end and produce evidence.
6. Only after proven GHL gaps: build the NeuronX thin brain (webhooks + scoring + briefing + analytics).

## Required Session Startup (Always)

At the start of every session:

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Read `PROJECT_MEMORY.md`.
4. Read the authoritative docs listed in **Authority (SSOT)**.
5. Summarize current execution stage and what is already completed.
6. Continue from the latest stage (do not restart from assumptions).

## Execution Order (GHL Gold Build)

Follow the blueprint-defined order when building Gold:

1. Custom fields and tags
2. Pipeline stages
3. Consultation calendar
4. Lead capture form
5. Landing page / funnel
6. Workflows and templates
7. Snapshot → Install → UAT

Source of truth for Phase 1 build steps:
- `/docs/02_operating_system/ghl_configuration_blueprint.md`

## Tooling Policy

Preferred tools, in order:

1. GHL native UI features (configure-first).
2. Durable public APIs (OAuth v2) for reads/verification and provisioning where supported.
3. Browser/UI automation (Playwright) only where API is insufficient.

- **AUTHENTICATED_UI_AUTOMATION_RULE**: Do not treat SaaS tools (Vapi, Make, etc.) as "manual by default". Always attempt authenticated UI automation via persisted Skyvern/Playwright sessions first. Only escalate to founder if blocked by missing credentials, 2FA, or billing constraints.

Do not write new custom backend code for Phase 1.

## Founder Interaction Policy

Founder involvement is allowed only for:

- Login
- 2FA
- CAPTCHA
- Irreversible approval prompts (OAuth install/permission grants, marketplace approvals)
- High-level product vision clarifications (not platform how-to)

When a checkpoint is required:

1. Stop exactly at that step.
2. Provide the exact URL/screen name.
3. Provide exact click instructions.
4. Resume immediately after confirmation.

Never delegate platform learning (“how GHL works”) to the founder.

## Secrets Policy (Non-Negotiable)

- Never paste secrets into chat, logs, code, or committed files.
- Never print access tokens, refresh tokens, client secrets, API keys.
- Prefer OS-level secret storage (e.g., macOS Keychain) for local lab work.

## Forbidden Behaviors

- Do not treat `/APP` as the MVP build path.
- Do not build AI calling in Phase 1 (Phase 1 is human-only contact attempts).
- Do not introduce a “shadow CRM” outside GHL.
- Do not change canon docs without explicit founder approval.
- Do not add broad scopes or permissions unless required by the current phase.

## GHL Execution Knowledge (Startup Rule)

Before any GHL provisioning or automation work, read:
- `docs/03_infrastructure/ghl_execution_memory.md`

Key operational facts:
- Custom fields, tags, and calendars can be created via GHL V2 API
- Pipeline, form, funnel, and workflow creation require Playwright UI automation
- GHL uses iframes heavily (form builder, workflow builder) — use `frame.locator()` not `page.locator()`
- Authenticated state file `.ghl-auth-state.json` enables headless-capable sessions
- Workflow builder has a modal overlay on first load — press Escape or force-click to dismiss
- Form builder uses `smooth-dnd` library — `frame.locator().dragTo()` works, raw `page.mouse` does not cross iframe boundaries
- GHL V2 API base: `https://services.leadconnectorhq.com`
- Token storage: `tools/ghl-lab/.tokens.json` (gitignored)

## Escalation / Blocker Handling

If blocked:

1. Isolate the blocker as a single sentence ("Blocked by X because Y").
2. Continue all other executable work in parallel.
3. Provide the smallest next action required to unblock.

