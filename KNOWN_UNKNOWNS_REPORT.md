# Phase 0: Known Unknowns Report

## STRICT EVIDENCE REQUIREMENT
In accordance with the Maker-Checker governance system, no assumptions are made in this report. Every claim is based on the current state of local documentation and the lack of live system verification in the current session.

## 1. Missing Data (What I Do Not Have)
*   **Live GHL Custom Fields & Tags**: I do not have real-time API evidence that the required AI fields (`ai_program_interest`, `ai_urgency`, `ai_lead_score`, `ai_complexity_flag`) and corresponding routing tags exist in the GHL `NeuronX Test Lab` sub-account.
*   **Live GHL Workflow State (WF-01 to WF-11)**: I do not have the current JSON configurations or active statuses of these workflows.
*   **Live Vapi Agent Configuration**: I do not have the current API response from Vapi for the `NeuronX Intake Agent`. Specifically, I do not know what the `serverUrl` is currently set to (Make.com vs. GHL Webhook).
*   **Vapi Phone Number Provisioning**: I do not have confirmation from the Vapi API that a phone number is successfully purchased, assigned to the assistant, and capable of inbound/outbound routing.
*   **GHL OAuth Token Status**: I do not know if the tokens in `tools/ghl-lab/.tokens.json` are currently valid or expired.
*   **Skyvern Session Validity**: I do not know if the Skyvern persistent session (`pbs_506976117979052016` referenced in `PROJECT_MEMORY.md`) is still active or requires re-authentication by the founder.

## 2. Requires Live Verification (No Inferred State)
*   **WF-04B (Inbound Webhook Receiver)**: Must be verified via GHL API or Skyvern UI check to confirm it exists and the trigger URL matches the Vapi `serverUrl`.
*   **Minimalist Architecture Reality**: `MINIMAL_VAPI_GHL_ARCHITECTURE.md` states Make.com/n8n are removed for v1 MVP. We must verify that no traffic is currently being routed through Make.com.
*   **GHL Native AI Features**: Need to verify if the "Conversational AI (SMS)" feature is toggled off (or in Suggest mode) in the GHL sub-account settings to comply with UPL guardrails.

## 3. Stale or Unreliable Information
*   **Workflow Completion Status**: There is a conflict in the local documentation. `PROJECT_MEMORY.md` states: *"WF-01: Configured & Verified... Next: WF-02 through WF-11"*. However, the system's core memory block (`03frppxj3q1pc30bi51xswqk3`) states: *"Skyvern's visual LLM agent successfully configured 11 workflows"*. This contradiction makes local file state unreliable; only live API/UI verification can be trusted.
*   **README.md**: Explicitly flagged in `PROJECT_MEMORY.md` as outdated (*"README.md still states Build Status: Not started. Treat this as outdated"*).

**Conclusion**: I cannot confirm the true state of the NeuronX MVP build without executing Phase 4 (Reality Check) via direct API calls to GHL and Vapi. Until Phase 4 is complete, all architectural plans in Phases 1-3 remain theoretical.