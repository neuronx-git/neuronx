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

const countries = ['India', 'Philippines', 'Nigeria', 'Brazil', 'UAE'];
const programs = ['Express Entry', 'Study Permit', 'Work Permit', 'Spousal Sponsorship', 'Visitor'];

const names = [
    'Aarav Patel', 'Priya Sharma', 'Rohan Singh', 'Diya Kumar', 'Vihaan Desai',
    'Maria Santos', 'Juan Dela Cruz', 'Jose Garcia', 'Anna Reyes', 'Pedro Mendoza',
    'Chinedu Okeke', 'Ngozi Eze', 'Ibrahim Abubakar', 'Amina Balogun', 'Oluwaseun Adebayo',
    'Lucas Silva', 'Julia Costa', 'Mateus Santos', 'Isabella Oliveira', 'Gabriel Pereira',
    'Ahmed Al Maktoum', 'Fatima Al Hashimi', 'Mohammed Al Farsi', 'Aisha Al Suwaidi', 'Omar Al Mansoori',
    'John Smith', 'Jane Doe', 'Michael Johnson', 'Emily Davis', 'David Wilson'
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

    const contactsToCreate = 30;
    const oppsConfig = [
        ...Array(5).fill(stages.NEW),
        ...Array(5).fill(stages.CONTACTING),
        ...Array(5).fill(stages.CONSULT_READY),
        ...Array(8).fill(stages.BOOKED),
        ...Array(4).fill(stages.RETAINED),
        ...Array(3).fill(stages.LOST)
    ];

    console.log(`Starting data population for Location: ${tokens.location_id}`);

    const createdContacts = [];

    for (let i = 0; i < contactsToCreate; i++) {
        const nameParts = names[i].split(' ');
        const country = countries[i % countries.length];
        const program = programs[i % programs.length];
        const email = `${nameParts[0].toLowerCase()}.${nameParts[1].toLowerCase()}@example.com`;
        const phone = `+1${Math.floor(Math.random() * 8000000000 + 2000000000)}`;

        console.log(`Creating contact ${i + 1}/${contactsToCreate}: ${names[i]}`);

        const contactData = {
            firstName: nameParts[0],
            lastName: nameParts[1],
            name: names[i],
            email: email,
            phone: phone,
            locationId: tokens.location_id,
            country: country,
            tags: ['demo-data', program.replace(' ', '-').toLowerCase()],
            customFields: [
                {
                    id: 'kuBPMaNdN6FJRfH9208q', // program_interest
                    field_value: program === 'Family Sponsorship' ? 'Spousal Sponsorship' : program
                }
            ]
        };

        const contactRes = await request('/contacts/', 'POST', tokens, contactData);
        if (!contactRes) continue;

        const contactId = contactRes.contact.id;
        createdContacts.push({ id: contactId, name: names[i], email, phone });

        // Assign opportunity
        const stageId = oppsConfig[i];
        let value = 0;
        if (stageId === stages.BOOKED) value = 150; // Consultation fee
        else if (stageId === stages.RETAINED) value = 3500 + Math.floor(Math.random() * 2000); // Retainer
        else if (stageId === stages.CONSULT_READY) value = 150;

        const oppData = {
            pipelineId: pipelineId,
            locationId: tokens.location_id,
            name: `${names[i]} - ${program}`,
            pipelineStageId: stageId,
            status: stageId === stages.RETAINED ? 'won' : (stageId === stages.LOST ? 'lost' : 'open'),
            contactId: contactId,
            monetaryValue: value
        };

        await request('/opportunities/', 'POST', tokens, oppData);

        // Add notes for conversation history on the first 5
        if (i < 5) {
            console.log(`Adding conversation history notes for ${names[i]}`);
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

        await delay(500); // rate limiting
    }

    console.log("Finished populating demo data.");
}

main().catch(console.error);