# Vapi Capability Matrix

| Feature Category | Description | API or UI | Current NeuronX Usage | Opportunity for Improvement | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Assistants API** | Define system prompts, voice models, and transcriber settings. | Both | High. Created `NeuronX Intake Agent`. | Dynamically inject lead's name/context into the prompt via API at call time. | High |
| **Function Calling** | Strict JSON schema extraction during conversation. | Both | High. Created `capture_lead_data`, `score_lead`, etc. | Add functions to check calendar availability mid-call via API. | High |
| **Outbound Calling** | Trigger calls via API payload. | API only | High. Used for speed-to-lead. | Implement retry logic (Attempt 2) if the first call goes to voicemail. | High |
| **Inbound Calling** | Route phone numbers directly to the AI agent. | Both | None yet. | Assign a Vapi number as the main office line for 24/7 AI answering. | Medium |
| **Voicemail Detection** | AMD (Answering Machine Detection) to drop messages. | Both | Configured in Assistant. | Create specific voicemail drop scripts based on the time of day. | Medium |
| **End-of-Call Webhooks** | POST structured data/transcripts to external servers. | Both | High. Routing to Make.com/n8n. | Pass deeper metadata (call duration, interruption count) to measure lead engagement. | High |
| **Sub-Accounts (Agency)** | Programmatically isolate clients, set spend limits. | API | None yet. | Crucial for SaaS scaling. Create a sub-account per GHL Location. | Critical |
| **Custom Voices** | Clone specific human voices (via ElevenLabs/PlayHT integration). | Both | Using stock "Sarah". | Clone the firm owner's voice to increase trust. | Low |
| **Barge-In/Interruption** | AI stops speaking when user interrupts. | Both | Configured. | Fine-tune sensitivity specifically for ESL speakers who may pause frequently. | Medium |