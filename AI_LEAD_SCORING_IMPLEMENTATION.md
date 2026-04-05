# AI Lead Scoring Implementation

## Architecture
The AI Lead Scoring model translates qualitative conversational data gathered by the Voice AI (or intake form) into a quantitative score (0-100) and actionable routing tags inside GoHighLevel.

Because NeuronX strictly adheres to the "Configuration First" and "Minimal Engineering" principles, the scoring logic is executed within **GoHighLevel Workflows** using standard conditional branching based on the Custom Fields populated by the Voice AI webhook.

## 1. GHL Workflow Implementation: `WF-04B — AI Lead Scoring Engine`

**Trigger:**
- Contact Changed: Custom Field `ai_summary` has changed. (This indicates the Voice AI webhook has successfully posted the end-of-call data).

**Execution Logic (If/Else Branches):**

### Branch 1: Human Escalation (Bypass Scoring)
- **Condition**: `ai_requires_human` is TRUE OR `ai_complexity_flag` includes "Deportation", "Inadmissibility", or "Criminality".
- **Action**:
  - Add Tag: `nx:human_escalation`
  - Update `ai_lead_score` to `0` (or leave blank)
  - Move Opportunity to Stage: `CONTACTING`
  - Send Internal SMS to Firm Owner.
  - End Workflow.

### Branch 2: High Priority (Score 80-100)
- **Condition**: 
  - `ai_program_interest` is "Express Entry" OR "Spousal Sponsorship" OR "LMIA"
  - AND `ai_urgency` is "Immediate" OR "1-3 months"
  - AND `ai_budget_awareness` is "Accepted Paid"
  - AND `ai_call_outcome` is "Qualified"
- **Action**:
  - Update `ai_lead_score` to `90`
  - Add Tag: `nx:score:high`
  - Move Opportunity to Stage: `CONSULT READY`
  - Send priority booking link SMS.

### Branch 3: Qualified (Score 60-79)
- **Condition**:
  - `ai_program_interest` is NOT empty
  - AND `ai_budget_awareness` is NOT "Refused Paid"
  - AND `ai_call_outcome` is "Qualified"
- **Action**:
  - Update `ai_lead_score` to `70`
  - Add Tag: `nx:score:med`
  - Move Opportunity to Stage: `CONSULT READY`
  - Send standard booking link SMS.

### Branch 4: Low Intent (Score 40-59)
- **Condition**:
  - `ai_urgency` is "6+ months" 
  - OR `ai_budget_awareness` is "Hesitant"
  - OR `ai_call_outcome` is "Not Ready"
- **Action**:
  - Update `ai_lead_score` to `50`
  - Add Tag: `nx:score:low`
  - Move Opportunity to Stage: `NURTURE`
  - Add to Nurture Email Campaign.

### Branch 5: Unqualified / Junk (Score 0-39)
- **Condition**:
  - `ai_budget_awareness` is "Refused Paid"
  - OR `ai_program_interest` is "Other/Invalid"
- **Action**:
  - Update `ai_lead_score` to `10`
  - Add Tag: `nx:score:junk`
  - Move Opportunity to Stage: `LOST`
  - End Workflow.

---

## 2. Dynamic Score Calculation (Alternative / V1.5)
If a strict 0-100 mathematical calculation is preferred over bucketed branching, a lightweight integration (e.g., Make.com) can calculate the exact integer before pushing to GHL:

```javascript
let score = 0;
// Program
if (["Express Entry", "Spousal Sponsorship", "LMIA"].includes(program)) score += 30;
else if (["Study Permit", "Work Permit"].includes(program)) score += 20;
else score += 10;

// Urgency
if (urgency === "Immediate") score += 20;
else if (urgency === "1-3 months") score += 15;
else if (urgency === "3-6 months") score += 10;

// Budget
if (budget === "Accepted Paid") score += 20;
else if (budget === "Hesitant") score += 10;

// Complexity
if (complexity === "None") score += 10;
else if (complexity === "Previous Refusal") score += 5;

// Responsiveness
if (outcome === "Qualified") score += 20;
else if (outcome === "Voicemail") score += 5;

return score;
```

**Implementation Recommendation for V1**: Use the **GHL Workflow Bucketing (Branching)** approach. It requires zero external code, is easily modifiable by the firm owner directly in the GHL UI, and provides the exact same operational outcome (correct pipeline routing and tagging).