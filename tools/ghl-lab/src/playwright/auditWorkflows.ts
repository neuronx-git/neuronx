import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const AUTH_FILE = path.join(__dirname, '../../.ghl-auth-state.json');

async function main() {
    console.log("Launching Local Playwright to audit workflows...");

    if (!fs.existsSync(AUTH_FILE)) {
        console.error("No auth state found.");
        process.exit(1);
    }

    const browser = await chromium.launch({ headless: false }); 
    const context = await browser.newContext({ storageState: AUTH_FILE });
    const page = await context.newPage();

    try {
        console.log("Navigating to workflows list...");
        await page.goto('https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/automation/workflows');
        
        // Wait for the table to load
        await page.waitForSelector('table', { timeout: 30000 });
        await page.waitForTimeout(5000); // Give JS time to render rows

        console.log("Extracting workflow names...");
        const workflows = await page.evaluate(() => {
            const rows = document.querySelectorAll('table tbody tr');
            const data: any[] = [];
            rows.forEach((row, index) => {
                // The name is usually in the second column
                const nameCell = row.querySelector('td:nth-child(2)');
                const statusCell = row.querySelector('td:nth-child(3)');
                const createdCell = row.querySelector('td:nth-child(7)');
                
                if (nameCell) {
                    data.push({
                        index,
                        name: nameCell.textContent?.trim() || 'Unknown',
                        status: statusCell?.textContent?.trim() || 'Unknown',
                        createdOn: createdCell?.textContent?.trim() || 'Unknown'
                    });
                }
            });
            return data;
        });

        console.log("Extracted Workflows:");
        console.log(JSON.stringify(workflows, null, 2));
        
        fs.writeFileSync(path.join(__dirname, '../../.ghl_workflows_audit.json'), JSON.stringify(workflows, null, 2));

    } catch (e) {
        console.error("Audit failed:", e);
    } finally {
        await browser.close();
    }
}

main();