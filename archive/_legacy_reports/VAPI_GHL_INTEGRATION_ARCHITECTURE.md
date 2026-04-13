# Vapi & GHL Webhook Integration Architecture

## The Data Flow

```mermaid
sequenceDiagram
    participant GHL as GoHighLevel (WF-01A)
    participant Vapi as Vapi API
    participant User as Lead (Phone)
    participant Make as Make.com (Webhook Receiver)
    
    GHL->>Vapi: POST /call/outbound (Phone Number, Name)
    Vapi->>User: Initiates Call
    User-->>Vapi: Conversation & Function Execution
    Vapi->>Make: POST end-of-call-report (JSON Payload)
    Make->>GHL: PUT /contacts/{id} (Update Custom Fields & Tags)
```

## Step 1: Outbound Call Trigger (GHL -> Vapi)

**GHL Workflow Action**: Webhook
**Method**: POST
**URL**: `https://api.vapi.ai/call/phone`
**Headers**:
- `Authorization`: `Bearer 46b108ac-57bc-42a7-9f22-f3365b387ae8` (Public API Key)
- `Content-Type`: `application/json`

**Payload**:
```json
{
  "phoneNumberId": "YOUR_VAPI_PHONE_NUMBER_ID",
  "customer": {
    "number": "{{contact.phone}}",
    "name": "{{contact.first_name}}"
  },
  "assistantId": "YOUR_VAPI_ASSISTANT_ID",
  "assistantOverrides": {
    "variableValues": {
      "first_name": "{{contact.first_name}}",
      "contact_id": "{{contact.id}}" 
    }
  }
}
```
*(Note: Passing the `contact_id` as a variable ensures Vapi returns it in the final report, allowing Make.com to know exactly which GHL contact to update).*

## Step 2: Vapi Function Execution (During Call)
As the conversation progresses, Vapi executes the functions defined in `VAPI_FUNCTION_SCHEMA.md` (e.g., `capture_lead_data`, `end_call_summary`). Vapi stores these outputs in its internal call state.

## Step 3: End of Call Webhook (Vapi -> Make.com)
When the call ends, Vapi sends an `end-of-call-report` event to the Server URL configured in the Vapi Dashboard (which points to a Make.com webhook).

**Vapi Payload Structure (Abridged)**:
```json
{
  "message": {
    "type": "end-of-call-report",
    "call": {
      "id": "call_12345",
      "status": "ended"
    },
    "artifact": {
      "transcript": "...",
      "summary": "Lead is interested in Express Entry...",
      "messages": [ ... ]
    },
    "toolCalls": [
      {
        "function": {
          "name": "capture_lead_data",
          "arguments": "{\"program_interest\":\"Express Entry\",\"urgency\":\"1-3 months\"}"
        }
      }
    ],
    "customer": {
      "name": "John",
      "number": "+1234567890"
    }
  }
}
```

## Step 4: Make.com Processing (Make.com -> GHL)

Make.com catches the Vapi payload and performs the following mapping to update the GHL Contact via the GHL v2 API (`PUT /contacts/{contact_id}`):

| Vapi Extracted Data | GHL Custom Field | GHL Tag to Add |
| :--- | :--- | :--- |
| `program_interest` | `ai_program_interest` | - |
| `country` | `ai_country` | - |
| `urgency` | `ai_urgency` | - |
| `complexity_flag` | `ai_complexity_flag` | - |
| `call_outcome` | `ai_call_outcome` | - |
| `summary` | `ai_summary` | - |
| `requires_human: true` | `ai_requires_human` | `nx:human_escalation` |

*(Note: The actual `ai_lead_score` integer calculation is handled inside GHL by `WF-04B` immediately after these fields are updated, maintaining the "Configuration First" principle).*