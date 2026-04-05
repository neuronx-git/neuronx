# NeuronX Archive

**Status**: Historical reference only  
**Authority**: Non-authoritative  
**Last Updated**: 2026-03-13

---

## What This Directory Contains

This `/archive` directory contains historical documents, drafts, and reference
material from earlier phases of the NeuronX project. These files are preserved
for traceability and context but are **not authoritative**.

---

## Authority Rule

**The governing canon for NeuronX lives exclusively in `/docs`.**

If any file in `/archive` conflicts with a file in `/docs`, the `/docs` version
wins without exception.

---

## Directory Structure

| Directory | Contents | Era |
|---|---|---|
| `_legacy_product/` | Original PRODUCT/ canon documents (VISION_CANON.md, PRD.md, etc.) | Pre-v3.0 |
| `_legacy_cockpit/` | COCKPIT governance artifacts, review documents, migration plans | Pre-v3.0 |
| `_legacy_agents/` | AGENTS/ role definitions, Trae review docs | Pre-v3.0 |
| `_legacy_governance/` | GOVERNANCE/ policies and approval gates | Pre-v3.0 |
| `_legacy_foundation/` | FOUNDATION/ AE-OS framework documents | Pre-v3.0 |

---

## When to Reference These Files

You may look here for:
- Historical context on why decisions were made
- Implementation clues in old code references
- Research notes that may inform build decisions
- Audit trails and review history

Do **not** use these files for:
- Current product requirements
- Operational specifications
- Trust boundaries or compliance rules
- Architecture decisions

---

## Deletion Policy

These files will be deleted **only after**:
1. v1 is live and stable
2. All useful information has been extracted or migrated to `/docs`
3. Founder explicitly approves deletion

Until then: **archive, don't delete.**
