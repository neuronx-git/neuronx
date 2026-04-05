import { SkyvernAgent } from "./SkyvernAgent";
import { WorkflowSkills } from "../skills/workflowSkills";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  if (!resumed) {
      console.log("Session expired. Run skyvernOrchestrator.ts first.");
      process.exit(1);
  }
  const skills = new WorkflowSkills(agent);

  const WF_03_ID = "fb1215b4-8343-4ccb-b874-12cfb616afea";
  const WF_04_ID = "838f7c38-3534-4d3b-9d4c-40b11f4a6772";
  const WF_05_ID = "9af911d1-b025-45d4-a083-f62364752318";
  const WF_06_ID = "5d0c1920-bf7b-45c2-9cf9-e40466e3e0aa";

  // WF-03
  try {
      console.log("Starting WF-03...");
      await skills.openWorkflow(WF_03_ID, "Mark Contacted Readiness");
      await skills.addTrigger(WF_03_ID, "Contact Tag", ["Tag Added is nx:contacted"]);
      await skills.addAction(WF_03_ID, "Add Contact Tag", "Tag: 'nx:assessment:required'");
      await skills.addAction(WF_03_ID, "Add Task", "Title: 'Complete readiness assessment (R1-R6)'");
      await skills.saveAndVerify(WF_03_ID, ["Contact Tag", "Add Contact Tag", "Add Task"]);
  } catch (e) { console.error("WF-03 Failed", e); }

  // WF-04 (Complex Branching)
  try {
      console.log("Starting WF-04...");
      await skills.openWorkflow(WF_04_ID, "Readiness Complete Invite Booking");
      await skills.addTrigger(WF_04_ID, "Contact Tag", ["Tag Added is nx:assessment:complete"]);
      
      // Special handling for branching
      // 1. Add If/Else
      await agent.executeStep(
          "Add action 'If/Else'. Name it 'Check Readiness'. Condition 1 'Ready': Custom Field 'readiness_outcome' is 'Ready' OR 'Ready - Urgent'. Condition 2 'Not Ready': Custom Field 'readiness_outcome' is 'Not Ready'. Save Action.", 
          skills["getBuilderUrl"](WF_04_ID)
      );
      
      // 2. YES Branch (Ready)
      await agent.executeStep(
          "Under the 'Ready' branch, add action 'Update Opportunity'. Pipeline: 'NeuronX - Immigration Intake', Stage: 'CONSULT READY'. Save.", 
          skills["getBuilderUrl"](WF_04_ID)
      );
      await agent.executeStep("Under the 'Ready' branch (after Update Opportunity), add action 'Add Contact Tag'. Tag: 'nx:consult_ready'. Save.", skills["getBuilderUrl"](WF_04_ID));
      await agent.executeStep("Under the 'Ready' branch (after Tag), add action 'Send SMS'. Message: 'Please book your consultation here: [link]'. Save.", skills["getBuilderUrl"](WF_04_ID));
      await agent.executeStep("Under the 'Ready' branch (after SMS), add action 'Send Email'. Subject: 'Book your consultation', Message: 'Link: [link]'. Save.", skills["getBuilderUrl"](WF_04_ID));
      await agent.executeStep("Under the 'Ready' branch (after Email), add action 'Add Contact Tag'. Tag: 'nx:booking:invited'. Save.", skills["getBuilderUrl"](WF_04_ID));

      // 3. Not Ready Branch
      await agent.executeStep(
          "Under the 'Not Ready' branch, add action 'Update Opportunity'. Pipeline: 'NeuronX - Immigration Intake', Stage: 'NURTURE'. Save.", 
          skills["getBuilderUrl"](WF_04_ID)
      );
      await agent.executeStep("Under the 'Not Ready' branch, add action 'Add Contact Tag'. Tag: 'nx:nurture:enter'. Save.", skills["getBuilderUrl"](WF_04_ID));

      // 4. Else Branch (Disqualified)
      await agent.executeStep(
          "Under the 'None' (Else) branch, add action 'Update Opportunity'. Pipeline: 'NeuronX - Immigration Intake', Stage: 'LOST'. Save.", 
          skills["getBuilderUrl"](WF_04_ID)
      );
      await agent.executeStep("Under the 'None' branch, add action 'Add Contact Tag'. Tag: 'nx:lost'. Save.", skills["getBuilderUrl"](WF_04_ID));

      await skills.saveAndVerify(WF_04_ID, ["Contact Tag", "If/Else", "Update Opportunity"]);
  } catch (e) { console.error("WF-04 Failed", e); }

  // WF-05
  try {
      console.log("Starting WF-05...");
      await skills.openWorkflow(WF_05_ID, "Appointment Booked Reminders");
      // Trigger: Appointment Status
      await skills.addTrigger(WF_05_ID, "Appointment Status", ["Event Type is 'Customer Booked Appointment'", "In Calendar 'Immigration Consultations'"]);
      
      await skills.addAction(WF_05_ID, "Update Opportunity", "Pipeline: 'NeuronX - Immigration Intake', Stage: 'BOOKED'");
      await skills.addAction(WF_05_ID, "Add Contact Tag", "Tag: 'nx:booking:confirmed'");
      await skills.addAction(WF_05_ID, "Send SMS", "Message: 'Consultation confirmed for {{appointment.start_time}}.'");
      await skills.addAction(WF_05_ID, "Send Email", "Subject: 'Consultation Confirmed', Message: 'Details: {{appointment.start_time}}'");
      
      // Waits
      await skills.addAction(WF_05_ID, "Wait", "Select 'Event/Appointment Time'. Select 'Before'. Set to 48 hours / 2 days.");
      await skills.addAction(WF_05_ID, "Send SMS", "Message: 'Your consultation is in 2 days. Reply YES to confirm.'");
      
      await skills.addAction(WF_05_ID, "Wait", "Select 'Event/Appointment Time'. Select 'Before'. Set to 24 hours / 1 day.");
      await skills.addAction(WF_05_ID, "Send SMS", "Message: 'Reminder: consultation tomorrow at {{appointment.time}}'");
      
      await skills.addAction(WF_05_ID, "Wait", "Select 'Event/Appointment Time'. Select 'Before'. Set to 2 hours.");
      await skills.addAction(WF_05_ID, "Send SMS", "Message: 'Your consultation starts in 2 hours.'");

      await skills.saveAndVerify(WF_05_ID, ["Appointment Status", "Wait", "Send SMS"]);
  } catch (e) { console.error("WF-05 Failed", e); }

  // WF-06
  try {
      console.log("Starting WF-06...");
      await skills.openWorkflow(WF_06_ID, "No-Show Recovery");
      await skills.addTrigger(WF_06_ID, "Appointment Status", ["Event Type is 'No-Show'"]); // Filter might just be "Appointment Status is No-Show" or "Event Type is No-Show"
      
      await skills.addAction(WF_06_ID, "Add Contact Tag", "Tag: 'nx:appointment:noshow'");
      await skills.addAction(WF_06_ID, "Wait", "Set Wait For to 5 minutes");
      await skills.addAction(WF_06_ID, "Send SMS", "Message: 'We missed you! Reschedule here: [link]'");
      await skills.addAction(WF_06_ID, "Wait", "Set Wait For to 10 minutes");
      await skills.addAction(WF_06_ID, "Add Task", "Title: 'Call no-show within 15 min'");
      await skills.addAction(WF_06_ID, "Wait", "Set Wait For to 2 hours");
      await skills.addAction(WF_06_ID, "Send SMS", "Message: 'Reschedule link: [link]'");
      await skills.addAction(WF_06_ID, "Wait", "Set Wait For to 1 day");
      await skills.addAction(WF_06_ID, "Send SMS", "Message: 'Follow up'");
      await skills.addAction(WF_06_ID, "Wait", "Set Wait For to 3 days");
      await skills.addAction(WF_06_ID, "Send Email", "Subject: 'We would love to reschedule', Message: 'Please book here: [link]'");
      await skills.addAction(WF_06_ID, "Wait", "Set Wait For to 7 days");
      await skills.addAction(WF_06_ID, "Send SMS", "Message: 'Final attempt to reschedule'");
      await skills.addAction(WF_06_ID, "Update Opportunity", "Pipeline: 'NeuronX - Immigration Intake', Stage: 'NURTURE'");

      await skills.saveAndVerify(WF_06_ID, ["Appointment Status", "Add Task", "Update Opportunity"]);
  } catch (e) { console.error("WF-06 Failed", e); }
}

main();
