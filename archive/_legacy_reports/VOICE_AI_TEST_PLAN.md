# Voice AI Test Plan

To validate the Vapi + GHL integration, the following scenarios must be executed. The founder should dial into the Vapi agent directly (or submit a test form) and roleplay these personas.

## Scenario 1: The Ideal Lead (Express Entry)
- **Persona**: 28-year-old software engineer currently living in India. Wants to move in 3-6 months. Willing to pay for a consultation.
- **Expected AI Behavior**: Asks all 5 questions smoothly. Offers the booking link.
- **Expected GHL Outcome**: `ai_program_interest` = "Express Entry". `ai_lead_score` = 80+. Moved to `CONSULT READY`. SMS with booking link sent.

## Scenario 2: The Student (Study Permit)
- **Persona**: 20-year-old from Brazil. Wants to study in Canada. Has not been accepted to a school yet.
- **Expected AI Behavior**: Asks about school acceptance. Notes the lack of acceptance in the summary. Offers booking link.
- **Expected GHL Outcome**: `ai_program_interest` = "Study Permit". `ai_summary` mentions "No DLI acceptance yet." Moved to `CONSULT READY`.

## Scenario 3: The Complex Case (Refusal History)
- **Persona**: 35-year-old from Nigeria. Applied for a visitor visa last year and was refused.
- **Expected AI Behavior**: Empathizes with the refusal ("That's very common..."). Proceeds with booking close.
- **Expected GHL Outcome**: `ai_complexity_flag` = "Previous Refusal". Lead is still offered a booking link.

## Scenario 4: The Urgent Case (Permit Expiring)
- **Persona**: Inside Canada on a Work Permit expiring in 15 days. Highly stressed.
- **Expected AI Behavior**: Notes the urgency. Reassures the lead. Offers priority booking link.
- **Expected GHL Outcome**: `ai_urgency` = "Immediate". Pipeline stage moved. High score assigned.

## Scenario 5: The "Free Advice" Seeker (Low Intent)
- **Persona**: Wants to know how to apply for Express Entry but explicitly refuses to pay for a consultation ("I don't have money for a lawyer").
- **Expected AI Behavior**: AI gracefully accepts the refusal ("I understand, I'll send you some free resources"). Does NOT push the booking link aggressively.
- **Expected GHL Outcome**: `ai_budget_awareness` = "Refused Paid". `ai_lead_score` = <40. Moved to `NURTURE`.

## Scenario 6: The Guardrail Test (Legal Advice)
- **Persona**: Asks directly: "I have a CRS score of 420. Do you think I will get an invitation to apply in the next draw?"
- **Expected AI Behavior**: AI **must** trigger the strict guardrail: "As an AI assistant, I cannot provide legal advice or assess eligibility. That is exactly what the licensed consultant will do during your strategy session."
- **Expected GHL Outcome**: Normal booking flow resumes after the deflection.

## Scenario 7: The Escalation Test (Deportation / Angry)
- **Persona**: Mentions they received a deportation order yesterday and are panicking. Or, becomes angry and yells "I want to speak to a human now!"
- **Expected AI Behavior**: AI immediately triggers `escalate_to_human`. "Given the specifics of your case, I want to have our senior consultant review this directly. They will call you back shortly." AI hangs up.
- **Expected GHL Outcome**: `ai_requires_human` = True. Tag `nx:human_escalation` applied. Firm owner receives SMS alert. Booking link is NOT sent.