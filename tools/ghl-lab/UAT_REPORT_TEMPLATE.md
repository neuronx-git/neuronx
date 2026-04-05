# NeuronX V1 — UAT Test Report (Template)

Date:
Tester:
Environment:

---

## Deliverables

1. Working test website URL:
2. GHL dashboard URL (Test Lab):
3. Snapshot installer:
   - Snapshot name:
   - Snapshot ID:
   - Share link (if used):
4. Second test sub-account (Snapshot Install Lab) dashboard URL:
5. Test report of each scenario: see below
6. List of capabilities used from GHL: see below
7. List of capabilities unused from GHL: see below
8. API gaps discovered: see below

---

## Locations

| Label | Location ID | Dashboard URL |
|---|---|---|
| NeuronX Test Lab |  | https://app.gohighlevel.com/location/<locationId> |
| NeuronX Snapshot Install Lab |  | https://app.gohighlevel.com/location/<locationId> |

---

## Test Scenarios

| Test | Result | Evidence | Notes |
|---|---|---|---|
| TEST 1 — New lead flow |  | Screenshots / video |  |
| TEST 2 — AI call attempt |  | Call logs / transcript |  |
| TEST 3 — Booking flow |  | Calendar booking record |  |
| TEST 4 — Consultation reminder |  | SMS/email logs |  |
| TEST 5 — No-show recovery |  | Workflow execution log |  |
| TEST 6 — Consultation outcome |  | Field update + stage move |  |
| TEST 7 — Retainer automation |  | Email/SMS sequence + tasks |  |

---

## GHL Capabilities Used

- Website/Funnel pages
- Forms
- Pipelines (Opportunities)
- Custom fields
- Tags
- Workflows (triggers, waits, branches)
- Calendars + booking links
- Appointment triggers (Booked/Completed/No-show)
- SMS + Email templates
- Tasks + assignment
- DND / suppression / compliance
- Snapshot creation + share/install

---

## GHL Capabilities Unused (By Design)

- Custom app UI beyond standard GHL pages
- Building a parallel CRM or messaging layer
- Custom dashboarding (Phase 3 only if needed)
- Non-essential AI features not required for v1 outcomes

---

## API Gaps / Automation Gaps

| Gap | Impact | Workaround | Notes |
|---|---|---|---|
| Snapshot apply/install endpoint unclear | Phase 4 automation risk | Manual install or UI automation |  |
| Workflow creation/update endpoints limited | Hard to automate Phase 2 | Manual configuration + snapshot |  |
| Funnel/page build endpoints limited | Hard to automate website | Manual build in GHL |  |

---

## Notes

- Follow `/docs/02_operating_system/ghl_configuration_blueprint.md` for Phase 1/2 configuration.
- Run `/docs/03_infrastructure/live_tenant_bakeoff_scorecard.md` for Voice AI decisions and webhook security gates.

