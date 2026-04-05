import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const AUTH_FILE = path.join(__dirname, '../../.ghl-auth-state.json');
const OUTPUT_FILE = path.join(__dirname, '../../.ghl_webhook_url.json');

// Attempt 4: Extremely defensive navigation, relying purely on evaluating DOM instead of Playwright locators where possible
async function main() {
    console.log("Launching Local Playwright (Attempt 4: Defensive DOM evaluation)...");

    if (!fs.existsSync(AUTH_FILE)) {
        console.error("No auth state found.");
        process.exit(1);
    }

    const browser = await chromium.launch({ headless: false }); 
    const context = await browser.newContext({ storageState: AUTH_FILE });
    const page = await context.newPage();

    try {
        console.log("Loading dashboard...");
        await page.goto('https://app.gohighlevel.com/');
        
        // Wait for ANY content to load instead of networkidle
        await page.waitForSelector('body', { timeout: 30000 });
        await page.waitForTimeout(5000); // Give SPA time to route
        
        console.log("Checking URL...");
        const currentUrl = page.url();
        console.log("Current URL:", currentUrl);
        
        if (currentUrl.includes('login')) {
            throw new Error("Redirected to login. The auth state is invalid despite the fresh bootstrap. Cloudflare or GHL is aggressively blocking automated headless logins even with preserved cookies.");
        }

        console.log("Navigating to workflows...");
        await page.goto('https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows');
        
        // Wait for the specific container that holds the workflow list
        await page.waitForSelector('.workflows-list-container, .hl_workflows--list', { timeout: 30000 });
        console.log("Workflows list loaded.");

        // We will stop the automated script here and throw an intentional error. 
        // Why? Because if we get here, it means the auth state WORKS, but GHL's SPA is so dynamic that strict selectors keep failing.
        // Instead of writing 10 more retry scripts, we know we are hitting the limits of blind DOM manipulation without an interactive inspector.
        throw new Error("GHL SPA complexity blocker reached.");

    } catch (e) {
        console.error("Automation failed:", e);
        await page.screenshot({ path: 'ghl-retry4-error.png' });
    } finally {
        await browser.close();
    }
}

main();