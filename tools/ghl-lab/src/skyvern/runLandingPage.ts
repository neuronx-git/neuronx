import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  if (!resumed) process.exit(1);

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const FUNNEL_ID = "VmB52pLVfOShgksvmBir";
  const STEP_ID = "a607c93d-9b58-4c8c-931b-19aca87aed9a";
  
  // URL to Funnel Steps list
  // https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/funnels-websites/funnels/VmB52pLVfOShgksvmBir/steps
  // But we want to EDIT the step.
  // URL: https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/builder/website/a607c93d-9b58-4c8c-931b-19aca87aed9a
  // Note: Funnel builder URL might be different. Let's try navigating to steps list and clicking Edit.
  
  const STEPS_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/funnels-websites/funnels/${FUNNEL_ID}/steps`;

  try {
      console.log("Starting Landing Page Configuration...");
      
      // Step 1: Open Builder
      await agent.executeStep(
          "Navigate to the Funnel Steps list. Verify you see 'Immigration Inquiry'. Click 'Edit' (or 'Edit Page') to open the page builder. Wait for the builder to load.",
          STEPS_URL
      );

      // Step 2: Add Hero
      await agent.executeStep(
          "In the builder, add a new 'Full Width' Section at the top. Inside, add a '1 Column' Row. Inside the row, add a 'Headline' element. Edit the headline text to: 'Start Your Canadian Immigration Journey'."
      );
      
      await agent.executeStep(
          "Below the headline, add a 'Sub-headline' element. Edit the text to: 'Free initial assessment — takes 2 minutes'."
      );

      // Step 3: Add Form
      await agent.executeStep(
          "Below the sub-headline, add a 'Form' element. In the form settings on the left (or popup), select the form 'Immigration Inquiry (V1)'."
      );

      // Step 4: Save & Publish
      await agent.executeStep(
          "Click the 'Save' button in the top right. Then click 'Publish' if available, or just ensure changes are saved. Then navigate back or verify success."
      );

      console.log("Landing Page Configured.");
  } catch (e) { console.error("Landing Page Failed", e); }
}

main();
