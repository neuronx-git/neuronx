# Autonomous Testing — Claude Agent SDK + Playwright MCP

## Purpose

Exploratory testing that discovers **unknown** failure modes. This layer is
NOT for regression (that's pytest + Shiplight). It's for finding edge cases
that humans miss and deterministic tests don't cover.

## How To Run

### Via Claude Code (Recommended)
```bash
# Start Claude Code in the repo
claude

# Then ask it to run exploratory tests:
> Run the autonomous form testing scenarios in tests/autonomous/scenarios/
> Use Playwright MCP to navigate and interact with the forms
```

### Via Claude Agent SDK (Programmatic)
```python
from claude_code_sdk import Claude

agent = Claude()
result = agent.run(
    prompt=open("tests/autonomous/scenarios/typebot_form_exploration.md").read(),
    tools=["playwright_mcp"],
    max_turns=50,
)
```

## Scenarios

| File | What It Tests | Estimated Time |
|------|---------------|----------------|
| `typebot_form_exploration.md` | All 8 program branches, field validation | 10-15 min |
| `form_reload_behavior.md` | Submit → reload → submit again, check duplication | 5 min |
| `multi_tenant_branding.md` | Load each tenant, screenshot compare | 5 min |
| `api_edge_cases.md` | Boundary payloads via API | 3 min |
| `full_pipeline.md` | Form → webhook → score → GHL tags (mocked) | 10 min |

## Guardrails

- **Environment**: Only `localhost:8000` and staging Railway URL
- **No destructive actions**: No DELETE, no prod contact creation
- **Artifact capture**: Screenshots + JSON report for every run
- **Max API calls**: 100 per run
- **Manual trigger only**: Never a CI gate
