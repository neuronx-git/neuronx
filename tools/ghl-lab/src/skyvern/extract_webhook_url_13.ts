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
      console.log("\nTrying to extract URL via Rename Trick (Attempt 13)...");
      
      const result1 = await agent.executeStep(
          "Navigate to the 'Automation' > 'Workflows' page. Find 'WF-04B - AI Call Receiver' and click to open it.",
          URL_WORKFLOWS_LIST
      );
      console.log("Step 1 (Open Workflow) Complete:", result1.status);

      const result2 = await agent.executeStep(
          "Click on the 'Inbound Webhook' trigger to open settings. In the panel on the right, find the 'Webhook URL'. Click the 'Copy' icon next to the URL to copy it to clipboard.",
          null
      );
      console.log("Step 2 (Copy) Complete:", result2.status);

      // Try to paste into the workflow name
      const result3 = await agent.executeStep(
          "Click on the workflow name at the top left of the screen (it currently says 'WF-04B - AI Call Receiver'). Delete the current name and PASTE the content from the clipboard (simulate Ctrl+V). Then, read the new text in that field and return it as {\"pasted_content\": \"...\"}.",
          null
      );
      console.log("Step 3 (Paste & Read) Complete:", result3.status);

      let extractedContent = "NOT_FOUND";
      if (result3.extracted_information) {
         try {
             const info = typeof result3.extracted_information === 'string' 
                ? JSON.parse(result3.extracted_information) 
                : result3.extracted_information;
             extractedContent = info.pasted_content || "NOT_FOUND";
         } catch(e) {
             console.log("Failed to parse extracted info:", result3.extracted_information);
             extractedContent = result3.extracted_information;
         }
      }
      
      console.log("Extracted Content:", extractedContent);
      
      if (extractedContent && extractedContent.includes("hooks")) {
          const webhookUrl = extractedContent;
          console.log("Found Webhook URL:", webhookUrl);
          const outputPath = path.join(__dirname, '..', '..', '.ghl_webhook_url.json');
          fs.writeFileSync(outputPath, JSON.stringify({ webhook_url: webhookUrl, timestamp: new Date().toISOString() }, null, 2));
          console.log(`Saved webhook URL to ${outputPath}`);
      }

      // Cleanup: Rename back
      await agent.executeStep(
          "Rename the workflow back to 'WF-04B - AI Call Receiver'.",
          null
      );

  } catch (error) {
      console.error("Extraction Failed:", error);
  }
}

main();