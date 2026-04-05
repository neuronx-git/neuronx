# NeuronX Open-Source Integration Stack

**Date**: 2026-04-01
**Status**: CANONICAL — All integration decisions documented here
**Rule**: Add tools one at a time, only when a proven need exists. Never batch-install.

---

## Architecture Overview

```
                    ┌─────────────────────────────────────────┐
                    │           GHL (System of Record)         │
                    │  Pipeline · Workflows · Calendar · CRM   │
                    └──────────────┬──────────────────────────┘
                                   │ Webhooks + API
                    ┌──────────────▼──────────────────────────┐
                    │        NeuronX FastAPI (Railway)          │
                    │  /webhooks · /score · /briefing · /trust  │
                    │  /analytics · /documents · /signatures    │
                    └──┬───────┬──────────┬───────────┬───────┘
                       │       │          │           │
              ┌────────▼──┐  ┌─▼────────┐ ┌▼─────────┐ ┌▼──────────┐
              │   VAPI     │  │PostgreSQL│ │Documenso │ │Docxtpl    │
              │  Voice AI  │  │  + sync  │ │ E-Sign   │ │ Doc Gen   │
              └────────────┘  └────┬─────┘ └──────────┘ └───────────┘
                                   │
                              ┌────▼─────┐
                              │ Metabase  │
                              │ Analytics │
                              └──────────┘

         ┌──────────────────────────────────────────────────┐
         │            Next.js + Vercel (neuronx.co)          │
         │  Marketing Site · Client Portal · Metabase Embed  │
         └──────────────────────────────────────────────────┘
```

---

## Tool Decisions

### APPROVED — Build in sequence

| # | Tool | Purpose | Deploy | Phase | Cost |
|---|------|---------|--------|-------|------|
| 1 | **Railway** | FastAPI hosting (always-on) | PaaS | Now | $5-20/mo |
| 2 | **PostgreSQL** | Data sync + analytics store | Railway add-on | Now | Included |
| 3 | **Docxtemplater** (python-docx-template) | Auto-generate retainer/consultation docs | Python library in FastAPI | Phase 1 | Free |
| 4 | **Metabase** | Pipeline analytics dashboards | Railway Docker | Phase 1 | Free OSS |
| 5 | **Next.js + Vercel** | neuronx.co website + client portal | Vercel | Phase 1 | Free tier |
| 6 | **Documenso** | E-signature for retainers | Railway Docker | Phase 2 | Free OSS |
| 7 | **Plausible** | Privacy-first website analytics | Script tag or Railway | Phase 2 | $9/mo cloud or free self-hosted |

### REJECTED — Do not add

| Tool | Reason |
|------|--------|
| **Odoo** | Full ERP — massive overlap with GHL, 2-4 week integration, maintenance burden. Violates Rule 8 (minimalist architecture). No production-grade immigration module exists. |
| **Nextcloud** | GHL has native document uploads via Client Portal + CRM. S3 is lighter if external storage needed. |
| **Twenty CRM / SuiteCRM** | GHL is already the CRM. Build custom analytics in FastAPI + Metabase instead of second CRM. |
| **Make.com / n8n** | Rule 8: NeuronX FastAPI IS the orchestration layer. No third-party middleware unless concrete blocker proven. |

---

## Phase 1 Integration Details

### 1. Docxtemplater (python-docx-template)

**What**: Generate .docx documents from templates with GHL contact data.

**Templates to create**:
1. Retainer Agreement — fees, scope, terms
2. Consultation Prep Packet — document checklist, program overview
3. Assessment Report — R1-R5 results, recommendation
4. Engagement Letter — formal offer

**Integration**:
```python
# Add to requirements.txt
docxtpl>=0.18.0

# New endpoint in neuronx-api
POST /documents/generate
  Body: { template: "retainer", contact_id: "abc123" }
  Returns: .docx file
```

**FastAPI endpoint** pulls contact data from GHL, fills template, returns file. Can also push to GHL note or email.

### 2. Metabase

**What**: SQL-based dashboards embedded in client portal.

**Dashboards to build**:
1. Pipeline Funnel — conversion rates by stage
2. Speed-to-Lead — avg time from inquiry to first contact
3. Consultant Performance — bookings, show rate, conversion by rep
4. Source Analysis — which lead sources convert best
5. Monthly Summary — new leads, consultations, retainers signed

**Deploy**: Railway one-click template (Metabase + PostgreSQL).

**Data sync**: FastAPI background job pulls GHL contacts/opportunities daily → PostgreSQL.

**Embed**: Metabase JWT embedding in Next.js portal.

### 3. Next.js + Vercel (neuronx.co)

**Pages**:
- `/` — Marketing homepage (features, pricing, testimonials)
- `/demo` — Demo booking page (embeds GHL calendar)
- `/login` — Client portal login (magic link via email)
- `/dashboard` — Client portal (Metabase embeds, pipeline view)
- `/documents` — Document upload/download
- `/blog` — SEO content (immigration updates)

**Auth**: Magic link email → verify code → NextAuth session → GHL contact lookup.

**API routes**: Next.js API routes proxy to FastAPI for auth-protected operations.

---

## Phase 2 Integration Details

### 4. Documenso (E-Signatures)

**When to add**: When retainer signing becomes a bottleneck (>5 retainers/month manual).

**Flow**:
```
Consultation outcome = "proceed"
  → FastAPI generates retainer via Docxtemplater
  → FastAPI sends to Documenso API for signature
  → Client receives email with signing link
  → Client signs
  → Documenso webhook → FastAPI → adds tag nx:retainer:signed in GHL
  → WF-10 triggers → RETAINED
```

### 5. Plausible

**When to add**: When Next.js site is live and you want privacy-friendly analytics.

**Integration**: Single `<script>` tag in `_app.tsx`. No backend work needed.

---

## Sales Productivity (Built into FastAPI + Metabase)

Instead of a separate tool, build lightweight activity tracking:

### FastAPI Endpoints
- `GET /analytics/queue?user_id=X` — prioritized work queue
- `GET /analytics/performance?user_id=X&days=30` — rep metrics
- `GET /analytics/pipeline` — funnel conversion rates (already exists)
- `GET /analytics/stuck` — stuck lead detection (already exists)

### Metabase Dashboards
- Calls/emails per rep per day (from GHL activity data)
- Pipeline velocity (days per stage)
- Source-to-retainer attribution
- Stuck lead heatmap

### GHL Native (no custom build needed)
- Pipeline Kanban board
- Contact activity timeline
- Task management (already created by WF-03, WF-07)
- Calendar availability and booking
- Smart Lists (filter contacts by tags/fields)

---

## Implementation Timeline

| Week | What | Who |
|------|------|-----|
| **Now** | FastAPI deployed to Railway | Claude + Founder (account) |
| **Week 2** | PostgreSQL + GHL data sync job | Claude |
| **Week 2** | Docxtemplater: retainer + assessment templates | Claude |
| **Week 3** | Next.js scaffold on Vercel (marketing + login) | Claude |
| **Week 3** | Metabase on Railway + pipeline dashboard | Claude |
| **Week 4** | Client portal (Next.js + Metabase embed) | Claude |
| **Week 5** | Documenso (if retainer volume justifies) | Claude |
| **Week 5** | Plausible (after site is live) | Claude |

---

## Cost Summary (Monthly)

| Service | Free Tier | Production |
|---------|-----------|------------|
| Railway (FastAPI) | 500 hrs | $5-20 |
| Railway (PostgreSQL) | Included | Included |
| Railway (Metabase) | — | $10-15 |
| Vercel (Next.js) | Hobby free | $0-20 |
| Documenso | Self-hosted free | $0 |
| Plausible | Self-hosted free | $0 (or $9 cloud) |
| **Total** | **$0** | **$15-55/mo** |

Compare: Odoo self-hosted = $200/mo hosting + 10-20 hrs/mo maintenance.
