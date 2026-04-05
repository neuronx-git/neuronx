# Human-in-the-Loop Escalation Playbook

## Purpose
To ensure that NeuronX complies with immigration regulations (preventing Unauthorized Practice of Law) and provides a premium experience, the AI must immediately hand off complex, sensitive, or high-value interactions to a licensed human professional.

## Escalation Triggers

The AI voice agent or webhook layer will trigger an escalation if the prospect:
1. **Severe Complexity**: Mentions deportation, removal orders, criminal history, or medical inadmissibility.
2. **Legal Advice Request**: Persistently asks "Am I eligible?" or "Will I get approved?" after being told the AI cannot answer.
3. **Explicit Handoff Request**: Says "I want to speak to a human" or "Transfer me to a real person."
4. **AI Confusion**: The AI confidence score drops below 70%, or the user's audio is entirely unintelligible.
5. **High Value / VIP**: Lead indicates a corporate/business immigration need (e.g., setting up a branch office) which typically exceeds standard intake flows.

---

## Escalation Workflow Execution

When an escalation trigger is hit, the end-of-call webhook payload will include:
`ai_requires_human: true`

This triggers a specific GoHighLevel Workflow (**WF-04A: Human Escalation**).

### 1. Tag Added
GHL applies the tag: `nx:human_escalation`

### 2. Internal Notification Sent
GHL sends an SMS and Push Notification to the assigned Firm Owner or Senior Intake Coordinator:
> 🚨 **NeuronX Escalation**: [Lead Name] requires human review. 
> Reason: [ai_summary / reason for escalation].
> Click here to call: [Link to Contact Card]

### 3. Pipeline Movement
The lead's Opportunity card is moved to the **CONTACTING** stage (or a dedicated **ESCALATED** stage if the firm prefers), pausing all automated booking links. 

### 4. Message Sent to Lead
GHL sends an immediate, reassuring SMS to the lead:
> "Hi [Name], this is the intake team at [Firm]. Based on your situation, we want our senior consultant to review your details personally. They will be calling you from this number shortly."

### 5. Consultant Task Created
GHL creates a Task on the contact record assigned to the human operator:
- **Title**: Urgent Escalation Callback: [Lead Name]
- **Due**: Within 15 minutes.
- **Notes**: Includes the `ai_summary` and the specific trigger (e.g., "Requested Human" or "Deportation Mentioned").

---

## Human Operator SLA
- The human operator must acknowledge the escalation within **15 minutes** during business hours.
- The operator reviews the AI call transcript/summary in the GHL notes.
- The operator calls the lead manually, bypassing the AI.
- Once handled, the operator removes the `nx:human_escalation` tag and manually moves the lead to **CONSULT READY** or **LOST**.