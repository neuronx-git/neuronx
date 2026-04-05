import fs from 'fs';
import path from 'path';

const VAPI_PRIVATE_KEY = "cb69d6fc-baf7-4881-8bff-20c7df251437";

async function request(endpoint: string, method: string, body?: any) {
    const url = `https://api.vapi.ai${endpoint}`;
    const options: any = {
        method,
        headers: {
            'Authorization': `Bearer ${VAPI_PRIVATE_KEY}`,
            'Content-Type': 'application/json'
        }
    };
    if (body) {
        options.body = JSON.stringify(body);
    }
    const response = await fetch(url, options);
    if (!response.ok) {
        const text = await response.text();
        console.error(`API Error ${method} ${endpoint}: ${response.status} ${text}`);
        return null;
    }
    return await response.json();
}

async function main() {
    console.log("Creating Vapi Assistant...");

    const systemPrompt = `You are Alex, the AI intake assistant for NeuronX Immigration Advisory, a premium Canadian immigration consulting firm. 

**Your Objective:**
You are calling a lead who just submitted an inquiry on our website. Your goal is to qualify their immigration needs, gather basic context, and invite them to book a formal strategy session with our licensed consultants.

**Your Persona:**
- Tone: Calm, professional, reassuring, and concise. 
- You are empathetic but efficient. Do not sound like an overly eager salesperson.
- You speak clearly and wait for the user to finish their thoughts before responding.

**STRICT GUARDRAILS (NEVER VIOLATE THESE):**
1. NEVER give legal advice.
2. NEVER predict the outcome of an application or assess eligibility.
3. If the user asks "Am I eligible?" or "Will I get approved?", you MUST say: "As an AI assistant, I cannot provide legal advice or assess eligibility. That is exactly what the licensed consultant will do during your strategy session."
4. If the user mentions DEPORTATION, REMOVAL ORDERS, CRIMINALITY, or MEDICAL INADMISSIBILITY, immediately trigger the escalate_to_human function.
5. If the user becomes angry, frustrated, or explicitly asks to speak to a human, immediately trigger the escalate_to_human function.

**Conversation Flow:**
1. Greeting: "Hi, is this {{first_name}}? ... Hi {{first_name}}, this is Alex calling from the intake team at NeuronX Immigration. I saw you just submitted an inquiry on our website. Do you have a quick minute to verify some details so we can pair you with the right consultant?"
2. If they say no/are busy: Say "No problem, I'll send you a text to reschedule. Have a great day!" and trigger end_call_summary.
3. If they say yes, proceed to ask the following qualification questions naturally, one at a time:
   - "What type of immigration program are you primarily interested in? (e.g., Express Entry, Study Permit, Sponsorship)"
   - "Are you currently living inside Canada, or applying from outside?"
   - "How quickly are you hoping to move forward? Is there an immediate deadline, or are you planning for the next 3 to 6 months?"
   - "Have you ever had a visa or immigration application refused by Canada in the past?"
   - "Our consultants charge a standard professional fee for the formal case assessment. Are you comfortable proceeding with a paid consultation to get a formal legal strategy?"
4. Booking Close (If qualified and accepts budget): "Thank you for sharing that. Based on what you've told me, the next step is a formal strategy session. I can send a secure booking link directly to your phone right now so you can pick a time that works for you. Does that sound good?"
   - If Yes: "Perfect. I've just sent that text message. The consultant will review all our notes today to prepare for your meeting. Have a great day!" -> Trigger schedule_consultation then end_call_summary.
   - If No/Declines Budget: "I understand. We do charge a fee for formal legal assessments. I'll email you some free resources for now, and you can reach back out whenever you feel ready." -> Trigger end_call_summary.`;

    const assistantBody = {
        name: "NeuronX Intake Agent",
        model: {
            provider: "openai",
            model: "gpt-4o-mini",
            messages: [
                {
                    role: "system",
                    content: systemPrompt
                }
            ],
            tools: [
                {
                    type: "function",
                    messages: [],
                    function: {
                        name: "capture_lead_data",
                        description: "Store qualification data gathered from the lead during the conversation.",
                        parameters: {
                            type: "object",
                            properties: {
                                program_interest: { type: "string", enum: ["Express Entry", "Study Permit", "Work Permit", "Family Sponsorship", "Visitor Visa", "PNP", "Other"] },
                                country: { type: "string" },
                                urgency: { type: "string", enum: ["Immediate", "1-3 months", "3-6 months", "6+ months"] },
                                complexity_flag: { type: "string", enum: ["None", "Previous Refusal", "Criminality", "Deportation", "Medical Inadmissibility"] }
                            },
                            required: []
                        }
                    }
                },
                {
                    type: "function",
                    messages: [],
                    function: {
                        name: "escalate_to_human",
                        description: "Instantly ends the AI flow and flags the lead for emergency human intervention. Use when user asks for legal advice, mentions deportation/criminality, or becomes angry.",
                        parameters: {
                            type: "object",
                            properties: {
                                reason: { type: "string" },
                                requires_human: { type: "boolean" }
                            },
                            required: ["reason", "requires_human"]
                        }
                    }
                },
                {
                    type: "function",
                    messages: [],
                    function: {
                        name: "schedule_consultation",
                        description: "Flags that the user has agreed to receive a consultation booking link.",
                        parameters: {
                            type: "object",
                            properties: {
                                booking_status: { type: "string", enum: ["Requested", "Declined"] }
                            },
                            required: ["booking_status"]
                        }
                    }
                },
                {
                    type: "function",
                    messages: [],
                    function: {
                        name: "end_call_summary",
                        description: "Compiles the final summary of the call before hanging up.",
                        parameters: {
                            type: "object",
                            properties: {
                                call_outcome: { type: "string", enum: ["Qualified", "Not Ready", "Voicemail", "Reschedule"] },
                                summary: { type: "string" }
                            },
                            required: ["call_outcome", "summary"]
                        }
                    }
                }
            ]
        },
        voice: {
            provider: "11labs",
            voiceId: "EXAVITQu4vr4xnSDxMaL" // Sarah / Professional Female
        },
        transcriber: {
            provider: "deepgram",
            model: "nova-2",
            language: "en-US"
        },
        firstMessage: "Hi, is this {{first_name}}?",
        voicemailMessage: "Hi {{first_name}}, this is Alex from NeuronX Immigration. We're calling about your immigration inquiry. We want to make sure you get the help you need. I'll send you a quick text message with a link to schedule a time to speak with our consultants. Talk to you soon!",
        endCallPhrases: ["Have a great day!", "Talk to you soon!", "Goodbye."],
        silenceTimeoutSeconds: 30,
        responseDelaySeconds: 0.8,
        backgroundSound: "office",
        serverUrl: "https://hook.us1.make.com/placeholder-url" // To be updated
    };

    const res = await request('/assistant', 'POST', assistantBody);
    
    if (res && res.id) {
        console.log(`✅ Assistant created successfully! ID: ${res.id}`);
        fs.writeFileSync(path.join(__dirname, '../../.vapi_assistant.json'), JSON.stringify(res, null, 2));
    } else {
        console.error("Failed to create assistant.");
    }
}

main().catch(console.error);