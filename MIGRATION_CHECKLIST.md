# VMC Production — Final Setup Checklist

## ✅ Current state — what's already DONE (zero manual work required)

| Resource | Status | Count |
|---|---|---|
| **Premium email templates (Postmark MIT-licensed)** | ✅ Uploaded | 26 VMC-* templates |
| **Custom fields** | ✅ Migrated | 140 (matches sandbox exactly) |
| **Tags** | ✅ Migrated | 107 (including all `nx:case:*`, `nx:decision:*`) |
| **Intake pipeline + 10 stages** | ✅ Live | 1 pipeline |
| **Intake workflows** | ✅ Live (unchanged from import) | 18 of 18 |
| **Demo contacts in GHL VMC** | ✅ Created | 30 (tag: `demo-data`) |
| **Railway API env** | ✅ Points to prod VMC | PIT + LOC ID |
| **PostgreSQL demo dataset** | ✅ Seeded | 30 contacts, 11 cases, 143 activities, $36K demo |
| **NeuronX SaaS config** | ✅ Built | 23 fields + 24 tags + 3 demo firms in NeuronX sub-account |
| **Metabase dashboards** | ✅ Live | 3 dashboards, 10 views, all populated |

## 🔍 Verified safety (2026-04-17)

Comparison of sandbox vs production VMC via API:
- **15/15 workflows UNCHANGED** after initial import (updatedAt = import time)
- **0 email template name collisions** with our 26 new templates
- **Our 30 demo contacts, 11 cases, 143 activities**: in PostgreSQL/GHL contacts — **NOT in snapshots** → 100% safe

## ⚠️ What's MISSING in production VMC (3 items)

1. ❌ **Case Processing pipeline** (9 stages) — not in snapshot when migration ran
2. ❌ **9 WF-CP workflows** — same reason
3. ⚠️ **3 broken "🚧 Processing - WF-10/11/13" duplicates** — draft status, harmless but cluttered

## 🎯 Recommendation: Build fresh in production (DO NOT re-import snapshot)

**Why not re-import the snapshot:**
- Importer can create MORE duplicate "🚧 Processing" workflows (that's exactly how we got the current 3)
- Lower risk to build the 3 missing items fresh in production UI

**Why building fresh is safe:**
- Case Processing pipeline design is documented in `docs/02_operating_system/ghl_configuration_blueprint.md`
- 9 WF-CP workflows are logically simple: stage-change trigger → tag update → email send
- We have 11 premium Case Processing email templates already live (VMC-15 through VMC-26) ready to plug into workflows

---

## 🔧 Your 3 manual tasks (~15 min total)

These require **production VMC Chrome profile** (which you called "neuronx" profile).

### Task 1 — Delete 3 broken "🚧 Processing" workflows (2 min)

**URL**: https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflows

Hover over each → click ⋮ (three dots) → Delete:
- 🚧 Processing - WF-10 Post-Consult Follow-Up
- 🚧 Processing - WF-11 Nurture Campaign Monthly
- 🚧 Processing - WF-13 PIPEDA Data Deletion Request

### Task 2 — Create "NeuronX - Case Processing" pipeline (2 min)

**URL**: https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/pipelines

Click **+ Create Pipeline** → Name: `NeuronX - Case Processing`

Add 9 stages in order:
```
0. ONBOARDING
1. DOC COLLECTION
2. FORM PREPARATION
3. INTERNAL REVIEW
4. SUBMITTED TO IRCC
5. PROCESSING
6. ADDITIONAL INFO (RFI)
7. DECISION RECEIVED
8. CASE CLOSED
```

### Task 3 — Create 9 WF-CP workflows (10 min)

For each workflow below, click **+ Create Workflow** → skip template → fill as shown.

All workflows:
- **Trigger**: Contact Tag Added (specific tag below)
- **Action 1**: Send Email (template specified)
- **Action 2**: Create Task (assigned to RCIC)

| # | Name | Trigger tag | Email template to use |
|---|---|---|---|
| 1 | WF-CP-01: Client Onboarding | `nx:case:onboarding` | `VMC-15-case-onboarding` |
| 2 | WF-CP-02: Document Collection Reminders | `nx:case:docs_pending` | `VMC-16-cp-docs-reminder` |
| 3 | WF-CP-03: Form Preparation | `nx:case:form_prep` | `VMC-17-cp-form-prep` |
| 4 | WF-CP-04: Internal Review | `nx:case:under_review` | `VMC-18-cp-internal-review` |
| 5 | WF-CP-05: IRCC Submission | `nx:case:submitted` | `VMC-19-cp-submitted` |
| 6 | WF-CP-06: Processing Status Checks | `nx:case:processing` | `VMC-20-cp-status-update` |
| 7 | WF-CP-07: Additional Info (RFI) | `nx:case:rfi` | `VMC-21-cp-rfi` |
| 8 | WF-CP-08: Decision Received | `nx:case:decision` | `VMC-22-cp-decision-approved` (branch by decision) |
| 9 | WF-CP-09: Case Closure | `nx:case:closed` | `VMC-25-cp-case-closed` |

### Task 4 (optional) — Create "NeuronX Sales" pipeline (2 min)

This is for the SaaS business (selling to immigration firms). Switch to **NeuronX sub-account** (not VMC).

**URL**: https://app.gohighlevel.com/v2/location/muc56LdMG8hkmlpFFuZE/pipelines

Name: `NeuronX Sales`. Stages:
```
0. NEW LEAD
1. QUALIFYING (BANT)
2. DEMO SCHEDULED
3. DEMO COMPLETED
4. PROPOSAL SENT
5. TRIAL ACTIVE
6. PAID CUSTOMER
7. CHURNED
```

The 23 SaaS custom fields + 24 tags + 3 demo firm prospects are already in place.

---

## 🎁 Alternative: I can pilot this via your Chrome browser

If you switch Chrome to your "neuronx" profile (production VMC access) and tell me you're ready, I can use Claude-in-Chrome to automate all 4 tasks above — you just watch/approve the clicks.

---

## 🔍 Verification

After completing the tasks, run this to verify:

```bash
cd /Users/ranjansingh/Desktop/NeuronX
python3 << 'EOF'
import httpx, json
with open("tools/ghl-lab/.pit-tokens.json") as f:
    pits = json.load(f)

VMC = pits["vmc"]
HDR = {"Authorization": f"Bearer {VMC['token']}", "Version": "2021-07-28"}
GHL = "https://services.leadconnectorhq.com"
LOC = VMC["locationId"]

wfs = httpx.get(f"{GHL}/workflows/?locationId={LOC}", headers=HDR, timeout=15).json().get("workflows", [])
pipes = httpx.get(f"{GHL}/opportunities/pipelines?locationId={LOC}", headers=HDR, timeout=15).json().get("pipelines", [])

broken = [w for w in wfs if "🚧" in w["name"]]
wf_cp = [w for w in wfs if w["name"].startswith("WF-CP")]
case_pipe = [p for p in pipes if "Case Processing" in p.get("name", "")]

print(f"✅ Workflows: {len(wfs)} total ({len(broken)} broken should be 0, {len(wf_cp)} WF-CP should be 9)")
print(f"✅ Pipelines: {len(pipes)} total ({len(case_pipe)} Case Processing should be 1)")
print()
print(f"{'PASS' if len(broken) == 0 and len(wf_cp) == 9 and len(case_pipe) == 1 else 'INCOMPLETE'}")
EOF
```

**Expected output**: `Workflows: 24 total (0 broken, 9 WF-CP), Pipelines: 2 total (1 Case Processing) — PASS`
