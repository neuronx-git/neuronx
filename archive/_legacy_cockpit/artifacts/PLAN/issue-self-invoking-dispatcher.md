# Issue: Self-Invoking Dispatcher Implementation

**Status**: 🟢 OPEN
**Labels**: `ready-for-factory`, `automation`, `T2`
**Assignee**: Factory

## Description
Implement the self-invoking dispatcher as per `COCKPIT/artifacts/PLAN/plan-self-invoking-dispatcher-20260129.md`.

## Acceptance Criteria
- [ ] `dispatcher.yml` triggers on label `ready-for-factory`.
- [ ] `dispatch_factory.py` can create a branch and PR.
- [ ] Trae enforcement is NOT bypassed.
- [ ] Governance artifacts are updated.

## Risks
- Infinite loops if dispatcher triggers itself (ensure ignoring own PRs).
- Secret leakage (ensure `FACTORY_API_KEY` is handled safely).
