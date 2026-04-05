import { SkyvernAgent } from "./SkyvernAgent";
import { WorkflowSkills } from "../skills/workflowSkills";

async function main() {
  const agent = new SkyvernAgent();
  
  // 1. Session Management
  const resumed = await agent.loadSession();
  if (!resumed) {
      console.log("Session expired or not found. Please run skyvernOrchestrator.ts first to login.");
      process.exit(1);
  }
  console.log(`Resumed session. App URL: ${agent.getAppUrl()}`);

  const skills = new WorkflowSkills(agent);
  const WF_02_ID = "43ecd109-6595-4f51-a0e0-e2421b3f8131";
  const WF_NAME = "Contact Attempt Sequence";

  try {
      console.log(`\nStarting ${WF_NAME} Configuration...`);
      
      // Step 1: Open Workflow
      await skills.openWorkflow(WF_02_ID, WF_NAME);

      // Step 2: Add Trigger
      await skills.addTrigger(WF_02_ID, "Contact Tag", ["Tag Added is nx:contacting:start"]);

      // Step 3: Add Actions
      // 1. Create Manual Action (Task)
      await skills.addAction(WF_02_ID, "Add Task", "Title: 'Call lead (Attempt 1)', Description: 'Initial outreach', Due Date: 0 days"); 
      // Note: "Create Manual Action" might be called "Add Task" in GHL. Guide says "Create Manual Action (Task)".

      // 2. Wait 30 mins
      await skills.addAction(WF_02_ID, "Wait", "Set Wait For to 30 minutes");

      // 3. Send SMS
      await skills.addAction(WF_02_ID, "Send SMS", "Message: 'Hi {{contact.first_name}}, we tried reaching you. You can book a call here: [calendar link]. Reply to this message anytime.'");

      // 4. Wait 2 hours
      await skills.addAction(WF_02_ID, "Wait", "Set Wait For to 2 hours");

      // 5. Create Manual Action (Task)
      await skills.addAction(WF_02_ID, "Add Task", "Title: 'Call lead (Attempt 2)'");

      // 6. Wait 1 business day
      await skills.addAction(WF_02_ID, "Wait", "Set Wait For to 1 day. Enable 'Advanced Window' if needed to ensure business day, or just set 1 day.");

      // 7. Create Manual Action (Task)
      await skills.addAction(WF_02_ID, "Add Task", "Title: 'Call lead (Attempt 3) + voicemail'");

      // 8. Wait 2 business days
      await skills.addAction(WF_02_ID, "Wait", "Set Wait For to 2 days");

      // 9. Send SMS
      await skills.addAction(WF_02_ID, "Send SMS", "Message: 'Hi {{contact.first_name}}, please book a call here: [booking link]. Reply if you need help.'");

      // 10. Wait 5 business days
      await skills.addAction(WF_02_ID, "Wait", "Set Wait For to 5 days");

      // 11. Send Email
      await skills.addAction(WF_02_ID, "Send Email", "Subject: 'Still interested?', Message: 'Hi {{contact.first_name}}, are you still looking for help? Book here: [booking link].'");

      // 12. Wait 10 business days
      await skills.addAction(WF_02_ID, "Wait", "Set Wait For to 10 days");

      // 13. Send SMS
      await skills.addAction(WF_02_ID, "Send SMS", "Message: 'We would still love to help. Book here: [link]'");

      // 14. Update Opportunity
      await skills.addAction(WF_02_ID, "Update Opportunity", "Pipeline: 'NeuronX - Immigration Intake', Stage: 'UNREACHABLE'");

      // 15. Add Contact Tag
      await skills.addAction(WF_02_ID, "Add Contact Tag", "Tag: 'nx:nurture:enter'");

      // Step 4: Save & Verify
      await skills.saveAndVerify(WF_02_ID, ["Contact Tag", "Call lead (Attempt 1)", "Wait", "Send SMS", "Update Opportunity"]);

      console.log(`${WF_NAME} Configuration Completed.`);

  } catch (error) {
      console.error("Workflow Execution Failed:", error);
  }
}

main();
