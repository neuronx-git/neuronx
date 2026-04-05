import { SkyvernAgent } from "./SkyvernAgent";
import { WorkflowSkills } from "../skills/workflowSkills";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  if (!resumed) process.exit(1);
  const skills = new WorkflowSkills(agent);

  try {
      console.log("Starting Junk Cleanup...");
      await skills.deleteJunkWorkflows();
      console.log("Cleanup Completed.");
  } catch (e) { console.error("Cleanup Failed", e); }
}

main();
