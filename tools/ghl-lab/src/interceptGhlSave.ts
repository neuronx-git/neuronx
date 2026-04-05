import { chromium, type Page, type Frame } from 'playwright';
import * as path from 'path';
import * as fs from 'fs';

const LOCATION_ID = 'FlRL82M0D6nclmKT7eXH';
const WF01_ID = '99ce0aa7-2491-4c91-9477-22969798e2b7';
const AUTH_PATH = path.join(__dirname, '..', '.ghl-auth-state.json');
const EVIDENCE_DIR = path.join(__dirname, '..', 'evidence');
const WF_EDITOR_URL = `https://app.gohighlevel.com/location/${LOCATION_ID}/workflow/${WF01_ID}`;
const WF_IFRAME_HOST = 'client-app-automation-workflows.leadconnectorhq.com';

if (!fs.existsSync(EVIDENCE_DIR)) fs.mkdirSync(EVIDENCE_DIR, { recursive: true });

async function waitForWfFrame(page: Page, timeoutMs = 40000): Promise<Frame | null> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const frame = page.frames().find(f => f.url().includes(WF_IFRAME_HOST));
    if (frame) return frame;
    await page.waitForTimeout(2000);
  }
  return null;
}

async function run() {
  console.log('=== INTERCEPT GHL SAVE REQUESTS ===');
  console.log('Goal: Discover what API call GHL makes when trigger/action is saved');
  console.log('Strategy: Listen to ALL network requests, add trigger via Playwright, log what goes to backend\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ storageState: AUTH_PATH });
  const page = await context.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  const capturedRequests: any[] = [];

  page.on('request', (req) => {
    const url = req.url();
    if (url.includes('leadconnectorhq.com') || url.includes('gohighlevel.com') || url.includes('msgsndr.com')) {
      const method = req.method();
      if (method === 'PUT' || method === 'POST' || method === 'PATCH') {
        const postData = req.postData();
        capturedRequests.push({
          method,
          url,
          postData: postData ? postData.substring(0, 2000) : null,
          time: new Date().toISOString(),
        });
        console.log(`  [NET] ${method} ${url.substring(0, 120)}`);
        if (postData) console.log(`    Body: ${postData.substring(0, 300)}`);
      }
    }
  });

  page.on('response', (resp) => {
    const url = resp.url();
    const status = resp.status();
    if ((url.includes('leadconnectorhq.com') || url.includes('gohighlevel.com') || url.includes('msgsndr.com')) &&
        (resp.request().method() === 'PUT' || resp.request().method() === 'POST' || resp.request().method() === 'PATCH')) {
      console.log(`  [RESP] ${status} ${resp.request().method()} ${url.substring(0, 120)}`);
    }
  });

  console.log('Opening WF-01 editor...');
  await page.goto(WF_EDITOR_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(15000);

  const frame = await waitForWfFrame(page);
  if (!frame) {
    console.error('FATAL: iframe not found');
    await browser.close();
    return;
  }

  for (let i = 0; i < 3; i++) {
    try { await page.keyboard.press('Escape'); } catch {}
    await page.waitForTimeout(500);
  }
  await page.waitForTimeout(3000);

  console.log('\n--- Pre-click captured requests ---');
  console.log(`Requests so far: ${capturedRequests.length}`);
  const preClickCount = capturedRequests.length;

  console.log('\nPanning canvas down to clear trigger from toolbar...');
  const vfPane = await frame.$('.vue-flow__pane');
  if (vfPane) {
    const box = await vfPane.boundingBox();
    if (box) {
      const cx = box.x + box.width / 2;
      const cy = box.y + box.height / 2;
      await page.mouse.move(cx, cy);
      await page.mouse.down();
      await page.mouse.move(cx, cy + 200, { steps: 10 });
      await page.mouse.up();
      await page.waitForTimeout(2000);
    }
  }

  const triggerRect = await frame.evaluate(() => {
    const el = document.querySelector('[data-id="add-new-trigger"]') as HTMLElement;
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2, top: r.top };
  });
  console.log(`Trigger rect after pan: ${JSON.stringify(triggerRect)}`);

  if (triggerRect && triggerRect.top > 60) {
    console.log('\nClicking trigger node...');
    await page.mouse.click(triggerRect.x, triggerRect.y);
    await page.waitForTimeout(5000);

    const bodyText = await frame.evaluate(() => document.body.innerText.substring(0, 2000));
    const hasPanel = bodyText.includes('Contact Created') || bodyText.includes('Form Submitted');
    console.log(`Trigger panel visible: ${hasPanel}`);

    if (hasPanel) {
      console.log('\nSelecting "Contact Created"...');
      const cc = frame.locator('text=Contact Created').first();
      if (await cc.count() > 0) {
        await cc.click({ timeout: 5000 });
        await page.waitForTimeout(3000);
      }

      console.log('Clicking "Save Trigger"...');
      const saveBtn = frame.locator('button:has-text("Save Trigger")').first();
      if (await saveBtn.count() > 0) {
        const box = await saveBtn.boundingBox();
        if (box) {
          console.log(`  Save button at (${box.x + box.width / 2}, ${box.y + box.height / 2})`);
          await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
          await page.waitForTimeout(5000);
        }
      }
    }
  }

  console.log('\n--- Post-click captured requests ---');
  const newRequests = capturedRequests.slice(preClickCount);
  console.log(`New requests after trigger attempt: ${newRequests.length}`);
  for (const req of newRequests) {
    console.log(`\n  ${req.method} ${req.url}`);
    if (req.postData) console.log(`  Body: ${req.postData.substring(0, 500)}`);
  }

  console.log('\n\nWaiting 10s for any delayed saves...');
  await page.waitForTimeout(10000);

  const laterRequests = capturedRequests.slice(preClickCount + newRequests.length);
  if (laterRequests.length > 0) {
    console.log(`\nDelayed requests: ${laterRequests.length}`);
    for (const req of laterRequests) {
      console.log(`  ${req.method} ${req.url}`);
      if (req.postData) console.log(`  Body: ${req.postData.substring(0, 500)}`);
    }
  } else {
    console.log('No delayed requests.');
  }

  console.log('\n\n=== ALL CAPTURED REQUESTS ===');
  for (const req of capturedRequests) {
    console.log(`${req.time} ${req.method} ${req.url.substring(0, 150)}`);
  }

  fs.writeFileSync(
    path.join(EVIDENCE_DIR, 'captured_requests.json'),
    JSON.stringify(capturedRequests, null, 2)
  );
  console.log(`\nSaved to evidence/captured_requests.json`);

  await page.screenshot({ path: path.join(EVIDENCE_DIR, `intercept_final_${Date.now()}.png`), fullPage: true });
  await browser.close();
}

run().catch(err => {
  console.error('Script error:', err);
  process.exit(1);
});
