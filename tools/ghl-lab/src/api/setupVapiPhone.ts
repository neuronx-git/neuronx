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
    console.log("Purchasing Vapi Phone Number...");

    const assistantDataPath = path.join(__dirname, '../../.vapi_assistant.json');
    if (!fs.existsSync(assistantDataPath)) {
        console.error("Assistant not found. Run setupVapiAssistant.ts first.");
        return;
    }
    const assistant = JSON.parse(fs.readFileSync(assistantDataPath, 'utf8'));

    // Buy a new phone number through Vapi (uses Twilio under the hood via Vapi API)
    const phoneBody = {
        provider: "vapi",
        number: "+1", // Just a dummy request for the first available US/Canada number. Note: Vapi's API might require specific formatting or a `buy` endpoint.
        // For Vapi API v1, to buy a number you just post to /phone-number with the provider.
        assistantId: assistant.id,
        name: "NeuronX Intake Line"
    };

    // Let's attempt to buy a number
    let res = await request('/phone-number/buy', 'POST', { areaCode: "647" }); // Attempt Toronto area code

    if (!res || res.error) {
        console.log("Failed to buy specific area code. Attempting to buy any US/CA number...");
        res = await request('/phone-number/buy', 'POST', {});
    }

    if (res && res.id) {
        console.log(`✅ Phone Number purchased! ID: ${res.id}, Number: ${res.number}`);
        
        // Now link it to the assistant
        const updateRes = await request(`/phone-number/${res.id}`, 'PATCH', {
            assistantId: assistant.id,
            name: "NeuronX Intake Line"
        });

        if (updateRes) {
            console.log("✅ Phone Number successfully linked to the Assistant.");
            fs.writeFileSync(path.join(__dirname, '../../.vapi_phone.json'), JSON.stringify(updateRes, null, 2));
        }
    } else {
        console.error("Failed to purchase phone number. You may need to add a credit card to your Vapi account manually.");
    }
}

main().catch(console.error);