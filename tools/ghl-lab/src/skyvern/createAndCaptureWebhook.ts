import { SkyvernAgent } from "./SkyvernAgent";
import fs from "fs";
import path from "path";

async function main() {
    const agent = new SkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        console.log("Session expired.");
        process.exit(1);
    }

    try {
        console.log("Creating WF-04B and capturing Webhook URL at source...");

        const result = await agent.executeStep(
            `Navigate to https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows.
             1. Click "Create Workflow" in the top right.
             2. Select "Start from scratch" and click "Continue".
             3. Click the workflow name at the top left and rename it EXACTLY to "WF-04B — Vapi Return Handler".
             4. Click "Add New Trigger".
             5. Search for "Inbound Webhook" and select it.
             6. The right sidebar will open. There is an input field containing a URL that starts with "https://".
             7. BEFORE doing anything else, COPY the exact text of that URL.
             8. Click "Save Trigger".
             9. Toggle the status from "Draft" to "Publish".
             10. Click "Save" in the top right.
             11. MUST RETURN the URL you copied as "webhookUrl" in the JSON output.`,
            "https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows"
        );

        console.log("Creation Result:", JSON.stringify(result, null, 2));
        
        if (result.extracted_information?.webhookUrl) {
            fs.writeFileSync(path.join(__dirname, '../../.ghl_webhook_url.json'), JSON.stringify(result.extracted_information, null, 2));
            console.log("✅ SUCCESS: Webhook URL captured immediately at creation!");
        } else {
            console.log("❌ FAILED: Workflow created but URL extraction failed again.");
        }

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();