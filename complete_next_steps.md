# Complete Next Steps (NeuronX)

This file is the single “what to do next” entrypoint for the repo.

## Current Status (Already Done)

### Phase A Product Canon — Trae Verdict

- Initial review (changes requested): [REVIEW_PHASE_A.md](file:///Users/ranjansingh/Desktop/NeuronX/COCKPIT/artifacts/TRAE_REVIEW/REVIEW_PHASE_A.md)
- Re-review (approved): [REVIEW_PHASE_A_REREVIEW.md](file:///Users/ranjansingh/Desktop/NeuronX/COCKPIT/artifacts/TRAE_REVIEW/REVIEW_PHASE_A_REREVIEW.md)

If you are about to execute work that depends on the Product Canon, you can treat Phase A as approved unless you have made additional canon edits since the re-review.

## Immediate Next Steps (Baseline First)

### 1) Stabilize installs/builds (Week 1 priority)

Follow the existing dependency repair plan:

- [PLAN-UNIT-1-DEPS.md](file:///Users/ranjansingh/Desktop/NeuronX/COCKPIT/artifacts/PLAN-UNIT-1-DEPS.md)

Goal: get the workspace building so test/coverage numbers are trustworthy.

### 2) Establish a test + coverage baseline

Once builds pass, run the repo’s existing test commands and record:
- Overall pass/fail
- Coverage baseline per major package (especially `APP/services/core-api/`)

This baseline is the reference point for enforcing higher standards going forward.

## How To Use Trae (Only When Needed)

### When you should invoke Trae

Invoke Trae when you are introducing or changing **T1/T2** risk items (governance, security controls, Product Canon, CI quality gates, build system, authz, etc.).

### Phase A Product Canon Trae Prompt (Copy/Paste)

Use this prompt only if you are initiating a *new* Product Canon review (i.e., you changed `PRODUCT/` canon after the approved re-review):

- Prompt source: [TRAE_HANDOFF_PROMPT.md](file:///Users/ranjansingh/Desktop/NeuronX/FRAMEWORK/TRAE_HANDOFF_PROMPT.md)

### Antigravity Self-Configuration Trae Prompt (Copy/Paste)

Use this prompt only for the Antigravity governance/self-config review:

- Prompt source: [TRAE_PROMPT-antigravity-self-config.md](file:///Users/ranjansingh/Desktop/NeuronX/COCKPIT/artifacts/TRAE_REVIEW/TRAE_PROMPT-antigravity-self-config.md)

## Execution Roles (Quick Reference)

- Antigravity: planning and governance artifacts
- Factory: execution agent that applies changes and opens PRs
- Trae: independent reviewer that produces verdict artifacts

