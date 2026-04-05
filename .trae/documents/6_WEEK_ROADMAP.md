# NeuronX 6-Week Tactical Roadmap

**Version**: 1.0  
**Date**: 2026-03-21  
**Objective**: Ship first paying pilot customer  
**Exit Criteria**: Immigration firm using NeuronX in production, first retainer signed via system

---

## Week 1: Complete Gold Build

### Monday: Resume Workflow Configuration

**Dependencies**: Founder login to Skyvern session `pbs_506976117979052016`

**Tasks**:
1. ✅ Verify Skyvern session active
2. ⚠️ Configure WF-02 (Contact Attempts) — 7-step sequence
3. ⚠️ Configure WF-03 (Mark Contacted) — assessment trigger
4. ⚠️ Verify WF-02 and WF-03 persistence

**Deliverable**: WF-02, WF-03 configured and published in GHL

---

### Tuesday: Booking & Reminders Workflows

**Tasks**:
1. ⚠️ Configure WF-04 (Readiness Complete → Booking Invite)
2. ⚠️ Configure WF-05 (Appointment Booked → Confirmation)
3. ⚠️ Configure WF-06 (Consultation Reminders) — 48h/24h/2h
4. ⚠️ Verify persistence

**Deliverable**: WF-04, WF-05, WF-06 configured and published

---

### Wednesday: Recovery & Outcome Workflows

**Tasks**:
1. ⚠️ Configure WF-07 (No-Show Recovery) — 6-step sequence
2. ⚠️ Configure WF-08 (Outcome Routing) — proceed/follow-up/declined
3. ⚠️ Verify persistence

**Deliverable**: WF-07, WF-08 configured and published

---

### Thursday: Follow-Up & Nurture Workflows

**Tasks**:
1. ⚠️ Configure WF-09 (Retainer Follow-Up) — days 0/1/2/5/10/14
2. ⚠️ Configure WF-10 (Post-Consult Follow-Up) — undecided prospects
3. ⚠️ Configure WF-11 (Nurture Campaign) — monthly email, quarterly SMS
4. ⚠️ Verify all 11 workflows published and active

**Deliverable**: All 11 workflows complete

---

### Friday: Content & Configuration

**Tasks**:
1. ⚠️ Configure form dropdown options:
   - Program Interest: Express Entry, Spousal, Study, Work, LMIA, PR Renewal, Citizenship, Visitor, Other
   - Current Location: In Canada, Outside Canada
   - Timeline: Urgent (30d), Near-term (1-3mo), Medium (3-6mo), Long-term (6mo+)
2. ⚠️ Edit landing page content:
   - Headline: "Immigration Advice Backed by a Structured Assessment Process"
   - Trust signals: CICC badge, "500+ Families Served", "Licensed RCICs"
   - Programs section: List core immigration programs
   - Footer: Compliance language (no eligibility guarantees)
3. ⚠️ Create message templates:
   - Acknowledgment SMS: "Hi [Name], thanks for reaching out. We'll contact you within 5 minutes."
   - Booking SMS: "Hi [Name], ready to book your consultation? [link]"
   - Reminder SMS (48h): "Hi [Name], your consultation is in 2 days. Reply YES to confirm."
   - No-show SMS: "Hi [Name], we missed you! Happy to reschedule: [link]"
4. ⚠️ Delete junk workflows (cleanup)

**Deliverable**: Gold sub-account fully configured

---

### Saturday: UAT Execution

**Tasks**:
1. ⚠️ UAT-01 (Happy Path):
   - Submit form → Verify contact created, opportunity in CONTACTING
   - Tag as `nx:contacted` → Complete readiness fields → Tag `nx:assessment:complete`
   - Verify stage → CONSULT READY, booking link sent
   - Book appointment → Verify BOOKED, reminders scheduled
   - Mark completed → Record outcome = "Proceed"
   - Verify retainer email sent, follow-up tasks created
2. ⚠️ UAT-02 (No-Show Recovery):
   - Book appointment → Mark No-Show
   - Verify recovery SMS sent, call task created
   - Rebook → Verify reminder schedule restarts
3. ⚠️ UAT-03 (Consent Suppression):
   - Submit lead without marketing consent
   - Move to NURTURE → Verify no marketing emails
   - Simulate STOP opt-out → Verify suppression applied
4. ⚠️ UAT-04 (Complex Lead Routing):
   - Set readiness outcome = "Ready — Complex"
   - Verify assigned to senior consultant, booking not auto-sent

**Deliverable**: UAT report with screenshots/evidence for all 4 scenarios

---

### Sunday: Week 1 Review

**Checklist**:
- ✅ All 11 workflows configured and published
- ✅ Form dropdowns populated
- ✅ Landing page content finalized
- ✅ Message templates created
- ✅ All 4 UAT scenarios passed
- ✅ UAT report signed off

**Milestone**: M1 — Gold Complete ✅

---

## Week 2: Snapshot Productization

### Monday: Snapshot Creation

**Tasks**:
1. ⚠️ In GHL Agency View → Account Snapshots → Create Snapshot
2. ⚠️ Name: "NeuronX Immigration Intake v1.0"
3. ⚠️ Verify snapshot includes:
   - Pipeline and stages ✅
   - All 11 workflows ✅
   - Forms ✅
   - Calendars ✅
   - Custom fields and tags ✅
   - Funnel/landing page ✅
4. ⚠️ Record snapshot ID
5. ⚠️ Create share link (if supported)

**Deliverable**: Snapshot created and ID recorded

---

### Tuesday: Snapshot Install

**Tasks**:
1. ⚠️ Create second test sub-account: "NeuronX Snapshot Install Lab"
2. ⚠️ Install snapshot (manual or Playwright automation)
3. ⚠️ Measure install time (target: < 30 min)
4. ⚠️ Document manual steps required

**Deliverable**: Snapshot installed in second tenant

---

### Wednesday: Snapshot Validation

**Tasks**:
1. ⚠️ Re-run UAT-01 in snapshot tenant (happy path)
2. ⚠️ Verify all workflows execute correctly
3. ⚠️ Verify form, calendar, pipeline, custom fields all present
4. ⚠️ Record any missing assets or configuration drift

**Deliverable**: Snapshot validation report

---

### Thursday: Onboarding Playbook

**Tasks**:
1. ⚠️ Document step-by-step onboarding process:
   - Create sub-account
   - Install snapshot
   - Configure firm branding (name, logo, colors)
   - Connect voice provider credentials (pending Week 3 decision)
   - Test submit form → verify flow
   - Go live
2. ⚠️ Estimate onboarding time: [X] hours
3. ⚠️ Identify manual steps that cannot be automated

**Deliverable**: Onboarding playbook v1.0

---

### Friday: Week 2 Review

**Checklist**:
- ✅ Snapshot created
- ✅ Snapshot installed in second tenant
- ✅ UAT-01 re-passed in snapshot tenant
- ✅ Install time < 30 min (or manual process documented)
- ✅ Onboarding playbook written

**Milestone**: M2 — Snapshot Proven ✅

---

## Week 3: Voice AI Bake-Off

### Monday: Track A — GHL Voice AI

**Tasks**:
1. ⚠️ Configure GHL Voice AI agent in Test Lab
2. ⚠️ Set prompt:
   - Identify as firm's AI-assisted team
   - Ask R1-R5 readiness questions (program interest, location, urgency, history, budget)
   - Offer to book consultation
   - Escalate on eligibility questions, deportation mentions, low confidence
3. ⚠️ Test 5 calls (role-play prospect scenarios)
4. ⚠️ Score against bake-off scorecard:
   - Tone control (1-5)
   - Script control (1-5)
   - Trust boundary safety (1-5)
   - Escalation / transfer (1-5)
   - Appointment booking (1-5)
   - CRM write-back (1-5)
   - Workflow triggering (1-5)
   - Consent enforcement (1-5)
   - Observability (1-5)
   - Reliability (1-5)
   - Cost (1-5)

**Deliverable**: Track A scorecard completed

---

### Tuesday: Track B — External Voice (Vapi)

**Tasks**:
1. ⚠️ Provision Vapi assistant (if not already done)
2. ⚠️ Configure immigration-specific prompts (same as Track A)
3. ⚠️ Test 5 calls (same scenarios as Track A)
4. ⚠️ Test webhook → GHL field update (readiness data write-back)
5. ⚠️ Score against bake-off scorecard (same criteria)

**Deliverable**: Track B scorecard completed

---

### Wednesday: Track D — Webhook Security

**Tasks**:
1. ⚠️ Set up webhook receiver (local or deployed)
2. ⚠️ Test GHL webhook signature verification:
   - Verify `X-GHL-Signature` (Ed25519)
   - Reject invalid signatures
   - Support legacy `X-WH-Signature` (RSA) if present
3. ⚠️ Test replay protection:
   - Reject stale webhooks (timestamp > 5 min old)
   - Reject duplicate `webhookId`
4. ⚠️ Document verification implementation

**Deliverable**: Webhook security validated

---

### Thursday: Voice Layer Decision

**Tasks**:
1. ⚠️ Compare Track A vs Track B scores:
   - Average score: Track A [X.X] vs Track B [Y.Y]
   - Trust boundary safety: Track A [X] vs Track B [Y]
   - Cost per successful contact: Track A [$X] vs Track B [$Y]
2. ⚠️ Founder reviews scorecards
3. ⚠️ Founder approves voice layer:
   - **Option A**: GHL Voice AI (if avg ≥ 4.0 and trust safety = 5)
   - **Option B**: Vapi (if materially better on tone/control/reliability)
4. ⚠️ Update `/docs/03_infrastructure/product_boundary.md`
5. ⚠️ Resolve OD-01 in `/docs/05_governance/open_decisions.md`

**Deliverable**: Voice layer locked ✅

---

### Friday: Week 3 Review

**Checklist**:
- ✅ Track A (GHL Voice AI) tested and scored
- ✅ Track B (External Voice) tested and scored
- ✅ Webhook security validated
- ✅ Voice layer decision made and documented
- ✅ OD-01 resolved

**Milestone**: M3 — Voice Locked ✅

---

## Week 4: Build NeuronX Thin Brain

### Monday-Tuesday: Core Components

**Tasks**:
1. ⚠️ Set up project scaffold:
   - Node.js/TypeScript or Python
   - Webhook server (Express or FastAPI)
   - Minimal data store (SQLite or PostgreSQL)
2. ⚠️ Build webhook receiver:
   - `/webhooks/ghl` — GHL form submission, appointment events
   - `/webhooks/voice` — Voice provider callback (call ended, transcript)
   - Signature verification (Ed25519 for GHL)
3. ⚠️ Build voice orchestrator:
   - Trigger voice call (GHL Voice AI API or Vapi API)
   - Process call outcome (parse transcript/summary)
   - Write to GHL custom fields (readiness data)

**Deliverable**: Webhook receiver + voice orchestrator working

---

### Wednesday: Readiness Scorer

**Tasks**:
1. ⚠️ Parse transcript/summary for R1-R5:
   - R1: Program Interest (extract: Express Entry, spousal, etc.)
   - R2: Current Location (extract: In Canada, Outside Canada)
   - R3: Timeline Urgency (extract: 30d, 1-3mo, 3-6mo, 6mo+)
   - R4: Prior Applications (extract: None, Approved, Has refusal)
   - R5: Budget Awareness (extract: Aware, Unaware, Unclear)
2. ⚠️ Calculate readiness outcome:
   - Ready (Standard): R1-R5 answered, no complexity flags
   - Ready (Urgent): R3 < 30 days
   - Ready (Complex): Complexity keywords detected (deportation, inadmissibility, etc.)
   - Not Ready: Prospect explicitly not ready
   - Disqualified: Unrelated inquiry
3. ⚠️ Write outcome to GHL custom fields
4. ⚠️ Trigger GHL workflow by adding tag: `nx:assessment:complete`

**Deliverable**: Readiness scorer working

---

### Thursday: Consultation Prep Assembler

**Tasks**:
1. ⚠️ Build scheduled job: runs 30 min before appointment
2. ⚠️ Pull data from GHL API:
   - Contact: name, phone, email
   - Custom fields: program interest, location, urgency, history, readiness outcome
   - Notes: all interaction notes
   - Tags: source, priority flags
   - Appointment: date, time, consultant
3. ⚠️ Assemble structured briefing:
   - Header: Name, contact, date, time, consultant
   - Section A: Inquiry (date, source, days since inquiry)
   - Section B: Readiness (R1-R5 data, outcome, flags)
   - Section C: Interactions (chronological: first contact, follow-ups, quotes)
   - Section D: Prep Notes (key questions, risk factors, suggested approach)
4. ⚠️ Deliver briefing:
   - Primary: Email to consultant
   - Secondary: GHL contact note

**Deliverable**: Consultation prep assembler working

---

### Friday: Trust Boundary Enforcer + Integration Test

**Tasks**:
1. ⚠️ Build trust boundary enforcer:
   - Detect eligibility questions in transcript → Flag for human review
   - Detect deportation/inadmissibility mentions → Escalate immediately
   - Detect emotional distress → Escalate
   - Log all AI interactions to compliance audit log
2. ⚠️ End-to-end integration test:
   - Submit form in GHL → Webhook received
   - NeuronX triggers voice call → Call executed
   - Voice provider callback → Transcript parsed
   - Readiness scored → GHL fields updated
   - Tag added → GHL workflow triggered (booking invite)
   - Appointment booked → Briefing assembled and delivered
3. ⚠️ Verify compliance log populated

**Deliverable**: NeuronX orchestration layer deployed and wired ✅

---

### Saturday: Week 4 Review

**Checklist**:
- ✅ Webhook receiver deployed and verified
- ✅ Voice orchestrator working (call trigger + outcome processing)
- ✅ Readiness scorer working (R1-R5 extraction + outcome calculation)
- ✅ Consultation prep assembler working (briefing delivery)
- ✅ Trust boundary enforcer active (compliance log populated)
- ✅ End-to-end test passed (form → call → GHL update → briefing)

**Milestone**: M4 — Orchestration Live ✅

---

## Week 5: Pilot Customer Onboarding (Part 1)

### Monday: Identify Pilot Customer

**Criteria**:
- Immigration consulting firm (RCIC or immigration lawyer)
- 100-200 inquiries/month
- 2-10 staff
- Currently using spreadsheets or basic CRM
- Willing to provide testimonial if successful

**Tasks**:
1. ⚠️ Founder identifies 1-3 candidate firms
2. ⚠️ Outreach: "We're launching an AI-assisted intake system for immigration firms. Free trial + white-glove setup. Interested?"
3. ⚠️ Schedule demo call

**Deliverable**: 1 pilot customer committed

---

### Tuesday: Pilot Demo & Agreement

**Tasks**:
1. ⚠️ Demo flow:
   - Show landing page (form submission)
   - Show AI call (role-play)
   - Show GHL pipeline (lead states)
   - Show consultation briefing
   - Show retainer automation
2. ⚠️ Present offer:
   - Free trial: First 30 days (or first 50 leads)
   - Success guarantee: If no improvement in conversion, no charge
   - White-glove setup: We install, configure, train
   - Monthly fee after trial: $1,500/month (lock in price)
3. ⚠️ Sign pilot agreement

**Deliverable**: Pilot agreement signed

---

### Wednesday: Firm Branding & Content

**Tasks**:
1. ⚠️ Collect firm assets:
   - Firm name
   - Logo
   - Brand colors
   - Team photos + RCIC#
   - Testimonials (if any)
   - Programs offered (Express Entry, Spousal, etc.)
2. ⚠️ Customize landing page:
   - Replace "NeuronX Immigration Advisory" with firm name
   - Upload logo
   - Add team section (photos + credentials)
   - List programs offered
   - Add trust signals (CICC badge, success stats)
3. ⚠️ Customize message templates:
   - Replace generic firm name with actual firm name
   - Update signature with firm contact info

**Deliverable**: Firm-branded snapshot ready

---

### Thursday: Sub-Account Creation & Snapshot Install

**Tasks**:
1. ⚠️ Create firm sub-account in GHL Agency
2. ⚠️ Install snapshot
3. ⚠️ Configure voice provider credentials:
   - GHL Voice AI: Configure in sub-account
   - Vapi: Create Vapi sub-account, link API key
4. ⚠️ Configure NeuronX orchestration:
   - Set webhook URLs
   - Set firm location ID
   - Set consultant email for briefings
5. ⚠️ Test end-to-end:
   - Submit form → Verify contact created
   - Trigger test call → Verify outcome processed
   - Book appointment → Verify briefing delivered

**Deliverable**: Firm sub-account live and tested

---

### Friday: Team Training

**Tasks**:
1. ⚠️ Train intake coordinator:
   - How to view work queue
   - How to manually tag leads
   - How to complete readiness assessment for human-handled leads
   - How to book manually if needed
   - How to handle escalations
2. ⚠️ Train consultants:
   - How to receive briefings (email or GHL note)
   - How to record consultation outcome
   - How to send retainer
3. ⚠️ Train firm owner:
   - How to view pipeline dashboard
   - How to review stuck leads
   - How to check daily briefing (pending analytics build)

**Deliverable**: Team trained and confident

---

## Week 6: Pilot Customer Onboarding (Part 2) & Go-Live

### Monday: Final Checks

**Tasks**:
1. ⚠️ Verify all workflows published and active
2. ⚠️ Verify landing page live and accessible
3. ⚠️ Verify form submission → contact creation works
4. ⚠️ Verify voice AI responds within 5 min
5. ⚠️ Verify compliance guardrails active (trust boundary enforcer)

**Deliverable**: Pre-launch checklist complete

---

### Tuesday: Soft Launch (Internal Test)

**Tasks**:
1. ⚠️ Firm submits 2-3 test leads (staff role-play prospects)
2. ⚠️ Monitor end-to-end flow:
   - Form → AI call → Readiness scored → Booking invite → Appointment → Briefing → Outcome → Retainer
3. ⚠️ Fix any issues discovered
4. ⚠️ Verify firm team comfortable with system

**Deliverable**: Soft launch successful

---

### Wednesday: Go-Live

**Tasks**:
1. ⚠️ Point firm's marketing (website, ads, social) to NeuronX landing page
2. ⚠️ Monitor first 5 real leads:
   - Speed-to-contact < 5 min?
   - AI call quality acceptable?
   - Readiness data captured correctly?
   - Booking flow working?
3. ⚠️ Standby for issues
4. ⚠️ Collect feedback from firm team

**Deliverable**: System live with real leads

---

### Thursday: First Consultation

**Tasks**:
1. ⚠️ Monitor first consultation:
   - Was briefing delivered?
   - Did consultant read briefing?
   - Was consultation outcome recorded?
2. ⚠️ If outcome = "Proceed":
   - Verify retainer email sent within 1 hour
   - Verify follow-up sequence initiated
3. ⚠️ Collect consultant feedback

**Deliverable**: First consultation completed via NeuronX

---

### Friday: First Retainer

**Tasks**:
1. ⚠️ Monitor retainer follow-up sequence:
   - Day 0: Retainer + checklist sent?
   - Day 1: Check-in SMS sent?
   - Day 2: Follow-up sent?
2. ⚠️ If retainer signed:
   - 🎉 **FIRST RETAINER VIA NEURONX** 🎉
   - Verify payment received
   - Update pipeline to RETAINED
3. ⚠️ Collect firm owner feedback
4. ⚠️ Request testimonial

**Deliverable**: First retainer signed ✅

---

### Saturday: Week 6 Review & Case Study

**Checklist**:
- ✅ Pilot customer onboarded
- ✅ System live and processing real leads
- ✅ First consultation booked via NeuronX
- ✅ First retainer signed via NeuronX
- ✅ Testimonial captured
- ✅ Case study written

**Milestone**: M5 — Pilot Deployed ✅

**Case Study Structure**:
1. **Firm Profile**: [Firm name], [X] staff, [X] inquiries/month
2. **Challenge**: Slow response, inconsistent follow-up, unprepared consultations
3. **Solution**: NeuronX AI-assisted intake + GHL automation
4. **Results**:
   - Speed-to-contact: [X] minutes (before) → < 5 min (after)
   - Booking rate: [X]% (before) → [Y]% (after)
   - Consultation show rate: [X]% (before) → [Y]% (after)
   - Consult-to-retained rate: [X]% (before) → [Y]% (after)
5. **Testimonial**: "[Quote from firm owner]"

---

## Success Metrics

### Week 1 Metrics
- ✅ 11 workflows configured
- ✅ 4 UAT scenarios passed
- ✅ 0 trust boundary violations

### Week 2 Metrics
- ✅ Snapshot created
- ✅ Snapshot installed < 30 min
- ✅ UAT re-passed in snapshot tenant

### Week 3 Metrics
- ✅ Voice layer locked
- ✅ Bake-off avg score ≥ 4.0
- ✅ Trust boundary safety = 5/5
- ✅ Webhook security validated

### Week 4 Metrics
- ✅ End-to-end test passed
- ✅ Compliance log populated
- ✅ Briefing delivered successfully

### Week 5-6 Metrics
- ✅ Pilot customer signed
- ✅ System live
- ✅ First AI call < 5 min
- ✅ First consultation briefing delivered
- ✅ First retainer signed via NeuronX
- ✅ $18K ARR locked in

---

## Post-Week 6: Scale Path

### Month 2: Refine + 2 More Pilots
- Iterate on pilot feedback
- Fix bugs discovered in production
- Onboard 2 more pilot customers
- Target: 3 customers @ $4,500/month = $54K ARR

### Month 3: Productize Onboarding
- Document repeatable onboarding process
- Build onboarding checklist
- Create training videos
- Target: 3 more customers (6 total) = $108K ARR

### Month 6: Build Sales Pipeline
- Hire BD/sales part-time
- Create NeuronX marketing site
- Run webinars for immigration firms
- Target: 10 customers = $180K ARR

### Month 12: Scale to 30 Customers
- Hire implementation specialist
- Hire support engineer
- Refine product based on 10-customer feedback
- Target: 30 customers = $540K ARR

### Month 18: Reach $1M ARR
- 50 customers @ $1,500/month avg
- Expand to US immigration firms (if Canadian market validated)
- Target: $900K ARR (round to $1M with upsells)

---

## Risk Mitigation Checklist

### Week 1 Risks
- ⚠️ Skyvern session expires → Save after each workflow
- ⚠️ Workflow persistence fails → Verify immediately after publish

### Week 2 Risks
- ⚠️ Snapshot missing assets → Checklist before creation
- ⚠️ Snapshot install fails → Manual install is acceptable

### Week 3 Risks
- ⚠️ Both voice options fail bake-off → Defer AI calling to v1.1, ship human-only
- ⚠️ Webhook security fails → Block v1 launch until fixed

### Week 4 Risks
- ⚠️ Integration bugs → Allocate 2 buffer days
- ⚠️ Voice provider downtime → Fallback to human queue

### Week 5-6 Risks
- ⚠️ Pilot customer backs out → Have 2-3 candidates ready
- ⚠️ System breaks in production → 24/7 monitoring week 1

---

## Founder Checkpoints

### Week 1
- **Day 1**: Log into Skyvern session (30 min)
- **Day 7**: Review UAT report (1 hour)

### Week 2
- **Day 3**: Review snapshot install time (30 min)

### Week 3
- **Day 4**: Approve voice layer decision (1 hour)

### Week 4
- **Day 5**: Review end-to-end test (1 hour)

### Week 5
- **Day 1**: Identify pilot customer (2 hours)
- **Day 2**: Demo call (1 hour)

### Week 6
- **Day 3**: Go-live monitoring (2 hours)
- **Day 5**: Review first retainer (1 hour)

**Total Founder Time**: ~10 hours over 6 weeks

---

## Conclusion

This 6-week roadmap is **achievable** if:
1. Skyvern workflow configuration resumes (requires founder login)
2. Voice bake-off executed on schedule
3. Pilot customer identified and committed
4. No major technical blockers

**The path to $1M ARR is clear. The only variable is execution speed.**

Next immediate action: **Log into Skyvern session to unblock Week 1.**
