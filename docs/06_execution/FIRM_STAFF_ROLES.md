# VMC Firm Staff Roles — FAANG/Big 5-style, Lean

**Philosophy:** 9 team members, production-quality role separation (inspired by McKinsey/Deloitte case-mgmt tiering + FAANG-style permission minimalism). Each role has explicit scope. No "anyone can do anything".

## Team hierarchy (9 people)

```
Managing Partner / Head RCIC (1)            ← admin, final sign-off
├─ Senior RCIC Consultant (2)               ← complex cases, peer review
├─ Junior RCIC Consultant (2)               ← standard cases, doc collection
├─ Client Success Manager (1)               ← post-retainer client comms
├─ Sales Development Rep (1)                ← lead qualification, demo booking
├─ Operations Manager (1)                   ← admin, workflows, reporting
└─ Intake Coordinator (1)                   ← triage, first-touch
```

## Role definitions

### 1. Managing Partner / Head RCIC — `admin`
- **Access:** Everything
- **Owns:** Pricing, firm strategy, compliance, final IRCC sign-off
- **Tools:** All GHL modules + Metabase admin + NeuronX admin panel
- **Metrics tracked:** Firm revenue, approval rate, team utilization, compliance incidents

### 2. Senior RCIC Consultant — `account/user` (not `assignedDataOnly`)
- **Access:** All contacts + pipeline + calendar + conversations + invoicing
- **Owns:** Complex cases (refusals, appeals, inadmissibility), peer-review junior work
- **Typical load:** 15-25 concurrent cases
- **Metrics:** Approval rate, avg time-to-submit, revenue per case

### 3. Junior RCIC Consultant — `account/user` + `assignedDataOnly=true`
- **Access:** Only their assigned contacts (data isolation)
- **Owns:** Standard cases (Express Entry, work permit, study permit)
- **Typical load:** 20-30 concurrent cases
- **Metrics:** Cases closed/month, doc-completion rate, SLA adherence

### 4. Client Success Manager — `account/user` (shared data access)
- **Access:** Contacts + conversations + campaigns + calendar
- **Owns:** Post-retainer client experience, NPS surveys, referral requests, upsell (family/citizenship)
- **Typical load:** Manages all active cases from relationship side
- **Metrics:** NPS, referral conversion, expansion revenue

### 5. Sales Development Rep — `account/user` + `assignedDataOnly=true`
- **Access:** Only new/inbound leads in pipeline stages NEW/CONTACTING
- **Owns:** First-touch qualification, demo booking, routing to RCIC
- **Typical load:** 30-50 new leads/week
- **Metrics:** Lead-to-booking conversion, time-to-first-response

### 6. Operations Manager — `account/admin`
- **Access:** All except financial/pricing
- **Owns:** Workflow maintenance, Metabase reporting, compliance tracking, snapshot/deploy coordination
- **Tools:** GHL admin panel, Metabase, Railway dashboard, Cloudflare DNS
- **Metrics:** System uptime, workflow failure rate, report delivery SLA

### 7. Intake Coordinator — `account/user` (shared)
- **Access:** Contacts + conversations + opportunities (NEW/CONTACTING stages only)
- **Owns:** Form-submit triage, matching leads to RCIC specialization, initial consultation booking
- **Typical load:** Handles 100% of inbound
- **Metrics:** Triage accuracy, matching quality, consultation show-up rate

## Calendar assignments (already configured in prod VMC)

| Calendar | Duration | Who's on it | Why |
|---|---|---|---|
| VMC — Free Initial Assessment | 15 min | Nina, Michael, Sarah, Arjun, Kwame | Round-robin: all RCICs + intake |
| VMC — Paid Consultation | 60 min | Nina, Michael, Sarah, Arjun | Only RCICs, not intake |
| VMC — Strategy Session (Complex) | 90 min | Rajiv, Nina, Michael | Head + Seniors only |

## Role-permission matrix (GHL)

| Permission | Mgr | Sr.RCIC | Jr.RCIC | CSM | SDR | Ops | Intake |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Contacts read | ✓all | ✓all | ✓own | ✓all | ✓own | ✓all | ✓NEW/CONTACTING |
| Contacts write | ✓ | ✓ | ✓own | ✓ | ✓own | ✓ | ✓assigned |
| Opportunities | ✓all | ✓all | ✓own | ✓all | ✓own | ✓all | ✓NEW only |
| Campaigns (email) | ✓ | — | — | ✓ | — | ✓ | — |
| Workflows | ✓ | — | — | — | — | ✓ | — |
| Settings | ✓ | — | — | — | — | ✓ | — |
| Reporting | ✓ | ✓own | ✓own | ✓ | ✓own | ✓ | ✓ |
| Invoicing | ✓ | ✓ | — | — | — | ✓ | — |
| Phone | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Assignment rules (automated via workflows)

**On lead creation** (WF-01 Instant Lead Capture):
1. Round-robin assign to Intake Coordinator (Kwame)
2. After AI call + scoring:
   - If complex → re-assign to Senior RCIC
   - If standard → round-robin Junior RCIC

**On retainer signed** (WF-CP-01 Client Onboarding):
1. Case auto-created in PostgreSQL
2. Assigned RCIC inherits from Opportunity assignee
3. CSM auto-added as co-assignee (for relationship mgmt)

**Escalation triggers** (re-assigns to Senior RCIC or Head):
- Tag `nx:human_escalation` → Senior RCIC
- Tag `nx:escalation:rcic_review` → Senior RCIC
- RFI received + Junior RCIC → auto-escalate to Senior

## Lean-team principles (FAANG/Big 5 hybrid)

1. **One-pizza ownership** — each case has exactly one primary owner (Case.assigned_rcic)
2. **Peer review gate** — Junior-handled cases require Senior sign-off at `under_review` stage (WF-CP-04)
3. **Documented handoffs** — every re-assignment logs Activity with reason
4. **Data isolation by default** — Junior + SDR + Intake use `assignedDataOnly=true` (can't browse others' contacts)
5. **Admin minimalism** — only Managing Partner + Ops Manager have admin; no role creep
6. **Weekly leaderboard** — Monday 8am email: Top RCIC by revenue + approval rate + SLA

## Revenue sharing / commission (not implemented yet, for reference)

Industry-standard splits (for pilot firms with real users):
- **Junior RCIC:** salary base; +5% of case retainer bonus
- **Senior RCIC:** +15% commission
- **CSM:** +2% on referral-sourced retainers
- **SDR:** +3% on leads that convert to retainer within 30 days

Track via Metabase: `v_team_leaderboard` (monthly) + `v_commission_due` (after `users` FK migration).

## Demo user credentials (all DEMO- prefixed)

Stored in `tools/ghl-lab/.team-users.json` (gitignored). Password for all demo users: `NeuronxDemo2026!Secure` (rotate before real pilot).

| Role | Name | Email |
|---|---|---|
| Managing Partner | DEMO - Rajiv Mehta | rajiv.mehta@demo.visamasters.ca |
| Senior RCIC | DEMO - Nina Patel | nina.patel@demo.visamasters.ca |
| Senior RCIC | DEMO - Michael Chen | michael.chen@demo.visamasters.ca |
| Junior RCIC | DEMO - Sarah Johnson | sarah.johnson@demo.visamasters.ca |
| Junior RCIC | DEMO - Arjun Kapoor | arjun.kapoor@demo.visamasters.ca |
| CSM | DEMO - Emily Brooks | emily.brooks@demo.visamasters.ca |
| SDR | DEMO - James Rodriguez | james.rodriguez@demo.visamasters.ca |
| Ops Manager | DEMO - Priya Sharma | priya.sharma.ops@demo.visamasters.ca |
| Intake Coordinator | DEMO - Kwame Mensah | kwame.mensah@demo.visamasters.ca |
