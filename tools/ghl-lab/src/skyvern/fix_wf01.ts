import dotenv from "dotenv";
import path from "path";
import { SkyvernAgent } from "./SkyvernAgent";

dotenv.config({ path: path.join(__dirname, "../../.env") });

async function main() {
    console.log("Starting WF-01 Targeted Fix...");
    
    if (!process.env.SKYVERN_API_KEY) {
        throw new Error("SKYVERN_API_KEY is required");
    }

    const agent = new SkyvernAgent();
    await agent.createSession("https://app.gohighlevel.com");
    
    const LOCATION_ID = "FlRL82M0D6nclmKT7eXH"; 
    const WORKFLOW_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;
    
    const instructions = `
        Navigate to the GoHighLevel URL: ${WORKFLOW_URL}.
        Wait for the workflows list to load.
        Search for "WF-01" in the search bar.
        Click on "WF-01 — Instant Lead Capture & Speed-to-Lead Engine".
        Wait for the workflow builder to load.
        
        TASK 1: Trigger Verification
        - Click on the top trigger box.
        - Ensure it is set to "Form Submitted".
        - Ensure the form selected is "Immigration Inquiry (V1)".
        - Save Trigger if you made changes.

        TASK 2: Action 1 (Instant SMS)
        - Click the first action box (should be "Send SMS").
        - If the message is generic, update it to: "Hi {{contact.first_name}}, this is the NeuronX Immigration intake team. We received your inquiry. Do you have a quick minute for a brief call to verify your details?"
        - Click Save Action.

        TASK 3: Action 2 (Wait)
        - Click the Wait action box.
        - Ensure the delay is exactly 2 Minutes.
        - Click Save Action.

        TASK 4: Action 3 (If/Else)
        - Click the If/Else action box.
        - Ensure the condition checks if the contact replied.
        - Click Save Action.

        TASK 5: The "No" Branch (Crucial)
        Under the "No" branch (or whatever branch represents 'did not reply'):
        1. Ensure there is a "Send SMS" action. (e.g. "Since we missed you, our AI assistant Alex will give you a quick call now.")
        2. Ensure there is a "Webhook" action (This is the Vapi trigger).
        3. If there are no tags, ADD an action: "Add Contact Tag", type "nx:new_lead" and hit enter, type "nx:ai_call_triggered" and hit enter. Save.
        4. If there is no field update, ADD an action: "Update Contact Field", select "ai_lead_score", enter value "10". Save.
        
        TASK 6: Publish
        - In the top right corner, toggle the switch from "Draft" to "Publish".
        - Click the blue "Save" button in the top right.
    `;

    console.log("Executing Skyvern Fix Task...");
    await agent.executeStep(instructions);
    
    console.log("Fix Task Completed.");
}

main().catch(console.error);
