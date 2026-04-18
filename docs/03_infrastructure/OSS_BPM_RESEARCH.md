# Open-Source BPM / Case / DMS / E-Sig Research

**Last updated:** 2026-04-18
**Purpose:** Find proven OSS tools to fill gaps in NeuronX stack without building from scratch, without fragile workarounds, and without new SaaS subscriptions.

## Executive summary — what to integrate

| Gap | Winner | Why | License |
|---|---|---|---|
| **E-signature** | **Docuseal** (docusealco/docuseal, 11k⭐) | MIT-licensed (vs Documenso AGPLv3 — commercial risk); Rails, Docker-ready; excellent API docs | MIT |
| **Document storage + search** | **Paperless-ngx** (60k⭐) | Best-in-class OCR archiving, Docker compose, tag/search, retention policies built in | GPLv3 |
| **Object storage (raw file bucket)** | **SeaweedFS** (24k⭐) | MinIO stripped web GUI in June 2025 (free tier crippled). SeaweedFS is drop-in S3-compatible, faster, fully open. | Apache 2.0 |
| **Enhanced case Kanban (optional)** | **Plane** (38k⭐) | Richer case board than GHL. AGPLv3 (OK for internal tools). Skip unless demo needs BPM screen. | AGPLv3 |
| **Sales performance analytics** | **Metabase** (already have) + new SQL views | Existing; no new tool needed. Expand views. | AGPLv3 |

## Rejected

| Tool | Reason |
|---|---|
| **Documenso** | AGPL v3 — if we offer customer-facing portal, viral copyleft risks forcing open-source of wrapper. Docuseal (MIT) is safer. |
| **Twenty CRM** | Great but we'd throw away GHL investment. Wrong call for 5-10 person firms. |
| **Huly Platform** | Too heavy (all-in-one = all-in-one problems). AGPL. |
| **Camunda / Flowable** | JVM overhead + BPMN 2.0 overkill for our 10-stage state machine. PostgreSQL state machine is enough. |
| **MinIO** | Stripped web admin UI from free tier June 2025. Forced-paid trajectory. |
| **Nextcloud / Nuxeo / Alfresco** | Wrong shape (file-sharing UI, or Java enterprise monsters). |
| **ERPNext** | Overlap with GHL too large. |

## Recommended architecture additions (3 small containers on Railway)

```
CURRENT STACK                           ADDITIONS
───────────────                         ───────────────────────
GHL (CRM + pipeline + email)            unchanged
VAPI (voice)                            unchanged
Typebot (forms)                         unchanged
FastAPI + PostgreSQL                    unchanged (+ new `documents` table)
Metabase (analytics)                    expand dashboards
Railway (deploy)                        + 3 containers

                                        SeaweedFS         ← raw S3-compatible bucket
                                        Paperless-ngx     ← OCR archive + retention
                                        Docuseal          ← e-signature
```

**Integration approach:** FastAPI proxies:
- `/docs/store/*` → SeaweedFS put/get (raw uploads)
- `/docs/archive/*` → Paperless-ngx (OCR search, retention)
- `/signatures/*` → Docuseal (already exists — swap body)

PostgreSQL `documents` table stores refs to SeaweedFS URLs + Paperless-ngx doc IDs per case.

## Sources
- [Plane](https://github.com/makeplane/plane)
- [Twenty](https://github.com/twentyhq/twenty)
- [Huly](https://github.com/hcengineering/platform)
- [Documenso](https://github.com/documenso/documenso)
- [Docuseal](https://github.com/docusealco/docuseal) ✅
- [OpenSign](https://github.com/OpenSignLabs/OpenSign)
- [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) ✅
- [SeaweedFS](https://github.com/seaweedfs/seaweedfs) ✅
- [MinIO GUI removal incident](https://www.futuriom.com/articles/news/minio-faces-fallout-for-stripping-features-from-web-gui/2025/06)
