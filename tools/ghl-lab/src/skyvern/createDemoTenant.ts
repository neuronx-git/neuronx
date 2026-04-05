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

  const SUBACCOUNTS_URL = "https://app.gohighlevel.com/accounts/list";

  try {
      console.log("Creating Demo Tenant...");

      const result = await agent.executeStep(
          `Navigate to Agency > Sub-Accounts.
           Click 'Create Sub-Account'.
           Choose 'Regular Account'.
           Select 'Enter Manually'.
           First Name: NeuronX
           Last Name: Demo
           Email: demo@neuronx.ai
           Business Name: "NeuronX Demo Tenant"
           Address: 456 Demo St
           City: Toronto
           Country: Canada
           State: Ontario
           Zip: M5V 3A1
           Phone: +15550001111
           Timezone: (GMT-05:00) Eastern Time (US & Canada)
           Click Save.
           Wait for the dashboard to load.
           Return the URL of the new dashboard.`,
          SUBACCOUNTS_URL
      );

      console.log("Demo Tenant Creation Result:", JSON.stringify(result, null, 2));

  } catch (e) { console.error("Failed to Create Demo Tenant", e); }
}

main();
