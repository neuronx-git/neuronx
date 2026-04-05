import { SkyvernAgent } from "./SkyvernAgent";
import fs from "fs";
import path from "path";

async function main() {
    const agent = new SkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        const url = await agent.createSession();
        console.log("ACTION REQUIRED: Log into GHL at " + url);
        process.exit(0);
    }

    try {
        console.log("Creating GHL WF-04B with Inbound Webhook...");

        const result = await agent.executeStep(
            `Navigate to https://app.gohighlevel.com.
             1. Go to 'Automation' > 'Workflows' > 'Create Workflow'.
             2. Select 'Start from Scratch' and click 'Continue'.
             3. Click to rename the workflow to 'WF-04B — Vapi Return Handler'.
             4. Click 'Add New Trigger' and search for 'Inbound Webhook'. Select it.
             5. Copy the generated Webhook URL and return it in the JSON output as 'webhookUrl'.
             6. Click 'Save Trigger'.
             7. Click 'Save' in the top right corner.
             8. Return the Webhook URL.`,
            "https://app.gohighlevel.com"
        );

        console.log("GHL Workflow Creation Result:", JSON.stringify(result, null, 2));
        
        // Save the result to extract the URL later
        fs.writeFileSync(path.join(__dirname, '../../.ghl_webhook_creation_result.json'), JSON.stringify(result, null, 2));

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();