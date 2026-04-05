import { chromium, Page, Frame } from 'playwright'

const AUTH = '/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json'
const LOC = 'FlRL82M0D6nclmKT7eXH'
const FORM_ID = 'FNMmVXpfUvUypS0c4oQ3'

function getFrame(page: Page): Frame {
  const f = page.frames().find(f => f.url().includes('leadgen-apps-form-survey-builder'))
  if (!f) throw new Error('Builder iframe not found')
  return f
}

async function waitForFields(frame: Frame, timeout = 30000): Promise<number> {
  const start = Date.now()
  while (Date.now() - start < timeout) {
    const n = await frame.locator('.smooth-dnd-draggable-wrapper.element-box').count().catch(() => 0)
    if (n > 0) return n
    await new Promise(r => setTimeout(r, 2000))
  }
  return 0
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
  await page.waitForTimeout(10000)

  const frame = getFrame(page)
  const rendered = await waitForFields(frame)
  console.log('Fields rendered:', rendered)

  const editTab = frame.getByText('Edit', { exact: true })
  if ((await editTab.count()) > 0) {
    await editTab.click()
    await page.waitForTimeout(3000)
  }

  const fields = await frame.evaluate(() => {
    const wrappers = document.querySelectorAll('.smooth-dnd-draggable-wrapper.element-box')
    return Array.from(wrappers).map((w, i) => ({
      index: i,
      text: (w.textContent ?? '').trim().substring(0, 80),
      hasLabel: !!w.querySelector('.label-input, [contenteditable]'),
    }))
  })
  console.log('Current fields:')
  fields.forEach(f => console.log(`  [${f.index}] ${f.text}`))

  console.log('\n=== Step 1: Click on each new field and configure ===')

  const fieldConfigs = [
    {
      currentName: 'Multi Line',
      newLabel: 'Notes / Message',
      placeholder: 'Tell us about your immigration goals...',
    },
    {
      currentName: 'Single Dropdown 17fpb',
      newLabel: 'Country of Residence',
      options: ['Canada', 'India', 'Philippines', 'Nigeria', 'Pakistan', 'Other'],
    },
    {
      currentName: 'Single Dropdown 168z3',
      newLabel: 'Program Interest',
      options: ['Express Entry', 'Provincial Nominee (PNP)', 'Study Permit', 'Work Permit', 'Family Sponsorship', 'Visitor Visa', 'Not Sure'],
    },
    {
      currentName: 'Single Dropdown 152dv',
      newLabel: 'Timeline',
      options: ['Within 3 months', '3-6 months', '6-12 months', 'More than 12 months', 'Just exploring'],
    },
  ]

  for (const config of fieldConfigs) {
    console.log(`\nConfiguring "${config.currentName}" -> "${config.newLabel}"...`)

    const fieldWrapper = frame.locator('.smooth-dnd-draggable-wrapper.element-box').filter({ hasText: config.currentName }).first()

    if ((await fieldWrapper.count()) === 0) {
      const altWrapper = frame.locator('.smooth-dnd-draggable-wrapper.element-box').filter({ hasText: config.newLabel }).first()
      if ((await altWrapper.count()) > 0) {
        console.log(`  Already renamed to "${config.newLabel}", skipping rename`)
        continue
      }
      console.log(`  Field "${config.currentName}" not found. Checking all fields...`)
      const all = await frame.evaluate(() => {
        return Array.from(document.querySelectorAll('.smooth-dnd-draggable-wrapper.element-box'))
          .map(w => (w.textContent ?? '').trim().substring(0, 60))
      })
      console.log('  All fields:', JSON.stringify(all))
      continue
    }

    await fieldWrapper.click()
    await page.waitForTimeout(2000)

    const settingsPanel = await frame.evaluate(() => {
      const panel = document.querySelector('[class*=edit-panel], [class*=field-settings], [class*=property-panel]')
      return panel ? (panel.textContent ?? '').trim().substring(0, 500) : 'no panel found'
    })
    console.log('  Settings panel:', settingsPanel.substring(0, 200))

    const labelInput = frame.locator('[contenteditable=true]').filter({ hasText: config.currentName }).first()
    if ((await labelInput.count()) > 0) {
      await labelInput.click()
      await page.keyboard.press('Meta+a')
      await page.keyboard.type(config.newLabel)
      console.log(`  Renamed to "${config.newLabel}"`)
    } else {
      console.log('  No contenteditable label found for rename')
      const allEditables = await frame.locator('[contenteditable=true]').all()
      for (const ed of allEditables) {
        const text = await ed.textContent().catch(() => '')
        if (text?.includes(config.currentName.split(' ')[0])) {
          await ed.click()
          await page.keyboard.press('Meta+a')
          await page.keyboard.type(config.newLabel)
          console.log(`  Renamed via partial match`)
          break
        }
      }
    }

    await page.waitForTimeout(1000)
  }

  console.log('\n=== Step 2: Save ===')
  await frame.getByText('Save', { exact: true }).click()
  await page.waitForTimeout(3000)
  console.log('Saved')

  const finalFields = await frame.evaluate(() => {
    return Array.from(document.querySelectorAll('.smooth-dnd-draggable-wrapper.element-box'))
      .map(w => (w.textContent ?? '').trim().substring(0, 60))
  })
  console.log('\nFinal fields:', JSON.stringify(finalFields))

  await browser.close()
}

run().catch((err) => {
  console.error('FATAL:', err.message)
  process.exit(1)
})
