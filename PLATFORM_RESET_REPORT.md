# Phase 1: Platform Reset Report

## STRICT EVIDENCE REQUIREMENT
*All architectural decisions below are sourced directly from the provided canonical files: `MINIMAL_VAPI_GHL_ARCHITECTURE.md`, `NEURONX_PLATFORM_GAP_ANALYSIS.md`, `GHL_CAPABILITY_MATRIX.md`, and `VAPI_CAPABILITY_MATRIX.md`.*

## 1. What should remain inside GHL native AI/features?
*Source: `GHL_CAPABILITY_MATRIX.md`, `MINIMAL_VAPI_GHL_ARCHITECTURE.md`*
*   **System of Record**: CRM, Pipelines, Tags, and Custom Fields (`ai_program_interest`, `ai_lead_score`).
*   **Workflow Branching & Execution**: All logic (If/Else, Wait steps, webhooks, internal routing) must occur natively in GHL (WF-01 to WF-11).
*   **Data Parsing**: GHL's native Inbound Webhook JSON mapper will extract variables directly from incoming payloads, eliminating the need for third-party parsers.
*   **Lead Capture & Scheduling**: Native GHL Forms, Funnels, and Calendars.
*   **Payments & Invoicing**: Automated consultation fee capture.
*   **Conversational AI (SMS/Webchat)**: Must remain inside GHL but restricted to **"Suggest" mode only** due to strict Unauthorized Practice of Law (UPL) guardrails.

## 2. What should use Vapi?
*Source: `VAPI_CAPABILITY_MATRIX.md`, `NEURONX_VOICE_AI_ARCHITECTURE.md`*
*   **Outbound Calling**: Speed-to-lead execution triggered by GHL API payload.
*   **Inbound Calling**: Routing the firm's main number directly to the AI agent for after-hours and immediate qualification.
*   **Conversational Guardrails**: Managing the strict UPL rules via system prompts (e.g., immediate escalation to a human if deportation/criminality is mentioned).
*   **Structured Data Extraction**: Utilizing strict Function Calling (`capture_lead_data`, `end_call_summary`) to guarantee structured JSON output.
*   **Call Summarization**: Generating the 2-sentence synopsis written specifically for the human consultant to read before the meeting.

## 3. What should be deferred to v2?
*Source: `MINIMAL_VAPI_GHL_ARCHITECTURE.md`*
*   **Third-Party Orchestration (Make.com / n8n)**: Entirely removed from v1 MVP.
*   **LLM "Pre-Consultation Briefing" Formatting**: Passing the Vapi output through a secondary GPT-4 prompt (via Make.com) to rewrite it into a beautiful PDF is deferred. v1 will drop raw Vapi summaries directly into GHL Contact Notes.
*   **Aggregating Multiple Tool Calls**: Since GHL's basic JSON mapper struggles to aggregate arrays, v1 requires Vapi to only call the data extraction function *once* at the very end of the call.
*   **Advanced Webhook Retry Logic**: Without Make.com, if GHL's webhook receiver drops a payload, automatic retries are lost.

## 4. What is the exact minimal v1 architecture?
*Source: `MINIMAL_VAPI_GHL_ARCHITECTURE.md`*

The architecture is a direct, point-to-point integration with zero middleware:

1. **Trigger**: GHL WF-01A (Outbound) catches a form submission.
2. **Dispatch**: GHL sends a `POST` request directly to the Vapi API (`/call/phone`) containing the lead data.
3. **Execution**: Vapi initiates the call, converses, and extracts JSON data via function calling.
4. **Return**: Upon call completion, Vapi sends the `end-of-call-report` directly to a GHL Inbound Webhook URL (configured in Vapi's `serverUrl`).
5. **Ingestion**: GHL WF-04B receives the payload, uses its native visual JSON path mapper to extract nodes (e.g., `message.toolCalls[0].function.arguments.program_interest`), and updates the Contact Custom Fields natively.