import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
    const agent = new SkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        const url = await agent.createSession();
        console.log("\n!!! ACTION REQUIRED !!!");
        console.log(`Please open this URL and LOG IN to Vapi: ${url}`);
        process.exit(0);
    }

    const VAPI_DASHBOARD_URL = `https://dashboard.vapi.ai/phone-numbers`;

    try {
        console.log("Navigating to Vapi Dashboard to claim free phone number (Attempt 2)...");

        // The first attempt might have failed because the user needs to physically log into Vapi in the browser session first.
        // Skyvern is executing, but it's probably hitting the login screen if the session doesn't have Vapi cookies.

        const result = await agent.executeStep(
            `Navigate to https://dashboard.vapi.ai/phone-numbers.
             If you see a login screen, DO NOT PROCEED. Return "Requires Login".
             If you are logged in:
             1. Click the button to buy or add a phone number.
             2. Select any available number.
             3. Confirm.
             4. Extract the Phone Number ID from the UI and return it.`,
            VAPI_DASHBOARD_URL
        );

        console.log("Vapi UI Execution Result:", JSON.stringify(result, null, 2));

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();