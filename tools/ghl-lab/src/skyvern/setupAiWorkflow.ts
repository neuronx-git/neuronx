import { SkyvernAgent } from "../skyvern/SkyvernAgent";

async function main() {
    const agent = new SkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        const url = await agent.createSession();
        console.log("\n!!! ACTION REQUIRED !!!");
        console.log(`Please open this URL and LOG IN: ${url}`);
        process.exit(0);
    }

    const LOCATION_ID = "FlRL82M0D6nclmKT7eXH"; // Demo Lab Tenant
    const WORKFLOWS_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automations`;

    try {
        console.log("Setting up WF-01A (AI Speed-to-Lead) Workflow...");

        // Note: Creating a workflow from scratch via Skyvern is highly complex due to the drag-and-drop canvas.
        // We will attempt a simplified prompt, but acknowledge this is the hardest boundary of UI automation.
        
        const result = await agent.executeStep(
            `Navigate to Automations. 
             Click "Create workflow" then "Start from scratch".
             Name the workflow "WF-01A — AI Speed-to-Lead Initialization".
             Add a Trigger: "Form Submitted". Select the "Immigration Inquiry (V1)" form.
             Add Action 1: "Wait" for 1 minute.
             Add Action 2: "Webhook". Method: POST. URL: "https://api.vapi.ai/call/outbound" (or a placeholder like https://hook.us1.make.com/placeholder).
             Add Action 3: "Add Contact Tag". Tag: "nx:ai_call_initiated".
             Save and Publish the workflow.`,
            WORKFLOWS_URL
        );

        console.log("Workflow Creation Result:", JSON.stringify(result, null, 2));

        const fs = require('fs');
        const path = require('path');
        
        const reportPath = path.join(__dirname, '../../../../AI_LAYER_SETUP_EXECUTION_REPORT.md');
        const reportContent = `# AI Layer Setup Execution Report\n\n## Automation Status\n\n- API Data Schema Setup: ✅ Completed (Custom Fields & Tags created)\n- Workflow Automation Setup: ${result.is_success ? '✅ Success' : '⚠️ Partial / Blocked'}\n\n## Skyvern Execution Log\n\n\`\`\`json\n${JSON.stringify(result, null, 2)}\n\`\`\`\n\nIf blocked, manual creation of WF-01A is required due to iframe/canvas limitations in the GHL workflow builder.`;
        
        fs.writeFileSync(reportPath, reportContent);
        console.log("Report saved to AI_LAYER_SETUP_EXECUTION_REPORT.md");

    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();