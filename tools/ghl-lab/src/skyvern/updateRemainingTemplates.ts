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
      WF_04: "838f7c38-3534-4d3b-9d4c-40b11f4a6772",
      WF_06: "5d0c1920-bf7b-45c2-9cf9-e40466e3e0aa",
      WF_09: "93b39b76-8db0-45f1-b48b-b36ddd8ddcbf",
      WF_10: "25046474-a6f3-4235-837f-81fd3e72f56b",
      WF_11: "7e0a17f4-461b-4404-9eb6-656e4782d476"
  };

  try {
      console.log("Starting Remaining Template Updates...");

      // WF-04 Update
      await updateWorkflow(agent, LOCATION_ID, WF_IDS.WF_04, "WF-04 Invite Booking", [
          { type: "SMS", text: PREMIUM_TEMPLATES.wf04_sms_invite },
          { type: "Email", subject: PREMIUM_TEMPLATES.wf04_email_invite_subject, body: PREMIUM_TEMPLATES.wf04_email_invite_body }
      ]);

      // WF-06 Update
      await updateWorkflow(agent, LOCATION_ID, WF_IDS.WF_06, "WF-06 No-Show Recovery", [
          { type: "SMS", text: PREMIUM_TEMPLATES.wf06_sms_recovery }
      ]);

      // WF-09 Update
      await updateWorkflow(agent, LOCATION_ID, WF_IDS.WF_09, "WF-09 Retainer Follow-up", [
          { type: "Email", subject: PREMIUM_TEMPLATES.wf09_email_retainer_subject, body: PREMIUM_TEMPLATES.wf09_email_retainer_body }
      ]);

      // WF-10 Update
      await updateWorkflow(agent, LOCATION_ID, WF_IDS.WF_10, "WF-10 Post-Consult Follow-up", [
          { type: "Email", subject: PREMIUM_TEMPLATES.wf10_email_summary_subject, body: PREMIUM_TEMPLATES.wf10_email_summary_body }
      ]);

      // WF-11 Update
      await updateWorkflow(agent, LOCATION_ID, WF_IDS.WF_11, "WF-11 Nurture", [
          { type: "Email", subject: PREMIUM_TEMPLATES.wf11_email_nurture_subject, body: PREMIUM_TEMPLATES.wf11_email_nurture_body }
      ]);

      console.log("All remaining updates completed.");

  } catch (e) { console.error("Update Failed", e); }
}

async function updateWorkflow(agent: SkyvernAgent, locationId: string, wfId: string, wfName: string, updates: any[]) {
    console.log(`Updating ${wfName}...`);
    const url = `https://app.gohighlevel.com/location/${locationId}/workflow/${wfId}`;
    
    // Step 1: Open Builder
    await agent.executeStep(
        `Open the workflow builder for '${wfName}'. Wait for it to load.`,
        url
    );

    // Step 2: Apply updates
    for (const update of updates) {
        if (update.type === "SMS") {
            await agent.executeStep(
                `Find the 'Send SMS' action. Click it. In the message box, REPLACE the entire text with: "${update.text.replace(/\n/g, '\\n')}". Click Save Action.`
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
