# VMC Email & SMS Template Registry

**Location**: FlRL82M0D6nclmKT7eXH (VMC Sub-Account)
**Last Updated**: 2026-03-30
**Total**: 11 production templates + 3 test (pending delete)

---

## Block 1 — Core Workflow Templates (Created 2026-03-23)

| # | GHL Name | ID | Trigger | Workflow |
|---|----------|----|---------|----------|
| 1 | VMC-inquiry-received | 69c131e926a76b29f946fa4b | Form submission | WF-01 |
| 2 | VMC-consultation-confirmed | 69c1325926a76b2c5b46fe5d | Appointment booked | WF-05 |
| 3 | VMC-consultation-reminder | 69c13298723a79284163f96c | 24hr before appointment | WF-06 |
| 4 | VMC-noshow-recovery | 69c132f7c3143084391c06ef | No-show detected | WF-07 |
| 5 | VMC-retainer-proposal | 69c13337088cc77b462ec407 | Consultation outcome=proceed | WF-09 |
| 6 | VMC-pipeda-acknowledgement | 69c133735c49a40a952e4985 | Form submission (consent) | WF-13 |
| 7 | VMC-monthly-nurture-base | 69c133a626a76b11de470b8d | Monthly drip sequence | WF-10 |

## Block 2B — Advanced Templates (Created 2026-03-30)

| # | GHL Name | ID | Subject Line | From | Trigger |
|---|----------|----|-------------|------|---------|
| 2.10 | VMC-complex-case-alert | 69ca6ee3f608ce36288d16d2 | Complex Case Flagged — {{contact.full_name}} | intake@neuronx.co | nx:human_escalation tag |
| 2.11 | VMC-pipeda-deletion-confirmation | 69ca6ee5874f3b25f8baab99 | Your Data Has Been Deleted — VMC | rcic@neuronx.co | PIPEDA deletion request |
| 2.12 | VMC-retainer-followup-7day | 69ca6ee6b3bc887b18efaaf3 | Following Up on Your Immigration Consultation | rcic@neuronx.co | 7 days after nx:retainer:sent |
| 2.13 | VMC-winback-nurture-30day | 69ca6ee7b3bc8814acefab0b | Still Thinking About Your Immigration Plans? | rcic@neuronx.co | 30-day re-engagement |

## Block 2B — SMS Variants (Workflow-Inline, No GHL Template ID)

| Variant | Tag Trigger | Content File |
|---------|-------------|-------------|
| ready_standard | nx:assessment:complete | templates/2.9-assessment-sms-variants.json |
| ready_urgent | nx:assessment:complete + nx:urgent | templates/2.9-assessment-sms-variants.json |
| ready_complex | nx:human_escalation | templates/2.9-assessment-sms-variants.json |
| not_ready | nx:not_ready | templates/2.9-assessment-sms-variants.json |
| disqualified | nx:disqualified | templates/2.9-assessment-sms-variants.json |

## HTML Body Files (For Email Builder Import)

| Template | HTML File |
|----------|-----------|
| 2.10 Complex Case Alert | templates/2.10-complex-case-alert.html |
| 2.11 PIPEDA Deletion | templates/2.11-pipeda-deletion-confirmation.html |
| 2.12 Retainer Follow-up | templates/2.12-retainer-followup-7day.html |
| 2.13 Win-Back Nurture | templates/2.13-winback-nurture-30day.html |

## Cleanup Needed (Test Templates — Delete in GHL UI)

| Name | ID |
|------|----|
| test-delete-me | 69ca6e1a22c1bcaf9c0df92c |
| temp-html-test | 69ca6e4f08db5438f0802fe1 |
| New Template | 69ca6e723a4ac3815593c2fe |
