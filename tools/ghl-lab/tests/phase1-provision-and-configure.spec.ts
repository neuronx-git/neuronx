import { test } from '@playwright/test'

function requireEnv(name: string): string {
  const v = process.env[name]
  if (!v) throw new Error(`Missing ${name}`)
  return v
}

test('Phase 1/2 GHL build (guided automation)', async ({ page }) => {
  const loginUrl = process.env.GHL_LOGIN_URL ?? 'https://app.gohighlevel.com/'
  const locationId = process.env.GHL_LOCATION_ID

  console.log('Open login URL:', loginUrl)
  console.log('This run is guided: it pauses for login/2FA and for UI steps that are not reliably automatable via public APIs.')

  await page.goto(loginUrl, { waitUntil: 'domcontentloaded' })

  console.log('\nACTION REQUIRED (Login):')
  console.log('- Log into HighLevel in the opened browser.')
  console.log('- Complete any 2FA/CAPTCHA if prompted.')
  console.log('- When you see the main HighLevel app, resume the script.')
  await page.pause()

  if (!locationId) {
    console.log('\nACTION REQUIRED (Provision sub-account):')
    console.log('- Switch to Agency view.')
    console.log('- Create a new sub-account named: "NeuronX Test Lab".')
    console.log('- Copy the Location ID (or open the sub-account so the URL contains /location/<id>).')
    console.log('- Stop this run, set env GHL_LOCATION_ID=<id>, then rerun this test.')
    await page.pause()
    return
  }

  const locationDashboardUrl = `https://app.gohighlevel.com/location/${locationId}/dashboard`
  console.log('\nNavigating to Location dashboard:', locationDashboardUrl)
  await page.goto(locationDashboardUrl, { waitUntil: 'domcontentloaded' })

  console.log('\nACTION REQUIRED (Phase 2 build inside GHL):')
  console.log('- Follow the exact build steps in /docs/02_operating_system/ghl_configuration_blueprint.md')
  console.log('- Build: funnel/page, form, pipeline stages, custom fields, tags, calendar, workflows WF-01..WF-11')
  console.log('- Keep this browser session open while you configure; resume between major milestones.')

  console.log('\nMilestone 1: Pipeline + stages created. Then resume.')
  await page.pause()

  console.log('\nMilestone 2: Custom fields + tags created. Then resume.')
  await page.pause()

  console.log('\nMilestone 3: Calendar + booking link created. Then resume.')
  await page.pause()

  console.log('\nMilestone 4: Form created + attached to landing page. Then resume.')
  await page.pause()

  console.log('\nMilestone 5: Workflows WF-01..WF-11 created. Then resume.')
  await page.pause()

  console.log('\nPhase 2 complete. Next: create Snapshot from this sub-account (Phase 3).')
})

