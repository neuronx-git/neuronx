---
description: Update STATE files after changes
---

# Update STATE Files Workflow

## Purpose
Update STATE/STATUS_LEDGER.md and STATE/LAST_KNOWN_STATE.md after any repository changes.

## When to Use
**MANDATORY for ALL PRs** (no exceptions)

## Steps

// turbo-all

### 1. Update STATUS_LEDGER.md

Update the following sections:

```markdown
## Current Objective
{What is the current high-level goal}

## Active Issues
- Issue #{NUMBER}: {Title} - {Status}

## Active PRs
- PR #{NUMBER}: {Title} - {Status}

## Last Completed Artifact
- {ARTIFACT_TYPE}: {Path} - {Date}

## Current Blockers
- {Blocker description} - {Waiting for what}

## Next Actions (Prioritized)
1. {Next action 1}
2. {Next action 2}
3. {Next action 3}

## Current Risk Tier
{T0|T1|T2|T3}

## Required Gates Status
- [ ] Gate 1: {Status}
- [ ] Gate 2: {Status}
```

### 2. Update LAST_KNOWN_STATE.md

Update the following sections:

```markdown
## State Machine Position
{IDLE|PLANNING|EXECUTING|WAITING_FOR_HUMAN}

## Active Task
{Current task description}

## Work in Progress
- {WIP item 1}
- {WIP item 2}

## GitHub State
- Branch: {branch_name}
- Last commit: {commit_hash}
- Open issues: {count}
- Open PRs: {count}

## CI/CD State
- Last CI run: {status}
- Last deploy: {timestamp}

## Risk Assessment
- Current risk tier: {T0|T1|T2|T3}
- Required approvals: {list}

## Quality State
- Test coverage: {percentage}
- Linting: {PASS|FAIL}
- Security scan: {PASS|FAIL}

## Governance Compliance
- Guardrails: {COMPLIANT|VIOLATIONS}
- Artifacts: {COMPLETE|MISSING}

## Agent Coordination
- Last handoff: {Agent A} → {Agent B}
- Waiting for: {Agent/Human}

## Blockers
- {Blocker 1}
- {Blocker 2}

## Next Actions
1. {Next action 1}
2. {Next action 2}

## Context Preservation
{Important context for resume protocol}

## Validation
- Last validated: {timestamp}
- Consistency check: {PASS|FAIL}
```

### 3. Verify Consistency

Check that STATUS_LEDGER and LAST_KNOWN_STATE are consistent:
- [ ] Current objective matches active task
- [ ] Risk tier is same in both files
- [ ] Next actions are aligned
- [ ] Blockers are consistent

## Success Criteria
- [ ] STATUS_LEDGER.md updated
- [ ] LAST_KNOWN_STATE.md updated
- [ ] Consistency verified
- [ ] No placeholder values remaining

## Validation Checks
- [ ] All required fields filled
- [ ] No sections skipped (unless N/A)
- [ ] Timestamps populated
- [ ] Links valid
- [ ] No placeholder text like "[CURRENT OBJECTIVE]"

## Next Steps
- Commit STATE updates with descriptive message
- If part of PR: Include in PR
- If after merge: Create a follow-up PR with the STATE updates
