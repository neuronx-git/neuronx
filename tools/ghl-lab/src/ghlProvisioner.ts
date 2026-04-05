import fs from 'node:fs'
import path from 'node:path'
import { readKeychainSecret } from './keychain'
import { getEnv } from './env'

const LOCATION_ID = 'FlRL82M0D6nclmKT7eXH'
const BASE_URL = 'https://services.leadconnectorhq.com'
const VERSION = '2021-07-28'

const TOKEN_FILE = path.resolve(__dirname, '..', '.tokens.json')

type ApiResult = { ok: true; data: any } | { ok: false; status: number; error: string }

function readTokenFile(): { access_token: string; refresh_token: string } | null {
  try {
    const raw = fs.readFileSync(TOKEN_FILE, 'utf-8')
    const parsed = JSON.parse(raw)
    if (parsed.access_token && parsed.refresh_token) return parsed
    return null
  } catch {
    return null
  }
}

function writeTokenFile(accessToken: string, refreshToken: string): void {
  const existing = readTokenFile() ?? {}
  const payload = {
    ...existing,
    access_token: accessToken,
    refresh_token: refreshToken,
    refreshed_at: new Date().toISOString(),
  }
  fs.writeFileSync(TOKEN_FILE, JSON.stringify(payload, null, 2), 'utf-8')
}

async function getAccessToken(): Promise<string> {
  const tokens = readTokenFile()
  if (!tokens) {
    throw new Error(`No tokens found at ${TOKEN_FILE}. Run oauth:server first.`)
  }

  const valid = await testToken(tokens.access_token)
  if (valid) return tokens.access_token

  console.log('Access token expired, refreshing...')

  const env = getEnv()
  let clientId: string
  let clientSecret: string
  try {
    clientId = await readKeychainSecret({ service: env.GHL_KEYCHAIN_SERVICE, account: 'oauth-client-id' })
    clientSecret = await readKeychainSecret({ service: env.GHL_KEYCHAIN_SERVICE, account: 'oauth-client-secret' })
  } catch {
    throw new Error('Missing OAuth client credentials in Keychain. Store client-id and client-secret first.')
  }

  const body = new URLSearchParams()
  body.set('grant_type', 'refresh_token')
  body.set('client_id', clientId)
  body.set('client_secret', clientSecret)
  body.set('refresh_token', tokens.refresh_token)

  const res = await fetch(`${BASE_URL}/oauth/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', Accept: 'application/json' },
    body,
  })

  const json = await res.json().catch(() => ({}))

  if (!res.ok) {
    const msg = (json as any)?.error_description ?? (json as any)?.message ?? `HTTP ${res.status}`
    throw new Error(`Token refresh failed: ${msg}. Re-run oauth:server.`)
  }

  const newAccess = (json as any).access_token as string
  const newRefresh = ((json as any).refresh_token as string) ?? tokens.refresh_token

  writeTokenFile(newAccess, newRefresh)
  console.log('Token refreshed and saved.')

  return newAccess
}

async function testToken(token: string): Promise<boolean> {
  try {
    const res = await fetch(`${BASE_URL}/locations/${LOCATION_ID}`, {
      headers: { Authorization: `Bearer ${token}`, Version: VERSION, Accept: 'application/json' },
    })
    return res.ok
  } catch {
    return false
  }
}

async function apiCall(
  token: string,
  method: string,
  path: string,
  body?: unknown,
): Promise<ApiResult> {
  const url = `${BASE_URL}${path}`
  const headers: Record<string, string> = {
    Authorization: `Bearer ${token}`,
    Version: VERSION,
    Accept: 'application/json',
  }
  if (body) headers['Content-Type'] = 'application/json'

  const res = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  const text = await res.text()
  let json: any
  try {
    json = text ? JSON.parse(text) : {}
  } catch {
    json = { raw: text }
  }

  if (!res.ok) {
    return { ok: false, status: res.status, error: json?.message ?? json?.error ?? `HTTP ${res.status}` }
  }
  return { ok: true, data: json }
}

function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms))
}

type FieldDef = {
  name: string
  dataType: string
  placeholder?: string
  options?: string[]
  model?: string
}

const CUSTOM_FIELDS: { folder: string; fields: FieldDef[] }[] = [
  {
    folder: 'Identity and Source',
    fields: [
      {
        name: 'lead_source',
        dataType: 'SINGLE_OPTIONS',
        options: ['Web Form', 'Facebook Ad', 'Google Ad', 'Phone Call', 'WhatsApp', 'Referral', 'Walk-In', 'Email', 'Other'],
      },
      { name: 'lead_source_detail', dataType: 'TEXT' },
      { name: 'utm_source', dataType: 'TEXT' },
      { name: 'utm_medium', dataType: 'TEXT' },
      { name: 'utm_campaign', dataType: 'TEXT' },
    ],
  },
  {
    folder: 'Readiness Assessment',
    fields: [
      {
        name: 'program_interest',
        dataType: 'SINGLE_OPTIONS',
        options: ['Express Entry', 'Spousal Sponsorship', 'Study Permit', 'Work Permit', 'LMIA', 'PR Renewal', 'Citizenship', 'Visitor', 'Other', 'Unknown'],
      },
      { name: 'program_interest_detail', dataType: 'TEXT' },
      {
        name: 'current_location',
        dataType: 'SINGLE_OPTIONS',
        options: ['In Canada', 'Outside Canada', 'Unknown'],
      },
      { name: 'location_detail', dataType: 'TEXT' },
      {
        name: 'timeline_urgency',
        dataType: 'SINGLE_OPTIONS',
        options: ['Urgent 30d', 'Near-term 1-3mo', 'Medium 3-6mo', 'Long-term 6mo+', 'Unknown'],
      },
      { name: 'urgency_detail', dataType: 'TEXT' },
      {
        name: 'prior_applications',
        dataType: 'SINGLE_OPTIONS',
        options: ['None', 'Approved only', 'Has refusal(s)', 'Unknown'],
      },
      { name: 'prior_application_detail', dataType: 'TEXT' },
      {
        name: 'budget_awareness',
        dataType: 'SINGLE_OPTIONS',
        options: ['Aware', 'Unaware', 'Unclear', 'Not discussed'],
      },
      {
        name: 'complexity_flags',
        dataType: 'MULTIPLE_OPTIONS',
        options: [
          'None',
          'Multiple refusals',
          'Inadmissibility',
          'Deportation/removal',
          'Custody',
          'Misrepresentation',
          'Active case elsewhere',
          'Minor involved',
        ],
      },
      {
        name: 'readiness_outcome',
        dataType: 'SINGLE_OPTIONS',
        options: ['Ready Standard', 'Ready Urgent', 'Ready Complex', 'Not Ready', 'Disqualified'],
      },
      { name: 'assessment_completed_at', dataType: 'DATE' },
      { name: 'assessed_by', dataType: 'TEXT' },
    ],
  },
  {
    folder: 'Attempt Tracking',
    fields: [
      { name: 'contact_attempt_count', dataType: 'NUMERICAL' },
      { name: 'last_contact_attempt_at', dataType: 'DATE' },
      {
        name: 'last_contact_attempt_method',
        dataType: 'SINGLE_OPTIONS',
        options: ['AI Call', 'Human Call', 'SMS', 'Email', 'WhatsApp'],
      },
      {
        name: 'last_contact_attempt_outcome',
        dataType: 'SINGLE_OPTIONS',
        options: ['Connected', 'Voicemail', 'No Answer', 'Delivered', 'Failed'],
      },
    ],
  },
  {
    folder: 'Booking',
    fields: [
      {
        name: 'confirmation_status',
        dataType: 'SINGLE_OPTIONS',
        options: ['Unconfirmed', 'Confirmed', 'Cancelled', 'Rescheduled'],
      },
      { name: 'reschedule_count', dataType: 'NUMERICAL' },
      {
        name: 'consultation_type',
        dataType: 'SINGLE_OPTIONS',
        options: ['Video', 'Phone', 'In-Person'],
      },
      { name: 'consultation_fee', dataType: 'MONETORY' },
    ],
  },
  {
    folder: 'Consultation Outcome',
    fields: [
      {
        name: 'consultation_outcome',
        dataType: 'SINGLE_OPTIONS',
        options: ['Proceed', 'Follow-Up', 'Declined', 'Complex', 'No-Show'],
      },
      { name: 'consultation_outcome_reason', dataType: 'TEXT' },
      { name: 'outcome_recorded_at', dataType: 'DATE' },
      { name: 'outcome_recorded_by', dataType: 'TEXT' },
    ],
  },
  {
    folder: 'Retainer',
    fields: [
      { name: 'retainer_sent', dataType: 'CHECKBOX' },
      { name: 'retainer_sent_at', dataType: 'DATE' },
      { name: 'retainer_signed', dataType: 'CHECKBOX' },
      { name: 'retainer_signed_at', dataType: 'DATE' },
      { name: 'payment_received', dataType: 'CHECKBOX' },
      { name: 'payment_received_at', dataType: 'DATE' },
      { name: 'engagement_value', dataType: 'MONETORY' },
    ],
  },
  {
    folder: 'Consent and Suppression',
    fields: [
      { name: 'marketing_consent', dataType: 'CHECKBOX' },
      { name: 'marketing_consent_granted_at', dataType: 'DATE' },
      {
        name: 'marketing_consent_method',
        dataType: 'SINGLE_OPTIONS',
        options: ['Form checkbox', 'Verbal logged', 'SMS opt-in'],
      },
      {
        name: 'suppression_reason',
        dataType: 'SINGLE_OPTIONS',
        options: ['Opt-out', 'CASL complaint', 'Manual'],
      },
    ],
  },
]

const TAGS = [
  'nx:new_inquiry',
  'nx:contacting:start',
  'nx:contacted',
  'nx:assessment:required',
  'nx:assessment:complete',
  'nx:consult_ready',
  'nx:booking:invited',
  'nx:booking:confirmed',
  'nx:appointment:noshow',
  'nx:consult:done',
  'nx:outcome:proceed',
  'nx:outcome:follow_up',
  'nx:outcome:declined',
  'nx:retainer:sent',
  'nx:retainer:signed',
  'nx:payment:received',
  'nx:nurture:enter',
  'nx:lost',
  'nx:consent:marketing_yes',
  'nx:consent:marketing_no',
  'nx:suppressed',
]

const PIPELINE_NAME = 'NeuronX — Immigration Intake'
const PIPELINE_STAGES = [
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

type Report = {
  customFieldsCreated: string[]
  customFieldsFailed: { name: string; error: string }[]
  foldersCreated: string[]
  foldersFailed: { name: string; error: string }[]
  tagsCreated: string[]
  tagsFailed: { name: string; error: string }[]
  pipelineCreated: string | null
  pipelineError: string | null
  calendarCreated: string | null
  calendarError: string | null
  scopeErrors: string[]
}

async function createCustomFieldFolder(
  token: string,
  name: string,
): Promise<{ ok: true; id: string } | { ok: false; error: string }> {
  const result = await apiCall(token, 'POST', `/locations/${LOCATION_ID}/customFields/folder`, { name })
  if (result.ok) {
    const id = result.data?.folder?.id ?? result.data?.id ?? result.data?.customFieldFolder?.id
    return { ok: true, id: id ?? 'unknown' }
  }
  return { ok: false, error: result.error }
}

async function createCustomField(
  token: string,
  field: FieldDef & { folderId?: string },
): Promise<{ ok: true; id: string } | { ok: false; error: string }> {
  let dataType = field.dataType
  if (dataType === 'MONETARY') dataType = 'MONETORY'

  const payload: any = {
    name: field.name,
    dataType,
    model: field.model ?? 'contact',
  }

  if (field.folderId) {
    payload.parentFolderId = field.folderId
  }

  if (field.options && field.options.length > 0) {
    payload.options = field.options
    payload.textBoxListOptions = field.options.map((label) => ({ label, prefillValue: '' }))
  }

  if (dataType === 'CHECKBOX' && !field.options) {
    payload.options = ['Yes', 'No']
    payload.textBoxListOptions = [
      { label: 'Yes', prefillValue: '' },
      { label: 'No', prefillValue: '' },
    ]
  }

  if (field.placeholder) {
    payload.placeholder = field.placeholder
  }

  const result = await apiCall(token, 'POST', `/locations/${LOCATION_ID}/customFields`, payload)
  if (result.ok) {
    const id = result.data?.customField?.id ?? result.data?.id ?? 'unknown'
    return { ok: true, id }
  }
  return { ok: false, error: result.error }
}

async function createTag(
  token: string,
  name: string,
): Promise<{ ok: true; id: string } | { ok: false; error: string }> {
  const result = await apiCall(token, 'POST', `/locations/${LOCATION_ID}/tags`, { name })
  if (result.ok) {
    const id = result.data?.tag?.id ?? result.data?.id ?? 'unknown'
    return { ok: true, id }
  }
  return { ok: false, error: result.error }
}

async function createPipeline(
  token: string,
): Promise<{ ok: true; id: string; stageIds: string[] } | { ok: false; error: string }> {
  const stages = PIPELINE_STAGES.map((name, i) => ({
    name,
    position: i,
  }))

  const result = await apiCall(token, 'POST', `/opportunities/pipelines`, {
    locationId: LOCATION_ID,
    name: PIPELINE_NAME,
    stages,
  })

  if (result.ok) {
    const id = result.data?.pipeline?.id ?? result.data?.id ?? 'unknown'
    const stageIds = (result.data?.pipeline?.stages ?? result.data?.stages ?? []).map(
      (s: any) => s.id ?? 'unknown',
    )
    return { ok: true, id, stageIds }
  }
  return { ok: false, error: result.error }
}

async function createCalendar(
  token: string,
): Promise<{ ok: true; id: string } | { ok: false; error: string }> {
  const result = await apiCall(token, 'POST', `/calendars/`, {
    locationId: LOCATION_ID,
    name: 'Immigration Consultations',
    description: 'Book a consultation with a licensed immigration consultant.',
    slug: 'immigration-consultations',
    widgetSlug: 'immigration-consultations',
    widgetType: 'classic',
    eventType: 'RoundRobin_OptimizeForAvailability',
    eventTitle: '{{contact.name}} - Immigration Consultation',
    slotDuration: 30,
    slotDurationUnit: 'mins',
    slotBuffer: 0,
    slotBufferUnit: 'mins',
    slotInterval: 30,
    slotIntervalUnit: 'mins',
    preBuffer: 0,
    preBufferUnit: 'mins',
    appoinmentPerSlot: 1,
    appoinmentPerDay: 10,
    enableRecurring: false,
    isLivePaymentMode: false,
    autoConfirm: true,
    shouldSendAlertEmailsToAssignedMember: true,
    googleInvitationEmails: false,
    allowReschedule: true,
    allowCancellation: true,
    shouldAssignContactToTeamMember: true,
    shouldSkipAssigningContactForExisting: true,
    notes: 'NeuronX V1 consultation calendar - 30min appointments, Mon-Fri 9-5 ET',
    formSubmitType: 'ThankYouMessage',
    formSubmitThanksMessage: 'Your consultation has been booked. You will receive a confirmation shortly.',
    stickyContact: true,
    isActive: true,
  })

  if (result.ok) {
    const id = result.data?.calendar?.id ?? result.data?.id ?? 'unknown'
    return { ok: true, id }
  }
  return { ok: false, error: result.error }
}

async function getExistingCustomFields(token: string): Promise<Set<string>> {
  const result = await apiCall(token, 'GET', `/locations/${LOCATION_ID}/customFields?model=contact`)
  if (!result.ok) return new Set()
  const fields = (result.data?.customFields ?? []) as any[]
  return new Set(fields.map((f: any) => f.name?.toLowerCase?.()))
}

async function getExistingTags(token: string): Promise<Set<string>> {
  const result = await apiCall(token, 'GET', `/locations/${LOCATION_ID}/tags`)
  if (!result.ok) return new Set()
  const tags = (result.data?.tags ?? []) as any[]
  return new Set(tags.map((t: any) => t.name?.toLowerCase?.()))
}

async function provisionAll(): Promise<Report> {
  const report: Report = {
    customFieldsCreated: [],
    customFieldsFailed: [],
    foldersCreated: [],
    foldersFailed: [],
    tagsCreated: [],
    tagsFailed: [],
    pipelineCreated: null,
    pipelineError: null,
    calendarCreated: null,
    calendarError: null,
    scopeErrors: [],
  }

  console.log('=== NeuronX Gold Provisioner ===')
  console.log(`Location: ${LOCATION_ID}`)
  console.log('')

  console.log('Obtaining access token...')
  let token: string
  try {
    token = await getAccessToken()
    console.log('Access token obtained.')
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e)
    console.error(`FATAL: ${msg}`)
    report.scopeErrors.push(msg)
    return report
  }

  console.log('Fetching existing custom fields and tags...')
  const existingFields = await getExistingCustomFields(token)
  const existingTags = await getExistingTags(token)
  console.log(`  Found ${existingFields.size} existing custom fields, ${existingTags.size} existing tags`)

  console.log('')
  console.log('--- BLOCK 1: Custom Fields ---')

  for (const group of CUSTOM_FIELDS) {
    console.log(`\nGroup: ${group.folder}`)

    for (const field of group.fields) {
      if (existingFields.has(field.name.toLowerCase())) {
        console.log(`  ⊘ ${field.name} (already exists, skipping)`)
        report.customFieldsCreated.push(field.name)
        continue
      }
      const fieldResult = await createCustomField(token, field)
      if (fieldResult.ok) {
        report.customFieldsCreated.push(field.name)
        console.log(`  ✓ ${field.name} (${field.dataType}) → ${fieldResult.id}`)
      } else {
        if (fieldResult.error.includes('Unauthorized') || fieldResult.error.includes('403')) {
          if (!report.scopeErrors.includes('locations/customFields.write')) {
            report.scopeErrors.push('locations/customFields.write')
          }
          console.error(`  ✗ ${field.name}: SCOPE ERROR`)
          break
        }
        report.customFieldsFailed.push({ name: field.name, error: fieldResult.error })
        console.error(`  ✗ ${field.name}: ${fieldResult.error}`)
      }
      await sleep(150)
    }

    if (report.scopeErrors.length > 0) {
      console.log('\nStopping custom field creation due to scope errors.')
      break
    }
  }

  console.log('')
  console.log('--- BLOCK 1: Tags ---')

  for (const tag of TAGS) {
    if (existingTags.has(tag.toLowerCase())) {
      console.log(`  ⊘ ${tag} (already exists, skipping)`)
      report.tagsCreated.push(tag)
      continue
    }
    const tagResult = await createTag(token, tag)
    if (tagResult.ok) {
      report.tagsCreated.push(tag)
      console.log(`  ✓ ${tag} → ${tagResult.id}`)
    } else {
      if (tagResult.error.includes('Unauthorized') || tagResult.error.includes('403')) {
        if (!report.scopeErrors.includes('locations/tags.write')) {
          report.scopeErrors.push('locations/tags.write')
        }
        console.error(`  ✗ ${tag}: SCOPE ERROR`)
        break
      }
      report.tagsFailed.push({ name: tag, error: tagResult.error })
      console.error(`  ✗ ${tag}: ${tagResult.error}`)
    }
    await sleep(150)
  }

  console.log('')
  console.log('--- BLOCK 2: Pipeline ---')
  console.log('  ⊘ GHL V2 API does not support pipeline creation. Pipeline must be created via GHL UI.')
  report.pipelineError = 'API_NOT_AVAILABLE: Must create via GHL UI'

  console.log('')
  console.log('--- BLOCK 3: Calendar ---')

  const calendarResult = await createCalendar(token)
  if (calendarResult.ok) {
    report.calendarCreated = calendarResult.id
    console.log(`  ✓ Calendar "Immigration Consultations" → ${calendarResult.id}`)
  } else {
    if (calendarResult.error.includes('Unauthorized') || calendarResult.error.includes('403')) {
      report.scopeErrors.push('calendars.write')
    }
    report.calendarError = calendarResult.error
    console.error(`  ✗ Calendar failed: ${calendarResult.error}`)
  }

  console.log('')
  console.log('=== REPORT ===')
  console.log(`Custom fields created: ${report.customFieldsCreated.length}`)
  console.log(`Custom fields failed: ${report.customFieldsFailed.length}`)
  console.log(`Folders created: ${report.foldersCreated.length}`)
  console.log(`Tags created: ${report.tagsCreated.length}`)
  console.log(`Tags failed: ${report.tagsFailed.length}`)
  console.log(`Pipeline: ${report.pipelineCreated ? '✓' : '✗'}`)
  console.log(`Calendar: ${report.calendarCreated ? '✓' : '✗'}`)

  if (report.scopeErrors.length > 0) {
    console.log('')
    console.log('SCOPE ERRORS DETECTED:')
    console.log('The OAuth token is missing required scopes. Update the Marketplace app scopes and re-authorize.')
    console.log('Required scopes:')
    console.log('  locations.readonly locations.write')
    console.log('  locations/customFields.readonly locations/customFields.write')
    console.log('  locations/tags.readonly locations/tags.write')
    console.log('  opportunities.readonly opportunities.write')
    console.log('  calendars.readonly calendars.write')
    console.log('  calendars/events.readonly calendars/events.write')
    console.log('  oauth.readonly oauth.write')
    console.log('')
    console.log(`Specific missing: ${report.scopeErrors.join(', ')}`)
  }

  if (report.customFieldsFailed.length > 0) {
    console.log('')
    console.log('Failed custom fields:')
    for (const f of report.customFieldsFailed) {
      console.log(`  - ${f.name}: ${f.error}`)
    }
  }

  if (report.tagsFailed.length > 0) {
    console.log('')
    console.log('Failed tags:')
    for (const f of report.tagsFailed) {
      console.log(`  - ${f.name}: ${f.error}`)
    }
  }

  return report
}

provisionAll()
  .then((report) => {
    const total =
      report.customFieldsCreated.length +
      report.tagsCreated.length +
      (report.pipelineCreated ? 1 : 0) +
      (report.calendarCreated ? 1 : 0)
    const failures =
      report.customFieldsFailed.length +
      report.tagsFailed.length +
      (report.pipelineError ? 1 : 0) +
      (report.calendarError ? 1 : 0)

    console.log(`\nTotal created: ${total} | Total failed: ${failures}`)

    if (failures > 0 || report.scopeErrors.length > 0) {
      process.exit(1)
    }
  })
  .catch((err) => {
    console.error(err instanceof Error ? err.message : err)
    process.exit(1)
  })
