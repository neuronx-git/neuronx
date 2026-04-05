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

  console.log('Opening WF-06...')
  await page.goto(`https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`, { waitUntil: 'domcontentloaded', timeout: 60000 })
  await page.waitForTimeout(20000)

  const lf = getWfFrame(page)!
  await lf.getByText('WF-06 No-Show Recovery').first().click()
  await page.waitForTimeout(15000)
  await page.keyboard.press('Escape')
  await page.waitForTimeout(2000)

  const frame = getWfFrame(page)!

  console.log('\n=== STEP 1: Add trigger ===')
  const trigNode = frame.locator('[data-id="add-new-trigger"]')
  if ((await trigNode.count()) > 0) {
    await trigNode.click({ timeout: 5000 }).catch(async () => {
      await trigNode.click({ force: true, timeout: 5000 })
    })
    await page.waitForTimeout(3000)
  }

  let text = await frame.evaluate(() => document.body?.innerText ?? '')
  console.log('Trigger panel open:', text.includes('Search For Triggers'))

  if (text.includes('Search For Triggers')) {
    await frame.getByText('Appointment Status', { exact: true }).first().click()
    await page.waitForTimeout(3000)
    console.log('Selected Appointment Status')

    const saveRect = await frame.evaluate(() => {
      const b = Array.from(document.querySelectorAll('button')).find(b => b.textContent?.trim() === 'Save Trigger')
      if (!b) return null
      const r = b.getBoundingClientRect()
      return { x: r.x + r.width / 2, y: r.y + r.height / 2, inView: r.top >= 0 && r.bottom <= window.innerHeight }
    })
    console.log('Save Trigger button:', saveRect)

    if (saveRect) {
      await page.mouse.click(saveRect.x, saveRect.y)
      console.log('Clicked Save Trigger')
      await page.waitForTimeout(5000)
    }
  }

  const nodes1 = await frame.evaluate(() =>
    Array.from(document.querySelectorAll('.vue-flow__node')).map(n => (n.textContent ?? '').trim().substring(0, 60))
  )
  console.log('Nodes after trigger:', nodes1)

  console.log('\n=== STEP 2: Add action via aria-label button ===')
  const addActionBtn = frame.locator('button[aria-label="Add Action"]')
  console.log('Add Action button count:', await addActionBtn.count())
  if ((await addActionBtn.count()) > 0) {
    await addActionBtn.click()
    await page.waitForTimeout(3000)

    text = await frame.evaluate(() => document.body?.innerText ?? '')
    console.log('Action panel open:', text.includes('Search For Actions'))

    if (text.includes('Search For Actions')) {
      const search = frame.locator('input[placeholder*="Search" i]')
      if ((await search.count()) > 0) {
        await search.fill('Add Contact Tag')
        await page.waitForTimeout(2000)
      }

      await frame.getByText('Add Contact Tag', { exact: true }).first().click()
      await page.waitForTimeout(3000)
      console.log('Selected Add Contact Tag')

      const saveActionRect = await frame.evaluate(() => {
        const b = Array.from(document.querySelectorAll('button')).find(b => b.textContent?.trim() === 'Save Action')
        if (!b) return null
        const r = b.getBoundingClientRect()
        return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
      })
      console.log('Save Action button:', saveActionRect)

      if (saveActionRect) {
        await page.mouse.click(saveActionRect.x, saveActionRect.y)
        console.log('Clicked Save Action')
        await page.waitForTimeout(5000)
      }
    }
  }

  const nodes2 = await frame.evaluate(() =>
    Array.from(document.querySelectorAll('.vue-flow__node')).map(n => (n.textContent ?? '').trim().substring(0, 60))
  )
  console.log('Nodes after action:', nodes2)

  console.log('\n=== STEP 3: Wait for auto-save ===')
  await page.waitForTimeout(10000)

  const savedText = await frame.evaluate(() => document.body?.innerText ?? '')
  console.log('Has "Saved" text:', savedText.includes('Saved'))
  console.log('Has "Unsaved" text:', savedText.includes('Unsaved'))

  console.log('\n=== STEP 4: Navigate away and back to verify persistence ===')
  await page.goto(`https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`, { waitUntil: 'domcontentloaded', timeout: 60000 })
  await page.waitForTimeout(20000)

  const lf2 = getWfFrame(page)!
  await lf2.getByText('WF-06 No-Show Recovery').first().click()
  await page.waitForTimeout(15000)
  await page.keyboard.press('Escape')
  await page.waitForTimeout(2000)

  const frame2 = getWfFrame(page)!
  const nodes3 = await frame2.evaluate(() =>
    Array.from(document.querySelectorAll('.vue-flow__node')).map(n => (n.textContent ?? '').trim().substring(0, 60))
  )
  console.log('\n=== VERIFICATION ===')
  console.log('Nodes after re-open:', nodes3)
  console.log('Trigger persisted:', nodes3.some(n => n.includes('Appointment')))
  console.log('Action persisted:', nodes3.some(n => n.includes('Add Contact Tag')))

  await browser.close()
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
