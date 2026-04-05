# Week 1 Checklist — GHL Gold Build Complete

**Objective**: Complete GHL Gold sub-account → Run UAT → Get M1 milestone
**Exit Criteria**: 11 workflows configured, 4 UAT scenarios passed, UAT report signed off
**Milestone**: M1 — Gold Complete

---

## PRE-REQUISITE (Before Week 1 Can Start)

### Founder: Log into Skyvern Session [BLOCKING]

```
URL: https://app.skyvern.com/browser-session/pbs_506976117979052016
Time Required: 30 minutes (one-time setup)
Impact: Unblocks WF-02 through WF-11 automation
```

**Steps for Founder**:
1. Open the URL above in browser
2. Log in with your GHL credentials
3. Complete any 2FA
4. Confirm session is active (should show GHL dashboard)
5. Notify AI agent: "Skyvern session is active"

---

## Day 1 (Monday): Resume Workflow Configuration

**Dependencies**: Skyvern session active

### WF-02: Contact Attempts (7-Step Sequence)
```bash
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-02
```
**Spec**:
- Trigger: Tag added `nx:lead_received` (or WF-01 completes)
- Action 1: SMS "Hi [Name], this is [Firm]. I'd love to chat about your immigration goals. Are you available for a quick call?"
- Wait: 2 hours
- Action 2: SMS "Hi [Name], tried reaching you — happy to chat when you're free."
- Wait: 4 hours
- Action 3: Phone call task assigned to intake coordinator
- Wait: Next day
- Action 4: SMS (morning) + call task
- Wait: Next day
- Action 5: Email outreach
- Wait: 2 days
- Action 6: SMS "Last check-in — let us know if you're still looking for immigration help."
- Wait: 3 days
- Action 7: Move to UNREACHABLE stage, tag `nx:unreachable`

### WF-03: Mark Contacted / Assessment Trigger
```bash
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-03
```
**Spec**:
- Trigger: Tag added `nx:contacted`
- Action: Move opportunity to ASSESSMENT SCHEDULED stage
- Action: Create task "Complete readiness assessment with [Name]"
- Action: Send SMS with assessment booking link

**Verification After Each WF**:
- Open GHL Workflows list
- Confirm WF appears with PUBLISHED status
- Check trigger and first action are correct

---

## Day 2 (Tuesday): Booking & Reminders Workflows

### WF-04: Readiness Complete → Booking Invite
```bash
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-04
```
**Spec**:
- Trigger: Tag added `nx:assessment:complete`
- Condition: `ai_readiness_outcome` NOT IN ["not_ready", "disqualified"]
- Action: Move to CONSULT READY stage
- Action: SMS with booking link `[consultation_booking_url]`
- Wait: 24 hours
- Action: If not booked, send reminder SMS

### WF-05: Appointment Booked → Confirmation
```bash
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-05
```
**Spec**:
- Trigger: Appointment status = "Booked" (Calendar: `To1U2KbcvJ0EAX0RGKHS`)
- Action: Move to BOOKED stage
- Action: Confirmation email with appointment details
- Action: Tag `nx:booked`

### WF-06: Consultation Reminders
```bash
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-06
```
**Spec**:
- Trigger: Appointment booked (48h before)
- Action 1 (48h before): SMS "Your consultation is in 2 days on [Date] at [Time]. Reply YES to confirm."
- Action 2 (24h before): SMS "Reminder: Tomorrow at [Time] with [Consultant Name]."
- Action 3 (2h before): SMS "Your consultation starts in 2 hours. Join here: [link]"
- Action 4 (15min before): Email with briefing link (if available)

---

## Day 3 (Wednesday): Recovery & Outcome Workflows

### WF-07: No-Show Recovery
```bash
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-07
```
**Spec**:
- Trigger: Appointment status = "No Show"
- Action: Move to NO-SHOW stage
- Action: Tag `nx:no_show`
- Wait: 1 hour
- Action: SMS "Hi [Name], we missed you today! Can we reschedule? [link]"
- Wait: 1 day
- Action: SMS "Still interested in booking? Here's the link: [link]"
- Wait: 2 days
- Action: Phone call task
- Wait: 2 days
- Action: SMS "Last attempt — happy to help when ready."
- Wait: 3 days
- Action: Move to COLD stage if no response

### WF-08: Consultation Outcome Routing
```bash
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-08
```
**Spec**:
- Trigger: Appointment marked completed + `ai_consultation_outcome` field updated
- Condition A (outcome = "Proceed"): Move to RETAINER stage, tag `nx:retainer_requested`, trigger WF-09
- Condition B (outcome = "Follow-Up"): Move to FOLLOW-UP stage, trigger WF-10
- Condition C (outcome = "Declined"): Move to DECLINED stage, trigger WF-11 (nurture)
- Condition D (outcome = "No Show"): Trigger WF-07

---

## Day 4 (Thursday): Follow-Up & Nurture Workflows

### WF-09: Retainer Follow-Up Sequence
```bash
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-09
```
**Spec**:
- Trigger: Tag `nx:retainer_requested`
- Day 0: Email retainer agreement + onboarding checklist
- Day 1: SMS "Hi [Name], just checking you received the retainer. Any questions?"
- Day 2: Follow-up email
- Day 5: SMS "Still here to help — shall we get started?"
- Day 10: SMS final check-in
- Day 14: Move to COLD if no response

### WF-10: Post-Consult Follow-Up (Undecided)
```bash
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-10
```
**Spec**:
- Trigger: Tag `nx:follow_up_needed`
- Week 1: SMS + email
- Week 2: SMS "Still thinking about it? Happy to answer any questions."
- Week 4: Email case study / success story
- Week 6: Final check-in

### WF-11: Nurture Campaign
```bash
cd tools/ghl-lab && npx tsx src/skyvern/skyvernOrchestrator.ts wf-11
```
**Spec**:
- Trigger: Move to NURTURE stage
- Monthly: Email newsletter / immigration updates
- Quarterly: SMS check-in
- Condition: Suppress if `nx:sms_stop` or `nx:email_unsubscribed` tags present

**Verify All 11 Workflows Published**:
```bash
cd tools/ghl-lab && npx tsx src/verifyWorkflows.ts
```

---

## Day 5 (Friday): Content & Configuration

### Form Dropdown Options
```bash
cd tools/ghl-lab && npx tsx src/fixFormDropdowns.ts
```
**Required Options**:
- **Program Interest**: Express Entry, Spousal Sponsorship, Study Permit, Work Permit, LMIA, PR Renewal, Citizenship, Visitor Visa, Other
- **Current Location**: In Canada, Outside Canada
- **Timeline**: Urgent (within 30 days), Near-term (1-3 months), Medium (3-6 months), Long-term (6+ months)

### Landing Page Content
```bash
cd tools/ghl-lab && npx tsx src/skyvern/implementGoldLandingPage.ts
```
**Required Content**:
- **Headline**: "Fast, Structured Immigration Intake — Backed by Licensed RCICs"
- **Sub-headline**: "Submit your inquiry and our AI-assisted team will contact you within 5 minutes."
- **CTA Button**: "Get Started — Free Initial Assessment"
- **Programs Section**: List 5-6 core programs with brief descriptions
- **Trust Signals**: CICC badge + "Licensed RCICs" + consultation count
- **Footer**: "We are a licensed immigration consulting firm. This form collects preliminary information only and does not constitute immigration advice. All consultations are conducted by licensed RCICs."

### Message Templates (via GHL API or Skyvern)
Ensure all SMS templates use `{{contact.firstName}}` personalization tokens.
Templates listed in `docs/06_execution/CURRENT_STATE.md` Block 7.

### Cleanup Junk Workflows
```bash
cd tools/ghl-lab && npx tsx src/deleteJunkWorkflows.ts
```

---

## Day 6 (Saturday): UAT Execution

### UAT-01: Happy Path (Inquiry → Retained)

**Setup**:
```bash
cd tools/ghl-lab && npx tsx src/api/populateDemoData.ts --scenario=happy_path
```

**Steps**:
1. Submit form at Funnel URL (get URL from `tools/ghl-lab/src/skyvern/getLandingPageUrl.ts`)
2. Verify: Contact created in GHL with correct fields
3. Verify: Opportunity created in CONTACTING stage
4. Add tag `nx:contacted` manually → verify stage moves to ASSESSMENT SCHEDULED
5. Fill readiness fields (R1-R5) + set outcome = "ready_standard"
6. Add tag `nx:assessment:complete` → verify CONSULT READY + booking SMS sent
7. Book appointment → verify stage = BOOKED + reminders scheduled
8. Mark appointment completed, set outcome = "Proceed"
9. Verify: Stage = RETAINER, retainer email sent, follow-up tasks created

**Pass Criteria**: All 9 steps complete without manual intervention (except steps 4, 5, 8)

### UAT-02: No-Show Recovery

**Steps**:
1. Create contact + book appointment (skip to step 7 of UAT-01)
2. Mark appointment as "No Show"
3. Verify: Stage = NO-SHOW, WF-07 triggered
4. Wait/simulate time → verify recovery SMS sent
5. Click rebook link → verify reminder schedule restarts

### UAT-03: Consent Suppression (CASL Compliance)

**Steps**:
1. Submit form with marketing consent = NO
2. Move contact to NURTURE stage
3. Verify: No marketing emails received (WF-11 suppressed)
4. Simulate SMS STOP from contact
5. Verify: Tag `nx:sms_stop` added, no more SMS from any workflow

### UAT-04: Complex Lead Routing

**Steps**:
1. Create contact + complete assessment
2. Set `ai_readiness_outcome` = "ready_complex" (deportation/inadmissibility flag)
3. Verify: Tag `nx:human_escalation` added
4. Verify: NOT automatically sent to self-serve booking
5. Verify: Task created for senior consultant review

**Evidence Required**: Screenshots of each step for UAT report.

---

## Day 7 (Sunday): Week 1 Review

### Checklist
- [ ] WF-01: Configured & verified ✅
- [ ] WF-02: Configured & verified
- [ ] WF-03: Configured & verified
- [ ] WF-04: Configured & verified
- [ ] WF-05: Configured & verified
- [ ] WF-06: Configured & verified
- [ ] WF-07: Configured & verified
- [ ] WF-08: Configured & verified
- [ ] WF-09: Configured & verified
- [ ] WF-10: Configured & verified
- [ ] WF-11: Configured & verified
- [ ] Form dropdown options populated
- [ ] Landing page content updated
- [ ] Message templates created (5 SMS + 2 email)
- [ ] Junk workflows deleted
- [ ] UAT-01: PASS
- [ ] UAT-02: PASS
- [ ] UAT-03: PASS
- [ ] UAT-04: PASS
- [ ] UAT report written with evidence
- [ ] PROJECT_MEMORY.md updated
- [ ] TEAM_LOG.md updated with M1 milestone

### Milestone M1 Achieved When
All checkboxes above are checked. Record in TEAM_LOG.md:
```
### [PROGRESS] YYYY-MM-DD — M1 GOLD COMPLETE
All 11 workflows configured. 4/4 UAT scenarios passed. UAT report complete.
Next: Week 2 — Snapshot creation.
```

---

**Template version**: 1.0
**Created**: 2026-03-21
