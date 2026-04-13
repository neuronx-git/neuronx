# Vapi Data Return Architecture

## The JSON Contract
This document defines the strict data structure that Vapi will return to Make.com (and subsequently GHL) upon call completion. This schema is enforced by the function definitions already injected into the Vapi agent.

## 1. Primary Data Payload
Located in `message.toolCalls` array of the `end-of-call-report`.

### A. Qualification Data (from `capture_lead_data`)
| Field | Type | Enum Values |
| :--- | :--- | :--- |
| `program_interest` | String | "Express Entry", "Study Permit", "Work Permit", "Family Sponsorship", "Visitor Visa", "PNP", "Other" |
| `country` | String | (Free text, e.g. "India", "Nigeria") |
| `urgency` | String | "Immediate", "1-3 months", "3-6 months", "6+ months" |
| `complexity_flag` | String | "None", "Previous Refusal", "Criminality", "Deportation", "Medical Inadmissibility" |

### B. Scoring Data (from `score_lead`)
| Field | Type | Enum Values |
| :--- | :--- | :--- |
| `budget_awareness` | String | "Accepted Paid", "Hesitant", "Refused Paid" |
| `estimated_score` | Integer | 0-100 |

### C. Outcome Data (from `end_call_summary`)
| Field | Type | Enum Values |
| :--- | :--- | :--- |
| `call_outcome` | String | "Qualified", "Not Ready", "Voicemail", "Reschedule" |
| `summary` | String | (Free text 2-sentence summary) |

### D. Escalation Flags (from `escalate_to_human`)
| Field | Type | Notes |
| :--- | :--- | :--- |
| `requires_human` | Boolean | If true, triggers immediate SMS alert to owner. |
| `reason` | String | e.g. "Mentioned deportation order from 2023" |

## 2. Webhook Aggregation Logic (Make.com)
Since Vapi may call multiple functions in one session (e.g. `capture_lead_data` early in the call, and `end_call_summary` at the end), the Make.com scenario must:
1. Iterate through `message.toolCalls`.
2. Aggregate the arguments from **all** function calls into a single flattened JSON object.
3. If a key appears multiple times (rare), prefer the latest value.

## 3. Final GHL Update Payload
Make.com will send this final object to GHL:

```json
{
  "customField": {
    "ai_program_interest": "{{program_interest}}",
    "ai_country": "{{country}}",
    "ai_urgency": "{{urgency}}",
    "ai_complexity_flag": "{{complexity_flag}}",
    "ai_budget_awareness": "{{budget_awareness}}",
    "ai_lead_score": {{estimated_score}},
    "ai_summary": "{{summary}}"
  },
  "tags": [
    "nx:call_completed",
    "{{call_outcome_tag}}", 
    "{{escalation_tag}}"
  ]
}
```
*Note: `{{call_outcome_tag}}` will be dynamically set to `nx:outcome:qualified` or `nx:outcome:voicemail` based on the enum.*