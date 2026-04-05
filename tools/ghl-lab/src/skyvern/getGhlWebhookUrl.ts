import { SkyvernAgent } from "./SkyvernAgent";
import fs from "fs";
import path from "path";

async function main() {
    const agent = new SkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        console.log("Session expired. Cannot retry without login.");
        process.exit(1);
    }

    try {
        console.log("Attempting to extract Webhook URL via Skyvern...");

        const result = await agent.executeStep(
            `Navigate to https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows.
             1. Wait for the list to load.
             2. Search for "WF-04B" in the search bar if needed, or find "WF-04B — Vapi Return Handler" in the list.
             3. Click on the workflow name to open the builder.
             4. Click on the "Inbound Webhook" trigger card at the top of the flow.
             5. A sidebar will open. Look for the URL field (it usually contains "hooks.leadconnectorhq.com" or "services.leadconnectorhq.com").
             6. Copy that text exactly.
             7. Return the URL in the JSON output as "webhookUrl".`,
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