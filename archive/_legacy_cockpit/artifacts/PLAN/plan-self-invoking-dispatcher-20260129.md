# Implementation Plan: Phase 1 — Self-Invoking Dispatcher

**Date**: 2026-01-29
**Objective**: Make Antigravity self-invoking via GitHub Issue labels, removing the need for manual task relay by the Founder.
**Risk Tier**: T2 (Automation Infrastructure Change)

## Goals
1. **Zero-Copy Handoff**: Founder triggers execution by approving/labeling, not copy-pasting.
2. **Automated PR Creation**: Factory creates PRs automatically with required artifacts.
3. **Trae Enforcement**: Governance remains intact.
4. **Founder Clarity**: Simplify Founder interactions to high-level approvals.

## Non-Goals
- Changing the codebase structure (APP/ or PRODUCT/).
- Implementing a full-blown AI agent (we use the existing simple python dispatcher first).

## Proposed Changes

### 1. Workflows
#### [MODIFY] [.github/workflows/dispatcher.yml](file:///Users/ranjansingh/Desktop/NeuronX/NeuronX/.github/workflows/dispatcher.yml)
- **Change**: Grant write permissions (contents, pull-requests).
- **Change**: Ensure `FACTORY_PAT` or `GITHUB_TOKEN` is used for PR creation.
- **Change**: Pass `ISSUE_BODY` and contexts correctly to the script.

### 2. Scripts
#### [MODIFY] [scripts/dispatch_factory.py](file:///Users/ranjansingh/Desktop/NeuronX/NeuronX/scripts/dispatch_factory.py)
- **Change**: Implement "Mock Factory" logic for Phase 1 that:
    1. Reads Issue Body.
    2. Creates a new branch `factory/issue-{n}`.
    3. Creates a dummy "Work" commit (files changed).
    4. Creates a PR referencing the Issue.
    5. Adds `PLAN` and `VERIFICATION` headers to PR body.
    6. Comments on Issue with PR link.

### 3. Governance & Configuration
#### [NEW] [AGENTS/MODEL_ROUTING.md](file:///Users/ranjansingh/Desktop/NeuronX/NeuronX/AGENTS/MODEL_ROUTING.md)
- **Content**: Define default models for Planner (Antigravity), Executor (Factory), and Reviewer (Trae).

#### [MODIFY] [RUNBOOKS/OPERATING_MANUAL.md](file:///Users/ranjansingh/Desktop/NeuronX/NeuronX/RUNBOOKS/OPERATING_MANUAL.md)
- **Change**: Update "Daily Founder Workflow" to remove "Resume Autonomous Work" manual copy-paste.

#### [MODIFY] [FRAMEWORK/HANDOFF_RULES.md](file:///Users/ranjansingh/Desktop/NeuronX/NeuronX/FRAMEWORK/HANDOFF_RULES.md)
- **Change**: Explicitly define the `ready-for-factory` label trigger.

### 4. Founder Playbook
#### [NEW] [FOUNDATION/09_FOUNDER_PLAYBOOK.md](file:///Users/ranjansingh/Desktop/NeuronX/NeuronX/FOUNDATION/09_FOUNDER_PLAYBOOK.md)
- **Content**: Define "What Requires Approval" vs "What is Autonomous".

## Verification Plan

### Automated
1. **Link Validation**: Dispatcher workflow logs "Success" and links to PR.
2. **Governance Check**: `machine-board` workflow passes on the Factory-created PR.

### Manual Verification
1. Create Test Issue "Test Self-Invoking".
2. Label `ready-for-factory`.
3. Verify PR created.
4. Verify PR body formats.
