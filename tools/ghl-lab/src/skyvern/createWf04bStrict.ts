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
        console.log("Creating WF-04B with strict persistence...");

        const result = await agent.executeStep(
            `Navigate to https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows.
             1. Click "Create Workflow".
             2. Select "Start from scratch" and click "Continue".
             3. Wait for the editor to load.
             4. Click the workflow name at the top left.
             5. Rename it EXACTLY to "WF-04B — Vapi Return Handler".
             6. Click "Add New Trigger".
             7. Search for "Inbound Webhook" and select it.
             8. Click "Save Trigger".
             9. Toggle the status from "Draft" to "Publish" (top right toggle).
             10. Click the blue "Save" button in the top right corner.
             11. Wait for the "Saved" confirmation or toast.
             12. Click the "< Back" button (top left chevron) to return to the list.
             13. Search the list for "WF-04B".
             14. Return { "created": true, "visibleInList": true } if you see it.`,
            "https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows"
        );

        console.log("Creation Result:", JSON.stringify(result, null, 2));
        
        fs.writeFileSync(path.join(__dirname, '../../.ghl_wf04b_creation.json'), JSON.stringify(result.extracted_information, null, 2));

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();