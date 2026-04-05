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
  
  // URLs
  const SETTINGS_EMAIL_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/settings/email-services`;
  const SETTINGS_PHONE_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/settings/phone-numbers`;
  const SETTINGS_PROFILE_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/settings/company`;
  const PIPELINES_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/settings/pipelines`;
  const CALENDARS_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/settings/calendars`;
  const FORMS_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/sites/forms/builder`;

  const reportData: any = {};

  try {
      console.log("Starting Platform Audit...");

      // 1. Email Services
      console.log("Auditing Email Services...");
      const emailResult = await agent.executeStep(
          "Check the Email Services page. Tell me if a dedicated sending domain is configured, and if the default provider (LeadConnector or Mailgun) is active. Note any missing authentication warnings.",
          SETTINGS_EMAIL_URL
      );
      reportData.email = emailResult;

      // 2. Phone / SMS
      console.log("Auditing Phone Services...");
      const phoneResult = await agent.executeStep(
          "Check the Phone Numbers page. Tell me if a phone number is assigned to this location. Also check the 'Trust Center' or 'A2P' tab if visible, and note the A2P 10DLC registration status.",
          SETTINGS_PHONE_URL
      );
      reportData.phone = phoneResult;

      // 3. Business Profile
      console.log("Auditing Business Profile...");
      const profileResult = await agent.executeStep(
          "Check the Business Profile page. Tell me if the Business Name, Address, Website, and Timezone are filled out.",
          SETTINGS_PROFILE_URL
      );
      reportData.profile = profileResult;

      // 4. Pipelines
      console.log("Auditing Pipelines...");
      const pipelineResult = await agent.executeStep(
          "Check the Pipelines page. Find the 'NeuronX - Immigration Intake' pipeline. List all the stages configured for this pipeline.",
          PIPELINES_URL
      );
      reportData.pipelines = pipelineResult;

      // 5. Calendars
      console.log("Auditing Calendars...");
      const calendarResult = await agent.executeStep(
          "Check the Calendars settings. Find the active calendar (e.g., Immigration Consultations). Is it linked to a team member? Does it have a custom booking link?",
          CALENDARS_URL
      );
      reportData.calendars = calendarResult;

      // 6. Forms
      console.log("Auditing Forms...");
      const formResult = await agent.executeStep(
          "Check the Forms Builder list. Tell me if the 'Immigration Inquiry' form exists and list its core fields if visible, or just confirm it exists.",
          FORMS_URL
      );
      reportData.forms = formResult;

      console.log("\n=== RAW AUDIT RESULTS ===");
      console.log(JSON.stringify(reportData, null, 2));

  } catch (e) { console.error("Audit Failed", e); }
}

main();
