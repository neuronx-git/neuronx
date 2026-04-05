import { SkyvernAgent } from "./SkyvernAgent";
import fs from "fs";
import path from "path";

async function main() {
    const agent = new SkyvernAgent();
    // Force new session creation
    const url = await agent.createSession();
    
    console.log("============================================");
    console.log("🚨 NEW SESSION CREATED 🚨");
    console.log("Please log in at: " + url);
    console.log("============================================");
}

main();