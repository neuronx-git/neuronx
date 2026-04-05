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

async function openWorkflow(page: Page, wfName: string): Promise<Frame | null> {
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )
  const listFrame = await waitForWfFrame(page)
  if (!listFrame) return null

  let link = listFrame.getByText(wfName)
  if ((await link.count()) === 0) {
    const nextBtn = listFrame.locator('button[aria-label="forward"]')
    if ((await nextBtn.count()) > 0) {
      await nextBtn.click()
      await page.waitForTimeout(5000)
      link = listFrame.getByText(wfName)
    }
  }
  if ((await link.count()) === 0) return null

  await link.first().click()
  await page.waitForTimeout(12000)
  await page.keyboard.press('Escape')
  await page.waitForTimeout(1000)

  const frame = getWfFrame(page)
  if (frame) {
    const builderTab = frame.locator('[data-name="builder"]')
    if ((await builderTab.count()) > 0) {
      await builderTab.first().click()
      await page.waitForTimeout(2000)
    }
  }
  return frame
}

async function addTriggerAndSave(frame: Frame, page: Page, triggerType: string): Promise<boolean> {
  const triggerNode = frame.locator('[data-id="add-new-trigger"]')
  if ((await triggerNode.count()) === 0) return false

  const clicked = await frame.evaluate(() => {
    const node = document.querySelector('[data-id="add-new-trigger"]') as HTMLElement
    if (!node) return false
    node.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }))
    return true
  })
  if (!clicked) return false
  await page.waitForTimeout(3000)

  let bodyText = await frame.evaluate(() => document.body?.innerText ?? '')
  if (!bodyText.includes('Search For Triggers') && !bodyText.includes('Add Trigger')) {
    await triggerNode.click({ force: true, timeout: 5000 }).catch(() => {})
    await page.waitForTimeout(3000)
    bodyText = await frame.evaluate(() => document.body?.innerText ?? '')
    if (!bodyText.includes('Search For Triggers') && !bodyText.includes('Add Trigger')) {
      console.log('    Trigger panel did not open')
      return false
    }
  }

  const option = frame.getByText(triggerType, { exact: true }).first()
  if ((await option.count()) === 0) {
    console.log(`    Trigger "${triggerType}" not found`)
    await page.keyboard.press('Escape')
    return false
  }

  await option.click()
  await page.waitForTimeout(3000)

  const saveBtnRect = await frame.evaluate(() => {
    const btn = document.querySelector('.pg-actions__btn--save-trig') as HTMLElement
    if (!btn) {
      const allBtns = Array.from(document.querySelectorAll('button'))
      const save = allBtns.find(b => b.textContent?.trim() === 'Save Trigger')
      if (save) {
        const r = save.getBoundingClientRect()
        return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
      }
      return null
    }
    const r = btn.getBoundingClientRect()
    return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
  })

  if (saveBtnRect) {
    await frame.evaluate(() => {
      const btn = document.querySelector('.pg-actions__btn--save-trig') as HTMLElement
      if (btn) btn.scrollIntoView({ block: 'center' })
      const allBtns = Array.from(document.querySelectorAll('button'))
      const save = allBtns.find(b => b.textContent?.trim() === 'Save Trigger')
      if (save) save.scrollIntoView({ block: 'center' })
    })
    await page.waitForTimeout(500)

    const updatedRect = await frame.evaluate(() => {
      const btn = document.querySelector('.pg-actions__btn--save-trig') as HTMLElement
      if (!btn) {
        const allBtns = Array.from(document.querySelectorAll('button'))
        const save = allBtns.find(b => b.textContent?.trim() === 'Save Trigger')
        if (save) {
          const r = save.getBoundingClientRect()
          return { x: r.x + r.width / 2, y: r.y + r.height / 2, visible: r.y > 0 && r.y < window.innerHeight }
        }
        return null
      }
      const r = btn.getBoundingClientRect()
      return { x: r.x + r.width / 2, y: r.y + r.height / 2, visible: r.y > 0 && r.y < window.innerHeight }
    })

    if (updatedRect) {
      const allIframes = await page.locator('iframe').all()
      let wfIframe = null
      for (const iframe of allIframes) {
        const src = await iframe.getAttribute('src').catch(() => '')
        if (src?.includes('automation-workflows')) {
          wfIframe = iframe
          break
        }
      }
      const iframeBox2 = wfIframe ? await wfIframe.boundingBox() : await page.locator('iframe').first().boundingBox()
      const ox2 = iframeBox2?.x ?? 0
      const oy2 = iframeBox2?.y ?? 0
      console.log(`    Iframe at (${ox2}, ${oy2}) size: ${iframeBox2?.width}x${iframeBox2?.height}`)
      const cx = ox2 + updatedRect.x
      const cy = oy2 + updatedRect.y
      console.log(`    Save Trigger at (${Math.round(cx)}, ${Math.round(cy)}) visible:${updatedRect.visible}`)

      await page.mouse.move(cx, cy)
      await page.waitForTimeout(200)
      await page.mouse.down()
      await page.waitForTimeout(100)
      await page.mouse.up()
      console.log('    Mouse down/up at Save Trigger')
      await page.waitForTimeout(5000)

      let savedOk = await frame.evaluate(() => {
        return !document.querySelector('.pg-actions__btn--save-trig')
      })
      if (!savedOk) {
        console.log('    Save didnt work, trying keyboard Enter...')
        await page.keyboard.press('Tab')
        await page.waitForTimeout(300)
        await page.keyboard.press('Enter')
        await page.waitForTimeout(5000)
        savedOk = await frame.evaluate(() => {
          return !document.querySelector('.pg-actions__btn--save-trig')
        })
      }
      if (!savedOk) {
        console.log('    Trying dispatchEvent chain...')
        await frame.evaluate(() => {
          const btn = document.querySelector('.pg-actions__btn--save-trig') as HTMLElement
          if (btn) {
            const events = ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click']
            for (const evt of events) {
              btn.dispatchEvent(new PointerEvent(evt, { bubbles: true, cancelable: true, composed: true }))
            }
          }
        })
        await page.waitForTimeout(5000)
      }
      console.log('    Save trigger final check')

      const afterSaveNodes = await frame.evaluate(() => {
        return Array.from(document.querySelectorAll('.vue-flow__node')).map(n => n.textContent?.trim() ?? '')
      })
      console.log('    Nodes after save:', afterSaveNodes)
    }
  } else {
    console.log('    Save Trigger button not found')
  }

  const addActionAppeared = await frame.evaluate(() => {
    return !!document.querySelector('.pg-actions__dv--add-action')
  })
  console.log('    + button appeared:', addActionAppeared)

  if (!addActionAppeared) {
    const allNodeText = await frame.evaluate(() => {
      return Array.from(document.querySelectorAll('.vue-flow__node'))
        .map(n => n.textContent?.trim() ?? '')
    })
    console.log('    Nodes after save:', allNodeText)
    const hasTrigger = allNodeText.some(n => n.includes('Trigger'))
    console.log('    Trigger node exists:', hasTrigger)

    const allDivClasses = await frame.evaluate(() => {
      return Array.from(document.querySelectorAll('[class*=pg-actions], [class*=add-action], [class*=plus]'))
        .map(el => ({
          cls: (el.className ?? '').toString().substring(0, 80),
          visible: el.getBoundingClientRect().width > 0,
        }))
    })
    console.log('    Action-related divs:', JSON.stringify(allDivClasses))
  }

  return true
}

async function addActionAndSave(frame: Frame, page: Page, actionName: string): Promise<boolean> {
  const iframeBox = await page.locator('iframe').first().boundingBox()
  const ox = iframeBox?.x ?? 0
  const oy = iframeBox?.y ?? 0

  const btnPos = await frame.evaluate(() => {
    const addDiv = document.querySelector('.pg-actions__dv--add-action')
    if (addDiv) {
      const rect = addDiv.getBoundingClientRect()
      return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 }
    }
    return null
  })

  if (btnPos) {
    await page.mouse.move(ox + btnPos.x, oy + btnPos.y)
    await page.waitForTimeout(500)
    await page.mouse.click(ox + btnPos.x, oy + btnPos.y)
    await page.waitForTimeout(3000)
  }

  const panelCheck = await frame.evaluate(() => document.body?.innerText?.includes('Search For Actions') ?? false)
  if (!panelCheck) {
    const clicked = await frame.evaluate(() => {
      const addDiv = document.querySelector('.pg-actions__dv--add-action')
      if (addDiv) {
        const btn = addDiv.querySelector('button') || addDiv
        ;(btn as HTMLElement).dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))
        ;(btn as HTMLElement).dispatchEvent(new PointerEvent('pointerup', { bubbles: true }))
        ;(btn as HTMLElement).dispatchEvent(new MouseEvent('click', { bubbles: true }))
        return true
      }
      return false
    })
    if (!clicked) {
      console.log('    + button not found in DOM')
      return false
    }
    await page.waitForTimeout(3000)
  }

  const panelText = await frame.evaluate(() => document.body?.innerText ?? '')
  if (!panelText.includes('Search For Actions') && !panelText.includes('Actions')) {
    console.log('    Action panel did not open')
    return false
  }

  const searchInput = frame.locator('input[placeholder*="Search" i]')
  if ((await searchInput.count()) > 0) {
    await searchInput.fill(actionName)
    await page.waitForTimeout(1500)
  }

  const option = frame.getByText(actionName, { exact: true }).first()
  if ((await option.count()) === 0) {
    console.log(`    Action "${actionName}" not in list`)
    await page.keyboard.press('Escape')
    await page.waitForTimeout(1000)
    return false
  }

  await option.click()
  await page.waitForTimeout(3000)

  const saveBtn = frame.getByText('Save Action', { exact: true })
  if ((await saveBtn.count()) > 0) {
    await saveBtn.click()
    await page.waitForTimeout(3000)
  }

  return true
}

interface WfConfig {
  name: string
  trigger: string
  actions: string[]
}

const CONFIGS: WfConfig[] = [
  { name: 'WF-01 New Inquiry Acknowledge', trigger: 'Form Submitted', actions: ['Add Contact Tag', 'Send SMS', 'Send Email', 'Add Contact Tag'] },
  { name: 'WF-02 Contact Attempt Sequence', trigger: 'Contact Tag', actions: ['Create Task', 'Wait', 'Send SMS', 'Wait', 'Create Task'] },
  { name: 'WF-03 Mark Contacted Readiness', trigger: 'Contact Tag', actions: ['Add Contact Tag', 'Create Task'] },
  { name: 'WF-04 Readiness Complete Invite Booking', trigger: 'Contact Tag', actions: ['Add Contact Tag', 'Send SMS', 'Send Email'] },
  { name: 'WF-05 Appointment Booked Reminders', trigger: 'Customer Booked Appointment', actions: ['Add Contact Tag', 'Send SMS', 'Send Email'] },
  { name: 'WF-06 No-Show Recovery', trigger: 'Appointment Status', actions: ['Add Contact Tag', 'Send SMS', 'Wait', 'Create Task'] },
  { name: 'WF-07 Consultation Outcome Capture', trigger: 'Appointment Status', actions: ['Create Task', 'Wait'] },
  { name: 'WF-08 Outcome Routing', trigger: 'Contact Changed', actions: ['Add Contact Tag'] },
  { name: 'WF-09 Retainer Follow-Up', trigger: 'Contact Tag', actions: ['Send Email', 'Wait', 'Send SMS'] },
  { name: 'WF-10 Post-Consult Follow-Up', trigger: 'Contact Tag', actions: ['Send Email', 'Wait', 'Send SMS'] },
  { name: 'WF-11 Nurture Campaign Monthly', trigger: 'Contact Tag', actions: ['Send Email'] },
]

async function run() {
  const browser = await chromium.launch({ headless: false })
  const ctx = await browser.newContext({ storageState: AUTH, viewport: { width: 1440, height: 900 } })
  const page = await ctx.newPage()

  let configured = 0

  for (let i = 0; i < CONFIGS.length; i++) {
    const cfg = CONFIGS[i]
    console.log(`\n=== [${i + 1}/11] ${cfg.name} ===`)

    const frame = await openWorkflow(page, cfg.name)
    if (!frame) {
      console.log('  SKIP: Could not open')
      continue
    }

    const nodes = await frame.evaluate(() => {
      return Array.from(document.querySelectorAll('.vue-flow__node')).map(n => n.textContent?.trim() ?? '')
    })
    const hasTriggerNode = nodes.some(n => n.includes('Trigger') && (n.includes('Form Submitted') || n.includes('Contact Tag') || n.includes('Appointment') || n.includes('Customer Booked') || n.includes('Contact Changed')))
    const hasEmptyTrigger = !hasTriggerNode

    if (!hasEmptyTrigger) {
      console.log('  Trigger already configured')
    } else {
      console.log(`  Setting trigger: ${cfg.trigger}`)
      const ok = await addTriggerAndSave(frame, page, cfg.trigger)
      if (!ok) {
        console.log('  Trigger FAILED')
        continue
      }
      console.log('  Trigger saved')
    }

    let addedActions = 0
    for (const action of cfg.actions) {
      const ok = await addActionAndSave(frame, page, action)
      if (ok) {
        addedActions++
        console.log(`    + ${action}`)
      } else {
        console.log(`    - ${action} (failed)`)
      }
    }

    console.log(`  Actions: ${addedActions}/${cfg.actions.length}`)
    configured++
  }

  console.log(`\n=== Configured ${configured}/11 workflows ===`)
  await browser.close()
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
