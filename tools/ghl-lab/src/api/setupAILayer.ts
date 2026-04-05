import fs from 'fs';
import path from 'path';

async function request(endpoint: string, method: string, tokens: any, body?: any) {
    const url = `https://services.leadconnectorhq.com${endpoint}`;
    const options: any = {
        method,
        headers: {
            'Authorization': `Bearer ${tokens.access_token}`,
            'Version': '2021-07-28',
            'Accept': 'application/json',
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
    const tokenPath = path.join(__dirname, '../../.tokens.json');
    if (!fs.existsSync(tokenPath)) {
        console.log("No tokens found. Skipping execution.");
        return;
    }
    const tokens = JSON.parse(fs.readFileSync(tokenPath, 'utf8'));
    const locationId = tokens.location_id;

    console.log(`Setting up AI Layer fields for location: ${locationId}`);

    // Create a folder for AI Fields first if possible, but for simplicity we will just create the fields.
    const newFields = [
        { name: "ai_program_interest", dataType: "TEXT", placeholder: "AI Extracted Program" },
        { name: "ai_country", dataType: "TEXT", placeholder: "AI Extracted Country" },
        { name: "ai_urgency", dataType: "SINGLE_OPTIONS", options: ["Immediate", "1-3 months", "3-6 months", "6+ months"] },
        { name: "ai_complexity_flag", dataType: "TEXT", placeholder: "e.g. Refusal, Criminality" },
        { name: "ai_lead_score", dataType: "NUMERICAL", placeholder: "0-100" },
        { name: "ai_call_outcome", dataType: "SINGLE_OPTIONS", options: ["Qualified", "Not Ready", "Voicemail", "Disconnected"] },
        { name: "ai_requires_human", dataType: "CHECKBOX", options: ["Yes", "No"] },
        { name: "ai_booking_status", dataType: "SINGLE_OPTIONS", options: ["Requested", "Declined", "Unclear"] },
        { name: "ai_summary", dataType: "LARGE_TEXT", placeholder: "AI Call Summary" }
    ];

    for (const field of newFields) {
        const body: any = {
            name: field.name,
            dataType: field.dataType,
            placeholder: field.placeholder || "",
            model: "contact"
        };
        if (field.options) {
            body.options = field.options;
        }

        console.log(`Creating field: ${field.name}...`);
        const res = await request(`/locations/${locationId}/customFields`, 'POST', tokens, body);
        if (res) {
            console.log(`✅ Success: ${field.name}`);
        }
        // sleep 500ms to avoid rate limits
        await new Promise(r => setTimeout(r, 500));
    }

    // Create tags
    const tags = ["nx:ai_call_initiated", "nx:human_escalation", "nx:score:high", "nx:score:med", "nx:score:low", "nx:score:junk"];
    for (const tag of tags) {
        console.log(`Creating tag: ${tag}...`);
        const res = await request(`/locations/${locationId}/tags`, 'POST', tokens, { name: tag });
        if (res) {
            console.log(`✅ Success: ${tag}`);
        }
        await new Promise(r => setTimeout(r, 500));
    }

    console.log("AI Setup Complete.");
}

main().catch(console.error);