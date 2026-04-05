# AI Messaging Automation Architecture

## Objective
Enhance GoHighLevel's native messaging capabilities with AI to provide highly contextual, program-specific responses without requiring human intervention for routine follow-ups.

## Guiding Principles
1. **Never Give Legal Advice**: AI-generated SMS/Email must strictly focus on scheduling, administrative updates, or generic program information.
2. **Human Override**: A human consultant can pause or override AI messaging at any time.
3. **Configuration First**: Use GHL's native Custom Values and Workflow logic. Only use LLM APIs for dynamic content generation when strict branching fails.

---

## 1. AI-Assisted SMS Responses (Conversational AI)

### Implementation Path: GHL Native Conversation AI (with strict training)
While GHL Native Voice AI was rejected for the initial outbound call, GHL's **Conversation AI (SMS/Webchat)** is acceptable for basic text-based Q&A if strictly constrained.

**Configuration Details:**
- **Mode**: "Suggest" mode initially (Intake coordinator approves responses). Transition to "Autopilot" after 30 days of training.
- **Goal**: Booking the consultation.
- **Training Data**: 
  - Firm pricing ($150 consultation fee).
  - Office hours (9 AM - 5 PM EST).
  - Program list (Express Entry, Study, Work, Family).
  - *Constraint*: "If asked about eligibility, say: 'I cannot assess your eligibility via text. Our licensed consultants will review your specific case during a strategy session.'"

---

## 2. Dynamic Email Follow-Ups (Contextual Nurture)

Instead of generic "Are you still interested?" emails, we use the `ai_program_interest` field to trigger hyper-relevant nurture emails.

### Workflow: `WF-11A — AI Nurture Branching`

**Trigger**: Lead enters `NURTURE` stage.

**Branch 1: Express Entry / PR**
- **Email Content**: Focus on CRS score factors, upcoming draw trends, and the importance of having documents ready.
- **Subject**: "How to maximize your Express Entry CRS score"

**Branch 2: Study Permit**
- **Email Content**: Focus on Designated Learning Institutions (DLIs), proof of funds, and post-graduation work permits (PGWP).
- **Subject**: "Planning your studies in Canada (and beyond)"

**Branch 3: Family Sponsorship**
- **Email Content**: Focus on proving relationship genuineness and financial undertaking requirements.
- **Subject**: "Keeping your family together in Canada"

**Branch 4: Default / Other**
- **Email Content**: General updates on Canadian immigration policy changes.

*Implementation*: This requires zero custom code. It uses native GHL Workflow `If/Else` branching based on the `ai_program_interest` custom field.

---

## 3. Contextual Consultation Reminders

Enhance standard reminders by injecting the lead's specific urgency or program interest.

### Workflow: `WF-05 — Appointment Reminders (Updated)`

**48-Hour Email Reminder Template:**
```html
Hi {{contact.first_name}},

This is a reminder for your upcoming immigration strategy session on {{appointment.start_time}}.

Our consultant has reviewed your initial file regarding your interest in **{{contact.ai_program_interest}}**. 

Because you indicated your timeline is **{{contact.ai_urgency}}**, we want to ensure we make the most of our time together. Please have any relevant documents (passports, previous applications, language test scores) ready for the call.

To confirm you will be attending, please reply YES to this email or text message.

Best,
NeuronX Advisory
```

## Summary
By leveraging the data extracted during the initial AI Voice Call (`ai_program_interest`, `ai_urgency`), we can dramatically increase the relevance and conversion rate of downstream SMS and Email automations entirely within native GoHighLevel, requiring zero external API calls for messaging.