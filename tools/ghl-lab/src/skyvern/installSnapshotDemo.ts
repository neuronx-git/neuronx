import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) process.exit(1);

  const SUBACCOUNTS_URL = "https://app.gohighlevel.com/accounts/list";

  try {
      console.log("Installing Gold Snapshot into Demo Tenant...");

      const result = await agent.executeStep(
          `Navigate to Agency > Sub-Accounts.
           Search for "NeuronX Demo Tenant".
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

  } catch (e) { console.error("Failed to Install Snapshot into Demo", e); }
}

main();
