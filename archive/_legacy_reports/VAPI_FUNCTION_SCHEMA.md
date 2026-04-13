# Vapi Function Schema

The following JSON schemas define the tools available to the Vapi agent. These functions enforce structured data extraction and control the flow of the conversation.

## 1. `capture_lead_data`
*Called throughout the conversation to store extracted data in the conversation state.*

```json
{
  "name": "capture_lead_data",
  "description": "Store qualification data gathered from the lead during the conversation.",
  "parameters": {
    "type": "object",
    "properties": {
      "program_interest": {
        "type": "string",
        "enum": ["Express Entry", "Study Permit", "Work Permit", "Family Sponsorship", "Visitor Visa", "PNP", "Other"],
        "description": "The primary immigration program the lead is interested in."
      },
      "country": {
        "type": "string",
        "description": "The lead's current country of residence."
      },
      "urgency": {
        "type": "string",
        "enum": ["Immediate", "1-3 months", "3-6 months", "6+ months"],
        "description": "How quickly the lead wants to move forward."
      },
      "complexity_flag": {
        "type": "string",
        "enum": ["None", "Previous Refusal", "Criminality", "Deportation", "Medical Inadmissibility"],
        "description": "Any complicating factors in the lead's history."
      }
    },
    "required": []
  }
}
```

## 2. `score_lead`
*Called internally by the AI (or server-side) before deciding the final booking path.*

```json
{
  "name": "score_lead",
  "description": "Calculate a preliminary lead score based on gathered data to determine if they qualify for immediate booking.",
  "parameters": {
    "type": "object",
    "properties": {
      "budget_awareness": {
        "type": "string",
        "enum": ["Accepted Paid", "Hesitant", "Refused Paid"],
        "description": "The lead's willingness to pay for a consultation."
      },
      "estimated_score": {
        "type": "integer",
        "description": "An estimated score from 0-100 based on program fit, urgency, and budget."
      }
    },
    "required": ["budget_awareness"]
  }
}
```

## 3. `escalate_to_human`
*Called IMMEDIATELY if the user hits a strict guardrail (e.g., asks for legal advice, mentions deportation, gets angry).*

```json
{
  "name": "escalate_to_human",
  "description": "Instantly ends the AI flow and flags the lead for emergency human intervention. Use when user asks for legal advice, mentions deportation/criminality, or becomes angry.",
  "parameters": {
    "type": "object",
    "properties": {
      "reason": {
        "type": "string",
        "description": "The specific reason for escalation (e.g., 'Asked if they will be approved', 'Mentioned previous deportation')."
      },
      "requires_human": {
        "type": "boolean",
        "description": "Always set to true."
      }
    },
    "required": ["reason", "requires_human"]
  }
}
```

## 4. `schedule_consultation`
*Called when the user agrees to receive the booking link.*

```json
{
  "name": "schedule_consultation",
  "description": "Flags that the user has agreed to receive a consultation booking link.",
  "parameters": {
    "type": "object",
    "properties": {
      "booking_status": {
        "type": "string",
        "enum": ["Requested", "Declined"],
        "description": "Whether the user agreed to receive the booking link."
      }
    },
    "required": ["booking_status"]
  }
}
```

## 5. `end_call_summary`
*Called at the very end of the call to compile all data for the final webhook payload.*

```json
{
  "name": "end_call_summary",
  "description": "Compiles the final summary of the call before hanging up.",
  "parameters": {
    "type": "object",
    "properties": {
      "call_outcome": {
        "type": "string",
        "enum": ["Qualified", "Not Ready", "Voicemail", "Reschedule"],
        "description": "The overall outcome of the call."
      },
      "summary": {
        "type": "string",
        "description": "A concise, 2-3 sentence summary of the lead's situation, needs, and any red flags. DO NOT include legal assessments."
      }
    },
    "required": ["call_outcome", "summary"]
  }
}
```