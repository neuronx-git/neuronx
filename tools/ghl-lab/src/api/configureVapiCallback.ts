import dotenv from "dotenv";
import path from "path";
import fs from "fs";

dotenv.config({ path: path.join(__dirname, "../../.env") });

const VAPI_PRIVATE_KEY = process.env.VAPI_PRIVATE_KEY;
const ASSISTANT_FILE = path.join(__dirname, "../../.vapi_assistant.json");
const GHL_WEBHOOK_RESULT = path.join(__dirname, "../../.ghl_webhook_creation_result.json");

async function main() {
    console.log("Configuring Vapi Callback URL via API...");

    if (!VAPI_PRIVATE_KEY) {
        console.error("VAPI_PRIVATE_KEY missing in .env");
        process.exit(1);
    }

    if (!fs.existsSync(ASSISTANT_FILE)) {
        console.error("Assistant ID not found. Has the assistant been created?");
        process.exit(1);
    }

    if (!fs.existsSync(GHL_WEBHOOK_RESULT)) {
        console.error("GHL Webhook result not found. Was the workflow created?");
        process.exit(1);
    }

    const assistantData = JSON.parse(fs.readFileSync(ASSISTANT_FILE, "utf-8"));
    const webhookData = JSON.parse(fs.readFileSync(GHL_WEBHOOK_RESULT, "utf-8"));
    
    // Skyvern returns the extracted information in 'extracted_information' or sometimes inside the result object depending on the prompt.
    // In our prompt we asked it to return { webhookUrl: "..." }.
    // Let's check the result structure.
    
    let webhookUrl = webhookData.extracted_information?.webhookUrl;
    
    if (!webhookUrl) {
        // Fallback: Check if we can find a URL-like string in the extracted info or logs?
        // Actually, looking at the previous Skyvern run, extracted_information was null.
        // This means Skyvern failed to extract the text into the JSON structure, even though it completed the task.
        // BUT, we can ask the user to provide it if automation failed to scrape it.
        // OR, we can try to re-run the extraction step?
        // Wait, if Skyvern completed successfully, maybe it's in the output I missed?
        // The output showed "extracted_information": null.
        
        console.error("❌ Skyvern completed the workflow creation but failed to extract the URL into the JSON output.");
        console.error("This happens if the prompt didn't explicitly trigger the extraction logic correctly or the DOM was tricky.");
        console.error("Please manually paste the Webhook URL for WF-04B below to continue:");
        
        // We will fail here and ask the user, or we can try to inspect the screenshot? No.
        // Let's exit and prompt the user.
        process.exit(1);
    }

    console.log(`Using Assistant ID: ${assistantData.id}`);
    console.log(`Using Webhook URL: ${webhookUrl}`);

    const response = await fetch(`https://api.vapi.ai/assistant/${assistantData.id}`, {
        method: "PATCH",
        headers: {
            "Authorization": `Bearer ${VAPI_PRIVATE_KEY}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            serverUrl: webhookUrl
        })
    });

    if (!response.ok) {
        console.error(`Failed to update assistant: ${response.status} ${await response.text()}`);
        process.exit(1);
    }

    const updatedAssistant = await response.json();
    console.log("✅ Vapi Assistant Updated Successfully!");
    console.log("Server URL set to:", updatedAssistant.serverUrl);
}

main();