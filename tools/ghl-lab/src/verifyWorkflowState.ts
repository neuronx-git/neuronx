import { chromium, Page, Frame } from 'playwright'

const AUTH = '/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json'
const LOC = 'FlRL82M0D6nclmKT7eXH'

const NAMES = [
  'WF-01 New Inquiry Acknowledge',
  'WF-02 Contact Attempt Sequence',
  'WF-03 Mark Contacted Readiness',
  'WF-04 Readiness Complete Invite Booking',
  'WF-05 Appointment Booked Reminders',
  'WF-06 No-Show Recovery',
  'WF-07 Consultation Outcome Capture',
  'WF-08 Outcome Routing',
  'WF-09 Retainer Follow-Up',
  'WF-10 Post-Consult Follow-Up',
  'WF-11 Nurture Campaign Monthly',
]

function getWfFrame(page: Page): Frame | null {
  return page.frames().find(f => f.url().includes('client-app-automation-workflows')) ?? null
}

async function waitForWfFrame(page: Page): Promise<Frame | null> {
  for (let i = 0; i < 15; i++) {
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

  const results: { name: string; nodes: string[]; hasTrigger: boolean; actionCount: number; hasAddAction: boolean }[] = []

  for (let i = 0; i < NAMES.length; i++) {
    const name = NAMES[i]
    console.log(`\n[${i + 1}/11] Checking ${name}...`)

    await page.goto(
      `https://app.gohighlevel.com/v2/location/${LOC}/automation/workflows`,
      { waitUntil: 'domcontentloaded', timeout: 60000 },
    )
    const lf = await waitForWfFrame(page)
    if (!lf) { console.log('  List frame not found'); continue }

    let link = lf.getByText(name)
    if ((await link.count()) === 0) {
      for (const sel of ['button[aria-label="forward"]', 'button:has-text("›")']) {
        const btn = lf.locator(sel)
        if ((await btn.count()) > 0) { await btn.first().click(); await page.waitForTimeout(5000); break }
      }
      link = lf.getByText(name)
    }
    if ((await link.count()) === 0) { console.log('  Not found'); continue }

    await link.first().click()
    await page.waitForTimeout(12000)
    await page.keyboard.press('Escape')
    await page.waitForTimeout(1000)

    const frame = getWfFrame(page)
    if (!frame) { console.log('  Frame lost'); continue }

    const nodes = await frame.evaluate(() =>
      Array.from(document.querySelectorAll('.vue-flow__node')).map(n => (n.textContent ?? '').trim().substring(0, 60))
    )
    const hasTrigger = nodes.some(n =>
      n.includes('Form Submitted') || n.includes('Contact Tag') || n.includes('Appointment')
      || n.includes('Customer Booked') || n.includes('Contact Changed')
    )
    const actionNodes = nodes.filter(n =>
      n.includes('Add Contact Tag') || n.includes('Send SMS') || n.includes('Send Email')
      || n.includes('Create Task') || n.includes('Wait')
    )
    const hasAddAction = await frame.evaluate(() => !!document.querySelector('.pg-actions__dv--add-action'))

    console.log(`  Trigger: ${hasTrigger ? 'YES' : 'NO'}`)
    console.log(`  Actions: ${actionNodes.length}`)
    console.log(`  Nodes: ${nodes.join(' | ')}`)

    results.push({ name, nodes, hasTrigger, actionCount: actionNodes.length, hasAddAction })
  }

  console.log('\n=== SUMMARY ===')
  let totalTriggers = 0, totalActions = 0
  for (const r of results) {
    if (r.hasTrigger) totalTriggers++
    totalActions += r.actionCount
    console.log(`${r.hasTrigger ? '✓' : '✗'} ${r.name}: trigger=${r.hasTrigger}, actions=${r.actionCount}`)
  }
  console.log(`\nTriggers: ${totalTriggers}/11, Actions: ${totalActions}`)

  await browser.close()
}

run().catch(err => { console.error('FATAL:', err.message); process.exit(1) })
