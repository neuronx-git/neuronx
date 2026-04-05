# NeuronX V1 Operating Specification

Version: 1.0
Status: CANONICAL
Last Updated: 2026-03-13
Authority: Founder
Implements: /docs/01_product/prd.md v3.0

---

## Operating Model (Layered Execution)

This operating specification assumes a strict responsibility split:

- **Layer 1 — GoHighLevel (execution layer)**: lead capture, CRM recordkeeping, workflows, pipeline movement, calendars, messaging sequences, reminders
- **Layer 2 — NeuronX (intelligence layer)**: readiness scoring, consultation briefing assembly, analytics, stuck-lead detection, trust boundary enforcement, webhook verification, and voice-layer outcome normalization

**Voice layer note**: AI calling in v1 may be executed by GoHighLevel Voice AI or an external provider. The bake-off determines which is used; this spec defines the required operational outcomes regardless of provider.

## 1. V1 Core Outcomes

| # | Outcome | Measurable Criteria |
|---|---|---|
| O1 | Every inquiry receives first contact within 5 min (AI) or 30 min (human) | Median speed-to-first-contact measured from inquiry timestamp to first outbound contact |
| O2 | Every contactable lead goes through structured readiness assessment before consultation offer | 100% of leads in CONTACTED state have assessment data before transitioning to CONSULT READY |
| O3 | Every booked consultation has a preparation briefing delivered to the consultant | Briefing delivered for >= 95% of booked consultations, >= 15 min before appointment |
| O4 | Every no-show triggers recovery within 15 minutes | Recovery sequence initiated for 100% of detected no-shows |
| O5 | Every completed consultation has outcome recorded and next action triggered within 1 hour | Outcome capture rate >= 90%. Retainer sent within 1 hour for "proceed" outcomes. |
| O6 | Firm owner can see pipeline health daily without asking anyone | Dashboard or daily briefing accessible with core metrics, updated at least daily |
| O7 | No AI interaction crosses a trust boundary | Zero incidents of AI providing eligibility assessments, program recommendations, legal advice, or outcome promises |

---

## 2. V1 Operational Flows

### FLOW 1: Inquiry Intake

| Element | Specification |
|---|---|
| **Trigger** | Prospect submits inquiry (web form, Facebook lead ad, missed call, WhatsApp, email, manual entry) |
| **Inputs** | Name, phone number, email (minimum). Optional: inquiry type, source, message |
| **Steps** | 1. Create lead record with timestamp and source tag. 2. Validate phone number format. 3. Assign state: NEW. 4. Log consent (inquiry = implied transactional consent; marketing requires explicit). 5. Trigger Flow 2. |
| **Outputs** | Lead record created. State = NEW. Source tagged. Consent logged. |
| **Failure** | Missing phone AND email: create record, flag "INCOMPLETE." Duplicate within 30 days: merge, log duplicate source, do not restart sequence. |
| **Fallback** | Incomplete records flagged for operator review within 1 business hour. |
| **Escalation** | Operator reviews incomplete records. |

### FLOW 2: First Response

| Element | Specification |
|---|---|
| **Trigger** | Lead enters NEW state |
| **Inputs** | Lead record |
| **Steps** | 1. Send instant acknowledgment (SMS/email) within 60 seconds. 2. Transition: NEW -> CONTACTING. 3. Trigger Flow 3. |
| **Outputs** | Acknowledgment sent. State = CONTACTING. Timestamp logged. |
| **Failure** | SMS/email delivery failure. |
| **Fallback** | SMS fails: attempt email. Email bounces: attempt call. Both fail: flag "DELIVERY FAILED." |
| **Escalation** | Delivery failure flagged for operator within 30 minutes. |

### FLOW 3: Contact Attempts

| Element | Specification |
|---|---|
| **Trigger** | Lead enters CONTACTING state |
| **Inputs** | Lead record, contact preferences, time zone |

**Contact Sequence**:

| Attempt | Timing | Method | Content |
|---|---|---|---|
| 1 | Within 5 min of inquiry | AI outbound call | Introduction, gather initial info, offer booking |
| 2 | 30 min after attempt 1 | SMS | Personalized message + booking link |
| 3 | 2 hours after attempt 1 | AI or human call | Second call attempt |
| 4 | Next business day AM | Call + voicemail | Follow-up reference |
| 5 | 2 business days | SMS | Booking link |
| 6 | 5 business days | Email | Firm intro + booking link |
| 7 | 10 business days | SMS | Final direct attempt |

| Element | Specification |
|---|---|
| **Outputs** | Contacted -> assessment (Flow 4). OR All 7 exhausted -> UNREACHABLE. |
| **Failure** | AI provider fails. All attempts exhausted. Lead opts out. |
| **Fallback** | AI fail: SMS fallback for that attempt; next attempt routes to human. Provider down: all to human queue. |
| **Escalation** | After attempt 3 with no contact: lead in operator priority queue. Opt-out: immediate suppression. |

### FLOW 4: Readiness Assessment

| Element | Specification |
|---|---|
| **Trigger** | Lead successfully contacted (live conversation) |
| **Inputs** | Lead record, conversation context |

**Readiness Dimensions**:

| Dimension | Data | Assessed By |
|---|---|---|
| R1: Program Interest | Express Entry, spousal, study, work, LMIA, other | AI or human |
| R2: Current Location | In Canada or abroad | AI or human |
| R3: Timeline / Urgency | Permit expiring, ITA received, long-term | AI or human |
| R4: Prior History | Previous applications, approvals, refusals | AI or human |
| R5: Budget Awareness | Understanding that services have a cost | Human preferred |
| R6: Complexity Screening | Multiple refusals, inadmissibility, deportation, minors, misrepresentation | Human only |

**Readiness Outcomes**:

| Outcome | Criteria | Next State |
|---|---|---|
| Ready -- Standard | R1-R5 answered, no R6 flags | CONSULT READY |
| Ready -- Urgent | R3 indicates deadline within 30 days | CONSULT READY (priority flag) |
| Ready -- Complex | R6 flag present | Held for senior review |
| Not Ready | Prospect explicitly not ready | NURTURE |
| Disqualified | Unrelated inquiry, no genuine need | LOST (reason: disqualified) |

| Element | Specification |
|---|---|
| **Outputs** | Dimensions logged. Outcome assigned. State transitioned. |
| **Failure** | Disconnect before complete. AI cannot determine program interest. |
| **Fallback** | Incomplete: log what was gathered, flag "PARTIAL ASSESSMENT," assign to operator. |
| **Escalation** | Any R6 flag: mandatory human review. AI low confidence: human queue. Prospect requests human: immediate handoff. |

### FLOW 5: Booking

| Element | Specification |
|---|---|
| **Trigger** | Lead enters CONSULT READY state |
| **Inputs** | Lead record with readiness data, consultant calendar |
| **Steps** | 1. Send booking invitation (SMS + email) with calendar link. 2. If booked: -> BOOKED, assign consultant, trigger Flow 6. 3. If not booked within 48h: follow-up message. 4. No booking within 5 days: operator assigned for manual attempt. 5. No booking within 14 days: -> NURTURE. |
| **Outputs** | BOOKED with consultant assigned. OR NURTURE. |
| **Failure** | No consultant availability within 7 days. Booking link error. |
| **Fallback** | No availability: notify firm owner. Link error: operator books manually. |
| **Escalation** | Urgent leads with no 48h availability: escalate to firm owner for emergency slot. |

### FLOW 6: Reminders

| Element | Specification |
|---|---|
| **Trigger** | Lead enters BOOKED state |

| Timing | Channel | Content |
|---|---|---|
| On booking | SMS + Email | Confirmation with date, time, consultant, agenda, link/address |
| 48h before | SMS | Reminder + "Reply YES to confirm" |
| 24h before | SMS | Reminder with link/address |
| 2h before | SMS | Final reminder |

| Element | Specification |
|---|---|
| **Outputs** | 4 touches sent. Confirmation reply logged. |
| **Failure** | SMS failure. Cancellation. Reschedule request. |
| **Fallback** | SMS fail: email. Cancel: offer reschedule. Reschedule: update, restart reminders. |
| **Escalation** | No confirmation reply to 48h AND no contact: operator calls at 24h. |

### FLOW 7: No-Show Recovery

| Element | Specification |
|---|---|
| **Trigger** | Appointment time + 5 min, no prospect contact |

| Step | Timing | Method |
|---|---|---|
| 1 | +5 min | SMS: "Is everything okay? Happy to reschedule." |
| 2 | +15 min | Call (human or AI) |
| 3 | +2 hours | SMS with rescheduling link |
| 4 | +1 business day | SMS |
| 5 | +3 business days | Email + booking link + direct number |
| 6 | +7 business days | SMS final attempt |

| Element | Specification |
|---|---|
| **Outputs** | Rebooked -> BOOKED (restart reminders). OR 6 attempts exhausted -> NURTURE. |
| **Failure** | Explicit cancel. All attempts exhausted. |
| **Fallback** | Cancellation: log reason, LOST or NURTURE based on reason. |
| **Escalation** | Priority leads: operator calls at step 2 instead of AI. |

### FLOW 8: Consultation Preparation

| Element | Specification |
|---|---|
| **Trigger** | Appointment within prep window (default: 30 min before) |
| **Inputs** | All lead data from CRM |
| **Steps** | 1. Pull data: contact, custom fields, notes, tags, appointment. 2. Assemble structured briefing: Header, Inquiry Summary, Readiness Data, Interaction History, Preparation Notes. 3. Deliver: primary = email, secondary = CRM note. 4. Log delivery timestamp. |
| **Outputs** | Briefing assembled, delivered, logged. |
| **Failure** | Insufficient data. Email failure. |
| **Fallback** | Incomplete data: partial briefing with flags. Email fail: CRM note + SMS alert to consultant. |
| **Escalation** | None (serves the human). |

### FLOW 9: Post-Consultation Outcome Capture

| Element | Specification |
|---|---|
| **Trigger** | Appointment time + duration + 15 min |
| **Steps** | 1. Prompt consultant for outcome. 2. Capture outcome. 3. Route. |

**Outcomes**:

| Outcome | Next Action |
|---|---|
| Proceed to Retainer | Trigger Flow 10. State -> CONSULT COMPLETED (sub: proceed). |
| Needs Follow-Up | Timed nurture sequence. State -> CONSULT COMPLETED (sub: follow_up). |
| Declined | State -> LOST. Log reason. |
| Complex -- Senior Review | Route to senior queue. State -> CONSULT COMPLETED (sub: complex). |
| No-Show | Trigger Flow 7 (if not already caught). |

| Element | Specification |
|---|---|
| **Failure** | Consultant does not record within 1 hour. |
| **Fallback** | 1h: reminder. 4h: escalation to firm owner. |
| **Escalation** | Non-compliance escalated to firm owner. |

### FLOW 10: Follow-Up to Retainer

| Element | Specification |
|---|---|
| **Trigger** | Outcome = "Proceed to Retainer" |
| **Steps** | Within 1 hour: send retainer + document checklist + payment instructions. |

**Follow-Up Sequence**:

| Day | Channel | Content |
|---|---|---|
| 0 (within 1h) | Email | Retainer agreement + checklist + payment link |
| 1 | SMS | Check-in |
| 2 | SMS or call | Walk through next steps |
| 5 | Email | Follow-up with urgency context |
| 10 | Call | Human call from consultant (not automated) |
| 14 | Email | Final follow-up. If unsigned -> NURTURE. |

| Element | Specification |
|---|---|
| **Outputs** | Signed + paid -> RETAINED. Unsigned after 14 days -> NURTURE. |
| **Failure** | Email failure. Payment failure. Prospect ghosts. |
| **Fallback** | Email fail: SMS with link. Payment fail: operator contacts about alternatives. |
| **Escalation** | Day 5+ unsigned: consultant follows up. Day 10: consultant calls personally. |

---

## 3. States and Status Model

### 3.1 Primary States

| State | Definition | Entry | Exit |
|---|---|---|---|
| **NEW** | Inquiry received, not yet acknowledged | Inquiry submitted | Acknowledgment sent -> CONTACTING |
| **CONTACTING** | Attempting to reach prospect | Acknowledgment sent | Contact made -> assessment. OR 7 attempts -> UNREACHABLE |
| **UNREACHABLE** | All contact attempts exhausted | 7 attempts, no response | 30-day hold -> NURTURE. OR re-initiates -> CONTACTING |
| **CONSULT READY** | Assessment complete, cleared for consultation | Readiness outcome = Ready | Booked -> BOOKED. OR 14 days -> NURTURE |
| **BOOKED** | Consultation scheduled | Appointment created | Consultation occurs -> CONSULT COMPLETED. No-show -> recovery |
| **CONSULT COMPLETED** | Consultation occurred, outcome recorded | Outcome captured | -> RETAINED / NURTURE / LOST per outcome |
| **RETAINED** | Retainer signed, payment confirmed | Retainer + payment | Terminal. Handoff to case management. |
| **LOST** | Prospect will not proceed | Declined at any stage | Terminal. Can move to NURTURE if reason supports. |
| **NURTURE** | Long-term follow-up | Various timeout conditions | Re-initiates -> appropriate active state |

### 3.2 State Transitions

```
NEW -> CONTACTING -> [contact] -> assessment -> CONSULT READY -> BOOKED -> CONSULT COMPLETED -> RETAINED
                  -> [7 fail] -> UNREACHABLE -> [30d] -> NURTURE
                                             -> [re-initiates] -> CONTACTING
CONSULT READY -> [14d no booking] -> NURTURE
BOOKED -> [no-show, recovery fails] -> NURTURE
CONSULT COMPLETED -> [proceed] -> retainer flow -> RETAINED
CONSULT COMPLETED -> [declined] -> LOST
CONSULT COMPLETED -> [thinking, 14d] -> NURTURE
CONSULT COMPLETED -> [complex] -> senior review -> CONSULT READY (re-book) or LOST
Any state -> [opt-out] -> LOST (reason: opt-out, suppressed)
Any state -> [prospect re-initiates] -> appropriate active state
```

### 3.3 Sub-Statuses

| State | Sub-Status | Meaning |
|---|---|---|
| CONTACTING | attempt_1 through attempt_7 | Current attempt |
| CONTACTING | ai_attempt / human_attempt | Attempt type |
| UNREACHABLE | hold / released_to_nurture | Hold period vs released |
| CONSULT READY | standard / urgent / complex_pending_review | Readiness type |
| BOOKED | confirmed / unconfirmed | Confirmation reply received |
| BOOKED | noshow_recovery_active | Recovery in progress |
| CONSULT COMPLETED | proceed / follow_up / declined / complex | Outcome |
| LOST | declined / disqualified / opt_out / unreachable_expired | Reason |
| NURTURE | from_unreachable / from_booking_timeout / from_consult_undecided / from_retainer_timeout | Entry source |

---

## 4. Required Data Model

### 4.1 Lead Record (Core)

| Field | Type | Required | Source |
|---|---|---|---|
| Lead ID | Unique ID | Yes | System |
| First Name | Text | Yes | Intake |
| Last Name | Text | No | Intake |
| Phone Number | Phone | Yes | Intake |
| Email | Email | Conditional | Intake |
| Current State | Enum | Yes | System |
| Current Sub-Status | Enum | No | System |
| State Changed At | Timestamp | Yes | System |
| Created At | Timestamp | Yes | System |
| Assigned Operator | Reference | No | System/manual |
| Assigned Consultant | Reference | No | At booking |
| Priority Flag | Boolean | No | System |
| Notes | Text (append-only) | No | Any |

### 4.2 Source Attribution

| Field | Type | Required |
|---|---|---|
| Lead Source | Enum (Web Form, Facebook Ad, Google Ad, Phone Call, WhatsApp, Referral, Walk-In, Email, Other) | Yes |
| Source Detail | Text | No |
| UTM Source / Medium / Campaign | Text | No |
| First Touch Channel | Enum | Yes |

### 4.3 Readiness Assessment

| Field | Type | Required | Assessed By |
|---|---|---|---|
| Program Interest | Enum (Express Entry, Spousal, Study, Work, LMIA, PR Renewal, Citizenship, Visitor, Other, Unknown) | Yes | AI or human |
| Program Interest Detail | Text | No | AI or human |
| Current Location | Enum (In Canada, Outside Canada, Unknown) | Yes | AI or human |
| Location Detail | Text | No | AI or human |
| Timeline Urgency | Enum (Urgent 30d, Near-term 1-3mo, Medium 3-6mo, Long-term 6mo+, Unknown) | Yes | AI or human |
| Urgency Detail | Text | No | AI or human |
| Prior Applications | Enum (None, Approved only, Has refusal(s), Unknown) | Yes | AI or human |
| Prior Application Detail | Text | No | AI or human |
| Budget Awareness | Enum (Aware, Unaware, Unclear, Not discussed) | No | Human preferred |
| Complexity Flags | Multi-select (None, Multiple refusals, Inadmissibility, Deportation/removal, Custody, Misrepresentation, Active case elsewhere, Minor involved) | No | Human only |
| Readiness Outcome | Enum (Ready Standard, Ready Urgent, Ready Complex, Not Ready, Disqualified) | Yes | System/human |
| Assessment Completed At | Timestamp | Yes | System |
| Assessed By | Reference or "AI" | Yes | System |

### 4.4 Booking

| Field | Type | Required |
|---|---|---|
| Consultation Date/Time | Datetime | Yes |
| Duration | Integer (minutes) | Yes |
| Type | Enum (Video, Phone, In-Person) | Yes |
| Fee | Currency | No |
| Booking Created At | Timestamp | Yes |
| Booking Source | Enum (Auto link, Manual link, Operator, Consultant) | Yes |
| Confirmation Status | Enum (Unconfirmed, Confirmed, Cancelled, Rescheduled) | Yes |
| Rescheduled From | Datetime | No |
| Reschedule Count | Integer | Yes |

### 4.5 Consultation Outcome

| Field | Type | Required |
|---|---|---|
| Occurred | Boolean | Yes |
| Outcome | Enum (Proceed, Follow-Up, Declined, Complex, No-Show) | Yes |
| Outcome Reason | Text | Yes for Follow-Up/Declined/Complex |
| Recorded At | Timestamp | Yes |
| Recorded By | Reference | Yes |
| Retainer Sent / Sent At | Boolean / Timestamp | No |
| Retainer Signed / Signed At | Boolean / Timestamp | No |
| Payment Received / Amount / At | Boolean / Currency / Timestamp | No |
| Engagement Value | Currency | No |

### 4.6 Contact Attempt Log

| Field | Type |
|---|---|
| Attempt Number | Integer (1-7) |
| Timestamp | Datetime |
| Method | Enum (AI Call, Human Call, SMS, Email, WhatsApp) |
| Outcome | Enum (Connected, Voicemail, No Answer, Delivered, Failed) |
| Duration | Integer (seconds, calls only) |
| Agent | Reference or "AI" |
| Notes | Text |

### 4.7 Follow-Up Log

| Field | Type |
|---|---|
| Sequence | Enum (Post-Consult, Post-Booking-Fail, No-Show-Recovery, Retainer, Nurture) |
| Step Number | Integer |
| Scheduled At / Sent At | Datetime |
| Channel | Enum (SMS, Email, Call) |
| Content Summary | Text |
| Response | Enum (No Response, Replied, Booked, Opted Out) |

### 4.8 Consent and Compliance

| Field | Type | Required |
|---|---|---|
| Transactional Consent | Boolean | Yes (implied by inquiry) |
| Marketing Consent | Boolean | Yes (default: false) |
| Marketing Consent Granted At | Timestamp | When applicable |
| Marketing Consent Method | Enum (Form checkbox, Verbal logged, SMS opt-in) | When applicable |
| Suppression Status | Boolean | Yes (default: false) |
| Suppression Reason | Enum (Opt-out, CASL complaint, Manual) | When suppressed |
| Suppression Applied At | Timestamp | When suppressed |
| Do Not Call | Boolean | Yes (default: false) |

---

## 5. Rules Engine

### R1: Speed-to-Lead

- R1.1: Acknowledgment within 60 seconds of inquiry
- R1.2: First AI call within 5 minutes of inquiry
- R1.3: If AI unavailable, lead in operator queue within 5 min with "SPEED ALERT"
- R1.4: Speed measured from inquiry timestamp to first successful outbound contact

### R2: Contact Sequence

- R2.1: Maximum 7 attempts before UNREACHABLE
- R2.2: Timing per Flow 3 sequence
- R2.3: No calls before 9 AM or after 8 PM prospect time zone. SMS until 9 PM.
- R2.4: Max 1 SMS per calendar day (excluding transactional)
- R2.5: Prospect requests callback time: schedule it, pause sequence

### R3: Escalation Triggers

- R3.1: Eligibility question -> redirect to consultant, flag for human
- R3.2: Deportation/removal/inadmissibility mention -> immediate human routing
- R3.3: Minor involved -> human routing
- R3.4: Explicit human request -> immediate transfer, no resistance
- R3.5: AI confidence below threshold (default 60%) -> human queue
- R3.6: Complexity flag -> held for senior review, no auto-advance
- R3.7: Emotional distress -> empathy, human callback, stop script

### R4: No-Show Handling

- R4.1: No-show detected at appointment + 5 min
- R4.2: Recovery initiates immediately (Flow 7)
- R4.3: Max 6 recovery attempts over 7 business days
- R4.4: Reschedule count >= 3: operator review before confirming
- R4.5: Messages must be empathetic, never punitive. No fees in v1.

### R5: Consent and Suppression

- R5.1: Inquiry = implied transactional consent
- R5.2: Marketing requires explicit consent. Default: not granted.
- R5.3: "STOP" reply: suppression within 5 minutes
- R5.4: Suppression stops: SMS, email marketing, AI calls, follow-up. Does NOT stop: active appointment reminders (transactional).
- R5.5: Suppression logged with timestamp, reason, method. Irreversible without re-consent.
- R5.6: CASL: firm ID, contact info, unsubscribe in every commercial message.

### R6: Follow-Up Windows

- R6.1: "Proceed" retainer: sent within 1h, follow-up days 1, 2, 5, 10, 14
- R6.2: "Thinking" post-consult: summary day 0, then days 2, 5, 7, 14 -> NURTURE
- R6.3: Booking follow-up: link immediately, then days 1, 3, 5, 10, 21 -> NURTURE after 14d
- R6.4: Nurture: monthly email (if marketing consent), quarterly SMS
- R6.5: Re-engagement from NURTURE: re-enter pipeline, retain previous data

### R7: Retainer Follow-Up

- R7.1: Retainer sent within 1 hour of "proceed"
- R7.2: Must be digitally signable
- R7.3: Payment must be digitally collectible
- R7.4: Follow-up days 1, 2, 5, 10. Day 10 = human call from consultant.
- R7.5: Unsigned after 14 days -> NURTURE

---

## 6. Dashboards and Reports

### 6.1 Firm Owner Dashboard (Daily, < 5 min)

| Information | Update |
|---|---|
| Pipeline snapshot: count per state | Real-time |
| Today: new inquiries, consultations, retainers signed | Real-time |
| Speed-to-contact: median trailing 7 days | Daily |
| Conversion funnel: trailing 30 days | Daily |
| Stuck leads: name, state, days in state | Real-time |
| Consultation schedule: today + tomorrow | Real-time |

### 6.2 Daily Briefing (Push, 8 AM)

```
[Firm] Daily Pipeline -- [Date]
New Inquiries Yesterday: [X]
First Contact Made: [X] (median: [X] min)
Consultations Completed: [X]
Retainers Signed: [X] ($[total])
Pipeline: [X] active | Stuck: [X] need attention
Today's Consultations: [X]
```

### 6.3 Monthly Review Report

| Information |
|---|
| Source-to-revenue: per source -- inquiries, contacted, booked, retained, revenue, cost, ROI |
| Conversion rates by stage (month-over-month) |
| Average time to retained (by program type) |
| Lost lead analysis: count by reason, top 3 |
| Nurture pool: total, re-engaged this month |

### 6.4 Intake Operator View (Continuous)

| Information |
|---|
| My queue: sorted by priority (urgent, speed-alert, manual follow-up, partial assessments) |
| Lead card: name, phone, state, readiness data, interaction history, last touch, days since |
| Today's tasks: callbacks, manual bookings, flagged follow-ups |
| My stats: contacts today, bookings today, queue size |

### 6.5 Consultant View (Before each consultation)

| Information |
|---|
| Today's consultations: name, time, program interest, priority, prep status |
| Consultation briefing: full structured document |
| Pending outcomes: consultations done but unrecorded |
| Retainer pipeline: leads with outcome=proceed, retainer pending, days since sent |

---

## 7. Manual vs Automated

### Manual in V1

| Activity | Who |
|---|---|
| GHL sub-account setup (pipeline, forms, calendars, workflows) | NeuronX onboarding |
| Complex lead review (R6 flags) | Senior consultant |
| Consultation delivery | Consultant |
| Outcome recording | Consultant |
| Retainer agreement creation | Firm |
| Payment collection | Firm |
| Pricing decisions | Firm owner |
| AI call script initial configuration | NeuronX + firm |
| Onboarding new firms | NeuronX team |
| Source-to-revenue cost input | Firm owner (monthly) |

### GHL Native Workflows

| Activity | GHL Feature |
|---|---|
| Instant acknowledgment | Workflow: Form Submitted -> Send SMS/Email |
| Lead record creation + source tag | Workflow: Form Submitted -> Create Contact + Tag |
| Booking confirmation | Workflow: Appointment Booked -> Send SMS/Email |
| Reminders (48h, 24h, 2h) | Workflow: Appointment Status -> Wait -> Send |
| No-show detection trigger | Workflow: Appointment No-Show |
| Pipeline stage movement | Workflow: triggers -> Update Opportunity |
| Round-robin assignment | Workflow: Contact Created -> Round Robin |
| Follow-up sequences | Workflow: Tag Added -> Wait -> Send |
| Stale lead detection | Workflow: Stale Opportunities |
| Booking link delivery | Workflow: Tag Added -> Send SMS with link |
| DND/opt-out handling | GHL built-in compliance |

### NeuronX Orchestration

| Activity |
|---|
| AI outbound call orchestration (webhook -> voice provider -> callback -> GHL API) |
| Call outcome interpretation and CRM update |
| Readiness scoring engine |
| Consultation prep assembly and delivery |
| Operator work queue prioritization |
| Conversion funnel analytics |
| Daily briefing generation |
| Stuck-lead detection with context |
| Trust boundary enforcement |
| Consent/suppression management |

### Deferred

| Activity | When |
|---|---|
| Operator scorecards | v1.5 |
| Lead source ROI (automated) | v1.5 |
| AI context memory | v1.5 |
| Multi-language | v2 |
| Case management handoff | v2 |
| Self-serve onboarding | v2+ |
| WhatsApp automation | v1.5 |
| Consultant performance comparison | v1.5 |

---

## 8. Failure Modes

### System Failures

| Mode | Detection | Response |
|---|---|---|
| Voice AI provider outage | API fail/timeout | All leads to operator queue with SPEED ALERT. GHL still sends ack. Alert owner. |
| GHL API unavailable | API calls fail | Queue operations, retry with backoff. >30 min: alert owner. Operators work in GHL directly. |
| NeuronX orchestrator down | Health check fail | GHL continues (acks, reminders, booking). AI calling stops. Prep not generated. Alert owner. |
| SMS delivery failure | Status = failed | Fallback to email. Persistent: flag for phone call. |
| Email delivery failure | Bounce | Fallback to SMS. Briefings: CRM note + SMS alert. |

### Operational Failures

| Mode | Detection | Response |
|---|---|---|
| Consultant does not record outcome | 1h past consultation | Reminder at 1h. Escalation to owner at 4h. |
| Lead stuck beyond threshold | Stuck-lead detection | Alert in dashboard. Owner/operator must act. |
| Booking capacity full | No slots within 7 days | Alert owner. Firm adds slots or consultant. |
| High no-show rate (>25% 14d) | Metric | Alert owner. Adjust reminders, timing, confirmation. |
| Low consult-to-retained (<20% 30d) | Metric | Alert owner. Review consultation, readiness, pricing. |

### Trust Boundary Failures

| Mode | Detection | Response |
|---|---|---|
| AI provides eligibility assessment | Transcript/log review | Investigate. Update prompt constraints. Contact affected prospect. Log as compliance incident. |
| AI fails to escalate | Trigger met, no escalation | Root cause. Fix rule/threshold. Human outreach to affected prospect. |
| AI impersonates human | Transcript/complaint | Update script. Implement disclosure policy. |
