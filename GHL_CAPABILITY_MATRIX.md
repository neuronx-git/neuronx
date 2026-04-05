# GoHighLevel (GHL) Capability Matrix

| Feature Category | Description | API or UI | Current NeuronX Usage | Opportunity for Improvement | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CRM & Pipelines** | Core lead tracking, stage movement, and custom field storage. | Both (API robust) | High. Using Custom Fields (`ai_program_interest`, etc.) and Pipelines (`Immigration Intake`). | Could utilize Smart Lists more heavily for targeted email blasts based on AI scoring. | High |
| **Workflows & Automations** | If/Else branching, wait steps, webhooks, internal notifications. | UI only (Builder) | High. Using WF-01 to WF-11 for speed-to-lead and nurture. | Deepen webhook usage to pass more contextual data to orchestration layers. | High |
| **Conversational AI** | Native GHL bot for SMS/Webchat booking. | UI | None (Deferred due to UPL risks). | Use in "Suggest" mode for human-in-the-loop SMS follow-ups. | Medium |
| **Calendars & Scheduling** | Round-robin booking, reminders, buffer times. | Both | High. Using `Immigration Consultations` calendar. | Integrate calendar events with Make.com to trigger pre-consultation AI briefings. | High |
| **Forms & Surveys** | Lead capture with conditional logic. | UI only (Builder) | High. Using `Immigration Inquiry (V1)`. | Use Survey logic to pre-filter totally unqualified leads before they even trigger a Vapi call. | Medium |
| **Payments & Invoicing** | Stripe/PayPal integration for consultation fees. | UI / API | None yet. | Automate invoice generation when a lead reaches "CONSULT READY" state. | High |
| **Funnels & Websites** | Landing page builder with split testing. | UI only (Builder) | Low. Basic funnel created. | Build highly optimized templates specific to Express Entry vs Study Permits. | Low |
| **Snapshots** | Template export/import for SaaS scaling. | UI / API (OAuth) | Core to deployment strategy. | Fully automate the snapshot push via API for new tenant onboarding. | High |
| **Review Management** | Automated SMS/Email review requests. | Both | None yet. | Trigger 5-star review requests 3 days after a successful consultation (excluding complex/refused cases). | Medium |
| **Reporting & Dashboards** | Conversion rates, call tracking, appointment show rates. | UI (Some API) | None yet. | Build custom dashboards tracking "AI Qualification Rate" vs "Human Conversion Rate". | High |