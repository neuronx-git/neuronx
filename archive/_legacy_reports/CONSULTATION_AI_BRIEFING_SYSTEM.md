# AI Consultation Briefing System

## Objective
To ensure that licensed immigration consultants enter every strategy session fully prepared, the NeuronX system automatically generates and delivers a pre-consultation briefing. This briefing is assembled by the AI using data extracted during the intake phase and pushed into the GoHighLevel (GHL) system.

## Trigger Mechanism
- **Workflow**: `WF-05A — AI Briefing Generation`
- **Trigger**: Appointment Status changes to "Confirmed" (or 2 hours prior to the appointment via a wait step).
- **Execution**: A webhook sends the GHL Contact data (including AI custom fields and notes) to an LLM (e.g., via OpenAI API or Make.com integration). The LLM formats the briefing and updates the GHL Contact Notes, and sends an internal email/notification to the assigned consultant.

## Briefing Structure (The Output)

The AI generates a structured summary in the following format:

---

**🚨 NEURONX CONSULTATION BRIEFING 🚨**

**Lead Profile:**
- **Name**: [Lead First Name] [Lead Last Name]
- **Location**: [ai_country] / [current_location]
- **Program Interest**: [ai_program_interest]
- **Urgency**: [ai_urgency]
- **NeuronX Lead Score**: [ai_lead_score]/100 ([Score Band])

**AI Conversation Summary:**
> [ai_summary] *(e.g., "Lead is a 28-year-old software engineer from Brazil looking to apply for Express Entry. They have not taken the IELTS yet but have their educational credentials assessed. They are highly motivated to move within the next 6 months.")*

**Risk & Complexity Flags:**
- ⚠️ [ai_complexity_flag] *(e.g., "Previous Refusal: Visitor Visa in 2022")*
- ⚠️ Budget Awareness: [ai_budget_awareness] *(e.g., "Hesitant about professional fees")*

**Consultant Action Plan (Recommended Questions):**
1. [AI Generated Question 1 based on context, e.g., "Ask for details regarding the 2022 visitor visa refusal to check for misrepresentation."]
2. [AI Generated Question 2, e.g., "Verify current English/French language proficiency scores."]
3. [AI Generated Question 3, e.g., "Discuss the retainer structure early to overcome budget hesitation."]

---

## Technical Implementation (No-Code / Low-Code)

1. **Webhook from GHL**:
   - GHL sends a POST request to Make.com containing: `contact.id`, `contact.name`, `contact.ai_summary`, `contact.ai_program_interest`, `contact.ai_urgency`, `contact.ai_complexity_flag`, `contact.ai_lead_score`.

2. **LLM Formatting (Make.com -> OpenAI)**:
   - **System Prompt**: "You are an immigration consultant assistant. Take the following JSON data about a prospective client and format it into a clean, highly readable Consultation Briefing. Generate 3 specific, strategic questions the consultant should ask during the meeting based on the provided data. DO NOT provide legal advice or assess eligibility in the briefing."

3. **Update GHL**:
   - Make.com uses the GHL API (`POST /contacts/{id}/notes`) to append the formatted briefing to the contact record.
   - Make.com uses the GHL API to send an internal notification (Email or App Notification) to the assigned user containing the briefing text.

## Fallback Mechanism
If the LLM generation fails, GHL natively sends an email containing the raw custom fields using standard template variables (e.g., `{{contact.ai_summary}}`, `{{contact.ai_program_interest}}`) to ensure the consultant is never completely blind.