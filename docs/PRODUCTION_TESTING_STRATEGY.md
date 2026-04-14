# NeuronX Production-Grade Testing Strategy

**Goal**: Remove 90-95% of human testing dependency for a solo founder.
**Date**: 2026-04-14
**Status**: IMPLEMENTATION IN PROGRESS

---

## The Problem

NeuronX has 15+ workflows, 8 program branches, 79 form variables, 5 external integrations, multi-tenant forms, document OCR, voice AI, and email delivery. A solo founder cannot manually test all permutations across form programs, field validation, workflow triggers, OCR accuracy, and voice flows.

## The Solution: 5-Layer Autonomous Testing Stack

```
Layer 5: Production Monitoring (Nightly)
  |  Smoke tests, deep health, synthetic webhooks
Layer 4: Autonomous Exploration (On-demand)
  |  Claude Agent SDK + Playwright MCP
Layer 3: Voice AI Testing (Weekly)
  |  VAPI Chat Tests + Evals (NO real phone calls)
Layer 2: Browser E2E + Shiplight AI (Per-commit)
  |  Typebot forms, multi-tenant branding, form validation
Layer 1: Deterministic Core (Per-commit, <6s)
  |  693 pytest tests, 92.5% coverage
```

---

## Layer 1: Deterministic Core (COMPLETE)

**693 tests | 92.5% coverage | 5.5s runtime | 0 failures**

Already implemented:
- Unit tests (scoring, trust, config, IRCC forms, webhook security)
- Integration tests (all routers, deep health, OpenAPI schema)
- Contract tests (GHL, VAPI, Typebot, Claude payload shapes)
- Database tests (all 9 models via async SQLite)
- E2E business flow tests (7 flows + failure handling)
- k6 performance scripts (smoke, webhook burst, scoring throughput)
- Promptfoo LLM evaluation (OCR extraction quality)
- CI/CD workflows (ci-api, ci-web, nightly)

**Human testing needed**: ZERO for this layer.

---

## Layer 2: Shiplight AI + Browser E2E

### What Shiplight Solves

Shiplight AI runs **on top of Playwright** with an AI layer that:
- Writes tests in natural-language YAML (not brittle selectors)
- Self-heals when UI changes
- Takes screenshots + traces for every step
- Has built-in email flow testing
- Integrates with Claude Code via MCP plugin

### Installation

```bash
# Install Shiplight MCP in Claude Code
claude mcp add shiplight -- npx -y @shiplightai/mcp@latest
```

### What To Test With Shiplight

| Scenario | YAML Test | Human Needed? |
|----------|-----------|---------------|
| Multi-tenant form rendering (VMC branding) | YES | NO |
| Typebot form loads in iframe | YES | NO |
| Form field validation (mandatory/optional) | YES | NO |
| Program-specific questions appear correctly | YES | NO |
| Form reload doesn't duplicate data | YES | NO |
| Landing page renders correctly | YES | NO |
| Health endpoints accessible | YES | NO |

### What NOT To Test With Shiplight

| Scenario | Why Not | Better Tool |
|----------|---------|-------------|
| GHL workflow builder UI | Nested iframes, 15s load, SPA complexity | GHL API outcome checks |
| VAPI voice calls | Not browser-based | VAPI Chat Tests |
| FastAPI endpoint logic | Not browser-based | pytest (already done) |
| Document OCR accuracy | API-only flow | Promptfoo (already done) |

### YAML Test Specs (Location: `tests/shiplight/`)

See `tests/shiplight/` directory for ready-to-run YAML test specs.

---

## Layer 3: VAPI Voice AI Testing (NO REAL PHONE CALLS)

### Discovery: VAPI Has Built-In Testing

VAPI provides three testing mechanisms that DO NOT require real phone calls:

#### 3A. Chat Test Suites (Text-Based, Free)
- Simulates conversations via text (no TTS/STT)
- Verifies conversational logic and tool calls
- Tests R1-R5 data extraction from conversations
- Dashboard: `dashboard.vapi.ai/test-suites`

#### 3B. Evals Framework (CI/CD Ready)
- Validates agent calls correct tools with correct arguments
- Three validation methods: exact match, regex, AI judge
- CLI: `vapi evals run` (CI-friendly)

#### 3C. Local Webhook Testing
```bash
# Forward VAPI webhooks to local FastAPI
vapi listen --forward-to http://localhost:8000/webhooks/voice
```

### VAPI Test Plan

| Test | Method | Cost | Human? |
|------|--------|------|--------|
| R1-R5 extraction from conversation | Chat Test Suite | FREE | NO |
| Correct tool calls (collect_readiness, book_consultation) | Evals | FREE | NO |
| End-of-call webhook → scoring → GHL update | Local webhook test | FREE | NO |
| Trust boundary triggers (escalation phrases) | Chat Test Suite | FREE | NO |
| Voice quality + telephony | Voice Test Suite | PAID (call minutes) | NO |

### Implementation

See `tests/vapi/` directory for test configurations.

---

## Layer 4: Autonomous Claude Agent SDK

### Purpose
Exploratory testing that discovers **unknown** failure modes. NOT for regression (that's Layers 1-2).

### What It Tests

| Scenario | How |
|----------|-----|
| Typebot form with all 8 program branches | Navigate iframe, select each program, verify correct questions |
| Form reload behavior (duplication vs overwrite) | Submit form, reload, submit again, check GHL API |
| Multi-tenant branding consistency | Load /form/{tenant}/onboarding for each tenant, screenshot compare |
| Edge cases in scoring | Send boundary payloads via API, verify outcome |
| End-to-end: form → webhook → score → GHL tags | Chain API calls, verify final contact state |

### Guardrails
- Environment allowlist: `localhost`, staging Railway URL only
- NO destructive actions (no DELETE, no real contact creation in prod)
- All runs produce screenshots + JSON report
- Manual trigger only (never a CI gate)
- Max 100 API calls per run

### Implementation

See `tests/autonomous/` directory for agent scripts.

---

## Layer 5: Production Monitoring (COMPLETE)

Already implemented:
- `GET /health/deep` — probes GHL, DB, Anthropic, Typebot, configs
- `nightly.yml` — daily smoke tests against production
- k6 performance scripts — webhook burst, scoring throughput

### Future (When Production GHL Active)
- **Mailosaur** — programmatic email inbox for verifying GHL emails
- **Synthetic webhook tests** — POST test payload to production, verify scoring

---

## What Remains Human-Only (5-10%)

These cannot be automated with ANY tool:

| Task | Why |
|------|-----|
| 2FA / CAPTCHA on GHL login | Security by design |
| GHL billing / account setup | Payment verification |
| RCIC license number update | Legal verification |
| Production GHL account purchase | Payment decision |
| Typebot S3 fix (Railway env var) | Infrastructure change |
| First real client UAT | Business validation |

Everything else is automated.

---

## Audit Rounds Strategy

### Round 1: Code + API (COMPLETE)
- 693 tests, 92.5% coverage
- All API endpoints tested
- All payload contracts validated
- All database models verified

### Round 2: Browser + Forms (THIS SESSION)
- Shiplight YAML tests for form rendering
- Typebot iframe interaction tests
- Multi-tenant branding verification
- Form validation (mandatory/optional fields)

### Round 3: Voice + Integration (NEXT SESSION)
- VAPI Chat Test Suites (R1-R5 extraction)
- VAPI Evals (tool call verification)
- Local webhook forwarding tests
- End-to-end: call → score → GHL update

### Round 4: Production Readiness (FINAL)
- Run all layers together
- Fix remaining failures
- Visual regression baseline
- Performance benchmarks
- Go/No-Go decision document

---

## Tool Decision Summary

| Tool | Role | Status |
|------|------|--------|
| **pytest** | Deterministic core (693 tests) | IMPLEMENTED |
| **k6** | Performance testing | IMPLEMENTED |
| **Promptfoo** | LLM OCR evaluation | IMPLEMENTED |
| **Shiplight AI** | Browser E2E via MCP | IMPLEMENTING |
| **VAPI Chat Tests** | Voice agent testing (no calls) | IMPLEMENTING |
| **VAPI Evals** | Tool call validation | IMPLEMENTING |
| **Claude Agent SDK** | Autonomous exploration | SCAFFOLDED |
| **Playwright MCP** | Direct browser control | AVAILABLE |
| **Mailosaur** | Email testing | FUTURE (needs prod GHL) |
| **Mechasm** | NOT CHOSEN | Too expensive, Shiplight better fit |
| **Locust** | NOT CHOSEN | k6 selected instead |
| **Pact** | NOT CHOSEN | JSON fixtures sufficient |

---

## Cost Estimate

| Item | Cost | Frequency |
|------|------|-----------|
| pytest/k6/Playwright | FREE | Every commit |
| Shiplight MCP plugin | FREE | Every commit |
| Promptfoo LLM eval | ~$2/run API credits | Weekly |
| VAPI Chat Tests | FREE | Weekly |
| VAPI Voice Tests | ~$1-5/run (call minutes) | Monthly |
| Shiplight Cloud (optional) | TBD (contact sales) | If needed |
| Mailosaur | Free tier (50 emails/mo) | When prod GHL active |
| **Total monthly**: | **<$30** | |
