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
        console.log("Extracting URL from newly created WF-04B...");

        // We specifically target the workflow by exact name now that we cleaned up
        const result = await agent.executeStep(
            `Navigate to https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows.
             1. Wait for the list.
             2. Find "WF-04B — Vapi Return Handler" and click it.
             3. Click on the "Inbound Webhook" trigger card.
             4. Look for the input field containing "https://services.leadconnectorhq.com/...".
             5. Copy the FULL URL from that field.
             6. Return it as "webhookUrl" in the JSON output.`,
            "https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows"
        );

        console.log("Extraction Result:", JSON.stringify(result, null, 2));
        
        if (result.extracted_information?.webhookUrl) {
            fs.writeFileSync(path.join(__dirname, '../../.ghl_webhook_url.json'), JSON.stringify(result.extracted_information, null, 2));
            console.log("✅ SUCCESS: Webhook URL captured!");
        } else {
            console.log("❌ FAILED: Could not extract URL from DOM.");
        }

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();