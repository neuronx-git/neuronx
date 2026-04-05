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
        console.log("Starting Controlled Cleanup...");

        const result = await agent.executeStep(
            `Navigate to https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows.
             1. Look at the list of workflows.
             2. Find the row for "New Workflow : 1773665053619".
             3. Click the three vertical dots (ellipsis) on the far right of that specific row.
             4. Click "Delete".
             5. Confirm the deletion in the popup modal.
             6. Repeat this process for "New Workflow : 1773665946429".
             7. Repeat this process for "New Workflow : 1773666055197".
             8. DO NOT click the ellipsis on any workflow starting with "WF-".
             9. Return a JSON object with { "cleanup": "complete" } when done.`,
            "https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows"
        );

        console.log("Cleanup Result:", JSON.stringify(result, null, 2));

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();