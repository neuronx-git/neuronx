import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) process.exit(1);

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const WF_IDS = [
      { id: "99ce0aa7-2491-4c91-9477-22969798e2b7", name: "WF-01 New Inquiry" },
      { id: "43ecd109-6595-4f51-a0e0-e2421b3f8131", name: "WF-02 Contact Attempt" },
      { id: "838f7c38-3534-4d3b-9d4c-40b11f4a6772", name: "WF-04 Invite Booking" }
  ];

  try {
      console.log("Generating Updated Template Report...");
      
      const allTemplates = [];

      for (const wf of WF_IDS) {
          const url = `https://app.gohighlevel.com/location/${LOCATION_ID}/workflow/${wf.id}`;
          
          const result = await agent.executeStep(
              `Navigate to the workflow builder for '${wf.name}'. Find every 'Send SMS' and 'Send Email' action. Click on each one to open settings, read the message text/body, and close. Return a list: { type, text }.`,
              url
          );
          
          allTemplates.push({ workflow: wf.name, templates: result.output });
      }

      console.log("REPORT_DATA:", JSON.stringify(allTemplates, null, 2));
      console.log("Full Skyvern Result Object:", JSON.stringify(allTemplates, null, 2)); // Duplicate to ensure we see it if output key is different

  } catch (e) { console.error("Report Gen Failed", e); }
}

main();
