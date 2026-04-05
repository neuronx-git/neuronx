import { SkyvernAgent } from "./SkyvernAgent";
import { PREMIUM_TEMPLATES } from "../content/message_templates";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) {
      console.log("No session found. Please login first.");
      process.exit(1);
  }

  const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";
  
  // Map Workflow IDs
  const WF_IDS = {
      WF_01: "99ce0aa7-2491-4c91-9477-22969798e2b7",
      WF_02: "43ecd109-6595-4f51-a0e0-e2421b3f8131",
      WF_04: "838f7c38-3534-4d3b-9d4c-40b11f4a6772",
      WF_05: "9af911d1-b025-45d4-a083-f62364752318",
      WF_06: "5d0c1920-bf7b-45c2-9cf9-e40466e3e0aa",
      WF_09: "93b39b76-8db0-45f1-b48b-b36ddd8ddcbf",
      WF_10: "25046474-a6f3-4235-837f-81fd3e72f56b",
      WF_11: "7e0a17f4-461b-4404-9eb6-656e4782d476"
  };

  try {
      console.log("Starting Premium Template Update...");

      // WF-01 Update
      await updateWorkflow(agent, LOCATION_ID, WF_IDS.WF_01, "WF-01 New Inquiry", [
          { type: "SMS", text: PREMIUM_TEMPLATES.wf01_sms_1 },
          { type: "Email", subject: PREMIUM_TEMPLATES.wf01_email_1_subject, body: PREMIUM_TEMPLATES.wf01_email_1_body }
      ]);

      // WF-02 Update
      await updateWorkflow(agent, LOCATION_ID, WF_IDS.WF_02, "WF-02 Contact Attempt", [
          { type: "SMS", text: PREMIUM_TEMPLATES.wf02_sms_1 },
          { type: "Email", subject: PREMIUM_TEMPLATES.wf02_email_final_subject, body: PREMIUM_TEMPLATES.wf02_email_final_body }
      ]);

      // WF-05 Update
      await updateWorkflow(agent, LOCATION_ID, WF_IDS.WF_05, "WF-05 Booking Reminders", [
          { type: "SMS", text: PREMIUM_TEMPLATES.wf05_sms_confirm },
          { type: "Email", subject: PREMIUM_TEMPLATES.wf05_email_confirm_subject, body: PREMIUM_TEMPLATES.wf05_email_confirm_body },
          { type: "SMS", text: PREMIUM_TEMPLATES.wf05_sms_reminder_48h }, // Matches first occurrence logic if vague, but better to be specific if possible
          { type: "SMS", text: PREMIUM_TEMPLATES.wf05_sms_reminder_24h },
          { type: "SMS", text: PREMIUM_TEMPLATES.wf05_sms_reminder_2h }
      ]);

      console.log("All updates completed.");

  } catch (e) { console.error("Update Failed", e); }
}

async function updateWorkflow(agent: SkyvernAgent, locationId: string, wfId: string, wfName: string, updates: any[]) {
    console.log(`Updating ${wfName}...`);
    const url = `https://app.gohighlevel.com/location/${locationId}/workflow/${wfId}`;
    
    // We construct a single prompt to do it all if possible, or iterate
    // Iterating is safer.
    
    // Step 1: Open Builder
    await agent.executeStep(
        `Open the workflow builder for '${wfName}'. Wait for it to load.`,
        url
    );

    // Step 2: Apply updates
    for (const update of updates) {
        if (update.type === "SMS") {
            await agent.executeStep(
                `Find the 'Send SMS' action. (If multiple, find the one that matches the sequence order or just the first one if not specified). Click it. In the message box, REPLACE the entire text with: "${update.text.replace(/\n/g, '\\n')}". Click Save Action.`
            );
        } else if (update.type === "Email") {
            await agent.executeStep(
                `Find the 'Send Email' action. Click it. Set Subject to: "${update.subject}". Set Message Body to: "${update.body.replace(/\n/g, '\\n')}". Click Save Action.`
            );
        }
    }

    // Step 3: Save Workflow
    await agent.executeStep(
        "Click the 'Save' button in the top right corner."
    );
    console.log(`Saved ${wfName}.`);
}

main();
