# Backlog: MVP Rehydration (Sprint 1)

**Goal**: Validate and Operationalize the Rehydrated Codebase.

## Epics

### EPIC-1: Platform Foundation
- [ ] **TASK-1.1**: Verify `tenancy` service isolation.
- [ ] **TASK-1.2**: Validate `billing-entitlements` schema.
- [ ] **TASK-1.3**: Test `ollama-gateway` connectivity.

### EPIC-2: GHL Integration
- [ ] **TASK-2.1**: Run integration tests for `adapters-ghl`.
- [ ] **TASK-2.2**: Verify `ghl-snapshots` deployment logic.
- [ ] **TASK-2.3**: Check `ghl-drift` detection mechanism.

### EPIC-3: Playbook Engine
- [ ] **TASK-3.1**: Execute sample playbook in `playbook-engine`.
- [ ] **TASK-3.2**: Verify `playbook-governance` rules are enforced.

### EPIC-4: Voice Orchestration
- [ ] **TASK-4.1**: Mock voice provider for `voice-orchestration` tests.

## Definition of Done (Rehydration)
- Component has passing unit tests.
- Component is documented in `FRAMEWORK_KNOWLEDGE/`.
- Component is listed in `PRODUCT/PRD.md`.
