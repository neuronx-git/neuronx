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

  const frame = getWfFrame(page)
  if (!frame) {
    console.log('Frame not found')
    await browser.close()
    return
  }

  const fullText = await frame.evaluate(() => document.body?.innerText ?? '')
  console.log('Full frame text:')
  console.log(fullText.substring(0, 3000))

  const rows = await frame.evaluate(() => {
    const trs = document.querySelectorAll('tr, [class*=workflow-row], [class*=list-item]')
    return Array.from(trs).map(r => ({
      text: (r.textContent ?? '').trim().substring(0, 100),
      cls: (r.className ?? '').toString().substring(0, 60),
    }))
  })
  console.log('\nRows:', JSON.stringify(rows.filter(r => r.text.length > 5).slice(0, 20), null, 2))

  const links = await frame.evaluate(() => {
    return Array.from(document.querySelectorAll('a')).map(a => ({
      text: (a.textContent ?? '').trim().substring(0, 60),
      href: a.getAttribute('href') ?? '',
    })).filter(a => a.text.length > 0 && (a.href.includes('workflow') || a.text.includes('Untitled') || a.text.includes('WF')))
  })
  console.log('\nWorkflow links:', JSON.stringify(links, null, 2))

  await browser.close()
}

run().catch((err) => {
  console.error('FATAL:', err.message)
  process.exit(1)
})
