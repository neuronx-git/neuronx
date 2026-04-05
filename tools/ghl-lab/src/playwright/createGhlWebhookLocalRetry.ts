import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const AUTH_FILE = path.join(__dirname, '../../.ghl-auth-state.json');
const OUTPUT_FILE = path.join(__dirname, '../../.ghl_webhook_url.json');

async function main() {
    console.log("Launching Local Playwright for GHL Webhook Creation (Retry)...");

    if (!fs.existsSync(AUTH_FILE)) {
        console.error("No auth state found. Cannot proceed without manual login.");
        process.exit(1);
    }

    const browser = await chromium.launch({ headless: false }); 
    const context = await browser.newContext({ storageState: AUTH_FILE });
    const page = await context.newPage();

    try {
        console.log("Navigating to Dashboard root first...");
        await page.goto('https://app.gohighlevel.com/');
        await page.waitForTimeout(5000); // Wait for hydration

        console.log("Navigating to Automation...");
        // Try clicking navigation instead of direct URL to ensure SPA state
        // This is safer against white-screen freezes
        await page.goto('https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows');
        
        // Wait for specific element instead of networkidle
        await page.waitForSelector('text=Create Workflow', { timeout: 60000 });

        console.log("Creating new Workflow...");
        await page.getByText('Create Workflow').click();
        
        console.log("Selecting Start from Scratch...");
        // The modal might take a second
        await page.waitForSelector('text=Start from Scratch');
        await page.getByText('Start from Scratch').click();
        await page.getByText('Continue').click();

        console.log("Waiting for Editor...");
        await page.waitForSelector('.workflow-name', { timeout: 60000 });
        
        console.log("Renaming workflow...");
        // Sometimes the click doesn't register if JS isn't ready
        await page.waitForTimeout(2000); 
        await page.locator('.workflow-name').click();
        await page.locator('.workflow-name input').fill('WF-04B — Vapi Return Handler');
        
        console.log("Adding Inbound Webhook Trigger...");
        await page.getByText('Add New Trigger').click();
        await page.getByPlaceholder('Search Triggers').fill('Inbound Webhook');
        // Wait for search results
        await page.waitForTimeout(1000);
        await page.getByText('Inbound Webhook').first().click();
        
        console.log("Extracting URL...");
        // The input usually has a copy button next to it
        // We'll try to find the input that contains "services.leadconnectorhq.com"
        await page.waitForTimeout(2000); // Let the URL generate
        
        // Try multiple selectors
        const webhookUrl = await page.evaluate(() => {
            const inputs = Array.from(document.querySelectorAll('input'));
            const webhookInput = inputs.find(i => i.value.includes('hooks.leadconnectorhq.com') || i.value.includes('services.leadconnectorhq.com'));
            return webhookInput ? webhookInput.value : null;
        });

        if (webhookUrl) {
            console.log(`✅ Captured Webhook URL: ${webhookUrl}`);
            fs.writeFileSync(OUTPUT_FILE, JSON.stringify({ webhookUrl }, null, 2));
        } else {
            throw new Error("Could not find Webhook URL in DOM");
        }
        
        console.log("Saving Trigger...");
        await page.getByText('Save Trigger').click();
        
        console.log("Publishing...");
        await page.locator('.workflow-status-toggle').click();
        await page.getByText('Save').last().click();
        console.log("Saved.");

    } catch (e) {
        console.error("Automation failed:", e);
        await page.screenshot({ path: 'ghl-retry-error.png' });
    } finally {
        await browser.close();
    }
}

main();