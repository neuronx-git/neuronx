# NeuronX

**AI-Assisted Sales and Intake Operating System for Immigration Consulting Firms**

---

## Quick Start

| I want to... | Go to |
|---|---|
| Understand what NeuronX is | `/docs/01_product/vision.md` |
| See what v1 must do | `/docs/01_product/prd.md` |
| Build or operate the system | `/docs/02_operating_system/operating_spec.md` |
| Run the sales process | `/docs/02_operating_system/sales_playbook.md` |
| Build Phase 1 in GoHighLevel (no code) | `/docs/02_operating_system/ghl_configuration_blueprint.md` |
| Integrate with GoHighLevel | `/docs/03_infrastructure/ghl_capability_map.md` |
| Understand system boundaries | `/docs/03_infrastructure/product_boundary.md` |
| Validate GHL leverage (capability audit) | `/docs/03_infrastructure/capability_lock_audit.md` |
| Run the live bake-off before architecture | `/docs/03_infrastructure/live_tenant_bakeoff_scorecard.md` |
| Ensure compliance | `/docs/04_compliance/trust_boundaries.md` |
| See what's undecided | `/docs/05_governance/open_decisions.md` |

---

## Document Authority

**Authoritative (Live Canon)**

Only `/docs/...` is authoritative. The governing hierarchy:

1. `/docs/04_compliance/trust_boundaries.md` — **overrides everything**
2. `/docs/01_product/vision.md` — product direction
3. `/docs/01_product/prd.md` — requirements
4. `/docs/02_operating_system/operating_spec.md` — implementation blueprint
5. `/docs/02_operating_system/sales_playbook.md` — human operations
6. `/docs/03_infrastructure/` — infrastructure and boundaries
7. `/docs/05_governance/open_decisions.md` — unresolved decisions

**Non-Authoritative (Reference Only)**

`/archive/` contains historical documents. If archive conflicts with `/docs`,
`/docs` wins.

---

## What NeuronX Is

NeuronX is the AI-assisted sales and intake operating system for Canadian
immigration consulting firms. It transforms the inquiry-to-retainer pipeline
into a high-performance, operationally disciplined system.

**Core principle**: GoHighLevel is the infrastructure. NeuronX is the
orchestration and intelligence layer on top.

---

## What NeuronX Is NOT

- NOT a CRM (GoHighLevel is the CRM)
- NOT a case management system
- NOT a voice provider
- NOT a multi-vertical platform (v1)
- NOT a self-serve product (premium onboarding)

---

## Repository Structure

```
NeuronX/
├── docs/                    ← AUTHORITATIVE CANON
│   ├── 01_product/          ← Vision and requirements
│   ├── 02_operating_system/ ← Operating spec and sales playbook
│   ├── 03_infrastructure/   ← GHL capabilities and product boundaries
│   ├── 04_compliance/       ← Trust boundaries and regulatory rules
│   └── 05_governance/       ← Open decisions
├── archive/                 ← HISTORICAL REFERENCE
│   ├── _legacy_product/
│   ├── _legacy_cockpit/
│   ├── _legacy_agents/
│   ├── _legacy_governance/
│   └── _legacy_foundation/
├── APP/                     ← Code (existing, reference only for v1)
│   ├── libs/
│   ├── services/
│   └── web/
└── README.md                ← This file
```

---

## Status

- **Product Canon**: v3.0 CANONICAL (in `/docs/`)
- **V1 Scope**: Defined in `/docs/02_operating_system/operating_spec.md`
- **Open Decisions**: 13 (see `/docs/05_governance/open_decisions.md`)
- **Build Status**: Not started — architecture phase pending

---

## Next Steps

1. **Resolve open decisions** (especially OD-01 voice provider, OD-13 tech boundary)
2. **Architecture phase** — design the orchestration service
3. **Build v1** — implement per operating_spec.md

---

## Contact

This is a founder-led project. All canon changes require founder approval.
