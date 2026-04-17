# NeuronX Email Templates

26 production-grade transactional email templates covering every workflow touchpoint in the customer journey.

## Source

Built on **Postmark Transactional Email Templates** (MIT licensed):
- https://github.com/ActiveCampaign/postmark-templates
- 5k+ GitHub stars, used across millions of production emails
- Battle-tested across 70+ email clients (Outlook, Gmail, Apple Mail, etc.)

## What changed from Postmark base

Only branding + content — structure is unchanged (preserves client-compatibility):
- Brand color: `#3869D4` (Postmark blue) → `#E8380D` (VMC red)
- Product name: placeholder → "Visa Master Canada"
- Footer: contact details + RCIC compliance note

## Files

| File | Purpose |
|---|---|
| `postmark-base.html` | Postmark "welcome" template (info/notification style) |
| `postmark-action-base.html` | Postmark "password-reset" template (CTA button style) |
| `generate.py` | Renders all 26 templates with VMC content |
| `upload.py` | Uploads rendered templates to GHL VMC via PIT |
| `manifest.json` | Generated list of all templates with subjects + metadata |
| `rendered/` | Generated HTML files (26 total) |

## Template Index

### Intake Funnel (14)
| # | Template | Workflow |
|---|---|---|
| 01 | inquiry-received | WF-01 Instant Lead Capture |
| 02 | outreach-attempt | WF-02 Contact Attempt Sequence |
| 03 | invite-booking | WF-04 Readiness Complete → Book |
| 04 | consultation-confirmed | WF-05 Appointment Reminders |
| 05 | consultation-reminder | WF-05 Appointment Reminders |
| 06 | noshow-recovery | WF-06 No-Show Recovery |
| 07 | retainer-proposal | WF-09 Retainer Follow-Up |
| 08 | retainer-followup | WF-09 / WF-10 |
| 09 | score-medium-handler | WF-12 Score Med Handler |
| 10 | monthly-nurture | WF-11 Nurture Campaign |
| 11 | winback-nurture | WF-11 Nurture Campaign |
| 12 | pipeda-ack | WF-13 PIPEDA Deletion |
| 13 | pipeda-deleted | WF-13 PIPEDA Deletion |
| 14 | complex-case-alert | Internal (WF-04B) |

### Case Processing (12)
| # | Template | Workflow |
|---|---|---|
| 15 | case-onboarding | WF-CP-01 Client Onboarding |
| 16 | cp-docs-reminder | WF-CP-02 Document Collection |
| 17 | cp-form-prep | WF-CP-03 Form Preparation |
| 18 | cp-internal-review | WF-CP-04 Internal Review |
| 19 | cp-submitted | WF-CP-05 IRCC Submission |
| 20 | cp-status-update | WF-CP-06 Processing Checks |
| 21 | cp-rfi | WF-CP-07 Additional Info |
| 22 | cp-decision-approved | WF-CP-08 (approved variant) |
| 23 | cp-decision-refused | WF-CP-08 (refused variant) |
| 24 | cp-decision-withdrawn | WF-CP-08 (withdrawn variant) |
| 25 | cp-case-closed | WF-CP-09 Case Closure |
| 26 | missed-ai-call | WF-04C Missed Call Recovery |

## Regenerate & Upload

```bash
# From project root
cd neuronx-api

# 1. Regenerate HTML
python3 email-templates/generate.py

# 2. Upload to GHL VMC (requires tools/ghl-lab/.pit-tokens.json)
python3 email-templates/upload.py
```

## GHL Merge Tags Used

All templates use standard GHL merge tags:
- `{{contact.first_name}}`, `{{contact.last_name}}`, `{{contact.full_name}}`
- `{{contact.email}}`, `{{contact.phone}}`, `{{contact.id}}`
- `{{contact.ai_program_interest}}`, `{{contact.ai_current_location}}`
- `{{contact.ai_timeline_urgency}}`, `{{contact.ai_readiness_score}}`
- `{{contact.case_id}}`, `{{contact.case_program_type}}`, `{{contact.case_assigned_rcic}}`
- `{{contact.ircc_receipt_number}}`, `{{contact.ircc_decision_date}}`, `{{contact.ircc_decision}}`
- `{{appointment.start_date}}`, `{{appointment.start_time}}`, `{{appointment.timezone}}`
- `{{appointment.meeting_url}}`, `{{appointment.reschedule_url}}`, `{{appointment.ics_url}}`
- `{{message.unsubscribe_url}}`, `{{location.id}}`

For template-specific tags (case-related, RFI, decision variants), see each HTML file.
