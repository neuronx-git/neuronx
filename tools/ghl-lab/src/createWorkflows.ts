import { chromium, Page, Frame } from 'playwright'

const AUTH = '/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json'
const LOC = 'FlRL82M0D6nclmKT7eXH'

const WORKFLOW_NAMES = [
  'WF-02 Contact Attempt Sequence',
  'WF-04 Readiness Complete Invite Booking',
]

function getWfFrame(page: Page): Frame | null {
  return page.frames().find(f => f.url().includes('client-app-automation-workflows')) ?? null
}

async function waitForWfFrame(page: Page, timeout = 30000): Promise<Frame | null> {
  const start = Date.now()
  while (Date.now() - start < timeout) {
    const frame = getWfFrame(page)
    if (frame) {
      const text = await frame.evaluate(() => document.body?.innerText ?? '').catch(() => '')
      if (text.length > 50) return frame
    }
    await page.waitForTimeout(2000)
  }
  return null
}

async function run() {
  const browser = await chromium.launch({ headless: false })
  const ctx = await browser.newContext({ storageState: AUTH, viewport: { width: 1440, height: 900 } })
  const page = await ctx.newPage()

  let created = 0

  for (let i = 0; i < WORKFLOW_NAMES.length; i++) {
    const wfName = WORKFLOW_NAMES[i]
    console.log(`\n[${i + 1}/11] Creating "${wfName}"...`)

    await page.goto(
      `https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`,
      { waitUntil: 'domcontentloaded', timeout: 60000 },
    )

    const frame = await waitForWfFrame(page)
    if (!frame) {
      console.log('  ERROR: Frame not found')
      continue
    }

    console.log('  Clicking Create Workflow...')
    const createBtn = frame.getByText('Create Workflow', { exact: true })
    const start = Date.now()
    while ((await createBtn.count()) === 0 && Date.now() - start < 15000) {
      await page.waitForTimeout(2000)
    }
    if ((await createBtn.count()) === 0) {
      console.log('  ERROR: Create Workflow not found')
      continue
    }
    await createBtn.click()
    await page.waitForTimeout(3000)

    console.log('  Looking for Start from Scratch...')
    let foundScratch = false
    const scratchStart = Date.now()
    while (Date.now() - scratchStart < 15000) {
      const scratchBtn = frame.getByText('Start from Scratch')
      const continueBtn = frame.getByText('Continue', { exact: true })
      if ((await scratchBtn.count()) > 0) {
        await scratchBtn.click()
        foundScratch = true
        break
      } else if ((await continueBtn.count()) > 0) {
        await continueBtn.click()
        foundScratch = true
        break
      }
      await page.waitForTimeout(2000)
    }
    if (!foundScratch) {
      console.log('  ERROR: No Scratch/Continue button')
      continue
    }

    console.log('  Waiting for editor...')
    await page.waitForTimeout(10000)

    const editorUrl = page.url()
    console.log('  URL:', editorUrl)

    const editorFrame = getWfFrame(page)
    if (editorFrame) {
      const edText = await editorFrame.evaluate(() => document.body?.innerText?.substring(0, 600) ?? '')
      console.log('  Editor:', edText.substring(0, 200))

      console.log('  Closing any modal overlays...')
      await editorFrame.evaluate(() => {
        const masks = document.querySelectorAll('.n-modal-mask, .n-modal-container, [class*=modal]')
        masks.forEach(m => {
          if (m instanceof HTMLElement) m.style.display = 'none'
        })
        const overlays = document.querySelectorAll('[aria-hidden=true]')
        overlays.forEach(o => {
          if (o instanceof HTMLElement && o.classList.contains('n-modal-mask')) {
            o.style.display = 'none'
          }
        })
      })
      await page.waitForTimeout(500)

      const escapeModal = async () => {
        await page.keyboard.press('Escape')
        await page.waitForTimeout(1000)
      }
      await escapeModal()

      console.log('  Renaming workflow...')
      let renamed = false

      for (const target of [editorFrame, page]) {
        const nameEl = target.locator('h1:has-text("New Workflow")').first()
        if ((await nameEl.count()) > 0) {
          console.log('  Found name element in', target === page ? 'page' : 'frame')
          await nameEl.click({ force: true, timeout: 5000 })
          await page.waitForTimeout(500)
          await page.keyboard.press('Meta+a')
          await page.keyboard.type(wfName)
          await page.keyboard.press('Enter')
          await page.waitForTimeout(500)
          renamed = true
          console.log('  Named:', wfName)
          break
        }
      }

      if (!renamed) {
        console.log('  Could not find name. Trying all h1/input...')
        for (const target of [editorFrame, page]) {
          const allH1 = await target.locator('h1').all()
          for (const h of allH1) {
            const t = await h.textContent().catch(() => '')
            if (t?.includes('New Workflow') || t?.includes('Untitled')) {
              await h.click({ force: true, timeout: 5000 })
              await page.waitForTimeout(300)
              await page.keyboard.press('Meta+a')
              await page.keyboard.type(wfName)
              await page.keyboard.press('Enter')
              renamed = true
              console.log('  Named via h1:', wfName)
              break
            }
          }
          if (renamed) break
        }
      }

      if (!renamed) console.log('  WARNING: Could not rename')

      await page.waitForTimeout(500)

      const saveBtn = editorFrame.locator('button').filter({ hasText: 'Save' }).first()
      if ((await saveBtn.count()) > 0) {
        await saveBtn.click({ force: true })
        await page.waitForTimeout(3000)
        console.log('  Saved')
      }
    }

    created++
    console.log(`  [${i + 1}] Done`)
  }

  console.log(`\n=== Workflows Created: ${created}/11 ===`)

  console.log('\nVerifying...')
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )
  const frame = await waitForWfFrame(page)
  if (frame) {
    const text = await frame.evaluate(() => document.body?.innerText ?? '')
    console.log('Final list:', text.substring(0, 2000))
  }

  await browser.close()
}

run().catch((err) => {
  console.error('FATAL:', err.message)
  process.exit(1)
})
