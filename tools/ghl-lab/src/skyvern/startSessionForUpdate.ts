import { SkyvernAgent } from "./SkyvernAgent";

async function main() {
  const agent = new SkyvernAgent();
  console.log("Creating new session for Template Update...");
  const url = await agent.createSession();
  
  console.log("\n!!! ACTION REQUIRED !!!");
  console.log("A new Skyvern session has been created.");
  console.log(`Please open this URL to monitor and LOG IN to GoHighLevel:`);
  console.log(url);
  console.log("\nOnce you have logged in, please run 'npx tsx src/skyvern/updateTemplates.ts' again.");
}

main();
