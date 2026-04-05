# NeuronX Founder Sanity Check

## Purpose
Quick 3-minute verification that the clean-installed snapshot is functionally intact.

## Target Tenant
- **Location ID**: `FlRL82M0D6nclmKT7eXH` (or new clean install ID)
- **Context**: This checklist verifies the snapshot installation, NOT the gold source.

## Checklist

### 1. Pipeline Verification
- [ ] Navigate to: **Opportunities > Pipelines**.
- [ ] Confirm pipeline named: `NeuronX - Immigration Intake` exists.
- [ ] Confirm stages (in order):
  - [ ] NEW
  - [ ] CONTACTING
  - [ ] UNREACHABLE
  - [ ] CONSULT READY
  - [ ] BOOKED
  - [ ] CONSULT COMPLETED
  - [ ] RETAINED
  - [ ] LOST
  - [ ] NURTURE

### 2. Workflow Verification
- [ ] Navigate to: **Automation > Workflows**.
- [ ] Confirm **11 workflows** exist with these exact names:
  - [ ] WF-01: New Inquiry Acknowledge
  - [ ] WF-02: Contact Attempt Sequence
  - [ ] WF-03: Mark Contacted → Readiness
  - [ ] WF-04: Readiness Complete → Invite Booking
  - [ ] WF-05: Appointment Booked → Reminders
  - [ ] WF-06: No-Show → Recovery
  - [ ] WF-07: Consultation Outcome Capture
  - [ ] WF-08: Outcome Routing
  - [ ] WF-09: Retainer Follow-Up
  - [ ] WF-10: Post-Consult Follow-Up (Undecided)
  - [ ] WF-11: Nurture Campaign Monthly
- [ ] Open **WF-01** and confirm:
  - [ ] Trigger: Form Submitted (`Immigration Inquiry (V1)`)
  - [ ] Actions include: SMS, Email, Tags, Pipeline updates.

### 3. Landing Page Verification
- [ ] Navigate to: **Sites > Funnels**.
- [ ] Confirm funnel named: `NeuronX Intake Landing (V1)` exists.
- [ ] Click the funnel > find step: `Immigration Inquiry`.
- [ ] Click **Preview** (or the link icon).
- [ ] Confirm the live page loads with:
  - [ ] Headline: "Immigration Advice Backed by a Structured Assessment Process"
  - [ ] Trust signals section (Licensed, Structured, Global)
  - [ ] Programs section (6 cards)
  - [ ] Form visible at bottom.

### 4. Form Verification
- [ ] Navigate to: **Sites > Forms**.
- [ ] Confirm form named: `Immigration Inquiry (V1)` exists.
- [ ] Click **Edit** or **Preview**.
- [ ] Confirm fields:
  - [ ] First Name
  - [ ] Last Name
  - [ ] Email
  - [ ] Phone
  - [ ] Program Interest (dropdown)
  - [ ] Current Location (dropdown)
  - [ ] Timeline (dropdown)

### 5. Calendar Verification
- [ ] Navigate to: **Calendars**.
- [ ] Confirm calendar named: `Immigration Consultations` exists.
- [ ] Click the calendar.
- [ ] Confirm it has:
  - [ ] A linked team member (or placeholder).
  - [ ] A booking link available.

### 6. Spot-Check UAT Evidence
- [ ] Navigate to: **Contacts**.
- [ ] Search for: `clean@neuronx.ai` (or the UAT test email used).
- [ ] If found, open the contact.
- [ ] Confirm:
  - [ ] Pipeline entry visible.
  - [ ] SMS/Email communication logged.

## Verdict
- **PASS**: All 6 sections checked. System is snapshot-valid.
- **FAIL**: Any missing item indicates incomplete installation or corruption.

## Actions on Failure
1. Verify snapshot was fully loaded (all asset types selected).
2. Re-run snapshot install if necessary.
3. Check GHL logs for errors during install.
