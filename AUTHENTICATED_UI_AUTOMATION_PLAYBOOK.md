# Authenticated UI Automation Playbook

## The Rule: AUTHENTICATED_UI_AUTOMATION_RULE
Never treat external SaaS tools (Vapi, ElevenLabs, Make, n8n, Twilio, etc.) as "manual by default." The same pattern of **Authenticated UI Automation** that successfully configured GoHighLevel workflows must be attempted for all SaaS platforms before requesting human intervention.

## The Strategy
Modern SaaS tools often gate API endpoints behind paywalls or lack API parity with their UI. However, their UIs are accessible via headless browsers *if* authentication is handled correctly. 

We solve the authentication barrier by:
1. Creating a persistent browser session (Playwright `storageState` or Skyvern session ID).
2. Asking the founder to log in *once* manually.
3. Reusing that authenticated session to drive all subsequent UI automation.

---

## The Automation Checklist (For Any New SaaS)

Before declaring a task "manual", you must complete this checklist:

### 1. Session Availability
- [ ] Do we already have an active session ID or saved `storageState` for this domain?
- [ ] If no, can we generate an auth URL to ask the founder to log in and capture the state?

### 2. State Persistence
- [ ] Does the platform use standard session cookies/tokens that survive a browser restart?
- [ ] Have we saved these cookies to `.env` or a local `.json` file for reuse?

### 3. Skyvern / Playwright Execution
- [ ] Have we written a script that loads the persisted session state?
- [ ] Can Skyvern successfully navigate the dashboard post-login?

### 4. Escalation Criteria
*Only escalate to the founder for manual execution if blocked by:*
- **Unavailable Credentials**: The founder cannot/will not provide login access.
- **Aggressive 2FA/CAPTCHA**: The platform forces a CAPTCHA or 2FA on *every single action*, breaking session persistence.
- **Billing / Payment**: The action requires entering a credit card or confirming a financial transaction.
- **Legal / Identity**: The action requires uploading an ID or signing a legal agreement.

---

## Implementation Pattern

### Step 1: Session Initialization
Create a script that checks for an existing session. If none exists, generate an interactive session and prompt the user to log in.

```typescript
// Example Skyvern Session Loader
const agent = new SkyvernAgent();
const resumed = await agent.loadSession();

if (!resumed) {
    const url = await agent.createSession();
    console.log("ACTION REQUIRED: Please open this URL, log in to the SaaS, and close the tab:", url);
    process.exit(0);
}
```

### Step 2: Authenticated Execution
Once the session is saved, write the automation prompt assuming the user is already logged into the dashboard.

```typescript
// Example Authenticated Execution
const result = await agent.executeStep(
    `Navigate to https://dashboard.saas.com/settings.
     Click the 'Add Webhook' button.
     Paste 'https://hook.make.com/xyz' into the URL field.
     Save.`,
    "https://dashboard.saas.com"
);
```

## Summary
By enforcing this playbook, NeuronX maintains its "zero-manual-work" philosophy for clients and operators, pushing the boundaries of what can be configured autonomously.