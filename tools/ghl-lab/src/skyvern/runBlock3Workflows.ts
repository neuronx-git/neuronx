import { SkyvernAgent } from "./SkyvernAgent";
import { WorkflowSkills } from "../skills/workflowSkills";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  if (!resumed) process.exit(1);
  const skills = new WorkflowSkills(agent);

  const WF_07_ID = "83177830-a2d2-4385-8efa-2c9b882d39b6";
  const WF_08_ID = "7c1b7487-f5c7-45e5-91d5-9052489bbbeb";
  const WF_09_ID = "93b39b76-8db0-45f1-b48b-b36ddd8ddcbf";
  const WF_10_ID = "25046474-a6f3-4235-837f-81fd3e72f56b";
  const WF_11_ID = "7e0a17f4-461b-4404-9eb6-656e4782d476";

  // WF-07
  try {
      console.log("Starting WF-07...");
      await skills.openWorkflow(WF_07_ID, "Consultation Outcome Capture");
      await skills.addTrigger(WF_07_ID, "Appointment Status", ["Event Type is 'Completed'", "In Calendar 'Immigration Consultations'"]); // Assuming specific calendar or global
      
      await skills.addAction(WF_07_ID, "Add Task", "Title: 'Record consultation outcome in custom field'");
      await skills.addAction(WF_07_ID, "Wait", "Set Wait For to 1 hour");
      await skills.addAction(WF_07_ID, "Internal Notification", "Type: 'Notification', Message: 'Outcome still needed for {{contact.name}}', Redirect to Contact"); 
      await skills.addAction(WF_07_ID, "Wait", "Set Wait For to 3 hours");
      await skills.addAction(WF_07_ID, "Internal Notification", "Type: 'Notification', Message: 'Missing outcome for {{contact.name}}'");

      await skills.saveAndVerify(WF_07_ID, ["Appointment Status", "Add Task", "Internal Notification"]);
  } catch (e) { console.error("WF-07 Failed", e); }

  // WF-08 (Branching)
  try {
      console.log("Starting WF-08...");
      await skills.openWorkflow(WF_08_ID, "Outcome Routing");
      await skills.addTrigger(WF_08_ID, "Contact Changed", ["Field is 'consultation_outcome'"]);
      
      // If/Else
      await agent.executeStep(
          "Add action 'If/Else'. Name it 'Check Outcome'. Condition 1 'Proceed': Custom Field 'consultation_outcome' is 'Proceed'. Condition 2 'Follow-Up': Custom Field 'consultation_outcome' is 'Follow-Up'. Save Action.",
          skills["getBuilderUrl"](WF_08_ID)
      );

      // Proceed Branch
      await agent.executeStep("Under 'Proceed' branch, add 'Add Contact Tag'. Tag: 'nx:outcome:proceed'. Save.", skills["getBuilderUrl"](WF_08_ID));
      await agent.executeStep("Under 'Proceed' branch, add 'Update Opportunity'. Pipeline: 'NeuronX - Immigration Intake', Stage: 'CONSULT COMPLETED'. Save.", skills["getBuilderUrl"](WF_08_ID));

      // Follow-Up Branch
      await agent.executeStep("Under 'Follow-Up' branch, add 'Add Contact Tag'. Tag: 'nx:outcome:follow_up'. Save.", skills["getBuilderUrl"](WF_08_ID));
      await agent.executeStep("Under 'Follow-Up' branch, add 'Update Opportunity'. Pipeline: 'NeuronX - Immigration Intake', Stage: 'CONSULT COMPLETED'. Save.", skills["getBuilderUrl"](WF_08_ID));

      // Else (Declined)
      await agent.executeStep("Under 'None' branch, add 'Add Contact Tag'. Tag: 'nx:outcome:declined'. Save.", skills["getBuilderUrl"](WF_08_ID));
      await agent.executeStep("Under 'None' branch, add 'Update Opportunity'. Pipeline: 'NeuronX - Immigration Intake', Stage: 'LOST'. Save.", skills["getBuilderUrl"](WF_08_ID));

      await skills.saveAndVerify(WF_08_ID, ["Contact Changed", "If/Else", "Update Opportunity"]);
  } catch (e) { console.error("WF-08 Failed", e); }

  // WF-09
  try {
      console.log("Starting WF-09...");
      await skills.openWorkflow(WF_09_ID, "Retainer Follow-Up");
      await skills.addTrigger(WF_09_ID, "Contact Tag", ["Tag Added is nx:outcome:proceed"]);
      
      await skills.addAction(WF_09_ID, "Send Email", "Subject: 'Next steps: retainer & checklist', Message: 'Here is the retainer doc...'");
      await skills.addAction(WF_09_ID, "Update Contact Field", "Field: 'retainer_sent', Value: 'true' (or checked)"); // Boolean checkbox or text? Guide says "Set retainer_sent = true".
      await skills.addAction(WF_09_ID, "Wait", "Set Wait For to 1 day");
      await skills.addAction(WF_09_ID, "Send SMS", "Message: 'Just checking in — did you receive the retainer?'");
      await skills.addAction(WF_09_ID, "Wait", "Set Wait For to 1 day");
      await skills.addAction(WF_09_ID, "Send SMS", "Message: 'Follow-up on retainer'");
      await skills.addAction(WF_09_ID, "Wait", "Set Wait For to 3 days");
      await skills.addAction(WF_09_ID, "Send Email", "Subject: 'Retainer follow-up'");
      await skills.addAction(WF_09_ID, "Wait", "Set Wait For to 5 days");
      await skills.addAction(WF_09_ID, "Add Task", "Title: 'Consultant call — Day 10 retainer chase'");
      await skills.addAction(WF_09_ID, "Wait", "Set Wait For to 4 days");
      await skills.addAction(WF_09_ID, "Send Email", "Subject: 'Final follow-up', Message: 'Final notice'");
      await skills.addAction(WF_09_ID, "Update Opportunity", "Pipeline: 'NeuronX - Immigration Intake', Stage: 'NURTURE'");

      await skills.saveAndVerify(WF_09_ID, ["Contact Tag", "Send Email", "Update Opportunity"]);
  } catch (e) { console.error("WF-09 Failed", e); }

  // WF-10
  try {
      console.log("Starting WF-10...");
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
      await skills.addAction(WF_10_ID, "Send Email", "Subject: 'Ready to move forward?'");
      await skills.addAction(WF_10_ID, "Update Opportunity", "Pipeline: 'NeuronX - Immigration Intake', Stage: 'NURTURE'");

      await skills.saveAndVerify(WF_10_ID, ["Contact Tag", "Send Email", "Update Opportunity"]);
  } catch (e) { console.error("WF-10 Failed", e); }

  // WF-11 (Branching)
  try {
      console.log("Starting WF-11...");
      await skills.openWorkflow(WF_11_ID, "Nurture Campaign Monthly");
      await skills.addTrigger(WF_11_ID, "Contact Tag", ["Tag Added is nx:nurture:enter"]);
      
      // If/Else
      await agent.executeStep(
          "Add action 'If/Else'. Name it 'Check Consent'. Condition 1 'Consent Given': Custom Field 'marketing_consent' is 'True' (or Checked). Save Action.",
          skills["getBuilderUrl"](WF_11_ID)
      );

      // Consent Given Branch
      await agent.executeStep("Under 'Consent Given' branch, add 'Send Email'. Subject: 'Monthly Immigration Update'. Save.", skills["getBuilderUrl"](WF_11_ID));
      await agent.executeStep("Under 'Consent Given' branch, add 'Wait'. Set Wait For to 30 days. Save.", skills["getBuilderUrl"](WF_11_ID));
      await agent.executeStep("Under 'Consent Given' branch, add 'Send Email'. Subject: 'Next Month Newsletter'. Save.", skills["getBuilderUrl"](WF_11_ID));
      await agent.executeStep("Under 'Consent Given' branch, add 'Wait'. Set Wait For to 60 days. Save.", skills["getBuilderUrl"](WF_11_ID));
      await agent.executeStep("Under 'Consent Given' branch, add 'Send SMS'. Message: 'How are things going?'. Save.", skills["getBuilderUrl"](WF_11_ID));

      // No Consent Branch (None) -> Do nothing

      await skills.saveAndVerify(WF_11_ID, ["Contact Tag", "If/Else", "Send Email"]);
  } catch (e) { console.error("WF-11 Failed", e); }
}

main();
