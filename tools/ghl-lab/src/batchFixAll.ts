/**
 * NeuronX — Batch Fix All GHL Operations
 *
 * Run this AFTER the GHL OAuth token has write scopes.
 * To fix scopes: Go to GHL Marketplace → Your App → OAuth Settings → Add write scopes
 * Then re-authorize the app in the sub-account.
 *
 * Usage: cd tools/ghl-lab && npx tsx src/batchFixAll.ts
 */

import * as fs from 'fs';
import * as path from 'path';

const LOCATION_ID = 'FlRL82M0D6nclmKT7eXH';
const API_BASE = 'https://services.leadconnectorhq.com';

function getToken(): string {
  const tokensPath = path.join(__dirname, '..', '.tokens.json');
  const tokens = JSON.parse(fs.readFileSync(tokensPath, 'utf-8'));
  return tokens.access_token;
}

async function apiCall(method: string, endpoint: string, body?: any): Promise<any> {
  const token = getToken();
  const opts: RequestInit = {
    method,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Version': '2021-07-28',
      'Content-Type': 'application/json',
    },
  };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(`${API_BASE}${endpoint}`, opts);
  const data = await res.json();

  if (!res.ok) {
    console.error(`❌ ${method} ${endpoint} — ${res.status}: ${JSON.stringify(data)}`);
    return null;
  }
  return data;
}

async function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================
// CUSTOM FIELDS TO CREATE
// ============================================
const FIELDS_TO_CREATE = [
  // P1 — Critical
  { name: 'retainer_amount', dataType: 'MONETARY' },
  { name: 'lost_reason', dataType: 'SINGLE_OPTIONS', options: ['Price too high', 'Bad timing', 'Chose competitor', 'Not eligible', 'Unresponsive', 'Changed mind', 'Other'] },
  { name: 'consultation_outcome', dataType: 'SINGLE_OPTIONS', options: ['Proceed with retainer', 'Needs more time', 'Not eligible', 'No-show', 'Client declined', 'Referred to other firm'] },

  // P2 — Readiness scoring
  { name: 'r2_education_level', dataType: 'SINGLE_OPTIONS', options: ['PhD/Masters', 'Bachelors', 'Diploma/Certificate', 'High School', 'Below High School', 'Unknown'] },
  { name: 'r4_budget_readiness', dataType: 'SINGLE_OPTIONS', options: ['Strong - Ready to invest', 'Moderate - Considering budget', 'Low - Price sensitive', 'Unknown'] },
  { name: 'r5_language_ability', dataType: 'SINGLE_OPTIONS', options: ['CLB 9+', 'CLB 7-8', 'CLB 5-6', 'Below CLB 5', 'Unknown'] },
  { name: 'r6_family_situation', dataType: 'SINGLE_OPTIONS', options: ['Single', 'Married/Common-law', 'Dependent children', 'Separated/Divorced', 'Unknown'] },

  // P2 — Compliance
  { name: 'ai_disclaimer_shown', dataType: 'CHECKBOX' },
  { name: 'ai_disclaimer_timestamp', dataType: 'DATE' },
  { name: 'consent_ip_address', dataType: 'TEXT' },
  { name: 'consent_form_version', dataType: 'TEXT' },
  { name: 'data_deletion_requested', dataType: 'CHECKBOX' },
  { name: 'conflict_check_cleared', dataType: 'CHECKBOX' },
];

// ============================================
// TAGS TO CREATE
// ============================================
const TAGS_TO_CREATE = [
  // Source tracking
  'nx:source:website',
  'nx:source:referral',
  'nx:source:paid_ad',
  'nx:source:google',
  'nx:source:meta',

  // Loss reason granularity
  'nx:lost:price',
  'nx:lost:timing',
  'nx:lost:unqualified',
  'nx:lost:competitor',

  // Proposal tracking
  'nx:proposal:sent',
  'nx:proposal:signed',

  // Language routing
  'nx:language:english',
  'nx:language:french',

  // Compliance
  'nx:ai_disclaimer_shown',
  'nx:casl:compliant',
  'nx:do_not_contact',

  // Multi-attempt tracking
  'nx:contacting:attempt2',
  'nx:contacting:attempt3',
  'nx:contacting:attempt4',
  'nx:contacting:attempt5',
  'nx:contacting:attempt6',
];

// ============================================
// MAIN EXECUTION
// ============================================
async function main() {
  console.log('🚀 NeuronX — Batch Fix All GHL Operations');
  console.log('=========================================\n');

  let successCount = 0;
  let failCount = 0;

  // --- CREATE CUSTOM FIELDS ---
  console.log('📋 Creating Custom Fields...');
  for (const field of FIELDS_TO_CREATE) {
    const body: any = { name: field.name, dataType: field.dataType, model: 'contact' };
    if (field.options) body.options = field.options;

    const result = await apiCall('POST', `/locations/${LOCATION_ID}/customFields`, body);
    if (result) {
      console.log(`  ✅ ${field.name} [${field.dataType}]`);
      successCount++;
    } else {
      failCount++;
    }
    await sleep(200); // Rate limit respect
  }

  // --- CREATE TAGS ---
  console.log('\n🏷️  Creating Tags...');
  for (const tagName of TAGS_TO_CREATE) {
    const result = await apiCall('POST', `/locations/${LOCATION_ID}/tags`, { name: tagName });
    if (result) {
      console.log(`  ✅ ${tagName}`);
      successCount++;
    } else {
      failCount++;
    }
    await sleep(200);
  }

  // --- UPDATE CALENDAR ---
  console.log('\n📅 Updating Calendar...');
  const calResult = await apiCall('PUT', `/calendars/To1U2KbcvJ0EAX0RGKHS`, {
    locationId: LOCATION_ID,
    name: 'Immigration Consultations',
    slotBuffer: 10,
    slotBufferUnit: 'mins',
    preBuffer: 5,
    preBufferUnit: 'mins',
    openHours: [
      { daysOfTheWeek: [1], hours: [{ openHour: 9, openMinute: 0, closeHour: 17, closeMinute: 0 }] },
      { daysOfTheWeek: [2], hours: [{ openHour: 9, openMinute: 0, closeHour: 17, closeMinute: 0 }] },
      { daysOfTheWeek: [3], hours: [{ openHour: 9, openMinute: 0, closeHour: 17, closeMinute: 0 }] },
      { daysOfTheWeek: [4], hours: [{ openHour: 9, openMinute: 0, closeHour: 17, closeMinute: 0 }] },
      { daysOfTheWeek: [5], hours: [{ openHour: 9, openMinute: 0, closeHour: 17, closeMinute: 0 }] },
    ],
  });
  if (calResult) {
    console.log('  ✅ Calendar availability set (Mon-Fri 9-5 ET, 10min buffer)');
    successCount++;
  } else {
    failCount++;
  }

  // --- DELETE JUNK FIELDS ---
  console.log('\n🗑️  Deleting Junk Fields...');
  // First find them
  const fieldsResult = await apiCall('GET', `/locations/${LOCATION_ID}/customFields`);
  if (fieldsResult) {
    const junkPatterns = ['152dv', '168z3', '1qpb'];
    const fields = fieldsResult.customFields || [];
    for (const field of fields) {
      const key = field.fieldKey || '';
      const name = field.name || '';
      if (junkPatterns.some(p => key.includes(p) || name.includes(p))) {
        const delResult = await apiCall('DELETE', `/locations/${LOCATION_ID}/customFields/${field.id}`);
        if (delResult !== null) {
          console.log(`  ✅ Deleted junk field: ${name} (${field.id})`);
          successCount++;
        } else {
          failCount++;
        }
        await sleep(200);
      }
    }
  }

  console.log('\n=========================================');
  console.log(`✅ Success: ${successCount} | ❌ Failed: ${failCount}`);
  console.log('=========================================');
}

main().catch(console.error);
