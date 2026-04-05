## Scope & Inputs
- Review the governance canon and enforcement implementation referenced in the Trae prompt: FOUNDATION/*, GOVERNANCE/*, FRAMEWORK/HANDOFF_RULES.md, .agent/workflows/*, FRAMEWORK/ANTIGRAVITY_FEATURES_AUDIT.md, and the full request artifact.
- Treat this as a T2 governance framework change audit (non-execution review).

## Audit Method
- Vision alignment: Check the proposed self-configuration against the AE-OS constitution (Antigravity never writes code, Trae is independent, governance is enforced automatically).
- Security review: Evaluate whether one-writer rule, approval gates, and “cannot bypass” claims are actually enforced by repo controls (branch protection + Machine Board + Trae validator), not just documented.
- Policy compliance: Validate risk tier assignment, artifact requirements, and Trae review process against FOUNDATION/03_GOVERNANCE_MODEL.md and GOVERNANCE/GUARDRAILS.md.
- Technical soundness: Inspect the workflows and enforcement scripts for bypass paths, contradictions, unsafe automation signals (e.g., // turbo-all), and operational foot-guns.

## Findings To Capture (Already Identified)
- Enforcement gap risk: machine-board’s Trae requirement is based on protected paths + PR description tier parsing (not labels), while trae-review-validator’s label parsing appears broken due to `PR_LABELS: $${{ ... }}`; together this can create label-only bypasses.
- Verdict semantics mismatch: some docs describe REQUEST_CHANGES as merge-allowed, but both enforcement paths currently block anything not in {APPROVE, EMERGENCY_OVERRIDE}.
- Emergency override looseness: implementation treats any PR body containing “emergency” and “override” as sufficient, which is weaker than a strict, auditable token + authorization requirement.
- Workflow safety: update-state.md uses `// turbo-all` and includes guidance that could encourage direct-to-main commits; this should be constrained to PR-only flows in governance docs.
- Contract enforceability: ANTIGRAVITY_BEHAVIOR.md is binding as documentation, but its “enforceability” depends on Machine Board / branch protection coverage; highlight any areas that remain policy-by-convention.

## Output Deliverable
- Produce the requested file: `COCKPIT/artifacts/TRAE_REVIEW/TRAE_VERDICT-20260130-antigravity-self-config.md`.
- Use the exact section and table format from the prompt, with:
  - A clear overall verdict (APPROVE / REQUEST_CHANGES / REJECT).
  - A findings table including the concrete enforcement gaps above (with severity and assessment).
  - A short “Critical Issues” checklist focused on specific repo changes needed to make governance non-bypassable.
  - Concrete recommendations (doc alignment + code/workflow fixes), and next steps conditional on verdict.

## Post-Verdict Follow-Through (If You Confirm Execution)
- If verdict is REQUEST_CHANGES or REJECT, prepare a minimal, targeted patch set to close the identified bypasses (e.g., fix PR_LABELS interpolation, align verdict semantics, tighten emergency override detection, and constrain update-state workflow guidance), then propose it for review.