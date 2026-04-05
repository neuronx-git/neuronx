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
        console.log("Navigating to Vapi Dashboard to claim free phone number...");

        const result = await agent.executeStep(
            `Navigate to https://dashboard.vapi.ai/phone-numbers.
             1. Look for a button that says "Buy Number" or "Add Number" or "Claim Free Number" and click it.
             2. If a modal appears, select any available US or Canadian number.
             3. Confirm the purchase/claim.
             4. Once the number is listed in the table, click on it or edit it.
             5. Set the "Assistant" dropdown to "NeuronX Intake Agent".
             6. Save the configuration.
             7. Extract the Phone Number and the Phone Number ID from the URL or page text and return it as JSON.`,
            VAPI_DASHBOARD_URL
        );

        console.log("Vapi UI Execution Result:", JSON.stringify(result, null, 2));

        const fs = require('fs');
        const path = require('path');
        fs.writeFileSync(path.join(__dirname, '../../.vapi_phone_ui_result.json'), JSON.stringify(result, null, 2));

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();