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
    await agent.createSession(); // Create a fresh session
    
    const LOCATION_ID = "FlRL82M0D6nclmKT7eXH"; 
    const WORKFLOW_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;
    
    // Chunk 1: Navigate and first 3 fields
    const chunk1 = `
        Navigate to ${WORKFLOW_URL}.
        Wait for the workflows list to load.
        Search for "WF-04B" in the search bar.
        Click on "WF-04B - AI Call Receiver".
        Wait for the workflow builder to load.
        
        If the trigger is not "Inbound Webhook", click it and set it to "Inbound Webhook", then save.
        
        Add 3 "Update Contact Field" actions right after the webhook:
        1. Click '+', search 'Update Contact Field'. Select field 'ai_summary'. Value: {% raw %}{{inboundWebhook.summary}}{% endraw %}. Click Save Action.
        2. Click '+', search 'Update Contact Field'. Select field 'ai_transcript'. Value: {% raw %}{{inboundWebhook.transcript}}{% endraw %}. Click Save Action.
        3. Click '+', search 'Update Contact Field'. Select field 'ai_call_id'. Value: {% raw %}{{inboundWebhook.call.id}}{% endraw %}. Click Save Action.
        
        Click the blue "Save" button in the top right to save the workflow.
    `;

    // Chunk 2: Next 4 fields
    const chunk2 = `
        You are in the workflow builder for WF-04B.
        Add 4 more "Update Contact Field" actions at the bottom of the current sequence:
        1. Click '+', search 'Update Contact Field'. Select field 'ai_call_duration'. Value: {% raw %}{{inboundWebhook.call.duration}}{% endraw %}. Save Action.
        2. Click '+', search 'Update Contact Field'. Select field 'ai_program_interest'. Value: {% raw %}{{inboundWebhook.structuredData.program_interest}}{% endraw %}. Save Action.
        3. Click '+', search 'Update Contact Field'. Select field 'ai_country'. Value: {% raw %}{{inboundWebhook.structuredData.country}}{% endraw %}. Save Action.
        4. Click '+', search 'Update Contact Field'. Select field 'ai_urgency'. Value: {% raw %}{{inboundWebhook.structuredData.urgency}}{% endraw %}. Save Action.
        
        Click the blue "Save" button in the top right.
    `;

    // Chunk 3: Next 4 fields
    const chunk3 = `
        You are in the workflow builder for WF-04B.
        Add 4 more "Update Contact Field" actions at the bottom:
        1. Click '+', search 'Update Contact Field'. Select field 'ai_lead_score'. Value: {% raw %}{{inboundWebhook.structuredData.lead_score}}{% endraw %}. Save Action.
        2. Click '+', search 'Update Contact Field'. Select field 'ai_complexity_flag'. Value: {% raw %}{{inboundWebhook.structuredData.complexity_flag}}{% endraw %}. Save Action.
        3. Click '+', search 'Update Contact Field'. Select field 'ai_booking_status'. Value: {% raw %}{{inboundWebhook.structuredData.booking_status}}{% endraw %}. Save Action.
        4. Click '+', search 'Update Contact Field'. Select field 'ai_requires_human'. Value: {% raw %}{{inboundWebhook.structuredData.requires_human}}{% endraw %}. Save Action.
        
        Click the blue "Save" button in the top right.
    `;
    
    // Chunk 4: Final fields and Tag
    const chunk4 = `
        You are in the workflow builder for WF-04B.
        Add these actions at the bottom:
        1. Click '+', search 'Update Contact Field'. Select field 'ai_sentiment'. Value: {% raw %}{{inboundWebhook.structuredData.sentiment}}{% endraw %}. Save Action.
        2. Click '+', search 'Update Contact Field'. Select field 'last_contact_attempt_outcome'. Value: {% raw %}{{inboundWebhook.structuredData.call_outcome}}{% endraw %}. Save Action.
        3. Click '+', search 'Update Contact Field'. Select field 'last_contact_attempt_method'. Value: "AI Call". Save Action.
        4. Click '+', search 'Add Contact Tag'. Type "nx:contacted" and hit enter. Save Action.
        
        Click the blue "Save" button in the top right.
    `;

    // Execute sequentially
    try {
        console.log("--- Executing Chunk 1/4 ---");
        await agent.executeStep(chunk1);
        
        console.log("--- Executing Chunk 2/4 ---");
        await agent.executeStep(chunk2);
        
        console.log("--- Executing Chunk 3/4 ---");
        await agent.executeStep(chunk3);
        
        console.log("--- Executing Chunk 4/4 ---");
        await agent.executeStep(chunk4);
        
        console.log("All chunks completed successfully!");
    } catch (e) {
        console.error("Execution failed:", e);
    }
}

main();
