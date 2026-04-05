import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) process.exit(1);

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";

  try {
      console.log("Verifying UAT Leads in GHL...");
      
      const verificationResult = await agent.executeStep(
          `
          Navigate to the Opportunities page.
          Check the 'NeuronX - Immigration Intake' pipeline.
          You should see 5 new contacts (e.g., Test Express Entry, Test Student Visa, etc.) in the 'NEW' or 'CONTACTING' stages.
          Click on one of them to open the contact details.
          Verify in the conversation history that an SMS and Email attempt were logged.
          Return a summary of what you see.
          `,
          `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/opportunities`
      );

      console.log("UAT Verification Results:", JSON.stringify(verificationResult, null, 2));

  } catch (e) { console.error("Failed", e); }
}

main();
