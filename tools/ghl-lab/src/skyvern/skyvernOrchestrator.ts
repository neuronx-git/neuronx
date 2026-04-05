import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  
  // 1. Session Management
  const resumed = await agent.loadSession();
  
  if (!resumed) {
      const url = await agent.createSession();
      console.log("\n!!! ACTION REQUIRED !!!");
      console.log("A new Skyvern session has been created.");
      console.log(`Please open this URL to monitor and LOG IN to GoHighLevel:`);
      console.log(url);
      console.log("\nOnce you have logged in, please run this script again to proceed with automation.");
      process.exit(0);
  } else {
      console.log(`Resumed session. App URL: ${agent.getAppUrl()}`);
  }

  // Constants
  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const WF_01_ID = "99ce0aa7-2491-4c91-9477-22969798e2b7";
  
  const URL_WORKFLOWS_LIST = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;
  const URL_WF_BUILDER = `https://app.gohighlevel.com/location/${LOCATION_ID}/workflow/${WF_01_ID}`;

  // 2. Define Atomic Steps for WF-01
  // Logic: Observe -> Plan -> Act -> Verify
  
  try {
      console.log("\nStarting WF-01 Configuration...");
      
      // Step 1: Navigate to Workflows List
      const result1 = await agent.executeStep(
          "Navigate to the 'Automation' > 'Workflows' page. Verify you are on the list of workflows.",
          URL_WORKFLOWS_LIST
      );
      console.log("Step 1 Complete:", result1.status);

      // Step 2: Open WF-01 Builder Directly
      // We navigate directly to the builder to avoid list search issues and ensure URL is present
      const result2 = await agent.executeStep(
          "Verify the workflow builder is open for 'New Inquiry Acknowledge'. If a modal overlay appears (like 'Welcome' or 'Tutorial'), dismiss it by clicking 'X' or pressing Escape.",
          URL_WF_BUILDER
      );
      console.log("Step 2 Complete:", result2.status);

      // Step 3: Add Trigger
      const result3 = await agent.executeStep(
          "Check if there is a trigger 'Form Submitted'. If not, click 'Add New Workflow Trigger', search for 'Form Submitted', select it. Then in the trigger settings on the right, add a Filter: 'Form is NeuronX Inquiry Form'. Click 'Save Trigger' at the bottom right. Dismiss any modal if it appears.",
          URL_WF_BUILDER
      );
      console.log("Step 3 Complete:", result3.status);

      // Step 4: Add Action
      const result4 = await agent.executeStep(
          "Check if there is an action 'Send SMS'. If not, click the '+' button to add an action. Search 'Send SMS'. In the message box, type: 'Hello {{contact.first_name}}, we received your inquiry.'. Click 'Save Action' at the bottom right.",
          URL_WF_BUILDER
      );
      console.log("Step 4 Complete:", result4.status);

      // Step 5: Save & Verify
      const result5 = await agent.executeStep(
          "Click the 'Save' button in the top right corner of the builder. Then click 'Publish' if it says 'Draft'. Then Reload the page. After reload, verify that the 'Form Submitted' trigger and 'Send SMS' action are still present.",
          URL_WF_BUILDER
      );
      console.log("Step 5 Complete:", result5.status);
      console.log("WF-01 Configuration Completed.");

  } catch (error) {
      console.error("Workflow Execution Failed:", error);
  }
}

main();
