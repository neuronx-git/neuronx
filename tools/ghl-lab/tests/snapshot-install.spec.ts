import { test } from '@playwright/test'

test('snapshot install (manual login + guided steps)', async ({ page }) => {
  const loginUrl = process.env.GHL_LOGIN_URL ?? 'https://app.gohighlevel.com/'
  const snapshotShareUrl = process.env.GHL_SNAPSHOT_SHARE_URL

  if (!snapshotShareUrl) {
    throw new Error('Missing GHL_SNAPSHOT_SHARE_URL')
  }

  await page.goto(loginUrl, { waitUntil: 'domcontentloaded' })

  await page.pause()

  await page.goto(snapshotShareUrl, { waitUntil: 'domcontentloaded' })

  await page.pause()
})

