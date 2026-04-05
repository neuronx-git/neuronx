import { SkyvernAgent } from "./SkyvernAgent";
import { WorkflowSkills } from "../skills/workflowSkills";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  
  if (!resumed) {
      const url = await agent.createSession();
      console.log("\n!!! ACTION REQUIRED !!!");
      console.log("A new Skyvern session has been created.");
      console.log(`Please open this URL to monitor and LOG IN to GoHighLevel:`);
      console.log(url);
      console.log("\nOnce you have logged in, please run this script again to proceed with automation.");
      process.exit(0);
  } else {
      console.log(`Resumed session. App URL: ${agent.getAppUrl()}`);
  }
  
  const skills = new WorkflowSkills(agent);

  const WF_10_ID = "25046474-a6f3-4235-837f-81fd3e72f56b";
  const WF_11_ID = "7e0a17f4-461b-4404-9eb6-656e4782d476";

  // WF-10 Retry
  try {
      console.log("Retrying WF-10...");
      await skills.openWorkflow(WF_10_ID, "Post-Consult Follow-Up");
      await skills.addTrigger(WF_10_ID, "Contact Tag", ["Tag Added is nx:outcome:follow_up"]);
      
      await skills.addAction(WF_10_ID, "Send Email", "Subject: 'Consultation summary', Message: 'Recap...'");
      await skills.addAction(WF_10_ID, "Wait", "Set Wait For to 2 days");
      await skills.addAction(WF_10_ID, "Send SMS", "Message: 'Checking in — any questions?'");
      await skills.addAction(WF_10_ID, "Wait", "Set Wait For to 3 days");
      await skills.addAction(WF_10_ID, "Send Email", "Subject: 'Resources for your immigration journey'");
      await skills.addAction(WF_10_ID, "Wait", "Set Wait For to 2 days");
      await skills.addAction(WF_10_ID, "Add Task", "Title: 'Call/SMS check-in'");
      await skills.addAction(WF_10_ID, "Wait", "Set Wait For to 7 days");
      // This failed last time, maybe try a simpler prompt or just retry
      await skills.addAction(WF_10_ID, "Send Email", "Subject: 'Ready to move forward?', Message: 'Closing email'");
      await skills.addAction(WF_10_ID, "Update Opportunity", "Pipeline: 'NeuronX - Immigration Intake', Stage: 'NURTURE'");

      await skills.saveAndVerify(WF_10_ID, ["Contact Tag", "Send Email", "Update Opportunity"]);
  } catch (e) { console.error("WF-10 Failed", e); }

  // WF-11
  try {
      console.log("Starting WF-11...");
      await skills.openWorkflow(WF_11_ID, "Nurture Campaign Monthly");
      await skills.addTrigger(WF_11_ID, "Contact Tag", ["Tag Added is nx:nurture:enter"]);
      
      // If/Else
      await agent.executeStep(
          "Add action 'If/Else'. Name it 'Check Consent'. Condition 1 'Consent Given': Custom Field 'marketing_consent' is 'True' (or Checked). Save Action.",
          skills.getBuilderUrl(WF_11_ID)
      );

      // Consent Given Branch
      await agent.executeStep("Under 'Consent Given' branch, add 'Send Email'. Subject: 'Monthly Immigration Update'. Save.", skills.getBuilderUrl(WF_11_ID));
      await agent.executeStep("Under 'Consent Given' branch, add 'Wait'. Set Wait For to 30 days. Save.", skills.getBuilderUrl(WF_11_ID));
      await agent.executeStep("Under 'Consent Given' branch, add 'Send Email'. Subject: 'Next Month Newsletter'. Save.", skills.getBuilderUrl(WF_11_ID));
      await agent.executeStep("Under 'Consent Given' branch, add 'Wait'. Set Wait For to 60 days. Save.", skills.getBuilderUrl(WF_11_ID));
      await agent.executeStep("Under 'Consent Given' branch, add 'Send SMS'. Message: 'How are things going?'. Save.", skills.getBuilderUrl(WF_11_ID));

      await skills.saveAndVerify(WF_11_ID, ["Contact Tag", "If/Else", "Send Email"]);
  } catch (e) { console.error("WF-11 Failed", e); }
}

main();
