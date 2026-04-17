"""
Upload all generated email templates to GHL via VMC PIT.

Uses POST /emails/builder to create each template.
"""
import httpx
import json
from pathlib import Path

# Load config
with open("tools/ghl-lab/.pit-tokens.json") as f:
    pits = json.load(f)

VMC_TOKEN = pits["vmc"]["token"]
VMC_LOC = pits["vmc"]["locationId"]
HDR = {"Authorization": f"Bearer {VMC_TOKEN}", "Version": "2021-07-28"}
GHL = "https://services.leadconnectorhq.com"

BASE = Path(__file__).parent
manifest = json.loads((BASE / "manifest.json").read_text())

# List existing templates so we can update-in-place if slug matches (prefix: VMC-)
def list_existing():
    with httpx.Client(timeout=15) as c:
        r = c.get(f"{GHL}/emails/builder?locationId={VMC_LOC}&limit=100", headers=HDR)
    r.raise_for_status()
    return r.json().get("builders", [])


print("=" * 70)
print(f"UPLOAD EMAILS to VMC [{VMC_LOC}]")
print("=" * 70)

existing = list_existing()
existing_by_name = {e["name"].lower(): e for e in existing}
print(f"  Existing templates: {len(existing)}")

created = 0
updated = 0
failed = []

for tpl in manifest:
    slug = tpl["slug"]
    # Prefix for VMC to keep names consistent
    name = f"VMC-{slug}"
    html = Path(tpl["path"]).read_text()
    subject = tpl["subject"]

    payload = {
        "locationId": VMC_LOC,
        "title": name,
        "name": name,
        "type": "html",
        "html": html,
        "subject": subject,
    }

    match = existing_by_name.get(name.lower())
    try:
        if match:
            # Update
            eid = match["id"]
            with httpx.Client(timeout=30) as c:
                r = c.put(f"{GHL}/emails/builder/{eid}?locationId={VMC_LOC}",
                          headers={**HDR, "Content-Type": "application/json"},
                          json=payload)
            if r.status_code < 400:
                updated += 1
                print(f"  ↻ UPDATED: {name} ({eid[:12]}) — {r.status_code}")
            else:
                failed.append((name, f"UPDATE {r.status_code}: {r.text[:150]}"))
                print(f"  ✗ UPDATE FAILED: {name} — {r.status_code} {r.text[:100]}")
        else:
            # Create
            with httpx.Client(timeout=30) as c:
                r = c.post(f"{GHL}/emails/builder",
                           headers={**HDR, "Content-Type": "application/json"},
                           json=payload)
            if r.status_code < 400:
                created += 1
                new_id = r.json().get("redirect", "") or r.json().get("id", "")
                print(f"  + CREATED: {name} — {r.status_code}")
            else:
                failed.append((name, f"CREATE {r.status_code}: {r.text[:150]}"))
                print(f"  ✗ CREATE FAILED: {name} — {r.status_code} {r.text[:100]}")
    except Exception as e:
        failed.append((name, str(e)))
        print(f"  ✗ ERROR: {name} — {e}")

print()
print("=" * 70)
print(f"SUMMARY: {created} created, {updated} updated, {len(failed)} failed")
if failed:
    print("\nFailures:")
    for name, err in failed:
        print(f"  • {name}: {err[:100]}")
print("=" * 70)
