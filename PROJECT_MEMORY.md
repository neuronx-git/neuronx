# NeuronX — Project Memory (Compact)

**Last Updated**: 2026-04-13
**Session**: Architecture audit + production hardening + Typebot form upgrade

## Canon (Authority)

- `/docs/*` is authoritative; `/archive/*` is reference only.
- `docs/04_compliance/trust_boundaries.md` overrides all implementation choices.
- Root has only 3 files: CLAUDE.md, PROJECT_MEMORY.md, AGENTS.md (109 stale files archived 2026-04-13)

## Architecture Decision (2026-04-13 — CANONICAL)

### Source of Truth Boundaries
- **GHL authoritative for**: contacts, pipeline, messages, calendar, tags, billing
- **PostgreSQL authoritative for**: cases, dependents, document metadata, scoring history, audit trail
- **Wrapper role**: Smart relay — stateless for most ops, stateful for case lifecycle + audit
- **No n8n/Temporal/document platforms needed** — Python code handles all integrations

### Rejected Tools (with evidence)
- **n8n / Activepieces**: Rejected — 800 LOC Python handles 4 integrations with 78 tests
- **Temporal**: Rejected — no long-running workflows; tenacity retry solves failure handling
- **FormKiQ / Paperless-ngx**: Rejected — 5 document types from templates; PostgreSQL table sufficient
- **Separate case management platform**: Rejected — GHL Custom Objects (10 field limit) + PostgreSQL covers it

## Live Services

| Service | URL | Status | Version |
|---------|-----|--------|---------|
| **NeuronX API** | neuronx-production-62f9.up.railway.app | ✅ Online | v0.4.0 |
| **Website** | www.neuronx.co | ✅ Live | v1.1.1 |
| **Typebot Builder** | builder-production-6784.up.railway.app | ✅ Online | — |
| **Typebot Viewer** | viewer-production-366c.up.railway.app | ✅ Online | — |
| **Metabase** | metabase-production-1846.up.railway.app | ✅ Online | — |
| **PostgreSQL** | Railway internal | ✅ Connected | 9 tables |

### Domain URLs
- Website: `www.neuronx.co` (Vercel)
- neuronx.co → 308 redirect to www.neuronx.co ✅
- Form: `www.neuronx.co/intake/vmc/onboarding` (Vercel proxy → Railway)
- forms.neuronx.co → Railway custom domain (SSL pending, use Vercel proxy)

## GitHub & Deployment

- **Active repo**: `neuronx-git/neuronx` (origin)
- **Old repo**: `ranjan-expatready/neuronx` — removed as remote, Railway switched to new repo
- **Railway**: auto-deploys from `neuronx-git/neuronx` main branch, root dir `/neuronx-api`
- **Vercel**: deploys from `neuronx-git/neuronx` main branch, root dir `neuronx-web`
- **Typebot**: Docker images from Docker Hub (not our repo)
- **⚠️ Railway deploy gotcha**: After a failed deploy, subsequent commits may not auto-deploy. Check Railway dashboard if version seems stale.

## NeuronX API — v0.4.0 (Railway)

### Sprint 1: Security & Reliability (2026-04-13)
- ✅ Webhook signature verification (Ed25519 GHL, HMAC VAPI)
- ✅ GHL client retry with exponential backoff (tenacity, 3 attempts)
- ✅ 429 rate limit handling with Retry-After header
- ✅ Connection pooling (shared httpx client)
- ✅ Idempotency tracking (processed_webhooks table)
- ✅ Dead letter queue (failed webhooks for retry)
- ✅ Admin endpoint secured (X-Admin-Key header)
- ✅ CORS restricted, dependencies pinned

### Sprint 2: Data Integrity (2026-04-13)
- ✅ Case ID: UUID-based collision-safe (NX-YYYYMMDD-{uuid[:8]})
- ✅ Config consolidation: removed 4 hardcoded Python dicts → YAML single source
- ✅ Dependents CRUD API (/dependents/ — PostgreSQL authoritative)
- ✅ Structured audit trail with request correlation IDs

### Sprint 3: Domain Knowledge + Forms (2026-04-13)
- ✅ Domain Knowledge Registry: 8 programs validated against IRCC April 2026 data
- ✅ Processing times updated (Express Entry 6mo, Spousal 15-24mo)
- ✅ Alembic migration system initialized
- ✅ 12 IRCC PDF forms downloaded from canada.ca
- ✅ Encrypted PDF fallback: HTML data sheet for unfillable forms
- ✅ Document OCR extraction: FastMRZ (passport, free) + Claude vision (all other docs)
- ✅ Auto-populate onboarding URL from Phase 1 data (GET /cases/onboarding-url/{contact_id})

### Database Tables (9)
contacts, opportunities, cases, activities, signatures, sync_log,
dependents, processed_webhooks, dead_letter_queue

### Key Endpoints
| Endpoint | What |
|----------|------|
| POST /webhooks/ghl | GHL events — sig verified + idempotent |
| POST /webhooks/voice | VAPI events — sig verified + idempotent + DLQ |
| POST /extract/upload | Document OCR — passport (FastMRZ) + all docs (Claude) |
| GET /cases/onboarding-url/{id} | Pre-filled onboarding URL from Phase 1 data |
| POST /cases/initiate | Start case after retainer |
| GET /form/{tenant}/{slug} | Multi-tenant form serving (native Typebot embed) |
| GET /extract/types | List 7 supported document types for OCR |

### Config Files (YAML — single source of truth)
- config/scoring.yaml — R1-R5 scoring weights + complexity keywords
- config/trust.yaml — escalation triggers + AI violation patterns
- config/programs.yaml — 8 programs, IRCC forms, processing times, doc checklists
- config/questionnaires.yaml — 68 questions across 8 programs
- config/ircc_field_mappings.yaml — questionnaire → IRCC PDF field mappings
- config/tenants.yaml — multi-tenant branding + form config
- config/case_emails.yaml — email templates (not yet wired)

## Typebot Smart Form

- **Builder**: builder-production-6784.up.railway.app/typebots/cmnrfu934000334qxnlmsvw2u/edit
- **Form URL**: www.neuronx.co/intake/vmc/onboarding
- **API Token**: SuUW5WiLi1IAjuja4Mdtlu16
- **Workspace ID**: cmnrfqc6z000034qx46joy6hf
- **Typebot ID**: cmnrfu934000334qxnlmsvw2u
- **Public ID**: vmc-onboarding
- **Variables**: 79 (from questionnaires.yaml)
- **Blocks**: 112 across 16 groups
- **Programs**: 8 (branching by program interest)
- **Document checklists**: per-program, shown before upload
- **Webhook**: neuronx-production-62f9.up.railway.app/typebot/webhook
- **Template**: Native Typebot embed (full-screen, responsive, Builder-managed)
- **⚠️ File upload**: Requires MinIO S3 fix (S3_ENDPOINT should use RAILWAY_PRIVATE_DOMAIN)
- **Prefill**: isInputPrefillEnabled=true (URL params auto-fill inputs)
- **Version**: Must be "6" (not "6.1" — viewer API rejects 6.1)

## GHL Gold Build — COMPLETE

| Asset | Count | Status |
|-------|-------|--------|
| Custom Fields | 140 | ✅ |
| Tags | 104 | ✅ |
| Pipelines | 2 (Intake + Case Processing) | ✅ |
| Workflows | 15 + 9 case processing | ✅ All published |
| Calendars | 4 | ✅ |
| Forms | 1 (Immigration Inquiry V1) | ✅ |
| Email Templates | 11 | ✅ |
| VAPI Voice Agent | 1 (wired to Railway) | ✅ |

### GHL DNS Records (neuronx.co — Internal Domain)
| Type | Name | Content |
|------|------|---------|
| A | neuronx.co | 216.198.79.1 (Vercel) |
| CNAME | www | cname.vercel-dns.com |
| CNAME | forms | neuronx-production-62f9.up.railway.app |
| CNAME | vmc | sites.ludicrous.cloud (GHL funnel) |
| CNAME | api | brand.ludicrous.cloud |
| CNAME | app | whitelabel.ludicrous.cloud |

## Website — v1.1.1 (Vercel)

- www.neuronx.co — React + Shadcn + Framer Motion + GSAP
- 8-stage pipeline animation (GSAP electrifying effect)
- Stripe-like animated hero background
- Code-split: 5 chunks (largest 148KB)
- SEO: robots.txt, sitemap.xml, JSON-LD, security headers
- Vercel proxy: /intake/* → Railway /form/*

## IRCC Domain Knowledge

- 8 programs covering ~100% of RCIC business
- P0 (full auto, ~75%): Express Entry, Spousal Sponsorship, Work Permit
- P1-P2 (checklists, ~25%): Study, LMIA, PR Renewal, Citizenship, Visitor
- 12 IRCC PDFs in repo (5 fillable, 4 encrypted w/ data sheet fallback, 3 flat)
- Processing times verified April 2026 against IRCC
- Full domain registry: docs/09_domain_knowledge/DOMAIN_KNOWLEDGE_REGISTRY.md

## What Blocks Pilot Launch

1. **Production GHL account** ($297/mo) — needed for email/SMS/phone
2. **Typebot file upload fix** — S3_ENDPOINT must use internal Railway URL
3. **E2E UAT** — needs production GHL
4. **RCIC license number** — update in config/ircc_field_mappings.yaml

## What Does NOT Block Pilot
- Client portal (RCICs use GHL directly)
- Admin dashboard (Metabase direct access sufficient)
- Chrome extension store deployment
- WhatsApp integration
- ERPNext/HR system

## Tests
- 78/78 passing (neuronx-api)
- Run: `cd neuronx-api && .venv/bin/python -m pytest tests/ -q`

## ⚠️ SANDBOX DISCOVERY (2026-03-26)
The GHL agency is a DEVELOPER SANDBOX. Email/SMS/phone blocked.
All config work transferable via Snapshot. Strategy: build in sandbox, migrate to paid account.
