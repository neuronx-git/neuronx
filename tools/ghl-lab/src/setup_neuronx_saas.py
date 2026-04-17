"""
Set up NeuronX SaaS-business configuration (separate from VMC customer product).

ARCHITECTURE CLARIFICATION:
  - VMC sub-account = DEMO of the customer experience.
    VMC shows what an immigration firm (our customer) gets.
    Workflows: WF-01...WF-CP-09 manage their prospects, consultations, cases.

  - NeuronX sub-account = THE SAAS BUSINESS ITSELF.
    NeuronX sells the platform to immigration firms.
    Needs completely different workflows: trial signup, demo booking, onboarding,
    subscription management, churn prevention, renewals.

This script creates in the NeuronX sub-account:
  - 20 custom fields for tracking SaaS sales metrics
  - 18 tags for the SaaS sales funnel
  - Demo seed data (3 firm prospects)

The SaaS sales pipeline "NeuronX Sales" with 8 stages must be created in UI
(pipeline API requires a scope none of our tokens have).
"""
import httpx
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
with open(ROOT / "tools/ghl-lab/.pit-tokens.json") as f:
    PITS = json.load(f)

NX_LOC = PITS["neuronx"]["locationId"]
NX_HDR = {"Authorization": f"Bearer {PITS['neuronx']['token']}",
          "Version": "2021-07-28", "Content-Type": "application/json"}
GHL = "https://services.leadconnectorhq.com"

print("=" * 80)
print(f"NEURONX SAAS-BUSINESS SETUP — Location: {NX_LOC}")
print("=" * 80)

# ═══════════════════════════════════════════════════════════════════
# CUSTOM FIELDS — for tracking SaaS sales to immigration firms
# ═══════════════════════════════════════════════════════════════════
CUSTOM_FIELDS = [
    # Firm profile
    {"name": "Firm Name", "dataType": "TEXT", "fieldKey": "firm_name"},
    {"name": "Firm Website", "dataType": "TEXT", "fieldKey": "firm_website"},
    {"name": "Firm Size (RCICs)", "dataType": "NUMERICAL", "fieldKey": "firm_rcic_count"},
    {"name": "Firm Annual Revenue", "dataType": "MONETORY", "fieldKey": "firm_revenue"},
    {"name": "Firm Province", "dataType": "SINGLE_OPTIONS", "fieldKey": "firm_province",
     "options": ["Ontario","British Columbia","Alberta","Quebec","Manitoba","Saskatchewan","Nova Scotia","New Brunswick","PEI","Newfoundland","Yukon","NWT","Nunavut"]},
    {"name": "Firm Current CRM", "dataType": "SINGLE_OPTIONS", "fieldKey": "firm_current_crm",
     "options": ["None","HubSpot","Salesforce","GoHighLevel","ClickUp","Monday","Other"]},
    {"name": "Firm Founded Year", "dataType": "NUMERICAL", "fieldKey": "firm_founded_year"},

    # SaaS qualification
    {"name": "Lead Source", "dataType": "SINGLE_OPTIONS", "fieldKey": "saas_lead_source",
     "options": ["Website","Google Ads","LinkedIn","Cold Email","Referral","Partner","Conference","Content Marketing","Other"]},
    {"name": "Lead Score", "dataType": "NUMERICAL", "fieldKey": "saas_lead_score"},
    {"name": "Decision Maker Role", "dataType": "SINGLE_OPTIONS", "fieldKey": "saas_dm_role",
     "options": ["Managing Partner","Founder","Ops Manager","Marketing Lead","RCIC","Other"]},
    {"name": "Main Pain Point", "dataType": "SINGLE_OPTIONS", "fieldKey": "saas_pain_point",
     "options": ["Lead response time","Lead quality","Consultation no-shows","Doc collection","Pipeline visibility","RCIC time on admin","Other"]},
    {"name": "BANT Budget Qualified", "dataType": "CHECKBOX", "fieldKey": "saas_bant_budget", "options": ["Yes", "No"]},
    {"name": "BANT Authority Qualified", "dataType": "CHECKBOX", "fieldKey": "saas_bant_authority", "options": ["Yes", "No"]},
    {"name": "BANT Need Qualified", "dataType": "CHECKBOX", "fieldKey": "saas_bant_need", "options": ["Yes", "No"]},
    {"name": "BANT Timeline Qualified", "dataType": "CHECKBOX", "fieldKey": "saas_bant_timeline", "options": ["Yes", "No"]},

    # Demo & trial
    {"name": "Demo Date", "dataType": "DATE", "fieldKey": "saas_demo_date"},
    {"name": "Demo Outcome", "dataType": "SINGLE_OPTIONS", "fieldKey": "saas_demo_outcome",
     "options": ["Strong interest","Needs to discuss","Not a fit","No-show","Rescheduled"]},
    {"name": "Trial Start Date", "dataType": "DATE", "fieldKey": "saas_trial_start"},
    {"name": "Trial Sub-Account ID", "dataType": "TEXT", "fieldKey": "saas_trial_subaccount"},
    {"name": "Plan Tier", "dataType": "SINGLE_OPTIONS", "fieldKey": "saas_plan",
     "options": ["Starter $500","Growth $1000","Scale $1500","Enterprise Custom"]},
    {"name": "MRR (CAD)", "dataType": "MONETORY", "fieldKey": "saas_mrr"},
    {"name": "Contract Signed Date", "dataType": "DATE", "fieldKey": "saas_contract_signed"},
    {"name": "Churn Risk Score", "dataType": "NUMERICAL", "fieldKey": "saas_churn_risk"},
]

# ═══════════════════════════════════════════════════════════════════
# TAGS — for the SaaS sales funnel
# ═══════════════════════════════════════════════════════════════════
TAGS = [
    # Lifecycle
    "nx-saas:new",
    "nx-saas:qualifying",
    "nx-saas:demo:scheduled",
    "nx-saas:demo:completed",
    "nx-saas:demo:no-show",
    "nx-saas:proposal:sent",
    "nx-saas:trial:active",
    "nx-saas:trial:expiring",
    "nx-saas:customer:paying",
    "nx-saas:customer:churning",
    "nx-saas:customer:churned",
    # Segmentation
    "nx-saas:segment:solo-rcic",
    "nx-saas:segment:small-firm",
    "nx-saas:segment:mid-firm",
    "nx-saas:segment:enterprise",
    # Tier
    "nx-saas:tier:starter",
    "nx-saas:tier:growth",
    "nx-saas:tier:scale",
    "nx-saas:tier:enterprise",
    # Flags
    "nx-saas:priority",
    "nx-saas:at-risk",
    "nx-saas:champion",
    "nx-saas:expansion-opp",
    # Demo marker
    "demo-data",
]

# ═══════════════════════════════════════════════════════════════════
# DEMO FIRMS — 3 realistic SaaS prospects
# ═══════════════════════════════════════════════════════════════════
DEMO_FIRMS = [
    {
        "firstName": "Chen", "lastName": "Park",
        "email": "chen.park@demo-maplecrestimmigration.ca",
        "phone": "+14162221001",
        "tags": ["nx-saas:customer:paying", "nx-saas:segment:small-firm", "nx-saas:tier:growth", "nx-saas:champion", "demo-data"],
        "firm": "Maplecrest Immigration Services",
        "website": "https://maplecrestimmigration.ca",
        "rcic_count": 4, "revenue": 650000, "province": "Ontario",
        "source": "LinkedIn", "score": 92,
        "role": "Managing Partner", "pain": "Lead response time",
        "plan": "Growth $1000", "mrr": 1000,
    },
    {
        "firstName": "Anjali", "lastName": "Singh",
        "email": "anjali@demo-vanimmigration.com",
        "phone": "+16042221002",
        "tags": ["nx-saas:trial:active", "nx-saas:segment:mid-firm", "nx-saas:tier:scale", "demo-data"],
        "firm": "Vancouver Immigration Partners",
        "website": "https://vanimmigration.com",
        "rcic_count": 8, "revenue": 1400000, "province": "British Columbia",
        "source": "Referral", "score": 85,
        "role": "Founder", "pain": "Pipeline visibility",
        "plan": "Scale $1500", "mrr": 0,
    },
    {
        "firstName": "Michel", "lastName": "Tremblay",
        "email": "mtremblay@demo-quebecimmi.ca",
        "phone": "+15142221003",
        "tags": ["nx-saas:demo:scheduled", "nx-saas:segment:solo-rcic", "nx-saas:priority", "demo-data"],
        "firm": "Tremblay & Associés Immigration",
        "website": "https://quebecimmi.ca",
        "rcic_count": 1, "revenue": 180000, "province": "Quebec",
        "source": "Google Ads", "score": 73,
        "role": "RCIC", "pain": "Consultation no-shows",
        "plan": "Starter $500", "mrr": 0,
    },
]


# ═══════════════════════════════════════════════════════════════════
# EXECUTE
# ═══════════════════════════════════════════════════════════════════

def get_existing_fields():
    r = httpx.get(f"{GHL}/locations/{NX_LOC}/customFields", headers=NX_HDR, timeout=15)
    return {f.get("fieldKey", "").replace("contact.", ""): f for f in r.json().get("customFields", [])}

def get_existing_tags():
    r = httpx.get(f"{GHL}/locations/{NX_LOC}/tags", headers=NX_HDR, timeout=15)
    return {t.get("name", "").lower() for t in r.json().get("tags", [])}


# STEP 1: Custom fields
print("\n[STEP 1] Creating 23 SaaS custom fields in NeuronX sub-account")
existing_fields = get_existing_fields()
created = skipped = failed = 0
for field in CUSTOM_FIELDS:
    key = field["fieldKey"]
    if key in existing_fields:
        skipped += 1
        continue
    try:
        r = httpx.post(f"{GHL}/locations/{NX_LOC}/customFields",
                       headers=NX_HDR, json=field, timeout=15)
        if r.status_code in (200, 201):
            created += 1
            print(f"  ✓ {field['name']} ({field['dataType']})")
        else:
            failed += 1
            print(f"  ✗ {field['name']}: [{r.status_code}] {r.text[:100]}")
    except Exception as e:
        failed += 1
        print(f"  ✗ {field['name']}: {e}")
print(f"\n  CREATED: {created}, SKIPPED: {skipped}, FAILED: {failed}")


# STEP 2: Tags
print(f"\n[STEP 2] Creating {len(TAGS)} SaaS tags")
existing_tags = get_existing_tags()
created = skipped = failed = 0
for tag_name in TAGS:
    if tag_name.lower() in existing_tags:
        skipped += 1
        continue
    try:
        r = httpx.post(f"{GHL}/locations/{NX_LOC}/tags",
                       headers=NX_HDR, json={"name": tag_name}, timeout=10)
        if r.status_code in (200, 201):
            created += 1
        else:
            failed += 1
    except Exception:
        failed += 1
print(f"  CREATED: {created}, SKIPPED: {skipped}, FAILED: {failed}")


# STEP 3: Demo firm contacts
print(f"\n[STEP 3] Creating {len(DEMO_FIRMS)} demo firm prospects")
for firm in DEMO_FIRMS:
    payload = {
        "locationId": NX_LOC,
        "firstName": firm["firstName"],
        "lastName": firm["lastName"],
        "email": firm["email"],
        "phone": firm["phone"],
        "tags": firm["tags"],
        "source": "demo-seed",
        "companyName": firm["firm"],
        "website": firm["website"],
        "customFields": [
            {"key": "firm_name", "field_value": firm["firm"]},
            {"key": "firm_website", "field_value": firm["website"]},
            {"key": "firm_rcic_count", "field_value": firm["rcic_count"]},
            {"key": "firm_revenue", "field_value": firm["revenue"]},
            {"key": "firm_province", "field_value": firm["province"]},
            {"key": "saas_lead_source", "field_value": firm["source"]},
            {"key": "saas_lead_score", "field_value": firm["score"]},
            {"key": "saas_dm_role", "field_value": firm["role"]},
            {"key": "saas_pain_point", "field_value": firm["pain"]},
            {"key": "saas_plan", "field_value": firm["plan"]},
            {"key": "saas_mrr", "field_value": firm["mrr"]},
        ],
    }
    try:
        r = httpx.post(f"{GHL}/contacts/", headers=NX_HDR, json=payload, timeout=15)
        if r.status_code in (200, 201):
            print(f"  ✓ {firm['firm']} ({firm['firstName']} {firm['lastName']}) — {firm['plan']}")
        elif r.status_code == 409 or "duplicate" in r.text.lower():
            print(f"  = {firm['firm']} (already exists)")
        else:
            print(f"  ✗ {firm['firm']}: [{r.status_code}] {r.text[:120]}")
    except Exception as e:
        print(f"  ✗ {firm['firm']}: {e}")


# SUMMARY
print("\n" + "=" * 80)
print("NEURONX SAAS-BUSINESS SETUP — COMPLETE (config side)")
print("=" * 80)
print("""
✅ Done via API:
   • 23 custom fields (firm profile, BANT, demo, trial, subscription, churn)
   • 24 tags (lifecycle, segment, tier, flags)
   • 3 demo firm prospects (small/mid/solo segments)

⚠️  PENDING (GHL pipeline API not accessible — 1-minute UI task):
   Create pipeline in NeuronX sub-account → Opportunities → Pipelines → Create:

   Pipeline: "NeuronX Sales"
   Stages (8):
     0. NEW LEAD
     1. QUALIFYING (BANT)
     2. DEMO SCHEDULED
     3. DEMO COMPLETED
     4. PROPOSAL SENT
     5. TRIAL ACTIVE (30 days)
     6. PAID CUSTOMER
     7. CHURNED

⚠️  OPTIONAL (for full SaaS sales automation):
   Workflows to build (can be done later, in UI or future snapshot):
     • NX-SAAS-01: New lead → qualification email
     • NX-SAAS-02: Demo booking → calendar + reminder
     • NX-SAAS-03: Demo follow-up (next-day)
     • NX-SAAS-04: Trial activation (snapshot deploy trigger)
     • NX-SAAS-05: Trial midpoint check-in (day 15)
     • NX-SAAS-06: Trial-to-paid conversion (day 30)
     • NX-SAAS-07: Monthly usage report
     • NX-SAAS-08: Churn-risk alert → renewal outreach
""")
