import { VapiSkyvernAgent } from "./VapiSkyvernAgent";
import readline from "readline";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function main() {
    const agent = new VapiSkyvernAgent();
    const resumed = await agent.loadSession();
    
    if (!resumed) {
        const url = await agent.createSession();
        console.log("\n========================================================");
        console.log("🚨 ACTION REQUIRED: VAPI AUTHENTICATION BOOTSTRAP 🚨");
        console.log("========================================================");
        console.log(`1. Open this URL in your browser: ${url}`);
        console.log(`2. Log into your Vapi account (https://dashboard.vapi.ai).`);
        console.log(`3. Once you see the Vapi dashboard, close the browser tab.`);
        console.log(`4. Press ENTER in this terminal to continue.`);
        console.log("========================================================");
        
        rl.question('', () => {
            console.log("Auth assumed complete. Session saved to .vapi-skyvern-session.json");
            rl.close();
            process.exit(0);
        });
    } else {
        console.log("Vapi Session already active. You can run the provisioning script.");
        rl.close();
    }
}

main();