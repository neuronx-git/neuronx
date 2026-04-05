import { VapiSkyvernAgent } from "./VapiSkyvernAgent";

async function main() {
    const agent = new VapiSkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        console.error("Session missing");
        process.exit(1);
    }

    try {
        console.log("Re-verifying Vapi Dashboard...");

        // Try a more explicit prompt just to click the "Buy Number" button, sometimes the modal needs multiple explicit steps
        const result = await agent.executeStep(
            `Navigate to https://dashboard.vapi.ai/phone-numbers.
             1. Look for a button that says 'Buy Number' or '+ Add Number'. Click it.
             2. A modal will open showing available numbers. Click 'Buy' next to the first number in the list.
             3. If there is a confirmation prompt, confirm it.
             4. Wait for the page to refresh.`,
            "https://dashboard.vapi.ai/phone-numbers"
        );

        console.log("Vapi UI Execution Result:", JSON.stringify(result, null, 2));
    } catch (e) { 
        console.error("Failed", e); 
    }
}

main();