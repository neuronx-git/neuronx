import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) process.exit(1);

  // User provided the Location ID directly
  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  
  // Fallback URL if extraction fails
  const KNOWN_FORM_URL = "https://api.leadconnectorhq.com/widget/form/FNMmVXpfUvUypS0c4oQ3";

  try {
      console.log(`Starting UAT on Tenant: ${LOCATION_ID}`);
      
      // 1. Submit Lead
      console.log("Submitting Clean Install Test Lead (Using Known Form URL)...");
      await agent.executeStep(
          `Navigate to: ${KNOWN_FORM_URL}
           Fill form:
           First Name: Clean
           Last Name: Install
           Email: clean@neuronx.ai
           Phone: +15559998888
           Program Interest: Express Entry
           Current Location: Canada
           Timeline: Within 3 months
           Submit the form. Wait for success message.`,
           KNOWN_FORM_URL
      );

      // 2. Verify Backend
      console.log("Verifying Backend Processing...");
      const verifyResult = await agent.executeStep(
          `Navigate to Opportunities.
           Check the 'NeuronX - Immigration Intake' pipeline.
           Look for 'Clean Install' in the NEW stage.
           Click the contact card.
           Verify in the center conversation pane that an SMS and Email attempt are logged.
           Return 'PASS' if verified.`,
           `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/opportunities`
      );

      console.log("UAT Result:", JSON.stringify(verifyResult, null, 2));

  } catch (e) { console.error("UAT Failed", e); }
}

main();
