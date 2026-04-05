import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) {
      console.log("No valid Skyvern session found.");
      process.exit(1);
  }

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const URL_WORKFLOWS_LIST = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;

  try {
      console.log("\nCreating a fresh workflow for Vapi...");
      
      // Step 1: Create new workflow
      await agent.executeStep(
          "Navigate to the 'Automation' > 'Workflows' page. Click 'Create Workflow', then click 'Start from scratch'.",
          URL_WORKFLOWS_LIST
      );
      console.log("Step 1: Created blank workflow.");

      // Step 2: Rename
      await agent.executeStep(
          "Click on the workflow name at the top left (e.g., 'New Workflow') and rename it to 'NeuronX Vapi Receiver'.",
          null
      );
      console.log("Step 2: Renamed workflow.");

      // Step 3: Add Webhook Trigger
      await agent.executeStep(
          "Click 'Add New Workflow Trigger'. Search for 'Inbound Webhook' and select it. Wait for the Webhook URL to generate. Click 'Save Trigger' at the bottom right.",
          null
      );
      console.log("Step 3: Added Webhook Trigger.");

      // Step 4: Add dummy action so it can be saved/published
      await agent.executeStep(
          "Click the '+' button to add an action. Search for 'Add Contact Note' and select it. In the note content, type 'Vapi Webhook Triggered'. Click 'Save Action'.",
          null
      );
      console.log("Step 4: Added Note Action.");

      // Step 5: Save and Publish
      await agent.executeStep(
          "Click 'Publish' at the top right to toggle from Draft to Publish. Then click the 'Save' button in the top right corner.",
          null
      );
      console.log("Step 5: Saved and Published.");

      // Step 6: Open Webhook settings to show URL to user
      await agent.executeStep(
          "Click on the 'Inbound Webhook' trigger box to open its settings panel on the right. Leave the panel open so the user can see the Webhook URL.",
          null
      );
      console.log("Step 6: Opened Webhook settings panel.");
      
      console.log("\n*** SUCCESS ***");
      console.log("The workflow 'NeuronX Vapi Receiver' has been created and published.");
      console.log("The Webhook URL should now be visible on your screen in the right panel.");

  } catch (error) {
      console.error("Workflow Creation Failed:", error);
  }
}

main();