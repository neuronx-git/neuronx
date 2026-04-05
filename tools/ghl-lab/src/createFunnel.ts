import { chromium, Page, Frame } from 'playwright'

const AUTH = '/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json'
const LOC = 'FlRL82M0D6nclmKT7eXH'
const FUNNEL_NAME = 'NeuronX Intake Landing (V1)'

async function run() {
  const browser = await chromium.launch({ headless: false })
  const ctx = await browser.newContext({ storageState: AUTH, viewport: { width: 1440, height: 900 } })
  const page = await ctx.newPage()

  console.log('Step 1: Navigate to Funnels...')
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/funnels-websites/funnels`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )
  await page.waitForTimeout(12000)

  const bodyText = await page.evaluate(() => document.body?.innerText ?? '')
  if (bodyText.includes(FUNNEL_NAME)) {
    console.log('Funnel already exists. Skipping creation.')
    await browser.close()
    process.exit(0)
  }

  console.log('Step 2: Click "New Funnel"...')
  await page.getByText('New Funnel', { exact: true }).first().click()
  await page.waitForTimeout(3000)

  console.log('Step 3: Select "From blank" and fill name...')
  const fromBlank = page.getByText('From blank', { exact: true })
  if ((await fromBlank.count()) > 0) {
    await fromBlank.click()
    await page.waitForTimeout(500)
  }

  const nameInput = page.locator('input[placeholder="Name for your awesome Funnel"]')
  await nameInput.waitFor({ timeout: 5000 })
  await nameInput.fill(FUNNEL_NAME)
  await page.waitForTimeout(500)
  console.log('  Name filled:', FUNNEL_NAME)

  console.log('Step 4: Click "Create"...')
  const createBtn = page.locator('.hl-modal-footer-actions button').filter({ hasText: 'Create' })
  await createBtn.click()
  await page.waitForTimeout(10000)

  console.log('URL after create:', page.url())
  const pageText = await page.evaluate(() => document.body?.innerText?.substring(0, 1000) ?? '')
  console.log('Page text:', pageText.substring(0, 500))

  const funnelCreated = page.url().includes('funnels-websites') || pageText.includes(FUNNEL_NAME)
  console.log('Funnel created:', funnelCreated)

  if (funnelCreated) {
    console.log('\n=== Step 5: Explore funnel step page ===')

    const allBtns = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('button, a, [role=button]'))
        .filter(b => b.getBoundingClientRect().width > 0)
        .map(b => ({
          text: (b.textContent ?? '').trim().substring(0, 60),
          tag: b.tagName,
          href: b.getAttribute('href') ?? '',
        }))
        .filter(b => b.text.length > 0 && b.text.length < 60)
    })
    console.log('Buttons:', JSON.stringify(allBtns.slice(0, 30), null, 2))
  }

  await browser.close()
  console.log('\nFunnel creation complete')
}

run().catch((err) => {
  console.error('FATAL:', err.message)
  process.exit(1)
})
