
## 9. Skyvern Execution Mode (2026-03-17)

### Strategy Switch
- **Previous Status**: Playwright/MCP failed persistence. Browser-Use failed credits.
- **New Status**: Skyvern Cloud is now the primary visual operator.
- **Architecture**: Trae (Planner) -> Skyvern Agent (Operator) -> GHL (Target).

### Implementation Details
- **SDK**: `@skyvern/client` (npm) was broken/missing. Used direct fetch to `https://api.skyvern.com/api/v1`.
- **Session Management**: `tools/ghl-lab/src/skyvern/SkyvernAgent.ts` manages persistent sessions (`pbs_...`).
- **Auth Strategy**: User logs in manually via Skyvern Live View URL (Founder Interaction Policy).
- **Execution Loop**: Atomic operations (Observe -> Plan -> Act -> Verify).

### Current Session
- **Session ID**: `pbs_506976117979052016`
- **Live View**: `https://app.skyvern.com/browser-session/pbs_506976117979052016`
- **Status**: Waiting for user login.
