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
        console.log("Navigating to Vapi Dashboard to claim free phone number (Authenticated)...");

        const result = await agent.executeStep(
            `You are already logged in. 
             Navigate to https://dashboard.vapi.ai/phone-numbers.
             1. Click the button to "Buy Number" or "Add Number" (this uses the free credit).
             2. In the modal, select any available US or Canadian number.
             3. Confirm the purchase.
             4. Once the number appears in the table, click to edit it.
             5. Set the "Assistant" dropdown to "NeuronX Intake Agent".
             6. Save the configuration.
             7. Extract the Phone Number and Phone Number ID from the UI and return it as a JSON object.`,
            VAPI_DASHBOARD_URL
        );

        console.log("Vapi UI Execution Result:", JSON.stringify(result, null, 2));

        fs.writeFileSync(path.join(__dirname, '../../.vapi_phone_ui_result.json'), JSON.stringify(result, null, 2));

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();