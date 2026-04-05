import dotenv from "dotenv";
import path from "path";
import { SkyvernAgent } from "./SkyvernAgent";

dotenv.config({ path: path.join(__dirname, "../../.env") });

async function main() {
    console.log("Starting WF-01 Direct Publish Task...");
    
    if (!process.env.SKYVERN_API_KEY) {
        throw new Error("SKYVERN_API_KEY is required");
    }

    const agent = new SkyvernAgent();
    await agent.createSession();
    
    const LOCATION_ID = "FlRL82M0D6nclmKT7eXH"; 
    const WORKFLOW_ID = "99ce0aa7-2491-4c91-9477-22969798e2b7"; // Hardcoded from previous checks
    const WORKFLOW_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows/${WORKFLOW_ID}`;
    
    const instructions = `
        Navigate directly to the workflow URL: ${WORKFLOW_URL}.
        Wait for the workflow builder canvas to fully load.
        In the top right corner, there is a toggle switch for Draft/Publish. 
        Click the toggle so it switches to "Publish".
        Then, click the blue "Save" button in the top right corner.
        Wait for the green "Workflow saved" success toast to appear.
    `;

    console.log("Executing Skyvern Publish Task...");
    await agent.executeStep(instructions);
    console.log("Publish Task Completed.");
}

main().catch(console.error);
EOF~