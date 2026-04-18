"""
Cleanup + rename GHL email templates in VMC.

What this does:
1. Archives 14 legacy duplicate templates (2 copies × 7 older versions)
2. Renames 26 premium templates to workflow-matched names
3. Verifies branding elements are present

GHL API:
- PATCH /emails/builder/{id} with {"locationId": ..., "name": ...} → rename
- PATCH /emails/builder/{id} with {"locationId": ..., "archived": true} → archive (hides from default list)

GHL doesn't support true DELETE via API; archive is the closest equivalent.

Idempotent — safe to run multiple times.
"""
import httpx
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
with open(ROOT / "tools/ghl-lab/.pit-tokens.json") as f:
    PITS = json.load(f)

VMC = PITS["vmc"]
HDR = {
    "Authorization": f"Bearer {VMC['token']}",
    "Version": "2021-07-28",
    "Content-Type": "application/json",
}
GHL = "https://services.leadconnectorhq.com"


# ── Rename plan: current slug → new workflow-matched name ─────────────
RENAMES = {
    # Intake funnel
    "VMC-01-inquiry-received":       "WF-01 · Inquiry Received (Welcome)",
    "VMC-02-outreach-attempt":       "WF-02 · Outreach Attempt (Missed AI Call)",
    "VMC-03-invite-booking":         "WF-04 · Invite to Book Consultation",
    "VMC-04-consultation-confirmed": "WF-05a · Booking Confirmed",
    "VMC-05-consultation-reminder":  "WF-05b · Consultation Reminder (Day Before)",
    "VMC-06-noshow-recovery":        "WF-06 · No-Show Recovery",
    "VMC-07-retainer-proposal":      "WF-09a · Retainer Proposal",
    "VMC-08-retainer-followup":      "WF-09b · Retainer Follow-Up",
    "VMC-09-score-medium-handler":   "WF-12 · Medium Score Nurture",
    "VMC-10-monthly-nurture":        "WF-11a · Monthly Nurture",
    "VMC-11-winback-nurture":        "WF-11b · Win-Back Nurture",
    "VMC-12-pipeda-ack":             "WF-13a · PIPEDA Acknowledgement",
    "VMC-13-pipeda-deleted":         "WF-13b · PIPEDA Data Deleted",
    "VMC-14-complex-case-alert":     "WF-04B · Complex Case Alert (Internal)",
    "VMC-26-missed-ai-call":         "WF-04C · Missed AI Call Recovery",

    # Case processing
    "VMC-15-case-onboarding":        "WF-CP-01 · Case Onboarding (Welcome)",
    "VMC-16-cp-docs-reminder":       "WF-CP-02 · Document Collection Reminder",
    "VMC-17-cp-form-prep":           "WF-CP-03 · Form Preparation Started",
    "VMC-18-cp-internal-review":     "WF-CP-04 · Internal Review in Progress",
    "VMC-19-cp-submitted":           "WF-CP-05 · Submitted to IRCC",
    "VMC-20-cp-status-update":       "WF-CP-06 · Monthly Status Update",
    "VMC-21-cp-rfi":                 "WF-CP-07 · IRCC Additional Info (RFI)",
    "VMC-22-cp-decision-approved":   "WF-CP-08a · Decision Approved 🎉",
    "VMC-23-cp-decision-refused":    "WF-CP-08b · Decision Refused",
    "VMC-24-cp-decision-withdrawn":  "WF-CP-08c · Decision Withdrawn",
    "VMC-25-cp-case-closed":         "WF-CP-09 · Case Closure",
}


def list_emails():
    r = httpx.get(
        f"{GHL}/emails/builder?locationId={VMC['locationId']}&limit=100",
        headers=HDR, timeout=15,
    )
    r.raise_for_status()
    return r.json().get("builders", [])


def patch_email(email_id: str, **fields):
    """PATCH a builder — name, archived, etc."""
    body = {"locationId": VMC["locationId"], **fields}
    r = httpx.patch(
        f"{GHL}/emails/builder/{email_id}",
        headers=HDR, json=body, timeout=15,
    )
    return r


def check_branding(email: dict) -> dict:
    """Fetch preview HTML + assert VMC branding present."""
    preview_url = email.get("previewUrl", "")
    if not preview_url:
        return {"ok": False, "reason": "no preview URL"}
    try:
        with httpx.Client(timeout=10, follow_redirects=True) as c:
            resp = c.get(preview_url)
        html = resp.text
        checks = {
            "primary_color_e8380d": "#E8380D" in html or "#e8380d" in html,
            "navy_0f172a":          "#0F172A" in html or "#0f172a" in html,
            "vmc_wordmark":         "Visa Master Canada" in html,
            "footer_address":       "Toronto" in html or "toronto" in html.lower(),
        }
        return {
            "ok": all(checks.values()),
            "checks": checks,
            "size": len(html),
        }
    except Exception as e:
        return {"ok": False, "reason": str(e)[:100]}


def main():
    print("=" * 70)
    print("EMAIL TEMPLATE CLEANUP + RENAME")
    print(f"Location: VMC {VMC['locationId']}")
    print("=" * 70)

    emails = list_emails()
    print(f"\nStart state: {len(emails)} templates")

    # ── Step 1: Archive legacy duplicates ──────────────────────────────
    print("\n[1] Archiving legacy duplicate templates...")
    legacy = [
        e for e in emails
        if not re.match(r"^(VMC-\d{2}-|WF-\d)", e["name"])
        and e["name"].lower().startswith("vmc-")
    ]
    print(f"  Found {len(legacy)} legacy templates to archive")

    archived = 0
    errors = []
    for e in legacy:
        time.sleep(0.3)  # rate limit buffer
        r = patch_email(e["id"], archived=True)
        if r.status_code == 200:
            archived += 1
            print(f"  ✓ Archived: {e['name']} ({e['id'][:12]})")
        else:
            errors.append((e["name"], r.status_code, r.text[:100]))
            print(f"  ✗ Failed: {e['name']} — {r.status_code}")

    # ── Step 2: Rename premium templates ───────────────────────────────
    print(f"\n[2] Renaming 26 premium templates to workflow-matched names...")
    emails = list_emails()  # refresh

    renamed = 0
    already = 0
    not_found = []
    for old_name, new_name in RENAMES.items():
        target = next((e for e in emails if e["name"] == old_name), None)
        # Also check if already renamed
        already_renamed = next((e for e in emails if e["name"] == new_name), None)
        if already_renamed:
            already += 1
            print(f"  = Already renamed: {new_name}")
            continue
        if not target:
            not_found.append(old_name)
            print(f"  ✗ Not found: {old_name}")
            continue
        time.sleep(0.3)
        r = patch_email(target["id"], name=new_name)
        if r.status_code == 200:
            renamed += 1
            print(f"  ✓ Renamed: {old_name}  →  {new_name}")
        else:
            errors.append((old_name, r.status_code, r.text[:100]))
            print(f"  ✗ Rename failed: {old_name} — {r.status_code}: {r.text[:100]}")

    # ── Step 3: Branding verification ──────────────────────────────────
    print(f"\n[3] Branding verification on all premium templates...")
    emails = list_emails()
    premium = [e for e in emails if e["name"].startswith("WF-")]
    print(f"  Inspecting {len(premium)} workflow-named templates")

    branding_issues = []
    for e in premium:
        result = check_branding(e)
        if not result.get("ok"):
            branding_issues.append({
                "name": e["name"],
                "reason": result.get("reason", "missing brand element"),
                "checks": result.get("checks", {}),
            })

    if branding_issues:
        print(f"  ⚠️  {len(branding_issues)} templates have branding gaps:")
        for bi in branding_issues[:10]:
            print(f"     {bi['name']}: {bi}")
    else:
        print(f"  ✓ All {len(premium)} templates pass brand checks (red #E8380D, navy #0F172A, VMC wordmark, Toronto footer)")

    # ── Summary ────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Archived legacy duplicates: {archived}")
    print(f"  Renamed premium templates: {renamed}")
    print(f"  Already renamed (no-op):   {already}")
    print(f"  Not found: {len(not_found)}")
    print(f"  Errors: {len(errors)}")
    print(f"  Branding issues: {len(branding_issues)}")

    emails_after = list_emails()
    visible = [e for e in emails_after if not e.get("archived")]
    print(f"\nFinal state: {len(emails_after)} total ({len(visible)} visible in GHL UI)")

    if not_found:
        print(f"\nNot found:")
        for n in not_found:
            print(f"  • {n}")
    if errors:
        print(f"\nErrors:")
        for name, code, msg in errors[:5]:
            print(f"  • {name}: [{code}] {msg}")


if __name__ == "__main__":
    main()
