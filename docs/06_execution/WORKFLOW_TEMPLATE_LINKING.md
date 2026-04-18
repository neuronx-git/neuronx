# Workflow → Email Template Linking Guide

**Date**: 2026-04-18
**For**: Ranjan (founder — UI operator)
**Time estimate**: 30 min for all 24 workflows
**Prerequisite**: 26 premium templates uploaded to VMC with VMC logo (done 2026-04-18)

---

## Why this doc exists

GHL workflow "Send Email" actions can be configured two ways:

1. **Inline compose** — raw text typed directly into the action (what VMC currently uses)
2. **Use Template** — reference to a saved template in Email Builder (what we want)

The 26 premium Postmark-based templates are already uploaded to VMC and named `WF-XX · Description` so typing "WF-" in the template dropdown filters to exactly the right ones. This migration preserves all existing triggers/conditions/waits — only the email body reference changes.

**Why the UI is the only path**: `/workflows/{id}` returns 404 in GHL's public API. No PATCH endpoint for workflow actions exists. See `WORKFLOW_API_DISCOVERY.md` for evidence.

---

## Pre-flight checks

1. Open https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/emails/email-builder — confirm you see 26 templates named `WF-01 · …` through `WF-CP-09 · …`.
2. Open https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflows — confirm 24 workflows, all **Published**.
3. Send yourself a test email from any WF-* template to verify VMC logo renders correctly in Gmail.

---

## The 24 → 26 mapping

Some workflows have multiple Send Email actions (e.g., WF-05 has booking confirmation + day-before reminder; WF-CP-08 has approved/refused/withdrawn branches). Link each one to its matching template.

| # | Workflow (click to open) | Send Email action → Template to select |
|---|---|---|
| 1 | [WF-01 — Instant Lead Capture](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/e1de5e90-77ec-4358-8591-68e105632c60) | Welcome email → **WF-01 · Inquiry Received (Welcome)** |
| 2 | [WF-02 Contact Attempt Sequence](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/1b56da34-bdeb-4611-833d-26322823d51f) | Outreach email(s) → **WF-02 · Outreach Attempt** |
| 3 | [WF-03 Contact Success Handler](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/ab57e816-6584-4932-aa92-a09d3666f9ad) | *(internal routing — usually no outbound email; skip if no Send Email action)* |
| 4 | [WF-04 Readiness Complete Invite Booking](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/af73a980-247f-46b9-9fa5-db1a30a348f6) | Booking invite → **WF-04 · Invite to Book Consultation** |
| 5 | [WF-04B AI Call Receiver](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/3d5d96b1-41ff-4bde-9ef6-c9775e1ecb50) | Internal alert → **WF-04B · Complex Case Alert (Internal)** |
| 6 | [WF-04C Missed Call Recovery](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/da4e1076-b4fa-48c3-bacc-2b1eb2b605cc) | Recovery email → **WF-04C · Missed AI Call Recovery** |
| 7 | [WF-05 Appointment Booked Reminders](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/b069f33c-890b-4f29-9bc2-5ee5f5a3f75b) | **2 actions:** immediate confirmation → **WF-05a · Booking Confirmed**; day-before reminder → **WF-05b · Consultation Reminder (Day Before)** |
| 8 | [WF-06 No-Show Recovery](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/6cd73766-eb93-4809-a00a-1d52a7ba4b6e) | No-show outreach → **WF-06 · No-Show Recovery** |
| 9 | [WF-07 Consultation Outcome Capture](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/046772da-6b4a-4cdb-8b51-1c19334e9818) | *(data capture — usually no outbound email; skip if no Send Email action)* |
| 10 | [WF-08 Outcome Routing](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/cb1c723e-9c6b-4ff5-a77a-54a096b3ae6d) | *(pipeline routing — usually no outbound email; skip if no Send Email action)* |
| 11 | [WF-09 Retainer Follow-Up](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/93e66879-0d58-4843-ad62-e0721956e9ce) | **2 actions:** proposal send → **WF-09a · Retainer Proposal**; 3-day nudge → **WF-09b · Retainer Follow-Up** |
| 12 | [WF-10 Post-Consult Follow-Up](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/5ecd9d37-e123-499b-a524-1124a8036be9) | Post-consult nudge → **WF-09b · Retainer Follow-Up** (reuse — same copy fits) |
| 13 | [WF-11 Nurture Campaign Monthly](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/bca6784d-8b5d-4fb1-a26c-813adf16a2fc) | **2 actions:** monthly update → **WF-11a · Monthly Nurture**; inactive win-back → **WF-11b · Win-Back Nurture** |
| 14 | [WF-12 Score Med Handler](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/08af8eaf-215c-4432-8894-3ef55dcfc8c2) | Medium-score email → **WF-12 · Medium Score Nurture** |
| 15 | [WF-13 PIPEDA Data Deletion Request](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/c9359d6e-ae86-4242-bfc1-87d8e026f94e) | **2 actions:** acknowledgement → **WF-13a · PIPEDA Acknowledgement**; confirmation → **WF-13b · PIPEDA Data Deleted** |
| 16 | [WF-CP-01 Client Onboarding](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/147d613a-6988-428c-bcc1-dc0c669db452) | Welcome → **WF-CP-01 · Case Onboarding (Welcome)** |
| 17 | [WF-CP-02 Document Collection Reminders](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/79e5b266-e3d0-4aa6-9d7c-cd22c5119b45) | Docs reminder → **WF-CP-02 · Document Collection Reminder** |
| 18 | [WF-CP-03 Form Preparation](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/1ce015d3-c441-4398-9a6e-1993446f00ee) | Forms started → **WF-CP-03 · Form Preparation Started** |
| 19 | [WF-CP-04 Internal Review](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/c2109569-d6ce-4e9e-8a00-233f630ff560) | QA update → **WF-CP-04 · Internal Review in Progress** |
| 20 | [WF-CP-05 IRCC Submission](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/06582a80-dcbb-4647-a39a-49133d81de19) | Submitted → **WF-CP-05 · Submitted to IRCC** |
| 21 | [WF-CP-06 Processing Status Checks](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/09ed1d99-3cc4-48c5-81e8-b144f8aaaa6b) | Monthly status → **WF-CP-06 · Monthly Status Update** |
| 22 | [WF-CP-07 Additional Info (RFI)](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/b6345f68-07c7-4730-96f9-8474246ad450) | RFI alert → **WF-CP-07 · IRCC Additional Info (RFI)** |
| 23 | [WF-CP-08 Decision Received](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/11130465-2010-45f4-afee-e817171c3213) | **3 branches:** approved → **WF-CP-08a · Decision Approved 🎉**; refused → **WF-CP-08b · Decision Refused**; withdrawn → **WF-CP-08c · Decision Withdrawn** |
| 24 | [WF-CP-09 Case Closure](https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflow/edit/6e352a9f-1896-4154-98ec-61f6d35822e9) | Final package → **WF-CP-09 · Case Closure** |

**Total Send Email actions across 24 workflows: ~29** (WF-05, WF-09, WF-11, WF-13 have 2 each; WF-CP-08 has 3 branches).

---

## Step-by-step UI procedure (per workflow)

For each row in the table above:

1. **Click the workflow link** → workflow editor opens. If a "Draft/Published" modal appears, click **Edit** or press Escape.
2. **Find the Send Email action** — it's a rectangular node with an envelope icon labeled "Send Email". Click it.
3. The right drawer opens showing "Send Email" config. At the top, switch **From Scratch** / **Compose Email** tab → **Use Template** tab (the exact label varies by GHL UI version — look for the template dropdown).
4. **Click the template dropdown** → type `WF-` into the search. The list filters to the 26 candidates.
5. **Select the template** named in the table above.
6. Scroll down → confirm **Subject** is auto-populated from the template (it will be). Override if needed.
7. Click **Save Action** at the bottom of the drawer.
8. Top-right of workflow editor → click **Save** (the full workflow).
9. If workflow was **Published**, click the **Republish** button to apply the change to live runs.
10. Repeat for next Send Email action in the same workflow (WF-05, WF-09, WF-11, WF-13, WF-CP-08 have multiples).

**Save frequently.** GHL's workflow editor has lost in-flight edits before.

---

## Smoke test after linking

1. Go to https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/contacts → pick any DEMO contact.
2. Send yourself a test: from the contact page → Conversations → "+ New Email" → click the template picker → select **WF-01 · Inquiry Received (Welcome)** → click Send.
3. Check your Gmail Primary inbox. Verify:
   - ✅ VMC logo renders at top (centered, 160px wide)
   - ✅ Merge tags like `{{contact.first_name}}` were substituted with your name
   - ✅ Brand color is VMC red (#E8380D) on buttons, not Postmark blue
   - ✅ SPF/DKIM/DMARC pass (open email → ⋮ → "Show original" → all 3 should say PASS)
   - ✅ Lands in Primary, not Promotions

---

## Known merge tags in these templates

| Tag | Source |
|---|---|
| `{{contact.first_name}}`, `{{contact.last_name}}`, `{{contact.email}}`, `{{contact.phone}}` | Contact record |
| `{{contact.ai_program_interest}}`, `{{contact.case_id}}`, `{{contact.ircc_receipt_number}}` | Custom fields (140 total on VMC) |
| `{{appointment.start_date}}`, `{{appointment.start_time}}`, `{{appointment.meeting_url}}`, `{{appointment.reschedule_url}}`, `{{appointment.ics_url}}` | Set automatically when triggered from appointment events (WF-05, WF-06) |
| `{{user.name}}`, `{{user.email}}`, `{{user.phone}}` | Assigned user / RCIC |
| `{{location.name}}`, `{{location.address}}`, `{{location.phone}}` | VMC sub-account settings |
| `{{message.unsubscribe_url}}` | CASL compliance — always present |
| `{{nurture.month}}` | Custom — fill manually each month in WF-11a monthly nurture |

All are standard GHL Handlebars tags except `{{nurture.month}}` which needs monthly manual update.

---

## If something goes wrong

- **Template dropdown is empty when typing "WF-"** → templates aren't visible to the current user; switch to the VMC location explicitly via top-left location picker.
- **Subject has `{{contact.first_name}}` literal in preview** → correct; GHL substitutes at send time, not preview time.
- **Email lands in Promotions / Spam** → `mg.neuronx.co` SPF/DKIM/DMARC are all verified. If a recipient still routes to Promotions, their filter is aggressive; fix is individual recipient action, not our config.
- **Logo doesn't render (broken image)** → verify `https://neuronx-production-62f9.up.railway.app/static/vmc-logo.png` loads in your browser. If 404, Railway static middleware may be down — I'll fix server-side.

---

## When complete, tell me and I'll:

1. Run a live send-test via API to one demo contact
2. Verify all tags substitute correctly
3. Check SPF/DKIM/DMARC in message headers
4. Move to P0 #3 (PIPEDA disclosure to VAPI) and #4 (fix stale pipeline ID in `/analytics/pipeline`)
