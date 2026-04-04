# NeuronX Sales Scripts — Complete Call Guide

**Purpose**: Every call type has a script. Staff never improvise on compliance-critical topics.
**Delivery**: GHL Custom Menu page (staff-only) + printed quick-reference cards.
**Rule**: AI (VAPI) uses the AI scripts. Humans use the human scripts. Never cross them.

---

## Script 1: INBOUND INQUIRY CALL (Receptionist / Intake Coordinator)

**When**: New prospect calls the firm directly (before AI assessment).
**Goal**: Capture info, book consultation, warm handoff.
**Duration**: 3-5 minutes.

### Opening
```
"Good [morning/afternoon], thank you for calling [Firm Name].
This is [Your Name], how can I help you today?"
```

### If they describe their immigration need:
```
"Thank you for sharing that. We work with many clients on [their program type].

Let me ask a few quick questions so I can connect you with the right consultant:

1. What immigration program are you interested in?
   [Express Entry / Spousal / Work Permit / Study / LMIA / PR Renewal / Citizenship / Visitor]

2. Are you currently in Canada or outside Canada?

3. Is there a timeline or deadline you're working with?
   [Urgent <30 days / 1-3 months / 3-6 months / No rush]

4. Have you applied to Immigration Canada before?
   [No / Yes-Approved / Yes-Refused / Complex situation]
```

### Booking the consultation:
```
"Based on what you've shared, I'd recommend booking a consultation with one of
our licensed consultants. They can review your specific situation and give you
a clear assessment.

Our consultations are [fee]. They typically run 30-45 minutes.

I have availability [offer 2-3 times]. Which works best for you?"
```

### If they ask about eligibility:
```
"That's a great question, and it's exactly what our consultants assess
during the consultation. I'm not able to give eligibility advice, but I can
tell you that our RCICs handle [program type] cases regularly.

Would you like to book a time to discuss your specific situation?"
```
**COMPLIANCE**: Never say "you're eligible", "you'll get approved", or "you qualify".

### If they ask about price:
```
"Our consultation fee is [amount]. Professional fees for the full case
depend on the complexity — your consultant will discuss that during
the consultation.

Many clients find the consultation alone gives them clarity on their
options and next steps."
```

### Closing:
```
"Great, I've booked you for [date] at [time] with [Consultant Name].

You'll receive a confirmation email and text message shortly with all the
details. If you need to reschedule, just reply to the text.

Is there anything else I can help with? ... Thank you for calling [Firm].
We look forward to speaking with you!"
```

---

## Script 2: AI OUTBOUND CALL (VAPI Agent — First Contact)

**When**: 2-5 minutes after form submission. VAPI calls automatically.
**Goal**: Confirm inquiry, collect R1-R5, offer booking.
**Duration**: 3-5 minutes.
**Compliance**: AI MUST NOT assess eligibility, recommend pathways, or promise outcomes.

### VAPI System Prompt (Already configured)
```
You are a professional intake assistant for [Firm Name], a licensed Canadian
immigration consulting firm. You are calling to follow up on an immigration
inquiry that was just submitted.

Your job:
1. Confirm the person submitted the inquiry
2. Collect 5 readiness dimensions (program interest, location, timeline,
   prior applications, budget awareness)
3. Offer to book a consultation
4. Be warm, professional, concise

You MUST NOT:
- Assess eligibility for any program
- Recommend immigration pathways
- Interpret immigration law
- Promise outcomes or processing times
- Claim to be a licensed consultant

If asked about eligibility, say: "That's exactly what our licensed consultants
assess during the consultation. Shall I book you in?"

If the person seems distressed, emotional, or mentions deportation/removal,
say: "I understand this is important. Let me connect you with a team member
who can help right away." Then trigger transfer_to_human function.
```

### VAPI Structured Data Extraction (analysisPlan)
```json
{
  "structuredDataPlan": {
    "schema": {
      "type": "object",
      "properties": {
        "program_interest": { "type": "string", "description": "Immigration program: Express Entry, Spousal, Work Permit, Study Permit, LMIA, PR Renewal, Citizenship, Visitor, Other" },
        "current_location": { "type": "string", "description": "In Canada or Outside Canada" },
        "timeline_urgency": { "type": "string", "description": "Urgent (<30 days), Near-term (1-3 months), Medium (3-6 months), Long-term (6+ months)" },
        "prior_applications": { "type": "string", "description": "None, Approved, Has Refusal, Complex" },
        "budget_awareness": { "type": "string", "description": "Aware, Unaware, Unclear" },
        "booking_interest": { "type": "boolean", "description": "Did the prospect agree to book a consultation?" },
        "escalation_needed": { "type": "boolean", "description": "Does the prospect need immediate human contact?" }
      }
    }
  }
}
```

---

## Script 3: FOLLOW-UP CALL (Human — After AI Assessment)

**When**: Contact scored medium (40-69) or form-only scored. Human follows up.
**Goal**: Complete assessment, address concerns, book consultation.
**Duration**: 5-10 minutes.

### Opening
```
"Hi [Name], this is [Your Name] from [Firm Name]. I'm following up on your
immigration inquiry — you reached out about [program interest].

I wanted to connect personally to understand your situation better and
see how we can help. Do you have a few minutes?"
```

### If they already spoke with AI:
```
"I see you spoke with our intake team earlier. I have some notes here —
you're interested in [program] and you're currently [location].

I just wanted to fill in a couple more details so we can prepare
properly for your consultation."
```

### Discovery Questions (Complete R4-R5 if missing):
```
"Have you applied to Immigration Canada before?
... [if yes] How did that go?"

"Our consultations are [fee], and professional fees vary by case complexity.
Is that something you've thought about?"
```

### Addressing Hesitation:
```
If "I'm not sure I need a consultant":
"That's fair. Many of our clients felt the same way initially. What they found
is that a 30-minute consultation saved them months of uncertainty. Our RCICs
see patterns in cases like yours every day — they can tell you exactly where
you stand and what your options are."

If "I'm shopping around":
"Absolutely, you should. When you're comparing, here's what I'd suggest
looking for: are they licensed RCICs? Do they have a structured intake
process? Do they prepare a briefing before your consultation?
We do all three. That said, you'll know best who feels like the right fit."

If "I need to talk to my spouse/family":
"Of course. When do you think you'll have a chance to discuss?
I can hold a time slot for you — no commitment until you confirm."
```

### Closing:
```
"Based on what you've shared, [Consultant Name] would be a great fit
for your consultation. They handle [program type] cases regularly.

I have [date/time] available. Shall I book that for you?"
```

---

## Script 4: PRE-CONSULTATION CALL (RCIC — Optional 5-min Warm-Up)

**When**: 5 minutes before consultation. Quick call to set tone.
**Goal**: Build rapport before formal consultation.

```
"Hi [Name], it's [Consultant Name] from [Firm]. I just wanted to say
hello before our consultation at [time].

I've reviewed your intake information — I see you're looking at
[program] from [location]. I have a few questions prepared, but I
also want to make sure we cover what's most important to you.

Is there anything specific you're hoping we'll address today?"
```

---

## Script 5: CONSULTATION — 5-PHASE GUIDE (RCIC)

**Duration**: 30-45 minutes. Delivered via pre-consultation briefing (already built in FastAPI).

### Phase 1: Opening (3 min)
```
"[Name], thank you for joining today. I'm [Name], a Regulated Canadian
Immigration Consultant — my license number is R[number].

I've reviewed your inquiry and our intake notes. You're interested in
[program interest], you're currently [in/outside Canada], and your
timeline is [urgency]. Is that correct?

Here's how I'd like to structure our time today:
1. I'll ask some detailed questions to understand your full picture
2. I'll share my assessment of your options
3. We'll discuss fees and next steps

Sound good? Let's start."
```

### Phase 2: Discovery (10-15 min)
**Express Entry specific questions:**
- Age, education level, language scores (IELTS/TEF)?
- Years of Canadian/foreign work experience?
- Do you have a provincial nomination or job offer?
- Current CRS score estimate?

**Spousal specific questions:**
- How long have you been in the relationship?
- Do you live together? Since when?
- Is the sponsor a citizen or PR?
- Any previous sponsorship applications?

**Work Permit specific questions:**
- Do you have a job offer from a Canadian employer?
- What is the NOC code for the position?
- Has the employer started an LMIA?
- Current immigration status?

### Phase 3: Assessment (5-7 min)
```
"Based on everything you've shared, here's my assessment:

[Program-specific analysis]

Your case has [strong / some / challenging] elements.
[Specific strengths and concerns].

I want to be transparent — I can't guarantee any outcome.
What I can tell you is [honest assessment of viability]."
```

**COMPLIANCE**: Never say "guaranteed", "you will be approved", or "100% chance."
**SAY INSTEAD**: "strong case", "well-positioned", "areas that need attention."

### Phase 4: Offer & Pricing (5-7 min)
```
"If you'd like to proceed, here's what our engagement includes:

[Scope of services — specific to program]
- Document preparation and review
- Form completion and submission
- Correspondence with IRCC
- Status monitoring until decision

Our professional fee for [program] is $[amount].
Payment is [terms — e.g., 50% upfront, 50% at submission].

Do you have any questions about the scope or fees?"
```

**If "too expensive":**
```
"I understand. Let me put it in context — this fee covers [X hours]
of professional work, including [specifics]. Many clients find that
the cost of mistakes on a self-filed application — delays, refusals,
reapplication fees — far exceeds the professional fee.

We also offer [payment plan option if available]."
```

### Phase 5: Close (3-5 min)

**If proceeding:**
```
"Excellent. Here's what happens next:
1. Within the hour, you'll receive a retainer agreement via email
2. Review and sign it digitally
3. Once signed and payment is received, we assign your case to [RCIC]
4. You'll receive a detailed document checklist
5. We target [timeline] for submission

Any last questions? ... Great, thank you [Name]. We're excited to
work on your case."
```

**If needs to think:**
```
"Absolutely, take your time. I'll send you a summary of what we
discussed today so you have it in writing.

When do you think you'll have a decision? ... I'll follow up
[date] if I haven't heard from you. Sound fair?"
```

**If not proceeding:**
```
"I understand, and I appreciate your time today. May I ask what's
behind your decision? [Listen — don't argue]

If anything changes, we're here. I'll make sure your file stays
on record so you won't have to start from scratch."
```

---

## Script 6: RETAINER CLOSING CALL (RCIC or Coordinator)

**When**: Retainer sent but unsigned after 3+ days.
**Goal**: Address concerns, close the deal.

```
"Hi [Name], it's [Name] from [Firm]. I'm following up on the retainer
agreement we sent on [date].

I wanted to check — did you have a chance to review it?

... [Listen for objections]
```

**Common objections:**

| Objection | Response |
|-----------|----------|
| "Still thinking" | "What specifically are you weighing? I'm happy to clarify anything." |
| "Price is high" | "I understand. What we've quoted includes [full scope]. Many clients find the retainer pays for itself in avoided delays and errors." |
| "Comparing with others" | "That's smart. When comparing, check: are they licensed? What's included in the fee? Is there a document prep guarantee? We include all of that." |
| "Timing isn't right" | "When would be better? Keep in mind that [program-specific urgency — CRS draws, processing times, policy changes]." |
| "Spouse disagrees" | "Would it help if I set up a brief 15-minute call with both of you? Sometimes hearing it directly helps." |
| "Had a bad experience before" | "I'm sorry to hear that. Can you share what happened? We specifically structure our process to avoid [their concern]." |

### Final close:
```
"Here's what I can do — if you sign today, I'll [specific incentive
if applicable, e.g., prioritize your case for this month's submission
window / include one free status check call].

Shall I resend the agreement?"
```

---

## Script 7: REFERRAL ASK (Post-Case Closure)

**When**: 30 days after case closed with positive outcome.
**Channel**: Email + SMS.

### Email
```
Subject: Quick Favor, [Name]?

Hi [Name],

I hope everything is going well since [your PR was approved / you
arrived in Canada / your work permit came through].

I have a quick ask — do you know anyone who's going through the
immigration process right now? A friend, family member, or colleague
who might benefit from the same structured approach we used for
your case?

If so, just reply with their name and I'll reach out personally.
No pressure — just thought I'd ask.

[Consultant Name]
[Firm Name]
```

### SMS
```
Hi [Name], hope things are going well! Quick question — do you know
anyone going through the immigration process? Would love to help them
the same way we helped you. Just share their name if so! — [Name], [Firm]
```

---

## Compliance Reminders (Every Script)

| Rule | What to Say | What NEVER to Say |
|------|-------------|-------------------|
| Eligibility | "That's what our consultants assess" | "You're eligible" |
| Outcomes | "Strong case" / "Well-positioned" | "Guaranteed" / "Will be approved" |
| Timelines | "Current average processing is X" | "You'll get it by [date]" |
| Legal advice | "Our RCIC will review your options" | "The law says you should..." |
| Credentials | "Licensed RCIC #R[number]" | "I'm an immigration lawyer" (unless true) |
| Emotional | "I understand, let me connect you with..." | Continuing the script |
