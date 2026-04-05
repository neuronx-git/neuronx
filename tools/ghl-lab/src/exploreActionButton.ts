import { chromium, Page, Frame } from 'playwright'

const AUTH = '/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json'
const LOC = 'FlRL82M0D6nclmKT7eXH'

function getWfFrame(page: Page): Frame | null {
  return page.frames().find(f => f.url().includes('client-app-automation-workflows')) ?? null
}

async function run() {
  const browser = await chromium.launch({ headless: false })
  const ctx = await browser.newContext({ storageState: AUTH, viewport: { width: 1440, height: 900 } })
  const page = await ctx.newPage()

  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )
  await page.waitForTimeout(20000)

  const listFrame = getWfFrame(page)
  if (!listFrame) { await browser.close(); return }

  await listFrame.getByText('WF-01 New Inquiry Acknowledge').first().click()
  await page.waitForTimeout(12000)
  await page.keyboard.press('Escape')
  await page.waitForTimeout(1000)

  const frame = getWfFrame(page)
  if (!frame) { await browser.close(); return }

  const builderTab = frame.locator('[data-name="builder"]')
  if ((await builderTab.count()) > 0) {
    await builderTab.first().click()
    await page.waitForTimeout(2000)
  }

  console.log('=== Finding the Add Action (+) button ===')

  const pgActionsDiv = await frame.evaluate(() => {
    const div = document.querySelector('.pg-actions__dv--add-action')
    if (!div) return 'NOT_FOUND'
    const rect = div.getBoundingClientRect()
    return {
      cls: div.className,
      text: (div.textContent ?? '').trim(),
      html: div.innerHTML.substring(0, 300),
      rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) },
    }
  })
  console.log('pg-actions div:', JSON.stringify(pgActionsDiv, null, 2))

  const allEdgeButtons = await frame.evaluate(() => {
    return Array.from(document.querySelectorAll('.vue-flow__edge, [class*=edge], [class*=add-action]'))
      .filter(el => el.getBoundingClientRect().width > 0)
      .map(el => ({
        tag: el.tagName,
        cls: (el.className ?? '').toString().substring(0, 80),
        text: (el.textContent ?? '').trim().substring(0, 40),
        rect: {
          x: Math.round(el.getBoundingClientRect().x),
          y: Math.round(el.getBoundingClientRect().y),
          w: Math.round(el.getBoundingClientRect().width),
          h: Math.round(el.getBoundingClientRect().height),
        },
      }))
  })
  console.log('Edge/add elements:', JSON.stringify(allEdgeButtons.slice(0, 10), null, 2))

  console.log('\n=== Try clicking the + via dispatchEvent on button inside pg-actions ===')
  const clickResult = await frame.evaluate(() => {
    const addDiv = document.querySelector('.pg-actions__dv--add-action')
    if (!addDiv) return 'div_not_found'
    const btn = addDiv.querySelector('button')
    if (!btn) return 'btn_not_found'
    btn.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))
    btn.dispatchEvent(new PointerEvent('pointerup', { bubbles: true }))
    btn.dispatchEvent(new MouseEvent('click', { bubbles: true }))
    return 'clicked'
  })
  console.log('Click result:', clickResult)
  await page.waitForTimeout(3000)

  const afterClick = await frame.evaluate(() => document.body?.innerText?.substring(0, 1500) ?? '')
  const hasActionPanel = afterClick.includes('Search For Actions') || afterClick.includes('Add Action') || afterClick.includes('Send SMS') || afterClick.includes('Add Contact Tag')
  console.log('Action panel opened:', hasActionPanel)
  console.log('After click text:', afterClick.substring(0, 500))

  if (!hasActionPanel) {
    console.log('\n=== Try Playwright click on the + button ===')
    const plusBtnLocator = frame.locator('.pg-actions__dv--add-action button')
    console.log('Button count:', await plusBtnLocator.count())
    if ((await plusBtnLocator.count()) > 0) {
      const box = await plusBtnLocator.boundingBox()
      console.log('Button bounding box:', box)
      if (box) {
        const iframeEl = await page.locator('iframe').first().boundingBox()
        const ox = iframeEl?.x ?? 0
        const oy = iframeEl?.y ?? 0
        console.log('Iframe offset:', { ox, oy })
        console.log('Click target:', { x: ox + box.x + box.width / 2, y: oy + box.y + box.height / 2 })
        await page.mouse.click(ox + box.x + box.width / 2, oy + box.y + box.height / 2)
        await page.waitForTimeout(3000)

        const afterMouse = await frame.evaluate(() => document.body?.innerText?.substring(0, 500) ?? '')
        console.log('After mouse click:', afterMouse.substring(0, 300))
      }
    }
  }

  await browser.close()
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
