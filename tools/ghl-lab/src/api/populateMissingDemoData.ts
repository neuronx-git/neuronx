import fs from 'fs';
import path from 'path';

const pipelineId = 'Dtj9nQVd3QjL7bAb3Aiw';
const stages = {
    NEW: 'b319c338-215f-44fe-a0da-0c0c7a1f84a4',
    CONTACTING: 'f08d0408-dc0c-4809-ae88-0b5631cc22fc',
    CONSULT_READY: '231d5e26-2ea7-43a9-b91c-dd0b21971983',
    BOOKED: '07348d98-10a3-400d-b2de-a770dd9fa8c6',
    RETAINED: '618ef749-6c96-4eca-b144-fe87064e549c',
    LOST: 'ed164220-700e-42ef-a89d-1b198ef1c229'
};

const programs = ['Express Entry', 'Study Permit', 'Work Permit', 'Spousal Sponsorship', 'Visitor'];

const missingNames = [
    'Vihaan Desai', 'Pedro Mendoza', 'Oluwaseun Adebayo', 'Gabriel Pereira', 'Omar Al Mansoori', 'David Wilson'
];

// Reconstruct the missing opps config
const missingOpps = [
    stages.NEW, // Vihaan was index 4 (0-4 is NEW)
    stages.CONTACTING, // Pedro was index 9 (5-9 is CONTACTING)
    stages.CONSULT_READY, // Oluwaseun was index 14 (10-14 is CONSULT_READY)
    stages.BOOKED, // Gabriel was index 19 (15-22 is BOOKED)
    stages.RETAINED, // Omar was index 24 (23-26 is RETAINED)
    stages.LOST // David was index 29 (27-29 is LOST)
];

async function delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

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
    const tokens = JSON.parse(fs.readFileSync(tokenPath, 'utf8'));

    for (let i = 0; i < missingNames.length; i++) {
        const nameParts = missingNames[i].split(' ');
        const country = 'AE'; // ISO code for UAE
        // The original logic had program = programs[i % programs.length] but based on original index.
        // The original indices were: 4, 9, 14, 19, 24, 29.
        // 4 % 5 = 4 (Visitor)
        // 9 % 5 = 4 (Visitor)
        // 14 % 5 = 4 (Visitor)
        const program = 'Visitor'; // They were all index % 5 = 4
        
        const email = `${nameParts[0].toLowerCase()}.${nameParts[1].toLowerCase()}@example.com`;
        const phone = `+1${Math.floor(Math.random() * 8000000000 + 2000000000)}`;

        console.log(`Creating missing contact: ${missingNames[i]}`);

        const contactData = {
            firstName: nameParts[0],
            lastName: nameParts[1],
            name: missingNames[i],
            email: email,
            phone: phone,
            locationId: tokens.location_id,
            country: country,
            tags: ['demo-data', program.replace(' ', '-').toLowerCase()],
            customFields: [
                {
                    id: 'kuBPMaNdN6FJRfH9208q',
                    field_value: program
                }
            ]
        };

        const contactRes = await request('/contacts/', 'POST', tokens, contactData);
        if (!contactRes) continue;

        const contactId = contactRes.contact.id;

        // Assign opportunity
        const stageId = missingOpps[i];
        let value = 0;
        if (stageId === stages.BOOKED) value = 150;
        else if (stageId === stages.RETAINED) value = 3500 + Math.floor(Math.random() * 2000);
        else if (stageId === stages.CONSULT_READY) value = 150;

        const oppData = {
            pipelineId: pipelineId,
            locationId: tokens.location_id,
            name: `${missingNames[i]} - ${program}`,
            pipelineStageId: stageId,
            status: stageId === stages.RETAINED ? 'won' : (stageId === stages.LOST ? 'lost' : 'open'),
            contactId: contactId,
            monetaryValue: value
        };

        await request('/opportunities/', 'POST', tokens, oppData);
        
        if (i === 0) {
            // First one was Vihaan Desai (index 4 in original), which needs conversation history
            console.log(`Adding conversation history notes for ${missingNames[i]}`);
            const noteText = `[SMS Exchange] 
Agent: Hi ${nameParts[0]}, we received your inquiry for ${program}. Are you available for a quick chat?
Lead: Yes, tomorrow works.
[Consultation Reminder]
System: Reminder for your consultation tomorrow at 2PM.
[Intake Discussion]
Agent: Lead is interested in ${program} from ${country}. Seems qualified.`;

            await request(`/contacts/${contactId}/notes`, 'POST', tokens, {
                body: noteText,
                userId: tokens.user_id || undefined
            });
        }

        await delay(500);
    }
}

main().catch(console.error);