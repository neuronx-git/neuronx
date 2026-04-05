import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) {
      process.exit(1);
  }

  // Fallback: try to find the "preview" or "visit" link for the funnel
  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const FUNNEL_ID = "VmB52pLVfOShgksvmBir";
  const FUNNEL_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/funnels-websites/funnels/${FUNNEL_ID}/steps`;

  try {
      console.log("Finding Public URL via Visual Inspection...");
      
      const result = await agent.executeStep(
          "Navigate to the Funnel Steps list. Look for the 'Immigration Inquiry' step. There should be a small 'external link' icon or the URL text itself displayed near the step name. Click that link or extract the URL. If you click it, return the new tab's URL.",
          FUNNEL_URL
      );

      console.log("Visual Inspection Result:", JSON.stringify(result, null, 2));
  } catch (e) { console.error("Failed to get URL", e); }
}

main();
