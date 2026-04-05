# Automation Readiness Audit (v1)

**Date**: 2026-01-29
**Auditor**: Antigravity

## 1. Workflow Reality

| Workflow | File | Trigger | Status |
|----------|------|---------|--------|
| **Dispatcher** | `.github/workflows/dispatcher.yml` | `issues: [labeled]` | ⚠️ Exists but shell-only |
| **Machine Board** | `.github/workflows/machine-board.yml` | `pull_request` | ✅ Active |
| **Trae Validator** | `.github/workflows/trae-review-validator.yml` | `pull_request` | ✅ Active |
| **Daily Brief** | `.github/workflows/daily-brief.yml` | `schedule`, `workflow_dispatch` | ✅ Active |
| **Release** | `.github/workflows/release.yml` | `push: tags`, `release` | ✅ Active |

## 2. Artifact Locations

| Artifact Type | Path | Verified |
|---------------|------|----------|
| **Daily Brief** | `COCKPIT/artifacts/DAILY_BRIEF/` | ✅ Yes |
| **Approvals Queue** | `COCKPIT/artifacts/APPROVALS_QUEUE/` | ✅ Yes |
| **Plans** | `COCKPIT/artifacts/PLAN/` | ✅ Yes |
| **Verifications** | `COCKPIT/artifacts/VERIFICATION/` | ✅ Yes |

## 3. Governance Rules

- **Protected Paths**: `GOVERNANCE/`, `AGENTS/`, `COCKPIT/`, `.github/workflows/`, `STATE/` are confirmed as protected.
- **Risk Tiers**: Defined in `GOVERNANCE/RISK_TIERS.md`. T1-T4 classifications exist.
- **Trae Enforcement**: `TRAE_REVIEW` artifacts are mandatory for T1-T4 changes.

## 4. Execution Tooling

- **Factory Runner**: `scripts/dispatch_factory.py` exists but is currently a shell.
- **Headless Mode**: Missing specific "headless" flag handling in script, but architecture supports it.
- **Secrets**: `FACTORY_API_KEY` is referenced in `dispatcher.yml`.

## 5. Missing / Changes Required

1. **Dispatcher Implementation**: `dispatcher.yml` needs to actually invoke the operational functionality, not just log.
2. **Factory Script**: `scripts/dispatch_factory.py` needs to be implemented to actually perform "work" (or mock it for Phase 1).
3. **Founder Playbook**: Needs update for "No-Copy" protocol.
4. **Model Routing**: `AGENTS/MODEL_ROUTING.md` is missing.

## 6. Readiness Verdict
**Go for Phase 1.** Infrastructure exists. Key missing piece is the *logic* inside `dispatch_factory.py` and the `dispatcher.yml` permissions.
