import { chromium, Page, Frame } from 'playwright'

const AUTH = '/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json'
const LOC = 'FlRL82M0D6nclmKT7eXH'

function getWfFrame(page: Page): Frame | null {
  return page.frames().find(f => f.url().includes('client-app-automation-workflows')) ?? null
}

async function waitForWfFrame(page: Page, timeout = 30000): Promise<Frame | null> {
  const start = Date.now()
  while (Date.now() - start < timeout) {
    const f = getWfFrame(page)
    if (f) {
      const t = await f.evaluate(() => document.body?.innerText ?? '').catch(() => '')
      if (t.length > 50) return f
    }
    await page.waitForTimeout(2000)
  }
  return null
}

async function run() {
  const browser = await chromium.launch({ headless: false })
  const ctx = await browser.newContext({ storageState: AUTH, viewport: { width: 1440, height: 900 } })
  const page = await ctx.newPage()

  console.log('Opening workflow list...')
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )
  const listFrame = await waitForWfFrame(page)
  if (!listFrame) { await browser.close(); return }

  console.log('Clicking WF-01...')
  await listFrame.getByText('WF-01 New Inquiry Acknowledge').first().click()
  await page.waitForTimeout(15000)

  await page.keyboard.press('Escape')
  await page.waitForTimeout(1000)

  const frame = getWfFrame(page)
  if (!frame) { console.log('No editor frame'); await browser.close(); return }

  const text = await frame.evaluate(() => document.body?.innerText ?? '')
  console.log('Editor text (300):', text.substring(0, 300))

  const hasEmptyTrigger = text.includes('Add New Trigger')
  console.log('Trigger empty:', hasEmptyTrigger)

  if (hasEmptyTrigger) {
    console.log('\nEnsuring Builder tab is active...')
    const builderTab = frame.locator('[data-name="builder"], [aria-label="Builder"]')
    if ((await builderTab.count()) > 0) {
      await builderTab.first().click()
      await page.waitForTimeout(2000)
    }

    console.log('\nStep 1: Click "Add New Trigger" node...')
    const triggerNode = frame.locator('[data-id="add-new-trigger"]')
    if ((await triggerNode.count()) > 0) {
      await triggerNode.scrollIntoViewIfNeeded()
      await page.waitForTimeout(500)
      await triggerNode.click({ position: { x: 50, y: 20 }, force: true })
    } else {
      console.log('  Trigger node not found by data-id, trying click via JS...')
      await frame.evaluate(() => {
        const node = document.querySelector('[data-id="add-new-trigger"]')
        if (node) (node as HTMLElement).click()
      })
    }
    await page.waitForTimeout(3000)

    const panel = await frame.evaluate(() => document.body?.innerText?.substring(0, 1500) ?? '')
    console.log('Trigger panel text:', panel.substring(0, 500))

    console.log('\nStep 2: Click "Form Submitted"...')
    await frame.getByText('Form Submitted', { exact: true }).first().click()
    await page.waitForTimeout(3000)

    const configPanel = await frame.evaluate(() => document.body?.innerText?.substring(0, 1500) ?? '')
    console.log('Config panel:', configPanel.substring(0, 500))

    console.log('\nStep 3: Save Trigger...')
    const saveBtn = frame.getByText('Save Trigger', { exact: true })
    console.log('Save Trigger button count:', await saveBtn.count())
    if ((await saveBtn.count()) > 0) {
      await saveBtn.click()
      await page.waitForTimeout(5000)
    }

    const afterSave = await frame.evaluate(() => document.body?.innerText?.substring(0, 800) ?? '')
    console.log('After save:', afterSave.substring(0, 400))

    console.log('\n=== Check nodes after trigger save ===')
    const nodesAfter = await frame.evaluate(() => {
      return Array.from(document.querySelectorAll('[class*=vue-flow__node]')).map(n => ({
        cls: (n.className ?? '').toString().substring(0, 100),
        text: (n.textContent ?? '').trim().substring(0, 60),
      }))
    })
    console.log(JSON.stringify(nodesAfter, null, 2))

    const allClickable = await frame.evaluate(() => {
      return Array.from(document.querySelectorAll('button, [role=button], [class*=add], [class*=plus]'))
        .filter(el => {
          const r = el.getBoundingClientRect()
          return r.width > 0 && r.height > 0 && r.width < 200
        })
        .map(el => ({
          tag: el.tagName,
          text: (el.textContent ?? '').trim().substring(0, 40),
          cls: (el.className ?? '').toString().substring(0, 80),
          pos: { x: Math.round(el.getBoundingClientRect().x), y: Math.round(el.getBoundingClientRect().y) },
        }))
    })
    console.log('Clickable:', JSON.stringify(allClickable.slice(0, 20), null, 2))
  }

  await browser.close()
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
