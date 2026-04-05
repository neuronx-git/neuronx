# Factory Execution Proof Run — Evidence Report

**Date**: 2026-02-04
**Auditor**: Claude (Antigravity/CTO)
**Mode**: READ-WRITE EXECUTION VERIFICATION

---

## Executive Summary

**VERDICT**: Factory Cloud API execution **FAILED** — API endpoint does not exist as implemented.

**Root Cause**: The `dispatch_factory.py` script attempts to POST to `https://api.factory.ai/v1/executions`, but **Factory.ai does not have a REST API**. Factory uses CLI-based execution via `droid exec` command.

---

## Evidence Collected

### 1. FACTORY_API_KEY Configuration

| Check | Result |
|-------|--------|
| Secret Configured | YES |
| Created | 2026-02-04T08:25:08Z |
| Key Format | `fk-4SFn...` (valid Factory format) |

### 2. API Connectivity Test

**Endpoint Tested**: `https://api.factory.ai/v1/executions`

| Method | HTTP Code | Result |
|--------|-----------|--------|
| POST | 405 | Method Not Allowed |
| GET | 404 | Not Found |

**Root Page Response** (`https://api.factory.ai/`):
```
"Factory Backend API"
"Visit app.factory.ai to access the web app."
```

### 3. Factory Documentation Research

**Source**: [Factory Droid Exec Documentation](https://docs.factory.ai/cli/droid-exec/overview)

**Key Findings**:
- Factory uses **CLI-based execution** via `droid exec` command
- **No REST API documented** for programmatic execution
- Authentication is via `FACTORY_API_KEY` environment variable
- Integration requires running the `droid` CLI tool

**Correct Usage Pattern**:
```bash
export FACTORY_API_KEY=fk-...
droid exec "task description" --auto medium
```

### 4. Dispatcher Workflow Status

| Check | Result |
|-------|--------|
| Workflow File | Committed to main |
| Trigger | `issues: [labeled]` |
| Label | `ready-for-factory` |
| Issue-Triggered Runs | 0 (none triggered) |

**Note**: Even if the workflow triggered, it would fail because the REST API endpoint doesn't exist.

---

## Root Cause Analysis

### What Was Implemented

```python
# dispatch_factory.py (incorrect assumption)
FACTORY_API_BASE = "https://api.factory.ai/v1"

response = requests.post(
    f"{FACTORY_API_BASE}/executions",
    headers={"Authorization": f"Bearer {api_key}"},
    json=payload
)
```

### What Factory Actually Requires

```bash
# Factory uses CLI, not REST API
droid exec "implement feature X" \
  --auto medium \
  --output-format json \
  --cwd /path/to/repo
```

### Gap Analysis

| Assumption | Reality |
|------------|---------|
| REST API exists | No REST API, CLI only |
| POST to /executions | Endpoint returns 404/405 |
| Bearer token auth | ENV variable auth |
| Serverless invocation | Requires `droid` CLI installed |

---

## Impact Assessment

### What Works

- FACTORY_API_KEY is correctly formatted and stored
- dispatcher.yml workflow is correctly structured
- SDLC validation logic is correct
- Safety gates (PR-only, governance) are correct

### What Doesn't Work

- API call in dispatch_factory.py fails (endpoint doesn't exist)
- No end-to-end Factory execution is possible with current implementation
- Issues labeled `ready-for-factory` will not produce Factory PRs

---

## Recommended Resolution

### Option A: Use Factory CLI in GitHub Actions

```yaml
# dispatcher.yml - corrected approach
- name: Install Factory CLI
  run: |
    curl -fsSL https://get.factory.ai | bash
    export PATH="$HOME/.factory/bin:$PATH"

- name: Execute Factory Droid
  env:
    FACTORY_API_KEY: ${{ secrets.FACTORY_API_KEY }}
  run: |
    droid exec "Implement issue #$ISSUE_NUMBER: $ISSUE_TITLE" \
      --auto medium \
      --output-format json
```

### Option B: Use Factory SDK (if available)

Research whether Factory provides a Python/Node SDK for programmatic invocation.

### Option C: Mock Execution (Current Fallback)

The current implementation already creates branches/PRs as a mock. This provides a working workflow without real Factory execution.

---

## Verification Status

| Requirement | Status | Evidence |
|-------------|--------|----------|
| API reachable | PARTIAL | Domain exists, endpoint returns 404 |
| API authenticates | FAILED | No endpoint accepts auth |
| Workflow triggers | UNTESTED | Issues event not observed |
| Factory creates execution | FAILED | No valid API to call |
| PR created | N/A | Blocked by API failure |

---

## Conclusion

**Factory execution is NOT OPERATIONAL** due to incorrect API endpoint assumption.

The system is **SAFELY DEGRADED** because:
1. Governance gates are intact
2. No unsafe operations can occur
3. Mock fallback provides branch/PR creation

**Action Required**: Implement correct Factory CLI integration or accept mock-mode operation.

---

## References

- [Factory Droid Exec Overview](https://docs.factory.ai/cli/droid-exec/overview)
- [Factory GitHub](https://github.com/Factory-AI/factory)
- [Factory App](https://app.factory.ai)

---

**Report Generated**: 2026-02-04
**Verdict**: FAILED — API endpoint does not exist as implemented
