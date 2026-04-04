# GHL Pipeline #2: Case Processing

**Purpose**: Track immigration cases from retainer signed to case closed.
**Trigger**: Contact enters RETAINED state in Pipeline #1 (Intake).
**Build Method**: GHL API for fields/tags, UI for pipeline stages + workflows.

---

## Pipeline Stages

| # | Stage | Entry Trigger | Exit Trigger | Auto-Actions |
|---|-------|--------------|--------------|--------------|
| 1 | ONBOARDING | Tag `nx:retainer:signed` + `nx:payment:received` | Client completes intake questionnaire | WF-CP-01: Welcome email + doc checklist + portal access |
| 2 | DOC COLLECTION | Intake questionnaire submitted | All required docs uploaded | WF-CP-02: Weekly reminder if docs outstanding. Deadline alert at 14 days. |
| 3 | FORM PREPARATION | All docs received | RCIC completes form prep | WF-CP-03: Task created for assigned RCIC. Internal deadline set. |
| 4 | INTERNAL REVIEW | Forms prepared | Senior RCIC approves | WF-CP-04: Notify senior RCIC. QC checklist auto-generated. |
| 5 | SUBMITTED TO IRCC | Senior approves | Receipt number entered | WF-CP-05: Log date, notify client "Application submitted", set 30-day check-in. |
| 6 | PROCESSING | Receipt number entered | IRCC decision or RFI | WF-CP-06: Monthly status check task. Client update every 30 days. |
| 7 | ADDITIONAL INFO | IRCC requests more docs | Additional docs submitted | WF-CP-07: Urgent alert to RCIC + client. 15-day deadline. |
| 8 | DECISION RECEIVED | IRCC issues decision | RCIC reviews + communicates | WF-CP-08: Notify RCIC immediately. Schedule client call. |
| 9 | CASE CLOSED | Client notified of outcome | Final docs delivered | WF-CP-09: Satisfaction survey. Review request. Archive case. |

---

## Custom Fields (Case-Specific)

Create via GHL API: `POST /locations/{id}/customFields`

| Field Key | Label | Type | Options |
|-----------|-------|------|---------|
| `case_id` | Case ID | TEXT | — |
| `case_program_type` | Case Program Type | SINGLE_OPTIONS | Express Entry, Spousal Sponsorship, Work Permit, Study Permit, LMIA, PR Renewal, Citizenship, Visitor Visa, Other |
| `case_assigned_rcic` | Assigned RCIC | TEXT | — |
| `case_assigned_at` | Case Assigned Date | DATE | — |
| `ircc_receipt_number` | IRCC Receipt Number | TEXT | — |
| `ircc_submission_date` | IRCC Submission Date | DATE | — |
| `ircc_program_stream` | IRCC Program Stream | TEXT | — |
| `case_deadline_date` | Next Deadline | DATE | — |
| `case_deadline_type` | Deadline Type | SINGLE_OPTIONS | Doc Collection, Form Prep, IRCC Response, Client Action, Internal Review |
| `docs_outstanding` | Outstanding Documents | LARGE_TEXT | — |
| `docs_received_count` | Docs Received Count | NUMERICAL | — |
| `docs_required_count` | Docs Required Count | NUMERICAL | — |
| `case_status_notes` | Status Notes | LARGE_TEXT | — |
| `case_complexity` | Case Complexity | SINGLE_OPTIONS | Standard, Complex, High-Priority, Expedited |
| `ircc_decision` | IRCC Decision | SINGLE_OPTIONS | Pending, Approved, Refused, Withdrawn, Returned |
| `ircc_decision_date` | IRCC Decision Date | DATE | — |
| `case_closed_date` | Case Closed Date | DATE | — |
| `case_close_reason` | Close Reason | SINGLE_OPTIONS | Approved, Refused, Client Withdrew, Refund, Other |
| `client_satisfaction` | Client Satisfaction | SINGLE_OPTIONS | Very Satisfied, Satisfied, Neutral, Dissatisfied |
| `retainer_value` | Retainer Value | MONETORY | — |

---

## Tags (Case Processing)

| Tag | Added By | Purpose |
|-----|----------|---------|
| `nx:case:onboarding` | WF-CP-01 | Client in onboarding |
| `nx:case:docs_pending` | WF-CP-02 | Waiting for client documents |
| `nx:case:docs_complete` | WF-CP-02 | All docs received |
| `nx:case:form_prep` | WF-CP-03 | RCIC preparing forms |
| `nx:case:under_review` | WF-CP-04 | Senior RCIC reviewing |
| `nx:case:submitted` | WF-CP-05 | Filed with IRCC |
| `nx:case:processing` | WF-CP-06 | IRCC processing |
| `nx:case:rfi` | WF-CP-07 | IRCC requested additional info |
| `nx:case:decision` | WF-CP-08 | Decision received |
| `nx:case:closed` | WF-CP-09 | Case closed |
| `nx:case:approved` | WF-CP-08 | IRCC approved |
| `nx:case:refused` | WF-CP-08 | IRCC refused |
| `nx:case:overdue` | WF-CP-02/03 | Deadline passed without action |

---

## Workflow Specifications (WF-CP-01 through WF-CP-09)

### WF-CP-01: Client Onboarding
**Trigger**: Tag added `nx:retainer:signed` AND `nx:payment:received`
**Actions**:
1. Add tag `nx:case:onboarding`
2. Create opportunity in Case Processing pipeline → ONBOARDING stage
3. Send email: "Welcome to [Firm] — Your Case Has Begun"
   - Personalized doc checklist based on `case_program_type`
   - Client portal login instructions
   - Timeline expectations
4. SMS: "Welcome aboard, {{name}}! Check your email for your document checklist and portal access."
5. Create task: "Assign RCIC to case — {{name}} ({{case_program_type}})"
6. Set `case_deadline_date` = today + 14 days (doc collection deadline)

### WF-CP-02: Document Collection Reminders
**Trigger**: Tag added `nx:case:docs_pending`
**Actions**:
1. Wait 7 days → If `docs_received_count` < `docs_required_count`:
   - Email: "Friendly reminder — we're still waiting for {{docs_outstanding}}"
2. Wait 14 days → If still incomplete:
   - SMS: "Hi {{name}}, your documents are due. Please upload via your portal or reply here."
   - Add tag `nx:case:overdue`
   - Create task: "Follow up on overdue docs — {{name}}"
3. When `docs_received_count` >= `docs_required_count`:
   - Remove tag `nx:case:docs_pending`
   - Add tag `nx:case:docs_complete`
   - Move to FORM PREPARATION stage
   - Notify RCIC: "All documents received for {{name}} — ready for form prep"

### WF-CP-03: Form Preparation
**Trigger**: Tag added `nx:case:docs_complete`
**Actions**:
1. Add tag `nx:case:form_prep`
2. Create task for `case_assigned_rcic`: "Prepare IRCC forms — {{name}} ({{case_program_type}})"
3. Set internal deadline: `case_deadline_date` = today + 7 days
4. When task completed:
   - Move to INTERNAL REVIEW stage
   - Add tag `nx:case:under_review`

### WF-CP-04: Internal Review (QC)
**Trigger**: Tag added `nx:case:under_review`
**Actions**:
1. Create task for senior RCIC: "QC Review — {{name}} ({{case_program_type}})"
2. Email RCIC: QC checklist (completeness, accuracy, compliance)
3. When approved:
   - Move to SUBMITTED TO IRCC stage
   - Notify preparing RCIC: "QC approved — ready to submit"

### WF-CP-05: IRCC Submission
**Trigger**: Custom field `ircc_receipt_number` is set (non-empty)
**Actions**:
1. Add tag `nx:case:submitted`
2. Set `ircc_submission_date` = today
3. Send client email: "Great news — your application has been submitted to IRCC"
   - Include receipt number
   - Estimated processing time (generic, no promises)
   - "We'll monitor your case and update you regularly"
4. SMS: "{{name}}, your immigration application is submitted! Receipt: {{ircc_receipt_number}}. We'll keep you updated."
5. Set `case_deadline_date` = today + 30 days (first check-in)

### WF-CP-06: Processing Status Checks
**Trigger**: Tag `nx:case:processing` + recurring (every 30 days)
**Actions**:
1. Create task for RCIC: "Check IRCC status — {{name}} ({{ircc_receipt_number}})"
2. After task completed with status update:
   - Send client email: monthly status update
   - Update `case_status_notes`
3. Reset `case_deadline_date` = today + 30 days

### WF-CP-07: Additional Information Request (RFI)
**Trigger**: Tag added `nx:case:rfi`
**Actions**:
1. URGENT: Email RCIC immediately: "IRCC has requested additional information for {{name}}"
2. Email client: "Action Required — IRCC needs additional documents"
   - What's needed (from `case_status_notes`)
   - Deadline (from `case_deadline_date`)
   - How to upload
3. SMS: "URGENT: {{name}}, IRCC needs additional documents. Check your email for details."
4. Set `case_deadline_date` = today + 15 days
5. Follow WF-CP-02 reminder logic for doc collection

### WF-CP-08: Decision Received
**Trigger**: Custom field `ircc_decision` changed from "Pending"
**Actions**:
- **If Approved**:
  1. Add tag `nx:case:approved`
  2. Create task: "Schedule congratulations call with {{name}}"
  3. Email client: "Congratulations — Your Application Has Been Approved!"
  4. Move to CASE CLOSED
- **If Refused**:
  1. Add tag `nx:case:refused`
  2. Create task: "Schedule review call with {{name}} — discuss options"
  3. Email client: "Important Update About Your Application"
  4. Do NOT auto-close — RCIC must discuss options first

### WF-CP-09: Case Closure
**Trigger**: Move to CASE CLOSED stage
**Actions**:
1. Add tag `nx:case:closed`
2. Set `case_closed_date` = today
3. Send email: satisfaction survey link
4. Wait 7 days → Send email: "Would you leave us a review?"
5. Wait 30 days → Send email: referral request + "Do you have friends/family who need help?"
6. Archive case (remove from active pipeline view)

---

## Implementation Notes

**API-capable**: Custom fields, tags, contact updates
**UI-only**: Pipeline creation (stages), workflow builder, Custom Objects setup
**NeuronX API additions needed**:
- `POST /webhooks/ghl` handler for case stage changes
- `POST /documents/checklist` — generate program-specific doc checklist
- `GET /analytics/cases` — case processing metrics (time-per-stage, completion rate)
