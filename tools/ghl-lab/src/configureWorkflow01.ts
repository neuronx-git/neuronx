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

async function openWorkflow(page: Page, wfName: string): Promise<Frame | null> {
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )
  const listFrame = await waitForWfFrame(page)
  if (!listFrame) return null

  const link = listFrame.getByText(wfName)
  if ((await link.count()) === 0) {
    console.log(`  "${wfName}" not found on first page, checking page 2...`)
    const nextPage = listFrame.locator('[aria-label="Next Page"], [class*=next]')
    if ((await nextPage.count()) > 0) {
      await nextPage.click()
      await page.waitForTimeout(5000)
    }
    if ((await link.count()) === 0) return null
  }

  await link.first().click()
  await page.waitForTimeout(12000)
  await page.keyboard.press('Escape')
  await page.waitForTimeout(1000)

  return getWfFrame(page)
}

async function clickTriggerType(frame: Frame, page: Page, triggerName: string): Promise<boolean> {
  console.log(`  Adding trigger: "${triggerName}"`)

  const addTriggerNode = frame.locator('.vue-flow__node-newTrigger')
  if ((await addTriggerNode.count()) > 0) {
    await addTriggerNode.click()
    await page.waitForTimeout(3000)
  }

  const triggerOption = frame.getByText(triggerName, { exact: true })
  if ((await triggerOption.count()) === 0) {
    console.log(`    Trigger "${triggerName}" not found in list`)
    return false
  }

  await triggerOption.first().click()
  await page.waitForTimeout(3000)

  console.log(`    Trigger "${triggerName}" selected`)
  return true
}

async function run() {
  const browser = await chromium.launch({ headless: false })
  const ctx = await browser.newContext({ storageState: AUTH, viewport: { width: 1440, height: 900 } })
  const page = await ctx.newPage()

  console.log('=== Configuring WF-01: New Inquiry Acknowledge ===')

  const frame = await openWorkflow(page, 'WF-01 New Inquiry Acknowledge')
  if (!frame) {
    console.log('ERROR: Could not open WF-01')
    await browser.close()
    return
  }

  console.log('WF-01 editor loaded')

  const editorText = await frame.evaluate(() => document.body?.innerText ?? '')
  console.log('Editor text (200):', editorText.substring(0, 200))

  console.log('\nStep 1: Add "Form Submitted" trigger...')
  const ok = await clickTriggerType(frame, page, 'Form Submitted')
  if (!ok) {
    console.log('  Could not add trigger')
    await browser.close()
    return
  }

  console.log('\nStep 2: Configure trigger settings...')
  const configText = await frame.evaluate(() => document.body?.innerText?.substring(0, 2000) ?? '')
  console.log('Config panel:', configText.substring(0, 800))

  const allInputs = await frame.evaluate(() => {
    return Array.from(document.querySelectorAll('input, select, textarea, [class*=select], [class*=dropdown]')).map(el => ({
      tag: el.tagName,
      type: el.getAttribute('type') ?? '',
      placeholder: el.getAttribute('placeholder') ?? '',
      value: (el as any).value ?? '',
      cls: (el.className ?? '').toString().substring(0, 60),
    }))
  })
  console.log('Inputs:', JSON.stringify(allInputs.slice(0, 15), null, 2))

  const btns = await frame.evaluate(() => {
    return Array.from(document.querySelectorAll('button'))
      .filter(b => b.getBoundingClientRect().width > 0)
      .map(b => (b.textContent ?? '').trim().substring(0, 60))
      .filter(t => t.length > 0)
  })
  console.log('Buttons:', JSON.stringify(btns.slice(0, 15)))

  const selects = await frame.evaluate(() => {
    return Array.from(document.querySelectorAll('[class*=n-select], [class*=n-base-selection]')).map(el => ({
      text: (el.textContent ?? '').trim().substring(0, 80),
      cls: (el.className ?? '').toString().substring(0, 80),
    }))
  })
  console.log('Select elements:', JSON.stringify(selects.slice(0, 10), null, 2))

  await browser.close()
}

run().catch((err) => {
  console.error('FATAL:', err.message)
  process.exit(1)
})
