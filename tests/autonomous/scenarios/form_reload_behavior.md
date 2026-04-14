# Autonomous Test: Form Reload Behavior

## Objective
Test what happens when a user reloads the Typebot form mid-way or after completion.
Verify: does data get duplicated? Does the form restart? Is session preserved?

## Test Steps

### Test A: Reload Mid-Form
1. Navigate to https://www.neuronx.co/intake/vmc/onboarding
2. Select "Express Entry" as program
3. Answer 3-4 questions (name, email, phone)
4. Reload the page (Ctrl+R / Cmd+R)
5. Check: Does the form restart from the beginning?
6. Check: Are the previously entered answers remembered?
7. If form restarts, fill in the same answers again
8. Complete the form
9. Check via API: Was only ONE contact created, or duplicates?

### Test B: Complete Form + Revisit
1. Navigate to the form URL
2. Complete the entire form with test data
3. Navigate to the same URL again
4. Check: Does a new empty form appear?
5. Complete the form again with the SAME email
6. Check via API: Was the contact updated or duplicated?

### Test C: Multiple Tabs
1. Open the form URL in Tab 1
2. Open the same URL in Tab 2
3. Fill partial data in Tab 1
4. Fill different data in Tab 2
5. Submit Tab 1
6. Submit Tab 2
7. Check: How are the submissions handled? Two contacts? One overwritten?

## Verification
- Call GET /health to verify API is accessible
- After each form submission, wait 5s for webhook processing
- Check the scoring endpoint or webhook logs for duplicate detection

## Output
Report: duplication risk level (none/low/medium/high) with evidence.
