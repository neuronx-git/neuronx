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
      console.log("\nTrying to extract webhook URL from the opened workflow, simpler prompt...");
      
      const result = await agent.executeStep(
          "Look at the screen. You should see a workflow trigger named 'Inbound Webhook'. Click on it to open the side panel. In the side panel, look for a text box labeled 'Webhook URL' and a 'Copy' button next to it. Extract the text from that 'Webhook URL' box and return it as a JSON object: {\"webhook_url\": \"<url_here>\"}",
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
             extractedUrl = result.extracted_information; // Fallback to raw string
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