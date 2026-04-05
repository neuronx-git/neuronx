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
  const frame = await waitForWfFrame(page)
  if (!frame) {
    console.log('Frame not found')
    await browser.close()
    return
  }

  const text = await frame.evaluate(() => document.body?.innerText ?? '')
  console.log('Page text:', text.substring(0, 1000))

  const junkRows = await frame.evaluate(() => {
    const rows = document.querySelectorAll('tr, [class*=workflow-row]')
    const junk: { index: number; text: string }[] = []
    rows.forEach((r, i) => {
      const t = (r.textContent ?? '').trim()
      if (t.includes('New Workflow :')) {
        junk.push({ index: i, text: t.substring(0, 80) })
      }
    })
    return junk
  })
  console.log('Junk workflows found:', junkRows.length)
  junkRows.forEach(j => console.log(`  [${j.index}] ${j.text}`))

  for (const junk of junkRows) {
    console.log(`\nDeleting: "${junk.text.substring(0, 40)}"...`)

    const row = frame.locator('tr, [class*=workflow-row]').nth(junk.index)
    const moreBtn = row.locator('[class*=more], [class*=menu], [class*=action], button').last()

    if ((await moreBtn.count()) > 0) {
      await moreBtn.click()
      await page.waitForTimeout(1500)

      const deleteOption = frame.getByText('Delete', { exact: true }).last()
      if ((await deleteOption.count()) > 0) {
        await deleteOption.click()
        await page.waitForTimeout(2000)

        const confirmBtn = frame.getByText('Delete', { exact: true }).last()
        if ((await confirmBtn.count()) > 0) {
          await confirmBtn.click()
          await page.waitForTimeout(3000)
          console.log('  Deleted')
        }
      }
    }
  }

  await browser.close()
  console.log('\nJunk cleanup complete')
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
