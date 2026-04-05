# Browser Operator Architecture — NeuronX GHL Automation

Version: 1.0
Created: 2026-03-16
Status: ACTIVE

---

## 1. Problem Statement

GHL's workflow editor, form builder, and funnel page builder use Vue.js/Pinia with iframe-hosted SPAs. Playwright's DOM-level event dispatch (`click()`, `dispatchEvent()`, keyboard events) does NOT trigger Vue.js reactivity, so changes appear visually but do not persist to the GHL backend.

This document defines the MCP-based browser operator architecture that replaces fragile script-based Playwright automation.

---

## 2. Architecture Decision

### Primary Tool: Playwright MCP (`@playwright/mcp`)

| Factor | Decision |
|---|---|
| Package | `@playwright/mcp@latest` (Microsoft official) |
| Transport | stdio (Trae IDE native) |
| Connection mode | CDP endpoint (`--cdp-endpoint http://127.0.0.1:9222`) |
| Fallback mode | Storage state (`--storage-state .ghl-auth-state.json`) |
| LLM dependency | None (deterministic, accessibility-tree based) |
| Cost | Zero (no API keys required) |

### Why Playwright MCP

1. Connects to founder's existing logged-in Chrome session via CDP
2. Uses structured accessibility tree snapshots (not screenshots)
3. Deterministic tool application (no LLM token cost per action)
4. Persistent browser state across tool calls within a session
5. Native Trae IDE integration (stdio transport)
6. Already has Playwright in project dependencies

### Secondary Tool (Escalation): Stagehand

If Playwright MCP hits the same Vue.js persistence wall for workflow trigger/action configuration, Stagehand provides AI-native `act()` that dispatches events via CDP at a deeper level. Stagehand's `deepLocator()` handles iframe traversal automatically.

Stagehand requires an LLM API key and adds per-action cost, so it is only used for operations that Playwright MCP cannot complete.

---

## 3. Execution Hierarchy

```
Priority 1: GHL V2 API (durable, versioned, deterministic)
Priority 2: Playwright MCP via CDP (accessibility tree, deterministic)
Priority 3: Stagehand act() via CDP (AI-native, LLM-dependent)
Priority 4: Human manual configuration (founder checkpoint)
```

---

## 4. Connection Modes

### Mode A: CDP Connection (Primary)

```
Chrome (with --remote-debugging-port=9222)
  └── Playwright MCP (--cdp-endpoint http://127.0.0.1:9222)
       └── Trae IDE (stdio transport)
```

Launch script: `tools/ghl-lab/launch-chrome-cdp.sh`

Advantages:
- Uses founder's real Chrome profile (cookies, extensions, logged-in state)
- No separate auth management needed
- Can see exactly what the MCP server sees in the browser

### Mode B: Storage State (Fallback)

```
Playwright MCP (--browser chrome --storage-state .ghl-auth-state.json)
  └── Trae IDE (stdio transport)
```

Advantages:
- Works without pre-launching Chrome
- Auth state from previous Playwright sessions

Disadvantages:
- Launches fresh Chromium (not real Chrome)
- Auth state may be expired
- Cannot reuse existing tabs

---

## 5. Trae MCP Configuration

### CDP Mode (add to Trae MCP settings)

```json
{
  "Playwright-MCP-GHL": {
    "command": "npx",
    "args": [
      "-y",
      "@playwright/mcp@latest",
      "--cdp-endpoint", "http://127.0.0.1:9222",
      "--viewport-size", "1440x900",
      "--timeout-navigation", "30000",
      "--timeout-action", "10000"
    ],
    "env": {}
  }
}
```

### Storage State Mode (add to Trae MCP settings)

```json
{
  "Playwright-MCP-Auth": {
    "command": "npx",
    "args": [
      "-y",
      "@playwright/mcp@latest",
      "--browser", "chrome",
      "--storage-state", "/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.ghl-auth-state.json",
      "--viewport-size", "1440x900",
      "--timeout-navigation", "30000",
      "--timeout-action", "10000"
    ],
    "env": {}
  }
}
```

---

## 6. MCP Tools Available

Playwright MCP exposes these tools to the LLM/agent:

| Tool | Purpose | GHL Use Case |
|---|---|---|
| `browser_navigate` | Go to URL | Open workflow editor, form builder |
| `browser_snapshot` | Get accessibility tree | Read page structure, find elements |
| `browser_click` | Click element by ref | Click triggers, actions, buttons |
| `browser_type` | Type into element | Fill workflow names, template text |
| `browser_select_option` | Select dropdown value | Set form field options |
| `browser_drag` | Drag element | Form builder field reorder |
| `browser_press_key` | Press keyboard key | Escape modal, Enter to confirm |
| `browser_wait` | Wait for condition | SPA render time |
| `browser_tab_list` | List open tabs | Find GHL tab |
| `browser_console_messages` | Read console | Debug Vue.js errors |
| `browser_evaluate` | Execute JavaScript | Query Vue/Pinia state directly |

---

## 7. GHL-Specific Patterns

### Navigating to Workflow Editor

```
1. browser_navigate → https://app.gohighlevel.com/v2/location/{locationId}/automation/list
2. browser_wait → 15s for SPA render
3. browser_snapshot → find workflow by name
4. browser_click → workflow link
5. browser_wait → 10s for editor iframe to load
6. browser_snapshot → read iframe content (trigger nodes, action nodes)
```

### Iframe Detection

GHL uses these iframe hosts:
- Workflow builder: `client-app-automation-workflows.leadconnectorhq.com`
- Form builder: `leadgen-apps-form-survey-builder.leadconnectorhq.com`

Playwright MCP's accessibility tree includes iframe content, so elements inside iframes are accessible without manual frame switching.

### Vue.js State Persistence Test

Before each configuration session, run a persistence test:
1. Add a test trigger to WF-01
2. Navigate away
3. Return and verify trigger exists
4. If not persisted → escalate to Stagehand or human

---

## 8. Files and Scripts

| File | Purpose |
|---|---|
| `tools/ghl-lab/launch-chrome-cdp.sh` | Launch Chrome with CDP on port 9222 |
| `tools/ghl-lab/src/testMcpCdp.ts` | Test CDP connection via Playwright |
| `tools/ghl-lab/.ghl-auth-state.json` | Playwright auth state (gitignored) |
| `tools/ghl-lab/.tokens.json` | OAuth tokens (gitignored) |

---

## 9. Known Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Vue.js still ignores MCP clicks | Workflow config impossible via automation | Escalate to Stagehand, then human manual |
| Auth state expired | Connection fails | Re-login via Chrome, re-save state |
| GHL SPA changes | Selectors/accessibility tree changes | Snapshot before each action, adapt |
| CDP port conflict | Can't connect | Kill existing Chrome, relaunch |

---

## 10. Decision Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-03-16 | Selected Playwright MCP as primary | Zero LLM cost, CDP connect, Trae native, deterministic |
| 2026-03-16 | Stagehand as secondary (escalation only) | AI-native iframe/Vue support, but LLM-dependent |
| 2026-03-16 | Rejected Browserbase | Cloud-only, paid SaaS, can't use local Chrome |
| 2026-03-16 | Rejected Browser-use | Python-based, same Puppeteer limitations |
| 2026-03-16 | Chrome DevTools MCP kept for debugging | Already installed, useful for performance analysis |
