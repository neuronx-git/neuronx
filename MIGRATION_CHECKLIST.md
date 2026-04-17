# VMC Production — Final Setup State (Updated 2026-04-17 evening)

## ✅ What's DONE — best-in-class 5-10 person immigration firm setup

| Resource | Count | Status |
|---|---|---|
| **Team members (9 users)** | 9 | ✅ Managing Partner + 2 Senior RCICs + 2 Junior RCICs + CSM + SDR + Ops Manager + Intake Coordinator |
| **Custom fields** | 140 | ✅ Matches sandbox exactly |
| **Tags** | 120 | ✅ All `nx:case:*`, `nx:decision:*`, `nx:score:*` |
| **Email templates** | 40 | ✅ 26 premium Postmark-based + 14 original |
| **Intake pipeline** | 1 (10 stages) | ✅ Live |
| **Intake workflows** | 18 | ✅ Live + unchanged since import |
| **Calendars** | 14 (3 shared + 11 personal) | ✅ Real team assignments |
| **GHL contacts (demo)** | 35 | ✅ All assigned to real RCICs (round-robin) |
| **PostgreSQL demo data** | 15 cases, 9 stages, 185 activities, $48.5K revenue | ✅ |
| **NeuronX SaaS sub-account** | 23 fields + 24 tags + 3 firm demos | ✅ Ready for selling the platform |
| **Metabase dashboards** | 3 dashboards, 10 SQL views | ✅ Populated |
| **Railway API** | Points to prod VMC + new PIT | ✅ All health checks green |

## 👥 The Firm Team (all DEMO-prefixed)

| # | Role | Name | Email | License |
|---|---|---|---|---|
| 1 | Managing Partner / Head RCIC | DEMO - Rajiv Mehta | rajiv.mehta@demo.visamasters.ca | R123456 |
| 2 | Senior RCIC Consultant | DEMO - Nina Patel | nina.patel@demo.visamasters.ca | R234567 |
| 3 | Senior RCIC Consultant | DEMO - Michael Chen | michael.chen@demo.visamasters.ca | R345678 |
| 4 | Junior RCIC Consultant | DEMO - Sarah Johnson | sarah.johnson@demo.visamasters.ca | R456789 |
| 5 | Junior RCIC Consultant | DEMO - Arjun Kapoor | arjun.kapoor@demo.visamasters.ca | R567890 |
| 6 | Client Success Manager | DEMO - Emily Brooks | emily.brooks@demo.visamasters.ca | — |
| 7 | Sales Development Rep | DEMO - James Rodriguez | james.rodriguez@demo.visamasters.ca | — |
| 8 | Operations Manager | DEMO - Priya Sharma | priya.sharma.ops@demo.visamasters.ca | — |
| 9 | Intake Coordinator | DEMO - Kwame Mensah | kwame.mensah@demo.visamasters.ca | — |

**Password:** `NeuronxDemo2026!Secure` (all demo users — rotate before real pilot)

## 📅 Calendar Assignments

| Calendar | Duration | Team Members | Widget Slug |
|---|---|---|---|
| VMC — Free Initial Assessment | 15 min | Nina, Michael, Sarah, Arjun, Kwame (5) | `vmc-free-assessment` |
| VMC — Paid Consultation | 60 min | Nina, Michael, Sarah, Arjun (4) | `vmc-paid-consult` |
| VMC — Strategy Session (Complex Cases) | 90 min | Rajiv, Nina, Michael (3) | `vmc-strategy-session` |

## ⚠️ What's STILL MISSING (requires GHL UI — PIT scope can't do these)

1. **Case Processing pipeline** (9 stages) — API returns 401 on pipeline POST
2. **9 WF-CP workflows** — GHL workflow CRUD is UI-only
3. **3 broken "🚧 Processing" duplicate workflows** — cluttered, harmless, UI delete only

## 🎯 Remaining Manual Tasks (~15 min in GHL UI)

### Task 1 — Delete 3 broken "🚧 Processing" workflows (2 min)
URL: https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/automation/workflows

### Task 2 — Create "NeuronX - Case Processing" pipeline (2 min)
URL: https://app.gohighlevel.com/v2/location/vb8iWAwoLi2uT3s5v1OW/pipelines

9 stages:
```
0. ONBOARDING
1. DOC COLLECTION
2. FORM PREPARATION
3. INTERNAL REVIEW
4. SUBMITTED TO IRCC
5. PROCESSING
6. ADDITIONAL INFO (RFI)
7. DECISION RECEIVED
8. CASE CLOSED
```

### Task 3 — Build 9 WF-CP workflows (10 min)
For each, trigger = Contact Tag Added + Action = Send Email using the premium template:

| # | Workflow | Trigger Tag | Email Template | Assign to |
|---|---|---|---|---|
| 1 | WF-CP-01 Client Onboarding | `nx:case:onboarding` | VMC-15-case-onboarding | Case assigned RCIC |
| 2 | WF-CP-02 Docs Reminders | `nx:case:docs_pending` | VMC-16-cp-docs-reminder | Case RCIC + day 3, 7, 14 reminders |
| 3 | WF-CP-03 Form Preparation | `nx:case:form_prep` | VMC-17-cp-form-prep | Case RCIC |
| 4 | WF-CP-04 Internal Review | `nx:case:under_review` | VMC-18-cp-internal-review | Case RCIC |
| 5 | WF-CP-05 IRCC Submission | `nx:case:submitted` | VMC-19-cp-submitted | Case RCIC |
| 6 | WF-CP-06 Status Updates | `nx:case:processing` | VMC-20-cp-status-update | Case RCIC (monthly) |
| 7 | WF-CP-07 RFI Alert | `nx:case:rfi` | VMC-21-cp-rfi | Case RCIC + CSM |
| 8 | WF-CP-08 Decision (3 branches) | `nx:case:decision` + decision tag | VMC-22/23/24 (approved/refused/withdrawn) | Case RCIC |
| 9 | WF-CP-09 Case Closure | `nx:case:closed` | VMC-25-cp-case-closed | CSM |

### Task 4 — Link 26 premium email templates to existing 18 workflows (5 min)
For each workflow below, click the Send Email action → select the VMC-* template:

| Workflow | Email Template |
|---|---|
| WF-01 Instant Lead Capture | VMC-01-inquiry-received |
| WF-02 Contact Attempt Sequence | VMC-02-outreach-attempt |
| WF-04 Readiness Complete | VMC-03-invite-booking |
| WF-04B AI Call Receiver | VMC-14-complex-case-alert (for escalations) |
| WF-04C Missed Call Recovery | VMC-26-missed-ai-call |
| WF-05 Appointment Reminders | VMC-04-consultation-confirmed + VMC-05-consultation-reminder |
| WF-06 No-Show Recovery | VMC-06-noshow-recovery |
| WF-09 Retainer Follow-Up | VMC-07-retainer-proposal + VMC-08-retainer-followup |
| WF-10 Post-Consult Follow-Up | VMC-08-retainer-followup |
| WF-11 Nurture Campaign Monthly | VMC-10-monthly-nurture + VMC-11-winback-nurture |
| WF-12 Score Med Handler | VMC-09-score-medium-handler |
| WF-13 PIPEDA Data Deletion | VMC-12-pipeda-ack + VMC-13-pipeda-deleted |

### Task 5 (optional) — Create NeuronX Sales pipeline (2 min)
URL: https://app.gohighlevel.com/v2/location/muc56LdMG8hkmlpFFuZE/pipelines

8 stages: NEW LEAD → QUALIFYING (BANT) → DEMO SCHEDULED → DEMO COMPLETED → PROPOSAL SENT → TRIAL ACTIVE → PAID CUSTOMER → CHURNED

## 🔍 Verification script

Run this after completing manual tasks:

```bash
cd /Users/ranjansingh/Desktop/NeuronX
python3 tools/ghl-lab/src/e2e_audit.py
# Check docs/06_execution/RESOURCE_DIFF.md for sync status
```

## 🎁 Demo dataset highlights (for investor showcase)

**Production VMC:**
- 30 demo contacts across 12 countries, 8 immigration programs
- 15 cases in 9 different lifecycle stages
- $48,500 demo revenue
- 185 activity records powering Metabase timeline
- Real RCIC assignments (Rajiv/Nina/Michael/Sarah/Arjun rotation)

**NeuronX SaaS sub-account:**
- 3 demo firm prospects (Maplecrest Immigration / Vancouver Immigration Partners / Tremblay & Associés)
- Segments: small-firm / mid-firm / solo-rcic
- Tiers: Growth $1,000 MRR / Scale $1,500 MRR / Starter $500 MRR

## 📁 Key scripts (all in repo)

| Script | Purpose |
|---|---|
| `tools/ghl-lab/src/refresh_oauth.py` | Refresh sandbox OAuth using .env creds |
| `tools/ghl-lab/src/build_firm_team.py` | Create 9 team users with role permissions |
| `tools/ghl-lab/src/build_firm_calendars.py` | Create 3 shared calendars with team assignments |
| `tools/ghl-lab/src/migrate_to_vmc.py` | Migrate fields/tags sandbox → VMC |
| `tools/ghl-lab/src/setup_neuronx_saas.py` | Setup NeuronX SaaS sub-account |
| `tools/ghl-lab/src/e2e_audit.py` | Full side-by-side audit |
| `tools/ghl-lab/src/prod_deep_audit.py` | Prod VMC deep-dive audit |
| `neuronx-api/email-templates/generate.py` | Generate 26 Postmark-based templates |
| `neuronx-api/email-templates/upload.py` | Upload templates to VMC |
| `neuronx-api/scripts/seed_premium_demo.py` | Seed PostgreSQL + GHL demo data |
