import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) process.exit(1);

  const CLEAN_LAB_ID = "XXXXXXXXXXXXX"; // Need to get this dynamically or ask user if script failed to return it.
  // Based on previous step, Skyvern might not have returned the URL textually. 
  // Let's assume we are ON the dashboard of the new account or can find it.
  
  // Strategy: Go to Sub-Accounts list, search for "NeuronX Clean Lab", click Manage Client, then Load Snapshot.
  const SUBACCOUNTS_URL = "https://app.gohighlevel.com/accounts/list";

  try {
      console.log("Installing Snapshot into Clean Lab...");

      const result = await agent.executeStep(
          `Navigate to Agency > Sub-Accounts.
           Search for "NeuronX Clean Lab".
           Click 'Manage Client' (or the name).
           Click 'Actions' dropdown > 'Load Snapshot'.
           Select Snapshot: "NeuronX Gold v1.0 — 2026-03-17".
           Click Proceed.
           Select ALL assets (Pipelines, Workflows, Forms, etc.).
           Click Proceed/Overwrite.
           Confirm.
           Wait for success message.`,
          SUBACCOUNTS_URL
      );

      console.log("Snapshot Install Result:", JSON.stringify(result, null, 2));

  } catch (e) { console.error("Failed to Install Snapshot", e); }
}

main();
