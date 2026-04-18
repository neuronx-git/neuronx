"""
Re-upload the 26 premium template HTML bodies to GHL, matching by the new
workflow-aligned names (WF-01 ... WF-CP-09) rather than the old VMC-NN-* slugs.

This refreshes the HTML stored in GHL so the VMC logo, updated branding, and
any copy fixes take effect. Template IDs + names are preserved; only the
HTML body + subject + preview are replaced via PATCH.
"""
import httpx
import json
import time
from pathlib import Path

BASE = Path(__file__).parent
ROOT = BASE.parent.parent

with open(ROOT / "tools/ghl-lab/.pit-tokens.json") as f:
    PITS = json.load(f)
VMC = PITS["vmc"]
HDR = {
    "Authorization": f"Bearer {VMC['token']}",
    "Version": "2021-07-28",
    "Content-Type": "application/json",
}
GHL = "https://services.leadconnectorhq.com"

# Maps old slug → new workflow name (mirror of cleanup_and_rename.py)
RENAMES = {
    "01-inquiry-received":       "WF-01 · Inquiry Received (Welcome)",
    "02-outreach-attempt":       "WF-02 · Outreach Attempt (Missed AI Call)",
    "03-invite-booking":         "WF-04 · Invite to Book Consultation",
    "04-consultation-confirmed": "WF-05a · Booking Confirmed",
    "05-consultation-reminder":  "WF-05b · Consultation Reminder (Day Before)",
    "06-noshow-recovery":        "WF-06 · No-Show Recovery",
    "07-retainer-proposal":      "WF-09a · Retainer Proposal",
    "08-retainer-followup":      "WF-09b · Retainer Follow-Up",
    "09-score-medium-handler":   "WF-12 · Medium Score Nurture",
    "10-monthly-nurture":        "WF-11a · Monthly Nurture",
    "11-winback-nurture":        "WF-11b · Win-Back Nurture",
    "12-pipeda-ack":             "WF-13a · PIPEDA Acknowledgement",
    "13-pipeda-deleted":         "WF-13b · PIPEDA Data Deleted",
    "14-complex-case-alert":     "WF-04B · Complex Case Alert (Internal)",
    "15-case-onboarding":        "WF-CP-01 · Case Onboarding (Welcome)",
    "16-cp-docs-reminder":       "WF-CP-02 · Document Collection Reminder",
    "17-cp-form-prep":           "WF-CP-03 · Form Preparation Started",
    "18-cp-internal-review":     "WF-CP-04 · Internal Review in Progress",
    "19-cp-submitted":           "WF-CP-05 · Submitted to IRCC",
    "20-cp-status-update":       "WF-CP-06 · Monthly Status Update",
    "21-cp-rfi":                 "WF-CP-07 · IRCC Additional Info (RFI)",
    "22-cp-decision-approved":   "WF-CP-08a · Decision Approved 🎉",
    "23-cp-decision-refused":    "WF-CP-08b · Decision Refused",
    "24-cp-decision-withdrawn":  "WF-CP-08c · Decision Withdrawn",
    "25-cp-case-closed":         "WF-CP-09 · Case Closure",
    "26-missed-ai-call":         "WF-04C · Missed AI Call Recovery",
}


def list_existing():
    r = httpx.get(
        f"{GHL}/emails/builder?locationId={VMC['locationId']}&limit=100",
        headers=HDR, timeout=15,
    )
    r.raise_for_status()
    return r.json().get("builders", [])


def update_template(email_id: str, name: str, subject: str, html: str):
    """PATCH with full content replacement."""
    payload = {
        "locationId": VMC["locationId"],
        "name": name,
        "subject": subject,
        "html": html,
        "type": "html",
    }
    r = httpx.patch(
        f"{GHL}/emails/builder/{email_id}",
        headers=HDR, json=payload, timeout=30,
    )
    return r


def main():
    print("=" * 70)
    print("RE-UPLOAD TEMPLATES with VMC logo + refreshed HTML")
    print("=" * 70)

    manifest = json.loads((BASE / "manifest.json").read_text())
    existing = list_existing()
    by_name = {e["name"]: e for e in existing}

    print(f"\nManifest: {len(manifest)} templates")
    print(f"GHL existing (active): {len(existing)}")

    updated = 0
    skipped = 0
    errors = []

    for tpl in manifest:
        slug = tpl["slug"]
        new_name = RENAMES.get(slug)
        if not new_name:
            skipped += 1
            print(f"  ? No rename mapping for slug '{slug}' — skipping")
            continue

        target = by_name.get(new_name)
        if not target:
            skipped += 1
            print(f"  ? Not in GHL: '{new_name}' — skipping")
            continue

        html = Path(tpl["path"]).read_text()
        subject = tpl["subject"]

        time.sleep(0.4)  # rate limit buffer
        r = update_template(target["id"], new_name, subject, html)
        if r.status_code == 200:
            updated += 1
            # Verify logo is in the updated HTML
            has_logo = "vmc-logo" in html
            mark = "🖼 " if has_logo else "   "
            print(f"  {mark} ✓ {new_name}")
        else:
            errors.append((new_name, r.status_code, r.text[:150]))
            print(f"  ✗ {new_name} — [{r.status_code}] {r.text[:120]}")

    print("\n" + "=" * 70)
    print(f"UPDATED: {updated}, SKIPPED: {skipped}, FAILED: {len(errors)}")
    print("=" * 70)

    if errors:
        print("\nFailures:")
        for name, code, msg in errors:
            print(f"  • {name}: [{code}] {msg}")


if __name__ == "__main__":
    main()
