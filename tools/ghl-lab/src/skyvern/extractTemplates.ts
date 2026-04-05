import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) process.exit(1);

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const WF_01_ID = "99ce0aa7-2491-4c91-9477-22969798e2b7"; // Inquiry Acknowledge
  const WF_02_ID = "43ecd109-6595-4f51-a0e0-e2421b3f8131"; // Contact Attempt
  const WF_05_ID = "9af911d1-b025-45d4-a083-f62364752318"; // Booking Reminders
  
  // URL to Workflows
  const WF_URL_BASE = `https://app.gohighlevel.com/location/${LOCATION_ID}/workflow`;

  try {
      console.log("Extracting Templates...");
      
      // Use a more iterative approach since the prompt above is too complex for one step.
      // We will loop through each workflow individually.

      const workflows = [
        { id: WF_01_ID, name: "WF-01 New Inquiry Acknowledge" },
        { id: WF_02_ID, name: "WF-02 Contact Attempt Sequence" },
        { id: WF_05_ID, name: "WF-05 Appointment Booked Reminders" }
      ];

      for (const wf of workflows) {
          console.log(`Extracting from ${wf.name}...`);
          const url = `https://app.gohighlevel.com/location/${LOCATION_ID}/workflow/${wf.id}`;
          
          const result = await agent.executeStep(
              `Navigate to the workflow builder for '${wf.name}'. Find every 'Send SMS' and 'Send Email' action. Click on each one to open its settings, read the message body text, and then close the settings. Return a JSON list of all messages found: { type: "SMS"|"Email", text: "..." }.`,
              url
          );
          console.log(`${wf.name} Result:`, JSON.stringify(result, null, 2));
      }
  } catch (e) { console.error("Failed to extract templates", e); }
}

main();
