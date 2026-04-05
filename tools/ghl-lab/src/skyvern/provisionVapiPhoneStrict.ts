import { VapiSkyvernAgent } from "./VapiSkyvernAgent";
import fs from "fs";
import path from "path";

async function main() {
    const agent = new VapiSkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        console.error("Failed to load Vapi session. The user may not have completed the login or the session expired.");
        process.exit(1);
    }

    const VAPI_DASHBOARD_URL = `https://dashboard.vapi.ai/phone-numbers`;

    try {
        console.log("Navigating to Vapi Dashboard to claim free phone number (Attempt 3: Strict DOM guidance)...");

        // The UI might have a specific flow. Let's make the prompt very explicit and ask it to describe what it sees if it fails.
        const result = await agent.executeStep(
            `You are logged into the Vapi Dashboard.
             Navigate to https://dashboard.vapi.ai/phone-numbers.
             1. Look for a button containing the text "Buy Number". It might be in the top right corner. Click it.
             2. A modal or a new page should appear allowing you to search for a number.
             3. If there is a search or filter, leave it default (US/Canada).
             4. Click the "Buy" or "Claim" button next to the FIRST available phone number in the list.
             5. If a confirmation dialog appears, confirm the purchase.
             6. Wait for the success notification.
             7. Find the newly added phone number in the table on the phone-numbers page.
             8. Click on that number to edit it.
             9. Find the "Assistant" dropdown/select field and choose "NeuronX Intake Agent".
             10. Save changes.
             11. Extract the Phone Number ID (usually looks like a UUID) and the Phone Number string from the page and return them as JSON.
             
             If you cannot find the "Buy Number" button, explain what you see on the screen instead.`,
            VAPI_DASHBOARD_URL
        );

        console.log("Vapi UI Execution Result:", JSON.stringify(result, null, 2));

        fs.writeFileSync(path.join(__dirname, '../../.vapi_phone_ui_result.json'), JSON.stringify(result, null, 2));

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();