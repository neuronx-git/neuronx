import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) process.exit(1);

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const WF_01_ID = "99ce0aa7-2491-4c91-9477-22969798e2b7"; // Inquiry Acknowledge
  
  const WF_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows/${WF_01_ID}`;

  try {
      console.log("Adding Internal Notification to WF-01...");

      await agent.executeStep(
          `Navigate to WF-01.
           Find the start of the workflow (after Trigger).
           Add a new Action: 'Internal Notification'.
           Type: Email.
           To User Type: All Users (or Account Owner).
           Subject: "New Immigration Lead: {{contact.name}}"
           Message: "A new lead just submitted the intake form. Name: {{contact.name}}, Email: {{contact.email}}, Phone: {{contact.phone}}. Please review in GHL."
           Save the Action.
           Save the Workflow.`,
          WF_URL
      );

      console.log("Internal Notification Added.");

  } catch (e) { console.error("Failed to Add Notification", e); }
}

main();
