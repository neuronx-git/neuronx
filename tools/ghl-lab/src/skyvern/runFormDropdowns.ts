import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  if (!resumed) process.exit(1);

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  const FORM_ID = "FNMmVXpfUvUypS0c4oQ3";
  // Builder URL: https://leadgen-apps-form-survey-builder.leadconnectorhq.com/form-builder-v2/FNMmVXpfUvUypS0c4oQ3?locationId=FlRL82M0D6nclmKT7eXH
  // Note: It's an iframe usually, but we can try navigating directly to the builder URL or via GHL UI.
  // Using direct builder URL might be blocked by auth if not framed correctly?
  // Safest is to navigate via GHL UI.
  
  const FORMS_LIST_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/sites/forms/builder`;

  try {
      console.log("Starting Form Dropdowns Configuration...");
      
      // Step 1: Open Form Builder
      await agent.executeStep(
          "Navigate to Sites > Forms > Builder. Find 'Immigration Inquiry (V1)' and click Edit.",
          FORMS_LIST_URL
      );

      // Step 2: Program Interest
      await agent.executeStep(
          "Find the 'Program Interest' dropdown field. Click it to open settings. In the Options list, ensure these options exist (add/edit as needed): 'Express Entry', 'Provincial Nominee (PNP)', 'Study Permit', 'Work Permit', 'Family Sponsorship', 'Visitor Visa', 'Not Sure'.",
          null // Pass null for URL since we are already on the page
      );

      // Step 3: Current Location
      await agent.executeStep(
          "Find the 'Current Location' (or Country) dropdown field. Click it. Set options: 'Canada', 'India', 'Philippines', 'Nigeria', 'Pakistan', 'Other'.",
          null
      );

      // Step 4: Timeline
      await agent.executeStep(
          "Find the 'Timeline' dropdown field. Click it. Set options: 'Within 3 months', '3-6 months', '6-12 months', 'More than 12 months', 'Just exploring'.",
          null
      );

      // Step 5: Save
      await agent.executeStep(
          "Click 'Save' or 'Integrate' -> 'Save' to save the form.",
          null
      );

      console.log("Form Dropdowns Configured.");
  } catch (e) { console.error("Form Dropdowns Failed", e); }
}

main();
