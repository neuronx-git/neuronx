# NeuronX Sales Workflows — Email & SMS Content (Block 2D)

**Purpose**: Workflows for selling NeuronX to immigration firms (NX-WF-01→06)
**Status**: Content ready. Build workflows in production GHL account (post-sandbox).
**Pipeline**: NeuronX Sales Pipeline (create in production account)

---

## NX-WF-01: New Firm Lead Alert

**Trigger**: Contact created in NeuronX sales pipeline
**Action**: Internal alert to founder

### Internal Email (to founder)
**Subject**: New NeuronX Lead — {{contact.full_name}} from {{contact.company}}
**Body**:
```
New immigration firm lead:

Name: {{contact.full_name}}
Firm: {{contact.company}}
Email: {{contact.email}}
Phone: {{contact.phone}}
Source: {{contact.source}}
Submitted: {{contact.date_created}}

Action: Review and respond within 2 hours.
```

---

## NX-WF-02: Demo Booked Confirmation

**Trigger**: Calendar booking on NeuronX Demo calendar
**Action**: Confirmation + prep to prospect

### Email
**Subject**: Your NeuronX Demo is Confirmed — {{appointment.date}}
**From**: ranjan@neuronx.co
**Body**:
```
Hi {{contact.first_name}},

Your NeuronX product demo is confirmed:

Date: {{appointment.date}}
Time: {{appointment.time}} ET
Duration: 30 minutes
Link: {{appointment.meeting_link}}

What to expect:
- Live walkthrough of the AI intake system
- How NeuronX handles leads from inquiry to retainer
- Your firm's specific use case and configuration options
- Pricing and onboarding timeline

No preparation needed on your end — just bring your questions.

Looking forward to speaking with you,
Ranjan Singh
Founder, NeuronX
```

### SMS
```
Hi {{contact.first_name}}, your NeuronX demo is confirmed for {{appointment.date}} at {{appointment.time}} ET. Meeting link: {{appointment.meeting_link}} — Ranjan, NeuronX
```

---

## NX-WF-03: Demo Follow-Up Sequence

**Trigger**: Tag `nx:demo:completed`
**Action**: 3-email follow-up over 7 days

### Email 1 (Immediate)
**Subject**: Thanks for Exploring NeuronX, {{contact.first_name}}
```
Hi {{contact.first_name}},

Thanks for taking the time to see NeuronX in action today.

As we discussed, NeuronX automates the inquiry-to-retainer funnel for immigration firms:

1. AI answers within 5 minutes of every inquiry
2. Structured readiness assessment — no manual qualification
3. Automated consultation booking and reminders
4. Pre-consultation briefing delivered to your RCIC
5. Retainer follow-up until signed or nurtured

I've attached a brief one-pager summarizing what we covered.

If you have questions or want to start your 14-day trial, just reply to this email.

Best,
Ranjan
```

### Email 2 (Day 3)
**Subject**: How {{contact.company}} Could Save 10+ Hours/Week
```
Hi {{contact.first_name}},

Quick follow-up from our demo. Most firms we work with tell us their intake coordinator spends 10-15 hours per week on:

- Calling back new inquiries (often too late — they've moved on)
- Manually assessing if prospects are consultation-ready
- Chasing no-shows and rescheduling
- Following up on unsigned retainers

NeuronX automates all four. Your RCIC walks into every consultation prepared — briefing on their desk, prospect pre-qualified.

Ready to see it with your own leads? Start a 14-day trial — zero commitment.

Ranjan
```

### Email 3 (Day 7)
**Subject**: Last Thought — NeuronX for {{contact.company}}
```
Hi {{contact.first_name}},

I wanted to share one last thought before moving on.

The firms seeing the biggest impact with NeuronX have one thing in common: they were losing qualified prospects between inquiry and first contact. The average immigration firm takes 48+ hours to respond — by then, the prospect has contacted 3 other firms.

NeuronX responds in under 5 minutes. That alone changes the game.

If the timing isn't right, no worries at all. I'll check back in a month. But if you want to start — reply "GO" and I'll set up your account today.

Ranjan
```

---

## NX-WF-04: Trial Started — Onboarding Drip

**Trigger**: Tag `nx:trial:started`
**Action**: 5 emails over 14 days

### Email 1 (Day 0)
**Subject**: Welcome to NeuronX — Let's Get You Set Up
```
Hi {{contact.first_name}},

Welcome aboard! Your NeuronX trial is active.

Here's what happens next:

1. TODAY: I'll send you a calendar link to schedule your 30-min setup call
2. SETUP CALL: We'll configure your pipeline, calendar, and AI voice agent together
3. DAY 2-3: Your first test leads flow through the system
4. DAY 7: Check-in call to review performance and adjust
5. DAY 14: Decision time — continue or cancel, no pressure

Your setup call link: [BOOKING_LINK]

Let's make this the easiest part of your week.

Ranjan
```

### Email 2 (Day 3)
**Subject**: Your First Leads Are Flowing — Here's What to Watch
```
Quick note: by now your NeuronX system should have processed its first few test leads.

Check your pipeline dashboard. You should see:
- Leads auto-categorized by readiness (High / Medium / Low)
- AI call recordings with transcripts
- Upcoming consultations pre-briefed

If anything looks off, reply to this email. I'll jump in and fix it same-day.
```

### Email 3 (Day 7)
**Subject**: Week 1 Check-In — How's NeuronX Working?
```
Hi {{contact.first_name}},

It's been a week since you started your NeuronX trial. Time for a quick check-in.

By now you should have seen:
- AI responding to inquiries within minutes
- Prospects booked into your calendar automatically
- Pre-consultation briefings delivered before each meeting

I'd love to hop on a 15-minute call to review your first week. Book here: [BOOKING_LINK]

If everything is running smoothly and you'd like to continue, just reply "KEEP" and I'll activate your subscription.
```

### Email 4 (Day 10)
**Subject**: 4 Days Left on Your Trial
```
Hi {{contact.first_name}},

Your NeuronX trial wraps up in 4 days. Here's a quick summary of your trial performance:

[METRICS PLACEHOLDER — to be auto-populated by NeuronX API]
- Leads processed: X
- Consultations booked: X
- Average response time: X minutes

Ready to keep going? Reply "YES" and I'll activate your subscription.

Have questions? Reply here — I respond personally.

Ranjan
```

### Email 5 (Day 14)
**Subject**: Your NeuronX Trial Has Ended
```
Hi {{contact.first_name}},

Your 14-day trial has ended. Your system is now paused — no data is lost.

Two options:
1. ACTIVATE: Reply "GO" → I'll activate your plan within the hour
2. PAUSE: No action needed → system stays paused, your config is saved for 30 days

Either way, your pipeline configuration, custom fields, and AI training are preserved.

Thanks for giving NeuronX a try.

Ranjan
```

---

## NX-WF-05: Trial → Paid Conversion

**Trigger**: Tag `nx:converted`
**Action**: Welcome + setup call

### Email
**Subject**: You're Live on NeuronX — Welcome, {{contact.first_name}}!
```
Hi {{contact.first_name}},

Your NeuronX subscription is now active. Welcome to the family.

Your plan: {{contact.plan_name}}
Billing: Monthly via Stripe
Support: Direct access to me — ranjan@neuronx.co

What's next:
- Your system is already live and processing leads
- If you have team members to add, reply with their emails
- Your first invoice will arrive in 30 days

If you ever need anything — reply to this email. I'm your direct line.

Here's to more signed retainers,
Ranjan
```

### SMS
```
{{contact.first_name}}, you're officially live on NeuronX! Your AI intake system is active and ready. Questions? Text me anytime. — Ranjan
```

---

## NX-WF-06: Churned / Lost — Win-Back Sequence

**Trigger**: Tag `nx:churned`
**Action**: Monthly win-back for 3 months

### Email 1 (Month 1)
**Subject**: We Miss You, {{contact.first_name}} — What Can We Improve?
```
Hi {{contact.first_name}},

I noticed you decided not to continue with NeuronX. No hard feelings — I'd genuinely appreciate understanding what didn't work for you.

Was it:
- Pricing? (We have flexible plans)
- Features? (We ship updates weekly)
- Timing? (Your config is saved — pick up anytime)
- Something else?

Just reply with a sentence or two. It helps us get better.

Ranjan
```

### Email 2 (Month 2)
**Subject**: NeuronX Update — New Features Since You Left
```
Hi {{contact.first_name}},

A quick update on what's new at NeuronX since we last spoke:

[CHANGELOG PLACEHOLDER — update monthly with real features]

If any of these address what held you back, I'd love to give you another look — 7-day free trial, no credit card.

Ranjan
```

### Email 3 (Month 3 — Final)
**Subject**: Final Check-In — Is NeuronX Right for {{contact.company}}?
```
Hi {{contact.first_name}},

This is my last follow-up. If NeuronX isn't the right fit, I respect that completely.

But if there's ever a day when you're drowning in unqualified leads, missed follow-ups, or manual intake work — we'll be here. Your saved configuration means you can go live in under an hour.

Wishing you and {{contact.company}} all the best.

Ranjan
```
