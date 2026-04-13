# Phase 3: Execution Method Matrix

## STRICT EVIDENCE REQUIREMENT
*Following the explicit hierarchy: API first → Skyvern second → Playwright third. Sourced from `PROJECT_MEMORY.md`, `AGENTS.md`, and system rules.*

| Remaining Task | Preferred Method | Exact Reason |
| :--- | :--- | :--- |
| **Configure WF-02 to WF-11** | **Skyvern** | GHL does not expose Workflow configuration via public API. Core memory `03frppxj3q1pc30bi51xswqk3` confirms Skyvern Cloud successfully automated the workflow builder on 2026-03-17 using a persistent session. |
| **Configure WF-04B (Inbound Webhook & JSON Mapper)** | **Skyvern** | The Inbound Webhook mapping UI is embedded within the GHL Workflow Builder SPA. No public API exists for creating or mapping webhook triggers. |
| **Configure Form Dropdowns** | **Skyvern** | The GHL Form builder operates inside an iframe (`leadgen-apps-form-survey-builder`). `AGENTS.md` confirms API cannot modify form fields, but UI automation (Skyvern/Playwright) can. Skyvern is preferred over raw Playwright. |
| **Edit Landing Page Content** | **Skyvern** | The GHL Funnel/website builder is a heavy SPA page editor without API support for content manipulation. |
| **Delete Junk Workflows (Cleanup)** | **Skyvern** | Workflow list management and deletion must be handled via the UI as there is no documented V2 API endpoint for workflow deletion. |
| **Update Vapi Agent `serverUrl`** | **API** | Vapi has a robust REST API. We can use `PATCH /assistant/{id}` to update the `serverUrl` to point to the new GHL WF-04B webhook, avoiding unnecessary UI automation. |
| **Vapi Phone Number Provisioning** | **API** | Vapi provides the `POST /phone-number` API to programmatically purchase and assign phone numbers to an assistant. |
| **Vapi Sub-Account Creation** | **API** | Vapi provides the `/org/subaccount` API to isolate tenants and enforce hard spend limits programmatically. |
| **GHL Snapshot Creation & Install** | **Founder Checkpoint -> API** | While the GHL V2 API supports snapshot installation, the initial Marketplace OAuth consent grant requires a Founder Checkpoint (irreversible approval prompt) as per the non-negotiable rules in `AGENTS.md`. |