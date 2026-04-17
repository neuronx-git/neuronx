# Email Template → Workflow Mapping

Generated: 2026-04-17T12:27:34.382155Z

## Proposed email assignments for each workflow

Each workflow below should use the specified premium email template.

| # | Template | Workflow | When it fires |
|---|---|---|---|
| ✅ | `VMC-01-inquiry-received` | WF-01 — Instant Lead Capture | Welcome after form submit |
| ✅ | `VMC-02-outreach-attempt` | WF-02 — Contact Attempt Sequence | Email after AI couldn't reach |
| ✅ | `VMC-03-invite-booking` | WF-04 — Readiness Complete → Invite Booking | Post-AI call invite to book |
| ✅ | `VMC-04-consultation-confirmed` | WF-05 — Appointment Booked Reminders | Booking confirmation |
| ✅ | `VMC-05-consultation-reminder` | WF-05 — Appointment Booked Reminders | Day-before reminder |
| ✅ | `VMC-06-noshow-recovery` | WF-06 — No-Show Recovery | Post no-show outreach |
| ✅ | `VMC-07-retainer-proposal` | WF-09 — Retainer Follow-Up | Proposal sent |
| ✅ | `VMC-08-retainer-followup` | WF-09/WF-10 — Retainer/Post-Consult Follow-Up | Follow-up nudge |
| ✅ | `VMC-09-score-medium-handler` | WF-12 — Score Med Handler | Medium lead → nurture |
| ✅ | `VMC-10-monthly-nurture` | WF-11 — Nurture Campaign Monthly | Monthly updates |
| ✅ | `VMC-11-winback-nurture` | WF-11 — Nurture Campaign Monthly | Win-back |
| ✅ | `VMC-12-pipeda-ack` | WF-13 — PIPEDA Data Deletion Request | Request received |
| ✅ | `VMC-13-pipeda-deleted` | WF-13 — PIPEDA Data Deletion Request | Deletion confirmed |
| ✅ | `VMC-14-complex-case-alert` | WF-04B — AI Call Receiver [v14-STABLE] | Internal escalation |
| ✅ | `VMC-15-case-onboarding` | WF-CP-01 — Client Onboarding | Welcome to case |
| ✅ | `VMC-16-cp-docs-reminder` | WF-CP-02 — Document Collection Reminders | Docs reminder |
| ✅ | `VMC-17-cp-form-prep` | WF-CP-03 — Form Preparation | Forms being prepared |
| ✅ | `VMC-18-cp-internal-review` | WF-CP-04 — Internal Review | QA in progress |
| ✅ | `VMC-19-cp-submitted` | WF-CP-05 — IRCC Submission | Submitted confirmation |
| ✅ | `VMC-20-cp-status-update` | WF-CP-06 — Processing Status Checks | Monthly update |
| ✅ | `VMC-21-cp-rfi` | WF-CP-07 — Additional Info (RFI) | RFI alert |
| ✅ | `VMC-22-cp-decision-approved` | WF-CP-08 — Decision Received | Approved variant |
| ✅ | `VMC-23-cp-decision-refused` | WF-CP-08 — Decision Received | Refused variant |
| ✅ | `VMC-24-cp-decision-withdrawn` | WF-CP-08 — Decision Received | Withdrawn variant |
| ✅ | `VMC-25-cp-case-closed` | WF-CP-09 — Case Closure | Case archive + review |
| ✅ | `VMC-26-missed-ai-call` | WF-04C — Missed Call Recovery | AI couldn't reach |

## How to link in GHL UI

1. Go to Automation → Workflows → [workflow name]
2. Find the 'Send Email' action (or add one if missing)
3. Click the email body → select 'From Template'
4. Choose the VMC-* template from the dropdown
5. Save + Publish workflow

**Note:** Workflow email actions in GHL cannot be modified via public API (v2). This requires UI clicks.