import { chromium } from 'playwright';

const CDP_ENDPOINT = process.env.CDP_ENDPOINT || 'http://127.0.0.1:9222';

async function testCdpConnection() {
  console.log(`Connecting to CDP endpoint: ${CDP_ENDPOINT}`);

  try {
    const browser = await chromium.connectOverCDP(CDP_ENDPOINT);
    console.log('Connected to browser');
    console.log(`Contexts: ${browser.contexts().length}`);

    const context = browser.contexts()[0];
    if (!context) {
      console.log('No browser context found. Open a tab in Chrome first.');
      return;
    }

    const pages = context.pages();
    console.log(`Pages: ${pages.length}`);
    for (const p of pages) {
      console.log(`  - ${p.url()} (title: ${await p.title()})`);
    }

    const ghlPage = pages.find(p => p.url().includes('gohighlevel.com'));
    if (!ghlPage) {
      console.log('\nNo GHL page found. Navigate to GHL in Chrome first.');
      console.log('Opening GHL dashboard...');
      const newPage = await context.newPage();
      await newPage.goto('https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/dashboard', {
        waitUntil: 'domcontentloaded',
        timeout: 30000,
      });
      await newPage.waitForTimeout(15000);
      console.log(`New page title: ${await newPage.title()}`);
      console.log(`New page URL: ${newPage.url()}`);
    } else {
      console.log(`\nFound GHL page: ${ghlPage.url()}`);
      console.log(`Title: ${await ghlPage.title()}`);

      const frames = ghlPage.frames();
      console.log(`\nFrames on GHL page: ${frames.length}`);
      for (const f of frames) {
        const url = f.url();
        if (url && url !== 'about:blank') {
          console.log(`  - ${url.substring(0, 100)}`);
        }
      }
    }

    console.log('\nCDP connection test PASSED');
  } catch (err: any) {
    if (err.message.includes('ECONNREFUSED')) {
      console.error('\nChrome is not running with remote debugging.');
      console.error('Run: ./tools/ghl-lab/launch-chrome-cdp.sh');
    } else {
      console.error(`Connection failed: ${err.message}`);
    }
    process.exit(1);
  }
}

testCdpConnection();
