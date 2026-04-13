# NeuronX Voice AI Architecture (Vapi)

This defines the productized AI Voice layer. It is designed to be cloned via the Vapi API for every new tenant.

## 1. Agent Structure
- **Model**: `gpt-4o-mini` (Optimized for lowest latency conversational turn-taking).
- **Voice**: ElevenLabs `jennifer` (Professional, empathetic, clear English).
- **Transcriber**: Deepgram `nova-2` (Best for heavy accents/ESL speakers).

## 2. Conversation States (The Prompt Machine)
1. **Greeting**: "Hi, is this {{first_name}}? ... Hi {{first_name}}, this is Alex from NeuronX Immigration..."
2. **Consent**: Verify they have a minute to chat. If not -> Trigger `end_call` with outcome `reschedule`.
3. **Qualification Loop**: Ask the 4 core questions naturally (Program, Location, Urgency, Refusal History).
4. **Budget Check**: Soft pitch the paid strategy session.
5. **Close**: "I'll send a booking link to your phone now." -> Trigger `schedule_consultation`.

## 3. Structured Data Extraction (Function Calling)
The AI is strictly bound to these tools to extract JSON data mid-call.

- **`capture_lead_data`**
  - `program_interest` (Enum: Express Entry, Study Permit, etc.)
  - `urgency` (Enum: Immediate, 1-3 months, 6+ months)
  - `complexity_flag` (Enum: None, Previous Refusal)

## 4. Human Escalation Triggers
Immigration consultants risk their license (RCIC) if an AI gives Unauthorized Practice of Law (UPL). 

- **Trigger Event**: User asks "Will I get approved?" or mentions "Deportation/Criminality".
- **Action**: AI immediately invokes the `escalate_to_human` function.
- **AI Output**: "Because of the specific details of your situation, I cannot provide an assessment. Let me have our senior consultant review your file and call you back directly."
- **System Outcome**: AI hangs up. Webhook fires `requires_human: true`. GHL alerts the firm owner.

## 5. End of Call Summary
- **`end_call_summary`**
  - `call_outcome` (Enum: Qualified, Not Ready, Voicemail)
  - `summary` (String: A 2-sentence synopsis written specifically for the human consultant to read before the meeting).