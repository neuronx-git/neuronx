import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) process.exit(1);

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";

  try {
      console.log("Verifying Pipeline Entry...");
      
      const pipelineResult = await agent.executeStep(
          `
          Navigate to the Opportunities page.
          Check the 'NeuronX - Immigration Intake' pipeline.
          Look for a contact named 'Test User' in the 'NEW' or 'CONTACTING' stage.
          Confirm if the contact is present.
          `,
          `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/opportunities`
      );
      console.log("Pipeline Verification:", JSON.stringify(pipelineResult, null, 2));

      console.log("Verifying Contact Details & Comms...");
      const contactResult = await agent.executeStep(
          `
          Navigate to the Contacts page.
          Search for 'test@neuronx.ai' or 'Test User'.
          Click on the contact to open their details.
          In the middle conversation column, verify if an SMS and Email were sent (or attempted).
          Note any error messages (like 'Delivery Failed' or 'A2P pending').
          Return the communication status.
          `,
          `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/contacts/smart_list/All`
      );
      console.log("Contact Verification:", JSON.stringify(contactResult, null, 2));

  } catch (e) { console.error("Failed", e); }
}

main();
