import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const AUTH_FILE = path.join(__dirname, '../../.ghl-auth-state.json');
const OUTPUT_FILE = path.join(__dirname, '../../.ghl_webhook_url.json');

async function main() {
    console.log("Launching Local Playwright (Attempt 3: Bypass SPA routing)...");

    if (!fs.existsSync(AUTH_FILE)) {
        console.error("No auth state found.");
        process.exit(1);
    }

    const browser = await chromium.launch({ headless: false }); 
    const context = await browser.newContext({ storageState: AUTH_FILE });
    const page = await context.newPage();

    try {
        console.log("Navigating directly to workflow builder URL...");
        // Instead of trying to click "Create Workflow" which might be hidden behind a loading state or different DOM,
        // Let's try to navigate to the specific location's workflow list and wait for the table or empty state.
        await page.goto('https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows');
        
        console.log("Waiting for network idle...");
        await page.waitForLoadState('networkidle', { timeout: 60000 });

        console.log("Looking for Create button...");
        // GHL often changes button text slightly or uses different classes.
        // Let's look for common variations.
        const createBtn = page.locator('button:has-text("Create workflow")').first();
        await createBtn.waitFor({ state: 'visible', timeout: 30000 });
        await createBtn.click();

        console.log("Handling modal...");
        await page.locator('text=Start from scratch').click({ timeout: 10000 });
        await page.locator('button:has-text("Continue")').click();

        console.log("Waiting for editor to load...");
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(5000); // Give the canvas time to render

        console.log("Renaming...");
        await page.locator('.workflow-name').click();
        await page.locator('.workflow-name input').fill('WF-04B — Vapi Return Handler');
        await page.keyboard.press('Enter');

        console.log("Adding Trigger...");
        await page.locator('text=Add New Trigger').click();
        await page.locator('input[placeholder="Search"]').fill('Inbound Webhook');
        await page.waitForTimeout(1000);
        await page.locator('text=Inbound Webhook').first().click();

        console.log("Extracting URL...");
        await page.waitForTimeout(3000); // Wait for generation
        
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
        await page.locator('button:has-text("Save Trigger")').click();
        
        console.log("Publishing...");
        await page.locator('.workflow-status-toggle').click();
        await page.locator('button:has-text("Save")').last().click();
        console.log("Saved.");

    } catch (e) {
        console.error("Automation failed:", e);
        await page.screenshot({ path: 'ghl-retry3-error.png' });
    } finally {
        await browser.close();
    }
}

main();