import { chromium } from 'playwright'

const AUTH = '/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json'
const LOC = 'FlRL82M0D6nclmKT7eXH'
const FUNNEL_ID = 'VmB52pLVfOShgksvmBir'

async function run() {
  const browser = await chromium.launch({ headless: false })
  const ctx = await browser.newContext({ storageState: AUTH, viewport: { width: 1440, height: 900 } })
  const page = await ctx.newPage()

  console.log('Navigating to funnel steps...')
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/funnels-websites/funnels/${FUNNEL_ID}/steps`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )
  await page.waitForTimeout(12000)

  const bodyText = await page.evaluate(() => document.body?.innerText ?? '')

  if (bodyText.includes('Immigration Inquiry')) {
    console.log('Funnel step already exists. Skipping.')
    await browser.close()
    process.exit(0)
  }

  console.log('Step 1: Click "Add New Step or Import"...')
  await page.getByText('Add New Step').first().click()
  await page.waitForTimeout(3000)

  console.log('Step 2: Fill step name and path...')
  const nameInput = page.locator('input[placeholder="Name for Page"]')
  await nameInput.waitFor({ timeout: 5000 })
  await nameInput.fill('Immigration Inquiry')

  const pathInput = page.locator('input[placeholder="Path"]')
  await pathInput.fill('inquiry')
  await page.waitForTimeout(500)

  console.log('Step 3: Click "Create Funnel Step"...')
  await page.getByText('Create Funnel Step', { exact: true }).click()
  await page.waitForTimeout(8000)

  console.log('URL:', page.url())
  const afterText = await page.evaluate(() => document.body?.innerText?.substring(0, 1000) ?? '')
  console.log('After step creation:', afterText.substring(0, 500))

  const stepCreated = afterText.includes('Immigration Inquiry')
  console.log('Step created:', stepCreated)

  if (stepCreated) {
    console.log('\nStep 4: Look for page editor button...')
    const editBtn = page.getByText('Edit').first()
    const openEditor = page.getByText('Open Editor')
    const editPage = page.getByText('Edit Page')

    const allBtns = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('button, a'))
        .filter(b => b.getBoundingClientRect().width > 0)
        .map(b => (b.textContent ?? '').trim().substring(0, 60))
        .filter(t => t.length > 0 && t.length < 60)
    })
    console.log('Available buttons:', JSON.stringify(allBtns.slice(0, 20)))
  }

  await browser.close()
  console.log('\nFunnel step creation complete')
}

run().catch((err) => {
  console.error('FATAL:', err.message)
  process.exit(1)
})
