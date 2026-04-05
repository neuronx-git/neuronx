# NeuronX Human-in-Loop AI Architecture

## Principle
AI augments human consultants. AI handles speed, consistency, and data capture. Humans handle immigration advice, eligibility assessment, and licensed judgment.

---

## Architecture Overview

```
Lead Submit (Form)
    ↓
GHL WF-01 (Instant Ack)
    ↓
AI Call (60 seconds) ← **NeuronX AI Layer**
    ↓
Readiness Data → GHL Custom Fields
    ↓
AI Decision:
  - Simple/Ready → Auto-book calendar
  - Complex → Human Escalation
  - Uncertain → Human Escalation
    ↓
Human Consultant (Consultation)
    ↓
Outcome → GHL Field Update
    ↓
AI Follow-Up (Retainer Sequences)
```

---

## 1. AI Inbound Call Flow

### Trigger
- **GHL Workflow**: WF-01 fires → Webhook to NeuronX AI service → AI calls lead within 60s.

### AI Script (Immigration-Specific)
```
AI: "Hi [First Name], this is Alex from [Firm Name]. I'm calling because you just inquired about Canadian immigration. Do you have 2 minutes?"

[If Yes]
AI: "Great. I'd like to ask a few quick questions to understand your situation and connect you with the right consultant."

Q1: "Which immigration program are you most interested in? Express Entry, Study Permit, Work Permit, or Family Sponsorship?"
→ Store in GHL Field: `program_interest`

Q2: "Are you currently in Canada or outside Canada?"
→ Store in GHL Field: `current_location`

Q3: "What's your timeline? Are you looking to move within 3 months, 6 months, or is this longer-term planning?"
→ Store in GHL Field: `timeline_urgency`

Q4: "Have you ever applied for Canadian immigration before?"
→ Store in GHL Field: `prior_applications`

[End]
AI: "Perfect. Based on what you've shared, I'm going to connect you with one of our licensed consultants. You can book a time that works for you at [calendar link]. I'll also send that link via SMS right now. Does that work?"

[If Yes]
AI: "Great. You'll receive the SMS in the next minute. Looking forward to helping you with your Canadian immigration journey. Have a great day!"

[End Call → Update GHL]
- Add Tag: `nx:contacted`
- Add Tag: `nx:assessment:required`
- Send SMS with booking link (via GHL WF-04)
```

### Human Escalation Triggers (During AI Call)
1. **Explicit Request**: "I want to speak to a person."
2. **Complexity Signals**: Keywords like "refusal", "inadmissibility", "deportation", "criminal record".
3. **AI Uncertainty**: Sentiment analysis detects frustration or confusion.
4. **High Value**: Detects "urgent" + "premium service" in conversation.

**Escalation Action**:
- AI: "I understand. Let me transfer you to one of our consultants right now."
- GHL Action: Create Task "URGENT: Transfer call to consultant".
- Fallback: If no one available, AI: "Our team is currently with other clients. I'll have a consultant call you back within the next 30 minutes. Can I confirm your phone number is [phone]?"

---

## 2. AI Outbound Call Flow

### Trigger
- **GHL Workflow**: WF-02 fires after 30 minutes of no contact → Webhook to NeuronX AI → AI calls lead.

### AI Script (Follow-Up)
```
AI: "Hi [First Name], this is Alex from [Firm Name]. We tried reaching you earlier about your immigration inquiry. Is now a good time for a quick call?"

[If Yes]
AI: "Great. I'd like to help you book a consultation with one of our licensed consultants. Have you had a chance to review the booking link we sent?"

[If No]
AI: "No problem. I can send it again right now. Or I can help you book a time over the phone. Which works better for you?"

[If Book Now]
AI: "Perfect. What day this week works best for you? We have availability on [list next 3 days]."
→ Use GHL Calendar API to check availability.
→ Book appointment.
→ Confirm via SMS.

[End Call]
```

---

## 3. Lead Scoring System

### Readiness Score (GHL-Compatible)
Store in GHL Custom Field: `readiness_score` (Number, 0-100).

**Calculation** (AI computes, writes to GHL):
- Program Interest Clarity: +20
- Location Known: +15
- Timeline Defined: +15
- Prior Application Mentioned: +10
- Budget Awareness: +15
- Engagement (call answered, responded to SMS): +15
- Urgency Keywords: +10

**Thresholds**:
- **80-100**: Ready (Auto-book)
- **50-79**: Follow-up (Human touch recommended)
- **0-49**: Nurture (Long-term sequence)

### Human Escalation Score
Store in GHL Field: `escalation_priority` (Dropdown: Low, Medium, High, URGENT).

**Triggers**:
- **URGENT**: Refusal keywords, inadmissibility, explicit high-value signals.
- **High**: Complex program (PNP), multiple refusals, tight timeline.
- **Medium**: Standard inquiries, no red flags.
- **Low**: Just exploring, 12+ month timeline.

---

## 4. Persistent Memory (GHL Data Structures)

### Custom Fields (AI Writes, GHL Stores)
- `ai_call_attempted`: Checkbox
- `ai_call_connected`: Checkbox
- `ai_call_transcript_summary`: Long Text (max 500 chars)
- `ai_detected_complexity_flags`: Multi-Select (Refusal, Inadmissibility, Minor, etc.)
- `readiness_score`: Number
- `escalation_priority`: Dropdown

### Tags (AI Adds, GHL Triggers Workflows)
- `nx:ai_call:success`
- `nx:ai_call:no_answer`
- `nx:ai_escalation:complex`
- `nx:ai_escalation:urgent`

### Notes (AI Appends)
- AI writes call summary to GHL Contact Notes.
- Example: "AI Call Summary: Lead interested in Express Entry. Currently in India. Timeline: 6 months. No prior applications. Booked consultation for Mar 20 at 2pm."

---

## 5. Consultation Briefing Generation

### Trigger
- **GHL Workflow**: 30 minutes before appointment → Webhook to NeuronX AI.

### AI Task
1. Pull from GHL API:
   - Contact Name, Email, Phone
   - Program Interest, Location, Timeline
   - Prior Applications
   - All Notes, Tags, Conversation History
2. Generate Briefing (Markdown format):

```markdown
# Consultation Briefing: [Name]

**Date**: [Appointment Date/Time]
**Consultant**: [Assigned Consultant]

## Lead Overview
- **Program Interest**: Express Entry
- **Current Location**: India
- **Timeline**: 3-6 months
- **Prior Applications**: No

## Key Context
- Inquiry Date: Mar 15, 2026
- First Contact: Mar 15 (AI call, 2min)
- Engagement: High (responded to SMS, booked within 24h)

## AI Call Summary
"Lead is a software engineer in India. CRS score unknown. Interested in Federal Skilled Worker stream. No prior refusals. Budget-aware (asked about fees). Timeline driven by job offer expiry."

## Recommended Focus
- Assess CRS score
- Discuss FSW vs CEC pathways
- Clarify job offer validity

## Red Flags
None.
```

3. Email briefing to consultant (GHL Email action).
4. Append briefing to GHL Contact Notes.

---

## 6. Human Escalation Triggers (Comprehensive)

| Trigger Type | Condition | GHL Action | AI Action |
|:---|:---|:---|:---|
| **Complexity** | Keywords: refusal, inadmissibility, criminal, minor | Add Tag `nx:ai_escalation:complex` → Create Task "Review before booking" | Transfer call OR Flag for manual outreach |
| **High Value** | Keywords: urgent + premium, corporate sponsorship, family of 5+ | Add Tag `nx:ai_escalation:urgent` → Notify owner | Prioritize human callback |
| **AI Uncertainty** | Sentiment < 50%, multiple "I don't know" responses | Add Tag `nx:ai_call:uncertain` → Create Task | End call gracefully, request human callback |
| **Explicit Request** | "I want to speak to a person" | Create Task "Transfer NOW" | Transfer OR schedule immediate callback |
| **No Answer (3x)** | AI calls 3 times, no pickup | Move to UNREACHABLE stage | Stop AI calling, enter WF-02 (human sequence) |

---

## 7. Technology Stack (Proposed)

### AI Voice Provider (Options)
- **GHL Native Voice AI** (if available): Use natively, no external integration.
- **External** (Vapi, Bland, Retell): Webhook integration.

### NeuronX Orchestration Layer (Minimal)
- **Purpose**: Webhook receiver, AI call trigger, GHL API writer.
- **Tech**: Node.js + Express (stateless where possible).
- **Deploy**: Railway, Render, Fly.io.
- **Data Store**: Minimal (call transcripts, audit log). GHL is system of record.

### GHL Integration Points
- **Inbound Webhooks**: Form submit, appointment booked, field change.
- **Outbound API**: Update contact fields, add tags, create notes, book appointments.

---

## 8. Revenue Impact Projections

| Metric | Before AI | After AI | Lift |
|:---|:---|:---|:---|
| **Speed-to-First-Contact** | 4 hours (manual) | 60 seconds (AI) | **240x faster** |
| **Contact Rate** | 40% (manual) | 75% (AI) | **+87.5%** |
| **Booking Rate** | 25% (manual) | 45% (AI + booking assist) | **+80%** |
| **Overall Conversion** | 8% (manual) | 15% (AI-augmented) | **+87.5%** |

**ROI Example**:
- 100 inquiries/month
- Before: 8 retainers ($20K revenue)
- After: 15 retainers ($37.5K revenue)
- **Lift**: +$17.5K/month = **$210K/year**

---

## Final Note
This architecture treats GHL as the operating system and AI as a speed/consistency enhancer. Humans remain in control of all immigration advice and eligibility decisions, ensuring regulatory compliance.
