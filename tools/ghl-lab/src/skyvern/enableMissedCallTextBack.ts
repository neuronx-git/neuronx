import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) {
      const url = await agent.createSession();
      console.log("\n!!! ACTION REQUIRED !!!");
      console.log("A new Skyvern session has been created.");
      console.log(`Please open this URL to monitor and LOG IN to GoHighLevel:`);
      console.log(url);
      console.log("\nOnce you have logged in, please run this script again.");
      process.exit(0);
  }

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  
  // URL to Business Profile Settings
  const SETTINGS_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/settings/company`;

  try {
      console.log("Enabling Missed Call Text Back...");

      await agent.executeStep(
          `Navigate to Settings > Business Profile (or Company).
           Scroll down to the 'Missed Call Text Back' section.
           Ensure the checkbox 'Enable Missed Call Text Back' is CHECKED.
           In the message box, set the text to: "Hi, this is NeuronX Immigration Advisory. I saw we just missed your call. How can we help?"
           Click 'Save Missed Call Text Back Settings' (or the main Save button at bottom).`,
          SETTINGS_URL
      );

      console.log("Missed Call Text Back Enabled.");

  } catch (e) { console.error("Failed to Enable MCTB", e); }
}

main();
