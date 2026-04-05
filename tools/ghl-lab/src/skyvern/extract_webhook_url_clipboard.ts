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
      console.log("\nTrying to extract URL via Clipboard Paste...");
      
      // Step 1: Open Workflow
      const result1 = await agent.executeStep(
          "Navigate to the 'Automation' > 'Workflows' page. Find 'WF-04B - AI Call Receiver' and click to open it.",
          URL_WORKFLOWS_LIST
      );
      console.log("Step 1 (Open Workflow) Complete:", result1.status);

      // Step 2: Copy URL
      const result2 = await agent.executeStep(
          "Click on the 'Inbound Webhook' trigger to open settings. In the settings panel on the right, find the 'Webhook URL' section. Click the 'Copy' icon (two overlapping squares) next to the URL input box to copy the URL to clipboard.",
          null
      );
      console.log("Step 2 (Copy to Clipboard) Complete:", result2.status);

      // Step 3: Add Note Action
      const result3 = await agent.executeStep(
          "Click the '+' button to add a new action. Search for 'Add Contact Note' and select it.",
          null
      );
      console.log("Step 3 (Add Action) Complete:", result3.status);

      // Step 4: Paste and Extract
      // We ask Skyvern to paste. If it can't, we might fail here.
      const result4 = await agent.executeStep(
          "In the 'Note' text area, type 'URL: ' and then PASTE the content from the clipboard (simulate Ctrl+V or Command+V). Then, read the entire text content of the Note text area and return it in your extraction output as {\"note_content\": \"...\"}.",
          null
      );
      console.log("Step 4 (Paste & Extract) Complete:", result4.status);

      let extractedContent = "NOT_FOUND";
      if (result4.extracted_information) {
         try {
             const info = typeof result4.extracted_information === 'string' 
                ? JSON.parse(result4.extracted_information) 
                : result4.extracted_information;
             extractedContent = info.note_content || "NOT_FOUND";
         } catch(e) {
             console.log("Failed to parse extracted info:", result4.extracted_information);
             extractedContent = result4.extracted_information;
         }
      }
      
      console.log("Extracted Content:", extractedContent);
      
      // Try to parse URL from content
      // Expected: "URL: https://..."
      const urlMatch = extractedContent.match(/https:\/\/services\.leadconnectorhq\.com\/hooks\/[a-zA-Z0-9\/]+/);
      if (urlMatch) {
          const webhookUrl = urlMatch[0];
          console.log("Found Webhook URL:", webhookUrl);
          const outputPath = path.join(__dirname, '..', '..', '.ghl_webhook_url.json');
          fs.writeFileSync(outputPath, JSON.stringify({ webhook_url: webhookUrl, timestamp: new Date().toISOString() }, null, 2));
          console.log(`Saved webhook URL to ${outputPath}`);
      } else {
          console.log("Could not find valid Webhook URL in extracted content.");
      }

  } catch (error) {
      console.error("Extraction Failed:", error);
  }
}

main();