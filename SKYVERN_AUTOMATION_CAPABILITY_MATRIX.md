# Skyvern Automation Capability Matrix

| Feature Category | Description | API or UI | Current NeuronX Usage | Opportunity for Improvement | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Visual Element Recognition** | Clicking buttons based on visual context rather than strict DOM selectors. | API | Used for GHL Workflow builder and Vapi dashboard. | Expand to automate Stripe billing setups. | High |
| **Persistent Sessions** | Reusing cookies/local storage across runs (`browser_session_id`). | API | Core pattern established (GHL & Vapi). | Build a central session-manager service that refreshes tokens weekly. | Critical |
| **Data Extraction** | Reading text/values from complex UIs and returning JSON. | API | Used to extract Vapi Phone Number IDs. | Use to scrape GHL reporting dashboards if API limits are hit. | Medium |
| **Interactive Pausing** | Handing control to a human for CAPTCHA/2FA, then resuming. | API | Core pattern established for login bootstrapping. | Standardize the CLI prompt for the founder to handle these elegantly. | High |
| **Cross-Iframe Navigation** | Interacting with embedded tools (like GHL Form Builder). | API | Used during GHL Gold Build. | Use to automate the configuration of GHL Custom Values inside the iframe. | Medium |