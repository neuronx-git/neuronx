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

  const lf = getWfFrame(page)
  if (!lf) { await browser.close(); return }

  await lf.getByText('WF-06 No-Show Recovery').first().click()
  await page.waitForTimeout(15000)
  await page.keyboard.press('Escape')
  await page.waitForTimeout(2000)

  const frame = getWfFrame(page)!
  const text = await frame.evaluate(() => document.body?.innerText ?? '')
  console.log('Editor text (first 2000):')
  console.log(text.substring(0, 2000))

  console.log('\n=== All buttons in editor ===')
  const btns = await frame.evaluate(() => {
    return Array.from(document.querySelectorAll('button'))
      .filter(b => b.getBoundingClientRect().width > 0)
      .map(b => ({
        text: (b.textContent ?? '').trim().substring(0, 50),
        cls: (b.className ?? '').toString().substring(0, 80),
        rect: { x: Math.round(b.getBoundingClientRect().x), y: Math.round(b.getBoundingClientRect().y) },
      }))
      .filter(b => b.text.length > 0)
  })
  console.log(JSON.stringify(btns, null, 2))

  console.log('\n=== Nodes ===')
  const nodes = await frame.evaluate(() =>
    Array.from(document.querySelectorAll('.vue-flow__node')).map(n => (n.textContent ?? '').trim().substring(0, 60))
  )
  console.log(nodes)

  console.log('\n=== Header area ===')
  const header = await frame.evaluate(() => {
    const h = document.querySelector('#cmp-header, [class*=header], header')
    if (!h) return 'no header found'
    return (h.textContent ?? '').trim().substring(0, 200)
  })
  console.log(header)

  console.log('\n=== Looking for Save/Publish/Draft toggle ===')
  const toggles = await frame.evaluate(() => {
    return Array.from(document.querySelectorAll('button, [role=switch], [class*=toggle], [class*=publish], [class*=draft]'))
      .filter(el => el.getBoundingClientRect().width > 0)
      .map(el => ({
        tag: el.tagName,
        text: (el.textContent ?? '').trim().substring(0, 40),
        cls: (el.className ?? '').toString().substring(0, 60),
        role: el.getAttribute('role') ?? '',
        ariaLabel: el.getAttribute('aria-label') ?? '',
        pos: { x: Math.round(el.getBoundingClientRect().x), y: Math.round(el.getBoundingClientRect().y) },
      }))
  })
  console.log(JSON.stringify(toggles.slice(0, 20), null, 2))

  await browser.close()
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
