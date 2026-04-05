---
description: Invoke Trae for T1/T2 review
---

# Invoke Trae Review Workflow

## Purpose
Invoke Trae (external security and policy reviewer) for all T1/T2 PRs.

## When to Use
- PR labeled `tier-1` or `critical`
- PR labeled `tier-2` or `high-risk`
- Protected paths changed (GOVERNANCE/, AGENTS/, COCKPIT/, .github/workflows/, STATE/)
- Machine Board flags Trae check required

## Steps

### 1. Verify Trae Review Required
Check if any of these conditions are met:
- [ ] PR is T1 or T2
- [ ] Protected path changed
- [ ] Machine Board flagged

### 2. Prepare Trae Review Request
Gather required information:
- PR number and URL
- Changed files
- Risk tier
- PLAN artifact (if exists)
- Verification proof (if exists)

### 3. Invoke Trae
// Note: Actual Trae invocation mechanism depends on Trae API/service
// This is a placeholder for the invocation process

Create request payload:
```yaml
pr_number: {PR_NUMBER}
pr_url: {PR_URL}
risk_tier: {T1|T2}
changed_files:
  - path/to/file1
  - path/to/file2
review_scope:
  - GOVERNANCE/GUARDRAILS.md
  - scripts/governance_validator.py
```

### 4. Wait for Trae Verdict
Possible verdicts:
- APPROVE: No issues, safe to merge
- REJECT: Critical issues found
- REQUEST_CHANGES: Issues found, must address and re-request before merge
- EMERGENCY_OVERRIDE: Trae unavailable, critical fix
- ERROR: Trae service error

### 5. Create TRAE_REVIEW Artifact
Create file: `COCKPIT/artifacts/TRAE_REVIEW/TRAE-YYYYMMDD-{PR}.yml`

```yaml
ARTIFACT_TYPE: TRAE_REVIEW
artifact_id: "TRAE-YYYYMMDD-{PR}"
created_at: "{TIMESTAMP}"
created_by: "Factory (based on Trae verdict)"

pr_number: {PR}
pr_url: "{PR_URL}"

# TRAE'S VERDICT
verdict: "{APPROVE|REJECT|REQUEST_CHANGES|EMERGENCY_OVERRIDE|ERROR}"
signature: "trae-external-reviewer"

# VISION ALIGNMENT CHECK
vision_alignment: "{YES|CONCERNS|NO}"
vision_concerns: []

review_scope:
  - "path/to/file1"
  - "path/to/file2"

security_findings: []
policy_violations: []

recommendations: |
  {Trae's recommendations}

review_timestamp: "{TIMESTAMP}"
expiry_days: 7

links:
  github_pr: "{PR_URL}"
  artifact_file: "COCKPIT/artifacts/TRAE_REVIEW/TRAE-YYYYMMDD-{PR}.yml"
  vision_document: "FOUNDATION/01_VISION.md"
```

### 6. Update PR with Trae Verdict
Add comment to PR with Trae verdict and link to artifact.

## Success Criteria
- [ ] Trae invoked successfully
- [ ] Trae verdict received
- [ ] TRAE_REVIEW artifact created
- [ ] PR updated with verdict
- [ ] Machine Board validation passes

## Emergency Override
If Trae service unavailable and critical fix needed:
1. Declare emergency in PR description
2. Get founder authorization
3. Create EMERGENCY_OVERRIDE artifact
4. Post-merge review required when Trae restored

## Next Steps
- If APPROVE: Machine Board allows merge
- If REJECT: Fix issues and re-request Trae
- If REQUEST_CHANGES: Fix issues and re-request Trae
- If EMERGENCY_OVERRIDE: Merge with post-review required
