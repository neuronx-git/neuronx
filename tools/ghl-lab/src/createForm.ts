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

async function addFieldViaLocatorDrag(frame: Frame, elementText: string, index: number) {
  console.log(`  [${index}] Adding "${elementText}"...`)

  const source = frame.locator('.gui__builder-card').filter({ hasText: elementText }).first()
  if ((await source.count()) === 0) {
    console.log(`    Source "${elementText}" not found`)
    return false
  }

  await source.scrollIntoViewIfNeeded()
  await new Promise(r => setTimeout(r, 500))

  const target = frame.locator('.smooth-dnd-container.vertical').first()
  if ((await target.count()) === 0) {
    console.log('    Drop target not found')
    return false
  }

  try {
    await source.dragTo(target, { timeout: 10000 })
    console.log('    dragTo completed')
    await new Promise(r => setTimeout(r, 2000))
    return true
  } catch (e: any) {
    console.log('    dragTo failed:', e.message.split('\n')[0])
    return false
  }
}

async function addFieldViaMouseDrag(frame: Frame, page: Page, elementText: string) {
  console.log(`  Trying mouse-based drag for "${elementText}"...`)

  await frame.evaluate((text) => {
    const cards = document.querySelectorAll('.gui__builder-card')
    for (const card of cards) {
      if (card.textContent?.trim() === text) {
        card.scrollIntoView({ block: 'center', behavior: 'instant' })
        return
      }
    }
  }, elementText)
  await page.waitForTimeout(500)

  const sourcePos = await frame.evaluate((text) => {
    const cards = document.querySelectorAll('.gui__builder-card')
    for (const card of cards) {
      if (card.textContent?.trim() === text) {
        const r = card.getBoundingClientRect()
        return { x: r.x + r.width / 2, y: r.y + r.height / 2, visible: r.y >= 0 && r.y < window.innerHeight }
      }
    }
    return null
  }, elementText)

  if (!sourcePos) {
    console.log('    Source not found')
    return false
  }

  const targetPos = await frame.evaluate(() => {
    const container = document.querySelector('.smooth-dnd-container.vertical')
    if (!container) return null
    const r = container.getBoundingClientRect()
    const lastChild = container.lastElementChild
    if (lastChild) {
      const lr = lastChild.getBoundingClientRect()
      return { x: r.x + r.width / 2, y: lr.y + lr.height + 20 }
    }
    return { x: r.x + r.width / 2, y: r.y + r.height / 2 }
  })

  if (!targetPos) {
    console.log('    Target not found')
    return false
  }

  console.log(`    Source: (${Math.round(sourcePos.x)}, ${Math.round(sourcePos.y)}) visible:${sourcePos.visible}`)
  console.log(`    Target: (${Math.round(targetPos.x)}, ${Math.round(targetPos.y)})`)

  const frameElement = await page.locator('iframe').first().elementHandle()
  const iframeBox = await frameElement?.boundingBox()
  const ox = iframeBox?.x ?? 0
  const oy = iframeBox?.y ?? 0

  const sx = ox + sourcePos.x
  const sy = oy + sourcePos.y
  const tx = ox + targetPos.x
  const ty = oy + Math.min(targetPos.y, 700)

  await page.mouse.move(sx, sy)
  await page.waitForTimeout(100)
  await page.mouse.down()
  await page.waitForTimeout(600)

  for (let i = 1; i <= 50; i++) {
    await page.mouse.move(
      sx + (tx - sx) * (i / 50),
      sy + (ty - sy) * (i / 50),
    )
    await page.waitForTimeout(20)
  }

  await page.waitForTimeout(400)
  await page.mouse.up()
  await page.waitForTimeout(2000)

  return true
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
  console.log('Frame found')

  const rendered = await waitForFields(frame)
  console.log('Fields rendered:', rendered)

  const editTab = frame.getByText('Edit', { exact: true })
  if ((await editTab.count()) > 0) {
    await editTab.click()
    await page.waitForTimeout(3000)
  }

  const fieldsToAdd = [
    { type: 'Single Dropdown', label: 'Country of Residence' },
    { type: 'Single Dropdown', label: 'Program Interest' },
    { type: 'Single Dropdown', label: 'Timeline' },
    { type: 'Multi Line', label: 'Notes / Message' },
  ]

  for (let i = 0; i < fieldsToAdd.length; i++) {
    const before = await frame.locator('.smooth-dnd-draggable-wrapper.element-box').count()

    const added = await addFieldViaLocatorDrag(frame, fieldsToAdd[i].type, i)
    let after = await frame.locator('.smooth-dnd-draggable-wrapper.element-box').count()
    console.log(`    locatorDrag: ${before} -> ${after}`)

    if (after <= before) {
      await addFieldViaMouseDrag(frame, page, fieldsToAdd[i].type)
      after = await frame.locator('.smooth-dnd-draggable-wrapper.element-box').count()
      console.log(`    mouseDrag: ${before} -> ${after}`)
    }

    if (after > before) {
      console.log(`  SUCCESS: "${fieldsToAdd[i].label}" added`)
    } else {
      console.log(`  FAILED: Could not add "${fieldsToAdd[i].label}"`)
    }
  }

  const finalCount = await frame.locator('.smooth-dnd-draggable-wrapper.element-box').count()
  console.log('\nFinal field count:', finalCount)

  const fieldList = await frame.evaluate(() => {
    const wrappers = document.querySelectorAll('.smooth-dnd-draggable-wrapper.element-box')
    return Array.from(wrappers).map(w => (w.textContent ?? '').trim().substring(0, 60))
  })
  console.log('Fields:', JSON.stringify(fieldList))

  await frame.getByText('Save', { exact: true }).click()
  await page.waitForTimeout(3000)
  console.log('Saved')

  await browser.close()
}

run().catch((err) => {
  console.error('FATAL:', err.message)
  process.exit(1)
})
