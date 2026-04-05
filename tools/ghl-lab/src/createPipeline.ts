import { chromium } from 'playwright'

const AUTH = '/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json'
const LOC = 'FlRL82M0D6nclmKT7eXH'
const PIPELINE_NAME = 'NeuronX \u2014 Immigration Intake'
const STAGES = [
  'NEW',
  'CONTACTING',
  'UNREACHABLE',
  'CONSULT READY',
  'BOOKED',
  'CONSULT COMPLETED',
  'RETAINED',
  'LOST',
  'NURTURE',
]

async function run() {
  const browser = await chromium.launch({ headless: false })
  const context = await browser.newContext({
    storageState: AUTH,
    viewport: { width: 1440, height: 900 },
  })
  const page = await context.newPage()

  console.log('Navigating to Opportunities...')
  await page.goto(
    `https://app.gohighlevel.com/v2/location/${LOC}/opportunities/list`,
    { waitUntil: 'domcontentloaded', timeout: 60000 },
  )

  console.log('Waiting for page to fully render...')
  await page.waitForTimeout(15000)

  const bodyText = await page.evaluate(() => document.body?.innerText ?? '')
  console.log('Page text (first 800):', bodyText.substring(0, 800))

  if (bodyText.includes(PIPELINE_NAME)) {
    console.log('Pipeline already exists. Skipping creation.')
    await browser.close()
    process.exit(0)
  }

  console.log('Step 1: Opening Create Pipeline modal...')
  const createNewBtn = page.getByText('Create New Pipeline', { exact: true })
  const createPipelineBtn = page.getByText('Create Pipeline').first()

  if ((await createNewBtn.count()) > 0) {
    console.log('  Found "Create New Pipeline" button')
    await createNewBtn.click()
  } else if ((await createPipelineBtn.count()) > 0) {
    console.log('  Found "Create Pipeline" button')
    await createPipelineBtn.click()
  } else {
    console.log('  No create button found. Looking for alternative...')
    const allBtns = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('button, [role=button]'))
        .filter(b => b.getBoundingClientRect().width > 0)
        .map(b => (b.textContent ?? '').trim().substring(0, 60))
    })
    console.log('  Available buttons:', JSON.stringify(allBtns))
    await browser.close()
    process.exit(1)
  }
  await page.waitForTimeout(4000)

  console.log('Step 2: Filling pipeline name...')
  const nameInput = page.locator('input[placeholder="Marketing pipeline"]')
  await nameInput.waitFor({ timeout: 5000 })
  await nameInput.click()
  await nameInput.fill(PIPELINE_NAME)
  await page.waitForTimeout(500)
  console.log('  Name:', PIPELINE_NAME)

  console.log('Step 3: Renaming existing stages...')
  const stageSelector = 'input[placeholder="Enter stage name"]'
  let stageInputs = page.locator(stageSelector)
  let count = await stageInputs.count()
  console.log(`  Found ${count} default stages`)

  for (let i = 0; i < Math.min(count, STAGES.length); i++) {
    const input = stageInputs.nth(i)
    await input.click({ clickCount: 3 })
    await input.fill(STAGES[i])
    await page.waitForTimeout(300)
    console.log(`  Stage ${i + 1}: ${STAGES[i]}`)
  }

  console.log('Step 4: Adding remaining stages...')
  for (let i = count; i < STAGES.length; i++) {
    const addBtn = page.getByText('Add stage', { exact: true })
    await addBtn.click()
    await page.waitForTimeout(800)

    const allInputs = page.locator(stageSelector)
    const newCount = await allInputs.count()
    const lastInput = allInputs.nth(newCount - 1)
    await lastInput.fill(STAGES[i])
    await page.waitForTimeout(300)
    console.log(`  Stage ${i + 1}: ${STAGES[i]}`)
  }

  console.log('Step 5: Verifying all stages...')
  const allStages = page.locator(stageSelector)
  const total = await allStages.count()
  console.log(`  Total stages: ${total}`)
  for (let i = 0; i < total; i++) {
    const val = await allStages.nth(i).inputValue()
    console.log(`  [${i + 1}] ${val}`)
  }

  console.log('Step 6: Clicking Create...')
  await page.waitForTimeout(1000)

  const createBtn = page.locator('button').filter({ hasText: /^Create$/ }).last()
  const btnClasses = await createBtn.getAttribute('class')
  const isDisabled = btnClasses?.includes('disabled') ?? false
  console.log(`  Disabled: ${isDisabled}`)

  if (isDisabled) {
    console.log('  ERROR: Create button is disabled. Dumping page state...')
    const text = await page.evaluate(() => document.body?.innerText?.substring(0, 2000) ?? '')
    console.log(text)
    await browser.close()
    process.exit(1)
  }

  await createBtn.click()
  await page.waitForTimeout(5000)
  console.log('  Clicked Create')
  console.log('  URL:', page.url())

  const finalText = await page.evaluate(() => document.body?.innerText?.substring(0, 3000) ?? '')
  const success = finalText.includes(PIPELINE_NAME) || finalText.includes('Immigration Intake')
  console.log(`  Pipeline visible: ${success}`)
  console.log('  Body snippet:', finalText.substring(0, 600))

  await browser.close()

  if (success) {
    console.log('\nBLOCK 2 COMPLETE: Pipeline created successfully')
    process.exit(0)
  } else {
    console.log('\nBLOCK 2 UNCERTAIN: Check GHL manually')
    process.exit(1)
  }
}

run().catch((err) => {
  console.error('FATAL:', err.message)
  process.exit(1)
})
