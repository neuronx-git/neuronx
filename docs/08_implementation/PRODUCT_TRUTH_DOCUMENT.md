# NeuronX — Product Truth Document

**Purpose**: Factual product capabilities. No marketing. Used to ensure website copy is accurate.
**Date**: 2026-04-11
**Status**: CANONICAL — website copy must not exceed these claims

---

## 1. EXACT CAPABILITIES (What Works Today)

### FULLY BUILT AND TESTED
| Capability | How It Works | Evidence |
|-----------|-------------|---------|
| **Lead Scoring (0-100)** | Algorithm scores 5 dimensions (R1-R5) with base points + modifiers. Config-driven via scoring.yaml. | 78 tests pass. Correctly routes: >=70 high, 40-69 med, <40 low |
| **Pre-Consultation Briefing** | Template-based (NOT LLM). Fetches contact + scoring from GHL, generates HTML + plain text summary. | Delivers via email + GHL note |
| **Trust Boundary Checking** | Regex keyword matching on transcripts. Flags eligibility questions, deportation mentions, emotional distress. | Catches violations, returns compliant/non-compliant |
| **VAPI Webhook Processing** | Receives end-of-call data from VAPI, extracts R1-R5 structured data, scores lead, updates GHL fields + tags. | Full pipeline tested |
| **Typebot Form Webhook** | Receives form submissions, maps answers to GHL custom fields, generates document checklists. | Working on Railway |
| **Document Checklists** | Returns program-specific required + conditional documents. All 8 programs covered. | JSON output, config-driven |
| **Case Processing Endpoints** | Initiate case, update stage, record submission/decision. 10-stage pipeline. | GHL-dependent |
| **Program Questionnaires** | 13-16 questions per program from YAML config. Common + program-specific. | 8 programs covered |
| **Multi-Tenant Form Serving** | /form/{tenant}/{form} renders branded Typebot form per client. Branding from tenants.yaml. | Working on Railway |

### BUILT BUT NOT PRODUCTION-VERIFIED
| Capability | Status | Blocker |
|-----------|--------|---------|
| **13 GHL Workflows** | Published in GHL sandbox | SMS/email blocked in sandbox. Need $97+ GHL plan. |
| **Chrome Extension** | Code exists (6 files, manifest v3) | Never tested on real IRCC portal pages |
| **IRCC PDF Auto-Fill** | pypdf code exists | Needs actual IRCC PDF templates downloaded to templates/ircc/ |

### STUBBED (Endpoint Exists, Minimal Data)
| Capability | What It Returns |
|-----------|----------------|
| Pipeline Analytics | Stage counts only — no conversion rates, no trends |
| Stuck Lead Detection | Basic query — no sophisticated detection |
| Daily Dashboard | Total count only — no real dashboard |
| Compliance Audit Log | Empty list — logging framework not implemented |

### NOT BUILT (Mentioned in Docs, No Code)
| Capability | Status |
|-----------|--------|
| Metabase Dashboards | Designed, not deployed |
| Data Persistence (PostgreSQL) | Schema defined, DATABASE_URL not configured |
| Retainer .docx Generation | Not implemented |
| E-Signature (Documenso) | Service class exists, not connected to any endpoint |
| Client Portal | Not built |
| RCIC Dashboard | Not built |
| AI Voice Script Customization | Managed in VAPI dashboard, not NeuronX |
| Daily Briefing Email (Cron) | Not built |

---

## 2. AUTOMATED vs ASSISTED vs MANUAL

| Step | Type | Details |
|------|------|---------|
| Inquiry received → contact created | **AUTOMATED** | GHL form + webhook |
| AI outbound call within 5 min | **AUTOMATED** | VAPI calls, WF-02 triggers (needs production GHL) |
| Readiness assessment during call | **AUTOMATED** | VAPI asks questions, extracts R1-R5 |
| Lead scoring (0-100) | **AUTOMATED** | Algorithm in NeuronX API |
| Score → tag → workflow routing | **AUTOMATED** | WF-04B maps score to tag, triggers WF-04/11/12 |
| Consultation booking | **ASSISTED** | System sends booking link, prospect books themselves |
| Pre-consultation briefing | **AUTOMATED** | Template assembled from GHL data, delivered via email |
| Consultation itself | **MANUAL** | RCIC conducts the meeting |
| Retainer decision | **MANUAL** | RCIC + prospect agree |
| Retainer sending | **MANUAL** | RCIC sends retainer (no e-sign integration yet) |
| Case initiation | **ASSISTED** | API endpoint exists, RCIC triggers |
| Document collection | **ASSISTED** | Checklist generated, reminders automated (needs production GHL) |
| IRCC form prep | **ASSISTED** | Data sheets generated, RCIC reviews + submits |
| IRCC submission | **MANUAL** | RCIC submits to IRCC portal |
| Case tracking | **ASSISTED** | Stage updates via API, notifications via workflows |

---

## 3. LIMITATIONS AND CONSTRAINTS

### Technical
- **Sandbox GHL**: Email, SMS, phone all blocked. 11 of 13 workflows can't fully execute.
- **No LLM in briefings**: Briefings are template-based, not AI-generated. They present data, don't analyze it.
- **No real-time analytics**: Pipeline analytics are stubbed. No trend data, no conversion rates.
- **No data persistence**: PostgreSQL schema exists but isn't active. GHL is sole data store.
- **IRCC forms**: Only IMM 5476 has been tested for auto-fill. Other forms need PDF templates.

### Operational
- **Single-tenant API**: Currently hardcoded to one GHL location. Multi-tenant requires tenants.yaml config per client.
- **VAPI script is external**: NeuronX cannot modify what the AI says on calls without accessing VAPI dashboard.
- **No offline capability**: All features require internet + GHL API access.

### Business
- **13 workflows, not 24**: Website previously claimed 24. Actual: 13 published. 9 case processing workflows were planned but are GHL UI-dependent.
- **No paying customers yet**: All testimonials on the website are illustrative, not from real customers.
- **Pilot not yet run**: No E2E test with real prospect → real call → real booking has been completed.

---

## 4. AI BEHAVIOR BOUNDARIES

### AI DOES:
- Greet the caller as the firm's AI assistant
- Ask factual questions: program interest, location, timeline, prior history, budget
- Collect structured answers for scoring
- Offer to book a consultation
- Provide the booking link
- Escalate to human when triggered

### AI DOES NOT:
- Assess immigration eligibility
- Recommend immigration pathways
- Interpret immigration law or policy
- Promise application outcomes or processing times
- Represent itself as a licensed RCIC or lawyer
- Handle payment or financial information
- Continue conversation when deportation/removal is mentioned
- Continue when prospect requests a human
- Continue when emotional distress is detected
- Continue when a minor is involved

### Enforcement:
- Trust boundary checker scans every transcript post-call
- Violations logged (when audit log is implemented)
- Contact tagged `nx:human_escalation` for human follow-up
- AI cannot override escalation triggers (hardcoded in VAPI + NeuronX)

---

## 5. REAL OUTPUT EXAMPLES

### Scoring Output (POST /score/lead)
```json
{
  "contact_id": "abc123",
  "score": 87,
  "outcome": "ready_standard",
  "dimensions": {
    "r1_program_interest": {"value": "Express Entry", "points": 16},
    "r2_current_location": {"value": "In Canada", "points": 16},
    "r3_timeline_urgency": {"value": "Near-term", "points": 21},
    "r4_prior_applications": {"value": "None", "points": 16},
    "r5_budget_awareness": {"value": "Aware", "points": 26}
  },
  "confidence": 1.0,
  "tags_to_add": ["nx:score:high", "nx:assessment:complete"],
  "reasoning": "All 5 dimensions captured. Score 87 = ready_standard."
}
```

### Briefing Output (POST /briefing/generate)
```
PRE-CONSULTATION BRIEFING
Contact: Priya Sharma | priya@example.com | +1-647-555-0123
Score: 87/100 (HIGH) — Ready Standard

READINESS ASSESSMENT
R1 Program Interest: Express Entry
R2 Current Location: In Canada
R3 Timeline: Near-term (1-3 months)
R4 Prior Applications: None
R5 Budget Awareness: Aware and prepared

FLAGS: None

RECOMMENDED TALKING POINTS:
- Discuss CRS score calculation
- Review education credential assessment status
- Confirm language test scores (IELTS/CELPIP)
- Discuss settlement funds requirements
```

### Trust Check Output (POST /trust/check)
```json
{
  "contact_id": "abc123",
  "compliant": false,
  "requires_escalation": true,
  "flags": ["eligibility_question"],
  "violations": [],
  "escalation_reason": "Prospect asked 'Am I eligible for Express Entry?' — requires RCIC response, not AI."
}
```

---

## 6. KEY DIFFERENTIATION (Factual, Not Marketing)

### vs Raw GHL (GoHighLevel)
| What | GHL Alone | NeuronX + GHL |
|------|-----------|---------------|
| Lead scoring | None | 0-100 algorithm with 5 dimensions |
| AI outbound calling | None (basic Voice AI exists) | VAPI with structured data extraction |
| Pre-consultation briefings | None | Auto-generated from scoring data |
| Trust boundary enforcement | None | Regex-based compliance checking |
| Immigration-specific workflows | Generic templates | 13 immigration-specific workflows |
| Case processing pipeline | Can build manually | Pre-built 10-stage pipeline |
| IRCC form data | None | Program-specific checklists + field mappings |

### vs CaseEasy
| What | CaseEasy | NeuronX |
|------|----------|---------|
| Focus | Post-retainer case management | Pre-retainer lead conversion |
| AI calling | No | Yes (VAPI) |
| Lead scoring | Eligibility scoring | Sales readiness scoring |
| Pre-consultation prep | No | Yes (briefings) |
| IRCC forms | Auto-fill | Data sheets (auto-fill partial) |
| Pipeline management | Case pipeline | Intake pipeline + case pipeline |
| Overlap | Case management after retainer | Intake automation before retainer |
| Complementary? | Yes — CaseEasy manages cases, NeuronX fills the pipeline |

### What NeuronX Actually Adds That Nothing Else Does
1. **5-minute AI response** to every inquiry (VAPI + GHL workflow)
2. **Structured 0-100 readiness scoring** tuned to immigration programs
3. **Auto-generated consultation briefings** before every meeting
4. **Trust boundary enforcement** on every AI conversation
5. **Config-driven immigration workflows** (scoring.yaml, programs.yaml, trust.yaml)

---

## WEBSITE COPY ACCURACY CHECKLIST

Before publishing any claim, verify against this document:

| Claim | Accurate? | Notes |
|-------|-----------|-------|
| "Calls within 5 minutes" | YES (when production GHL active) | VAPI + WF-02 |
| "Scores readiness on 5 dimensions" | YES | R1-R5 algorithm, tested |
| "Pre-consultation briefings" | YES | Template-based, working |
| "24 automated workflows" | **NO** — say "13 workflows" or "automated workflow engine" | 13 exist, 9 planned |
| "IRCC form auto-fill" | PARTIAL — say "IRCC data sheets" or "form preparation assistance" | Only IMM 5476 tested |
| "Real-time analytics dashboard" | **NO** — say "pipeline visibility" | Analytics are stubbed |
| "Case processing pipeline" | YES | 10 stages, endpoints working |
| "Built by an RCIC" | YES | Sanjay Singh Kumar, R705959 |
| "5,000+ clients" | YES | Visa Master Canada track record |
| "E-signatures" | **NO** — not connected | Service exists, not wired |
| "Client portal" | **NO** — not built | |
| "AI-powered briefings" | MISLEADING — say "auto-generated briefings" | Template-based, not LLM |
