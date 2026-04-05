/**
 * WF-02 Retry Loop Builder
 * Builds the 6-attempt contact sequence in GHL workflow editor
 * Uses saved auth state - no login required
 */

import { chromium, Page, Frame } from 'playwright';
import * as path from 'path';

const AUTH_STATE = path.join(__dirname, '../.ghl-auth-state.json');
const WF02_URL = 'https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/workflow/43ecd109-6595-4f51-a0e0-e2421b3f8131';
const VAPI_ASSISTANT_ID = 'your-vapi-assistant-id'; // Will use webhook action

async function wait(ms: number) {
  return new Promise(r => setTimeout(r, ms));
}

async function getWorkflowFrame(page: Page): Promise<Frame | null> {
  await wait(3000);
  const frames = page.frames();
  return frames.find(f => f.url().includes('automation') || f.url().includes('workflow')) || null;
}

async function clickAdd(page: Page, frameOrPage: Page | Frame) {
  // Click the + button to add new action
  await (frameOrPage as any).click('button:has-text("Add"), [data-testid="add-action"], .add-action-btn', { timeout: 5000 }).catch(() => {});
}

async function main() {
  console.log('🚀 Opening WF-02 in browser...');

  const browser = await chromium.launch({ headless: false, slowMo: 500 });
  const context = await browser.newContext({
    storageState: AUTH_STATE,
    viewport: { width: 1440, height: 900 }
  });
  const page = await context.newPage();

  try {
    console.log('📂 Navigating to WF-02...');
    await page.goto(WF02_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await wait(8000);

    console.log('📸 Taking screenshot of current WF-02 state...');
    await page.screenshot({ path: '/tmp/wf02-current.png', fullPage: true });
    console.log('Screenshot saved: /tmp/wf02-current.png');

    // Check what's currently in the workflow
    const title = await page.title();
    console.log('Page title:', title);

    const content = await page.content();
    const hasWorkflow = content.includes('WF-02') || content.includes('Contact Attempt');
    console.log('Workflow loaded:', hasWorkflow);

    // Look for existing actions
    const actionTexts = await page.$$eval('[class*="action"], [class*="step"], [class*="node"]',
      els => els.map(el => el.textContent?.trim().substring(0, 50)).filter(Boolean)
    ).catch(() => []);
    console.log('Existing actions found:', actionTexts.slice(0, 10));

    await wait(5000);
    await page.screenshot({ path: '/tmp/wf02-loaded.png', fullPage: false });
    console.log('✅ WF-02 loaded. Screenshots saved to /tmp/');
    console.log('Current URL:', page.url());

  } catch (err) {
    console.error('Error:', err);
    await page.screenshot({ path: '/tmp/wf02-error.png' });
  } finally {
    await wait(3000);
    await browser.close();
  }
}

main();
