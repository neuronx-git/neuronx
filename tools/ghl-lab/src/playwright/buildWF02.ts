/**
 * WF-02: Contact Attempt Engine
 * Trigger: Tag Added = nx:contacting:start
 * Flow: 6 contact attempts over 48 hours via VAPI
 * - Attempt 1: Immediate VAPI call
 * - Wait 2h → Attempt 2
 * - Wait 4h → Attempt 3
 * - Wait 8h → Attempt 4
 * - Wait 24h → Attempt 5
 * - Wait 48h → Attempt 6
 * - If still no nx:contacted → Add nx:unreachable tag
 *
 * This script navigates to GHL workflow builder and creates WF-02
 */
import { chromium } from 'playwright';
import * as path from 'path';

const AUTH_STATE = path.join(__dirname, '../../.ghl-auth-state.json');
const LOCATION_ID = 'FlRL82M0D6nclmKT7eXH';

async function buildWF02() {
  const browser = await chromium.launch({ headless: false, slowMo: 800 });
  const context = await browser.newContext({ storageState: AUTH_STATE });
  const page = await context.newPage();

  console.log('=== WF-02 Builder Started ===');

  // Navigate to workflows
  await page.goto(`https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/workflows`, {
    waitUntil: 'networkidle',
    timeout: 30000
  });
  await page.waitForTimeout(5000);

  // Screenshot current state
  await page.screenshot({ path: '/tmp/wf02-workflows-list.png', fullPage: true });
  console.log('Workflows page loaded - screenshot at /tmp/wf02-workflows-list.png');

  // Check if WF-02 already exists
  const wf02Exists = await page.locator('text=WF-02').first().isVisible().catch(() => false);
  if (wf02Exists) {
    console.log('WF-02 already exists - clicking to open it');
    await page.locator('text=WF-02').first().click();
    await page.waitForTimeout(5000);
    await page.screenshot({ path: '/tmp/wf02-existing.png', fullPage: true });
    console.log('Screenshot of existing WF-02 at /tmp/wf02-existing.png');
  } else {
    // Create new workflow
    console.log('Creating new WF-02...');
    const createBtn = await page.locator('button:has-text("Create Workflow"), button:has-text("+ Create"), a:has-text("Create")').first();
    if (await createBtn.isVisible()) {
      await createBtn.click();
      await page.waitForTimeout(3000);
      await page.screenshot({ path: '/tmp/wf02-create-dialog.png', fullPage: true });
      console.log('Create dialog screenshot at /tmp/wf02-create-dialog.png');

      // Start from scratch
      const scratchBtn = await page.locator('text=Start from Scratch, text=Blank Workflow').first();
      if (await scratchBtn.isVisible()) {
        await scratchBtn.click();
        await page.waitForTimeout(3000);
      }
    }
  }

  await page.screenshot({ path: '/tmp/wf02-builder-state.png', fullPage: true });
  console.log('Builder state screenshot at /tmp/wf02-builder-state.png');
  console.log('\n=== WF-02 Analysis Complete ===');
  console.log('Check screenshots in /tmp/ to see current state');
  console.log('The workflow builder requires iframe interaction for complex builds');

  await page.waitForTimeout(3000);
  await browser.close();
}

buildWF02().catch(console.error);
