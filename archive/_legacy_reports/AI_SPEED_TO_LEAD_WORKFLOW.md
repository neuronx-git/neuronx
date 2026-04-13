# AI Speed-to-Lead Workflow (GHL)

This document outlines the two interconnected GoHighLevel workflows required to trigger the Vapi AI and process its results.

---

## 1. `WF-01A — AI Speed-to-Lead Initialization`
*Purpose: Trigger the outbound Vapi call when a new lead arrives.*

- **Trigger**: Form Submitted
  - *Filter*: Form is "Immigration Inquiry (V1)"
- **Condition (If/Else)**: Business Hours Check
  - *Branch A (Within Hours 8am-8pm)*: Proceed to call.
  - *Branch B (Outside Hours)*: Send SMS ("Hi {{contact.first_name}}, we received your inquiry. Our AI assistant will call you tomorrow morning to verify your details.") -> Wait until 9:00 AM -> Proceed to call.
- **Action 1**: Wait 1 Minute (To appear natural, not instant).
- **Action 2**: Webhook (POST to Vapi)
  - URL: `https://api.vapi.ai/call/phone`
  - Headers: Auth Bearer `46b108ac-57bc-42a7-9f22-f3365b387ae8`
  - Body: Custom JSON (Contains Phone, Name, and `contact_id`).
- **Action 3**: Add Contact Tag: `nx:ai_call_initiated`
- **Action 4**: Update Opportunity Stage -> `CONTACTING`

---

## 2. `WF-04B — AI Lead Scoring & Routing Engine`
*Purpose: Catch the data returned by Vapi (via Make.com) and route the lead.*

- **Trigger**: Contact Changed
  - *Filter*: Custom Field `ai_summary` Has Changed (This guarantees the webhook has finished updating the contact).
- **Condition (If/Else Branches)**:

  - **Branch 1: Human Escalation**
    - *Filter*: Tag includes `nx:human_escalation` OR `ai_requires_human` = Yes
    - *Action*: Send Internal Notification (SMS) to Firm Owner ("URGENT: Lead requires human review. Reason: {{contact.ai_summary}}").

  - **Branch 2: Qualified (Ready to Book)**
    - *Filter*: `ai_call_outcome` = "Qualified" AND `ai_budget_awareness` != "Refused Paid"
    - *Action*: Update `ai_lead_score` = 80
    - *Action*: Add Tag `nx:score:high`
    - *Action*: Move Opportunity Stage -> `CONSULT READY`
    - *Action*: Send SMS: "Hi {{contact.first_name}}, as promised, here is the link to book your formal strategy session for your {{contact.ai_program_interest}} application: [Calendar Link]"

  - **Branch 3: Not Ready / Nurture**
    - *Filter*: `ai_call_outcome` = "Not Ready"
    - *Action*: Update `ai_lead_score` = 40
    - *Action*: Add Tag `nx:score:low`
    - *Action*: Move Opportunity Stage -> `NURTURE`
    - *Action*: Add to Nurture Email Sequence based on `ai_program_interest`.

  - **Branch 4: Voicemail / Unanswered**
    - *Filter*: `ai_call_outcome` = "Voicemail"
    - *Action*: Wait 2 hours.
    - *Action*: Send SMS: "Hi {{contact.first_name}}, this is NeuronX. We tried calling regarding your immigration inquiry. You can book a time directly here: [Calendar Link]"
    - *Action*: Move Opportunity Stage -> `UNREACHABLE`