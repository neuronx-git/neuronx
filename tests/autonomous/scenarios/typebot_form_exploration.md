# Autonomous Test: Typebot Form Exploration

## Objective
Navigate to the NeuronX onboarding form and test all 8 immigration program branches.
For each branch, verify that correct program-specific questions appear and incorrect
questions do NOT appear.

## Environment
- URL: https://www.neuronx.co/intake/vmc/onboarding
- Typebot form runs inside an iframe embed
- 8 program branches: Express Entry, Spousal Sponsorship, Study Permit, Work Permit,
  LMIA, PR Renewal, Citizenship, Visitor Visa

## Test Steps

### For EACH of the 8 programs:

1. Navigate to https://www.neuronx.co/intake/vmc/onboarding
2. Wait for the Typebot iframe to load (look for chat-like interface)
3. When asked about program interest, select the target program
4. Proceed through ALL questions until the form completes or loops
5. Record every question text that appears
6. Take a screenshot after completing the form

### Verification Checklist (per program):

- [ ] Welcome message displayed
- [ ] Program selection question appeared
- [ ] Program-specific questions matched the expected set
- [ ] No questions from other programs appeared
- [ ] Mandatory fields enforced (cannot skip without answering)
- [ ] Form reached completion (thank you / summary)
- [ ] No JavaScript errors in console
- [ ] No broken UI elements

### Expected Program-Specific Questions:

**Express Entry**: CRS score, language test type, education level, work experience years, NOC code
**Spousal Sponsorship**: Relationship type, sponsor status, cohabitation proof
**Study Permit**: Institution name, program of study, acceptance letter, proof of funds
**Work Permit**: Employer name, LMIA status, job offer details
**LMIA**: Business name, NOC code, wages offered, recruitment efforts
**PR Renewal**: PR card number, residency days, travel history
**Citizenship**: PR duration, language test, criminal record check
**Visitor Visa**: Purpose of visit, ties to home country, invitation letter

## Output Format

Produce a JSON report:
```json
{
  "programs_tested": 8,
  "programs_passed": N,
  "programs_failed": N,
  "details": [
    {
      "program": "Express Entry",
      "questions_seen": ["..."],
      "unexpected_questions": ["..."],
      "missing_questions": ["..."],
      "mandatory_fields_enforced": true,
      "completed_successfully": true,
      "screenshot": "express_entry_complete.png"
    }
  ]
}
```

## Safety
- Do NOT submit real personal data (use test data only)
- Do NOT interact with any payment or billing forms
- Do NOT navigate away from neuronx.co domain
