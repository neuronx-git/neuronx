import dotenv from "dotenv";
import path from "path";
import { SkyvernAgent } from "./SkyvernAgent";

dotenv.config({ path: path.join(__dirname, "../../.env") });

async function main() {
    console.log("Initializing Skyvern to fix Create Contact mapping...");
    
    if (!process.env.SKYVERN_API_KEY) {
        throw new Error("SKYVERN_API_KEY is required");
    }

    const agent = new SkyvernAgent();
    await agent.loadSession();
    
    const LOCATION_ID = "FlRL82M0D6nclmKT7eXH"; 
    const WORKFLOW_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;

    const instructions = `
        Navigate to the GoHighLevel URL: ${WORKFLOW_URL}.
        Wait for the workflows list to load.
        Search for and click on the workflow named "WF-04B - AI Call Receiver".
        Wait for the workflow builder to load.
        Click on the "Create Contact" action box (it has a blue icon and an orange error exclamation mark).
        In the right-side panel that opens, click the "+ Add Field" button.
        In the dropdown that appears, type "First Name" and select it.
        In the input box next to "First Name", type exactly "Vapi Caller".
        Click the blue "Save Action" button at the bottom right of the panel.
        Click the blue "Save" button in the top right corner of the main screen.
    `;

    console.log("Executing Skyvern Task...");
    await agent.executeStep(instructions);
    
    console.log("Skyvern task completed.");
}

main().catch(console.error);
