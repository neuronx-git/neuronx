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

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const FUNNEL_ID = "VmB52pLVfOShgksvmBir";
  const STEP_ID = "a607c93d-9b58-4c8c-931b-19aca87aed9a"; // "Immigration Inquiry" step
  
  // URL to edit the step
  const BUILDER_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/builder/website/${STEP_ID}`;

  try {
      console.log("Starting Gold-Class Landing Page Implementation...");

      // Step 1: Open Builder
      await agent.executeStep(
          "Open the Funnel Builder for the 'Immigration Inquiry' page. Wait for it to load completely.",
          BUILDER_URL
      );

      // Step 2: Hero Section
      await agent.executeStep(
          `Find the Hero Section (top section).
           1. Update the Main Headline to: "Immigration Advice Backed by a Structured Assessment Process"
           2. Update the Subheadline to: "Book a consultation to assess your options for Express Entry, Study Permits, Family Sponsorship, and Work Permits."
           3. Ensure the primary CTA button says: "Start Your Immigration Assessment" and scrolls to the form section.
           4. If there is a background image, ensure it looks professional (or leave default).`
      );

      // Step 3: Trust Signals (New Section below Hero)
      await agent.executeStep(
          `Add a new 'Full Width' Section below the Hero.
           Inside, add a '3 Column' Row.
           Col 1: Add Icon + Text "Licensed & Regulated" (CICC Member).
           Col 2: Add Icon + Text "Structured Process" (Transparent Assessment).
           Col 3: Add Icon + Text "Global Reach" (Serving Clients Worldwide).
           Style this section with a light background to distinguish it.`
      );

      // Step 4: Programs Section
      await agent.executeStep(
          `Add a new Section titled "Our Areas of Expertise".
           Add a '3 Column' Row.
           Col 1: Headline "Express Entry" + text "Federal Skilled Worker, CEC, FST."
           Col 2: Headline "Study Permits" + text "School admission & visa application."
           Col 3: Headline "Family Sponsorship" + text "Spousal, parent, & grandparent sponsorship."
           Add another '3 Column' Row below it.
           Col 1: Headline "Work Permits" + text "LMIA & LMIA-exempt streams."
           Col 2: Headline "PNP" + text "Provincial Nominee Programs."
           Col 3: Headline "Visitor Visas" + text "TRV & Super Visas."`
      );

      // Step 5: How It Works
      await agent.executeStep(
          `Add a new Section titled "How Our Process Works".
           Add a '3 Column' Row.
           Col 1: Step 1 "Submit Assessment" (Fill our secure form).
           Col 2: Step 2 "Expert Review" (We analyze your profile).
           Col 3: Step 3 "Consultation" (Get a clear roadmap).`
      );

      // Step 6: About Team (Simple Text)
      await agent.executeStep(
          `Add a new Section titled "About NeuronX Immigration Advisory".
           Add a Paragraph element: "We are a team of licensed professionals dedicated to simplifying Canadian immigration. We use advanced technology to ensure no detail is missed in your application."`
      );

      // Step 7: Form Section (Ensure Visibility)
      await agent.executeStep(
          `Scroll to the existing Form section.
           Ensure the headline above the form says: "Begin Your Assessment".
           Ensure the "Immigration Inquiry (V1)" form is visible.`
      );

      // Step 8: Save
      await agent.executeStep(
          "Click the 'Save' button in the top right corner. Wait for the 'Saved' notification."
      );

      console.log("Gold-Class Page Implemented.");

  } catch (e) { console.error("Page Update Failed", e); }
}

main();
