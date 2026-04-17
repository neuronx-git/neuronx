# NeuronX E2E Resource Sync Audit

**Generated:** 2026-04-17T12:27:20.564529Z


## 🎯 Executive Summary

| Resource | Sandbox | Prod VMC | Gap | Status |
|---|---|---|---|---|
| Custom Fields | 140 | 140 | 0 missing | ✅ |
| Tags | 104 | 116 | 0 missing | ✅ |
| Pipelines | 2 | 1 | 1 missing | ❌ |
| Calendars | 3 | 1 | 3 missing | ⚠️ |
| Workflows | 24 | 18 | 9 missing, 3 broken | ❌ |
| Forms | 2 | 1 | 1 missing | ⚠️ |
| Emails | 11 | 33 | Production has +22 (new premium) | ✅ |
- **Sandbox:** `FlRL82M0D6nclmKT7eXH`
- **Production VMC:** `vb8iWAwoLi2uT3s5v1OW`


## 1. Custom Fields

| | Sandbox | Production VMC |
|---|---|---|
| Count | 140 | 140 |
| Only in sandbox | 0 | — |
| Only in VMC | — | 0 |
| Common | 140 | 140 |


## 2. Tags

| | Sandbox | VMC |
|---|---|---|
| Count | 104 | 116 |

**Tags only in VMC (12):** `follow-up, high priority, nx:consult:completed, nx:consult:ready, nx:decision:approved, nx:decision:refused, nx:new, nx:no_show, nx:nurture, nx:urgent, nx:winback, warm lead`

## 3. Pipelines

**Sandbox (2 pipelines):**

- **NeuronX - Case Processing** (9 stages): ONBOARDING → DOC COLLECTION → FORM PREPARATION → INTERNAL REVIEW → SUBMITTED TO IRCC → PROCESSING → ADDITIONAL INFO (RFI) → DECISION RECEIVED → CASE CLOSED
- **NeuronX — Immigration Intake** (10 stages): NEW → CONTACTING → UNREACHABLE → CONSULT READY → BOOKED → CONSULT COMPLETED → PROPOSAL SENT → RETAINED → LOST → NURTURE

**Production VMC (1 pipelines):**

- **NeuronX — Immigration Intake** (10 stages): NEW → CONTACTING → UNREACHABLE → CONSULT READY → BOOKED → CONSULT COMPLETED → PROPOSAL SENT → RETAINED → LOST → NURTURE

⚠️ **Missing pipelines in VMC:** `NeuronX - Case Processing`

## 4. Calendars

**Sandbox (3):** 
`VMC — Free Initial Assessment` (15min), `VMC — Paid Consultation` (30min), `VMC — Strategy Session (Complex Cases)` (60min)

**VMC (1):** 
`Immigration Consultations` (30min)

⚠️ **Missing calendars in VMC:** VMC — Paid Consultation, VMC — Free Initial Assessment, VMC — Strategy Session (Complex Cases)

## 5. Workflows

| | Sandbox | VMC |
|---|---|---|
| Count | 24 | 18 |
| Missing in VMC | 9 | — |
| Extra in VMC | — | 3 |


**Workflows missing from VMC (9):**

- ❌ WF-CP-01: Client Onboarding
- ❌ WF-CP-02: Document Collection Reminders
- ❌ WF-CP-03: Form Preparation
- ❌ WF-CP-04: Internal Review
- ❌ WF-CP-05: IRCC Submission
- ❌ WF-CP-06: Processing Status Checks
- ❌ WF-CP-07: Additional Info (RFI)
- ❌ WF-CP-08: Decision Received
- ❌ WF-CP-09: Case Closure

**Workflows only in VMC (3):**

- 🚧 🚧 Processing - WF-10 Post-Consult Follow-Up (status: draft)
- 🚧 🚧 Processing - WF-11 Nurture Campaign Monthly (status: draft)
- 🚧 🚧 Processing - WF-13 PIPEDA Data Deletion Request (status: draft)

## 6. Forms

**Sandbox (2):** Form 1, Immigration Inquiry (V1)

**VMC (1):** Immigration Inquiry (V1)

## 7. Email Templates

| | Sandbox | VMC |
|---|---|---|
| Count | 11 | 33 |


**Email templates missing from VMC (11):**

- 01-inquiry-received
- 02-consultation-confirmed
- 03-consultation-reminder
- 04-noshow-recovery
- 05-retainer-proposal
- 06-pipeda-acknowledgement
- 07-monthly-nurture
- 08-complex-case-alert
- 09-pipeda-deletion
- 10-retainer-followup
- 11-winback-nurture

**Email templates only in VMC (33) — our 26 premium + 14 originals:**

- ✓ VMC-01-inquiry-received
- ✓ VMC-02-outreach-attempt
- ✓ VMC-03-invite-booking
- ✓ VMC-04-consultation-confirmed
- ✓ VMC-05-consultation-reminder
- ✓ VMC-06-noshow-recovery
- ✓ VMC-07-retainer-proposal
- ✓ VMC-08-retainer-followup
- ✓ VMC-09-score-medium-handler
- ✓ VMC-10-monthly-nurture
- ✓ VMC-11-winback-nurture
- ✓ VMC-12-pipeda-ack
- ✓ VMC-13-pipeda-deleted
- ✓ VMC-14-complex-case-alert
- ✓ VMC-15-case-onboarding
- ✓ VMC-16-cp-docs-reminder
- ✓ VMC-17-cp-form-prep
- ✓ VMC-18-cp-internal-review
- ✓ VMC-19-cp-submitted
- ✓ VMC-20-cp-status-update
- ✓ VMC-21-cp-rfi
- ✓ VMC-22-cp-decision-approved
- ✓ VMC-23-cp-decision-refused
- ✓ VMC-24-cp-decision-withdrawn
- ✓ VMC-25-cp-case-closed
- ✓ VMC-26-missed-ai-call
- ✓ VMC-consultation-confirmed
- ✓ VMC-consultation-reminder
- ✓ VMC-inquiry-received
- ✓ VMC-monthly-nurture-base
- ✓ VMC-noshow-recovery
- ✓ VMC-pipeda-acknowledgement
- ✓ VMC-retainer-proposal