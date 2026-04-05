import { SkyvernAgent } from "./SkyvernAgent";
import * as fs from 'fs';
import * as path from 'path';

async function main() {
  const agent = new SkyvernAgent();
  
  const resumed = await agent.loadSession();
  
  if (!resumed) {
      console.log("No valid Skyvern session found. Please run skyvernOrchestrator.ts first to log in.");
      process.exit(1);
  }

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const URL_WORKFLOWS_LIST = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;

  try {
      console.log("\nTrying to find the newly created WF-04B and extract the URL...");
      
      const result1 = await agent.executeStep(
          "Navigate to the 'Automation' > 'Workflows' page. Find the workflow named 'WF-04B - AI Call Receiver' and click on it to open the builder.",
          URL_WORKFLOWS_LIST
      );
      console.log("Step 1 (Open Workflow) Complete:", result1.status);

      const result2 = await agent.executeStep(
          "Click on the 'Inbound Webhook' trigger box to open its settings panel on the right. In the right panel, find the 'Webhook URL' input field. Copy the exact text inside that field. Return it in your extraction output using this exact JSON schema: {\"webhook_url\": \"the_url_you_copied\"}. Do not return anything else.",
          null
      );
      console.log("Step 2 (Extract URL) Complete:", result2.status);
      
      let extractedUrl = "NOT_FOUND";
      if (result2.extracted_information) {
         try {
             const info = typeof result2.extracted_information === 'string' 
                ? JSON.parse(result2.extracted_information) 
                : result2.extracted_information;
             extractedUrl = info.webhook_url || "NOT_FOUND";
         } catch(e) {
             console.log("Failed to parse extracted info:", result2.extracted_information);
             extractedUrl = result2.extracted_information;
         }
      }
      
      console.log("Extracted Webhook URL:", extractedUrl);
      
      if (extractedUrl !== "NOT_FOUND" && typeof extractedUrl === 'string' && extractedUrl.startsWith('http')) {
        const outputPath = path.join(__dirname, '..', '..', '.ghl_webhook_url.json');
        fs.writeFileSync(outputPath, JSON.stringify({ webhook_url: extractedUrl, timestamp: new Date().toISOString() }, null, 2));
        console.log(`Saved webhook URL to ${outputPath}`);
      } else {
        console.log("Failed to extract a valid URL. Skyvern returned:", extractedUrl);
      }

  } catch (error) {
      console.error("Extraction Failed:", error);
  }
}

main();