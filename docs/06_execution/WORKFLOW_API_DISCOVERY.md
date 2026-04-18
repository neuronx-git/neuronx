# Workflow API Discovery — Triple-Check Verdict

**Date**: 2026-04-18
**Status**: ❌ **CONFIRMED IMPOSSIBLE** — workflow action content cannot be read via any GHL API
**Verification**: Official OpenAPI spec + live probe with all 3 tokens
**Decision**: Fall back to Claude-in-Chrome scrape OR AI-regenerated copy (Path C)

---

## Question

Can we read GHL workflow internals (triggers, if-else branches, Send Email body text, Send SMS text, wait steps, filters) via any API, so we can programmatically extract all 24 VMC workflows at `vb8iWAwoLi2uT3s5v1OW` and use that text to rebuild premium email templates?

## Verdict

**NO.** Triple-checked via: (a) GHL's official OpenAPI spec in their public GitHub repo, (b) Marketplace docs + OAuth scopes page, (c) community threads (Reddit, GitHub, GHL Ideas board), (d) live probe with VMC location PIT, NeuronX location PIT, agency PIT, and sandbox OAuth.

## Evidence

### 1) Official OpenAPI spec — workflows

Source: [github.com/GoHighLevel/highlevel-api-docs/apps/workflows.json](https://raw.githubusercontent.com/GoHighLevel/highlevel-api-docs/main/apps/workflows.json)

The Workflows resource has **exactly one endpoint**: `GET /workflows/?locationId=X`. No `/workflows/{id}`, `/actions`, `/steps`, `/nodes`, `/triggers`, `/details`, `/config`, `/export`. The response `WorkflowSchema` contains only: `id`, `name`, `status`, `version`, `createdAt`, `updatedAt`, `locationId`. No action/body/trigger/content fields exist.

### 2) OAuth scopes

Source: [marketplace.gohighlevel.com/docs/Authorization/Scopes](https://marketplace.gohighlevel.com/docs/Authorization/Scopes/index.html)

Only one workflow scope exists: `workflows.readonly` (Sub-Account). No `workflows.write`, no `workflows.v2.readonly`, no `automation.*`, no `workflows.actions.readonly`. Our OAuth + PITs already hold this scope; adding more would not help because the endpoints do not exist.

### 3) Live probe (2026-04-18, post-triple-check)

```
✅ 200  GET /workflows/?locationId=vb8iWAwoLi2uT3s5v1OW
         → 24 workflows, keys: [id, name, status, version, createdAt, updatedAt, locationId]

❌ 404  GET /workflows/{id}
❌ 404  GET /workflows/{id}?locationId={loc}
❌ 404  GET /workflows/{id}/actions
❌ 404  GET /workflows/{id}/export
✅ 200  GET /snapshots/?companyId=qKxHWhSxcGxcW3YycTui
         → [{id, name, type}] — metadata ONLY, no content export
❌ 422  GET /snapshots/  (companyId required; same metadata-only shape)
```

Prior session (`docs/06_execution/WORKFLOW_INTERNALS.md`) already tested 16 endpoint variants across 4 hosts with 3 token types — all 404. Confirmed unchanged in 2026-04-18 re-probe.

### 4) Snapshot export

Source: [github.com/GoHighLevel/highlevel-api-docs/apps/snapshots.json](https://raw.githubusercontent.com/GoHighLevel/highlevel-api-docs/main/apps/snapshots.json)

Snapshots API has 4 endpoints: `GET /snapshots/`, `POST /snapshots/share/link`, `GET /snapshots/snapshot-status/{snapshotId}`, `GET /snapshots/snapshot-status/{snapshotId}/location/{locationId}`. **None return workflow content.** Share-link transfers opaque references to the Snapshot push system — no JSON export of actions exists.

### 5) Community confirmation

- [GHL Ideas: Export/Import workflow as JSON](https://ideas.gohighlevel.com/automations/p/export-import-workflow-as-a-json-file) — 267 votes, open since May 2025, still under review
- [GHL Ideas: Workflow Draft and Publishing API](https://ideas.gohighlevel.com/apis/p/workflow-draft-and-publishing-api) — open
- [GHL Ideas: Export Snapshots to JSON](https://ideas.gohighlevel.com/snapshots/p/ability-to-export-snapshots-to-json) — open
- No Reddit, GitHub, or third-party library reports of anyone extracting workflow action content programmatically.

### 6) Why the UI can do it (and we cannot)

The workflow builder iframe (`client-app-automation-workflows.leadconnectorhq.com`) hits the internal `backend.leadconnectorhq.com` host using a browser-session JWT (not an OAuth/PIT Bearer). This host is not documented, not supported for third parties, and requires user-session cookies we cannot obtain server-side. It is the route the UI — and any UI-automation tool like Claude-in-Chrome or Playwright — uses.

## Decision

Use **Claude-in-Chrome** (Path A from BOOTSTRAP Part I) OR **AI-regenerated copy** (Path C).

- **Path A**: Ranjan switches Chrome to the profile logged into NeuronX agency, opens the VMC workflows page, says "go". Agent drives click-through-all-24-workflows with `mcp__Claude_in_Chrome__*` tools. ~20 min. Preserves founder's voice.
- **Path C**: Skip extraction. Regenerate 26 templates using AI best-practice copy inferred from workflow name + purpose mapped in `EMAIL_WORKFLOW_MAP.md`. ~5 min. Less personalized but unblocks investor demo today.

No further API investigation warranted. Case closed.

## References

- [GHL OpenAPI workflows.json (official)](https://raw.githubusercontent.com/GoHighLevel/highlevel-api-docs/main/apps/workflows.json)
- [GHL OpenAPI snapshots.json (official)](https://raw.githubusercontent.com/GoHighLevel/highlevel-api-docs/main/apps/snapshots.json)
- [Get Workflow endpoint reference](https://marketplace.gohighlevel.com/docs/ghl/workflows/get-workflow/index.html)
- [OAuth Scopes reference](https://marketplace.gohighlevel.com/docs/Authorization/Scopes/index.html)
- Prior internal probe: `docs/06_execution/WORKFLOW_INTERNALS.md`
- Bootstrap fallback plan: `BOOTSTRAP_NEXT_SESSION.md` Part I
