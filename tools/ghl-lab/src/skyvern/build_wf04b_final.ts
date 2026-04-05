import dotenv from "dotenv";
import path from "path";
import { SkyvernAgent } from "./SkyvernAgent";

dotenv.config({ path: path.join(__dirname, "../../.env") });

async function main() {
    console.log("Starting Chunked Execution for WF-04B...");
    
    if (!process.env.SKYVERN_API_KEY) {
        throw new Error("SKYVERN_API_KEY is required");
    }

    const agent = new SkyvernAgent();
    await agent.createSession(); 
    
    const LOCATION_ID = "FlRL82M0D6nclmKT7eXH"; 
    const WORKFLOW_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;
    
    const chunk1 = `
        Navigate to ${WORKFLOW_URL}.
        Wait for the workflows list to load.
        Search for "WF-04B" in the search bar.
        Click on "WF-04B - AI Call Receiver".
        Wait for the workflow builder to load.
        
        Click the "+" button below the webhook trigger.
        Search for "Update Contact Field" and click it.
        Select "ai_summary" from the field dropdown.
        In the value box, type: {% raw %}{{inboundWebhook.summary}}{% endraw %}
        Click "Save Action".
        
        Click the "+" button again.
        Search for "Update Contact Field" and click it.
        Select "ai_transcript" from the field dropdown.
        In the value box, type: {% raw %}{{inboundWebhook.transcript}}{% endraw %}
        Click "Save Action".
        
        Click the blue "Save" button in the top right to save the workflow.
    `;

    const chunk2 = `
        You are in the workflow builder for WF-04B.
        Click the "+" button at the very bottom of the workflow.
        Search for "Update Contact Field" and click it.
        Select "ai_call_id" from the field dropdown.
        In the value box, type: {% raw %}{{inboundWebhook.call.id}}{% endraw %}
        Click "Save Action".
        
        Click the "+" button at the very bottom again.
        Search for "Update Contact Field" and click it.
        Select "ai_call_duration" from the field dropdown.
        In the value box, type: {% raw %}{{inboundWebhook.call.duration}}{% endraw %}
        Click "Save Action".
        
        Click the blue "Save" button in the top right to save the workflow.
    `;

    const chunk3 = `
        You are in the workflow builder for WF-04B.
        Click the "+" button at the very bottom of the workflow.
        Search for "Update Contact Field" and click it.
        Select "ai_program_interest" from the field dropdown.
        In the value box, type: {% raw %}{{inboundWebhook.structuredData.program_interest}}{% endraw %}
        Click "Save Action".
        
        Click the "+" button at the very bottom again.
        Search for "Update Contact Field" and click it.
        Select "ai_country" from the field dropdown.
        In the value box, type: {% raw %}{{inboundWebhook.structuredData.country}}{% endraw %}
        Click "Save Action".
        
        Click the blue "Save" button in the top right.
    `;
    
    try {
        console.log("--- Executing Chunk 1 ---");
        await agent.executeStep(chunk1);
        console.log("--- Executing Chunk 2 ---");
        await agent.executeStep(chunk2);
        console.log("--- Executing Chunk 3 ---");
        await agent.executeStep(chunk3);
        console.log("Completed!");
    } catch (e) {
        console.error("Execution failed:", e);
    }
}

main();
