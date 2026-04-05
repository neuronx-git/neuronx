import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) process.exit(1);

  // Fallback to standard GHL preview widget URL since Skyvern couldn't extract the text easily
  // Usually it is: https://api.leadconnectorhq.com/widget/form/FNMmVXpfUvUypS0c4oQ3
  // Or the funnel URL. Let's use the form widget directly to ensure a clean submission.
  const FORM_URL = "https://api.leadconnectorhq.com/widget/form/FNMmVXpfUvUypS0c4oQ3";

  try {
      console.log("Executing Form Submission...");
      
      const result = await agent.executeStep(
          `
          Navigate to the form.
          Fill out the form with these exact details:
          - First Name: Test
          - Last Name: User
          - Email: test@neuronx.ai
          - Phone: +15551112222
          - Program Interest: Express Entry
          - Location: India
          - Timeline: 3-6 months
          
          Submit the form. Wait for the success message or redirect.
          `,
          FORM_URL
      );

      console.log("Form Submission Result:", JSON.stringify(result, null, 2));

  } catch (e) { console.error("Failed", e); }
}

main();
