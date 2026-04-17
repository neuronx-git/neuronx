# Manual Build: Case Processing Pipeline + 9 WF-CP Workflows

**Time needed:** ~30 minutes
**Target:** Production VMC sub-account (`vb8iWAwoLi2uT3s5v1OW`)
**Why manual:** GHL's v2 API doesn't expose Pipeline CREATE or Workflow CRUD to any token we have (OAuth, agency PIT, location PIT all return 401 on POST /opportunities/pipelines and /workflows).

---

## Prerequisites — already done ✅
- [x] 140 custom fields (incl. case_id, case_program_type, ircc_receipt_number, ircc_decision, etc.)
- [x] 120 tags (incl. nx:case:onboarding, nx:case:docs_pending, ..., nx:decision:approved, nx:decision:refused, nx:decision:withdrawn)
- [x] 26 premium email templates (VMC-15 through VMC-26 are case-processing)
- [x] 9 team members (Rajiv, Nina, Michael, Sarah, Arjun, Emily, James, Priya, Kwame)

---

## Part 1 — First, delete 3 broken workflows (2 min)

1. Open: https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflows
2. Find each of these (they have 🚧 prefix and `draft` status):
   - 🚧 Processing - WF-10 Post-Consult Follow-Up
   - 🚧 Processing - WF-11 Nurture Campaign Monthly
   - 🚧 Processing - WF-13 PIPEDA Data Deletion Request
3. Hover over each → click ⋮ (three dots) → **Delete**

---

## Part 2 — Create "NeuronX - Case Processing" pipeline (2 min)

1. Open: https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/opportunities
2. Click **Pipelines** (top tab) → **+ Create New Pipeline**
3. **Name**: `NeuronX - Case Processing`
4. Add these 9 stages in this exact order (click "+ Add Stage" between each):

| Position | Stage Name |
|---|---|
| 0 | ONBOARDING |
| 1 | DOC COLLECTION |
| 2 | FORM PREPARATION |
| 3 | INTERNAL REVIEW |
| 4 | SUBMITTED TO IRCC |
| 5 | PROCESSING |
| 6 | ADDITIONAL INFO (RFI) |
| 7 | DECISION RECEIVED |
| 8 | CASE CLOSED |

5. Click **Save**

---

## Part 3 — Build 9 WF-CP Workflows (25 min)

### Template for all 9 workflows

For EACH workflow:
1. Go to https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflows
2. Click **+ Create Workflow** → choose **Start from Scratch** → blank
3. Name the workflow per the table below
4. **Trigger**: Click "Add New Trigger" → Select **Contact Tag** → **Add Tag** → specific tag per table
5. **Actions**: Add in sequence:
   - **Send Email** → choose template from table
   - **Create Task** → assigned to "Case Assigned RCIC" (custom field: `{{contact.case_assigned_rcic}}`)
6. Click **Save** → **Publish**

### Workflow #1: WF-CP-01 Client Onboarding

- **Name**: `WF-CP-01: Client Onboarding`
- **Trigger**: Contact Tag Added = `nx:case:onboarding`
- **Action 1**: Send Email → template **VMC-15-case-onboarding**
- **Action 2**: Wait 3 days
- **Action 3**: IF tag `nx:case:docs_pending` NOT present → Send Email **VMC-16-cp-docs-reminder**
- **Publish**

### Workflow #2: WF-CP-02 Document Collection Reminders

- **Name**: `WF-CP-02: Document Collection Reminders`
- **Trigger**: Contact Tag Added = `nx:case:docs_pending`
- **Action 1**: Wait 3 days
- **Action 2**: Send Email → **VMC-16-cp-docs-reminder**
- **Action 3**: Wait 4 days (total day 7)
- **Action 4**: IF tag `nx:case:docs_complete` NOT added → Send Email **VMC-16-cp-docs-reminder** + Create Task for Case RCIC ("Call client re: outstanding docs")
- **Action 5**: Wait 7 days (total day 14)
- **Action 6**: IF still not complete → Send Email **VMC-16-cp-docs-reminder** with URGENT subject + Create Task ("Escalate to senior RCIC")
- **Publish**

### Workflow #3: WF-CP-03 Form Preparation

- **Name**: `WF-CP-03: Form Preparation`
- **Trigger**: Contact Tag Added = `nx:case:form_prep`
- **Action 1**: Send Email → **VMC-17-cp-form-prep**
- **Action 2**: Create Task for Case RCIC: "Prepare IRCC forms for this case" (due in 7 days)
- **Publish**

### Workflow #4: WF-CP-04 Internal Review

- **Name**: `WF-CP-04: Internal Review`
- **Trigger**: Contact Tag Added = `nx:case:under_review`
- **Action 1**: Send Email → **VMC-18-cp-internal-review**
- **Action 2**: Create Task for Senior RCIC: "QA review for {{contact.case_id}}" (due in 3 days)
- **Publish**

### Workflow #5: WF-CP-05 IRCC Submission

- **Name**: `WF-CP-05: IRCC Submission`
- **Trigger**: Contact Tag Added = `nx:case:submitted`
- **Action 1**: Send Email → **VMC-19-cp-submitted**
- **Action 2**: Create Task for Ops Manager: "Confirm IRCC submission receipt number for {{contact.case_id}}" (due in 5 days)
- **Publish**

### Workflow #6: WF-CP-06 Processing Status Checks

- **Name**: `WF-CP-06: Processing Status Checks`
- **Trigger**: Contact Tag Added = `nx:case:processing`
- **Action 1**: Wait 30 days
- **Action 2**: Send Email → **VMC-20-cp-status-update**
- **Action 3**: LOOP Wait 30 days → Send Email (same) — use GHL's repeat schedule
- **Publish**

### Workflow #7: WF-CP-07 Additional Info (RFI)

- **Name**: `WF-CP-07: Additional Info (RFI)`
- **Trigger**: Contact Tag Added = `nx:case:rfi`
- **Action 1**: Send Email → **VMC-21-cp-rfi** (URGENT)
- **Action 2**: Send SMS (if enabled): "URGENT: IRCC has requested additional info on your case. Please check email."
- **Action 3**: Create Task for Case RCIC: "RFI response needed within 24h for {{contact.case_id}}" (priority: HIGH, due in 1 day)
- **Action 4**: Notify Client Success Manager (internal email)
- **Publish**

### Workflow #8: WF-CP-08 Decision Received

- **Name**: `WF-CP-08: Decision Received`
- **Trigger**: Contact Tag Added = `nx:case:decision`
- **Action 1 (Branch by tag)**:
  - IF tag `nx:decision:approved` → Send Email **VMC-22-cp-decision-approved**
  - IF tag `nx:decision:refused` → Send Email **VMC-23-cp-decision-refused**
  - IF tag `nx:decision:withdrawn` → Send Email **VMC-24-cp-decision-withdrawn**
- **Action 2**: Create Task for Case RCIC: "Final case review + next steps call" (due in 5 days)
- **Action 3 (if approved only)**: Add tag `nx:testimonial:requested`
- **Publish**

### Workflow #9: WF-CP-09 Case Closure

- **Name**: `WF-CP-09: Case Closure`
- **Trigger**: Contact Tag Added = `nx:case:closed`
- **Action 1**: Send Email → **VMC-25-cp-case-closed**
- **Action 2**: Move opportunity to "CASE CLOSED" stage in Case Processing pipeline
- **Action 3**: Create Task for CSM: "Schedule 3-month check-in" (due in 90 days)
- **Action 4 (if approved)**: Add tag `nx:pr_approved_date` + schedule citizenship reminder (3 years)
- **Publish**

---

## Part 4 — Link 26 premium email templates to existing 18 workflows (5 min)

For each workflow below, open it → find the "Send Email" action → change the email to the premium VMC-* template:

| Workflow | Existing email → Change to |
|---|---|
| WF-01 Instant Lead Capture | → `VMC-01-inquiry-received` |
| WF-02 Contact Attempt Sequence | → `VMC-02-outreach-attempt` |
| WF-04 Readiness Complete | → `VMC-03-invite-booking` |
| WF-04B AI Call Receiver | → `VMC-14-complex-case-alert` (internal escalation only) |
| WF-04C Missed Call Recovery | → `VMC-26-missed-ai-call` |
| WF-05 (booking confirmation) | → `VMC-04-consultation-confirmed` |
| WF-05 (day-before reminder) | → `VMC-05-consultation-reminder` |
| WF-06 No-Show Recovery | → `VMC-06-noshow-recovery` |
| WF-09 (retainer proposal) | → `VMC-07-retainer-proposal` |
| WF-09 (follow-up nudge) | → `VMC-08-retainer-followup` |
| WF-10 Post-Consult Follow-Up | → `VMC-08-retainer-followup` |
| WF-11 (monthly nurture) | → `VMC-10-monthly-nurture` |
| WF-11 (win-back) | → `VMC-11-winback-nurture` |
| WF-12 Score Med Handler | → `VMC-09-score-medium-handler` |
| WF-13 (PIPEDA ack) | → `VMC-12-pipeda-ack` |
| WF-13 (deletion confirmed) | → `VMC-13-pipeda-deleted` |

---

## Part 5 — Verification (1 min)

Run from terminal:

```bash
cd /Users/ranjansingh/Desktop/NeuronX
python3 << 'EOF'
import httpx, json
with open("tools/ghl-lab/.pit-tokens.json") as f:
    pits = json.load(f)
VMC_LOC = pits["vmc"]["locationId"]
HDR = {"Authorization": f"Bearer {pits['vmc']['token']}", "Version": "2021-07-28"}
GHL = "https://services.leadconnectorhq.com"

wfs = httpx.get(f"{GHL}/workflows/?locationId={VMC_LOC}", headers=HDR, timeout=15).json().get("workflows", [])
pipes = httpx.get(f"{GHL}/opportunities/pipelines?locationId={VMC_LOC}", headers=HDR, timeout=15).json().get("pipelines", [])

broken = [w for w in wfs if "🚧" in w["name"]]
wf_cp = [w for w in wfs if w["name"].startswith("WF-CP")]
case_pipe = [p for p in pipes if "Case Processing" in p.get("name", "")]

print(f"Workflows: {len(wfs)} total ({len(broken)} broken should be 0, {len(wf_cp)} WF-CP should be 9)")
print(f"Pipelines: {len(pipes)} total ({len(case_pipe)} Case Processing should be 1)")
print()
if len(broken) == 0 and len(wf_cp) == 9 and len(case_pipe) == 1:
    print("🎉 PASS — 100% sync achieved")
else:
    print("❌ INCOMPLETE — see counts above")
EOF
```

**Expected after 30 min:**
- Workflows: 24 total (0 broken, 9 WF-CP, 15 original)
- Pipelines: 2 (Intake + Case Processing)

---

## 🎁 Pro Tip: Save work as a snapshot from VMC

Once you've built everything in production VMC, create your own snapshot **from prod VMC**:

1. Agency Dashboard → Snapshots → **Create Snapshot**
2. Source: VMC (production)
3. Include: Pipelines, Workflows, Emails, Custom Fields, Tags, Calendars
4. Name: `VMC Production v1.0 — 2026-04-17`

This becomes your template to deploy to future pilot customers in <30 minutes.
