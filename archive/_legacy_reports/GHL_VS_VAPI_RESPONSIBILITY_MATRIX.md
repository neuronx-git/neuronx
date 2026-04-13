# Phase 2: GHL vs Vapi Responsibility Matrix

## STRICT EVIDENCE REQUIREMENT
*Sourced from `MINIMAL_VAPI_GHL_ARCHITECTURE.md`, `IMMIGRATION_SALES_OS_FEATURE_MAP.md`, `GHL_CAPABILITY_MATRIX.md`, and `VAPI_CAPABILITY_MATRIX.md`.*

| Category | Responsible Platform | Justification (Source) |
| :--- | :--- | :--- |
| **Workflow Generation** | **GHL** | GHL is the mandatory system of record and execution engine (`AGENTS.md`). |
| **Workflow Branching** | **GHL** | If/Else routing logic based on AI-extracted custom fields occurs natively in GHL Workflows (`IMMIGRATION_SALES_OS_FEATURE_MAP.md`). |
| **Outbound Voice Calling** | **Vapi** | Triggered via GHL API payload for speed-to-lead (`VAPI_CAPABILITY_MATRIX.md`). |
| **Inbound Answering** | **Vapi** | Routing the firm's main Twilio/GHL number directly to the Vapi assistant for 24/7 AI answering (`NEURONX_PLATFORM_GAP_ANALYSIS.md`). |
| **Lead Scoring** | **Vapi (Extraction) & GHL (Routing)** | Vapi uses the `score_lead` function call to assess the conversation; GHL mathematically routes the lead (VIP vs Nurture) based on that score (`VAPI_CAPABILITY_MATRIX.md`, `IMMIGRATION_SALES_OS_FEATURE_MAP.md`). |
| **Summaries** | **Vapi** | The `end_call_summary` function creates a 2-sentence synopsis written for the human consultant (`NEURONX_VOICE_AI_ARCHITECTURE.md`). |
| **Consultant Briefing** | **GHL (Raw Note) / Deferred** | Advanced LLM formatting via Make.com is deferred to v2. For v1, the raw Vapi summary string is dropped directly into the GHL Contact Notes (`MINIMAL_VAPI_GHL_ARCHITECTURE.md`). |
| **Templates** | **GHL** | SMS and Email message templates live natively within GHL (`GHL_CAPABILITY_MATRIX.md`). |
| **Websites/Funnels** | **GHL** | Multi-step, high-converting intake forms embedded in specialized landing pages use GHL Native tools (`IMMIGRATION_SALES_OS_FEATURE_MAP.md`). |
| **Brand Voice** | **Vapi (Spoken) & GHL (Written)** | Vapi manages the spoken voice (e.g., ElevenLabs `jennifer`) and conversational persona. GHL manages written brand voice via SMS/Email templates (`NEURONX_VOICE_AI_ARCHITECTURE.md`). |
| **Reporting** | **GHL** | Custom dashboards tracking "AI Qualification Rate" vs "Human Conversion Rate" rely on GHL's native UI (`GHL_CAPABILITY_MATRIX.md`). |
| **Callbacks/Webhooks** | **GHL (Receiver) & Vapi (Sender)** | Vapi's `serverUrl` fires the `end-of-call-report` directly to GHL's native Inbound Webhook trigger (WF-04B) (`MINIMAL_VAPI_GHL_ARCHITECTURE.md`). |