import dotenv from "dotenv";
import path from "path";
import fs from "fs";

dotenv.config({ path: path.join(__dirname, "../../.env") });

const VAPI_PRIVATE_KEY = process.env.VAPI_PRIVATE_KEY;
const ASSISTANT_FILE = path.join(__dirname, "../../.vapi_assistant.json");

async function main() {
    console.log("Upgrading Vapi Assistant with Human Handoff & Language Support...");

    if (!VAPI_PRIVATE_KEY) {
        console.error("VAPI_PRIVATE_KEY missing in .env");
        process.exit(1);
    }

    if (!fs.existsSync(ASSISTANT_FILE)) {
        console.error("Assistant ID not found.");
        process.exit(1);
    }

    const assistantData = JSON.parse(fs.readFileSync(ASSISTANT_FILE, "utf-8"));

    const systemPrompt = `
You are Alex, the AI intake assistant for NeuronX Immigration Advisory.

**OBJECTIVE:**
Qualify leads for Canadian immigration services. Be professional, empathetic, and concise.

**LANGUAGE PROTOCOL:**
1. **Start EVERY call** by asking: "Hi, this is Alex from NeuronX Immigration. Do you prefer to speak in English, or would another language be better?"
2. If they say a language other than English (e.g., Spanish, French, Hindi, Punjabi, Mandarin), **IMMEDIATELY SWITCH** to that language and continue the conversation fluently in that language.
3. Use the user's preferred language for the rest of the call.

**HUMAN HANDOFF PROTOCOL:**
1. If the user asks to speak to a human, gets angry, or asks a complex legal question you cannot answer:
   - Say: "I understand. Let me transfer you to a senior consultant immediately. Please hold."
   - Trigger the 'transferCall' function to forward the call.

**QUALIFICATION FLOW (After language is set):**
1. "What type of immigration program are you interested in? (Work, Study, Sponsorship, etc.)"
2. "Are you currently inside Canada or outside?"
3. "Do you have any prior refusals or legal issues we should know about?"

**GUARDRAILS:**
- NEVER give legal advice.
- If asked about eligibility, say: "Our licensed consultants will assess that in detail during the strategy session."
`;

    const response = await fetch(`https://api.vapi.ai/assistant/${assistantData.id}`, {
        method: "PATCH",
        headers: {
            "Authorization": `Bearer ${VAPI_PRIVATE_KEY}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            model: {
                messages: [
                    {
                        role: "system",
                        content: systemPrompt
                    }
                ],
                provider: "openai",
                model: "gpt-4o",
                tools: [
                    {
                        "type": "function",
                        "function": {
                            "name": "transferCall",
                            "description": "Transfers the call to a human agent.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "destination": { 
                                        "type": "string", 
                                        "description": "The phone number to transfer to (e.g. +16475550199)." 
                                    }
                                },
                                "required": ["destination"]
                            }
                        }
                    }
                ]
            },
            firstMessage: "Hi, this is Alex from NeuronX. Do you prefer English or another language?",
            voice: {
                provider: "11labs",
                voiceId: "EXAVITQu4vr4xnSDxMaL"
            },
            forwardingPhoneNumber: "+16479315181" 
        })
    });

    if (!response.ok) {
        console.error(`Failed to upgrade assistant: ${response.status} ${await response.text()}`);
        process.exit(1);
    }

    const updated = await response.json();
    console.log("✅ Vapi Assistant Upgraded Successfully!");
    console.log("- Multi-language support enabled (GPT-4o)");
    console.log("- Human Handoff enabled");

    fs.writeFileSync(ASSISTANT_FILE, JSON.stringify(updated, null, 2));
}

main();
