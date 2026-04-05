# NeuronX GHL Test Lab Builder

Purpose: Provision and validate the **GHL-only** NeuronX v1 system for visual UAT.

This tool focuses on what can be automated safely via HighLevel public APIs:

- Create test sub-accounts (locations)
- Create sub-accounts **with a snapshot pre-applied** (when supported)
- Generate a repeatable run log and UAT report template

What this tool does **not** automate (by design):

- Building funnels/website pages
- Creating complex workflows via API (often not exposed as a public "create workflow" endpoint)

For those, follow the no-code build blueprint:

- `/docs/02_operating_system/ghl_configuration_blueprint.md`

---

## Required Credentials (do not commit)

Preferred (no secrets in files): store the agency key in macOS Keychain.

Add/update the key (prompts for the secret, no echo):

```bash
security add-generic-password -U -s "neuronx-ghl" -a "agency-api-key" -T "" -w
```

Do not paste API keys into chat, commits, or command-line arguments.

Then run:

```bash
pnpm ghl:lab identify-key
pnpm ghl:lab create-location --name "NeuronX Test Lab"
```

Alternative (not recommended): provide `GHL_AGENCY_API_KEY` in the process environment.

---

## Marketplace OAuth (No Agency Key)

If you are using a GoHighLevel Marketplace OAuth app (Client ID + Client Secret), store these in Keychain:

```bash
security add-generic-password -U -s "neuronx-ghl" -a "oauth-client-id" -T "" -w
security add-generic-password -U -s "neuronx-ghl" -a "oauth-client-secret" -T "" -w
```

Default local redirect URI used by this lab tool:

- `http://localhost:3000/auth/neuronx/callback`

Important:

- Your Marketplace app must allow this Redirect URI for the lab flow.
- If your Marketplace app only allows an HTTPS redirect, you must use a hosted callback endpoint instead of the local server.

Start the local OAuth callback server (prints the install URL):

```bash
pnpm ghl:lab oauth:server
```

Optional overrides:

```
GHL_V1_BASE_URL=https://rest.gohighlevel.com
GHL_DEFAULT_TIMEZONE=Canada/Eastern
```

Notes:

- This builder uses the legacy v1 location create endpoint because it supports creating locations and (optionally) applying a snapshot in the same request.
- If your account requires a different auth method (OAuth v2 + SaaS scopes), this tool will need a small adapter update.

---

## Commands

Run with `pnpm` from repo root.

### 0) Confirm the key type

```
pnpm ghl:lab identify-key
```

### 1) Create the “NeuronX Test Lab” sub-account

```
pnpm ghl:lab create-location --name "NeuronX Test Lab"
```

### 2) Create a second sub-account (for snapshot install test)

```
pnpm ghl:lab create-location --name "NeuronX Snapshot Install Lab"
```

### 3) Create a sub-account with snapshot applied

```
pnpm ghl:lab create-location --name "NeuronX Snapshot Install Lab" --snapshotId <SNAPSHOT_ID>

---

## UI Automation (Optional)

Snapshot install may require UI steps depending on plan and API availability.

There is a Playwright skeleton test at:

- `tools/ghl-lab/tests/snapshot-install.spec.ts`

Run it by setting:

```
GHL_SNAPSHOT_SHARE_URL=...
```

Then:

```bash
pnpm exec playwright test -c tools/ghl-lab/playwright.config.ts
```

This intentionally pauses for manual login and 2FA.
```

---

## Phase Execution Notes

### Phase 1 (Environment)

- Use `create-location` to create the sub-account(s).

### Phase 2 (Configure in GHL)

- Follow `/docs/02_operating_system/ghl_configuration_blueprint.md`
- Build the full working system manually in GHL (no code)

### Phase 3 (Snapshot)

- Create snapshot inside GHL UI from the configured “gold” sub-account
- Record snapshot ID

How to capture snapshot ID:
- In Agency View → **Account Snapshots**, open the snapshot. The snapshot ID is typically visible in the snapshot details URL or in the share-link configuration.

### Phase 4 (Automated deployment)

- Use `--snapshotId` to create a new sub-account with the snapshot applied (if supported)
- If snapshot application is not supported for your plan/account, fall back to manual snapshot install

### Phase 5 (UAT)

- Run the UAT scenarios in the blueprint and record results

---

## Output

Each command prints:

- Location (sub-account) ID
- Suggested dashboard URL (`https://app.gohighlevel.com/location/<locationId>`)
