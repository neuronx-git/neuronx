# VMC Workflow Trigger → Action Reference (Complete)

**Generated**: 2026-03-30 (API audit + documentation review)
**Location**: FlRL82M0D6nclmKT7eXH (VMC Sub-Account)
**Pipeline**: NeuronX — Immigration Intake (`Dtj9nQVd3QjL7bAb3Aiw`)
**Total Workflows**: 15 (all published)
**Total nx: Tags**: 64
**Pipeline Stages**: 10

---

## Pipeline Stages

| # | Stage | ID |
|---|-------|----|
| 1 | NEW | b319c338-215f-44fe-a0da-0c0c7a1f84a4 |
| 2 | CONTACTING | f08d0408-dc0c-4809-ae88-0b5631cc22fc |
| 3 | UNREACHABLE | d69ffbcd-b510-4ff7-bf71-dccc33cc7cb9 |
| 4 | CONSULT READY | 231d5e26-2ea7-43a9-b91c-dd0b21971983 |
| 5 | BOOKED | 07348d98-10a3-400d-b2de-a770dd9fa8c6 |
| 6 | CONSULT COMPLETED | 45df0bc1-646b-4a02-961b-74ba35d173a8 |
| 7 | PROPOSAL SENT | 3f5139bc-b9bb-4080-8754-caab73399ac2 |
| 8 | RETAINED | 618ef749-6c96-4eca-b144-fe87064e549c |
| 9 | LOST | ed164220-700e-42ef-a89d-1b198ef1c229 |
| 10 | NURTURE | b4fc6746-1049-47a4-95e1-24426e3bbaa1 |

---

## Workflow Summary Table

| WF | Name | Trigger | Listens For | Tags Added | Stage Change |
|----|------|---------|-------------|------------|--------------|
| 01 | New Inquiry Acknowledge | Form Submitted | Immigration Inquiry form | `nx:new_inquiry`, `nx:contacting:start` | → NEW → CONTACTING |
| 02 | Contact Attempt Sequence | Tag Added | `nx:contacting:start` | `nx:contacting:attempt1-6`, `nx:nurture:enter` | → UNREACHABLE (if all fail) |
| 03 | Mark Contacted | Tag Added | `nx:contacted` | `nx:assessment:required` | (none) |
| 04 | Readiness Ready → Booking | Tag Added | `nx:score:high` | `nx:consult_ready`, `nx:booking:invited` | → CONSULT READY |
| 04B | VAPI Data Mapper [v14] | Inbound Webhook | VAPI end-of-call | `nx:score:high/med/low`, `nx:contacted`, `nx:human_escalation` | (routing only) |
| 04C | Missed Call Recovery | Property Changed | Voicemail/No Answer | `nx:missed_call` | (none) |
| 05 | Appointment Booked | Appointment Event | Calendar booking | `nx:booking:confirmed` | → BOOKED |
| 06 | No-Show Recovery | Tag Added | `nx:appointment:noshow` | (none) | → NURTURE (if recovery fails) |
| 07 | Consultation Outcome | Tag Added | `nx:consult:done` | (none) | → CONSULT COMPLETED |
| 08 | Outcome Routing | Tag Added | `nx:human_escalation` | `nx:human:pending` | (manual hold) |
| 09 | Retainer Follow-Up | Tag Added | `nx:retainer:sent` | (none) | → NURTURE (if unsigned 14d) |
| 10 | Post-Consult Follow-Up | Tag Added | `nx:retainer:signed` | (none) | → RETAINED (terminal) |
| 11 | Nurture Campaign Monthly | Tag Added | `nx:score:low` | `nx:nurture:enter` | → NURTURE |
| 12 | Score Med Handler | Tag Added | `nx:score:med` | (none) | CONTACTING (hold) |
| 13 | PIPEDA Data Deletion | Tag Added | `nx:pipeda:deletion_requested` | (none) | (compliance only) |

---

## Detailed Workflow Specifications

### WF-01: New Inquiry → Acknowledge + Start Contacting
- **ID**: `99ce0aa7-2491-4c91-9477-22969798e2b7`
- **Trigger**: Form Submitted (Immigration Inquiry V1)
- **Actions**: Create contact → Set lead_source + UTM fields → Add `nx:new_inquiry` → Create opportunity (NEW stage) → Send ack SMS + email → Add `nx:contacting:start` → Move to CONTACTING
- **Template**: VMC-inquiry-received (`69c131e926a76b29f946fa4b`)
- **Fields Set**: `lead_source`, `utm_source`, `utm_medium`, `utm_campaign`

### WF-02: Contact Attempt Sequence (7-Step)
- **ID**: `43ecd109-6595-4f51-a0e0-e2421b3f8131`
- **Trigger**: Tag `nx:contacting:start`
- **Actions**: 7 attempts over 10 business days (VAPI call → SMS → call → SMS → email → SMS → final SMS) → If all fail: Move to UNREACHABLE, add `nx:nurture:enter`
- **Webhook**: VAPI call orchestration (POST https://api.vapi.ai/call)

### WF-03: Mark Contacted → Require Assessment
- **ID**: `fb1215b4-8343-4ccb-b874-12cfb616afea`
- **Trigger**: Tag `nx:contacted` (set by WF-04B)
- **Actions**: Add `nx:assessment:required` → Create task "Complete readiness assessment (R1-R5)"

### WF-04: Readiness Complete → Invite Booking
- **ID**: `838f7c38-3534-4d3b-9d4c-40b11f4a6772`
- **Trigger**: Tag `nx:score:high` (set by WF-04B, score >= 70)
- **Actions**: Move to CONSULT READY → Add `nx:consult_ready` → Send booking link SMS + email → Add `nx:booking:invited`

### WF-04B: VAPI Data Mapper → Lead Score Router (CRITICAL HUB)
- **ID**: `cc52cbeb-8d4d-4bdc-b43d-fdb3c0bb9f1f`
- **Trigger**: Inbound Webhook (VAPI end-of-call JSON)
- **Actions**: Parse VAPI data → Map R1-R5 fields → Score routing (>=70 → `nx:score:high`, 40-69 → `nx:score:med`, <40 → `nx:score:low`) → Add `nx:contacted` → If complexity flags: add `nx:human_escalation`
- **Fields Set**: `program_interest`, `current_location`, `timeline_urgency`, `prior_applications`, `budget_awareness`, `readiness_outcome`, `assessment_completed_at`, `assessed_by`

### WF-04C: Missed Call Recovery
- **ID**: `5a1b58a3-a9c8-48b0-aa64-c24d8cd45185`
- **Trigger**: Contact Property Changed (Voicemail/No Answer)
- **Actions**: Wait 5min → Send recovery SMS with booking link → Add `nx:missed_call`

### WF-05: Appointment Booked → Confirmation + Reminders
- **ID**: `9af911d1-b025-45d4-a083-f62364752318`
- **Trigger**: Customer Booked Appointment (any VMC calendar)
- **Actions**: Move to BOOKED → Add `nx:booking:confirmed` → Send confirmation SMS+email → Reminders at 48h, 24h, 2h before
- **Templates**: VMC-consultation-confirmed (`69c1325926a76b2c5b46fe5d`), VMC-consultation-reminder (`69c13298723a79284163f96c`)

### WF-06: No-Show Recovery (6-Step)
- **ID**: `5d0c1920-bf7b-45c2-9cf9-e40466e3e0aa`
- **Trigger**: Tag `nx:appointment:noshow` (manual)
- **Actions**: 6 recovery attempts over 7 days (SMS → call task → SMS → SMS → email → final SMS) → If all fail: Move to NURTURE
- **Template**: VMC-noshow-recovery (`69c132f7c3143084391c06ef`)

### WF-07: Consultation Completed → Outcome Capture
- **ID**: `83177830-a2d2-4385-8efa-2c9b882d39b6`
- **Trigger**: Tag `nx:consult:done` (manual by consultant)
- **Actions**: Move to CONSULT COMPLETED → Send thank you SMS+email → Create task "Record outcome" → 1h reminder → 4h escalation to firm owner

### WF-08: Outcome Routing (Human Escalation)
- **ID**: `7c1b7487-f5c7-45e5-91d5-9052489bbbeb`
- **Trigger**: Tag `nx:human_escalation` (set by WF-04B)
- **Actions**: Send alert email to RCIC → Create task "Review complex case" → Add `nx:human:pending` → HOLD (no auto-advance)
- **Template**: VMC-complex-case-alert (`69ca6ee3f608ce36288d16d2`)

### WF-09: Retainer Follow-Up (14-Day Sequence)
- **ID**: `93b39b76-8db0-45f1-b48b-b36ddd8ddcbf`
- **Trigger**: Tag `nx:retainer:sent` (manual)
- **Actions**: Day 0 retainer email → Day 1 SMS → Day 2 email → Day 5 email → Day 10 call task → Day 14 final email → Move to NURTURE if unsigned
- **Templates**: VMC-retainer-proposal (`69c13337088cc77b462ec407`), VMC-retainer-followup-7day (`69ca6ee6b3bc887b18efaaf3`)
- **Fields Set**: `retainer_sent`, `retainer_sent_at`

### WF-10: Retainer Signed → Welcome (Terminal)
- **ID**: `25046474-a6f3-4235-837f-81fd3e72f56b`
- **Trigger**: Tag `nx:retainer:signed` (manual)
- **Actions**: Move to RETAINED → Send welcome SMS+email → Set `retainer_signed`, `payment_received` fields → Handoff to case management
- **Fields Set**: `retainer_signed`, `retainer_signed_at`, `payment_received`, `payment_received_at`

### WF-11: Nurture Campaign Monthly
- **ID**: `7e0a17f4-461b-4404-9eb6-656e4782d476`
- **Trigger**: Tag `nx:score:low` (set by WF-04B, score < 40)
- **Actions**: Add `nx:nurture:enter` → Branch by program (Express Entry / Spousal / Work / Study / General) → Monthly email + quarterly SMS → Re-engage if contact replies/books
- **Templates**: VMC-monthly-nurture-base (`69c133a626a76b11de470b8d`), VMC-winback-nurture-30day (`69ca6ee7b3bc8814acefab0b`)
- **NEEDS**: Task 2.14 — 8 program-specific content branches (currently general only)

### WF-12: Score Medium Handler
- **ID**: `6f01a5e0-40c5-48a9-994e-122c4a84dea4`
- **Trigger**: Tag `nx:score:med` (set by WF-04B, score 40-69)
- **Actions**: Hold in CONTACTING → Send SMS + email → Alert assigned user → Create task "Operator review — medium-fit lead"

### WF-13: PIPEDA Data Deletion
- **ID**: `823e3e74-3435-4b48-bbbf-c199a937ec15`
- **Trigger**: Tag `nx:pipeda:deletion_requested` (manual by admin)
- **Actions**: Send admin alert → Send ack email → Create deletion task → Set `suppression_reason` + `suppression_status`
- **Templates**: VMC-pipeda-acknowledgement (`69c133735c49a40a952e4985`), VMC-pipeda-deletion-confirmation (`69ca6ee5874f3b25f8baab99`)
- **NEEDS**: Task 2.15 — End-to-end test of deletion flow

---

## Tag Cross-Reference (Who Adds → Who Listens)

| Tag | Added By | Triggers |
|-----|----------|----------|
| `nx:new_inquiry` | WF-01 | — |
| `nx:contacting:start` | WF-01 | → WF-02 |
| `nx:contacting:attempt1-6` | WF-02 | — |
| `nx:contacted` | WF-04B | → WF-03 |
| `nx:assessment:required` | WF-03 | — |
| `nx:score:high` | WF-04B | → WF-04 |
| `nx:score:med` | WF-04B | → WF-12 |
| `nx:score:low` | WF-04B | → WF-11 |
| `nx:human_escalation` | WF-04B | → WF-08 |
| `nx:human:pending` | WF-08 | — |
| `nx:missed_call` | WF-04C | — |
| `nx:consult_ready` | WF-04 | — |
| `nx:booking:invited` | WF-04 | — |
| `nx:booking:confirmed` | WF-05 | — |
| `nx:appointment:noshow` | Manual | → WF-06 |
| `nx:consult:done` | Manual | → WF-07 |
| `nx:retainer:sent` | Manual | → WF-09 |
| `nx:retainer:signed` | Manual | → WF-10 |
| `nx:nurture:enter` | WF-02, WF-11 | — |
| `nx:pipeda:deletion_requested` | Manual | → WF-13 |

---

## Stage Transition Matrix

| From | To | Workflow | Condition |
|------|----|----------|-----------|
| — | NEW | WF-01 | Form submitted |
| NEW | CONTACTING | WF-01 | After acknowledgment |
| CONTACTING | UNREACHABLE | WF-02 | 7 attempts exhausted |
| CONTACTING | CONSULT READY | WF-04 | Score >= 70 |
| (any) | BOOKED | WF-05 | Appointment booked |
| BOOKED | CONSULT COMPLETED | WF-07 | Consultation done |
| BOOKED | NURTURE | WF-06 | No-show recovery exhausted |
| CONSULT COMPLETED | RETAINED | WF-10 | Retainer signed + paid |
| CONSULT COMPLETED | NURTURE | WF-09 | Unsigned after 14 days |
| (various) | NURTURE | WF-02/06/09/11 | Various failure/timeout |

---

## Remaining Work (Block 2C)

| Task | What's Needed | Can API? |
|------|---------------|----------|
| 2.14 | WF-11: Add 8 program-specific nurture branches (EE, Spousal, Work Permit, Study Permit, LMIA, PR Renewal, Citizenship, Visitor) | NO — Workflow builder UI only |
| 2.15 | WF-13: Test PIPEDA deletion (add tag → verify task + email + suppression) | PARTIAL — Can add tag via API, verify field changes |
