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
  const FUNNEL_ID = "VmB52pLVfOShgksvmBir";
  const STEPS_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/funnels-websites/funnels/${FUNNEL_ID}/steps`;

  try {
      console.log("Identifying Exact Landing Page URL...");
      
      const result = await agent.executeStep(
          "Navigate to the Funnel Steps list. Look for the 'Immigration Inquiry' step. Click the 'Preview' or 'Link' icon to open the live page. Return the exact URL of the live page (it usually starts with https://api.leadconnectorhq.com or a custom domain).",
          STEPS_URL
      );

      console.log("Landing Page URL Result:", JSON.stringify(result, null, 2));

  } catch (e) { console.error("Failed", e); }
}

main();
