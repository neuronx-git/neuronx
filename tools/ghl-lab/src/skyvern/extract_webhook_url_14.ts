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
      console.log("\nTrying to extract URL via HTML Extraction (Attempt 14)...");
      
      const result1 = await agent.executeStep(
          "Navigate to the 'Automation' > 'Workflows' page. Find 'WF-04B - AI Call Receiver' and click to open it.",
          URL_WORKFLOWS_LIST
      );
      console.log("Step 1 (Open Workflow) Complete:", result1.status);

      const result2 = await agent.executeStep(
          "Click on the 'Inbound Webhook' trigger to open settings. In the panel on the right, look for the 'Webhook URL' input box.",
          null
      );
      console.log("Step 2 (Open Settings) Complete:", result2.status);

      // Try to get the HTML of the input
      const result3 = await agent.executeStep(
          "Find the text input element that displays the Webhook URL (it starts with 'https://services.leadconnectorhq.com'). Return the full HTML of this input element (including its value attribute) in your extraction output as {\"element_html\": \"...\"}.",
          null
      );
      console.log("Step 3 (Get HTML) Complete:", result3.status);

      let extractedHtml = "NOT_FOUND";
      if (result3.extracted_information) {
         try {
             const info = typeof result3.extracted_information === 'string' 
                ? JSON.parse(result3.extracted_information) 
                : result3.extracted_information;
             extractedHtml = info.element_html || "NOT_FOUND";
         } catch(e) {
             console.log("Failed to parse extracted info:", result3.extracted_information);
             extractedHtml = result3.extracted_information;
         }
      }
      
      console.log("Extracted HTML:", extractedHtml);
      
      // Parse URL from HTML
      // Look for value="..."
      const valueMatch = extractedHtml.match(/value=["'](https:\/\/services\.leadconnectorhq\.com\/hooks\/[^"']+)["']/);
      if (valueMatch) {
          const webhookUrl = valueMatch[1];
          console.log("Found Webhook URL:", webhookUrl);
          const outputPath = path.join(__dirname, '..', '..', '.ghl_webhook_url.json');
          fs.writeFileSync(outputPath, JSON.stringify({ webhook_url: webhookUrl, timestamp: new Date().toISOString() }, null, 2));
          console.log(`Saved webhook URL to ${outputPath}`);
      } else {
          // Fallback: maybe the URL is in the text content
          const textMatch = extractedHtml.match(/https:\/\/services\.leadconnectorhq\.com\/hooks\/[a-zA-Z0-9\/\-_]+/);
          if (textMatch) {
              const webhookUrl = textMatch[0];
              console.log("Found Webhook URL (from text):", webhookUrl);
              const outputPath = path.join(__dirname, '..', '..', '.ghl_webhook_url.json');
              fs.writeFileSync(outputPath, JSON.stringify({ webhook_url: webhookUrl, timestamp: new Date().toISOString() }, null, 2));
              console.log(`Saved webhook URL to ${outputPath}`);
          } else {
              console.log("Could not find valid Webhook URL in extracted HTML.");
          }
      }

  } catch (error) {
      console.error("Extraction Failed:", error);
  }
}

main();