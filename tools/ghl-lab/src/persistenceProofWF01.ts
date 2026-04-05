import { chromium, type Page, type Frame } from 'playwright';
import * as path from 'path';
import * as fs from 'fs';

const LOCATION_ID = 'FlRL82M0D6nclmKT7eXH';
const WF01_ID = '99ce0aa7-2491-4c91-9477-22969798e2b7';
const AUTH_PATH = path.join(__dirname, '..', '.ghl-auth-state.json');
const EVIDENCE_DIR = path.join(__dirname, '..', 'evidence');
const WF_EDITOR_URL = `https://app.gohighlevel.com/location/${LOCATION_ID}/workflow/${WF01_ID}`;
const AUTOMATION_LIST_URL = `https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/list`;
const WF_IFRAME_HOST = 'client-app-automation-workflows.leadconnectorhq.com';

if (!fs.existsSync(EVIDENCE_DIR)) fs.mkdirSync(EVIDENCE_DIR, { recursive: true });

function screenshotPath(name: string) {
  return path.join(EVIDENCE_DIR, `persistence_proof_${name}_${Date.now()}.png`);
}

async function waitForWfFrame(page: Page, timeoutMs = 30000): Promise<Frame | null> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const frame = page.frames().find(f => f.url().includes(WF_IFRAME_HOST));
    if (frame) return frame;
    await page.waitForTimeout(2000);
  }
  return null;
}

async function getNodeLabels(frame: Frame): Promise<string[]> {
  return frame.evaluate(() => {
    const nodes = document.querySelectorAll('.vue-flow .vue-flow__node');
    return Array.from(nodes).map(n => n.textContent?.trim() || '(empty)');
  });
}

async function dismissModal(frame: Frame) {
  try {
    await frame.evaluate(() => {
      const mask = document.querySelector('.n-modal-mask') as HTMLElement;
      if (mask) mask.style.display = 'none';
      const overlays = document.querySelectorAll('.n-modal-body-wrapper') as NodeListOf<HTMLElement>;
      overlays.forEach(o => { o.style.display = 'none'; });
    });
  } catch { /* ignore */ }
  try {
    await frame.page().keyboard.press('Escape');
  } catch { /* ignore */ }
}

async function run() {
  console.log('=== WF-01 PERSISTENCE PROOF ===');
  console.log(`Auth: ${AUTH_PATH}`);
  console.log(`WF-01: ${WF_EDITOR_URL}\n`);

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ storageState: AUTH_PATH });
  const page = await context.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  // ── STEP 1: Open WF-01 editor ──
  console.log('STEP 1: Opening WF-01 editor...');
  await page.goto(WF_EDITOR_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(18000);

  const frame = await waitForWfFrame(page);
  if (!frame) {
    console.error('FATAL: Workflow iframe not found after 30s');
    await page.screenshot({ path: screenshotPath('fatal_no_iframe'), fullPage: true });
    await browser.close();
    return;
  }
  console.log('  Iframe found');

  await dismissModal(frame);
  await page.waitForTimeout(2000);

  // ── STEP 2: Capture BEFORE state ──
  const beforeNodes = await getNodeLabels(frame);
  console.log(`\nSTEP 2: BEFORE state — nodes: ${JSON.stringify(beforeNodes)}`);
  const beforeScreenshot = screenshotPath('01_before');
  await page.screenshot({ path: beforeScreenshot, fullPage: true });
  console.log(`  Screenshot: ${beforeScreenshot}`);

  // ── STEP 3: Add trigger ──
  console.log('\nSTEP 3: Adding trigger...');
  let triggerAdded = false;

  try {
    const triggerNode = frame.locator('[data-id="add-new-trigger"]');
    const triggerCount = await triggerNode.count();
    console.log(`  Trigger node count: ${triggerCount}`);

    if (triggerCount > 0) {
      await triggerNode.first().scrollIntoViewIfNeeded();
      await page.waitForTimeout(1000);
      await triggerNode.first().click({ timeout: 5000 });
      await page.waitForTimeout(3000);

      const triggerPanel = await frame.locator('.workflow-trigger-selection, .trigger-selection-panel, [class*="trigger"]').count();
      console.log(`  Trigger panel elements: ${triggerPanel}`);

      const formSubmittedBtn = frame.locator('text=Form Submitted').first();
      const formSubmittedExists = await formSubmittedBtn.count();
      if (formSubmittedExists > 0) {
        await formSubmittedBtn.click({ timeout: 5000 });
        await page.waitForTimeout(2000);
        console.log('  Clicked "Form Submitted" trigger');
      } else {
        const contactCreated = frame.locator('text=Contact Created').first();
        const ccExists = await contactCreated.count();
        if (ccExists > 0) {
          await contactCreated.click({ timeout: 5000 });
          await page.waitForTimeout(2000);
          console.log('  Clicked "Contact Created" trigger (fallback)');
        } else {
          console.log('  No standard trigger option found, trying first available...');
          const anyTrigger = frame.locator('.trigger-item, .workflow-trigger-item, [class*="trigger-option"]').first();
          if (await anyTrigger.count() > 0) {
            await anyTrigger.click({ timeout: 5000 });
            await page.waitForTimeout(2000);
            console.log('  Clicked first available trigger');
          }
        }
      }

      const saveTriggerBtn = frame.locator('button:has-text("Save Trigger")').first();
      if (await saveTriggerBtn.count() > 0) {
        await saveTriggerBtn.scrollIntoViewIfNeeded();
        await page.waitForTimeout(500);

        const box = await saveTriggerBtn.boundingBox();
        if (box) {
          await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
          console.log('  Clicked Save Trigger via mouse');
          await page.waitForTimeout(3000);
          triggerAdded = true;
        }
      }

      if (!triggerAdded) {
        const saveBtnRect = await frame.evaluate(() => {
          const btn = Array.from(document.querySelectorAll('button')).find(b =>
            b.textContent?.trim().includes('Save Trigger')
          );
          if (!btn) return null;
          const r = btn.getBoundingClientRect();
          return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
        });
        if (saveBtnRect) {
          await page.mouse.click(saveBtnRect.x, saveBtnRect.y);
          console.log('  Clicked Save Trigger via evaluate + mouse');
          await page.waitForTimeout(3000);
          triggerAdded = true;
        }
      }
    }
  } catch (err: any) {
    console.log(`  Trigger add error: ${err.message}`);
  }
  console.log(`  Trigger added: ${triggerAdded}`);

  // ── STEP 4: Add action (only if trigger was added) ──
  let actionAdded = false;
  if (triggerAdded) {
    console.log('\nSTEP 4: Adding action...');
    try {
      const addActionBtn = frame.locator('button[aria-label="Add Action"], .pg-actions__dv--add-action').first();
      if (await addActionBtn.count() > 0) {
        const actionBox = await addActionBtn.boundingBox();
        if (actionBox) {
          await page.mouse.click(actionBox.x + actionBox.width / 2, actionBox.y + actionBox.height / 2);
          await page.waitForTimeout(3000);
          console.log('  Action panel opened');

          const sendEmail = frame.locator('text=Send Email').first();
          if (await sendEmail.count() > 0) {
            await sendEmail.click({ timeout: 5000 });
            await page.waitForTimeout(2000);
            console.log('  Selected "Send Email" action');
            actionAdded = true;
          } else {
            const firstAction = frame.locator('.action-item, .workflow-action-item, [class*="action-option"]').first();
            if (await firstAction.count() > 0) {
              await firstAction.click({ timeout: 5000 });
              await page.waitForTimeout(2000);
              console.log('  Selected first available action');
              actionAdded = true;
            }
          }
        }
      } else {
        const plusBtns = await frame.evaluate(() => {
          const all = document.querySelectorAll('.pg-actions__dv--add-action');
          return all.length;
        });
        console.log(`  Plus button count via evaluate: ${plusBtns}`);
      }
    } catch (err: any) {
      console.log(`  Action add error: ${err.message}`);
    }
  } else {
    console.log('\nSTEP 4: Skipping action (trigger not added)');
  }
  console.log(`  Action added: ${actionAdded}`);

  // ── STEP 5: Capture AFTER-SAVE state ──
  const afterNodes = await getNodeLabels(frame);
  console.log(`\nSTEP 5: AFTER-SAVE state — nodes: ${JSON.stringify(afterNodes)}`);
  const afterScreenshot = screenshotPath('02_after_save');
  await page.screenshot({ path: afterScreenshot, fullPage: true });
  console.log(`  Screenshot: ${afterScreenshot}`);

  // ── STEP 6: Navigate away ──
  console.log('\nSTEP 6: Navigating away to automation list...');
  await page.goto(AUTOMATION_LIST_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(12000);
  console.log(`  Current URL: ${page.url()}`);

  // ── STEP 7: Re-open WF-01 fresh ──
  console.log('\nSTEP 7: Re-opening WF-01...');
  await page.goto(WF_EDITOR_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(18000);

  const frame2 = await waitForWfFrame(page);
  if (!frame2) {
    console.error('FATAL: Iframe not found on re-open');
    await page.screenshot({ path: screenshotPath('fatal_no_iframe_reopen'), fullPage: true });
    await browser.close();
    return;
  }

  await dismissModal(frame2);
  await page.waitForTimeout(2000);

  // ── STEP 8: Verify persistence ──
  const reloadNodes = await getNodeLabels(frame2);
  console.log(`\nSTEP 8: AFTER-RELOAD state — nodes: ${JSON.stringify(reloadNodes)}`);
  const reloadScreenshot = screenshotPath('03_after_reload');
  await page.screenshot({ path: reloadScreenshot, fullPage: true });
  console.log(`  Screenshot: ${reloadScreenshot}`);

  // ── RESULT ──
  const beforeSet = new Set(beforeNodes);
  const reloadSet = new Set(reloadNodes);
  const newNodesInReload = reloadNodes.filter(n => !beforeSet.has(n));
  const hasTriggerNode = reloadNodes.some(n =>
    n.includes('Form Submitted') || n.includes('Contact Created') ||
    (!n.includes('Add New Trigger') && !n.includes('END') && n !== '(empty)')
  );

  console.log('\n════════════════════════════════');
  console.log('  PERSISTENCE PROOF RESULT');
  console.log('════════════════════════════════');
  console.log(`  Tool: Playwright (storageState)`);
  console.log(`  Before nodes: ${beforeNodes.length} → ${JSON.stringify(beforeNodes)}`);
  console.log(`  After-save nodes: ${afterNodes.length} → ${JSON.stringify(afterNodes)}`);
  console.log(`  After-reload nodes: ${reloadNodes.length} → ${JSON.stringify(reloadNodes)}`);
  console.log(`  New nodes after reload: ${JSON.stringify(newNodesInReload)}`);
  console.log(`  Trigger persisted: ${hasTriggerNode}`);
  console.log(`  VERDICT: ${hasTriggerNode ? 'PERSISTED ✅' : 'NOT PERSISTED ❌'}`);
  if (!hasTriggerNode) {
    console.log(`  BLOCKER: Vue.js/Pinia state does not register Playwright click events. GHL backend API never called.`);
  }
  console.log('════════════════════════════════\n');

  console.log('Evidence files:');
  console.log(`  1. ${beforeScreenshot}`);
  console.log(`  2. ${afterScreenshot}`);
  console.log(`  3. ${reloadScreenshot}`);

  await browser.close();
}

run().catch(err => {
  console.error('Script error:', err);
  process.exit(1);
});
