import dotenv from "dotenv";
import path from "path";
import fs from "fs";

dotenv.config({ path: path.join(__dirname, "../../.env") });

const VAPI_PRIVATE_KEY = process.env.VAPI_PRIVATE_KEY;
const ASSISTANT_FILE = path.join(__dirname, "../../.vapi_assistant.json");

async function main() {
    console.log("Updating Vapi Callback URL to new webhook...");

    if (!VAPI_PRIVATE_KEY) {
        console.error("VAPI_PRIVATE_KEY missing in .env");
        process.exit(1);
    }

    if (!fs.existsSync(ASSISTANT_FILE)) {
        console.error("Assistant ID not found. Has the assistant been created?");
        process.exit(1);
    }

    const assistantData = JSON.parse(fs.readFileSync(ASSISTANT_FILE, "utf-8"));
    const webhookUrl = "https://services.leadconnectorhq.com/hooks/FlRL82M0D6nclmKT7eXH/webhook-trigger/78a5bcc1-2528-4675-b356-0dbd42dd5aeb";

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
    
    // Update local file
    fs.writeFileSync(ASSISTANT_FILE, JSON.stringify(updatedAssistant, null, 2));
}

main();
