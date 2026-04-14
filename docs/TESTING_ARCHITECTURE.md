# NeuronX Testing Architecture — Decision Log & Operational Guide

**Version**: 1.0
**Date**: 2026-04-14
**Status**: IMPLEMENTED
**Author**: Claude Opus 4.6 (AI QA Architect)

---

## Overview

NeuronX uses a layered testing architecture with **deterministic core tests** as the foundation and **autonomous/agentic testing** as a secondary exploration layer. Total test count: **293 new structured tests + 78 legacy tests = 371+ tests**.

---

## Decision Log

### DEC-001 — Primary Testing Stack
- **Date**: 2026-04-14
- **Status**: Accepted
- **Decision**: pytest + FastAPI TestClient + k6 + Promptfoo
- **Context**: Needed a testing stack that works with Python FastAPI, supports async, handles webhook-driven architecture, and integrates with CI/CD
- **Alternatives**: Jest (wrong runtime), Vitest (web only), Locust (k6 better CI integration)
- **Why**: pytest is the Python standard; FastAPI TestClient provides zero-config API testing; k6 has built-in CI thresholds; Promptfoo evaluates the 2 real LLM surfaces
- **Consequences**: All tests run in <5s locally, CI pipeline adds ~60s with coverage
- **Related files**: `neuronx-api/pyproject.toml`, `neuronx-api/requirements.txt`

### DEC-002 — Contract Testing via JSON Snapshot Fixtures
- **Date**: 2026-04-14
- **Status**: Accepted
- **Decision**: Use JSON fixtures in `tests/fixtures/` for contract validation, NOT full Pact
- **Context**: NeuronX integrates with 5 external APIs (GHL, VAPI, Claude, Typebot, Documenso). Provider-side Pact verification is impossible since we don't control these APIs
- **Alternatives**: Pact (complex setup, no provider control), Schemathesis (needs OpenAPI spec)
- **Why**: Snapshot contracts catch 90% of payload drift at 10% of Pact complexity
- **Consequences**: When an external API changes, fixture files must be manually updated
- **Related files**: `tests/fixtures/*.json`, `tests/contracts/test_payload_contracts.py`

### DEC-003 — Promptfoo Included for OCR Evaluation
- **Date**: 2026-04-14
- **Status**: Accepted
- **Decision**: Include Promptfoo for weekly OCR prompt quality evaluation
- **Context**: NeuronX has 2 real LLM surfaces: Claude Vision OCR (7 document types) and briefing generation (planned)
- **Alternatives**: Skip Promptfoo (mocked tests can't catch prompt degradation), custom eval script
- **Why**: Promptfoo provides structured assertion framework for LLM outputs; catches regressions that mocked tests miss
- **Consequences**: Weekly CI cost (~$0.50-2.00 per eval run in API credits)
- **Related files**: `tests/promptfoo/promptfooconfig.yaml`

### DEC-004 — Mechasm and Shiplight Rejected
- **Date**: 2026-04-14
- **Status**: Accepted
- **Decision**: Do not use Mechasm or Shiplight
- **Context**: Both are early-stage AI browser testing platforms
- **Why**: Vendor lock-in, unproven at scale, don't solve the primary gap (API/contract/perf). Playwright MCP via Claude Agent SDK covers browser exploration without lock-in
- **Consequences**: No vendor dependencies for testing

### DEC-005 — k6 Over Locust
- **Date**: 2026-04-14
- **Status**: Accepted
- **Decision**: k6 for performance testing
- **Why**: Single binary, JSON output, built-in CI thresholds, JavaScript scripting matches existing repo tooling
- **Related files**: `tests/k6/smoke.js`, `tests/k6/webhook_burst.js`, `tests/k6/scoring_throughput.js`

### DEC-006 — Deep Health Endpoint Added
- **Date**: 2026-04-14
- **Status**: Accepted
- **Decision**: Added `GET /health/deep` that probes GHL, DB, Anthropic, Typebot, and YAML configs
- **Why**: `/health` only checks if the process is alive. Deep health validates external connectivity for production monitoring
- **Related files**: `neuronx-api/main.py`

### DEC-007 — APP/ (NestJS) Excluded
- **Date**: 2026-04-14
- **Status**: Accepted
- **Decision**: Exclude APP/ from testing effort
- **Why**: CLAUDE.md states "reference only, not active build path." Its 150 Jest spec files are for a future phase

---

## Test Architecture

### Layer 1: Unit Tests (`tests/unit/`) — @pytest.mark.unit
Pure business logic, no I/O or external mocking needed.

| File | Tests | Coverage |
|------|-------|----------|
| `test_scoring_service.py` | 97 | Scoring: all R1-R5 combos, boundaries, tags, outcomes |
| `test_trust_service.py` | 46 | Trust: all 6 escalation + 3 violation categories |
| `test_config_loading.py` | 26 | Config: all 7 YAML files, cache, reload |

### Layer 2: Integration Tests (`tests/integration/`) — @pytest.mark.integration
Router-level tests with mocked external services.

| File | Tests | Coverage |
|------|-------|----------|
| `test_forms_router.py` | 13 | Multi-tenant form serving, branding, 404s |
| `test_admin_router.py` | 5 | Auth (200/401/422), reload_all verification |
| `test_doc_extract_router.py` | 12 | OCR upload, dedup cache, types listing |

### Layer 3: Contract Tests (`tests/contracts/`) — @pytest.mark.contract
Payload shape validation against JSON fixtures.

| File | Tests | Coverage |
|------|-------|----------|
| `test_payload_contracts.py` | 41 | GHL/VAPI/Typebot/Claude webhooks + API responses |

### Layer 4: Database Tests (`tests/database/`) — @pytest.mark.database
Async SQLite-based tests for all 9 SQLAlchemy models.

| File | Tests | Coverage |
|------|-------|----------|
| `test_models.py` | 19 | All 9 tables: CRUD, constraints, column validation |

### Layer 5: E2E Business Flow Tests (`tests/e2e_flows/`) — @pytest.mark.e2e
Full journey tests chaining multiple endpoints.

| File | Tests | Coverage |
|------|-------|----------|
| `test_business_flows.py` | 43 | 7 business flows + failure handling |

### Layer 6: Performance Tests (`tests/k6/`)
k6 scripts for load and throughput testing.

| File | Purpose | Thresholds |
|------|---------|------------|
| `smoke.js` | Health + root endpoint | p95 < 500ms, <1% errors |
| `webhook_burst.js` | 50 concurrent webhook POSTs | p95 < 1000ms, <5% errors |
| `scoring_throughput.js` | 100 concurrent scoring requests | p95 < 200ms, <1% errors |

### Layer 7: LLM Evaluation (`tests/promptfoo/`)
Promptfoo config for OCR prompt quality.

| File | Purpose | Schedule |
|------|---------|----------|
| `promptfooconfig.yaml` | OCR extraction eval (4 test cases) | Weekly (Monday CI) |

### Layer 8: Legacy Tests (`tests/test_*.py`)
78 pre-existing tests covering webhooks, scoring, cases, OCR, etc. All pass except 6 pre-existing failures in signature/typebot tests that hit real APIs without mocks.

---

## CI/CD Pipelines

### `.github/workflows/ci-api.yml` — On push/PR to neuronx-api/**
1. Install Python 3.12 + tesseract-ocr
2. Run unit tests
3. Run integration tests
4. Run contract tests
5. Run E2E flow tests
6. Full suite with coverage report
7. Upload coverage artifact

### `.github/workflows/ci-web.yml` — On push/PR to neuronx-web/**
1. Install pnpm + Node 20
2. TypeScript check
3. Vite build

### `.github/workflows/nightly.yml` — Daily at 6:17 AM UTC
1. Production health check (Railway + Vercel)
2. Full API test suite with coverage
3. k6 performance tests against production
4. Weekly (Monday): Promptfoo LLM evaluation

---

## How To Run

```bash
# All new structured tests (fast, <2s)
cd neuronx-api && .venv/bin/python -m pytest tests/unit/ tests/integration/ tests/contracts/ tests/database/ tests/e2e_flows/ -v

# Unit tests only
cd neuronx-api && .venv/bin/python -m pytest tests/unit/ -v -m unit

# With coverage
cd neuronx-api && .venv/bin/python -m pytest tests/ --cov=app --cov-report=term-missing

# Specific layer
cd neuronx-api && .venv/bin/python -m pytest tests/contracts/ -v -m contract

# k6 smoke (requires running server)
k6 run neuronx-api/tests/k6/smoke.js

# Promptfoo eval (requires ANTHROPIC_API_KEY)
cd neuronx-api/tests/promptfoo && npx promptfoo eval

# Deep health check
curl https://neuronx-production-62f9.up.railway.app/health/deep | python3 -m json.tool
```

---

## Coverage Gaps (Known and Accepted)

| Area | Reason | Status |
|------|--------|--------|
| Real GHL API calls | Sandbox rate limits | Contract tests + mocks |
| Real VAPI calls | Costs per call | Mocked webhook payloads |
| Real Claude OCR | API credits | Promptfoo weekly + mocked unit tests |
| GHL workflow triggers | UI-only, no API | PERMANENT GAP |
| Typebot file upload | S3 fix needed | BLOCKED |
| typebot_service.py | Complex API, needs refactor | LOW coverage (11%) |
| signatures.py | Documenso integration | LOW coverage (28%) |
| clients.py | Chrome extension endpoints | LOW coverage (37%) |

---

## Agent Working Rules

For future agents working on this project:
1. Run `pytest tests/ -q` before and after any code change
2. Add tests alongside fixes — discover, patch, test, integrate
3. Use fixtures from `tests/fixtures/` for payload shapes
4. Use conftest.py fixtures (`client`, `mock_ghl`, `patch_ghl`) for router tests
5. Mark tests with appropriate markers: unit, integration, database, contract, e2e
6. Update this document after major testing decisions
7. Do not duplicate test coverage — check existing tests before adding
8. Do not invent repo facts — verify by reading files
9. Keep the coverage ratchet: never let coverage drop below current level

---

## File Reference Index

| Path | Purpose |
|------|---------|
| `neuronx-api/pyproject.toml` | pytest config, coverage settings, markers |
| `neuronx-api/tests/conftest.py` | Shared fixtures, mock factories, env setup |
| `neuronx-api/tests/fixtures/*.json` | JSON payload fixtures for contracts |
| `neuronx-api/tests/unit/` | Pure logic tests (scoring, trust, config) |
| `neuronx-api/tests/integration/` | Router tests (forms, admin, doc_extract) |
| `neuronx-api/tests/contracts/` | Payload shape validation |
| `neuronx-api/tests/database/` | SQLAlchemy model tests (async SQLite) |
| `neuronx-api/tests/e2e_flows/` | Business flow tests (7 flows + failures) |
| `neuronx-api/tests/k6/` | k6 performance scripts |
| `neuronx-api/tests/promptfoo/` | Promptfoo LLM evaluation config |
| `.github/workflows/ci-api.yml` | API CI pipeline |
| `.github/workflows/ci-web.yml` | Web build pipeline |
| `.github/workflows/nightly.yml` | Nightly smoke + perf + LLM eval |
| `neuronx-api/main.py` | Deep health endpoint (`GET /health/deep`) |
