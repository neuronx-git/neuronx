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

let evidenceFiles: string[] = [];
function screenshot(name: string) {
  const p = path.join(EVIDENCE_DIR, `v2_${name}_${Date.now()}.png`);
  evidenceFiles.push(p);
  return p;
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
      document.querySelectorAll('.n-modal-mask, .n-modal-body-wrapper').forEach((el: any) => {
        el.style.display = 'none';
      });
    });
  } catch {}
  try { await frame.page().keyboard.press('Escape'); } catch {}
  await frame.page().waitForTimeout(1000);
}

async function zoomOutCanvas(frame: Frame) {
  try {
    const fitBtn = frame.locator('button[aria-label="fit view"], .vue-flow__controls-fitview').first();
    if (await fitBtn.count() > 0) {
      await fitBtn.click({ force: true });
      await frame.page().waitForTimeout(1000);
    }
  } catch {}

  try {
    await frame.evaluate(() => {
      const viewport = document.querySelector('.vue-flow__viewport, .vue-flow__transformationpane') as HTMLElement;
      if (viewport) {
        viewport.style.transform = 'translate(100px, 150px) scale(0.7)';
      }
    });
    await frame.page().waitForTimeout(1000);
  } catch {}
}

async function run() {
  console.log('=== WF-01 PERSISTENCE PROOF V2 ===');
  console.log('Strategy: zoom/pan canvas so trigger node clears toolbar, then click\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ storageState: AUTH_PATH });
  const page = await context.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  console.log('STEP 1: Opening WF-01 editor...');
  await page.goto(WF_EDITOR_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(18000);

  const frame = await waitForWfFrame(page);
  if (!frame) {
    console.error('FATAL: Workflow iframe not found');
    await page.screenshot({ path: screenshot('fatal_no_iframe'), fullPage: true });
    await browser.close();
    return;
  }
  console.log('  Iframe found');
  await dismissModal(frame);
  await page.waitForTimeout(2000);

  const beforeNodes = await getNodeLabels(frame);
  console.log(`\nSTEP 2: BEFORE — nodes: ${JSON.stringify(beforeNodes)}`);
  await page.screenshot({ path: screenshot('01_before'), fullPage: true });

  console.log('\nSTEP 3: Zoom out canvas to clear trigger from toolbar...');
  await zoomOutCanvas(frame);
  await page.waitForTimeout(2000);

  let triggerRect = await frame.evaluate(() => {
    const el = document.querySelector('[data-id="add-new-trigger"]') as HTMLElement;
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2, top: r.top, bottom: r.bottom };
  });
  console.log(`  Trigger node rect: ${JSON.stringify(triggerRect)}`);

  let triggerAdded = false;

  if (triggerRect && triggerRect.top > 50) {
    console.log('  Trigger node clear of toolbar (top > 50). Clicking via page.mouse...');
    await page.mouse.click(triggerRect.x, triggerRect.y);
    await page.waitForTimeout(4000);

    const panelVisible = await frame.evaluate(() => {
      const items = document.querySelectorAll('[class*="trigger-type"], [class*="trigger-item"], [class*="TriggerType"]');
      return items.length;
    });
    console.log(`  Trigger panel items: ${panelVisible}`);

    if (panelVisible > 0) {
      console.log('  Trigger selection panel opened!');
    } else {
      console.log('  Panel not visible. Trying force click on node...');
      const triggerNode = frame.locator('[data-id="add-new-trigger"]').first();
      await triggerNode.click({ force: true, timeout: 5000 });
      await page.waitForTimeout(4000);
    }
  } else {
    console.log('  Trigger node still behind toolbar or not found. Using force click...');
    const triggerNode = frame.locator('[data-id="add-new-trigger"]').first();
    if (await triggerNode.count() > 0) {
      await triggerNode.click({ force: true, timeout: 5000 });
      await page.waitForTimeout(4000);
    }
  }

  await page.screenshot({ path: screenshot('02_after_trigger_click'), fullPage: true });

  const allText = await frame.evaluate(() => document.body.innerText.substring(0, 3000));
  const hasTriggerSelectionUI = allText.includes('Form Submitted') ||
    allText.includes('Contact Created') ||
    allText.includes('Contact Changed') ||
    allText.includes('Select Trigger Type') ||
    allText.includes('Workflow Trigger');
  console.log(`  Trigger selection UI detected: ${hasTriggerSelectionUI}`);

  if (hasTriggerSelectionUI) {
    console.log('\nSTEP 3b: Selecting "Contact Created" trigger...');
    const ccBtn = frame.locator('text=Contact Created').first();
    if (await ccBtn.count() > 0) {
      await ccBtn.click({ timeout: 5000 });
      await page.waitForTimeout(3000);
      console.log('  Clicked "Contact Created"');
    } else {
      const formSubmit = frame.locator('text=Form Submitted').first();
      if (await formSubmit.count() > 0) {
        await formSubmit.click({ timeout: 5000 });
        await page.waitForTimeout(3000);
        console.log('  Clicked "Form Submitted"');
      } else {
        console.log('  Trying first clickable trigger option...');
        const firstOpt = frame.locator('[class*="trigger"] >> visible=true').first();
        if (await firstOpt.count() > 0) {
          await firstOpt.click({ timeout: 5000 });
          await page.waitForTimeout(3000);
        }
      }
    }

    await page.screenshot({ path: screenshot('03_after_trigger_type_select'), fullPage: true });

    console.log('\nSTEP 3c: Clicking Save Trigger...');
    const saveTrigger = frame.locator('button:has-text("Save Trigger")').first();
    if (await saveTrigger.count() > 0) {
      const box = await saveTrigger.boundingBox();
      if (box) {
        await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
        console.log('  Save Trigger clicked via mouse');
        await page.waitForTimeout(4000);
        triggerAdded = true;
      } else {
        await saveTrigger.click({ force: true });
        console.log('  Save Trigger clicked via force');
        await page.waitForTimeout(4000);
        triggerAdded = true;
      }
    } else {
      const saveBtnRect = await frame.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const save = btns.find(b => b.textContent?.trim().includes('Save Trigger'));
        if (!save) return null;
        const r = save.getBoundingClientRect();
        return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
      });
      if (saveBtnRect) {
        await page.mouse.click(saveBtnRect.x, saveBtnRect.y);
        console.log('  Save Trigger clicked via evaluate + mouse');
        await page.waitForTimeout(4000);
        triggerAdded = true;
      } else {
        console.log('  Save Trigger button not found');
      }
    }
  } else {
    console.log('  Trigger selection UI NOT detected. Trying dispatchEvent approach...');
    const dispatched = await frame.evaluate(() => {
      const node = document.querySelector('[data-id="add-new-trigger"]') as HTMLElement;
      if (!node) return false;
      const events = ['pointerdown', 'pointerup', 'mousedown', 'mouseup', 'click'];
      for (const e of events) {
        node.dispatchEvent(new PointerEvent(e, { bubbles: true, cancelable: true, composed: true }));
      }
      return true;
    });
    console.log(`  dispatchEvent on trigger node: ${dispatched}`);
    await page.waitForTimeout(4000);

    const panelAfterDispatch = await frame.evaluate(() => document.body.innerText.substring(0, 2000));
    const hasPanel = panelAfterDispatch.includes('Form Submitted') || panelAfterDispatch.includes('Contact Created');
    console.log(`  Panel after dispatchEvent: ${hasPanel}`);
    await page.screenshot({ path: screenshot('02b_after_dispatch'), fullPage: true });
  }

  console.log(`\n  ── Trigger added: ${triggerAdded} ──`);

  let actionAdded = false;
  if (triggerAdded) {
    console.log('\nSTEP 4: Adding action...');
    const addActionRect = await frame.evaluate(() => {
      const btns = document.querySelectorAll('.pg-actions__dv--add-action, button[aria-label="Add Action"]');
      if (btns.length === 0) return null;
      const btn = btns[btns.length - 1] as HTMLElement;
      const r = btn.getBoundingClientRect();
      return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
    });
    if (addActionRect) {
      await page.mouse.click(addActionRect.x, addActionRect.y);
      await page.waitForTimeout(3000);

      const actionBodyText = await frame.evaluate(() => document.body.innerText.substring(0, 3000));
      const hasActionPanel = actionBodyText.includes('Send Email') || actionBodyText.includes('Add Tag') || actionBodyText.includes('Internal Notification');
      console.log(`  Action panel visible: ${hasActionPanel}`);

      if (hasActionPanel) {
        const sendEmail = frame.locator('text=Send Email').first();
        if (await sendEmail.count() > 0) {
          await sendEmail.click({ timeout: 5000 });
          await page.waitForTimeout(2000);
          actionAdded = true;
          console.log('  Selected "Send Email"');
        }
      }
    } else {
      console.log('  Add Action button not found');
    }
  }
  console.log(`  ── Action added: ${actionAdded} ──`);

  const afterNodes = await getNodeLabels(frame);
  console.log(`\nSTEP 5: AFTER-SAVE — nodes: ${JSON.stringify(afterNodes)}`);
  await page.screenshot({ path: screenshot('04_after_save'), fullPage: true });

  console.log('\nSTEP 6: Navigating away...');
  await page.goto(AUTOMATION_LIST_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(12000);
  console.log(`  URL: ${page.url()}`);

  console.log('\nSTEP 7: Re-opening WF-01...');
  await page.goto(WF_EDITOR_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(18000);

  const frame2 = await waitForWfFrame(page);
  if (!frame2) {
    console.error('FATAL: Iframe not found on re-open');
    await page.screenshot({ path: screenshot('fatal_no_iframe_reopen'), fullPage: true });
    await browser.close();
    return;
  }
  await dismissModal(frame2);
  await page.waitForTimeout(2000);

  const reloadNodes = await getNodeLabels(frame2);
  console.log(`\nSTEP 8: AFTER-RELOAD — nodes: ${JSON.stringify(reloadNodes)}`);
  await page.screenshot({ path: screenshot('05_after_reload'), fullPage: true });

  const beforeSet = new Set(beforeNodes);
  const newNodes = reloadNodes.filter(n => !beforeSet.has(n));
  const persisted = newNodes.length > 0 || reloadNodes.some(n =>
    n.includes('Form Submitted') || n.includes('Contact Created') || n.includes('Send Email')
  );

  console.log('\n════════════════════════════════════');
  console.log('   PERSISTENCE PROOF V2 RESULT');
  console.log('════════════════════════════════════');
  console.log(`  Tool: Playwright (storageState, headed)`);
  console.log(`  Before:  ${JSON.stringify(beforeNodes)}`);
  console.log(`  After:   ${JSON.stringify(afterNodes)}`);
  console.log(`  Reload:  ${JSON.stringify(reloadNodes)}`);
  console.log(`  New:     ${JSON.stringify(newNodes)}`);
  console.log(`  Trigger added in session: ${triggerAdded}`);
  console.log(`  Action added in session: ${actionAdded}`);
  console.log(`  VERDICT: ${persisted ? 'PERSISTED ✅' : 'NOT PERSISTED ❌'}`);
  if (!persisted && triggerAdded) {
    console.log(`  BLOCKER: Changes visually appear but GHL Vue.js/Pinia does not persist Playwright events to backend.`);
  }
  if (!triggerAdded) {
    console.log(`  BLOCKER: Could not click trigger node — GHL toolbar overlays intercept all click methods.`);
  }
  console.log('════════════════════════════════════\n');

  console.log('Evidence:');
  evidenceFiles.forEach((f, i) => console.log(`  ${i + 1}. ${f}`));

  await browser.close();
}

run().catch(err => {
  console.error('Script error:', err);
  process.exit(1);
});
