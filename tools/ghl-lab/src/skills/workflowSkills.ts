import { SkyvernAgent } from "../skyvern/SkyvernAgent";

const LOCATION_ID = "FlRL82M0D6nclmKT7eXH";

export class WorkflowSkills {
  constructor(private agent: SkyvernAgent) {}

  public getBuilderUrl(workflowId: string): string {
    return `https://app.gohighlevel.com/location/${LOCATION_ID}/workflow/${workflowId}`;
  }

  async openWorkflow(workflowId: string, workflowName: string) {
    const url = this.getBuilderUrl(workflowId);
    return this.agent.executeStep(
      `Verify the workflow builder is open for '${workflowName}'. If a modal overlay appears (like 'Welcome' or 'Tutorial'), dismiss it by clicking 'X' or pressing Escape.`,
      url
    );
  }

  async addTrigger(workflowId: string, triggerName: string, filters: string[]) {
    const url = this.getBuilderUrl(workflowId);
    const filterText = filters.length > 0 ? `Then in the trigger settings on the right, add these Filters: ${filters.join(", ")}.` : "";
    return this.agent.executeStep(
      `Check if there is a trigger '${triggerName}'. If not, click 'Add New Workflow Trigger', search for '${triggerName}', select it. ${filterText} Click 'Save Trigger' at the bottom right. Dismiss any modal if it appears.`,
      url
    );
  }

  async addAction(workflowId: string, actionName: string, configDescription: string) {
    const url = this.getBuilderUrl(workflowId);
    return this.agent.executeStep(
      `Check if there is an action '${actionName}'. If not, click the '+' button to add an action. Search '${actionName}'. Configure it: ${configDescription}. Click 'Save Action' at the bottom right.`,
      url
    );
  }

  async saveAndVerify(workflowId: string, expectedItems: string[]) {
    const url = this.getBuilderUrl(workflowId);
    return this.agent.executeStep(
      `Click the 'Save' button in the top right corner of the builder. Then click 'Publish' if it says 'Draft'. Then Reload the page. After reload, verify that these items are still present: ${expectedItems.join(", ")}.`,
      url
    );
  }
  
  async deleteJunkWorkflows() {
      // Navigate to workflows list
      const listUrl = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`;
      return this.agent.executeStep(
          "Navigate to the Workflows list. Look for any workflows named 'New Workflow : ...' (followed by numbers). For each one found: click the three dots menu on the right, select Delete, and confirm deletion. Repeat until no junk workflows remain.",
          listUrl
      );
  }
}
