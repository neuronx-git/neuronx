## Phase 1: Repository Access Configuration
- Confirm repository root is readable and discoverable.
- Verify `FRAMEWORK/` and `PRODUCT/` are accessible and listable.
- Verify `COCKPIT/artifacts/TRAE_REVIEW/` exists; confirm write access by creating the review artifact file in Phase 4 (this is the definitive permission check).

## Phase 2: Prompt Execution Protocol
- Load and apply the full instructions in `FRAMEWORK/TRAE_HANDOFF_PROMPT.md`, including the mandated markdown structure and allowed verdict values.
- Enumerate every file in `PRODUCT/` and build a checklist to ensure each file is reviewed.

## Phase 3: Comprehensive PRODUCT Review
- Read each `PRODUCT/*.md` document end-to-end.
- For each document, extract:
  - Core claims/requirements (market, ICP, roadmap, architecture, compliance).
  - Internal consistency issues (within-file).
  - Cross-document consistency issues (between files).
  - Security/compliance realism gaps (esp. SOC 2 timelines, data handling, dependency risks).
- Record every deficiency with:
  - Severity label: Critical / Major / Minor.
  - Exact file path and line ranges.
  - Specific, actionable remediation steps.

## Phase 4: Generate Review Artifact
- Create `COCKPIT/artifacts/TRAE_REVIEW/REVIEW_PHASE_A.md`.
- Use the exact skeleton required by `TRAE_HANDOFF_PROMPT.md`.
- Ensure the artifact also satisfies the workflow’s needs by:
  - Making findings explicit and actionable.
  - Including recommendations as “Mitigation Proposed” (risk table) and checkbox action items.
  - Issuing a single clear verdict in the required verdict field.

## Phase 5: Review Outcome Determination & Workflow Communication
- Choose verdict:
  - APPROVE only if no material deficiencies exist.
  - REQUEST_CHANGES if any deficiencies exist (mapped to the workflow’s “REQUESTS CHANGES” intent).
- After successfully writing the artifact, respond with exactly:
  - `Trae has finished`
- Provide no additional commentary in the chat response to preserve the blind review protocol.