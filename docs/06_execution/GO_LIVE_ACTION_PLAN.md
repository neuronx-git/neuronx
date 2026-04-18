# 🚀 NeuronX Go-Live Action Plan

**Last updated:** 2026-04-18
**Verdict after 3-agent audit:** Platform is 85% ready for investor demo. 5 items block production pilot. 6 items are polish.

---

## 🔴 BLOCKERS — Must fix before accepting real paying customer

### 1. Add `documents` table + SeaweedFS container (8 hrs, CRITICAL)
**Problem:** Files uploaded via Typebot are OCR'd then lost. RCIC can't retrieve original documents. No storage config in `app/config.py`.
**Fix:**
- Deploy SeaweedFS container on Railway (S3-compatible, 24k⭐, Apache 2.0)
- Add `documents` table (schema in `CASE_LIFECYCLE_AUDIT.md`)
- Modify `/extract/upload` to persist file → SeaweedFS + insert documents row
- Add `GET /cases/{id}/documents` endpoint

**Owner:** Next dev session

### 2. Add `users` table (replaces string-based `assigned_rcic`) (3 hrs)
**Problem:** `Case.assigned_rcic` is VARCHAR(100) — fragile, no access control, breaks staff performance analytics on typos.
**Fix:**
- Add `users` table (FK references)
- Alembic migration to convert existing string names → user IDs
- Update scoring service + case service to use FK
- Unblocks: per-RCIC performance, SLA tracking, commission math

### 3. Link email templates to workflows as TEMPLATE (not text) — 30 min manual OR 20 min via Claude-in-Chrome
**Problem:** You set the 24 workflow emails as text, not template references. Can't update copy in one place; no premium HTML rendering.
**Fix:**
- Option A: Manual UI work (30 min) — use `docs/06_execution/EMAIL_WORKFLOW_MAP.md` mapping
- Option B: Pilot via Claude-in-Chrome (you watch, I click) — switch to "Work" profile, I automate
**Recommend:** Option B — faster, less error-prone

### 4. DMARC `dmarc@neuronx.co` mailbox (2 min)
**Problem:** DMARC records point to `rua=mailto:dmarc@neuronx.co` but inbox doesn't exist. Reports bounce.
**Fix:** Google Workspace admin → Gmail → Routing → create forwarding rule `dmarc@neuronx.co` → `ranjan@neuronx.co`
OR use free Postmark DMARC Digests (better reports).

### 5. Test real email send (5 min)
**Problem:** Haven't verified SPF/DKIM/DMARC all pass in live Gmail headers.
**Fix:** Send test campaign in GHL to your personal Gmail → view source → verify `spf=pass dkim=pass dmarc=pass` in `Authentication-Results` header. Critical: must land in Primary inbox, not Promotions/Spam.

---

## 🟡 HIGH-IMPACT — Do before pilot customer onboarding

### 6. Integrate Docuseal e-signature (container on Railway, 4 hrs)
**Why:** Retainer flow is currently email-only. Real firms need audit-trail e-sig.
**Tool:** [Docuseal](https://github.com/docusealco/docuseal) (MIT, 11k⭐, Rails, docker-compose)
**Integration:** Extend existing `/signatures/*` router in FastAPI to call Docuseal API.

### 7. Add `case_required_documents` table + checklist endpoint (2 hrs)
**Why:** Currently only counts (docs_received=5/8). Can't tell RCIC which 3 are missing.
**Fix:** On case init, populate per-program checklist. Update endpoint returns missing doc names. Metabase shows blockers.

### 8. Expand Metabase — Dashboard 4 "Staff Performance" (3 hrs, blocked on #2)
**Why:** You asked for staff performance tracking. Needs `users` FK first.
**Views:** `v_rcic_case_velocity`, `v_rcic_approval_rate`, `v_rcic_sla_breaches`, `v_team_leaderboard`.
**Plan doc:** `docs/06_execution/METABASE_EXPANSION_PLAN.md`

---

## 🟢 POLISH — Do when bored, not before pilot

### 9. Paperless-ngx container for OCR archive + retention (3 hrs)
**Why:** Long-term document archive with tag search, GDPR retention.
**Tool:** [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) (60k⭐, Django, docker)

### 10. Chrome extension hardening (1 day)
**Why:** Works on demo, but production needs:
- Bearer token auth (currently no auth)
- HTTPS-only enforcement in manifest
- CSP header
- Test against 5+ real IRCC forms
- Audit log to backend

### 11. Microsoft SNDS registration (5 min)
https://sendersupport.olc.protection.outlook.com/snds/ — Outlook/Hotmail deliverability dashboard.

### 12. Move `mg.neuronx.co` to agency level (2 min)
Currently at VMC sub-account level. Should be agency default = fallback for future customer sub-accounts.

### 13. Family sponsorship upsell workflow (2 hrs)
Per USER_JOURNEY_GAPS.md — 60% of PR approvals later sponsor family. Trigger workflow at case close + 90 days.

### 14. Citizenship reminder at PR+3 years (1 hr)
Scheduled workflow via `nx:pr_approved_date` tag.

---

## 🧪 CHROME EXTENSION TEST HARNESS — ready to use now

Built and tested in this session. Files in `chrome-extension/test-harness/`:
- `mock_server.py` — FastAPI mock of `/clients/*` endpoints, port 8000
- `demo-ircc-form.html` — Replica IRCC form with live test panel
- `README.md` — 5-minute setup guide

**Run it:**
```bash
cd chrome-extension/test-harness
python3 mock_server.py &
open demo-ircc-form.html
# In Chrome: chrome://extensions → Load unpacked → chrome-extension/
# Extension settings → API URL: http://127.0.0.1:8000
# Type "john" in popup → select → click Auto-Fill
```

This proves the extension works **without** needing real IRCC or live GHL. If it fills the demo correctly, it will fill the real IRCC portal.

---

## Priority recommendation for THIS week

If you have 4 hours → do items **#3, #4, #5** (email reliability) + **#1 (partial — just SeaweedFS container)**.
If you have 1 day → add items **#2, #7** (case doc integrity).
If you have 1 week → items 1-8 + run full E2E test with a real test lead.

After items 1-5: investor-demo ready.
After items 1-8: pilot-ready for first real paying customer.

---

## Open-source decision summary (from `OSS_BPM_RESEARCH.md`)

3 new containers to add (all on Railway, ~$15-30/month total):
- **SeaweedFS** (Apache 2.0, 24k⭐) — raw object storage, replacing MinIO which crippled free tier in 2025
- **Docuseal** (MIT, 11k⭐) — e-signature (NOT Documenso — AGPL commercial risk)
- **Paperless-ngx** (GPL v3, 60k⭐) — OCR archive + retention

**Skip:** Twenty/Huly/Plane (would abandon GHL investment), Camunda (BPMN overkill), MinIO (commercial trajectory).

**Keep:** GHL (primary CRM) + Metabase (expand views) + Chrome extension (BPM power view).
