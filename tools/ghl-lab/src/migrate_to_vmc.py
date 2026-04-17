"""
Migrate missing config from SANDBOX → VMC (new production).

What this script does:
  1. Fetches all custom fields from sandbox (OAuth)
  2. Fetches all tags from sandbox
  3. Fetches Case Processing pipeline from sandbox
  4. Creates each missing one in VMC (PIT)
  5. Reports what was created / already-existed / failed

Safe to run multiple times (idempotent — skips existing items).
"""
import httpx
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
with open(ROOT / "tools/ghl-lab/.tokens.json") as f:
    OAUTH = json.load(f)
with open(ROOT / "tools/ghl-lab/.pit-tokens.json") as f:
    PITS = json.load(f)

SANDBOX_LOC = OAUTH["locationId"]
SANDBOX_HDR = {"Authorization": f"Bearer {OAUTH['access_token']}", "Version": "2021-07-28"}

VMC_LOC = PITS["vmc"]["locationId"]
VMC_HDR = {"Authorization": f"Bearer {PITS['vmc']['token']}", "Version": "2021-07-28",
           "Content-Type": "application/json"}

GHL = "https://services.leadconnectorhq.com"

print("=" * 80)
print(f"MIGRATE: SANDBOX [{SANDBOX_LOC}] → VMC [{VMC_LOC}]")
print("=" * 80)


def get_all(loc, hdr, path_template, arr_key):
    """Fetch a resource list."""
    url = f"{GHL}{path_template.format(loc=loc)}"
    with httpx.Client(timeout=15) as c:
        r = c.get(url, headers=hdr)
    if r.status_code == 200:
        return r.json().get(arr_key, [])
    return []


# ── STEP 1: CUSTOM FIELDS ────────────────────────────────────────────
print("\n[STEP 1] Custom Fields")
sandbox_fields = get_all(SANDBOX_LOC, SANDBOX_HDR, "/locations/{loc}/customFields", "customFields")
vmc_fields = get_all(VMC_LOC, VMC_HDR, "/locations/{loc}/customFields", "customFields")

vmc_field_keys = {f.get("fieldKey", "").replace("contact.", "") for f in vmc_fields}
vmc_field_names = {f.get("name", "").lower() for f in vmc_fields}

print(f"  Sandbox: {len(sandbox_fields)} | VMC: {len(vmc_fields)}")

missing_fields = [
    f for f in sandbox_fields
    if f.get("fieldKey", "").replace("contact.", "") not in vmc_field_keys
    and f.get("name", "").lower() not in vmc_field_names
]
print(f"  Missing in VMC: {len(missing_fields)}")

created_fields = 0
failed_fields = []
for f in missing_fields:
    name = f.get("name", "")
    field_key = f.get("fieldKey", "").replace("contact.", "")
    data_type = f.get("dataType", "TEXT")
    # Build create payload
    payload = {
        "name": name,
        "dataType": data_type,
        "fieldKey": field_key,
    }
    # For option-based fields, add options
    if data_type in ("SINGLE_OPTIONS", "MULTIPLE_OPTIONS", "CHECKBOX", "RADIO"):
        opts = f.get("picklistOptions", [])
        if opts:
            # GHL API expects options as string array
            payload["options"] = [o.get("value", o) if isinstance(o, dict) else o for o in opts]
    if "placeholder" in f:
        payload["placeholder"] = f["placeholder"]

    try:
        with httpx.Client(timeout=15) as c:
            r = c.post(f"{GHL}/locations/{VMC_LOC}/customFields",
                       headers=VMC_HDR, json=payload)
        if r.status_code in (200, 201):
            created_fields += 1
            print(f"  ✓ {name} ({data_type})")
        else:
            failed_fields.append((name, r.status_code, r.text[:100]))
    except Exception as e:
        failed_fields.append((name, "EXC", str(e)[:100]))

print(f"\n  CREATED: {created_fields}, FAILED: {len(failed_fields)}")
if failed_fields:
    print("  Failures:")
    for n, code, err in failed_fields[:10]:
        print(f"    ✗ {n}: [{code}] {err}")


# ── STEP 2: TAGS ─────────────────────────────────────────────────────
print("\n[STEP 2] Tags")
sandbox_tags = get_all(SANDBOX_LOC, SANDBOX_HDR, "/locations/{loc}/tags", "tags")
vmc_tags = get_all(VMC_LOC, VMC_HDR, "/locations/{loc}/tags", "tags")

vmc_tag_names = {t.get("name", "").lower() for t in vmc_tags}
missing_tags = [t for t in sandbox_tags if t.get("name", "").lower() not in vmc_tag_names]
print(f"  Sandbox: {len(sandbox_tags)} | VMC: {len(vmc_tags)}")
print(f"  Missing in VMC: {len(missing_tags)}")

created_tags = 0
failed_tags = []
for t in missing_tags:
    name = t.get("name", "")
    try:
        with httpx.Client(timeout=15) as c:
            r = c.post(f"{GHL}/locations/{VMC_LOC}/tags",
                       headers=VMC_HDR, json={"name": name})
        if r.status_code in (200, 201):
            created_tags += 1
        else:
            failed_tags.append((name, r.status_code, r.text[:80]))
    except Exception as e:
        failed_tags.append((name, "EXC", str(e)[:80]))

print(f"  CREATED: {created_tags}, FAILED: {len(failed_tags)}")
if failed_tags:
    for n, code, err in failed_tags[:5]:
        print(f"    ✗ {n}: [{code}] {err}")


# ── STEP 3: PIPELINES ────────────────────────────────────────────────
print("\n[STEP 3] Pipelines")
sandbox_pipes = get_all(SANDBOX_LOC, SANDBOX_HDR, "/opportunities/pipelines?locationId={loc}", "pipelines")
vmc_pipes = get_all(VMC_LOC, VMC_HDR, "/opportunities/pipelines?locationId={loc}", "pipelines")

vmc_pipe_names = {p.get("name", "").lower() for p in vmc_pipes}
missing_pipes = [p for p in sandbox_pipes if p.get("name", "").lower() not in vmc_pipe_names]
print(f"  Sandbox: {len(sandbox_pipes)} | VMC: {len(vmc_pipes)}")
print(f"  Missing in VMC: {len(missing_pipes)}")

# Pipeline create API is limited in GHL — usually requires specific format
# Best attempt:
for p in missing_pipes:
    name = p.get("name", "")
    stages = p.get("stages", [])
    payload = {
        "name": name,
        "locationId": VMC_LOC,
        "stages": [{"name": s.get("name", ""), "position": s.get("position", i)}
                   for i, s in enumerate(stages)],
    }
    try:
        with httpx.Client(timeout=15) as c:
            r = c.post(f"{GHL}/opportunities/pipelines",
                       headers=VMC_HDR, json=payload)
        if r.status_code in (200, 201):
            print(f"  ✓ CREATED pipeline: {name} ({len(stages)} stages)")
        else:
            print(f"  ✗ FAILED pipeline: {name} — [{r.status_code}] {r.text[:150]}")
    except Exception as e:
        print(f"  ✗ EXCEPTION: {name} — {e}")


# ── SUMMARY ──────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("POST-MIGRATION STATE")
print("=" * 80)
after_fields = get_all(VMC_LOC, VMC_HDR, "/locations/{loc}/customFields", "customFields")
after_tags = get_all(VMC_LOC, VMC_HDR, "/locations/{loc}/tags", "tags")
after_pipes = get_all(VMC_LOC, VMC_HDR, "/opportunities/pipelines?locationId={loc}", "pipelines")
print(f"  Custom Fields: {len(vmc_fields)} → {len(after_fields)}")
print(f"  Tags: {len(vmc_tags)} → {len(after_tags)}")
print(f"  Pipelines: {len(vmc_pipes)} → {len(after_pipes)}")
