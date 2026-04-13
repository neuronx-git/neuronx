# AI Layer Implementation Path

## Architecture Overview
The system relies on GoHighLevel (GHL) as the absolute system of record. The external AI voice platform (e.g., Vapi/Bland) operates purely as a stateless execution engine that reads context from GHL and writes results back.

## 1. How Lead Enters AI Calling Flow
1. Lead submits the `Immigration Inquiry (V1)` form on the landing page.
2. GHL creates the contact and moves the opportunity to the `NEW` stage.
3. If the form was submitted within business hours (or extended AI hours), the lead qualifies for immediate speed-to-lead routing.

## 2. Workflow Trigger (Starting the Call)
- **Workflow**: `WF-01A — AI Speed-to-Lead Initialization`
- **Trigger**: Form Submission.
- **Action 1**: Wait 1 minute (to seem natural, not robotic).
- **Action 2**: Outbound Webhook to the Voice AI API (POST request).
  - **Payload**: Contact Name, Phone Number, Program Interest (from form), Firm Name, Consultant Name.
- **Action 3**: Tag lead `nx:ai_call_initiated`.

## 3. Storing Conversation Outputs in GHL
When the call terminates, the Voice AI platform triggers an "End of Call" webhook.
- A thin integration layer (e.g., Make.com or a serverless function) catches this payload.
- It maps the extracted JSON data to GHL Custom Fields via the GHL API:
  - `ai_program_interest`
  - `ai_country`
  - `ai_urgency`
  - `ai_complexity_flag`
  - `ai_lead_score`
  - `ai_call_outcome` (e.g., "Qualified", "Voicemail", "Human Escalation")
  - **Contact Note**: The full call summary and transcript link is appended to the GHL Contact Notes for the human consultant to read.

## 4. Triggering the Booking
**Scenario A (AI Books Live)**: 
The AI is connected to the GHL Calendar API and books the slot live on the call.
**Scenario B (AI Sends Link - Recommended for V1)**:
The AI says, "I'm sending you a secure link right now to pick a time."
- The AI end-of-call webhook updates `ai_booking_status` to "Requested".
- GHL Workflow `WF-04` detects this change and instantly fires the booking link via SMS/Email.

## 5. Human Escalation Routing
If the lead asks for legal advice, becomes frustrated, or has a highly complex case (e.g., deportation):
- The AI politely ends the intake: "Because of the specifics of your case, I want to have our senior consultant review this directly. They will call you back shortly."
- End-of-call webhook pushes `ai_requires_human = true` and tags `nx:human_escalation`.
- GHL Workflow detects the tag -> Sends internal SMS/Push Notification to the firm owner -> Moves pipeline stage to `CONTACTING (Escalated)`.

## 6. Failed or Unanswered Calls
If the AI encounters a voicemail or no-answer:
- Webhook returns `ai_call_outcome = voicemail`.
- GHL Workflow detects this outcome.
- **Action**: GHL sends an automated SMS: *"Hi [Name], this is NeuronX Advisory. We just tried calling about your immigration inquiry. Are you available later today, or would you prefer to book a time here: [Link]?"*

## 7. Retry Logic
- If `ai_call_outcome` = "no-answer", GHL drops the lead into a wait step (e.g., Wait 2 hours).
- After 2 hours, check if `nx:contacted` tag exists. If not, trigger a second Webhook to the Voice AI for Attempt 2.
- Cap AI voice attempts at 2. Subsequent attempts fallback to standard human/SMS workflows (`WF-02`).

## 8. Configuration Split
- **Configured purely in GHL**: Pipeline stages, SMS/Email templates, wait steps, internal notifications, calendar availability.
- **Configured in Voice AI Platform**: System prompt, voice model, voice speed, interruption handling, data extraction schema.
- **Integration Layer**: Webhook mapping (Voice AI JSON -> GHL Custom Fields).