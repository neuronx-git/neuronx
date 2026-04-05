import dotenv from "dotenv";
import path from "path";
import { SkyvernAgent } from "./SkyvernAgent";

dotenv.config({ path: path.join(__dirname, "../../.env") });

async function main() {
    console.log("Starting WF-01 Inspection...");
    
    if (!process.env.SKYVERN_API_KEY) {
        throw new Error("SKYVERN_API_KEY is required");
    }

    const agent = new SkyvernAgent();
    await agent.createSession("https://app.gohighlevel.com"); // Force new session creation since loadSession failed
    
    const LOCATION_ID = "FlRL82M0D6nclmKT7eXH"; 
    const WORKFLOW_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;
    
    const instructions = `
        Navigate to the GoHighLevel URL: ${WORKFLOW_URL}.
        Wait for the workflows list to load.
        Search for "WF-01" in the search bar.
        Click on "WF-01 — Instant Lead Capture & Speed-to-Lead Engine".
        Wait for the workflow builder to load.
        
        INSPECTION TASK:
        1. Look at the Trigger at the top. Is it "Form Submitted"?
        2. Look at the first action. Is it "Send SMS"?
        3. Look at the toggle in the top right. Is it "Draft" or "Publish"?
    `;

    console.log("Executing Skyvern Inspection Task...");
    await agent.executeStep(instructions);
    
    console.log("Inspection Task Completed.");
}

main().catch(console.error);
