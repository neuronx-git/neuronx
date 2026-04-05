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

async function openWorkflow(page: Page, name: string): Promise<Frame | null> {
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )
  const lf = await waitForWfFrame(page)
  if (!lf) return null

  let link = lf.getByText(name)
  if ((await link.count()) === 0) {
    const paginators = [
      lf.locator('button[aria-label="forward"]'),
      lf.locator('button[aria-label="next"]'),
      lf.locator('[class*=pagination] button:last-child'),
      lf.locator('button:has-text("›")'),
      lf.locator('button:has-text("Next")'),
    ]
    for (const p of paginators) {
      if ((await p.count()) > 0) {
        await p.first().click()
        await page.waitForTimeout(5000)
        link = lf.getByText(name)
        if ((await link.count()) > 0) break
      }
    }
  }
  if ((await link.count()) === 0) {
    console.log(`  "${name}" not found on any page`)
    return null
  }

  await link.first().click()
  await page.waitForTimeout(15000)
  await page.keyboard.press('Escape')
  await page.waitForTimeout(2000)

  const frame = getWfFrame(page)
  if (!frame) return null

  const bt = frame.locator('[data-name="builder"]')
  if ((await bt.count()) > 0) await bt.first().click({ force: true })
  await page.waitForTimeout(2000)

  return frame
}

async function setTrigger(page: Page, frame: Frame, triggerName: string): Promise<boolean> {
  const nodes = await frame.evaluate(() =>
    Array.from(document.querySelectorAll('.vue-flow__node')).map(n => n.textContent?.trim() ?? '')
  )
  const hasAddNewTrigger = nodes.some(n => n.includes('Add New Trigger'))
  const hasTriggerNode = nodes.some(n =>
    n.includes('Form Submitted') || n.includes('Contact Tag')
    || n.includes('Appointment Status') || n.includes('Customer Booked')
    || n.includes('Contact Changed')
  )

  if (hasTriggerNode) {
    console.log('    Trigger already set')
    return true
  }

  if (!hasAddNewTrigger) {
    console.log('    No trigger nodes found at all. Nodes:', nodes)
    return false
  }

  const trigNode = frame.locator('[data-id="add-new-trigger"]')
  if ((await trigNode.count()) === 0) {
    console.log('    [data-id=add-new-trigger] not found')
    return false
  }

  try {
    await trigNode.click({ timeout: 5000 })
  } catch {
    try {
      await trigNode.click({ force: true, timeout: 5000 })
    } catch {
      console.log('    Trigger node click failed completely')
      return false
    }
  }
  await page.waitForTimeout(3000)

  const text = await frame.evaluate(() => document.body?.innerText ?? '')
  if (!text.includes('Search For Triggers')) {
    console.log('    Trigger panel did not open, retrying...')
    const rect = await frame.evaluate(() => {
      const el = document.querySelector('[data-id="add-new-trigger"]') as HTMLElement
      if (!el) return null
      const r = el.getBoundingClientRect()
      return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
    })
    if (rect) {
      await page.mouse.click(rect.x, rect.y)
      await page.waitForTimeout(3000)
    }
    const text2 = await frame.evaluate(() => document.body?.innerText ?? '')
    if (!text2.includes('Search For Triggers')) {
      console.log('    Trigger panel still did not open')
      return false
    }
  }

  const opt = frame.getByText(triggerName, { exact: true }).first()
  if ((await opt.count()) === 0) return false
  await opt.click()
  await page.waitForTimeout(3000)

  const saveBtn = frame.locator('button').filter({ hasText: 'Save Trigger' })
  if ((await saveBtn.count()) > 0) {
    const rect = await frame.evaluate(() => {
      const b = Array.from(document.querySelectorAll('button')).find(b => b.textContent?.trim() === 'Save Trigger')
      if (!b) return null
      const r = b.getBoundingClientRect()
      return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
    })
    if (rect) {
      await page.mouse.click(rect.x, rect.y)
      await page.waitForTimeout(5000)
    }
  }

  const afterNodes = await frame.evaluate(() =>
    Array.from(document.querySelectorAll('.vue-flow__node')).map(n => n.textContent?.trim() ?? '')
  )
  const saved = afterNodes.some(n => n.includes('Trigger') && !n.includes('Add New Trigger'))
  console.log('    Trigger saved:', saved)
  return saved
}

async function addAction(page: Page, frame: Frame, actionName: string): Promise<boolean> {
  await frame.evaluate(() => {
    const fitBtn = document.querySelector('[data-testid="fit-view-button"], button[title*="Fit"], .vue-flow__controls button:nth-child(3)')
    if (fitBtn) (fitBtn as HTMLElement).click()
  })
  await page.waitForTimeout(1000)

  let plusRect = await frame.evaluate(() => {
    const all = document.querySelectorAll('.pg-actions__dv--add-action')
    const last = all[all.length - 1]
    if (!last) return null
    last.scrollIntoView({ block: 'center' })
    const r = last.getBoundingClientRect()
    if (r.width > 0 && r.y > 0 && r.y < window.innerHeight) {
      return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
    }
    return null
  })

  if (!plusRect) {
    await frame.evaluate(() => {
      const viewport = document.querySelector('.vue-flow__transformationpane') as HTMLElement
      if (viewport) {
        const currentTransform = viewport.style.transform
        const match = currentTransform.match(/translate\(([-\d.]+)px,\s*([-\d.]+)px\)\s*scale\(([-\d.]+)\)/)
        if (match) {
          const [, x, y, s] = match
          const newScale = Math.max(0.3, parseFloat(s) * 0.6)
          viewport.style.transform = `translate(${x}px, ${y}px) scale(${newScale})`
        }
      }
    })
    await page.waitForTimeout(500)

    plusRect = await frame.evaluate(() => {
      const all = document.querySelectorAll('.pg-actions__dv--add-action')
      const last = all[all.length - 1]
      if (!last) return null
      const r = last.getBoundingClientRect()
      if (r.width > 0) return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
      return null
    })
  }

  if (!plusRect) {
    console.log(`    No + button for action "${actionName}"`)
    return false
  }

  await page.mouse.click(plusRect.x, plusRect.y)
  await page.waitForTimeout(3000)

  const text = await frame.evaluate(() => document.body?.innerText ?? '')
  if (!text.includes('Search For Actions')) {
    await frame.evaluate(() => {
      const d = document.querySelector('.pg-actions__dv--add-action')
      if (d) {
        const btn = d.querySelector('button') || d
        ;(btn as HTMLElement).dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))
        ;(btn as HTMLElement).dispatchEvent(new PointerEvent('pointerup', { bubbles: true }))
        ;(btn as HTMLElement).dispatchEvent(new MouseEvent('click', { bubbles: true }))
      }
    })
    await page.waitForTimeout(3000)
  }

  const text2 = await frame.evaluate(() => document.body?.innerText ?? '')
  if (!text2.includes('Search For Actions')) {
    console.log(`    Action panel did not open for "${actionName}"`)
    return false
  }

  const search = frame.locator('input[placeholder*="Search" i]')
  if ((await search.count()) > 0) {
    await search.fill(actionName)
    await page.waitForTimeout(2000)
  }

  let opt = frame.getByText(actionName, { exact: true }).first()
  if ((await opt.count()) === 0) {
    opt = frame.locator(`text="${actionName}"`).first()
  }
  if ((await opt.count()) === 0) {
    opt = frame.locator(`*:has-text("${actionName}")`).first()
  }
  if ((await opt.count()) === 0) {
    const match = await frame.evaluate((name) => {
      const els = document.querySelectorAll('*')
      for (const el of els) {
        if (el.children.length === 0 && el.textContent?.trim() === name) {
          const r = el.getBoundingClientRect()
          if (r.width > 0 && r.height > 10 && r.height < 60) return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
        }
      }
      return null
    }, actionName)
    if (match) {
      await page.mouse.click(match.x, match.y)
      await page.waitForTimeout(3000)
      const saveR = await frame.evaluate(() => {
        const b = Array.from(document.querySelectorAll('button')).find(b => b.textContent?.trim() === 'Save Action')
        if (!b) return null
        const r = b.getBoundingClientRect()
        return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
      })
      if (saveR) { await page.mouse.click(saveR.x, saveR.y); await page.waitForTimeout(3000) }
      return true
    }
    console.log(`    Action "${actionName}" not found at all`)
    await page.keyboard.press('Escape')
    await page.waitForTimeout(1000)
    return false
  }

  await opt.click()
  await page.waitForTimeout(3000)

  const saveRect = await frame.evaluate(() => {
    const b = Array.from(document.querySelectorAll('button')).find(b => b.textContent?.trim() === 'Save Action')
    if (!b) return null
    const r = b.getBoundingClientRect()
    return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
  })
  if (saveRect) {
    await page.mouse.click(saveRect.x, saveRect.y)
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

  let triggersDone = 0
  let actionsDone = 0

  for (let i = 0; i < CONFIGS.length; i++) {
    const cfg = CONFIGS[i]
    console.log(`\n=== [${i + 1}/11] ${cfg.name} ===`)

    const frame = await openWorkflow(page, cfg.name)
    if (!frame) {
      console.log('  SKIP: Could not open')
      continue
    }

    const trigOk = await setTrigger(page, frame, cfg.trigger)
    if (trigOk) triggersDone++

    const freshFrame = getWfFrame(page)!
    let actCount = 0
    for (const act of cfg.actions) {
      const ok = await addAction(page, freshFrame, act)
      if (ok) { actCount++; console.log(`    + ${act}`) }
      else console.log(`    - ${act} (failed)`)
    }
    actionsDone += actCount
    console.log(`  Actions: ${actCount}/${cfg.actions.length}`)
  }

  console.log(`\n=== DONE: Triggers ${triggersDone}/11, Actions ${actionsDone} total ===`)
  await browser.close()
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
