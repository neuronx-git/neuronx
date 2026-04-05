# AI Lead Scoring Model

## Scoring Philosophy
The scoring model operates on a 0-100 scale. It evaluates the data extracted by the AI voice agent (or intake form) to determine the lead's quality, urgency, and routing path.

## Scoring Dimensions (100 Points Total)

1. **Program Fit (30 points)**
   - Express Entry / Spousal Sponsorship / LMIA: +30
   - Study Permit / Work Permit (Standard): +20
   - Visitor Visa / Other: +10
   - Unknown/Unclear: 0

2. **Urgency (20 points)**
   - Immediate (< 30 days, e.g., permit expiring): +20
   - Near-term (1-3 months): +15
   - Medium (3-6 months): +10
   - Long-term (6+ months) / "Just browsing": +0

3. **Budget / Financial Seriousness (20 points)**
   - Agrees to paid consultation: +20
   - Asks about pricing but remains open: +10
   - Explicitly refuses paid consultation / looking for free advice: 0

4. **Complexity (10 points)**
   - Clean history (No refusals, no criminality): +10
   - Standard Refusal (e.g., previous visitor visa denied): +5
   - Severe Complexity (Inadmissibility, deportation): 0 (Score doesn't matter; triggers immediate human escalation)

5. **Communication Responsiveness (20 points)**
   - Answers first AI call and completes assessment: +20
   - Answers on second attempt: +10
   - Voicemail / SMS only: +5

---

## Score Bands & Routing Rules

| Score Band | Classification | Tag Applied | Pipeline Routing | Action |
| :--- | :--- | :--- | :--- | :--- |
| **80 – 100** | **High Priority** | `nx:score:high` | `CONSULT READY` | Send priority booking link. Alert team if not booked within 4 hours. |
| **60 – 79** | **Qualified** | `nx:score:med` | `CONSULT READY` | Send standard booking link via SMS/Email. |
| **40 – 59** | **Low Intent** | `nx:score:low` | `NURTURE` | Do not aggressively push booking. Send educational email sequences. |
| **0 – 39** | **Unqualified** | `nx:score:junk` | `LOST` | Archive. Stop automation. |

*(Note: Any lead flagged with `ai_requires_human = true` bypasses scoring routing and moves immediately to human review).*

---

## GHL Custom Field Mapping

The following Custom Fields must be created in GHL to store the AI's output and feed the scoring engine:

- `ai_program_interest` (Dropdown: Express Entry, Study, Work, Sponsorship, Visitor, PNP, Other)
- `ai_country` (Text: Extracted country name)
- `ai_urgency` (Dropdown: Immediate, 1-3 months, 3-6 months, 6+ months)
- `ai_complexity_flag` (Text: None, Refusal, Criminality, Deportation)
- `ai_budget_awareness` (Dropdown: Accepted Paid, Hesitant, Refused Paid)
- `ai_lead_score` (Numerical: 0-100)
- `ai_call_outcome` (Dropdown: Qualified, Not Ready, Voicemail, Disconnected)
- `ai_requires_human` (Checkbox: True/False)
- `ai_booking_status` (Dropdown: Requested, Declined, Unclear)
- `ai_summary` (Large Text: 2-3 sentence AI generated summary of the call)