import dotenv from "dotenv";
import path from "path";
import { SkyvernAgent } from "./SkyvernAgent";

dotenv.config({ path: path.join(__dirname, "../../.env") });

async function main() {
    console.log("Starting Diagnostic Task...");
    
    if (!process.env.SKYVERN_API_KEY) {
        throw new Error("SKYVERN_API_KEY is required");
    }

    const agent = new SkyvernAgent();
    await agent.createSession();
    
    const LOCATION_ID = "FlRL82M0D6nclmKT7eXH"; 
    const WORKFLOW_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;
    
    const instructions = `
        Navigate to the GoHighLevel URL: ${WORKFLOW_URL}.
        Wait for the workflows list to load.
        Search for "WF-01" in the search bar.
        Click on "WF-01 — Instant Lead Capture & Speed-to-Lead Engine".
        Wait for the workflow builder to load completely.
        
        Click the toggle in the top right corner to change it from "Draft" to "Publish".
        Then, crucially, click the blue "Save" button in the top right corner.
        Wait for the "Saved successfully" toast notification to appear.
        
        Return the exact text of the button you clicked to save.
    `;

    console.log("Executing Diagnostic Task...");
    const result = await agent.executeStep(instructions);
    console.log("Result:", JSON.stringify(result, null, 2));
}

main().catch(console.error);
