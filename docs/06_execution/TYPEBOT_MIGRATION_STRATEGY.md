# GHL Forms → Typebot Migration Strategy

**Date**: 2026-04-11
**Status**: RECOMMENDATION

---

## Current Forms Inventory

| Form | Platform | Status | Purpose |
|------|----------|--------|---------|
| Immigration Inquiry (V1) | GHL | LIVE | Initial intake — program, contact info, consent |
| VMC Client Onboarding | Typebot (self-hosted) | LIVE | Post-retainer onboarding — 8 programs, 16 groups, file upload |
| RCIC Outcome Survey | GHL | LIVE | Post-consultation — 5 fields |
| Client Satisfaction Survey | Not built | - | Post-case feedback |
| Document Upload Form | Not built | - | Document collection |

---

## Migration Evaluation

### Forms to KEEP in GHL

| Form | Reason |
|------|--------|
| RCIC Outcome Survey | Internal form (RCIC fills out), 5 simple fields. No benefit from conversational UX. GHL stores data natively in custom fields. |

### Forms to MIGRATE to Typebot

| Form | Priority | Reason |
|------|----------|--------|
| Immigration Inquiry (V1) | P1 | Conversational UX increases completion 2-3x. Typebot can branch by program, call NeuronX API mid-flow for scoring, and show dynamic doc checklists. GHL form is flat with no conditional logic. |
| Client Satisfaction Survey | P2 | Conversational format feels less like a chore. Can include NPS question with follow-up branching. |
| Document Upload Form | P2 | Typebot supports file uploads (self-hosted). Can show dynamic checklist per program. GHL portal is clunky for document collection. |

### Forms to BUILD NEW in Typebot

| Form | Priority | Description |
|------|----------|-------------|
| Consultation Prep Questionnaire | P1 | Pre-consultation form sent after booking. Program-specific deep questions. Webhook to NeuronX API generates briefing. |
| Document Collection Wizard | P2 | Step-by-step guided upload per document type. Shows checkmarks as documents are uploaded. |

---

## Migration Pros/Cons

### Pros of Typebot Migration
- 2-3x form completion rates (conversational UX vs traditional forms)
- Mid-flow API calls (real-time scoring, dynamic content)
- File upload support (self-hosted = unlimited, free)
- Full white-label (no "Powered by" branding)
- Conditional branching with visual builder
- Webhook on submit → NeuronX API → GHL custom fields
- JSON portable (export/import between environments)
- Same API format for Cloud and self-hosted

### Cons of Typebot Migration
- Data doesn't auto-populate GHL custom fields (needs webhook middleware)
- Two systems to maintain (GHL + Typebot)
- Self-hosted requires Railway maintenance ($15/mo)
- Typebot visual builder required for complex forms (API has limitations)
- No native GHL contact creation (webhook → NeuronX API → GHL API required)

### Data Flow After Migration

```
Prospect fills Typebot form
  → Typebot fires webhook to NeuronX API
  → NeuronX API creates/updates GHL contact with custom fields
  → NeuronX API scores lead (POST /score/form)
  → NeuronX API adds appropriate tags to GHL contact
  → GHL workflows trigger based on tags (WF-01, WF-04, etc.)
```

---

## Implementation Plan

### Phase 1: Replace Intake Form (Week 1)
1. Build new "Immigration Assessment" form in Typebot visual builder
2. Include: welcome, personal info, program selection, program-specific questions, consent
3. Add mid-flow scoring call to NeuronX API
4. Add webhook on submit → POST /typebot/webhook
5. Test: form submit → GHL contact created → WF-01 fires
6. Replace GHL form URL on landing page with Typebot embed

### Phase 2: Build Consultation Prep Form (Week 2)
1. Build pre-consultation questionnaire in Typebot
2. Program-specific deep questions (timeline, documents, budget)
3. Webhook → NeuronX API generates briefing
4. Send Typebot link in WF-05 confirmation email

### Phase 3: Document Collection Wizard (Week 3)
1. Build guided upload form per program
2. Show checklist, mark completed items
3. File uploads to MinIO (self-hosted)
4. Webhook → NeuronX API updates case status

---

## Customizable Typebot Elements (Current Status)

| Element | Current | Optimized |
|---------|---------|-----------|
| Welcome GIF | UN Migration GIF (professional) | **DONE** - Updated from SpongeBob |
| Bot name | "VMC Client Onboarding" | Could add "Maya" or "Nova" as bot persona |
| Chat bubble colors | Navy #0F172A (host) + Red #E8380D (guest) | **DONE** - VMC brand |
| Button colors | Red #E8380D | **DONE** - VMC brand |
| Font | Inter | **DONE** - Professional, readable |
| Background | Light gray #F9FAFB | **DONE** - Clean |
| Avatar | None set | **RECOMMEND**: Add VMC logo as bot avatar |
| Input placeholder | Default | Could customize per field |
| Progress bar | Not configured | Could add to show form completion % |
| Custom CSS | Not configured | Could add for further branding |
