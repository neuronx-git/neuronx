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

  try {
      console.log("\nTrying to extract webhook URL from the opened workflow...");
      
      const result = await agent.executeStep(
          "Look at the currently open workflow. Click on the 'Inbound Webhook' trigger to open its settings. Look for the 'Webhook URL' field in the settings panel on the right. Copy that URL and return it as a JSON string in your extraction output, using the key 'webhook_url'. Example: {\"webhook_url\": \"https://services.leadconnectorhq.com/hooks/...\"}",
          null
      );
      console.log("Extraction Step Complete:", result.status);
      
      let extractedUrl = "NOT_FOUND";
      if (result.extracted_information) {
         try {
             const info = typeof result.extracted_information === 'string' 
                ? JSON.parse(result.extracted_information) 
                : result.extracted_information;
             extractedUrl = info.webhook_url || "NOT_FOUND";
         } catch(e) {
             console.log("Failed to parse extracted info:", result.extracted_information);
         }
      }
      
      console.log("Extracted Webhook URL:", extractedUrl);
      
      if (extractedUrl !== "NOT_FOUND") {
        const outputPath = path.join(__dirname, '..', '..', '.ghl_webhook_url.json');
        fs.writeFileSync(outputPath, JSON.stringify({ webhook_url: extractedUrl, timestamp: new Date().toISOString() }, null, 2));
        console.log(`Saved webhook URL to ${outputPath}`);
      }

  } catch (error) {
      console.error("Extraction Failed:", error);
  }
}

main();