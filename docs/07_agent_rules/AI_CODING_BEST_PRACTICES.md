# AI Coding Agent Best Practices — NeuronX

**Version**: 1.0
**Date**: 2026-03-21
**Authority**: CLAUDE.md references this file
**Scope**: Governs behavior of all AI agents working on NeuronX codebase

---

## Core Philosophy

**Ship working software. Update state. Escalate blockers. Don't over-engineer.**

Every action should move NeuronX closer to its first paying customer.
Governance serves shipping — not the other way around.

---

## 1. State Awareness (Most Important)

Every AI session MUST:

```
1. Read PROJECT_MEMORY.md — understand current state
2. Read COCKPIT/WORKSPACE/TEAM_LOG.md — understand recent decisions
3. Read docs/06_execution/CURRENT_STATE.md — know what's done vs pending
4. Read docs/05_governance/open_decisions.md — know what's blocked
```

**Before building anything, verify**:
- Is this already built? (Check CURRENT_STATE.md)
- Is this blocked by an open decision? (Check open_decisions.md)
- Does GHL already do this natively? (Check product_boundary.md)

**After completing anything, update**:
- `PROJECT_MEMORY.md` — what you completed
- `COCKPIT/WORKSPACE/TEAM_LOG.md` — log the event
- `docs/06_execution/CURRENT_STATE.md` — update status table

---

## 2. Tool Selection Hierarchy

### For GHL Configuration
```
Priority 1: GHL V2 API
  → Most reliable, fastest, no UI fragility
  → Use for: custom fields, tags, calendars, contacts, opportunities

Priority 2: Playwright (saved auth state)
  → When API doesn't support the operation
  → Use for: pipelines, forms, funnels

Priority 3: Skyvern (visual LLM)
  → When Playwright struggles with complex SPA interactions
  → Use for: workflows, complex UI flows
  → Requires: Skyvern session active (founder login)

Priority 4: Browser extension / founder session
  → Last resort for blocked automation
  → Document the pattern, then automate

Priority 5: Manual (founder action)
  → ONLY for: 2FA, CAPTCHA, billing confirmation, identity verification
  → Always provide exact steps + expected outcome
```

### For Code
```
Priority 1: GHL native workflow (no code needed)
Priority 2: GHL webhook + NeuronX API (thin wrapper)
Priority 3: Salvage from /APP/* (reference only, selective)
Priority 4: Write new code (last resort)
```

---

## 3. Incremental Testing

**Rule**: Never batch more than 1 unit of work without verifying.

```
Wrong: Configure WF-02 through WF-11, then test all.
Right: Configure WF-02 → verify → WF-03 → verify → WF-04 → verify...
```

**Verification checklist for each workflow**:
1. Open GHL Workflows list
2. Confirm workflow appears with PUBLISHED status
3. Check trigger type is correct
4. Check first action is correct
5. Record ID or confirmation in CURRENT_STATE.md

---

## 4. Error Handling & Retries

**If a tool call fails**:
1. Log the error in TEAM_LOG.md with exact error message
2. Try once with a modified approach
3. If still failing — escalate to TEAM_LOG.md with `[BLOCKER]` tag
4. Do NOT retry the same approach 3+ times

**Never**:
- Silently ignore failures
- Assume a workflow was saved without verifying
- Retry indefinitely hoping something changes

---

## 5. Compliance-First Development

**Before building any AI call feature**:
1. Read `docs/04_compliance/trust_boundaries.md`
2. Run `TrustService.check_transcript()` on test transcripts
3. Ensure all test cases pass before integration

**Trust boundary rules are HARD constraints**:
- AI must never assess eligibility
- AI must never recommend pathways
- Escalation triggers must be checked in every call

---

## 6. Secrets Discipline

**Never**:
- Paste API keys in code files
- Log tokens or secrets
- Commit `.env`, `.tokens.json`, `.ghl-auth-state.json`

**Always**:
- Read from environment variables
- Use `tools/ghl-lab/.tokens.json` for GHL tokens (gitignored)
- Reference `.env.example` as template

---

## 7. Documentation Discipline

**After every meaningful action**:
```python
# Pattern to follow:
1. Complete task
2. Verify task (don't assume)
3. Update CURRENT_STATE.md (change status from PENDING to DONE + add ID)
4. Log in TEAM_LOG.md with [PROGRESS] tag
5. Update PROJECT_MEMORY.md compact entry
```

**Never create random markdown files** in project root or COCKPIT/.
Use TEAM_LOG.md for all coordination.

---

## 8. Code Quality Standards

### Python (neuronx-api/)
```python
# Use pydantic for all data models
class ReadinessInput(BaseModel):
    contact_id: str
    r1_program_interest: Optional[ProgramInterest] = None

# Type hints everywhere
async def score_lead(payload: ReadinessInput) -> ReadinessScore:

# Meaningful logging
logger.info("Scored lead %s: %s (score=%d)", contact_id, outcome, score)

# No magic strings — use enums
class ReadinessOutcome(str, Enum):
    READY_STANDARD = "ready_standard"
```

### TypeScript (tools/ghl-lab/)
```typescript
// Always use TypeScript types
interface GHLContact {
  id: string;
  firstName: string;
  customFields: Array<{ key: string; fieldValue: string }>;
}

// Explicit error handling
try {
  const result = await skyvernClient.executeTask(goal);
  if (!result.success) throw new Error(`Skyvern task failed: ${result.error}`);
} catch (error) {
  logger.error('WF-02 configuration failed:', error);
  // Log to TEAM_LOG.md, don't swallow
}
```

---

## 9. Git Discipline

```bash
# Branch per feature
git checkout -b feat/wf-02-contact-attempts

# Commit after each verified unit
git commit -m "feat: configure WF-02 contact attempts — 7-step sequence (verified published)"

# Never commit
.tokens.json
.ghl-auth-state.json
.env
node_modules/
```

---

## 10. Escalation Protocol

**When blocked**:
1. Try for no more than 30 minutes
2. Log in TEAM_LOG.md: `[BLOCKER] YYYY-MM-DD — <description> — Owner: <Founder/Trae>`
3. Propose 2-3 alternative approaches
4. Continue with other tasks while waiting for resolution

**When discovering a new GHL limitation**:
1. Log in `docs/03_infrastructure/ghl_execution_memory.md` with date
2. Verify against `docs/03_infrastructure/product_boundary.md`
3. If product-impacting: escalate to TEAM_LOG.md with `[DECISION]` request

---

## 11. Week-Specific Priorities

### Currently: Week 1
**Focus**: GHL Gold Build completeness
**Success criteria**: 11 workflows + 4 UAT scenarios
**Do NOT start**: Voice integration, NeuronX API endpoints (Week 4)
**Do NOT spend time on**: Architecture debates, `/APP/*` codebase

### Week 2: Snapshot
**Focus**: Package Gold sub-account for replication
**Do NOT start**: Voice bake-off (Week 3)

### Week 3: Voice Bake-Off
**Focus**: Lock OD-01 (voice provider)
**Do NOT start**: Full NeuronX API build (Week 4)

### Week 4: Thin Brain
**Focus**: FastAPI webhook + scoring + briefings
**Do NOT start**: Pilot onboarding (Week 5)

---

## 12. Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | What to Do Instead |
|---|---|---|
| Building `/APP/*` for MVP | Over-engineered, not integrated | GHL-first always |
| Adding Make.com without proven blocker | Unnecessary complexity | Direct GHL↔VAPI webhooks first |
| Batching 10 workflows then testing | Hard to debug, wastes time | Verify after each WF |
| Silent failure on Skyvern task | State becomes unknown | Verify + log every task |
| Making voice decisions without bake-off | Locks wrong architecture | Run bake-off Week 3 |
| Creating random .md files in root | Document clutter | Use TEAM_LOG.md |
| Implementing features before OD resolved | May need to rebuild | Block on OD + escalate |
| Committing credentials | Security incident | .gitignore + env vars |

---

**This document governs AI coding agent behavior.**
**Updated when new lessons are learned. Add to `ghl_execution_memory.md` for GHL-specific patterns.**
