# Orchestration Capability Matrix (Make.com / n8n)

| Feature Category | Description | API or UI | Current NeuronX Usage | Opportunity for Improvement | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Webhook Receivers** | Catch incoming HTTP POST requests. | UI | Core layer for catching Vapi payload. | Implement strict schema validation to drop bad requests before processing. | High |
| **JSON Parsing** | Extracting specific keys from nested JSON arrays. | UI | Used to extract Vapi function arguments. | Handle scenarios where Vapi returns partial JSON or hallucinated keys. | High |
| **API Routing (HTTP Modules)** | Sending authenticated requests to GHL. | UI | Core layer for `PUT /contacts/{id}`. | Implement exponential backoff for GHL rate limits. | Critical |
| **LLM Integration (OpenAI)** | Passing data to GPT for formatting/summarization. | UI | None yet. | Use to generate the "Pre-Consultation Briefing" document. | High |
| **Data Stores / State** | Temporary database for holding state between runs. | UI | None yet. | Use to track "minutes used per client" for billing purposes. | Medium |
| **Error Handlers** | Try/Catch routing for failed API calls. | UI | None yet. | Send Slack/Discord alerts to the admin if a GHL sync fails. | High |
| **Template Cloning** | Exporting scenarios as blueprints. | Both | None yet. | Automate the deployment of the Make scenario for new tenants via API. | Critical |