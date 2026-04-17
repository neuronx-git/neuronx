"""
Create 3 VMC calendars with proper team assignments.

1. Free Initial Assessment (15 min) — all RCICs + Intake Coordinator
2. Paid Consultation (30 min) — Senior + Junior RCICs
3. Strategy Session - Complex Cases (60 min) — Senior RCICs + Managing Partner

Run: python3 tools/ghl-lab/src/build_firm_calendars.py
"""
import httpx
import json
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
with open(ROOT / "tools/ghl-lab/.pit-tokens.json") as f:
    PITS = json.load(f)
with open(ROOT / "tools/ghl-lab/.team-users.json") as f:
    TEAM = json.load(f)

GHL = "https://services.leadconnectorhq.com"
VMC_LOC = PITS["vmc"]["locationId"]
VMC_HDR = {"Authorization": f"Bearer {PITS['vmc']['token']}", "Version": "2021-07-28",
           "Content-Type": "application/json"}

# Build email → user_id lookup
user_by_email = {}
for u in TEAM["users"]:
    if u.get("ghl_id"):
        user_by_email[u["email"].lower()] = u["ghl_id"]

def user_id(email_prefix):
    """Find user id by email prefix match."""
    for email, uid in user_by_email.items():
        if email_prefix.lower() in email.lower():
            return uid
    return None

# Map team members to assign
head_rcic = user_id("rajiv.mehta")
senior_rcic_1 = user_id("nina.patel")
senior_rcic_2 = user_id("michael.chen")
junior_rcic_1 = user_id("sarah.johnson")
junior_rcic_2 = user_id("arjun.kapoor")
intake = user_id("kwame.mensah")

# Open hours: Mon-Fri 9 AM - 5 PM ET — one entry per day as integers (1=Mon ... 5=Fri)
OPEN_HOURS = [
    {"daysOfTheWeek": [day],
     "hours": [{"openHour": 9, "openMinute": 0, "closeHour": 17, "closeMinute": 0}]}
    for day in [1, 2, 3, 4, 5]
]

def team_members_spec(user_ids, priority=1):
    """Build teamMembers array. Minimum viable format."""
    return [
        {"userId": uid, "priority": float(priority), "isPrimary": i == 0}
        for i, uid in enumerate(user_ids) if uid
    ]

CALENDARS = [
    {
        "name": "VMC — Free Initial Assessment",
        "description": "Complimentary 15-minute initial immigration consultation to assess your case and explain pathways.",
        "slotDuration": 15, "slotDurationUnit": "mins",
        "slotInterval": 15, "slotIntervalUnit": "mins",
        "slotBuffer": 5, "slotBufferUnit": "mins",
        "appoinmentPerSlot": 1, "appoinmentPerDay": 20,
        "widgetSlug": "vmc-free-assessment",
        "calendarType": "round_robin", "eventType": "RoundRobin_OptimizeForAvailability",
        "eventTitle": "Free Immigration Assessment - {{contact.name}}",
        "eventColor": "#E8380D",
        "team_ids": [senior_rcic_1, senior_rcic_2, junior_rcic_1, junior_rcic_2, intake],
    },
    {
        "name": "VMC — Paid Consultation",
        "description": "60-minute in-depth paid consultation with a Regulated Canadian Immigration Consultant (RCIC). Full case review and strategy session.",
        "slotDuration": 60, "slotDurationUnit": "mins",
        "slotInterval": 30, "slotIntervalUnit": "mins",
        "slotBuffer": 15, "slotBufferUnit": "mins",
        "appoinmentPerSlot": 1, "appoinmentPerDay": 6,
        "widgetSlug": "vmc-paid-consult",
        "calendarType": "round_robin", "eventType": "RoundRobin_OptimizeForAvailability",
        "eventTitle": "Paid Immigration Consultation - {{contact.name}}",
        "eventColor": "#0F172A",
        "team_ids": [senior_rcic_1, senior_rcic_2, junior_rcic_1, junior_rcic_2],
    },
    {
        "name": "VMC — Strategy Session (Complex Cases)",
        "description": "90-minute strategy session for complex immigration cases — refusals, appeals, inadmissibility, time-sensitive matters. Reserved for Senior RCICs.",
        "slotDuration": 90, "slotDurationUnit": "mins",
        "slotInterval": 30, "slotIntervalUnit": "mins",
        "slotBuffer": 30, "slotBufferUnit": "mins",
        "appoinmentPerSlot": 1, "appoinmentPerDay": 3,
        "widgetSlug": "vmc-strategy-session",
        "calendarType": "round_robin", "eventType": "RoundRobin_OptimizeForAvailability",
        "eventTitle": "Complex Case Strategy - {{contact.name}}",
        "eventColor": "#DC2626",
        "team_ids": [head_rcic, senior_rcic_1, senior_rcic_2],
    },
]


def list_calendars():
    r = httpx.get(f"{GHL}/calendars/?locationId={VMC_LOC}", headers=VMC_HDR, timeout=15)
    return r.json().get("calendars", []) if r.status_code == 200 else []


print("=" * 80)
print("BUILDING 3 CALENDARS with proper team assignments")
print("=" * 80)

existing = list_calendars()
existing_names = {c["name"].lower() for c in existing}
print(f"  Existing calendars: {len(existing)}")

created = 0
skipped = 0
failed = []

for cal in CALENDARS:
    if cal["name"].lower() in existing_names:
        skipped += 1
        print(f"  = {cal['name']} (exists)")
        continue

    team_ids = [uid for uid in cal.pop("team_ids") if uid]
    if not team_ids:
        failed.append((cal["name"], "No valid team members"))
        print(f"  ✗ {cal['name']} — no team members found")
        continue

    payload = {
        "locationId": VMC_LOC,
        "teamMembers": team_members_spec(team_ids),
        "openHours": OPEN_HOURS,
        "isActive": True,
        "autoConfirm": True,
        "allowReschedule": True,
        "allowCancellation": True,
        **cal,
    }

    time.sleep(1)
    r = httpx.post(f"{GHL}/calendars/", headers=VMC_HDR, json=payload, timeout=20)
    if r.status_code in (200, 201):
        cal_id = r.json().get("calendar", {}).get("id", "?")
        created += 1
        print(f"  ✓ Created '{cal['name']}' — id: {cal_id[:12]} — {len(team_ids)} team members")
    else:
        failed.append((cal['name'], f"[{r.status_code}] {r.text[:250]}"))
        print(f"  ✗ {cal['name']} — [{r.status_code}]")
        print(f"      {r.text[:250]}")

print()
print("=" * 80)
print(f"CREATED: {created}, SKIPPED: {skipped}, FAILED: {len(failed)}")
if failed:
    print("\nFailures:")
    for name, err in failed:
        print(f"  • {name}: {err}")
print("=" * 80)
