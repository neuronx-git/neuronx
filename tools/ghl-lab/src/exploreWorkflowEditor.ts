import { chromium, Page, Frame } from 'playwright'

const AUTH = '/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json'
const LOC = 'FlRL82M0D6nclmKT7eXH'

function getWfFrame(page: Page): Frame | null {
  return page.frames().find(f => f.url().includes('client-app-automation-workflows')) ?? null
}

async function waitForWfFrame(page: Page, timeout = 30000): Promise<Frame | null> {
  const start = Date.now()
  while (Date.now() - start < timeout) {
    const frame = getWfFrame(page)
    if (frame) {
      const text = await frame.evaluate(() => document.body?.innerText ?? '').catch(() => '')
      if (text.length > 50) return frame
    }
    await page.waitForTimeout(2000)
  }
  return null
}

async function run() {
  const browser = await chromium.launch({ headless: false })
  const ctx = await browser.newContext({ storageState: AUTH, viewport: { width: 1440, height: 900 } })
  const page = await ctx.newPage()

  console.log('Navigating to workflow list...')
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )

  const frame = await waitForWfFrame(page)
  if (!frame) {
    console.log('Frame not found')
    await browser.close()
    return
  }

  const text = await frame.evaluate(() => document.body?.innerText ?? '')
  console.log('List page:', text.substring(0, 500))

  console.log('\nLooking for WF-01...')
  const wf01Link = frame.getByText('WF-01 New Inquiry Acknowledge')
  if ((await wf01Link.count()) === 0) {
    console.log('WF-01 not found on this page')
    const allLinks = await frame.evaluate(() => {
      return Array.from(document.querySelectorAll('a, [class*=workflow-name], td'))
        .map(el => (el.textContent ?? '').trim().substring(0, 60))
        .filter(t => t.includes('WF-') || t.includes('New Workflow'))
    })
    console.log('Found workflows:', JSON.stringify(allLinks))
    await browser.close()
    return
  }

  console.log('Clicking WF-01...')
  await wf01Link.first().click()
  await page.waitForTimeout(12000)

  console.log('URL:', page.url())

  await page.keyboard.press('Escape')
  await page.waitForTimeout(1000)

  const editorFrame = getWfFrame(page)
  if (!editorFrame) {
    console.log('Editor frame not found after click')
    const allFrames = page.frames().map(f => f.url().substring(0, 100))
    console.log('Frames:', allFrames)
    await browser.close()
    return
  }

  const editorText = await editorFrame.evaluate(() => document.body?.innerText ?? '')
  console.log('Editor text:', editorText.substring(0, 1500))

  console.log('\nLooking for trigger/action UI elements...')
  const allBtns = await editorFrame.evaluate(() => {
    return Array.from(document.querySelectorAll('button, [role=button], [class*=add], [class*=trigger], [class*=action]'))
      .filter(b => b.getBoundingClientRect().width > 0)
      .map(b => ({
        text: (b.textContent ?? '').trim().substring(0, 80),
        cls: (b.className ?? '').toString().substring(0, 80),
        tag: b.tagName,
      }))
      .filter(b => b.text.length > 0 && b.text.length < 80)
  })
  console.log('Elements:', JSON.stringify(allBtns.slice(0, 30), null, 2))

  const triggerArea = editorFrame.getByText('Add New Trigger')
  const addTrigger = editorFrame.getByText('Add Trigger')
  const addAction = editorFrame.getByText('Add Action')
  const plus = editorFrame.locator('[class*=add-button], [class*=plus]')

  console.log('\nAdd New Trigger:', await triggerArea.count())
  console.log('Add Trigger:', await addTrigger.count())
  console.log('Add Action:', await addAction.count())
  console.log('Plus buttons:', await plus.count())

  if ((await addTrigger.count()) > 0) {
    console.log('\n=== Clicking Add Trigger ===')
    await addTrigger.first().click()
    await page.waitForTimeout(3000)

    const panelText = await editorFrame.evaluate(() => document.body?.innerText?.substring(0, 3000) ?? '')
    console.log('After Add Trigger:', panelText.substring(0, 1500))
  } else if ((await triggerArea.count()) > 0) {
    console.log('\n=== Clicking Add New Trigger ===')
    await triggerArea.first().click()
    await page.waitForTimeout(3000)

    const panelText = await editorFrame.evaluate(() => document.body?.innerText?.substring(0, 3000) ?? '')
    console.log('After Add New Trigger:', panelText.substring(0, 1500))
  }

  await browser.close()
}

run().catch((err) => {
  console.error('FATAL:', err.message)
  process.exit(1)
})
