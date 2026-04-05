---
description: Generate daily brief at 09:00 UTC
---

# Daily Brief Generation Workflow

## Purpose
Auto-generate daily brief and approvals queue at 09:00 UTC for founder's 5-10 minute daily review.

## When to Use
- Automated: Every day at 09:00 UTC via .github/workflows/daily-brief.yml
- Manual: When founder requests status update

## Steps

### 1. Read Current State
// turbo
```bash
# Read STATUS_LEDGER
cat STATE/STATUS_LEDGER.md

# Read LAST_KNOWN_STATE
cat STATE/LAST_KNOWN_STATE.md
```

### 2. Scan GitHub State
Gather:
- Open PRs (count, status, labels)
- Open issues (count, priority, labels)
- Recent commits (last 24 hours)
- CI/CD status (passing/failing)
- Trae reviews pending

### 3. Generate Daily Brief

Create file: `COCKPIT/artifacts/DAILY_BRIEF/BRIEF-YYYYMMDD.md`

```markdown
# Daily Brief - YYYY-MM-DD

## Executive Summary
- Open PRs: {count}
- Issues: {blocked_count} blocked, {waiting_count} waiting for approval
- Trae review required: {count} PR(s)
- CI/CD status: {PASS|FAIL}

## Trae Review Required (T1-T2)
- PR #{NUMBER}: {Title}
  - Status: Waiting for Trae review
  - Risk Tier: {T1|T2}
  - Action: Factory will invoke Trae

## Approvals Queue
- PR #{NUMBER}: {Title}
  - Risk Tier: {T1|T2}
  - Waiting for: Founder explicit authorization
  - Action: Founder approves/denies via Approvals Queue

- Issue #{NUMBER}: {Title}
  - Risk Tier: {T2}
  - Waiting for: Approval to proceed
  - Action: Founder approves/denies

## Blocked Items
- Issue #{NUMBER}: {Title}
  - Blocked by: {Reason}
  - Estimated resolution: {timeframe}

## Completed Yesterday
- PR #{NUMBER}: {Title} - Merged
- Issue #{NUMBER}: {Title} - Closed

## Next Actions
1. {Action 1}
2. {Action 2}
3. {Action 3}

## Metrics
- Cycle time: {average_days} days
- Deployment frequency: {count} per week
- Test coverage: {percentage}%
- Cost (last 24h): ${amount}
```

### 4. Generate Approvals Queue

Create file: `COCKPIT/artifacts/APPROVALS_QUEUE/APPROVALS-YYYYMMDD.md`

```markdown
# Approvals Queue - YYYY-MM-DD

## Pending Approvals

### Production Deployment (T1 - Critical)
- **PR #{NUMBER}**: {Title}
  - **Risk Tier**: T1 (Critical)
  - **Type**: Production Deployment
  - **Waiting for**: Founder explicit authorization
  - **Rollback plan**: Tested and ready
  - **Trae verdict**: APPROVE
  - **Action**: Approve/Deny/Defer

**Decision**: [ ] YES  [ ] NO  [ ] DEFER
**Rationale**: _______________

---

### Database Migration (T2 - High)
- **Issue #{NUMBER}**: {Title}
  - **Risk Tier**: T2 (High)
  - **Type**: Database Migration
  - **Waiting for**: Approval to proceed
  - **Impact**: {description}
  - **Rollback plan**: {description}
  - **Action**: Approve/Deny/Defer

**Decision**: [ ] YES  [ ] NO  [ ] DEFER
**Rationale**: _______________

---

## Decisions Made
{List of decisions from previous days}
```

### 5. Create PR with Artifacts
Create PR with:
- Title: "Daily Brief - YYYY-MM-DD"
- Body: Link to BRIEF-YYYYMMDD.md and APPROVALS-YYYYMMDD.md
- Label: `daily-brief`
- Auto-merge: After founder review

## Success Criteria
- [ ] BRIEF-YYYYMMDD.md created
- [ ] APPROVALS-YYYYMMDD.md created
- [ ] PR created with artifact links
- [ ] Founder notified (via PR)

## Automation
This workflow should be automated via .github/workflows/daily-brief.yml:

```yaml
name: Daily Brief
on:
  schedule:
    - cron: '0 9 * * *'  # 09:00 UTC daily
  workflow_dispatch:  # Manual trigger

jobs:
  generate-brief:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate Daily Brief
        run: |
          # Run daily-brief workflow
          # Create artifacts
          # Create PR
```

## Next Steps
- Founder reviews daily brief (5-10 minutes)
- Founder makes decisions in Approvals Queue
- Antigravity reads decisions and proceeds
