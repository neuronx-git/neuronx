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
        console.log("Executing Strict Reality Check (Tenant & Workflow Existence)...");

        const result = await agent.executeStep(
            `Navigate to https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows.
             1. Verify Tenant:
                a. Look at the top left corner or the URL.
                b. Confirm the Location ID is "FlRL82M0D6nclmKT7eXH".
                c. Confirm the Sub-Account Name is "NeuronX Test Lab".
             2. Verify Workflow:
                a. Wait for the list to load.
                b. Search for "WF-04B".
                c. Look for any row that contains "WF-04B" or "Vapi Return Handler".
             3. Return a JSON object with:
                - tenantId: string (found ID)
                - tenantName: string (found name)
                - wf04bExists: boolean (true/false)
                - wf04bName: string (exact name found if exists)
                - allWorkflows: array of strings (names of all visible workflows)`,
            "https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows"
        );

        console.log("Reality Check Result:", JSON.stringify(result, null, 2));
        
        fs.writeFileSync(path.join(__dirname, '../../.ghl_reality_check.json'), JSON.stringify(result.extracted_information, null, 2));

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();