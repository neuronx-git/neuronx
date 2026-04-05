import dotenv from "dotenv";
import path from "path";

dotenv.config({ path: path.join(__dirname, "../../.env") });

const API_KEY = process.env.SKYVERN_API_KEY;
const BASE_URL_V1 = "https://api.skyvern.com/v1";
const BASE_URL_API = "https://api.skyvern.com/api/v1";

async function testAPI() {
  if (!API_KEY) {
    console.error("No API Key");
    return;
  }

  // Create session
  console.log("Creating session...");
  const sessionResp = await fetch(`${BASE_URL_V1}/browser_sessions`, {
      method: "POST",
      headers: { "x-api-key": API_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ timeout: 60 }),
  });
  const sessionData = await sessionResp.json();
  const sessionId = sessionData.browser_session_id;
  console.log("Session:", sessionId);

  // Run Task
  console.log("Running task...");
  const taskResp = await fetch(`${BASE_URL_API}/tasks`, {
      method: "POST",
      headers: { "x-api-key": API_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({
          prompt: "Go to example.com",
          url: "https://example.com",
          browser_session_id: sessionId
      })
  });
  const taskData = await taskResp.json();
  const taskId = taskData.task_id;
  console.log("Task ID:", taskId);

  // Check Status
  console.log("Checking status...");
  // Try /api/v1/tasks/{id}
  const statusResp = await fetch(`${BASE_URL_API}/tasks/${taskId}`, {
      method: "GET",
      headers: { "x-api-key": API_KEY }
  });
  if (statusResp.ok) {
      console.log("Status /tasks/{id}:", await statusResp.json());
  } else {
      console.log("Failed /tasks/{id}:", statusResp.status);
      // Try /v1/runs/{id}
      const runResp = await fetch(`${BASE_URL_V1}/runs/${taskId}`, {
          method: "GET",
          headers: { "x-api-key": API_KEY }
      });
      if (runResp.ok) {
          console.log("Status /runs/{id}:", await runResp.json());
      } else {
          console.log("Failed /runs/{id}:", runResp.status);
      }
  }
}

testAPI();
