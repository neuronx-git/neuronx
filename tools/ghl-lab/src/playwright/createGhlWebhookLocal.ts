import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const AUTH_FILE = path.join(__dirname, '../../.ghl-auth-state.json');
const OUTPUT_FILE = path.join(__dirname, '../../.ghl_webhook_url.json');

async function main() {
    console.log("Launching Local Playwright for GHL Webhook Creation...");

    if (!fs.existsSync(AUTH_FILE)) {
        console.error("No auth state found. Cannot proceed without manual login.");
        process.exit(1);
    }

    const browser = await chromium.launch({ headless: false }); // Visible for debugging
    const context = await browser.newContext({ storageState: AUTH_FILE });
    const page = await context.newPage();

    try {
        console.log("Navigating to Workflows...");
        // Go directly to workflow list
        await page.goto('https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows');
        await page.waitForLoadState('networkidle');

        // Check if we need to create or edit
        // We'll just create a new one to be safe and distinct
        console.log("Creating new Workflow...");
        await page.getByText('Create Workflow').click();
        
        // Handle the "Start from scratch" modal
        try {
            await page.getByText('Start from Scratch').click({ timeout: 5000 });
            await page.getByText('Continue').click();
        } catch (e) {
            console.log("Might already be in editor or UI changed.");
        }

        await page.waitForLoadState('networkidle');
        
        // Name the workflow
        console.log("Renaming workflow...");
        await page.locator('.workflow-name').click();
        await page.locator('.workflow-name input').fill('WF-04B — Vapi Return Handler');
        
        // Add Trigger
        console.log("Adding Inbound Webhook Trigger...");
        await page.getByText('Add New Trigger').click();
        await page.getByPlaceholder('Search Triggers').fill('Inbound Webhook');
        await page.getByText('Inbound Webhook').first().click();
        
        // Capture URL
        // Wait for the URL input to appear. It usually auto-generates.
        const urlLocator = page.locator('input[readonly]').first(); // Usually the webhook URL is readonly
        await urlLocator.waitFor({ state: 'visible' });
        const webhookUrl = await urlLocator.inputValue();
        
        console.log(`✅ Captured Webhook URL: ${webhookUrl}`);
        
        // Save Trigger
        await page.getByText('Save Trigger').click();
        
        // Publish and Save
        console.log("Publishing...");
        await page.locator('.workflow-status-toggle').click(); // Toggle Draft -> Publish
        await page.getByText('Save').last().click();
        
        // Write to file
        fs.writeFileSync(OUTPUT_FILE, JSON.stringify({ webhookUrl }, null, 2));
        console.log("Saved URL to file.");

    } catch (e) {
        console.error("Automation failed:", e);
        // Take screenshot
        await page.screenshot({ path: 'ghl-error.png' });
    } finally {
        await browser.close();
    }
}

main();