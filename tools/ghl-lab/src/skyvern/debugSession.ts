import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  const resumed = await agent.loadSession();
  if (!resumed) {
      console.log("No session.");
      process.exit(1);
  }

  try {
      console.log("Debugging session...");
      // Try navigating to Dashboard to reset state
      const result = await agent.executeStep(
          "Navigate to the main Dashboard. Describe what you see.",
          "https://app.gohighlevel.com/"
      );
      console.log("Debug Result:", result.output);
  } catch (e) {
      console.error("Debug Failed:", e);
  }
}

main();
