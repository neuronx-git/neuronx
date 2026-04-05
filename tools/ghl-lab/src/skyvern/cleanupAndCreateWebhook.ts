import { SkyvernAgent } from "./SkyvernAgent";
import fs from "fs";
import path from "path";

async function main() {
    const agent = new SkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        console.log("Session expired. Please use the previous manual step or re-bootstrap.");
        process.exit(1);
    }

    try {
        console.log("Cleaning up redundant workflows...");

        const result = await agent.executeStep(
            `Navigate to https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows.
             1. Wait for the list to load.
             2. Identify rows where the Name starts with "New Workflow :" (e.g. "New Workflow : 177366...").
             3. For EACH of these rows:
                a. Click the vertical ellipsis (three dots) menu on the far right of that row.
                b. Click "Delete".
                c. Confirm the deletion if a modal appears.
             4. Do NOT delete any workflow starting with "WF-".
             5. After cleaning up, create a NEW workflow named "WF-04B — Vapi Return Handler" (if it doesn't exist).
             6. Add the "Inbound Webhook" trigger.
             7. Copy the Webhook URL.
             8. Save and Publish.
             9. Return the Webhook URL as "webhookUrl" in the JSON.`,
            "https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows"
        );

        console.log("Cleanup Result:", JSON.stringify(result, null, 2));
        
        if (result.extracted_information?.webhookUrl) {
            fs.writeFileSync(path.join(__dirname, '../../.ghl_webhook_url.json'), JSON.stringify(result.extracted_information, null, 2));
            console.log("✅ SUCCESS: Cleanup done & Webhook URL captured!");
        } else {
            console.log("⚠️ Cleanup likely done, but extraction might have failed.");
        }

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();