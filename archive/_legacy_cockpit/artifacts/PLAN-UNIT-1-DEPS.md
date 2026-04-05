# PLAN: Fix Core API Dependencies (Unit 1)

**Task**: Fix Broken Dependency Linking (D-04)
**Risk Tier**: **T2 (High Risk)** - Modifies build configuration and dependencies.
**Owner**: Factory (Code Agent)

## 1. Goal
Restore the connection between `core-api` and the workspace libraries (`APP/libs/*`). Currently, `core-api` fails to build because it cannot resolve `@neuronx/*` imports.

## 2. Invariants
*   **Protocol**: All internal dependencies MUST use `workspace:*` or `workspace:^`.
*   **Pathing**: No relative paths (`../../`) allowed in `package.json`.
*   **Scope**: Only modify `APP/services/core-api/package.json`. Do NOT touch `src/` code yet.

## 3. Required Changes

### `APP/services/core-api/package.json`
*   **Remove**: Any dependencies pointing to `file:../../packages/` or similar legacy paths.
*   **Add/Update**:
    *   `"@neuronx/playbook-engine": "workspace:*"`
    *   `"@neuronx/decision-engine": "workspace:*"`
    *   `"@neuronx/voice-twilio": "workspace:*"`
    *   `"@neuronx/adapter-sdk": "workspace:*"` (and others revealed by `list_dir APP/libs`)

## 4. Verification Plan
1.  **Install**: Run `pnpm install` (must succeed with no "missing peer" warnings).
2.  **Build Check**: Run `pnpm --filter @neuronx/core-api build`.
    *   *Expectation*: It will likely still FAIL, but with *different* errors (TypeScript errors inside `src/` instead of "Module not found").
    *   *Success Criteria*: Error messages shift from "Cannot find module" to "Type mismatch".

## 5. Rollback Plan
*   Revert `package.json` changes via git checkout.
