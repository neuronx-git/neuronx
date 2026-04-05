import { Skyvern } from "@skyvern/client";
import dotenv from "dotenv";
import path from "path";

dotenv.config({ path: path.join(__dirname, "../../.env") });

async function main() {
  const apiKey = process.env.SKYVERN_API_KEY;
  if (!apiKey) {
    console.error("No API Key found");
    process.exit(1);
  }
  
  console.log("Initializing Skyvern client...");
  const client = new Skyvern({
    apiKey: apiKey,
  });

  try {
    console.log("Creating browser session...");
    // Check if browserSessions.create exists
    const session = await client.browserSessions.create({
        // url: "https://app.gohighlevel.com", // Optional initial URL
    });
    console.log("Session Created:", session);
    console.log("Session ID:", session.browser_session_id);

    // Run a simple task to check login status
    console.log("Running task to check login status...");
    const task = await client.runTask({
      prompt: "Check if the user is logged in. If you see a login form, say 'Not Logged In'. If you see a dashboard, say 'Logged In'.",
      url: "https://app.gohighlevel.com",
      browser_session_id: session.browser_session_id,
    });
    
    console.log("Task Response:", task);
  } catch (error) {
    console.error("Error:", error);
  }
}

main();
