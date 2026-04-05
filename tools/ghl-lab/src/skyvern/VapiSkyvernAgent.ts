import dotenv from "dotenv";
import fs from "fs";
import path from "path";

dotenv.config({ path: path.join(__dirname, "../../.env") });

const SKYVERN_API_KEY = process.env.SKYVERN_API_KEY;
const VAPI_SESSION_FILE = path.join(__dirname, "../../.vapi-skyvern-session.json");
const BASE_URL_V1 = "https://api.skyvern.com/v1";
const BASE_URL_API = "https://api.skyvern.com/api/v1";

export class VapiSkyvernAgent {
  private sessionId: string | null = null;
  private appUrl: string | null = null;

  constructor() {
    if (!SKYVERN_API_KEY) {
      throw new Error("SKYVERN_API_KEY is not set in .env");
    }
  }

  async loadSession(): Promise<boolean> {
    if (fs.existsSync(VAPI_SESSION_FILE)) {
      const data = JSON.parse(fs.readFileSync(VAPI_SESSION_FILE, "utf-8"));
      try {
        const resp = await fetch(`${BASE_URL_V1}/browser_sessions/${data.sessionId}`, {
            method: "GET",
            headers: { "x-api-key": SKYVERN_API_KEY! }
        });
        if (resp.ok) {
            const sessionData = await resp.json();
            if (sessionData.status === 'terminated' || sessionData.status === 'completed') {
                console.log("Vapi Session terminated/completed. Creating new.");
                return false;
            }
            this.sessionId = data.sessionId;
            this.appUrl = data.appUrl;
            console.log(`Resumed Vapi Skyvern session: ${this.sessionId}`);
            return true;
        }
      } catch (e) {
        console.log("Saved Vapi session invalid. Creating new.");
      }
    }
    return false;
  }

  async createSession() {
    console.log("Creating new Vapi Skyvern browser session...");
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
    
    fs.writeFileSync(VAPI_SESSION_FILE, JSON.stringify({ 
        sessionId: this.sessionId,
        appUrl: this.appUrl 
    }, null, 2));
    
    console.log(`Created new Vapi Skyvern session: ${this.sessionId}`);
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
    
    const targetUrl = url || "https://dashboard.vapi.ai";

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