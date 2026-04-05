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
function ss(name: string) {
  const p = path.join(EVIDENCE_DIR, `v3_${name}_${Date.now()}.png`);
  evidenceFiles.push(p);
  return p;
}

async function waitForWfFrame(page: Page, timeoutMs = 40000): Promise<Frame | null> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const frame = page.frames().find(f => f.url().includes(WF_IFRAME_HOST));
    if (frame) return frame;
    await page.waitForTimeout(2000);
  }
  return null;
}

async function waitForVueFlowNodes(frame: Frame, timeoutMs = 25000): Promise<string[]> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const nodes = await frame.evaluate(() => {
      const els = document.querySelectorAll('.vue-flow .vue-flow__node');
      return Array.from(els).map(n => n.textContent?.trim() || '');
    });
    if (nodes.length > 0) return nodes;
    await frame.page().waitForTimeout(2000);
  }
  return [];
}

async function dismissModal(frame: Frame) {
  for (let i = 0; i < 3; i++) {
    try {
      await frame.evaluate(() => {
        document.querySelectorAll('.n-modal-mask, .n-modal-body-wrapper, .n-modal-container').forEach((el: any) => {
          el.style.display = 'none';
          el.remove();
        });
      });
    } catch {}
    try { await frame.page().keyboard.press('Escape'); } catch {}
    await frame.page().waitForTimeout(500);
  }
}

async function dumpDomInfo(frame: Frame, label: string) {
  const info = await frame.evaluate(() => {
    const vueFlowEl = document.querySelector('.vue-flow');
    const nodes = document.querySelectorAll('.vue-flow .vue-flow__node');
    const triggerNode = document.querySelector('[data-id="add-new-trigger"]');
    const allDataIds = Array.from(document.querySelectorAll('[data-id]')).map(el => ({
      dataId: el.getAttribute('data-id'),
      tag: el.tagName,
      classes: el.className.toString().substring(0, 80),
      text: el.textContent?.trim().substring(0, 40),
    }));
    const viewportEl = document.querySelector('.vue-flow__viewport, .vue-flow__transformationpane');
    const viewportTransform = viewportEl ? (viewportEl as HTMLElement).style.transform : 'N/A';

    return {
      hasVueFlow: !!vueFlowEl,
      nodeCount: nodes.length,
      nodeLabels: Array.from(nodes).map(n => n.textContent?.trim()),
      hasTriggerNode: !!triggerNode,
      triggerNodeRect: triggerNode ? (() => {
        const r = triggerNode.getBoundingClientRect();
        return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top) };
      })() : null,
      dataIdElements: allDataIds.slice(0, 20),
      viewportTransform,
    };
  });
  console.log(`\n  [${label}] DOM dump:`);
  console.log(`    vue-flow exists: ${info.hasVueFlow}`);
  console.log(`    nodes: ${info.nodeCount} → ${JSON.stringify(info.nodeLabels)}`);
  console.log(`    trigger node exists: ${info.hasTriggerNode}`);
  console.log(`    trigger rect: ${JSON.stringify(info.triggerNodeRect)}`);
  console.log(`    viewport transform: ${info.viewportTransform}`);
  console.log(`    data-id elements: ${JSON.stringify(info.dataIdElements.map(d => d.dataId))}`);
  return info;
}

async function run() {
  console.log('=== WF-01 PERSISTENCE PROOF V3 ===');
  console.log('Strategy: wait for vue-flow nodes, dump DOM, try multiple click approaches\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ storageState: AUTH_PATH });
  const page = await context.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  console.log('STEP 1: Opening WF-01 editor...');
  await page.goto(WF_EDITOR_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(15000);

  const frame = await waitForWfFrame(page);
  if (!frame) {
    console.error('FATAL: Workflow iframe not found');
    await page.screenshot({ path: ss('fatal'), fullPage: true });
    await browser.close();
    return;
  }
  console.log('  Iframe found. Waiting for vue-flow nodes...');

  await dismissModal(frame);
  await page.waitForTimeout(3000);

  const beforeNodes = await waitForVueFlowNodes(frame);
  console.log(`\nSTEP 2: BEFORE — nodes: ${JSON.stringify(beforeNodes)}`);
  await page.screenshot({ path: ss('01_before'), fullPage: true });

  const domInfo = await dumpDomInfo(frame, 'BEFORE');

  if (!domInfo.hasTriggerNode) {
    console.log('\n  Trigger node [data-id="add-new-trigger"] NOT in DOM.');
    console.log('  Checking if it exists under different selector...');

    const altSearch = await frame.evaluate(() => {
      const allNodes = document.querySelectorAll('.vue-flow__node');
      return Array.from(allNodes).map(n => ({
        id: n.getAttribute('data-id'),
        classes: n.className.toString(),
        text: n.textContent?.trim().substring(0, 60),
        rect: (() => {
          const r = n.getBoundingClientRect();
          return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) };
        })(),
      }));
    });
    console.log(`  All vue-flow__node elements: ${JSON.stringify(altSearch, null, 2)}`);
  }

  console.log('\nSTEP 3: Attempting to click trigger node...');
  let triggerAdded = false;

  if (domInfo.hasTriggerNode && domInfo.triggerNodeRect) {
    const rect = domInfo.triggerNodeRect;
    console.log(`  Trigger at (${rect.x}, ${rect.y}), top=${rect.top}`);

    if (rect.top < 60) {
      console.log('  Trigger behind toolbar. Panning canvas down 200px...');
      const vfEl = await frame.$('.vue-flow__pane');
      if (vfEl) {
        const vfBox = await vfEl.boundingBox();
        if (vfBox) {
          const cx = vfBox.x + vfBox.width / 2;
          const cy = vfBox.y + vfBox.height / 2;
          await page.mouse.move(cx, cy);
          await page.mouse.down();
          await page.mouse.move(cx, cy + 200, { steps: 10 });
          await page.mouse.up();
          await page.waitForTimeout(2000);

          const newRect = await frame.evaluate(() => {
            const el = document.querySelector('[data-id="add-new-trigger"]');
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return { x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2), top: Math.round(r.top) };
          });
          console.log(`  After pan — trigger rect: ${JSON.stringify(newRect)}`);
          if (newRect && newRect.top > 60) {
            await page.mouse.click(newRect.x, newRect.y);
            console.log('  Clicked trigger via page.mouse after pan');
            await page.waitForTimeout(4000);
          }
        }
      }
    } else {
      await page.mouse.click(rect.x + rect.w! / 2 || rect.x, rect.y + rect.h! / 2 || rect.y);
      console.log('  Clicked trigger via page.mouse (clear of toolbar)');
      await page.waitForTimeout(4000);
    }

    const bodyText = await frame.evaluate(() => document.body.innerText.substring(0, 2000));
    const hasPanel = bodyText.includes('Form Submitted') || bodyText.includes('Contact Created') || bodyText.includes('Workflow Trigger');
    console.log(`  Trigger panel visible: ${hasPanel}`);

    if (!hasPanel) {
      console.log('  Trying force click...');
      try {
        const trigLoc = frame.locator('[data-id="add-new-trigger"]').first();
        await trigLoc.click({ force: true, timeout: 5000 });
        await page.waitForTimeout(4000);
        const bodyText2 = await frame.evaluate(() => document.body.innerText.substring(0, 2000));
        const hasPanel2 = bodyText2.includes('Form Submitted') || bodyText2.includes('Contact Created');
        console.log(`  Panel after force click: ${hasPanel2}`);
      } catch (e: any) {
        console.log(`  Force click error: ${e.message.substring(0, 100)}`);
      }
    }
  } else {
    console.log('  No trigger node found. Trying to find clickable trigger area...');
    const triggerByText = frame.locator('text=Add New Trigger').first();
    if (await triggerByText.count() > 0) {
      console.log('  Found "Add New Trigger" text element. Clicking...');
      await triggerByText.click({ force: true, timeout: 5000 });
      await page.waitForTimeout(4000);
    }
  }

  await page.screenshot({ path: ss('02_after_trigger_attempt'), fullPage: true });

  const bodyAfterClick = await frame.evaluate(() => document.body.innerText.substring(0, 3000));
  const triggerPanelOpen = bodyAfterClick.includes('Form Submitted') ||
    bodyAfterClick.includes('Contact Created') ||
    bodyAfterClick.includes('Contact Changed') ||
    bodyAfterClick.includes('Workflow Trigger') ||
    bodyAfterClick.includes('Select a trigger');

  if (triggerPanelOpen) {
    console.log('\n  Trigger panel IS open. Selecting trigger...');
    const triggers = ['Contact Created', 'Form Submitted', 'Contact Changed'];
    for (const t of triggers) {
      const btn = frame.locator(`text=${t}`).first();
      if (await btn.count() > 0) {
        await btn.click({ timeout: 5000 });
        console.log(`  Selected "${t}"`);
        await page.waitForTimeout(3000);
        break;
      }
    }

    await page.screenshot({ path: ss('03_trigger_selected'), fullPage: true });

    console.log('  Looking for Save Trigger button...');
    const saveBtn = frame.locator('button:has-text("Save Trigger")').first();
    if (await saveBtn.count() > 0) {
      const box = await saveBtn.boundingBox();
      if (box) {
        await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
        console.log('  Save Trigger clicked');
        await page.waitForTimeout(4000);
        triggerAdded = true;
      }
    }
  } else {
    console.log('\n  Trigger panel NOT open after all attempts.');
  }

  console.log(`\n  ═══ Trigger added: ${triggerAdded} ═══`);

  let actionAdded = false;
  if (triggerAdded) {
    console.log('\nSTEP 4: Adding action...');
    await page.waitForTimeout(2000);
    const actionBtnRect = await frame.evaluate(() => {
      const btns = document.querySelectorAll('.pg-actions__dv--add-action, button[aria-label="Add Action"]');
      for (const btn of Array.from(btns)) {
        const r = btn.getBoundingClientRect();
        if (r.width > 0 && r.height > 0) return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
      }
      return null;
    });
    if (actionBtnRect) {
      await page.mouse.click(actionBtnRect.x, actionBtnRect.y);
      await page.waitForTimeout(3000);
      const actionText = await frame.evaluate(() => document.body.innerText.substring(0, 2000));
      if (actionText.includes('Send Email') || actionText.includes('Add Tag')) {
        const sendEmail = frame.locator('text=Send Email').first();
        if (await sendEmail.count() > 0) {
          await sendEmail.click({ timeout: 5000 });
          await page.waitForTimeout(2000);
          actionAdded = true;
          console.log('  Action "Send Email" added');
        }
      }
    }
  }

  const afterNodes = await waitForVueFlowNodes(frame, 5000).catch(() => []);
  const afterFallback = afterNodes.length > 0 ? afterNodes : await frame.evaluate(() =>
    Array.from(document.querySelectorAll('.vue-flow .vue-flow__node')).map(n => n.textContent?.trim() || '')
  );
  console.log(`\nSTEP 5: AFTER-SAVE — nodes: ${JSON.stringify(afterFallback)}`);
  await page.screenshot({ path: ss('04_after_save'), fullPage: true });

  console.log('\nSTEP 6: Navigate away...');
  await page.goto(AUTOMATION_LIST_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(12000);

  console.log('\nSTEP 7: Re-open WF-01...');
  await page.goto(WF_EDITOR_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(18000);

  const frame2 = await waitForWfFrame(page);
  if (!frame2) {
    console.error('FATAL: iframe not found on reopen');
    await browser.close();
    return;
  }
  await dismissModal(frame2);
  await page.waitForTimeout(3000);

  const reloadNodes = await waitForVueFlowNodes(frame2);
  console.log(`\nSTEP 8: AFTER-RELOAD — nodes: ${JSON.stringify(reloadNodes)}`);
  await page.screenshot({ path: ss('05_after_reload'), fullPage: true });

  const defaultEmpty = ['END', 'Add New Trigger'];
  const isDefault = (nodes: string[]) =>
    nodes.length <= 2 && nodes.every(n => defaultEmpty.includes(n));

  const persisted = !isDefault(reloadNodes) && reloadNodes.some(n =>
    n.includes('Form Submitted') || n.includes('Contact Created') || n.includes('Send Email') || n.includes('Contact Changed')
  );

  console.log('\n═══════════════════════════════════════');
  console.log('    PERSISTENCE PROOF V3 RESULT');
  console.log('═══════════════════════════════════════');
  console.log(`  Tool: Playwright (storageState, headed)`);
  console.log(`  Before:  ${JSON.stringify(beforeNodes)}`);
  console.log(`  After:   ${JSON.stringify(afterFallback)}`);
  console.log(`  Reload:  ${JSON.stringify(reloadNodes)}`);
  console.log(`  Default empty: ${isDefault(reloadNodes)}`);
  console.log(`  Trigger added in session: ${triggerAdded}`);
  console.log(`  Action added in session: ${actionAdded}`);
  console.log(`  VERDICT: ${persisted ? 'PERSISTED ✅' : 'NOT PERSISTED ❌'}`);

  if (!triggerAdded) {
    console.log(`  BLOCKER: Cannot open trigger selection panel — GHL editor toolbar intercepts clicks and vue-flow node may not be in DOM at expected location.`);
    console.log(`  NEXT: Try Stagehand act() which uses AI to identify and interact with elements.`);
  } else if (!persisted) {
    console.log(`  BLOCKER: Changes visually appear but Vue.js/Pinia state does not register mutation — GHL backend never called.`);
    console.log(`  NEXT: Try Stagehand act() for AI-native event dispatch.`);
  }
  console.log('═══════════════════════════════════════\n');

  console.log('Evidence files:');
  evidenceFiles.forEach((f, i) => console.log(`  ${i + 1}. ${f}`));

  await browser.close();
}

run().catch(err => {
  console.error('Script error:', err);
  process.exit(1);
});
