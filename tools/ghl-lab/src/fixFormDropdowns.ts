import { chromium, Page, Frame } from 'playwright'

const AUTH = '/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json'
const LOC = 'FlRL82M0D6nclmKT7eXH'
const FORM_ID = 'FNMmVXpfUvUypS0c4oQ3'

function getFormFrame(page: Page): Frame | null {
  return page.frames().find(f => f.url().includes('leadgen-apps-form-survey-builder')) ?? null
}

async function waitForFormFrame(page: Page, timeout = 30000): Promise<Frame | null> {
  const start = Date.now()
  while (Date.now() - start < timeout) {
    const f = getFormFrame(page)
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

  console.log('Opening form builder...')
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/form-builder-v2/${FORM_ID}`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )
  await page.waitForTimeout(15000)

  const frame = await waitForFormFrame(page)
  if (!frame) {
    console.log('Form builder frame not found')
    await browser.close()
    return
  }

  console.log('Frame found. Clicking Edit tab...')
  const editTab = frame.getByText('Edit', { exact: true })
  if ((await editTab.count()) > 0) {
    await editTab.click()
    await page.waitForTimeout(3000)
  }

  const fieldWrappers = await frame.evaluate(() => {
    return Array.from(document.querySelectorAll('.smooth-dnd-draggable-wrapper.element-box'))
      .map((w, i) => ({
        index: i,
        text: (w.textContent ?? '').trim().substring(0, 80),
      }))
  })
  console.log('Form fields:')
  fieldWrappers.forEach(f => console.log(`  [${f.index}] ${f.text}`))

  const dropdownFields = [
    { label: 'Country of Residence', options: ['Canada', 'India', 'Philippines', 'Nigeria', 'Pakistan', 'Other'] },
    { label: 'Program Interest', options: ['Express Entry', 'Provincial Nominee (PNP)', 'Study Permit', 'Work Permit', 'Family Sponsorship', 'Visitor Visa', 'Not Sure'] },
    { label: 'Timeline', options: ['Within 3 months', '3-6 months', '6-12 months', 'More than 12 months', 'Just exploring'] },
  ]

  for (const dd of dropdownFields) {
    console.log(`\n=== Configuring "${dd.label}" ===`)

    const fieldWrapper = frame.locator('.smooth-dnd-draggable-wrapper.element-box').filter({ hasText: dd.label }).first()
    if ((await fieldWrapper.count()) === 0) {
      console.log(`  Field "${dd.label}" not found`)
      continue
    }

    await fieldWrapper.click()
    await page.waitForTimeout(2000)

    const panelText = await frame.evaluate(() => document.body?.innerText?.substring(0, 1000) ?? '')
    console.log('  Panel text:', panelText.substring(0, 300))

    const optionInputs = frame.locator('input[placeholder*="Enter" i], input[placeholder*="option" i], input[placeholder*="value" i]')
    const inputCount = await optionInputs.count()
    console.log(`  Option inputs found: ${inputCount}`)

    const existingInputs = await frame.evaluate(() => {
      return Array.from(document.querySelectorAll('input')).map(el => ({
        placeholder: el.placeholder,
        value: el.value,
        cls: el.className.substring(0, 60),
      })).filter(i => i.value.includes('Option') || i.placeholder.toLowerCase().includes('option') || i.placeholder.toLowerCase().includes('enter'))
    })
    console.log('  Existing inputs:', JSON.stringify(existingInputs))
  }

  await browser.close()
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
