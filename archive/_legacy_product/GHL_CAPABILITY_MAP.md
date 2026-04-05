# GoHighLevel Super Agency Pro — Capability Map

**Version**: v1.0
**Date**: 2026-02-03
**Status**: RESEARCH CHECKLIST
**Owner**: Product Droid
**Purpose**: Document GHL capabilities for NeuronX integration planning

---

## Overview

This document maps GoHighLevel (GHL) Super Agency Pro capabilities to determine what can be configured natively vs. what requires custom integration or code.

**Doctrine**: Configure-first. Only build code when native GHL configuration cannot achieve the requirement.

---

## 1. Native Features (Configure First)

### 1.1 CRM & Contact Management

| Feature | Native? | API Available? | NeuronX Action | Status |
|---------|---------|----------------|----------------|--------|
| Contact CRUD | YES | YES (`/contacts`) | Configure | **NEEDS VERIFICATION** |
| Custom Fields | YES | YES | Configure (up to 50?) | **NEEDS VERIFICATION** |
| Tags | YES | YES | Configure | **NEEDS VERIFICATION** |
| Contact Search | YES | YES (query params) | Configure | **NEEDS VERIFICATION** |
| Contact Import/Export | YES | LIMITED (CSV) | Configure native, build for automation | **NEEDS VERIFICATION** |
| Smart Lists | YES | LIMITED | Configure | **NEEDS VERIFICATION** |
| Contact Merge | YES | ? | Configure | **NEEDS VERIFICATION** |

### 1.2 Pipeline & Opportunities

| Feature | Native? | API Available? | NeuronX Action | Status |
|---------|---------|----------------|----------------|--------|
| Pipeline Creation | YES | YES (`/opportunities/pipelines`) | Configure | **NEEDS VERIFICATION** |
| Stage Management | YES | YES | Configure | **NEEDS VERIFICATION** |
| Opportunity CRUD | YES | YES (`/opportunities`) | Configure | **NEEDS VERIFICATION** |
| Pipeline Automation | YES | NO (workflow-based) | Configure via workflows | **NEEDS VERIFICATION** |
| Custom Fields | YES | YES | Configure | **NEEDS VERIFICATION** |
| Pipeline Reporting | YES | LIMITED | Configure, may need integration | **NEEDS VERIFICATION** |

### 1.3 Workflows & Automation

| Feature | Native? | API Available? | NeuronX Action | Status |
|---------|---------|----------------|----------------|--------|
| Workflow Builder | YES | LIMITED (trigger via webhook) | Configure | **NEEDS VERIFICATION** |
| Trigger Types | YES | N/A | Configure | **NEEDS VERIFICATION** |
| Action Types | YES | N/A | Configure | **NEEDS VERIFICATION** |
| Conditional Logic | YES | N/A | Configure | **NEEDS VERIFICATION** |
| Wait Actions | YES | N/A | Configure | **NEEDS VERIFICATION** |
| Webhook Actions | YES | N/A | Configure | **NEEDS VERIFICATION** |
| Custom Actions | LIMITED | N/A | May need integration | **NEEDS VERIFICATION** |

### 1.4 Snapshots

| Feature | Native? | API Available? | NeuronX Action | Status |
|---------|---------|----------------|----------------|--------|
| Snapshot Export | YES | **NO** (UI only) | Manual or browser automation | **CRITICAL - VERIFY** |
| Snapshot Import | YES | **NO** (UI only) | Manual or browser automation | **CRITICAL - VERIFY** |
| Snapshot Versioning | **NO** | **NO** | Build (external version control) | **CRITICAL - VERIFY** |
| Programmatic Deploy | **NO** | **NO** | Build (NOT AVAILABLE natively) | **CRITICAL - VERIFY** |

### 1.5 Webhooks

| Feature | Native? | API Available? | NeuronX Action | Status |
|---------|---------|----------------|----------------|--------|
| Incoming Webhooks | YES | YES | Configure | **NEEDS VERIFICATION** |
| Outgoing Webhooks | YES | YES (workflow action) | Configure | **NEEDS VERIFICATION** |
| Webhook Signatures | LIMITED | LIMITED | May need build | **NEEDS VERIFICATION** |
| Event Types | LIMITED | LIMITED | Document gaps, may need polling | **NEEDS VERIFICATION** |

### 1.6 Voice/Calling

| Feature | Native? | API Available? | NeuronX Action | Status |
|---------|---------|----------------|----------------|--------|
| Call Tracking | YES | YES | Configure | **NEEDS VERIFICATION** |
| Call Recording | YES | LIMITED | Configure | **NEEDS VERIFICATION** |
| IVR/Phone Trees | YES | NO | Configure | **NEEDS VERIFICATION** |
| Call Forwarding | YES | LIMITED | Configure | **NEEDS VERIFICATION** |
| Voice AI Integration | **NO** | **NO** | Build (NeuronX core feature) | **NEEDS VERIFICATION** |

---

## 2. Integration Required (Adapter Work)

### 2.1 Contact Sync (Bidirectional)

| Component | Build Required | Complexity | Risk Tier | Dependencies |
|-----------|----------------|------------|-----------|--------------|
| GHL → NeuronX | YES (webhook) | LOW | T3 | GHL webhook events |
| NeuronX → GHL | YES (API) | LOW | T3 | GHL API credentials |
| Conflict Resolution | YES | MEDIUM | T2 | Sync strategy decision |
| Field Mapping | YES | LOW | T3 | Schema definition |

**Implementation Notes**:
- Use GHL webhooks for real-time sync from GHL
- Use GHL API for pushing changes to GHL
- Need to handle: create, update, delete, merge conflicts
- Custom field mapping required

### 2.2 Opportunity Sync

| Component | Build Required | Complexity | Risk Tier | Dependencies |
|-----------|----------------|------------|-----------|--------------|
| Pipeline Sync | YES | MEDIUM | T3 | Pipeline mapping |
| Stage Transitions | YES | MEDIUM | T3 | Workflow integration |
| Opportunity Values | YES | LOW | T3 | Field mapping |

### 2.3 Webhook Processing

| Component | Build Required | Complexity | Risk Tier | Dependencies |
|-----------|----------------|------------|-----------|--------------|
| Webhook Receiver | YES | LOW | T3 | Infrastructure |
| Event Parsing | YES | MEDIUM | T3 | GHL event schema |
| Event Validation | YES | MEDIUM | T3 | Signature verification |
| Retry Logic | YES | MEDIUM | T3 | Queue infrastructure |

---

## 3. Code Required (Custom Development)

### 3.1 Snapshot Governance

**Why**: GHL does not support programmatic snapshot deployment or versioning.

**Components to Build**:
| Component | Complexity | Risk Tier | Notes |
|-----------|------------|-----------|-------|
| Snapshot Export Automation | HIGH | T2 | May require browser automation |
| Snapshot Version Control | MEDIUM | T3 | External Git-based system |
| Drift Detection | HIGH | T2 | Compare expected vs. actual |
| Programmatic Deployment | HIGH | T2 | If possible at all |

**Risk Assessment**: This is a significant gap. GHL does not expose snapshot APIs.

**Options**:
1. Browser automation (Puppeteer/Playwright) — fragile
2. Manual export/import with version control — process-heavy
3. Partner with GHL for API access — dependency

### 3.2 Voice Orchestration

**Why**: GHL has basic calling but no AI voice integration.

**Components to Build**:
| Component | Complexity | Risk Tier | Notes |
|-----------|------------|-----------|-------|
| Call Routing | HIGH | T2 | Integrate with voice provider |
| Context Injection | HIGH | T2 | Push CRM data to voice AI |
| Post-Call Analysis | MEDIUM | T3 | Receive call results |
| CRM Update | LOW | T3 | Write results to GHL |

**Architecture**:
```
NeuronX Voice Layer
    ↓ (call initiation)
Voice Provider (Twilio, Vapi, etc.)
    ↓ (call events)
NeuronX Orchestrator
    ↓ (context/results)
GHL CRM (via API)
```

### 3.3 Multi-Tenant Workspace Isolation

**Why**: GHL Super Agency supports sub-accounts but isolation is limited.

**Components to Build**:
| Component | Complexity | Risk Tier | Notes |
|-----------|------------|-----------|-------|
| Workspace Isolation Layer | HIGH | T2 | Tenant boundaries |
| API Key Management | MEDIUM | T2 | Per-tenant credentials |
| Rate Limiting | MEDIUM | T3 | Per-tenant limits |
| Audit Logging | MEDIUM | T3 | Per-tenant activity |

### 3.4 Playbook Engine

**Why**: GHL workflows are limited to predefined triggers and actions.

**Components to Build**:
| Component | Complexity | Risk Tier | Notes |
|-----------|------------|-----------|-------|
| Playbook Definition | HIGH | T2 | DSL or YAML schema |
| Playbook Execution | HIGH | T2 | State machine engine |
| GHL Action Adapter | MEDIUM | T3 | Map playbook actions to GHL API |
| Rollback Logic | HIGH | T2 | Undo capability |
| Version Control | MEDIUM | T3 | Playbook versioning |

---

## 4. Risks to Document

### 4.1 API Limitations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Rate Limits | HIGH | HIGH | Queue + exponential backoff |
| API Changes | MEDIUM | MEDIUM | Version pinning, adapter abstraction |
| Missing Events | HIGH | HIGH | Polling fallback for critical data |
| Pagination Limits | MEDIUM | LOW | Cursor-based pagination |
| Auth Expiry | MEDIUM | MEDIUM | Token refresh automation |

### 4.2 Snapshot Governance Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| No programmatic deploy | HIGH | CONFIRMED | Browser automation OR manual process |
| No versioning | HIGH | CONFIRMED | External version control |
| Drift undetectable | HIGH | HIGH | Periodic export + diff |
| Breaking changes | HIGH | MEDIUM | Snapshot testing before deploy |

### 4.3 Multi-Tenant Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Cross-tenant data leak | CRITICAL | LOW | Strict isolation layer, auditing |
| Sub-account API limits | HIGH | MEDIUM | Careful rate limiting |
| Billing complexity | MEDIUM | MEDIUM | Usage tracking per tenant |
| Credential exposure | CRITICAL | LOW | Secrets management, rotation |

### 4.4 Voice Integration Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Voice provider dependency | HIGH | MEDIUM | Abstraction layer |
| Call quality issues | MEDIUM | MEDIUM | Provider SLA monitoring |
| Compliance (recording) | HIGH | LOW | Consent management |
| Cost overruns | MEDIUM | MEDIUM | Usage caps, alerting |

---

## 5. Research Checklist (Browser Verification Required)

**Instructions**: These items require manual browser access to GHL Super Agency Pro dashboard to verify.

### Account & API

- [ ] Verify API key generation process
- [ ] Confirm rate limit values (requests per minute)
- [ ] Check OAuth flow for agency apps
- [ ] Verify webhook secret configuration
- [ ] Confirm sub-account API access patterns
- [ ] Check API versioning strategy

### Contacts & CRM

- [ ] Confirm custom field limit (50?)
- [ ] Test contact search query capabilities
- [ ] Verify bulk operations (import/export limits)
- [ ] Check contact merge functionality
- [ ] Verify webhook events for contact changes
- [ ] Test custom field types supported

### Pipelines

- [ ] Confirm pipeline automation triggers
- [ ] Test opportunity stage webhooks
- [ ] Verify pipeline-to-workflow connections
- [ ] Check pipeline custom field support
- [ ] Verify opportunity value tracking

### Workflows

- [ ] List all available trigger types
- [ ] List all available action types
- [ ] Test webhook action reliability
- [ ] Check workflow versioning (if any)
- [ ] Verify conditional logic capabilities
- [ ] Test workflow error handling

### Snapshots (CRITICAL)

- [ ] **Confirm no programmatic deploy exists**
- [ ] Document manual export process (steps, time)
- [ ] Document manual import process (steps, time)
- [ ] Check if snapshot includes workflows
- [ ] Check if snapshot includes automations
- [ ] Check if snapshot includes custom fields
- [ ] Check snapshot size limits
- [ ] Test snapshot compatibility across accounts

### Webhooks

- [ ] List all available webhook events
- [ ] Test webhook reliability (delivery rate)
- [ ] Verify retry behavior on failure
- [ ] Check signature verification options
- [ ] Verify webhook payload structure
- [ ] Test webhook latency

### Voice/Calling

- [ ] Check native voice capabilities
- [ ] Verify call tracking API
- [ ] Check recording access methods
- [ ] Verify IVR limitations
- [ ] Test call forwarding configuration

---

## 6. Decision Log

| Date | Decision | Rationale | Risk Tier | Status |
|------|----------|-----------|-----------|--------|
| TBD | Snapshot strategy | Depends on browser verification | T2 | PENDING |
| TBD | Polling fallback | For missing webhook events | T3 | PENDING |
| TBD | Multi-tenant approach | Depends on API limits | T2 | PENDING |
| TBD | Voice provider selection | Compare Twilio, Vapi, etc. | T2 | PENDING |
| TBD | Playbook DSL design | YAML vs. custom language | T2 | PENDING |

---

## 7. Next Steps

### Immediate (Before MVP)

1. [ ] Complete browser verification checklist
2. [ ] Document actual API rate limits
3. [ ] Prototype contact sync adapter
4. [ ] Test webhook reliability

### Short-term (MVP Phase)

1. [ ] Implement GHL OAuth adapter
2. [ ] Build bidirectional contact sync
3. [ ] Create snapshot export automation (if feasible)
4. [ ] Implement basic playbook engine

### Medium-term (Post-MVP)

1. [ ] Voice orchestration integration
2. [ ] Advanced drift detection
3. [ ] Multi-tenant isolation layer
4. [ ] Playbook marketplace foundation

---

**Last Updated**: 2026-02-03
**Browser Verification By**: TBD
**Status**: RESEARCH IN PROGRESS

---

**Document Status**: RESEARCH CHECKLIST
**Risk Tier**: T3 (Documentation)
**Next Review**: After browser verification complete
