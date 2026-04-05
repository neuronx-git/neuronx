import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import readline from 'readline';

const AUTH_FILE = path.join(__dirname, '../../.ghl-auth-state.json');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function main() {
    console.log("========================================================");
    console.log("🚨 ACTION REQUIRED: GHL FRESH AUTHENTICATION BOOTSTRAP 🚨");
    console.log("========================================================");
    console.log("A local browser window will open shortly.");
    console.log("1. Please log into GoHighLevel in that window.");
    console.log("2. Select the 'NeuronX Test Lab' sub-account.");
    console.log("3. Once you see the dashboard, come back to this terminal and press ENTER.");
    console.log("========================================================");

    const browser = await chromium.launch({ headless: false }); 
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto('https://app.gohighlevel.com/');

    rl.question('Press ENTER when you have fully logged in and selected the sub-account...', async () => {
        console.log("Saving fresh authentication state...");
        
        await context.storageState({ path: AUTH_FILE });
        
        console.log(`✅ Auth state saved to ${AUTH_FILE}`);
        
        await browser.close();
        rl.close();
        process.exit(0);
    });
}

main();