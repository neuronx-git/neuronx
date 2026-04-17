# VMC Migration — 3 Remaining Manual Tasks

Sandbox → production VMC migration is **95% complete** via API. These 3 tasks require GHL UI clicks because GHL's Workflow + Pipeline APIs are read-only for these operations.

**Total manual time: ~5 minutes.**

---

## ✅ What's already done (zero manual work)

- ✅ **26 premium email templates** uploaded to VMC (Postmark MIT-licensed base + VMC branding)
- ✅ **140 custom fields** migrated (includes all 20 case_*/ircc_* fields)
- ✅ **107 tags** migrated (includes all `nx:case:*` and `nx:decision:*` tags)
- ✅ **30 demo contacts** created in VMC (email: `*.demo.neuronx.co`, tag: `demo-data`)
- ✅ **PostgreSQL demo data**: 30 contacts, 30 opportunities, 11 cases, 143 activities, 13 signatures, 9 dependents
- ✅ **Railway API** updated to use new VMC PIT + location
- ✅ **Metabase dashboards** refreshed — $36K demo revenue showing, 11 cases across 7 stages

---

## 🔧 Your 3 manual tasks

### Task 1 — Delete 3 broken "🚧 Processing" workflow duplicates (2 min)

These are GHL's failed partial snapshot imports. They're disabled and won't run, but clutter the list.

**Steps:**
1. Log into https://app.gohighlevel.com → Switch to **Visa Master Canada** sub-account
2. Go to **Automation → Workflows**
3. Delete these 3 workflows:
   - 🚧 Processing - WF-10 Post-Consult Follow-Up
   - 🚧 Processing - WF-11 Nurture Campaign Monthly
   - 🚧 Processing - WF-13 PIPEDA Data Deletion Request

### Task 2 — Create "NeuronX — Case Processing" pipeline (1 min)

**Steps:**
1. **Opportunities → Pipelines → Create New Pipeline**
2. **Name**: `NeuronX — Case Processing`
3. Add these 9 stages in order:
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
4. Save

### Task 3 — Import the 9 WF-CP workflows (2 min)

The 9 case processing workflows (WF-CP-01 through WF-CP-09) need to come from a fresh snapshot.

**Option A (recommended — 2 min):**
1. In **sandbox agency** (old: `1H22jRUQWbxzaCaacZjO`):
   - Settings → Snapshots → **Create New Snapshot**
   - Name: "VMC Full v2 — 2026-04-17"
   - Source: VMC sandbox location
   - Include: Workflows only (faster)
   - Save
2. In **new agency** (NeuronX `qKxHWhSxcGxcW3YycTui`):
   - Settings → Snapshots → **Load Snapshot**
   - Select "VMC Full v2 — 2026-04-17"
   - Target: VMC location
   - Apply → this will add the 9 WF-CP workflows without touching the 18 already there

**Option B (if sandbox access lost):**
Rebuild manually — their designs are in `docs/02_operating_system/ghl_configuration_blueprint.md`.

---

## 🔍 How to verify everything works

After completing the 3 tasks, run this verification:

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

# Expected state
r = httpx.get(f"{GHL}/workflows/?locationId={LOC}", headers=HDR, timeout=15)
wfs = r.json().get("workflows", [])
broken = [w for w in wfs if "🚧" in w["name"]]
wf_cp = [w for w in wfs if w["name"].startswith("WF-CP")]

r = httpx.get(f"{GHL}/opportunities/pipelines?locationId={LOC}", headers=HDR, timeout=15)
pipes = r.json().get("pipelines", [])
case_pipe = [p for p in pipes if "Case Processing" in p.get("name", "")]

print(f"Workflows: {len(wfs)} total ({len(broken)} broken should be 0, {len(wf_cp)} WF-CP should be 9)")
print(f"Pipelines: {len(pipes)} total ({len(case_pipe)} Case Processing should be 1)")
EOF
```

Expected output after all 3 tasks:
```
Workflows: 24 total (0 broken should be 0, 9 WF-CP should be 9)
Pipelines: 2 total (1 Case Processing should be 1)
```

---

## 📊 Where to view the demo

- **FastAPI production**: https://neuronx-production-62f9.up.railway.app/demo/summary
- **Metabase dashboards**:
  - Pipeline Health: https://metabase-production-1846.up.railway.app/dashboard/8
  - Case Status: https://metabase-production-1846.up.railway.app/dashboard/9
  - Activity Timeline: https://metabase-production-1846.up.railway.app/dashboard/10
- **GHL VMC**: Log in → Contacts → filter by tag `demo-data` (30 contacts)

**Demo data highlights** (all prefixed `demo-` or `DEMO-`):
- 30 realistic contacts across 8 programs, 12 countries
- 11 active cases in 7 different stages (onboarding → closed/approved/refused)
- $36K demo revenue to show
- 143 activity records populating the timeline
- 2 approved + 1 refused decision to demo the case processing flow
- 1 case in RFI stage to demo the urgent workflow
