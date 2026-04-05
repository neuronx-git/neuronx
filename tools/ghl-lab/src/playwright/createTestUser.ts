import { chromium } from 'playwright';
import * as path from 'path';

const AUTH_STATE = path.join(__dirname, '../../.ghl-auth-state.json');
const LOCATION_ID = 'FlRL82M0D6nclmKT7eXH';

async function createTestUser() {
  const browser = await chromium.launch({ headless: false, slowMo: 500 });
  const context = await browser.newContext({ storageState: AUTH_STATE });
  const page = await context.newPage();

  console.log('Navigating to team settings...');
  await page.goto(`https://app.gohighlevel.com/v2/location/${LOCATION_ID}/settings/team`, {
    waitUntil: 'domcontentloaded',
    timeout: 60000
  });
  await page.waitForTimeout(8000);

  // Click Add User / Invite
  console.log('Looking for Add User button...');
  const addBtn = await page.locator('button:has-text("Add User"), button:has-text("Invite"), button:has-text("+ Add")').first();
  if (await addBtn.isVisible()) {
    await addBtn.click();
    console.log('Clicked Add User button');
  } else {
    // Try direct navigation
    await page.goto(`https://app.gohighlevel.com/v2/location/${LOCATION_ID}/settings/team/add`, { waitUntil: 'networkidle' });
  }
  await page.waitForTimeout(3000);

  // Take screenshot to see current state
  await page.screenshot({ path: '/tmp/test-user-state.png', fullPage: true });
  console.log('Screenshot saved to /tmp/test-user-state.png');

  // Fill in user details
  const firstNameField = await page.locator('input[placeholder*="First"], input[name*="first"], input[id*="first"]').first();
  if (await firstNameField.isVisible()) {
    await firstNameField.fill('Test');
    console.log('Filled first name');
  }

  const lastNameField = await page.locator('input[placeholder*="Last"], input[name*="last"], input[id*="last"]').first();
  if (await lastNameField.isVisible()) {
    await lastNameField.fill('RCIC');
    console.log('Filled last name');
  }

  const emailField = await page.locator('input[type="email"], input[placeholder*="email"], input[name*="email"]').first();
  if (await emailField.isVisible()) {
    await emailField.fill('test.rcic@visamastercanada.com');
    console.log('Filled email');
  }

  await page.screenshot({ path: '/tmp/test-user-filled.png', fullPage: true });
  console.log('Filled form - screenshot at /tmp/test-user-filled.png');
  console.log('User form filled. Waiting 5s before closing...');
  await page.waitForTimeout(5000);

  await browser.close();
  console.log('Done.');
}

createTestUser().catch(console.error);
