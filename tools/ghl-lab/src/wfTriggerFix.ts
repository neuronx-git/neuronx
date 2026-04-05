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

async function getIframeOffset(page: Page): Promise<{ x: number; y: number }> {
  const allIframes = await page.locator('iframe').all()
  for (const iframe of allIframes) {
    const src = await iframe.getAttribute('src').catch(() => '')
    if (src?.includes('automation-workflows')) {
      const box = await iframe.boundingBox()
      if (box) return { x: box.x, y: box.y }
    }
  }
  return { x: 0, y: 0 }
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
  const listFrame = await waitForWfFrame(page)
  if (!listFrame) { console.log('List frame not found'); await browser.close(); return }

  console.log('Clicking WF-01...')
  await listFrame.getByText('WF-01 New Inquiry Acknowledge').first().click()
  await page.waitForTimeout(15000)

  console.log('Dismissing modal...')
  await page.keyboard.press('Escape')
  await page.waitForTimeout(2000)

  const frame = getWfFrame(page)
  if (!frame) { console.log('Editor frame not found'); await browser.close(); return }

  console.log('Ensuring Builder tab...')
  const builderTab = frame.locator('[data-name="builder"]')
  if ((await builderTab.count()) > 0) {
    await builderTab.first().click({ force: true })
    await page.waitForTimeout(2000)
  }

  const iframeOffset = await getIframeOffset(page)
  console.log('Iframe offset:', iframeOffset)

  const allIframeInfo = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('iframe')).map((f, i) => ({
      i,
      src: f.src.substring(0, 80),
      box: f.getBoundingClientRect(),
    }))
  })
  console.log('All iframes:', JSON.stringify(allIframeInfo, null, 2))

  const text = await frame.evaluate(() => document.body?.innerText ?? '')
  console.log('Has Add New Trigger:', text.includes('Add New Trigger'))

  console.log('\n=== STEP 1: Click Add New Trigger ===')
  const triggerRect = await frame.evaluate(() => {
    const el = document.querySelector('[data-id="add-new-trigger"]') as HTMLElement
    if (!el) return null
    const r = el.getBoundingClientRect()
    return { x: r.x, y: r.y, w: r.width, h: r.height, cx: r.x + r.width / 2, cy: r.y + r.height / 2 }
  })
  console.log('Trigger node rect:', triggerRect)

  if (!triggerRect) {
    console.log('Trigger node not found in DOM')
    await browser.close()
    return
  }

  const whatIsAt = await page.evaluate(({x, y}) => {
    const el = document.elementFromPoint(x, y)
    return el ? { tag: el.tagName, text: (el.textContent ?? '').substring(0, 40), cls: (el.className ?? '').toString().substring(0, 60) } : null
  }, { x: triggerRect.cx, y: triggerRect.cy })
  console.log('Element at trigger coords (page level):', whatIsAt)

  console.log('Attempt 1: frame.locator click on add-new-trigger...')
  try {
    await frame.locator('[data-id="add-new-trigger"]').click({ timeout: 5000 })
    console.log('  frame.locator click succeeded')
  } catch (e) {
    console.log('  frame.locator click failed:', (e as Error).message.substring(0, 150))
    console.log('Attempt 2: page.mouse.click at iframe coords...')
    const tx = iframeOffset.x + triggerRect.cx
    const ty = iframeOffset.y + triggerRect.cy
    await page.mouse.click(tx, ty)
  }
  await page.waitForTimeout(4000)

  const frame2 = getWfFrame(page)!
  const afterTriggerClick = await frame2.evaluate(() => document.body?.innerText ?? '')
  console.log('Has trigger list:', afterTriggerClick.includes('Form Submitted'))

  if (!afterTriggerClick.includes('Form Submitted')) {
    console.log('Trigger panel did not open')
    await browser.close()
    return
  }

  console.log('\n=== STEP 2: Click Form Submitted ===')
  const formSubmittedRect = await frame2.evaluate(() => {
    const items = document.querySelectorAll('*')
    for (const item of items) {
      if (item.textContent?.trim() === 'Form Submitted' && item.getBoundingClientRect().width < 300) {
        const r = item.getBoundingClientRect()
        if (r.height > 10 && r.height < 60 && r.y > 200) {
          return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
        }
      }
    }
    return null
  })

  if (!formSubmittedRect) {
    console.log('"Form Submitted" element not found')
    await browser.close()
    return
  }

  const fsx = iframeOffset.x + formSubmittedRect.x
  const fsy = iframeOffset.y + formSubmittedRect.y
  console.log(`Clicking Form Submitted at page coords (${Math.round(fsx)}, ${Math.round(fsy)})`)
  await page.mouse.click(fsx, fsy)
  await page.waitForTimeout(4000)

  const frame3 = getWfFrame(page)!
  const afterFormClick = await frame3.evaluate(() => document.body?.innerText ?? '')
  console.log('Has Save Trigger:', afterFormClick.includes('Save Trigger'))
  console.log('Has config panel:', afterFormClick.includes('CHOOSE A WORKFLOW TRIGGER'))

  console.log('\n=== STEP 3: Click Save Trigger ===')
  const saveTrigRect = await frame3.evaluate(() => {
    const btns = document.querySelectorAll('button')
    for (const btn of btns) {
      if (btn.textContent?.trim() === 'Save Trigger') {
        const r = btn.getBoundingClientRect()
        return { x: r.x + r.width / 2, y: r.y + r.height / 2, w: r.width, h: r.height }
      }
    }
    return null
  })

  if (!saveTrigRect) {
    console.log('Save Trigger button not found')
    await browser.close()
    return
  }

  const stx = iframeOffset.x + saveTrigRect.x
  const sty = iframeOffset.y + saveTrigRect.y
  console.log(`Save Trigger at page coords (${Math.round(stx)}, ${Math.round(sty)}), size ${saveTrigRect.w}x${saveTrigRect.h}`)

  console.log('Checking if button is scrolled into view...')
  const viewportCheck = await frame3.evaluate(() => {
    const btns = document.querySelectorAll('button')
    for (const btn of btns) {
      if (btn.textContent?.trim() === 'Save Trigger') {
        const r = btn.getBoundingClientRect()
        return {
          inViewport: r.top >= 0 && r.bottom <= window.innerHeight && r.left >= 0 && r.right <= window.innerWidth,
          top: r.top, bottom: r.bottom, windowH: window.innerHeight,
        }
      }
    }
    return null
  })
  console.log('Viewport check:', viewportCheck)

  if (viewportCheck && !viewportCheck.inViewport) {
    console.log('Scrolling Save Trigger into view...')
    await frame3.evaluate(() => {
      const btns = document.querySelectorAll('button')
      for (const btn of btns) {
        if (btn.textContent?.trim() === 'Save Trigger') {
          btn.scrollIntoView({ block: 'center' })
          break
        }
      }
    })
    await page.waitForTimeout(500)

    const newRect = await frame3.evaluate(() => {
      const btns = document.querySelectorAll('button')
      for (const btn of btns) {
        if (btn.textContent?.trim() === 'Save Trigger') {
          const r = btn.getBoundingClientRect()
          return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
        }
      }
      return null
    })
    if (newRect) {
      const nx = iframeOffset.x + newRect.x
      const ny = iframeOffset.y + newRect.y
      console.log(`New coords after scroll: (${Math.round(nx)}, ${Math.round(ny)})`)
      await page.mouse.click(nx, ny)
    }
  } else {
    await page.mouse.click(stx, sty)
  }

  console.log('Waiting for save result...')
  await page.waitForTimeout(6000)

  const frame4 = getWfFrame(page)!
  const afterSave = await frame4.evaluate(() => document.body?.innerText ?? '')
  const stillHasSaveBtn = afterSave.includes('Save Trigger')
  const hasTriggerNode = afterSave.includes('Trigger\nForm Submitted') || afterSave.includes('TriggerForm Submitted')

  console.log('\n=== RESULT ===')
  console.log('Save Trigger still visible:', stillHasSaveBtn)
  console.log('Trigger node in flow:', hasTriggerNode)

  if (stillHasSaveBtn) {
    console.log('\nSave failed. Trying alternative: frame.locator click with force...')
    try {
      const saveBtn = frame4.locator('button:has-text("Save Trigger")')
      const box = await saveBtn.boundingBox()
      console.log('Button bounding box:', box)
      if (box) {
        await saveBtn.click({ force: true, timeout: 5000 })
        console.log('Force click succeeded')
        await page.waitForTimeout(5000)
        const frame5 = getWfFrame(page)!
        const final = await frame5.evaluate(() => document.body?.innerText ?? '')
        console.log('After force click - Save visible:', final.includes('Save Trigger'))
      }
    } catch (e) {
      console.log('Force click error:', (e as Error).message.substring(0, 100))
    }
  }

  const nodes = await (getWfFrame(page)!).evaluate(() => {
    return Array.from(document.querySelectorAll('.vue-flow__node')).map(n => n.textContent?.trim() ?? '')
  }).catch(() => [])
  console.log('Final vue-flow nodes:', nodes)

  const addActionExists = await (getWfFrame(page)!).evaluate(() => {
    return !!document.querySelector('.pg-actions__dv--add-action')
  }).catch(() => false)
  console.log('Add Action button exists:', addActionExists)

  await browser.close()
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
