# Product Reality Map (Phase 2 Ingestion)

**Date**: 2026-01-29
**Status**: INITIATED
**Scope**: `APP/` directory (Foreign Workload)

## 1. Architecture Reality
The system is bifurcated between a partially-modernized structure and legacy application configurations.

| Component | Path | State | Reality |
|---|---|---|---|
| **Core API** | `APP/services/core-api` | **Legacy/Broken** | NestJS app. `package.json` references `../../packages/` (legacy layout). Missing workspace protocol. Build fails. |
| **Portal** | `APP/web/customer-trust-portal` | **Legacy/Broken** | Next.js app. `next.config.js` uses deprecated fields. Missing dev dependencies. Build fails. |
| **Libraries** | `APP/libs/*` | **Modern/Healthy** | 30+ packages (e.g., `@neuronx/playbook-engine`). Correctly use `workspace:*` protocol. `package.json` names align with `@neuronx/*` scope. |
| **Workspace** | Root | **Healthy** | `pnpm-workspace.yaml` correctly defines `APP/services/*`, `APP/web/*`, `APP/libs/*`. |

## 2. Dependency Reality (The Rift)
The build failures (D-01/D-04) are caused by `core-api` looking for ghosts.

*   **Expected**: `core-api` → imports `@neuronx/playbook-engine` → resolves to `APP/libs/playbook-engine`.
*   **Actual**: `core-api` `package.json` dependencies are likely missing or pointing to file paths that no longer exist, or simply not using the `workspace:*` protocol.
*   **Evidence**: `playbook-engine` exists in `APP/libs`, but `core-api` build complains "Cannot find module".

## 3. Invariants & Risks
*   **Invariant 1**: All internal dependencies MUST use `workspace:*` or `workspace:^`.
*   **Invariant 2**: No relative paths (`../../`) allowed in `package.json` dependencies.
*   **Risk**: Touching `core-api` might reveal deep type mismatches (already seen 250+ typescript errors).
*   **Strategy**: Fix the linking first (D-04) to expose the true compilation errors, then fix the errors (D-01).

## 4. Remediation Backlog (Phase 2 Decomposed)

### Unit 1: Dependency Linking (D-04) - **HIGH PRIORITY**
*   **Goal**: Make `core-api` and `libs` talk to each other.
*   **Action**: Update `APP/services/core-api/package.json` to adding/updating `@neuronx/*` dependencies with `workspace:*`.
*   **Verify**: `pnpm install` succeeds without linking warnings.

### Unit 2: Import Refactoring (D-05)
*   **Goal**: Fix internal relative imports.
*   **Action**: Scan `src/` for Broken References (e.g. `../voice/` vs `../sla/`).
*   **Verify**: `tsc` (compiler) runs further than the import stage.

### Unit 3: Type Stabilization (D-01)
*   **Goal**: Green build.
*   **Action**: Fix the ~250 TS errors revealed after Unit 1 & 2.

### Unit 4: Database Sync (D-03)
*   **Goal**: Runtime readiness.
*   **Action**: `prisma generate` and `prisma migrate`.
