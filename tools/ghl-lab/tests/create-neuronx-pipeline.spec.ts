import { test, expect } from '@playwright/test'
import * as fs from 'fs'

const AUTH_STATE = 'tools/ghl-lab/.ghl-auth-state.json'
const NEURONX_LOCATION_ID = 'oZN1j4944EaIvXoI8rRA'

const STAGES = [
  'New Lead',
  'Qualified',
  'Demo Scheduled',
  'Demo Completed',
  'Proposal Sent',
  'Negotiation',
  'Closed Won',
  'Closed Lost',
]

test('Create NeuronX SaaS Sales Pipeline', async ({ browser }) => {
  const ctx = await browser.newContext({ storageState: AUTH_STATE })
  const page = await ctx.newPage()

  // Navigate to NeuronX sub-account pipelines
  await page.goto(`https://app.gohighlevel.com/location/${NEURONX_LOCATION_ID}/opportunities/pipelines`)
  await page.waitForTimeout(6000)

  // Click "Add Pipeline" button
  const addBtn = page.getByRole('button', { name: /add pipeline/i }).or(
    page.locator('button').filter({ hasText: /add pipeline/i })
  )
  await addBtn.first().click()
  await page.waitForTimeout(2000)

  // Enter pipeline name
  const nameInput = page.getByPlaceholder(/pipeline name/i).or(
    page.locator('input[placeholder*="name" i]').first()
  )
  await nameInput.fill('NeuronX — SaaS Sales')
  await page.waitForTimeout(500)

  // Some GHL versions show a create/save button at this point
  const createBtn = page.getByRole('button', { name: /^create$|^save$|^add$/i })
  if (await createBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
    await createBtn.click()
    await page.waitForTimeout(3000)
  }

  // Now add stages one by one
  for (const stage of STAGES) {
    // Look for "Add Stage" button
    const stageBtn = page.locator('button').filter({ hasText: /add stage/i }).or(
      page.getByRole('button', { name: /add stage/i })
    )
    await stageBtn.first().click({ timeout: 5000 }).catch(() => console.log('No add stage btn visible'))
    await page.waitForTimeout(1000)

    // Fill stage name
    const stageInput = page.locator('input[placeholder*="stage" i]').last().or(
      page.locator('.stage-input, [data-stage-input]').last()
    )
    await stageInput.fill(stage).catch(() => console.log(`Could not fill stage: ${stage}`))
    await page.keyboard.press('Enter')
    await page.waitForTimeout(800)
    console.log(`Added stage: ${stage}`)
  }

  // Save pipeline
  const saveBtn = page.getByRole('button', { name: /save|done|confirm/i }).last()
  if (await saveBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
    await saveBtn.click()
    await page.waitForTimeout(3000)
  }

  // Take screenshot as evidence
  await page.screenshot({ path: 'test-results/neuronx-pipeline-created.png', fullPage: true })
  console.log('✅ Pipeline creation attempted. Check screenshot.')

  await ctx.close()
})
