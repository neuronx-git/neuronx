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
      console.log("\nStarting Minimal WF-04B Creation...");
      
      const result1 = await agent.executeStep(
          "Navigate to the 'Automation' > 'Workflows' page. Click the button to 'Create Workflow'. Then click 'Start from scratch'.",
          URL_WORKFLOWS_LIST
      );
      console.log("Step 1 (Create Workflow) Complete:", result1.status);

      const result2 = await agent.executeStep(
          "Click on the workflow name at the top left (it probably says 'New Workflow') and rename it to 'WF-04B - AI Call Receiver'.",
          null // Stay on current page
      );
      console.log("Step 2 (Rename) Complete:", result2.status);

      const result3 = await agent.executeStep(
          "Click 'Add New Workflow Trigger'. Search for 'Inbound Webhook' and select it. Wait for the Webhook URL to generate. COPY the Webhook URL. DO NOT map fields yet. Click 'Save Trigger' at the bottom right.",
          null
      );
      console.log("Step 3 (Add Webhook Trigger) Complete:", result3.status);

      const result4 = await agent.executeStep(
          "Click the '+' button to add an action. Search for 'Add Contact Note' and select it. In the note content, type: 'Raw Vapi Webhook Received'. Click 'Save Action'.",
          null
      );
      console.log("Step 4 (Add Note Action) Complete:", result4.status);

      const result5 = await agent.executeStep(
          "Click the 'Save' button in the top right corner of the builder. Then click 'Publish' to toggle it from 'Draft' to 'Publish'. Click Save again.",
          null
      );
      console.log("Step 5 (Save & Publish) Complete:", result5.status);

      const result6 = await agent.executeStep(
          "You should have copied the Inbound Webhook URL in step 3. Please return the exact Webhook URL you copied as a JSON string in your extraction output, using the key 'webhook_url'. Example: {\"webhook_url\": \"https://services.leadconnectorhq.com/hooks/...\"}",
          null
      );
      console.log("Step 6 (Extract URL) Complete:", result6.status);
      
      // Attempt to parse extracted info
      let extractedUrl = "NOT_FOUND";
      if (result6.extracted_information) {
         try {
             // Skyvern sometimes returns a string, sometimes an object
             const info = typeof result6.extracted_information === 'string' 
                ? JSON.parse(result6.extracted_information) 
                : result6.extracted_information;
             extractedUrl = info.webhook_url || "NOT_FOUND";
         } catch(e) {
             console.log("Failed to parse extracted info:", result6.extracted_information);
         }
      }
      
      console.log("Extracted Webhook URL:", extractedUrl);
      
      // Save URL to file
      const outputPath = path.join(__dirname, '..', '..', '.ghl_webhook_url.json');
      fs.writeFileSync(outputPath, JSON.stringify({ webhook_url: extractedUrl, timestamp: new Date().toISOString() }, null, 2));
      console.log(`Saved webhook URL to ${outputPath}`);

  } catch (error) {
      console.error("Workflow Creation Failed:", error);
  }
}

main();