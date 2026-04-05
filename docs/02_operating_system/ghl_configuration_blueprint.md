# NeuronX V1 — GoHighLevel Configuration Blueprint (Phase 1: No Code)

Version: 1.0
Status: CANONICAL
Last Updated: 2026-03-13
Purpose: Build the entire NeuronX operational system inside GoHighLevel first

This document defines exactly what to configure in a single GHL sub-account to
make the v1 system fully testable end-to-end before writing any orchestration code.

Implements:
- `/docs/02_operating_system/operating_spec.md`
- `/docs/02_operating_system/sales_playbook.md`
- `/docs/04_compliance/trust_boundaries.md`

---

## Phase 1 Goal

Produce a working GHL sub-account where you can:

Submit a lead → see state transitions → receive messages → book consultation →
get reminders → handle no-show recovery → record consultation outcome → trigger
retainer follow-up → track pipeline.

AI calling and scoring are not required for Phase 1. This is execution-first.

---

## 0) Website Landing Page (Funnel) — Minimal UAT Page

Create a funnel or website page that allows a tester to submit a lead and book.

### Funnel/page name

**NeuronX Intake Landing (V1)**

### Must include

- Headline and short description of firm services (generic copy is fine for test)
- Embedded form: **Immigration Inquiry (V1)**
- Booking CTA linking to the **Immigration Consultations** calendar
- Compliance footer (no guarantees, no eligibility claims)

### Output required for deliverables

- The public page URL used for UAT submissions

---

## 1) Pipeline (Opportunities)

Create a pipeline named: **NeuronX — Immigration Intake**

### Stages (exact)

1. **NEW**
2. **CONTACTING**
3. **UNREACHABLE**
4. **CONSULT READY**
5. **BOOKED**
6. **CONSULT COMPLETED**
7. **RETAINED**
8. **LOST**
9. **NURTURE**

### Stage definitions

- **NEW**: Inquiry received; acknowledgment not yet sent
- **CONTACTING**: Active contact attempts in progress
- **UNREACHABLE**: 7 attempts exhausted; moved to hold and then nurture
- **CONSULT READY**: Readiness assessment complete; booking invited
- **BOOKED**: Consultation scheduled
- **CONSULT COMPLETED**: Consultation occurred; outcome recorded
- **RETAINED**: Retainer signed and first payment received
- **LOST**: Explicit decline, opt-out, disqualified, or terminal loss reason
- **NURTURE**: Long-term follow-up for not-ready and timed-out leads

---

## 2) Custom Fields (Business Data)

Create the minimum v1 fields required by the operating spec.

### Identity and source

- `lead_source` (dropdown)
- `lead_source_detail` (text)
- `utm_source` (text)
- `utm_medium` (text)
- `utm_campaign` (text)

### Readiness assessment (R1–R6)

- `program_interest` (dropdown)
- `program_interest_detail` (text)
- `current_location` (dropdown)
- `location_detail` (text)
- `timeline_urgency` (dropdown)
- `urgency_detail` (text)
- `prior_applications` (dropdown)
- `prior_application_detail` (text)
- `budget_awareness` (dropdown)
- `complexity_flags` (multi-select)
- `readiness_outcome` (dropdown)
- `assessment_completed_at` (date-time)
- `assessed_by` (text)

### Attempt tracking

- `contact_attempt_count` (number)
- `last_contact_attempt_at` (date-time)
- `last_contact_attempt_method` (dropdown)
- `last_contact_attempt_outcome` (dropdown)

### Booking

- `confirmation_status` (dropdown)
- `reschedule_count` (number)
- `consultation_type` (dropdown)
- `consultation_fee` (currency or number)

### Consultation outcome

- `consultation_outcome` (dropdown)
- `consultation_outcome_reason` (text)
- `outcome_recorded_at` (date-time)
- `outcome_recorded_by` (text)

### Retainer

- `retainer_sent` (checkbox)
- `retainer_sent_at` (date-time)
- `retainer_signed` (checkbox)
- `retainer_signed_at` (date-time)
- `payment_received` (checkbox)
- `payment_received_at` (date-time)
- `engagement_value` (currency or number)

### Consent and suppression

- `marketing_consent` (checkbox, default false)
- `marketing_consent_granted_at` (date-time)
- `marketing_consent_method` (dropdown)
- `suppression_reason` (dropdown)

---

## 3) Tags (Operational Triggers)

Use tags to trigger workflows.

### Core tags

- `nx:new_inquiry`
- `nx:contacting:start`
- `nx:contacted`
- `nx:assessment:required`
- `nx:assessment:complete`
- `nx:consult_ready`
- `nx:booking:invited`
- `nx:booking:confirmed`
- `nx:appointment:noshow`
- `nx:consult:done`
- `nx:outcome:proceed`
- `nx:outcome:follow_up`
- `nx:outcome:declined`
- `nx:retainer:sent`
- `nx:retainer:signed`
- `nx:payment:received`
- `nx:nurture:enter`
- `nx:lost`

### Compliance tags

- `nx:consent:marketing_yes`
- `nx:consent:marketing_no`
- `nx:suppressed`

---

## 4) Calendars

Create a calendar named: **Immigration Consultations**

### Required configuration

- Assign 1–N consultants
- Appointment duration: 30 minutes (standard)
- Booking widget/booking link enabled
- Confirmation page + email confirmation enabled
- Reschedule enabled

### Availability rule

- Must allow booking within 7 days for v1 testability

---

## 5) Forms (Lead Capture)

Create a primary form named: **Immigration Inquiry (V1)**

### Required fields

- First name
- Last name
- Phone
- Email
- Program interest (dropdown)
- Current location (dropdown)
- Timeline (dropdown)
- Free-text notes (optional)
- Marketing consent checkbox (unchecked by default)

### Consent language (must be explicit)

- Transactional consent: implied by submission for contacting them about their inquiry
- Marketing consent: separate checkbox, explicit

---

## 6) Workflows (Automation)

Create each workflow below. Name them exactly.

### WF-01 — New Inquiry → Acknowledge + Start Contacting

**Trigger**: Form submitted: Immigration Inquiry (V1)

**Actions**:
- Create/Update contact
- Set `lead_source` and UTM fields (if available)
- Add tag `nx:new_inquiry`
- Move opportunity to stage NEW (if opportunity exists; otherwise create opportunity in pipeline)
- Send SMS acknowledgment (firm-branded, compliant)
- Send email acknowledgment
- Add tag `nx:contacting:start`
- Move opportunity to CONTACTING

### WF-02 — Contact Attempt Sequence (Human-Only in Phase 1)

**Trigger**: Tag added `nx:contacting:start`

**Actions**:
- Create task: "Call lead (Attempt 1)"
- Wait 30 minutes
- If not contacted: send SMS with booking link and request callback
- Wait 2 hours
- Create task: "Call lead (Attempt 2)"
- Wait 1 business day
- Create task: "Call lead (Attempt 3) + leave voicemail"
- Wait 2 business days
- Send SMS with booking link
- Wait 5 business days
- Send email with booking link
- Wait 10 business days
- Send final SMS
- If still not contacted: move stage to UNREACHABLE, add tag `nx:nurture:enter`

Phase 1 constraint: do not attempt AI calling.

### WF-03 — Mark Contacted → Require Readiness Assessment

**Trigger**: Tag added `nx:contacted` (set manually by intake during Phase 1)

**Actions**:
- Add tag `nx:assessment:required`
- Create task: "Complete readiness assessment (R1–R6)"

### WF-04 — Readiness Complete → Invite Booking

**Trigger**: Tag added `nx:assessment:complete`

**Conditions**:
- If `readiness_outcome` is Ready (Standard or Urgent):
  - Move stage to CONSULT READY
  - Add tag `nx:consult_ready`
  - Send booking link (SMS + email)
  - Add tag `nx:booking:invited`
- If `readiness_outcome` is Not Ready:
  - Move stage to NURTURE
  - Add tag `nx:nurture:enter`
- If `readiness_outcome` is Disqualified:
  - Move stage to LOST
  - Add tag `nx:lost`
- If `readiness_outcome` is Ready — Complex:
  - Assign to senior consultant, create task: "Complex lead review"

### WF-05 — Appointment Booked → Confirm + Reminders

**Trigger**: Appointment booked on Immigration Consultations calendar

**Actions**:
- Move opportunity to BOOKED
- Add tag `nx:booking:confirmed`
- Send confirmation SMS + email (include agenda and link/address)
- Wait until 48 hours before appointment
- Send reminder SMS asking to reply YES to confirm
- Wait until 24 hours before appointment
- Send reminder SMS
- Wait until 2 hours before appointment
- Send reminder SMS

### WF-06 — No-Show → Recovery

**Trigger**: Appointment status = No-Show

**Actions**:
- Add tag `nx:appointment:noshow`
- Send +5 minute SMS (empathetic reschedule)
- Wait 10 minutes
- Create task: "Call no-show within 15 minutes"
- Wait 2 hours
- Send SMS with reschedule link
- Wait 1 business day
- Send SMS
- Wait 3 business days
- Send email
- Wait 7 business days
- Send final SMS
- Move to NURTURE if no rebook

### WF-07 — Consultation Completed → Outcome Capture

**Trigger**: Appointment status = Completed

**Actions**:
- Create task for consultant: "Record consultation outcome"
- Wait 1 hour
- If no outcome recorded: notify consultant again
- Wait 3 more hours
- If still missing: notify firm owner

### WF-08 — Outcome Routing

**Trigger**: Custom field `consultation_outcome` changes

**Branches**:
- Proceed:
  - Add tag `nx:outcome:proceed`
  - Move stage to CONSULT COMPLETED
  - Trigger retainer workflow (WF-09)
- Follow-Up:
  - Add tag `nx:outcome:follow_up`
  - Move stage to CONSULT COMPLETED
  - Trigger follow-up nurture (WF-10)
- Declined:
  - Add tag `nx:outcome:declined`
  - Move stage to LOST

### WF-09 — Retainer Follow-Up

**Trigger**: Tag added `nx:outcome:proceed`

**Actions**:
- Send retainer email + checklist + payment instructions (within 1 hour)
- Set `retainer_sent` true + timestamp
- Wait 1 day → send SMS check-in
- Wait 1 day → send SMS/email follow-up
- Wait 3 days → send email follow-up
- Wait 5 days → create task: "Consultant call (Day 10)"
- Wait 4 days → final email; then move to NURTURE if unsigned

### WF-10 — Post-Consult Follow-Up (Undecided)

**Trigger**: Tag added `nx:outcome:follow_up`

**Actions**:
- Day 0: send consultation summary email
- Wait 2 days: send SMS check-in
- Wait 3 days: send value-add email (program-relevant)
- Wait 2 days: call task or SMS
- Wait 7 days: gentle close email
- Move to NURTURE

### WF-11 — Nurture Campaign (Monthly)

**Trigger**: Tag added `nx:nurture:enter`

**Condition**:
- Only if `marketing_consent` is true and not suppressed

**Actions**:
- Monthly email newsletter
- Quarterly SMS check-in

---

## 7) Templates (Message Quality)

Create templates for:
- Acknowledgment SMS
- Booking link SMS
- Confirmation SMS/email
- Reminder SMS (48h/24h/2h)
- No-show recovery SMS/email
- Retainer delivery email
- Post-consultation summary email
- Nurture email

All templates must:
- Use firm name
- Avoid any claims of eligibility assessment or guaranteed outcomes
- Include opt-out in commercial messages

---

## 8) Phase 1 UAT Scenarios (Must Pass)

### Mapping to requested BUILD UAT tests

| Requested test | Covered in Phase 1? | Where |
|---|---|---|
| TEST 1 — new lead flow | Yes | UAT-01 |
| TEST 2 — AI call attempt | Not in Phase 1 | Phase 3 + live tenant bake-off (Voice AI) |
| TEST 3 — booking flow | Yes | UAT-01 |
| TEST 4 — consultation reminder | Yes | UAT-01 (BOOKED + reminders) |
| TEST 5 — no-show recovery | Yes | UAT-02 |
| TEST 6 — consultation outcome | Yes | UAT-01 |
| TEST 7 — retainer automation | Yes | UAT-01 |

### UAT-01 New lead lifecycle (happy path)

1. Submit form
2. Confirm: contact created + opportunity in NEW then CONTACTING
3. Confirm: ack SMS/email sent
4. Manually tag lead as `nx:contacted`
5. Complete readiness fields and set `readiness_outcome` = Ready
6. Add tag `nx:assessment:complete`
7. Confirm: stage moves to CONSULT READY and booking link sent
8. Book appointment
9. Confirm: stage moves to BOOKED and reminders scheduled
10. Mark appointment completed
11. Record outcome = Proceed
12. Confirm: retainer email sent and follow-up tasks created

### UAT-02 No-show recovery

1. Book appointment
2. Mark appointment as No-Show
3. Confirm: recovery SMS sent and call task created
4. Rebook using link
5. Confirm: appointment updates and reminder schedule restarts

### UAT-03 Consent suppression

1. Submit lead without marketing consent
2. Move to NURTURE
3. Confirm: no marketing emails sent
4. Toggle marketing consent true
5. Confirm: nurture email starts
6. Simulate STOP opt-out
7. Confirm: suppression applied and nurture stops

### UAT-04 Complex lead routing

1. Set readiness outcome to Ready — Complex
2. Add tag `nx:assessment:complete`
3. Confirm: assigned to senior consultant and booking not auto-sent

---

## Phase 2 — Snapshot Productization (Checklist)

1. Verify all workflows run correctly in the “gold” sub-account
2. Create snapshot from the gold sub-account
3. Confirm snapshot includes:
   - Pipeline and stages
   - Workflows
   - Forms
   - Calendars
   - Templates
   - Custom fields and tags
4. Create a new sub-account
5. Install snapshot into the new sub-account
6. Re-run UAT-01 through UAT-04
7. Measure install time and record manual steps

---

## Phase 3 — NeuronX Thin Brain (When to Start)

Start orchestration only after Phase 1 and Phase 2 pass.

Phase 3 adds:
- AI calling (GHL Voice AI or external)
- Automated readiness scoring based on transcript
- Consultation briefing assembly
- Analytics beyond native dashboards
- Stuck lead detection beyond basic triggers

Constraints:
- NeuronX must not replace any GHL-native capability
- NeuronX must follow product boundary and trust boundaries
