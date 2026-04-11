# NeuronX — Work Item Backlog (Target: Score 9+/10)

**Created**: 2026-04-11
**Current Score**: 7.1/10
**Target Score**: 9.0+/10
**Strategy**: Fix gaps in priority order of score impact

---

## SCORE BREAKDOWN (Current → Target)

| Dimension | Current | Target | Gap | How to Close |
|-----------|---------|--------|-----|-------------|
| Completeness | 7.5 | 9.5 | +2.0 | Fix Railway sync, GHL token, daily briefing, error handling |
| Quality | 7.0 | 9.0 | +2.0 | Professional icons, proper error responses, Chrome ext polish |
| UX | 6.5 | 9.0 | +2.5 | Typebot branding, avatar, theme, viewer fix, custom URL |
| Compliance | 8.5 | 9.5 | +1.0 | Already strong, minor: add consent logging |
| Maintainability | 8.0 | 9.0 | +1.0 | Backup Typebot form JSON, document all config |
| Deploy Readiness | 5.0 | 9.0 | +4.0 | E2E sandbox test, Railway sync, GHL token, prove it works |

---

## MASTER BACKLOG (Ordered by Score Impact)

### BLOCK A: Fix What's Broken (Score: 7.1 → 8.0)

| # | Work Item | Impact | Effort | Status |
|---|-----------|--------|--------|--------|
| A1 | Push code to GitHub (syncs Railway — 3 client endpoints) | Deploy +1.0 | 2 min | TODO |
| A2 | Generate professional NeuronX icon/avatar (replace ugly NX PNG) | UX +0.5 | 15 min | TODO |
| A3 | Fix Typebot viewer blank page (redeploy/debug Railway) | UX +1.0 | 30 min | TODO |
| A4 | Set Typebot bot name, avatar, favicon, custom URL | UX +0.5 | 20 min | TODO |
| A5 | Apply proper Typebot color theme (VMC brand, soothing palette) | UX +0.3 | 10 min | TODO |

### BLOCK B: Make It Production-Ready (Score: 8.0 → 8.7)

| # | Work Item | Impact | Effort | Status |
|---|-----------|--------|--------|--------|
| B1 | Add error handling to /clients/search (graceful 503 not 500) | Quality +0.3 | 10 min | TODO |
| B2 | Fix /score/lead dimension mapping (ai_ prefix fields) | Complete +0.3 | 20 min | TODO |
| B3 | Save Typebot form JSON backup to repo (disaster recovery) | Maintain +0.2 | 5 min | TODO |
| B4 | Add /clients/search graceful fallback when no GHL token | Quality +0.2 | 10 min | TODO |
| B5 | Build daily briefing endpoint (FC-NX-08) | Complete +0.3 | 1 hour | TODO |

### BLOCK C: Prove It Works — Sandbox E2E (Score: 8.7 → 9.0)

| # | Work Item | Impact | Effort | Status |
|---|-----------|--------|--------|--------|
| C1 | Dry-run E2E: Typebot submit → API webhook → GHL contact | Deploy +0.5 | 30 min | TODO |
| C2 | Dry-run E2E: Add tag via API → verify workflow triggers | Deploy +0.3 | 20 min | TODO |
| C3 | Dry-run E2E: Score lead → verify correct outcome/tags | Deploy +0.2 | 10 min | TODO |
| C4 | Test Chrome extension with demo contacts | Deploy +0.2 | 20 min | TODO |
| C5 | Document sandbox E2E results + confidence assessment | Deploy +0.3 | 15 min | TODO |

### BLOCK D: Polish & Scale (Score: 9.0 → 9.5)

| # | Work Item | Impact | Effort | Status |
|---|-----------|--------|--------|--------|
| D1 | Add analytics real data endpoints (FC-NX-07) | Complete +0.2 | 2 hours | TODO |
| D2 | Build consultation prep Typebot form | Complete +0.2 | 2 hours | TODO |
| D3 | Add IRCC form auto-fill to Chrome extension | Complete +0.2 | 3 hours | TODO |
| D4 | Operator work queue via GHL Smart Lists | Complete +0.1 | 1 hour | TODO |

---

## EXECUTION ORDER (This Session)

1. A2 — Professional icons (removes embarrassment factor)
2. A5 — Typebot color theme
3. A4 — Bot name, avatar, favicon, URL
4. A3 — Fix viewer blank page
5. B1-B4 — Code quality fixes
6. A1 — Push to GitHub (deploys everything)
7. B5 — Daily briefing endpoint
8. C1-C5 — Sandbox E2E testing
9. B3 — Backup form JSON

---

## $97 PLAN DECISION GATE

**Buy ONLY after ALL of these pass:**
- [ ] Typebot form renders and submits successfully
- [ ] NeuronX API creates GHL contact from webhook
- [ ] Scoring returns correct outcome
- [ ] Chrome extension loads and connects to API
- [ ] Briefing endpoint generates valid HTML
- [ ] At least 3 workflows trigger correctly via tag addition
- [ ] Sandbox E2E dry-run documented with evidence

**Then**: Buy $97 Starter plan (14-day free trial), test real email/SMS/phone, take Snapshot v3
