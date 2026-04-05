import 'dotenv/config';
import { BrowserUse } from 'browser-use-sdk';

const API_KEY = process.env.BROWSER_USE_API_KEY;
if (!API_KEY) {
  console.error('BROWSER_USE_API_KEY not set. Add it to tools/ghl-lab/.env');
  process.exit(1);
}

const client = new BrowserUse({ apiKey: API_KEY });

async function setup() {
  console.log('=== Browser-Use Cloud Setup ===\n');

  console.log('1. Checking account...');
  try {
    // const account = await client.billing.getAccount();
    // console.log(`   Total credits: $${account.totalCreditsBalanceUsd}`);
    console.log('   (Billing check skipped)');
  } catch (err: any) {
    console.log(`   Error: ${err.message?.substring(0, 200)}`);
  }

  console.log('\n2. Listing existing profiles...');
  try {
    const profiles = await client.profiles.list();
    const items = profiles.profiles || [];
    console.log(`   Found ${items.length} profiles`);
    for (const p of items) {
      console.log(`   - ${p.id} | ${p.name || '(no name)'} | created: ${p.createdAt || 'unknown'}`);
    }
  } catch (err: any) {
    console.log(`   Error: ${err.message?.substring(0, 200)}`);
  }

  console.log('\n3. Creating GHL browser profile...');
  try {
    const profile = await client.profiles.create({
      name: 'GHL NeuronX Test Lab',
    });
    console.log(`   Profile ID: ${profile.id}`);
    console.log(`   Name: ${profile.name}`);
    console.log('\n   *** NEXT STEP: Sync GHL cookies to this profile ***');
    console.log('   Run in terminal:');
    console.log(`   export BROWSER_USE_API_KEY="${API_KEY}"`);
    console.log('   curl -fsSL https://browser-use.com/profile.sh | sh');
    console.log(`   Then select profile "${profile.id}" and sync while logged into GHL.`);
  } catch (err: any) {
    console.log(`   Error: ${err.message?.substring(0, 200)}`);
    if (err.message?.includes('already exists')) {
      console.log('   Profile already exists. Listing profiles to find GHL profile...');
    }
  }

  console.log('\n=== Setup Complete ===');
  console.log('\nNext steps:');
  console.log('1. Sync GHL cookies to the new profile (see command above)');
  console.log('2. Run buTestWf01.ts to test WF-01 configuration via Browser-Use');
}

setup().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
