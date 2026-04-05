# Gold Pre-Snapshot Execution Pack — MANUAL ONLY

Status: FINAL
Date: 2026-03-17
Total estimated time: ~2 hours
Prerequisite: Logged into GHL at https://app.gohighlevel.com (NeuronX Test Lab sub-account)

---

## DO THIS NOW — Time-Blocked Checklist

### BLOCK 1: Junk Cleanup + Form Dropdowns (15 min)

- [ ] Delete 3 junk workflows
- [ ] Set form dropdown options (3 fields)

### BLOCK 2: Workflows WF-01 through WF-06 (30 min)

- [ ] WF-01 trigger + actions
- [ ] WF-02 trigger + actions
- [ ] WF-03 trigger + actions
- [ ] WF-04 trigger + actions
- [ ] WF-05 trigger + actions
- [ ] WF-06 trigger + actions

### BLOCK 3: Workflows WF-07 through WF-11 + Landing Page (30 min)

- [ ] WF-07 trigger + actions
- [ ] WF-08 trigger + actions
- [ ] WF-09 trigger + actions
- [ ] WF-10 trigger + actions
- [ ] WF-11 trigger + actions
- [ ] Landing page content

### BLOCK 4: Smoke Test + Snapshot Readiness (15 min)

- [ ] Submit test lead through form
- [ ] Verify contact, pipeline, tags, workflow execution
- [ ] Run snapshot readiness checklist
- [ ] Take snapshot (if all checks pass)

---

## BLOCK 1 — Junk Cleanup + Form Dropdowns

### 1A. Delete Junk Workflows (~2 min)

**Navigate:** Automation → Workflows

**Delete these 3 entries** (three-dot menu → Delete → Confirm):
1. `New Workflow : 1773665053619`
2. `New Workflow : 1773665946429`
3. `New Workflow : 1773666055197`

**Expected after:** Only WF-01 through WF-11 remain in the list (11 workflows).

### 1B. Form Dropdown Options (~10 min)

**Navigate:** Sites → Forms → click "Immigration Inquiry (V1)" → Edit

For each dropdown field, click the field in the builder → open field settings → set options:

**Field: Program Interest**
```
Express Entry
Provincial Nominee (PNP)
Study Permit
Work Permit
Family Sponsorship
Visitor Visa
Not Sure
```

**Field: Current Location (Country)**
```
Canada
India
Philippines
Nigeria
Pakistan
Other
```

**Field: Timeline**
```
Within 3 months
3-6 months
6-12 months
More than 12 months
Just exploring
```

Click **Save** after all three fields are configured.

**Expected after:** Form preview shows all dropdowns with correct options.

---

## BLOCK 2 — Workflows WF-01 through WF-06

**How to configure each workflow:**
1. Automation → Workflows → click the workflow name
2. Press Escape if a modal overlay appears
3. Click "Add New Trigger" node → select trigger type → configure → Save Trigger
4. Click the "+" button below the trigger to add actions in sequence
5. For each action: select type → configure → Save

### WF-01 — New Inquiry Acknowledge

**Trigger:** Form Submitted → select "Immigration Inquiry (V1)"

| # | Action Type | Configuration |
|---|---|---|
| 1 | Add Contact Tag | Tag: `nx:new_inquiry` |
| 2 | Create/Update Opportunity | Pipeline: NeuronX — Immigration Intake, Stage: NEW |
| 3 | Send SMS | Body: `Hi {{contact.first_name}}, thank you for your immigration inquiry. Our team will be in touch shortly. — [Firm Name]` |
| 4 | Send Email | Subject: `We received your inquiry` / Body: acknowledgment with firm branding |
| 5 | Add Contact Tag | Tag: `nx:contacting:start` |
| 6 | Update Opportunity | Move to stage: CONTACTING |

**Expected after:** Save all. "Execution Logs" tab should show trigger + 6 actions.

### WF-02 — Contact Attempt Sequence

**Trigger:** Contact Tag Added → `nx:contacting:start`

| # | Action Type | Configuration |
|---|---|---|
| 1 | Create Manual Action (Task) | Title: `Call lead (Attempt 1)` |
| 2 | Wait | 30 minutes |
| 3 | Send SMS | Body: `Hi {{contact.first_name}}, we tried reaching you. You can book a call here: [calendar link]. Reply to this message anytime.` |
| 4 | Wait | 2 hours |
| 5 | Create Manual Action (Task) | Title: `Call lead (Attempt 2)` |
| 6 | Wait | 1 business day |
| 7 | Create Manual Action (Task) | Title: `Call lead (Attempt 3) + voicemail` |
| 8 | Wait | 2 business days |
| 9 | Send SMS | Body: booking link + callback request |
| 10 | Wait | 5 business days |
| 11 | Send Email | Subject: `Still interested?` / Body: booking link + value message |
| 12 | Wait | 10 business days |
| 13 | Send SMS | Body: final outreach — `We'd still love to help. Book here: [link]` |
| 14 | Update Opportunity | Move to stage: UNREACHABLE |
| 15 | Add Contact Tag | Tag: `nx:nurture:enter` |

**Expected after:** 15 action steps visible in sequence.

### WF-03 — Mark Contacted → Readiness

**Trigger:** Contact Tag Added → `nx:contacted`

| # | Action Type | Configuration |
|---|---|---|
| 1 | Add Contact Tag | Tag: `nx:assessment:required` |
| 2 | Create Manual Action (Task) | Title: `Complete readiness assessment (R1-R6)` |

**Expected after:** 2 action steps.

### WF-04 — Readiness Complete → Invite Booking

**Trigger:** Contact Tag Added → `nx:assessment:complete`

| # | Action Type | Configuration |
|---|---|---|
| 1 | If/Else Condition | If custom field `readiness_outcome` = `Ready` or `Ready - Urgent` |
| 2 | (Yes branch) Update Opportunity | Move to stage: CONSULT READY |
| 3 | (Yes branch) Add Contact Tag | Tag: `nx:consult_ready` |
| 4 | (Yes branch) Send SMS | Body: booking link invitation |
| 5 | (Yes branch) Send Email | Subject: `Book your consultation` / Body: calendar link |
| 6 | (Yes branch) Add Contact Tag | Tag: `nx:booking:invited` |
| 7 | (No branch) If/Else | If `readiness_outcome` = `Not Ready` |
| 8 | (Not Ready) Update Opportunity | Move to stage: NURTURE |
| 9 | (Not Ready) Add Contact Tag | Tag: `nx:nurture:enter` |
| 10 | (Else: Disqualified) Update Opportunity | Move to stage: LOST |
| 11 | (Else: Disqualified) Add Contact Tag | Tag: `nx:lost` |

**Expected after:** Branching flow with 3 paths visible.

### WF-05 — Appointment Booked → Reminders

**Trigger:** Customer Booked Appointment → Calendar: "Immigration Consultations"

| # | Action Type | Configuration |
|---|---|---|
| 1 | Update Opportunity | Move to stage: BOOKED |
| 2 | Add Contact Tag | Tag: `nx:booking:confirmed` |
| 3 | Send SMS | Body: confirmation with date/time, agenda prep |
| 4 | Send Email | Subject: `Consultation confirmed` / Body: details + prep instructions |
| 5 | Wait | Until 48 hours before appointment |
| 6 | Send SMS | Body: `Your consultation is in 2 days. Reply YES to confirm.` |
| 7 | Wait | Until 24 hours before appointment |
| 8 | Send SMS | Body: `Reminder: consultation tomorrow at {{appointment.time}}` |
| 9 | Wait | Until 2 hours before appointment |
| 10 | Send SMS | Body: `Your consultation starts in 2 hours.` |

**Expected after:** 10 action steps with 3 timed waits.

### WF-06 — No-Show → Recovery

**Trigger:** Appointment Status → No Show

| # | Action Type | Configuration |
|---|---|---|
| 1 | Add Contact Tag | Tag: `nx:appointment:noshow` |
| 2 | Wait | 5 minutes |
| 3 | Send SMS | Body: `We missed you! Life happens. Reschedule here: [link]` |
| 4 | Wait | 10 minutes |
| 5 | Create Manual Action (Task) | Title: `Call no-show within 15 min` |
| 6 | Wait | 2 hours |
| 7 | Send SMS | Body: reschedule link |
| 8 | Wait | 1 business day |
| 9 | Send SMS | Body: follow-up |
| 10 | Wait | 3 business days |
| 11 | Send Email | Subject: `We'd love to reschedule` |
| 12 | Wait | 7 business days |
| 13 | Send SMS | Body: final reschedule attempt |
| 14 | Update Opportunity | Move to stage: NURTURE |

**Expected after:** 14 action steps.

---

## BLOCK 3 — Workflows WF-07 through WF-11 + Landing Page

### WF-07 — Consultation Outcome Capture

**Trigger:** Appointment Status → Completed (Show / Checked In)

| # | Action Type | Configuration |
|---|---|---|
| 1 | Create Manual Action (Task) | Title: `Record consultation outcome in custom field` |
| 2 | Wait | 1 hour |
| 3 | Internal Notification | Notify consultant: `Outcome still needed for {{contact.name}}` |
| 4 | Wait | 3 hours |
| 5 | Internal Notification | Notify firm owner: `Missing outcome for {{contact.name}}` |

**Expected after:** 5 action steps.

### WF-08 — Outcome Routing

**Trigger:** Contact Changed → Custom Field: `consultation_outcome`

| # | Action Type | Configuration |
|---|---|---|
| 1 | If/Else Condition | If `consultation_outcome` = `Proceed` |
| 2 | (Proceed) Add Contact Tag | Tag: `nx:outcome:proceed` |
| 3 | (Proceed) Update Opportunity | Move to stage: CONSULT COMPLETED |
| 4 | (Else) If/Else | If `consultation_outcome` = `Follow-Up` |
| 5 | (Follow-Up) Add Contact Tag | Tag: `nx:outcome:follow_up` |
| 6 | (Follow-Up) Update Opportunity | Move to stage: CONSULT COMPLETED |
| 7 | (Else: Declined) Add Contact Tag | Tag: `nx:outcome:declined` |
| 8 | (Declined) Update Opportunity | Move to stage: LOST |

**Expected after:** Branching flow with 3 outcome paths.

### WF-09 — Retainer Follow-Up

**Trigger:** Contact Tag Added → `nx:outcome:proceed`

| # | Action Type | Configuration |
|---|---|---|
| 1 | Send Email | Subject: `Next steps: retainer & checklist` / Body: retainer doc + payment instructions |
| 2 | Update Contact Field | Set `retainer_sent` = true |
| 3 | Wait | 1 day |
| 4 | Send SMS | Body: `Just checking in — did you receive the retainer?` |
| 5 | Wait | 1 day |
| 6 | Send SMS/Email | Follow-up on retainer |
| 7 | Wait | 3 days |
| 8 | Send Email | Subject: `Retainer follow-up` |
| 9 | Wait | 5 days |
| 10 | Create Manual Action (Task) | Title: `Consultant call — Day 10 retainer chase` |
| 11 | Wait | 4 days |
| 12 | Send Email | Subject: `Final follow-up` / Body: final notice |
| 13 | Update Opportunity | Move to stage: NURTURE (if unsigned) |

**Expected after:** 13 action steps.

### WF-10 — Post-Consult Follow-Up (Undecided)

**Trigger:** Contact Tag Added → `nx:outcome:follow_up`

| # | Action Type | Configuration |
|---|---|---|
| 1 | Send Email | Subject: `Consultation summary` / Body: recap + next steps |
| 2 | Wait | 2 days |
| 3 | Send SMS | Body: `Checking in — any questions from your consultation?` |
| 4 | Wait | 3 days |
| 5 | Send Email | Subject: `Resources for your immigration journey` / Body: value-add |
| 6 | Wait | 2 days |
| 7 | Create Manual Action (Task) | Title: `Call/SMS check-in` |
| 8 | Wait | 7 days |
| 9 | Send Email | Subject: `Ready to move forward?` / Body: gentle close |
| 10 | Update Opportunity | Move to stage: NURTURE |

**Expected after:** 10 action steps.

### WF-11 — Nurture Campaign Monthly

**Trigger:** Contact Tag Added → `nx:nurture:enter`

| # | Action Type | Configuration |
|---|---|---|
| 1 | If/Else Condition | If custom field `marketing_consent` = true |
| 2 | (Yes) Send Email | Subject: `Monthly Immigration Update` / Body: newsletter |
| 3 | (Yes) Wait | 30 days |
| 4 | (Yes) Send Email | Body: next month newsletter |
| 5 | (Yes) Wait | 60 days |
| 6 | (Yes) Send SMS | Body: `How are things going? We're here if you need us.` |
| 7 | (No consent) End / Do nothing |

**Expected after:** Conditional flow with consent check.

### Landing Page Content (~15 min)

**Navigate:** Sites → Funnels → "NeuronX Intake Landing (V1)" → click step "Immigration Inquiry" → Edit

**Add these elements top to bottom:**

1. **Hero Section**
   - Headline: `Start Your Canadian Immigration Journey`
   - Subheadline: `Free initial assessment — takes 2 minutes`
   - Background: professional, clean (use default theme)

2. **Form Embed**
   - Add Form element → select "Immigration Inquiry (V1)"
   - Button text: `Get Your Free Assessment`

3. **Alternative CTA Section**
   - Text: `Ready to talk? Book a consultation directly.`
   - Button: `Book Now` → link to calendar booking page URL

4. **Compliance Footer**
   - Text: `This form is for inquiry purposes only. Submitting this form does not create a solicitor-client relationship and does not guarantee eligibility for any immigration program.`

Click **Save** and **Publish**.

**Expected after:** Public URL loads with form, booking CTA, and compliance footer.

---

## BLOCK 4 — Smoke Test + Snapshot Readiness

### Smoke Test (~15 min)

| # | Action | Expected Result | Pass? |
|---|---|---|---|
| 1 | Open landing page URL in incognito | Page loads with form + booking CTA | [ ] |
| 2 | Fill form: First=Test, Last=Lead, Email=test@example.com, Phone=+16135551234, Program=Express Entry, Country=Canada, Timeline=3-6 months | All dropdowns work, consent checkbox visible | [ ] |
| 3 | Submit form | Success message / redirect | [ ] |
| 4 | Check GHL Contacts | "Test Lead" appears with filled fields | [ ] |
| 5 | Check Pipeline | Opportunity in NeuronX pipeline at NEW → CONTACTING | [ ] |
| 6 | Check Contact Tags | `nx:new_inquiry` and `nx:contacting:start` present | [ ] |
| 7 | Check WF-01 Execution Logs | Shows triggered, actions executed | [ ] |
| 8 | Book appointment via calendar link | Booking confirmation received | [ ] |
| 9 | Check WF-05 Execution Logs | Shows triggered on booking | [ ] |
| 10 | Delete test contact | Clean state for UAT | [ ] |

### Snapshot Readiness Checklist

Before creating the snapshot, verify every item:

| # | Item | How to Verify | Status |
|---|---|---|---|
| 1 | Pipeline has 9 stages | Opportunities → Pipeline settings | [ ] |
| 2 | 41 custom fields exist | Settings → Custom Fields → count | [ ] |
| 3 | 21 tags exist | Settings → Tags → count | [ ] |
| 4 | Calendar exists and has availability | Calendars → check "Immigration Consultations" | [ ] |
| 5 | Form has 3 working dropdowns | Sites → Forms → Preview | [ ] |
| 6 | Landing page published | Sites → Funnels → check status | [ ] |
| 7 | WF-01 has trigger + actions | Automation → WF-01 → check | [ ] |
| 8 | WF-02 has trigger + 15 actions | Automation → WF-02 → check | [ ] |
| 9 | WF-03 has trigger + 2 actions | Automation → WF-03 → check | [ ] |
| 10 | WF-04 has trigger + branching | Automation → WF-04 → check | [ ] |
| 11 | WF-05 has trigger + 10 actions | Automation → WF-05 → check | [ ] |
| 12 | WF-06 has trigger + 14 actions | Automation → WF-06 → check | [ ] |
| 13 | WF-07 has trigger + 5 actions | Automation → WF-07 → check | [ ] |
| 14 | WF-08 has trigger + branching | Automation → WF-08 → check | [ ] |
| 15 | WF-09 has trigger + 13 actions | Automation → WF-09 → check | [ ] |
| 16 | WF-10 has trigger + 10 actions | Automation → WF-10 → check | [ ] |
| 17 | WF-11 has trigger + consent check | Automation → WF-11 → check | [ ] |
| 18 | No junk workflows remain | Automation → only 11 named WFs | [ ] |
| 19 | Smoke test passed | All 10 items above | [ ] |
| 20 | All workflows in DRAFT (not published yet) | Check each — publish after UAT | [ ] |

### Create Snapshot

Once all 20 items pass:

1. Settings → Company → Snapshots
2. Click "Create New Snapshot"
3. Name: `NeuronX Gold v1.0 — YYYY-MM-DD`
4. Include: All (pipeline, workflows, forms, calendars, custom fields, tags, funnels)
5. Confirm creation
6. Record snapshot ID for UAT

---

## Summary

| Block | Time | Items |
|---|---|---|
| 1: Cleanup + Form | 15 min | Delete 3 junk WFs, set 3 dropdown fields |
| 2: WF-01 to WF-06 | 30 min | 6 workflows with triggers + actions |
| 3: WF-07 to WF-11 + Page | 30 min | 5 workflows + landing page |
| 4: Smoke Test + Snapshot | 15 min | 10-point test + 20-point checklist |
| **Total** | **~90 min** | |
