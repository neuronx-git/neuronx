import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
    const agent = new SkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        const url = await agent.createSession();
        console.log("\n!!! ACTION REQUIRED !!!");
        console.log(`Please open this URL and LOG IN: ${url}`);
        process.exit(0);
    }

    const LOCATION_ID = "FlRL82M0D6nclmKT7eXH"; 
    const FUNNELS_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/funnels-websites/funnels`;

    try {
        console.log("Extracting Funnel Information...");

        const result = await agent.executeStep(
            `Navigate to Sites > Funnels.
             For each funnel listed:
             1. Note the funnel name
             2. Click on it to see steps
             3. For each step, click the "Link" or "Preview" icon to get the public URL
             4. Return a summary with: Funnel Name, Step Name, Public URL, Preview URL, Status (Published/Draft)`,
            FUNNELS_URL
        );

        console.log("Funnel Extraction Result:", JSON.stringify(result, null, 2));

        const fs = require('fs');
        const path = require('path');
        
        const reportPath = path.join(__dirname, '../../../../NEURONX_FUNNEL_URLS_REPORT.md');
        const reportContent = `# NeuronX Funnel URLs Report\n\n## Verification Results\n\n${JSON.stringify(result, null, 2)}\n`;
        
        fs.writeFileSync(reportPath, reportContent);
        console.log("Report saved to NEURONX_FUNNEL_URLS_REPORT.md");

    } catch (e) { console.error("Failed", e); }
}

main();