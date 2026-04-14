# Autonomous Test: Full Pipeline (Form → Webhook → Score → GHL Tags)

## Objective
Test the complete end-to-end pipeline by simulating a real prospect journey
through API calls. This chains all systems together without needing real
GHL/VAPI/browser access.

## Pre-requisite
- NeuronX API must be running (localhost:8000 or staging URL)
- All external services can be mocked via test endpoints

## Test Steps

### Step 1: Simulate VAPI End-of-Call
POST to /webhooks/voice with an end-of-call-report payload:
```json
{
  "message": {
    "type": "end-of-call-report",
    "call": {"id": "test-pipeline-001", "status": "ended"},
    "analysis": {
      "structuredData": {
        "program_interest": "Express Entry",
        "current_location": "Outside Canada",
        "timeline_urgency": "Near-term (1-3 months)",
        "prior_applications": "None",
        "budget_awareness": "Aware"
      },
      "summary": "Standard prospect for Express Entry"
    },
    "artifact": {
      "transcript": "Prospect wants Express Entry, in India, 1-3 month timeline."
    },
    "customer": {"number": "+14165559999"}
  }
}
```
Verify: 200 response with scoring result

### Step 2: Verify Scoring
POST to /score/lead with the same R1-R5 data:
```json
{
  "contact_id": "test-pipeline-001",
  "r1_program_interest": "Express Entry",
  "r2_current_location": "Outside Canada",
  "r3_timeline_urgency": "Near-term (1-3 months)",
  "r4_prior_applications": "None",
  "r5_budget_awareness": "Aware"
}
```
Verify: score >= 70, outcome = "ready_standard", tags include "nx:score:high"

### Step 3: Test Trust Boundary
POST to /trust/check with a transcript containing escalation trigger:
```json
{
  "transcript": "Am I eligible for Express Entry? What are my chances?",
  "contact_id": "test-pipeline-001"
}
```
Verify: requires_escalation = true, flags include "eligibility_question"

### Step 4: Test Document OCR
POST to /extract/types
Verify: returns list of 7+ supported document types

### Step 5: Test Form Rendering
GET /form/vmc/onboarding
Verify: 200 response, HTML contains "typebot", tenant branding present

### Step 6: Health Verification
GET /health/deep
Verify: all checks pass, status = "ok"

## Expected End State
- Scoring: score >= 70, outcome = "ready_standard"
- Trust: escalation detected for eligibility question
- Forms: rendering correctly with branding
- Health: all systems green

## Output
JSON summary of all 6 steps with pass/fail and response data.
