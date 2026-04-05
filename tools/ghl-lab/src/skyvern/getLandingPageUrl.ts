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
  } else {
      console.log(`Resumed session. App URL: ${agent.getAppUrl()}`);
  }

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const FUNNEL_ID = "VmB52pLVfOShgksvmBir";
  const STEP_ID = "a607c93d-9b58-4c8c-931b-19aca87aed9a";
  
  const STEPS_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/funnels-websites/funnels/${FUNNEL_ID}/steps`;

  try {
      console.log("Identifying Landing Page URL...");
      
      // Step 1: Get the public URL from the Funnel Steps page
      const result = await agent.executeStep(
          "Navigate to the Funnel Steps list. Find the 'Immigration Inquiry' step. Look for the public URL (usually shown as a link icon or text like 'https://...'). Extract and return the full public URL of the landing page.",
          STEPS_URL
      );

      console.log("Landing Page URL Result:", JSON.stringify(result, null, 2));
  } catch (e) { console.error("Failed to get URL", e); }
}

main();
