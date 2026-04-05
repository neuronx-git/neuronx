import fs from 'fs';
import path from 'path';

async function testApi() {
    const tokenPath = path.join(__dirname, '../../.tokens.json');
    const tokens = JSON.parse(fs.readFileSync(tokenPath, 'utf8'));
    
    const response = await fetch(`https://services.leadconnectorhq.com/opportunities/pipelines?locationId=${tokens.location_id}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${tokens.access_token}`,
            'Version': '2021-07-28',
            'Accept': 'application/json'
        }
    });

    const data = await response.json();
    console.log(JSON.stringify(data, null, 2));
}

testApi().catch(console.error);