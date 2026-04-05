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
        console.log("Locating WF-04B and extracting URL (Final Attempt)...");

        // We will try a different strategy:
        // 1. Search for the workflow
        // 2. Open it
        // 3. Click the trigger
        // 4. Use a more aggressive extraction prompt
        
        const result = await agent.executeStep(
            `Navigate to https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows.
             1. Wait for list to load.
             2. Search for "WF-04B".
             3. Click on the row for "WF-04B — Vapi Return Handler".
             4. Click on the "Inbound Webhook" trigger card.
             5. Look for the input field with the URL.
             6. If you cannot "read" the text, try to click the "Copy" icon next to the URL field.
             7. Then, return a JSON object with:
                - foundWorkflow: boolean
                - webhookUrl: string (if you can read it)
                - status: string (e.g. "Workflow found, trigger opened")`,
            "https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows"
        );

        console.log("Extraction Result:", JSON.stringify(result, null, 2));
        
        if (result.extracted_information?.webhookUrl) {
            fs.writeFileSync(path.join(__dirname, '../../.ghl_webhook_url.json'), JSON.stringify(result.extracted_information, null, 2));
            console.log("✅ SUCCESS: Webhook URL captured!");
        } else {
            console.log("❌ FAILED: Workflow exists but URL is unreadable.");
        }

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();