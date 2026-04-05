import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  
  const resumed = await agent.loadSession();
  
  if (!resumed) {
      console.log("No valid Skyvern session found. Please run skyvernOrchestrator.ts first to log in.");
      process.exit(1);
  }

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const URL_WORKFLOWS_LIST = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;

  try {
      console.log("\nChecking list of workflows...");
      
      const result = await agent.executeStep(
          "Navigate to the 'Automation' > 'Workflows' page. Wait for the list to load. Look at all the workflow names listed. Return a list of all workflow names you see in the extraction output as {\"workflow_names\": [\"name1\", \"name2\", ...]}",
          URL_WORKFLOWS_LIST
      );
      
      console.log("Extraction Result:", JSON.stringify(result, null, 2));

  } catch (error) {
      console.error("Check Failed:", error);
  }
}

main();