import dotenv from "dotenv";
import fs from "fs";
import path from "path";

dotenv.config({ path: path.join(__dirname, "../../.env") });

const SKYVERN_API_KEY = process.env.SKYVERN_API_KEY;
const SESSION_FILE = path.join(__dirname, "../../.skyvern-session.json");
const BASE_URL_V1 = "https://api.skyvern.com/v1";
const BASE_URL_API = "https://api.skyvern.com/api/v1";

interface SkyvernSession {
  browser_session_id: string;
  app_url: string;
  status: string;
}

export class SkyvernAgent {
  private sessionId: string | null = null;
  private appUrl: string | null = null;

  constructor() {
    if (!SKYVERN_API_KEY) {
      throw new Error("SKYVERN_API_KEY is not set in .env");
    }
  }

  async loadSession(): Promise<boolean> {
    if (fs.existsSync(SESSION_FILE)) {
      const data = JSON.parse(fs.readFileSync(SESSION_FILE, "utf-8"));
      // Verify if session is valid
      try {
        const resp = await fetch(`${BASE_URL_V1}/browser_sessions/${data.sessionId}`, {
            method: "GET",
            headers: { "x-api-key": SKYVERN_API_KEY! }
        });
        if (resp.ok) {
            const sessionData = await resp.json();
            if (sessionData.status === 'terminated' || sessionData.status === 'completed') {
                console.log("Session terminated/completed. Creating new.");
                return false;
            }
            this.sessionId = data.sessionId;
            this.appUrl = data.appUrl; // Assuming we saved it
            console.log(`Resumed Skyvern session: ${this.sessionId}`);
            return true;
        }
      } catch (e) {
        console.log("Saved session invalid. Creating new.");
      }
    }
    return false;
  }

  async createSession() {
    console.log("Creating new Skyvern browser session...");
    const response = await fetch(`${BASE_URL_V1}/browser_sessions`, {
        method: "POST",
        headers: { "x-api-key": SKYVERN_API_KEY!, "Content-Type": "application/json" },
        body: JSON.stringify({ timeout: 60 }),
    });

    if (!response.ok) {
        throw new Error(`Failed to create session: ${response.status} ${await response.text()}`);
    }

    const data = await response.json();
    this.sessionId = data.browser_session_id;
    this.appUrl = data.app_url;
    
    fs.writeFileSync(SESSION_FILE, JSON.stringify({ 
        sessionId: this.sessionId,
        appUrl: this.appUrl 
    }, null, 2));
    
    console.log(`Created new Skyvern session: ${this.sessionId}`);
    console.log(`Live View URL: ${this.appUrl}`);
    return this.appUrl;
  }

  getAppUrl() {
      return this.appUrl;
  }

  async executeStep(prompt: string, url?: string) {
    if (!this.sessionId) {
      throw new Error("No active session. Call loadSession() or createSession() first.");
    }

    console.log(`Executing Step: "${prompt}"...`);
    
    // If url is explicitly null/undefined, we MUST omit it from payload?
    // Wait, the error "Field required" means url is MANDATORY in the body schema.
    // BUT previous error "Input should be a valid string" means it cannot be null.
    // This implies we MUST provide a string URL.
    // If we are continuing in a session, what URL do we use?
    // We can use the last known URL or just the base app URL?
    // Or maybe we can fetch the current URL from the session status?
    // For now, let's fallback to "https://app.gohighlevel.com" if not provided, 
    // effectively reloading or just satisfying the schema. 
    // Actually, if we provide a URL, Skyvern might navigate there. 
    // If we want to stay on current page, we might be stuck if URL is required.
    // Let's check if we can pass an empty string? 
    // Or maybe we should track the current URL in the agent.
    
    const targetUrl = url || this.appUrl || "https://app.gohighlevel.com";

    const payload: any = {
        prompt,
        url: targetUrl,
        browser_session_id: this.sessionId,
        include_action_history_in_verification: true
    };

    const response = await fetch(`${BASE_URL_API}/tasks`, {
        method: "POST",
        headers: { "x-api-key": SKYVERN_API_KEY!, "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        throw new Error(`Task submission failed: ${response.status} ${await response.text()}`);
    }

    const taskData = await response.json();
    const taskId = taskData.task_id;
    console.log(`Task Started: ${taskId}`);

    // Poll for completion
    let status = 'queued';
    let finalResult = null;
    
    while (['queued', 'running', 'created'].includes(status)) {
        await new Promise(resolve => setTimeout(resolve, 5000));
        
        const statusResp = await fetch(`${BASE_URL_API}/tasks/${taskId}`, {
            method: "GET",
            headers: { "x-api-key": SKYVERN_API_KEY! }
        });
        
        if (!statusResp.ok) {
            console.error(`Status check failed: ${statusResp.status}`);
            continue;
        }
        
        const runData = await statusResp.json();
        status = runData.status;
        process.stdout.write(".");
        
        if (['completed', 'failed', 'terminated', 'timed_out'].includes(status)) {
            finalResult = runData;
            break;
        }
    }
    console.log(`\nFinal Status: ${status}`);
    
    if (status !== 'completed') {
        throw new Error(`Step failed with status: ${status}`);
    }

    return finalResult;
  }
}
