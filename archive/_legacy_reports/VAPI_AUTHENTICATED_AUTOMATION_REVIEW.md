# Vapi Authenticated Automation Review

## The Problem
During Phase 8 of the Voice AI Implementation, we attempted to use Skyvern to automate the Vapi dashboard to claim a free phone number. The script successfully executed, but failed to complete the objective because the Vapi dashboard requires an active user session (login), which the headless Skyvern worker did not possess. We prematurely declared the task "manual" instead of solving the authentication layer.

## The Re-Evaluation (Applying the New Rule)
Can the same authenticated UI/session method used for GoHighLevel be applied to Vapi?
**Yes.**

Vapi, like GoHighLevel, uses standard session cookies to maintain login state. If we generate a Skyvern session, pause execution to allow the founder to log in manually *once*, we can save that session state and allow Skyvern to execute the phone number provisioning autonomously.

## The Implementation Plan

### Step 1: Initialize an Interactive Auth Session
We will write a new script (`authenticateVapi.ts`) that initializes a Skyvern session and outputs the URL to the terminal.
```typescript
const url = await agent.createSession();
console.log("ACTION REQUIRED: Open this URL, log into Vapi.ai, and press Enter in this terminal when done.");
```

### Step 2: Persist the Session
Once the founder presses Enter, the script saves the `browser_session_id` (e.g., `pbs_507036...`) to a local `.vapi_session.env` file. This is the exact same pattern we used for the GHL Playwright auth state.

### Step 3: Execute the Provisioning Script
We will update `provisionVapiPhone.ts` to load the Vapi session ID instead of the GHL session ID.

```typescript
const agent = new SkyvernAgent();
await agent.loadSession(process.env.VAPI_BROWSER_SESSION_ID); // Loads the authenticated state

const result = await agent.executeStep(
    `Navigate to https://dashboard.vapi.ai/phone-numbers.
     Click 'Buy Number'.
     Select any available US/CA number.
     Click confirm.
     Assign the number to the 'NeuronX Intake Agent' in the dropdown.`,
    "https://dashboard.vapi.ai/phone-numbers"
);
```

### Step 4: Extract the Phone ID
The script will instruct Skyvern to read the resulting Phone Number ID from the DOM and write it to `.vapi_phone.json`.

## Conclusion
There is no technical blocker preventing UI automation of Vapi. The previous failure was a process failure (not handling authentication), not a platform limitation. By applying the `AUTHENTICATED_UI_AUTOMATION_RULE`, we can successfully automate the phone number provisioning and linking process.