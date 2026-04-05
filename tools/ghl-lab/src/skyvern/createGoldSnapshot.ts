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

  // Agency View URL
  const AGENCY_SETTINGS_URL = "https://app.gohighlevel.com/settings/snapshots";

  try {
      console.log("Creating Gold Snapshot...");

      const result = await agent.executeStep(
          `Navigate to Agency Settings > Snapshots.
           Click 'Create New Snapshot'.
           Name: "NeuronX Gold v1.0 — 2026-03-17".
           Account: Select 'NeuronX Test Lab'.
           Click Save.
           Wait for the snapshot to appear in the list.
           Return 'Success' if created.`,
          AGENCY_SETTINGS_URL
      );

      console.log("Snapshot Creation Result:", JSON.stringify(result, null, 2));

  } catch (e) { console.error("Failed to Create Snapshot", e); }
}

main();
