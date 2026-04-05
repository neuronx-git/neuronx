import { SkyvernAgent } from "./SkyvernAgent";
import fs from "fs";
import path from "path";

async function main() {
    const agent = new SkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        const url = await agent.createSession();
        console.log("ACTION REQUIRED: Log into GHL at " + url);
        process.exit(0);
    }

    const VAPI_PAYLOAD = JSON.stringify({
        phoneNumberId: "43e01c63-f342-4a5c-84e8-5cd54810dd68",
        customer: {
            number: "{{contact.phone}}",
            name: "{{contact.first_name}}"
        },
        assistantId: "289a9701-9199-4d03-9416-49d18bec2f69",
        assistantOverrides: {
            variableValues: {
                first_name: "{{contact.first_name}}",
                contact_id: "{{contact.id}}"
            }
        }
    });

    try {
        console.log("Configuring GHL Webhook with Vapi Payload...");

        const result = await agent.executeStep(
            `Navigate to https://app.gohighlevel.com.
             1. Go to 'Automation' > 'Workflows'.
             2. Search for and open 'WF-01A'.
             3. Find the 'Webhook' action (it might be labeled 'Custom Webhook' or 'POST').
             4. Click on it to edit.
             5. Ensure the Method is POST and the URL is 'https://api.vapi.ai/call/phone'.
             6. In the Body/Payload section, select 'Custom Data' or 'Raw JSON'.
             7. Paste exactly this JSON into the raw body field:
                ${VAPI_PAYLOAD}
             8. Make sure to add a Header: Key='Authorization', Value='Bearer 46b108ac-57bc-42a7-9f22-f3365b387ae8'.
             9. Click Save Action.
             10. Click Save Workflow in the top right.`,
            "https://app.gohighlevel.com"
        );

        console.log("GHL Webhook Configuration Result:", JSON.stringify(result, null, 2));

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();