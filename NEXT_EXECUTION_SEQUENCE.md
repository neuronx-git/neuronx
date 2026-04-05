# Phase 5: Next Execution Sequence

## STRICT EVIDENCE REQUIREMENT
*This sequence is designed to resolve the UNKNOWN states identified in Phase 0 and Phase 4, and strictly enforce the Minimalist Architecture defined in Phase 1 and 2. Zero execution drift is permitted.*

### Sequence of Execution (Strict Order)

**Step 1: Verify GHL Data Foundation (API)**
*   **Action**: Execute a `GET` request to the GHL API (`/locations/{id}/customFields` and `/tags`) to definitively prove the existence of all AI routing fields (`ai_program_interest`, `ai_lead_score`, etc.).
*   **Reason**: We cannot configure WF-04B's JSON mapper if the destination fields do not exist.
*   **Method**: API Script (Node.js/cURL).

**Step 2: Provision WF-04B & Extract URL (Skyvern)**
*   **Action**: Use Skyvern to navigate to the GHL Workflow Builder, create "WF-04B - AI Call Receiver", set the trigger to "Inbound Webhook", and copy the generated Webhook URL.
*   **Reason**: GHL does not expose workflow creation or trigger URL retrieval via public API.
*   **Method**: Skyvern Cloud (Persistent Session).

**Step 3: Repoint Vapi Architecture (API)**
*   **Action**: Execute a `PATCH` request to the Vapi API (`/assistant/{id}`) replacing `"serverUrl": "https://hook.us1.make.com/placeholder-url"` with the newly generated GHL WF-04B Webhook URL.
*   **Reason**: This physically enforces the Phase 1 Platform Reset (removing Make.com from the architecture).
*   **Method**: API Script.

**Step 4: Execute Baseline Payload Test (API)**
*   **Action**: Trigger a test outbound call via Vapi API or manually submit the GHL form to force Vapi to fire an `end-of-call-report` into the GHL WF-04B webhook.
*   **Reason**: The GHL JSON mapping UI requires a "Sample Request" to be present before fields can be mapped.
*   **Method**: API / Live Test.

**Step 5: Configure GHL JSON Mapping (Skyvern)**
*   **Action**: Use Skyvern to map the incoming JSON payload (e.g., `message.toolCalls[0].function.arguments.program_interest`) to the GHL Custom Fields verified in Step 1.
*   **Reason**: Closes the loop, allowing GHL to mathematically route leads based on Vapi's extraction.
*   **Method**: Skyvern Cloud.

**Step 6: Founder Checkpoint (Final Lock)**
*   **Action**: Pause execution. Request the Founder to log into GHL, open WF-04B, and visually confirm the webhook is receiving data and mapping correctly.
*   **Reason**: Ensures the Minimalist Architecture is fully proven before we begin Snapshot deployment.

***WARNING: Execution of this sequence is paused until the Founder approves the Phase 1-4 reports.***