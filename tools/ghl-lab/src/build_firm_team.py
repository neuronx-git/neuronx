"""
Build the complete VMC firm team — 9 users for a realistic 5-10 person immigration firm.

Team hierarchy (per memory/feedback_agent_working_model.md):
1. Managing Partner / Head RCIC — admin, full access
2. Senior RCIC × 2 — consultant work
3. Junior RCIC × 2 — consultation, managed cases
4. Client Success Manager — post-sale, retention
5. Sales Development Rep — lead qualification
6. Operations Manager — admin, reporting, compliance
7. Intake Coordinator — first-response, form triage

All users are "DEMO - " prefixed for easy identification.

Run: python3 tools/ghl-lab/src/build_firm_team.py
"""
import httpx
import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
with open(ROOT / "tools/ghl-lab/.pit-tokens.json") as f:
    PITS = json.load(f)

GHL = "https://services.leadconnectorhq.com"
VMC_LOC = PITS["vmc"]["locationId"]
COMPANY = PITS["agency"]["companyId"]
VMC_HDR = {"Authorization": f"Bearer {PITS['vmc']['token']}", "Version": "2021-07-28",
           "Content-Type": "application/json"}

# 9-person best-in-class immigration firm
TEAM = [
    # ── Leadership ──
    {
        "firstName": "DEMO - Rajiv", "lastName": "Mehta",
        "email": "rajiv.mehta@demo.visamasters.ca",
        "phone": "+14165559001",
        "type": "account", "role": "admin",
        "title": "Managing Partner / Head RCIC",
        "license": "R123456",
        "perms": "admin",
    },
    # ── Senior RCICs ──
    {
        "firstName": "DEMO - Nina", "lastName": "Patel",
        "email": "nina.patel@demo.visamasters.ca",
        "phone": "+14165559002",
        "type": "account", "role": "user",
        "title": "Senior RCIC Consultant",
        "license": "R234567",
        "perms": "senior_rcic",
    },
    {
        "firstName": "DEMO - Michael", "lastName": "Chen",
        "email": "michael.chen@demo.visamasters.ca",
        "phone": "+14165559003",
        "type": "account", "role": "user",
        "title": "Senior RCIC Consultant",
        "license": "R345678",
        "perms": "senior_rcic",
    },
    # ── Junior RCICs ──
    {
        "firstName": "DEMO - Sarah", "lastName": "Johnson",
        "email": "sarah.johnson@demo.visamasters.ca",
        "phone": "+14165559004",
        "type": "account", "role": "user",
        "title": "Junior RCIC Consultant",
        "license": "R456789",
        "perms": "junior_rcic",
    },
    {
        "firstName": "DEMO - Arjun", "lastName": "Kapoor",
        "email": "arjun.kapoor@demo.visamasters.ca",
        "phone": "+14165559005",
        "type": "account", "role": "user",
        "title": "Junior RCIC Consultant",
        "license": "R567890",
        "perms": "junior_rcic",
    },
    # ── Non-RCIC operations ──
    {
        "firstName": "DEMO - Emily", "lastName": "Brooks",
        "email": "emily.brooks@demo.visamasters.ca",
        "phone": "+14165559006",
        "type": "account", "role": "user",
        "title": "Client Success Manager",
        "perms": "csm",
    },
    {
        "firstName": "DEMO - James", "lastName": "Rodriguez",
        "email": "james.rodriguez@demo.visamasters.ca",
        "phone": "+14165559007",
        "type": "account", "role": "user",
        "title": "Sales Development Rep",
        "perms": "sdr",
    },
    {
        "firstName": "DEMO - Priya", "lastName": "Sharma",
        "email": "priya.sharma.ops@demo.visamasters.ca",
        "phone": "+14165559008",
        "type": "account", "role": "admin",
        "title": "Operations Manager",
        "perms": "ops",
    },
    {
        "firstName": "DEMO - Kwame", "lastName": "Mensah",
        "email": "kwame.mensah@demo.visamasters.ca",
        "phone": "+14165559009",
        "type": "account", "role": "user",
        "title": "Intake Coordinator",
        "perms": "intake",
    },
]

# Permission templates by role
PERMISSIONS = {
    "admin": {
        "contactsEnabled": True, "campaignsEnabled": True, "workflowsEnabled": True,
        "triggersEnabled": True, "funnelsEnabled": True, "websitesEnabled": True,
        "opportunitiesEnabled": True, "dashboardStatsEnabled": True, "appointmentsEnabled": True,
        "reviewsEnabled": True, "onlineListingsEnabled": True, "phoneCallEnabled": True,
        "conversationsEnabled": True, "assignedDataOnly": False, "adwordsReportingEnabled": True,
        "membershipEnabled": True, "facebookAdsReportingEnabled": True,
        "attributionsReportingEnabled": True, "settingsEnabled": True, "tagsEnabled": True,
        "leadValueEnabled": True, "marketingEnabled": True,
        "bulkRequestsEnabled": True, "invoiceEnabled": True,
    },
    "senior_rcic": {
        "contactsEnabled": True, "conversationsEnabled": True, "opportunitiesEnabled": True,
        "appointmentsEnabled": True, "phoneCallEnabled": True, "tagsEnabled": True,
        "assignedDataOnly": False, "invoiceEnabled": True, "dashboardStatsEnabled": True,
    },
    "junior_rcic": {
        "contactsEnabled": True, "conversationsEnabled": True, "opportunitiesEnabled": True,
        "appointmentsEnabled": True, "phoneCallEnabled": True, "tagsEnabled": True,
        "assignedDataOnly": True,
    },
    "csm": {
        "contactsEnabled": True, "conversationsEnabled": True, "campaignsEnabled": True,
        "opportunitiesEnabled": True, "appointmentsEnabled": True, "phoneCallEnabled": True,
        "tagsEnabled": True, "assignedDataOnly": False,
    },
    "sdr": {
        "contactsEnabled": True, "conversationsEnabled": True, "opportunitiesEnabled": True,
        "appointmentsEnabled": True, "phoneCallEnabled": True, "tagsEnabled": True,
        "assignedDataOnly": True,
    },
    "ops": {
        "contactsEnabled": True, "campaignsEnabled": True, "workflowsEnabled": True,
        "triggersEnabled": True, "opportunitiesEnabled": True, "dashboardStatsEnabled": True,
        "appointmentsEnabled": True, "phoneCallEnabled": True, "conversationsEnabled": True,
        "assignedDataOnly": False, "settingsEnabled": True, "tagsEnabled": True,
    },
    "intake": {
        "contactsEnabled": True, "conversationsEnabled": True, "opportunitiesEnabled": True,
        "appointmentsEnabled": True, "phoneCallEnabled": True, "tagsEnabled": True,
        "assignedDataOnly": False,
    },
}


def list_existing_users():
    r = httpx.get(f"{GHL}/users/search?companyId={COMPANY}&locationId={VMC_LOC}",
                  headers=VMC_HDR, timeout=15)
    if r.status_code == 200:
        return r.json().get("users", [])
    # Fallback
    r = httpx.get(f"{GHL}/users/?locationId={VMC_LOC}", headers=VMC_HDR, timeout=15)
    return r.json().get("users", []) if r.status_code == 200 else []


def create_user(member):
    """Create one team member with proper permissions."""
    perms = PERMISSIONS.get(member["perms"], PERMISSIONS["junior_rcic"])
    payload = {
        "companyId": COMPANY,
        "firstName": member["firstName"],
        "lastName": member["lastName"],
        "email": member["email"],
        "phone": member["phone"],
        "password": "NeuronxDemo2026!Secure",
        "type": member["type"],
        "role": member["role"],
        "locationIds": [VMC_LOC],
        "permissions": perms,
    }
    r = httpx.post(f"{GHL}/users/", headers=VMC_HDR, json=payload, timeout=20)
    return r


print("=" * 80)
print(f"BUILDING FIRM TEAM — 9 members")
print(f"Location: {VMC_LOC}")
print("=" * 80)

existing = list_existing_users()
existing_emails = {u.get("email", "").lower() for u in existing}
print(f"  Existing users in VMC: {len(existing)}")

created = []
skipped = []
failed = []
created_ids = {}  # email → user_id

for m in TEAM:
    if m["email"].lower() in existing_emails:
        skipped.append(m["email"])
        print(f"  = {m['title']:<40} ({m['email']})")
        continue
    time.sleep(1.5)  # rate limit buffer
    r = create_user(m)
    if r.status_code in (200, 201):
        uid = r.json().get("id", "?")
        created.append({"email": m["email"], "id": uid, "title": m["title"]})
        created_ids[m["email"]] = uid
        print(f"  ✓ {m['title']:<40} (id: {uid[:12]})")
    else:
        failed.append((m["email"], r.status_code, r.text[:200]))
        print(f"  ✗ {m['title']:<40} [{r.status_code}] {r.text[:150]}")

print()
print("=" * 80)
print(f"CREATED: {len(created)}, SKIPPED: {len(skipped)}, FAILED: {len(failed)}")
if failed:
    print("\nFailures:")
    for e, s, t in failed:
        print(f"  {e}: [{s}] {t}")
print("=" * 80)

# Write user mapping for downstream scripts
(ROOT / "tools/ghl-lab/.team-users.json").write_text(
    json.dumps({
        "vmc_location": VMC_LOC,
        "users": [{**m, "ghl_id": created_ids.get(m["email"])} for m in TEAM if m["email"] in created_ids]
                 + [{"email": e, "ghl_id": None, "exists": True} for e in skipped],
    }, indent=2, default=str)
)
print(f"\n✓ Team map written to tools/ghl-lab/.team-users.json")
