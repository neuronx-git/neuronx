import 'dotenv/config';
import { BrowserUse } from 'browser-use-sdk';
import * as fs from 'fs';
import * as path from 'path';

const API_KEY = process.env.BROWSER_USE_API_KEY!;
const PROFILE_ID = process.env.BU_GHL_PROFILE_ID || '';
const LOCATION_ID = 'FlRL82M0D6nclmKT7eXH';
const EVIDENCE_DIR = path.join(__dirname, '..', 'evidence');

if (!fs.existsSync(EVIDENCE_DIR)) fs.mkdirSync(EVIDENCE_DIR, { recursive: true });

const client = new BrowserUse({ apiKey: API_KEY });

interface TaskResult {
  taskId: string;
  status: string;
  output: string;
  liveUrl?: string;
  steps?: number;
}

async function runBuTask(taskPrompt: string, label: string): Promise<TaskResult> {
  console.log(`\n[${label}] Sending task to Browser-Use Cloud...`);
  console.log(`[${label}] Prompt: ${taskPrompt.substring(0, 200)}...`);

  const createOpts: any = {
    task: taskPrompt,
  };
  if (PROFILE_ID) {
    createOpts.browser_profile_id = PROFILE_ID;
  }

  const task = await client.tasks.create(createOpts);
  console.log(`[${label}] Task ID: ${task.id}`);
  // Cast to any to avoid linter error if types are missing liveUrl on creation response
  const liveUrl = (task as any).liveUrl || 'N/A';
  console.log(`[${label}] Live URL: ${liveUrl}`);

  let maxPolls = 60;
  let finalStatus = 'unknown';
  while (maxPolls-- > 0) {
    await new Promise(r => setTimeout(r, 5000));
    const taskDetails = await client.tasks.get(task.id);
    finalStatus = taskDetails.status;
    if (finalStatus === 'finished' || finalStatus === 'failed' || finalStatus === 'stopped') {
      break;
    }
    if (maxPolls % 6 === 0) {
      console.log(`[${label}] Polling... status=${finalStatus}`);
    }
  }

  const details = await client.tasks.get(task.id);
  const output = details.output || '';
  const finalLiveUrl = (details as any).liveUrl || liveUrl;
  console.log(`[${label}] Final status: ${finalStatus}`);
  console.log(`[${label}] Output: ${output.substring(0, 500)}`);

  fs.writeFileSync(
    path.join(EVIDENCE_DIR, `bu_${label}_${Date.now()}.json`),
    JSON.stringify({ taskId: task.id, status: finalStatus, output, liveUrl: finalLiveUrl }, null, 2)
  );

  return { taskId: task.id, status: finalStatus, output, liveUrl: finalLiveUrl === 'N/A' ? undefined : finalLiveUrl };
}

function buildWfPrompt(wfName: string, wfIndex: string, trigger: string, actions: string[]): string {
  const actionList = actions.map((a, i) => `   ${i + 1}. ${a}`).join('\n');
  return `You are operating inside GoHighLevel (GHL).

Navigate to: https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/list

Find and click the workflow named "${wfName}" to open its editor.

Wait for the workflow editor to fully load (there may be a loading overlay — dismiss it by pressing Escape or waiting).

CONFIGURE THIS WORKFLOW:

Trigger: ${trigger}
  - Click the "Add New Trigger" node in the canvas
  - Select the trigger type listed above
  - Configure the trigger settings as specified
  - Click "Save Trigger"

Actions (add in this exact order):
${actionList}

For each action:
  - Click the "+" button below the last node
  - Search/select the action type
  - Configure the settings
  - Click "Save Action" if there is a save button

After adding all actions, verify:
  - The trigger node shows the correct trigger type
  - All ${actions.length} action nodes are visible in the flow
  - The workflow shows "Saved" status

Then navigate away to the automation list and re-open the same workflow to verify persistence.

Return a structured result:
1. Trigger configured: yes/no + type
2. Actions configured: count / expected ${actions.length}
3. Persisted after reload: yes/no
4. Any blocker encountered
5. Screenshot description of final state`;
}

const WORKFLOW_SPECS: { name: string; index: string; trigger: string; actions: string[] }[] = [
  {
    name: 'WF-01 New Inquiry Acknowledge',
    index: '01',
    trigger: 'Form Submitted → select "Immigration Inquiry (V1)"',
    actions: [
      'Add Contact Tag → "nx:new_inquiry"',
      'Create/Update Opportunity → Pipeline: NeuronX — Immigration Intake, Stage: NEW',
      'Send SMS → "Hi {{contact.first_name}}, thank you for your immigration inquiry. Our team will be in touch shortly."',
      'Send Email → Subject: "We received your inquiry" / Body: acknowledgment with firm branding',
      'Add Contact Tag → "nx:contacting:start"',
      'Update Opportunity → Move to stage: CONTACTING',
    ],
  },
  {
    name: 'WF-02 Contact Attempt Sequence',
    index: '02',
    trigger: 'Contact Tag Added → "nx:contacting:start"',
    actions: [
      'Create Manual Action (Task) → Title: "Call lead (Attempt 1)"',
      'Wait → 30 minutes',
      'Send SMS → booking link + callback request',
      'Wait → 2 hours',
      'Create Manual Action (Task) → Title: "Call lead (Attempt 2)"',
      'Wait → 1 business day',
      'Create Manual Action (Task) → Title: "Call lead (Attempt 3) + voicemail"',
      'Wait → 2 business days',
      'Send SMS → booking link + callback request',
      'Wait → 5 business days',
      'Send Email → Subject: "Still interested?" / Body: booking link + value message',
      'Wait → 10 business days',
      'Send SMS → "We\'d still love to help. Book here: [link]"',
      'Update Opportunity → Move to stage: UNREACHABLE',
      'Add Contact Tag → "nx:nurture:enter"',
    ],
  },
  {
    name: 'WF-03 Mark Contacted → Readiness',
    index: '03',
    trigger: 'Contact Tag Added → "nx:contacted"',
    actions: [
      'Add Contact Tag → "nx:assessment:required"',
      'Create Manual Action (Task) → Title: "Complete readiness assessment (R1-R6)"',
    ],
  },
  {
    name: 'WF-04 Readiness Complete → Invite Booking',
    index: '04',
    trigger: 'Contact Tag Added → "nx:assessment:complete"',
    actions: [
      'If/Else Condition → If custom field "readiness_outcome" = "Ready" or "Ready - Urgent"',
      '(Yes branch) Update Opportunity → Move to stage: CONSULT READY',
      '(Yes branch) Add Contact Tag → "nx:consult_ready"',
      '(Yes branch) Send SMS → booking link invitation',
      '(Yes branch) Send Email → Subject: "Book your consultation"',
      '(Yes branch) Add Contact Tag → "nx:booking:invited"',
      '(No branch) If/Else → If "readiness_outcome" = "Not Ready"',
      '(Not Ready) Update Opportunity → Move to stage: NURTURE',
      '(Not Ready) Add Contact Tag → "nx:nurture:enter"',
      '(Else: Disqualified) Update Opportunity → Move to stage: LOST',
      '(Else: Disqualified) Add Contact Tag → "nx:lost"',
    ],
  },
  {
    name: 'WF-05 Appointment Booked → Reminders',
    index: '05',
    trigger: 'Customer Booked Appointment → Calendar: "Immigration Consultations"',
    actions: [
      'Update Opportunity → Move to stage: BOOKED',
      'Add Contact Tag → "nx:booking:confirmed"',
      'Send SMS → confirmation with date/time',
      'Send Email → Subject: "Consultation confirmed"',
      'Wait → Until 48 hours before appointment',
      'Send SMS → "Your consultation is in 2 days. Reply YES to confirm."',
      'Wait → Until 24 hours before appointment',
      'Send SMS → "Reminder: consultation tomorrow"',
      'Wait → Until 2 hours before appointment',
      'Send SMS → "Your consultation starts in 2 hours."',
    ],
  },
  {
    name: 'WF-06 No-Show → Recovery',
    index: '06',
    trigger: 'Appointment Status → No Show',
    actions: [
      'Add Contact Tag → "nx:appointment:noshow"',
      'Wait → 5 minutes',
      'Send SMS → "We missed you! Reschedule here: [link]"',
      'Wait → 10 minutes',
      'Create Manual Action (Task) → Title: "Call no-show within 15 min"',
      'Wait → 2 hours',
      'Send SMS → reschedule link',
      'Wait → 1 business day',
      'Send SMS → follow-up',
      'Wait → 3 business days',
      'Send Email → Subject: "We\'d love to reschedule"',
      'Wait → 7 business days',
      'Send SMS → final reschedule attempt',
      'Update Opportunity → Move to stage: NURTURE',
    ],
  },
  {
    name: 'WF-07 Consultation Outcome Capture',
    index: '07',
    trigger: 'Appointment Status → Completed (Show / Checked In)',
    actions: [
      'Create Manual Action (Task) → Title: "Record consultation outcome"',
      'Wait → 1 hour',
      'Internal Notification → "Outcome still needed for {{contact.name}}"',
      'Wait → 3 hours',
      'Internal Notification → "Missing outcome for {{contact.name}}" (to firm owner)',
    ],
  },
  {
    name: 'WF-08 Outcome Routing',
    index: '08',
    trigger: 'Contact Changed → Custom Field: "consultation_outcome"',
    actions: [
      'If/Else Condition → If "consultation_outcome" = "Proceed"',
      '(Proceed) Add Contact Tag → "nx:outcome:proceed"',
      '(Proceed) Update Opportunity → Move to stage: CONSULT COMPLETED',
      '(Else) If/Else → If "consultation_outcome" = "Follow-Up"',
      '(Follow-Up) Add Contact Tag → "nx:outcome:follow_up"',
      '(Follow-Up) Update Opportunity → Move to stage: CONSULT COMPLETED',
      '(Else: Declined) Add Contact Tag → "nx:outcome:declined"',
      '(Declined) Update Opportunity → Move to stage: LOST',
    ],
  },
  {
    name: 'WF-09 Retainer Follow-Up',
    index: '09',
    trigger: 'Contact Tag Added → "nx:outcome:proceed"',
    actions: [
      'Send Email → Subject: "Next steps: retainer & checklist"',
      'Update Contact Field → Set "retainer_sent" = true',
      'Wait → 1 day',
      'Send SMS → "Did you receive the retainer?"',
      'Wait → 1 day',
      'Send SMS/Email → Follow-up on retainer',
      'Wait → 3 days',
      'Send Email → Subject: "Retainer follow-up"',
      'Wait → 5 days',
      'Create Manual Action (Task) → "Day 10 retainer chase call"',
      'Wait → 4 days',
      'Send Email → Subject: "Final follow-up"',
      'Update Opportunity → Move to stage: NURTURE (if unsigned)',
    ],
  },
  {
    name: 'WF-10 Post-Consult Follow-Up (Undecided)',
    index: '10',
    trigger: 'Contact Tag Added → "nx:outcome:follow_up"',
    actions: [
      'Send Email → Subject: "Consultation summary"',
      'Wait → 2 days',
      'Send SMS → "Checking in — any questions from your consultation?"',
      'Wait → 3 days',
      'Send Email → Subject: "Resources for your immigration journey"',
      'Wait → 2 days',
      'Create Manual Action (Task) → "Call/SMS check-in"',
      'Wait → 7 days',
      'Send Email → Subject: "Ready to move forward?"',
      'Update Opportunity → Move to stage: NURTURE',
    ],
  },
  {
    name: 'WF-11 Nurture Campaign Monthly',
    index: '11',
    trigger: 'Contact Tag Added → "nx:nurture:enter"',
    actions: [
      'If/Else Condition → If custom field "marketing_consent" = true',
      '(Yes) Send Email → Subject: "Monthly Immigration Update"',
      '(Yes) Wait → 30 days',
      '(Yes) Send Email → next month newsletter',
      '(Yes) Wait → 60 days',
      '(Yes) Send SMS → "How are things going? We\'re here if you need us."',
      '(No consent) End / Do nothing',
    ],
  },
];

async function runWorkflowTask(spec: typeof WORKFLOW_SPECS[0]): Promise<TaskResult> {
  const prompt = buildWfPrompt(spec.name, spec.index, spec.trigger, spec.actions);
  return runBuTask(prompt, `WF-${spec.index}`);
}

async function runFormDropdowns(): Promise<TaskResult> {
  const prompt = `You are operating inside GoHighLevel (GHL).

Navigate to: https://app.gohighlevel.com/v2/location/${LOCATION_ID}/settings/forms

Find and click the form named "Immigration Inquiry (V1)" to edit it.

For each of these 3 dropdown fields, click the field, open its settings, and set the options:

1. Field: "Program Interest"
   Options: Express Entry, Provincial Nominee (PNP), Study Permit, Work Permit, Family Sponsorship, Visitor Visa, Not Sure

2. Field: "Current Location (Country)"
   Options: Canada, India, Philippines, Nigeria, Pakistan, Other

3. Field: "Timeline"
   Options: Within 3 months, 3-6 months, 6-12 months, More than 12 months, Just exploring

Click Save after configuring all fields.

Return:
1. Each field configured: yes/no
2. Options count per field
3. Any blocker`;

  return runBuTask(prompt, 'FORM-DROPDOWNS');
}

async function runDeleteJunkWorkflows(): Promise<TaskResult> {
  const prompt = `You are operating inside GoHighLevel (GHL).

Navigate to: https://app.gohighlevel.com/v2/location/${LOCATION_ID}/automation/list

Find and delete these 3 workflows (they have auto-generated names starting with "New Workflow :"):
1. "New Workflow : 1773665053619"
2. "New Workflow : 1773665946429"
3. "New Workflow : 1773666055197"

For each: click the three-dot menu → Delete → Confirm deletion.

After all 3 are deleted, count the remaining workflows. There should be exactly 11 named WF-01 through WF-11.

Return:
1. Each deleted: yes/no
2. Remaining workflow count
3. Any blocker`;

  return runBuTask(prompt, 'DELETE-JUNK');
}

async function runLandingPage(): Promise<TaskResult> {
  const prompt = `You are operating inside GoHighLevel (GHL).

Navigate to: https://app.gohighlevel.com/v2/location/${LOCATION_ID}/funnels-websites

Find the funnel named "NeuronX Intake Landing (V1)" and click to edit it.
Click the step named "Immigration Inquiry" to open the page editor.

Add these sections top to bottom:

1. Hero Section:
   - Headline: "Start Your Canadian Immigration Journey"
   - Subheadline: "Free initial assessment — takes 2 minutes"

2. Form Embed:
   - Add a Form element
   - Select "Immigration Inquiry (V1)"
   - Button text: "Get Your Free Assessment"

3. Alternative CTA:
   - Text: "Ready to talk? Book a consultation directly."
   - Button: "Book Now"

4. Compliance Footer:
   - Text: "This form is for inquiry purposes only. Submitting this form does not create a solicitor-client relationship and does not guarantee eligibility for any immigration program."

Save and Publish the page.

Return:
1. Each section added: yes/no
2. Page published: yes/no
3. Public URL if visible
4. Any blocker`;

  return runBuTask(prompt, 'LANDING-PAGE');
}

const TASK_MAP: Record<string, () => Promise<TaskResult>> = {};
for (const spec of WORKFLOW_SPECS) {
  TASK_MAP[`wf-${spec.index}`] = () => runWorkflowTask(spec);
}
TASK_MAP['form-dropdowns'] = runFormDropdowns;
TASK_MAP['delete-junk'] = runDeleteJunkWorkflows;
TASK_MAP['landing-page'] = runLandingPage;

async function main() {
  const target = process.argv[2] || '';
  const validTargets = Object.keys(TASK_MAP);

  if (target === 'all') {
    console.log('=== Running ALL tasks in sequence ===\n');
    const results: Record<string, TaskResult> = {};

    const order = ['delete-junk', 'form-dropdowns',
      ...WORKFLOW_SPECS.map(s => `wf-${s.index}`),
      'landing-page'];

    for (const t of order) {
      try {
        results[t] = await TASK_MAP[t]();
        console.log(`\n✅ ${t}: ${results[t].status}`);
      } catch (err: any) {
        console.log(`\n❌ ${t}: ${err.message}`);
        results[t] = { taskId: '', status: 'error', output: err.message };
      }
    }

    console.log('\n\n=== SUMMARY ===');
    for (const [k, v] of Object.entries(results)) {
      console.log(`${v.status === 'finished' ? '✅' : '❌'} ${k}: ${v.status}`);
    }
    fs.writeFileSync(
      path.join(EVIDENCE_DIR, `bu_all_results_${Date.now()}.json`),
      JSON.stringify(results, null, 2)
    );

  } else if (TASK_MAP[target]) {
    await TASK_MAP[target]();
  } else {
    console.log('Usage: npx tsx src/buOrchestrator.ts <target>');
    console.log('\nTargets:');
    console.log('  all              — Run all tasks in sequence');
    for (const t of validTargets) {
      console.log(`  ${t.padEnd(20)} — ${t}`);
    }
  }
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
