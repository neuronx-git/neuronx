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

  console.log('Navigating to workflow list...')
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )
  const frame = await waitForWfFrame(page)
  if (!frame) { await browser.close(); return }

  console.log('Opening WF-01...')
  await frame.getByText('WF-01 New Inquiry Acknowledge').first().click()
  await page.waitForTimeout(12000)
  await page.keyboard.press('Escape')
  await page.waitForTimeout(1000)

  const wfFrame = getWfFrame(page)
  if (!wfFrame) { console.log('No editor frame'); await browser.close(); return }

  const text = await wfFrame.evaluate(() => document.body?.innerText ?? '')
  console.log('Editor full text:')
  console.log(text.substring(0, 2000))

  console.log('\n=== All vue-flow nodes ===')
  const nodes = await wfFrame.evaluate(() => {
    return Array.from(document.querySelectorAll('[class*=vue-flow__node]')).map(n => ({
      cls: n.className.substring(0, 100),
      text: (n.textContent ?? '').trim().substring(0, 60),
      rect: { x: Math.round(n.getBoundingClientRect().x), y: Math.round(n.getBoundingClientRect().y) },
    }))
  })
  console.log(JSON.stringify(nodes, null, 2))

  console.log('\n=== All edges ===')
  const edges = await wfFrame.evaluate(() => {
    return Array.from(document.querySelectorAll('[class*=vue-flow__edge]')).map(e => ({
      cls: e.className.substring(0, 100),
    }))
  })
  console.log('Edges:', edges.length)

  console.log('\n=== Plus/Add buttons (all interactable elements) ===')
  const interactable = await wfFrame.evaluate(() => {
    return Array.from(document.querySelectorAll('button, [role=button], svg, [class*=add], [class*=plus]'))
      .filter(b => b.getBoundingClientRect().width > 0 && b.getBoundingClientRect().height > 0)
      .map(b => ({
        tag: b.tagName,
        text: (b.textContent ?? '').trim().substring(0, 40),
        cls: (b.className ?? '').toString().substring(0, 80),
        rect: { x: Math.round(b.getBoundingClientRect().x), y: Math.round(b.getBoundingClientRect().y), w: Math.round(b.getBoundingClientRect().width), h: Math.round(b.getBoundingClientRect().height) },
      }))
      .filter(b => b.rect.w < 200 && b.rect.h < 200)
  })
  console.log(JSON.stringify(interactable.slice(0, 30), null, 2))

  await browser.close()
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
