import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) process.exit(1);

  // Sub-accounts URL
  const SUBACCOUNTS_URL = "https://app.gohighlevel.com/accounts/list";

  try {
      console.log("Creating Clean Lab Sub-Account...");

      const result = await agent.executeStep(
          `Navigate to Agency > Sub-Accounts.
           Click 'Create Sub-Account'.
           Choose 'Regular Account' (or Blank Snapshot).
           Select 'Enter Manually'.
           First Name: NeuronX
           Last Name: Lab
           Email: lab@neuronx.ai
           Business Name: "NeuronX Clean Lab"
           Address: 123 Tech Ave
           City: Toronto
           Country: Canada
           State: Ontario
           Zip: M5V 2T6
           Phone: +15550009999
           Timezone: (GMT-05:00) Eastern Time (US & Canada)
           Click Save.
           Wait for the dashboard to load.
           IMPORTANT: Return the URL of the new dashboard (it contains the Location ID).`,
          SUBACCOUNTS_URL
      );

      console.log("Sub-Account Creation Result:", JSON.stringify(result, null, 2));

  } catch (e) { console.error("Failed to Create Sub-Account", e); }
}

main();
