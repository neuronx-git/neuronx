# NeuronX V1 Live Tenant Bake-Off Scorecard

Version: 1.0
Status: CANONICAL
Last Updated: 2026-03-13
Purpose: Validate what stays native in GoHighLevel vs what NeuronX must wrap

---

## Overview

This bake-off exists to prevent architecture mistakes caused by assumptions.

It compares three tracks:

1. **Track A — GHL-native only**
   - GoHighLevel Voice AI
   - GoHighLevel workflows
   - GoHighLevel Conversation AI where relevant
2. **Track B — GHL + external voice**
   - Same flows, but external voice provider for first-contact calling
3. **Track C — Snapshot onboarding reality test**
   - Create snapshot
   - Share/install to sub-account
   - Measure manual effort, repeatability, update process

The outcome is a go/no-go decision matrix that locks:
- Voice layer choice (GHL Voice AI vs external)
- How much orchestration NeuronX truly needs
- Onboarding and distribution model for v1

In addition, the bake-off validates security-critical integration behavior (webhook authenticity and replay protection).

---

## Track A — GHL-Native Only (Voice AI + Workflows + Conversation AI)

### A1. Voice AI Evaluation

Score each criterion 1–5.

| Criterion | Description | Score (1–5) | Notes |
|---|---|---:|---|
| Tone control | Can it sound professional and empathetic in immigration context? |  |  |
| Script control | Can we reliably ask R1–R5 readiness questions without drift? |  |  |
| Trust boundary safety | Does it avoid advice/eligibility assessment by design? |  |  |
| Escalation / transfer | Can it hand off to a human smoothly when triggered? |  |  |
| Appointment booking | Can it book on the calendar during the call? |  |  |
| CRM write-back | Can it update contact fields/tags reliably during/after calls? |  |  |
| Workflow triggering | Can it trigger workflows based on call outcome? |  |  |
| Consent enforcement | Does it block outbound calls when consent is missing? |  |  |
| Observability | Do we get call logs, transcripts/summaries, outcomes? |  |  |
| Reliability | Call completion rate, failure rate, timeouts, carrier issues |  |  |
| Cost | Total cost per successful contacted lead |  |  |

**Pass threshold**:
- Any score of 1 on Trust boundary safety or Consent enforcement is an immediate FAIL.
- Target average ≥ 4.0 across tone/script/control/reliability.

### A2. Conversation AI Evaluation

| Criterion | Description | Score (1–5) | Notes |
|---|---|---:|---|
| Agent provisioning | Can we create/configure bots programmatically if needed? |  |  |
| Booking assistance | Can it guide a lead to book or confirm bookings? |  |  |
| Follow-up automation | Can it support follow-up flows without custom orchestration? |  |  |
| Data capture | Can it fill contact fields from conversation reliably? |  |  |
| Escalation | Can it stop and hand off cleanly? |  |  |
| Channel coverage | SMS, FB/IG, web chat; anything else critical for v1? |  |  |

**Decision intent**: Identify whether Conversation AI can replace parts of NeuronX follow-up and booking assistance, not whether it replaces NeuronX entirely.

---

## Track B — GHL + External Voice (Vapi/Bland/Retell)

The goal is not to default to external voice. The goal is to verify whether external voice is meaningfully better for immigration-specific constraints.

### B1. External Voice Evaluation

| Criterion | Description | Score (1–5) | Notes |
|---|---|---:|---|
| Tone control | Professional, empathetic, culturally appropriate |  |  |
| Script control | R1–R5 readiness questions, low drift |  |  |
| Trust boundary safety | Does it reliably refuse advice requests and escalate? |  |  |
| Appointment booking | Can it book in GHL calendars during call (directly or via wrapper)? |  |  |
| CRM context injection | Can we pass name/source/context into the call reliably? |  |  |
| Outcome write-back | Can results map cleanly into GHL fields/tags/stages? |  |  |
| Reliability | Call completion rate, latency, outages |  |  |
| Compliance controls | Opt-out handling, consent gating, logging |  |  |
| Observability | Transcripts, analytics, failure diagnosis |  |  |
| Cost | Total cost per successful contacted lead |  |  |

### B2. Orchestration Complexity Check

| Question | Yes/No | Notes |
|---|---|---|
| Does external voice require NeuronX to maintain significant conversation state? |  |  |
| Can we avoid building a queue/broker and rely on webhooks + retries? |  |  |
| Are error cases manageable without building a full backend? |  |  |

**Pass threshold**: External voice is justified only if it materially outperforms Track A on tone, script control, reliability, or compliance.

---

## Track C — Snapshot Onboarding Reality Test

This determines whether onboarding remains premium/manual in v1 or can be operationally semi-automated.

---

## Track D — Webhook Security and Replay Protection (Mandatory)

This validates that NeuronX can safely receive GoHighLevel webhooks without spoofing or replay risk.

### D1. Signature Verification

| Test | Expected Result | Pass/Fail | Notes |
|---|---|---|---|
| Webhook includes `X-GHL-Signature` | Header present on production webhooks |  |  |
| Verify `X-GHL-Signature` (Ed25519) | Valid signatures accepted; invalid rejected |  |  |
| Legacy fallback (if present) `X-WH-Signature` | If present during transition, verify correctly |  |  |
| Raw-body fidelity | Signature verification succeeds only when raw body is unmodified |  |  |

### D2. Replay Protection

| Test | Expected Result | Pass/Fail | Notes |
|---|---|---|---|
| Timestamp window enforced | Stale webhooks rejected |  |  |
| `webhookId` uniqueness enforced | Duplicate deliveries rejected (idempotent) |  |  |
| Logging | Verification outcome logged with timestamp + webhookId |  |  |

**Pass threshold**: Any failure to reject invalid signatures or obvious replays is an immediate blocker to architecture and build.

### C1. Snapshot Creation

| Step | Measure | Result | Notes |
|---|---|---|---|
| Build gold standard sub-account | Time (hours) |  |  |
| Create snapshot | Time (minutes) |  |  |
| Verify assets included | Yes/No |  | Workflows, forms, calendars, pipelines |

### C2. Snapshot Install / Share

| Step | Measure | Result | Notes |
|---|---|---|---|
| Create share link | Time (minutes) |  |  |
| Install into new sub-account | Time (minutes) |  |  |
| Install into existing sub-account | Time (minutes) |  |  |
| Conflicts and overrides | Qualitative |  |  |

### C3. Snapshot Updates

| Step | Measure | Result | Notes |
|---|---|---|---|
| Refresh snapshot | Time (minutes) |  |  |
| Push updates | Time (minutes) |  |  |
| Update safety | Yes/No | Can we select assets and avoid destructive overwrite? |

**Decision output**: Onboarding playbook and whether we can treat distribution as “install snapshot + connect voice.”

---

## Final Go/No-Go Matrix

### Voice Layer Decision

| Condition | Decision |
|---|---|
| Track A passes thresholds and is reliable | Choose **GHL Voice AI** for v1 |
| Track A fails and Track B passes | Choose **External Voice** for v1 |
| Both fail | Do not ship AI calling in v1; use human speed-to-lead only |

### Orchestration Scope Decision

| Condition | Decision |
|---|---|
| GHL-native covers booking, consent checks, field updates, and workflows reliably | NeuronX remains a thin analytics + briefing assembler |
| GHL-native lacks reliable field updates/transcripts or consent gating | NeuronX adds wrapper logic for scoring, audit logs, and gating |

### Onboarding Model Decision

| Condition | Decision |
|---|---|
| Snapshot install is repeatable and fast (< 30 minutes) | Snapshot-based onboarding is viable |
| Snapshot install is fragile/slow | Premium manual onboarding remains required in v1 |

---

## Required Artifacts After Bake-Off

After running the bake-off, update:

- `/docs/03_infrastructure/capability_lock_audit.md`
- `/docs/03_infrastructure/product_boundary.md`
- `/docs/05_governance/open_decisions.md` (resolve OD-01 if possible)
