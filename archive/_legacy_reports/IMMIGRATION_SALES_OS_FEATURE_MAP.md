# Immigration Sales OS Feature Map

## The Concept
NeuronX is not just a CRM; it is a highly opinionated, verticalized Operating System specifically designed for the regulatory and psychological realities of Canadian Immigration Consulting.

By combining the capabilities of GHL, Vapi, and Make.com, we create the following end-to-end OS.

---

### 1. Lead Capture (GHL Funnels & Forms)
- **Feature**: Multi-step, high-converting intake forms embedded in specialized landing pages (Express Entry vs Study vs Spousal).
- **Immigration Specifics**: Forms capture baseline metadata (Country of Citizenship, Marital Status) without asking for full CRS scores (which causes drop-off).
- **Tech**: GHL Native.

### 2. Speed-to-Lead Qualification (Vapi AI)
- **Feature**: Sub-5-minute outbound phone call.
- **Immigration Specifics**: The AI's sole job is to establish human connection, determine the program interest, flag legal complexities (Refusals, Criminality), and sell the value of a paid strategy session.
- **Guardrail**: Strict UPL (Unauthorized Practice of Law) prevention. AI cannot assess eligibility.
- **Tech**: Vapi Outbound triggered by GHL Webhook.

### 3. AI Lead Scoring & Routing (GHL Workflows)
- **Feature**: Mathematical routing based on AI extraction.
- **Immigration Specifics**: 
  - Express Entry + 30 days urgency = **High Score** -> VIP SMS Booking Sequence.
  - No budget + 2 years out = **Low Score** -> Placed into long-term newsletter nurture.
  - Deportation mentioned = **Escalation** -> Bypasses AI, alerts firm owner immediately.
- **Tech**: GHL If/Else Workflow branching based on Custom Fields updated by Make.com.

### 4. Consultation Preparation (Make.com + OpenAI)
- **Feature**: "The Consultant Briefing".
- **Immigration Specifics**: 2 hours before the Zoom meeting, the licensed consultant receives an AI-generated brief outlining the client's goals, red flags, and 3 specific strategic questions to ask during the call to increase retainer conversion.
- **Tech**: Make.com triggers 2hrs before GHL Appointment -> Passes GHL Notes to OpenAI -> Sends Slack/Email to Consultant.

### 5. Retainer Conversion & Invoicing (GHL Payments)
- **Feature**: Automated transition from "Consultation" to "Retained Client".
- **Immigration Specifics**: Trigger automated sending of the Initial Retainer Agreement (via GHL Documents/Signatures) and the Stripe invoice for the first installment.
- **Tech**: GHL Native Documents & Payments.

### 6. Client Onboarding (GHL Client Portal)
- **Feature**: Secure document collection.
- **Immigration Specifics**: Once retained, the client is granted access to a GHL Client Portal where they can securely upload passports, IELTS scores, and marriage certificates, keeping sensitive data out of email.
- **Tech**: GHL Native Client Portal.

### 7. Referral Generation (GHL Automations)
- **Feature**: Automated reputation management.
- **Immigration Specifics**: Immigration is a highly networked community. 7 days after a successful consultation (where `ai_complexity_flag` is NOT 'Deportation'), send an automated SMS: *"If you found our strategy session helpful, would you mind sharing our contact info with any friends looking to move to Canada?"*
- **Tech**: GHL Native Workflows.