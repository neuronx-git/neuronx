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
    console.log("Fetching Phone Numbers from Vapi...");

    // Now that the UI has potentially claimed a free number, let's fetch the numbers via API to get the ID.
    const res = await request('/phone-number', 'GET');
    
    if (res && res.length > 0) {
        console.log(`✅ Found ${res.length} phone number(s)!`);
        
        // Take the first number
        const phoneNumber = res[0];
        console.log(`Using Phone Number ID: ${phoneNumber.id} (${phoneNumber.number})`);

        fs.writeFileSync(path.join(__dirname, '../../.vapi_phone.json'), JSON.stringify(phoneNumber, null, 2));

        // Read the assistant ID
        const assistantDataPath = path.join(__dirname, '../../.vapi_assistant.json');
        if (fs.existsSync(assistantDataPath)) {
            const assistant = JSON.parse(fs.readFileSync(assistantDataPath, 'utf8'));
            
            // Link it if it's not already linked
            if (phoneNumber.assistantId !== assistant.id) {
                console.log("Linking Phone Number to Assistant...");
                const updateRes = await request(`/phone-number/${phoneNumber.id}`, 'PATCH', {
                    assistantId: assistant.id,
                    name: "NeuronX Intake Line"
                });
                if (updateRes) {
                    console.log("✅ Phone Number successfully linked to the Assistant.");
                }
            } else {
                console.log("✅ Phone Number is already linked to the Assistant.");
            }
        }

    } else {
        console.error("Failed to find any phone numbers. Skyvern UI execution may have failed or no free numbers were available.");
    }
}

main().catch(console.error);