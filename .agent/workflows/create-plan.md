---
description: Create PLAN artifact for non-trivial changes
---

# Create PLAN Artifact Workflow

## Purpose
Create a PLAN artifact in COCKPIT/artifacts/PLAN/ for any non-trivial change (T2/T3 risk tier).

## When to Use
- Non-trivial code changes
- Governance changes
- Infrastructure changes
- Any change requiring planning discipline

## Prerequisites

**MANDATORY**: Before using this workflow, Antigravity MUST have completed the startup sequence:
- ✅ FOUNDATION/01_VISION.md loaded
- ✅ STATE/STATUS_LEDGER.md loaded
- ✅ STATE/LAST_KNOWN_STATE.md loaded
- ✅ COCKPIT/WORKSPACE/TEAM_LOG.md loaded

**If startup sequence not completed**: Cannot proceed with planning. Complete startup first.

---

## Steps

### 1. Verify Vision Loaded (MANDATORY)
Confirm FOUNDATION/01_VISION.md has been loaded during startup sequence.

**Vision Alignment Check**: All PLAN artifacts MUST include Vision alignment section.

### 2. Assess Risk Tier
Determine risk tier based on GOVERNANCE/RISK_TIERS.md:
- T0: Informational (read-only)
- T3: Low risk (reversible, local scope)
- T2: High risk (broader impact, harder to reverse)
- T1: Critical (production, security, payments)

### 3. Estimate Cost
Calculate estimated cost:
- Tokens (input + output)
- Infrastructure (compute, API calls)
- Total cost estimate

### 4. Create PLAN Artifact
Create file: `COCKPIT/artifacts/PLAN/PLAN-YYYYMMDD-{description}.md`

Required sections:
- **Objective**: What success means
- **Non-Goals**: Explicit exclusions
- **Files/Directories Touched**: List of affected files
- **Risk Tier**: T0/T1/T2/T3
- **Rollback Strategy**: How to undo changes
- **Cost Estimate**: Total estimated cost
- **Verification Plan**: How to verify success
- **Vision Alignment**: How this aligns with FOUNDATION/01_VISION.md

### 5. Update STATE
// turbo
```bash
# Update STATUS_LEDGER with planning status
# Update LAST_KNOWN_STATE with PLANNING state
```

## Success Criteria
- [ ] PLAN artifact created in COCKPIT/artifacts/PLAN/
- [ ] All required sections present
- [ ] Risk tier assigned
- [ ] STATE files updated
- [ ] Vision alignment confirmed

## Next Steps
- If T1/T2: Request approval via Approvals Queue
- If T3: Proceed to execution
- If T0: No PLAN needed
