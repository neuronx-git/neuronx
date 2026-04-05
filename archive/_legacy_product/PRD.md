# Product Requirements Document: NeuronX

**Version**: 2.0 (Canonical)  
**Status**: CANONICAL  
**Owner**: Product Agent → Antigravity (CTO)  
**Ratified By**: Founder  
**Last Updated**: 2026-01-29

**References**:
- [Product Vision Canon](file:///Users/ranjansingh/Desktop/NeuronX/PRODUCT/VISION_CANON.md)
- [ICP & Personas](file:///Users/ranjansingh/Desktop/NeuronX/PRODUCT/ICP_AND_PERSONAS.md)
- [System Architecture](file:///Users/ranjansingh/Desktop/NeuronX/PRODUCT/SYSTEM_ARCHITECTURE.md)

---

## 1. Product Overview

NeuronX is an **Autonomous Business Orchestration Platform** that enables businesses to automate complex workflows by integrating CRM systems (GoHighLevel), AI voice agents, and deterministic playbook engines.

### Core Value Proposition

> "Deploy client infrastructure in 1 hour, not 3 days. Run your agency like a SaaS product."

**For**: GHL agency owners and operations managers  
**Who**: Need to scale client fulfillment without linear headcount growth  
**NeuronX**: Provides deterministic playbook orchestration with governance, reusability, and drift detection  
**Unlike**: Zapier, GHL native workflows, or custom development  
**NeuronX**: Offers version-controlled business logic that works across CRM, voice AI, and external systems

---

## 2. User Journeys

### Journey 1: Deploy New Client (Alex - Agency Owner)

**Current State** (Without NeuronX):
1. Receive new client contract
2. Manually configure GHL workspace (2-3 hours)
3. Import contacts and set up pipelines (2-4 hours)
4. Configure workflows and automation (4-8 hours)
5. Set up voice AI integration (if applicable) (4-6 hours)
6. Test everything manually (2-3 hours)
7. **Total**: 2-5 days of ops team time

**Future State** (With NeuronX):
1. Select "New Client" in NeuronX dashboard
2. Choose playbook template (e.g., "Home Services Agency")
3. Fill in client parameters (name, industry, phone number)
4. Deploy snapshot to GHL via NeuronX adapter
5. Verify deployment (automated checks run)
6. **Total**: \<1 hour, mostly automated

**Success Criteria**:
- ✅ 90% reduction in deployment time
- ✅ Zero configuration errors
- ✅ Repeatable process (any ops person can do it)

---

### Journey 2: Build Reusable Playbook (Jordan - Operations Manager)

**Current State**:
1. Client requests custom workflow
2. Build in GHL for one client
3. Manually copy-paste to other clients
4. Configurations drift over time
5. No version control or rollback
6. No testing before production

**Future State** (With NeuronX):
1. Design playbook logic in NeuronX UI
2. Define governance rules (e.g., "must update CRM within 5 min")
3. Test playbook in staging environment
4. Version and commit playbook
5. Deploy to subset of clients (beta test)
6. Roll out to all applicable clients with one click
7. Monitor execution, rollback if needed

**Success Criteria**:
- ✅ Playbooks reused 10+ times
- ✅ Zero production incidents from untested changes
- ✅ Rollback capability within 5 minutes

---

### Journey 3: Natural Voice Interaction (Maria - End User)

**Current State**:
1. Customer calls business
2. Voice AI answers but has no CRM context
3. Customer repeats information already in system
4. Appointment booked, but manual CRM update needed
5. No follow-up unless human remembers

**Future State** (With NeuronX):
1. Customer calls business
2. NeuronX routes call to voice AI with CRM context loaded
3. AI knows customer history ("Hi Maria, calling about your furnace inquiry?")
4. Books appointment, updates GHL opportunity automatically
5. Playbook triggers SMS confirmation + calendar invite
6. Post-call analysis logged for quality improvement

**Success Criteria**:
- ✅ \<2 minute call duration (vs 5+ minutes)
- ✅ Zero repeated information
- ✅ 95%+ CRM update accuracy
- ✅ Customer satisfaction: "felt natural, not robotic"

---

## 3. Functional Requirements

### 3.1 GoHighLevel (GHL) Integration (`adapters-ghl`)

#### FR-GHL-1: Bidirectional Contact Sync
- **Requirement**: Real-time sync of contacts between GHL and NeuronX
- **Acceptance Criteria**:
  - Contact created in GHL → appears in NeuronX within 30 seconds
  - Contact updated in playbook → GHL reflects changes within 30 seconds
  - Conflict resolution: Last-write-wins with audit log
- **Priority**: P0 (Critical)

#### FR-GHL-2: Opportunity Management
- **Requirement**: Playbooks can create and update GHL opportunities
- **Acceptance Criteria**:
  - Playbook action "Create Opportunity" succeeds 99.9% of time
  - Custom fields preserved during sync
  - Pipeline stage transitions trigger playbook events
- **Priority**: P0 (Critical)

#### FR-GHL-3: Snapshot Deployment
- **Requirement**: Deploy GHL snapshots programmatically via NeuronX
- **Acceptance Criteria**:
  - Snapshot deployed to new workspace in \<5 minutes
  - Parameterization (replace {{client_name}}, {{phone}}, etc.)
  - Deployment validation report (what succeeded/failed)
- **Priority**: P0 (Critical)

#### FR-GHL-4: Drift Detection
- **Requirement**: Detect when live GHL config diverges from intended snapshot
- **Acceptance Criteria**:
  - Daily drift scan for all managed workspaces
  - Alert if \>10% of workflows differ from source
  - One-click drift correction
- **Priority**: P1 (High)

#### FR-GHL-5: Sub-Account Management
- **Requirement**: Programmatically create and manage GHL sub-accounts (locations)
- **Acceptance Criteria**:
  - Create sub-account via API with customer details
  - Configure sub-account settings (name, timezone, etc.)
  - Deploy snapshot to sub-account automatically
  - Map NeuronX customer to GHL sub-account
- **Priority**: P0 (Critical)
- **Rationale**: Use GHL's native multi-tenancy instead of building custom

#### FR-GHL-6: White-Label Configuration
- **Requirement**: Configure GHL white-label branding for NeuronX
- **Acceptance Criteria**:
  - Custom domain (app.neuronx.ai) configured
  - Logo and brand colors applied
  - White-label mobile app configured
  - No GHL branding visible to end customers
- **Priority**: P0 (Critical)
- **Rationale**: Leverage GHL's white-label capabilities

#### FR-GHL-7: SaaS Mode Pricing
- **Requirement**: Configure custom pricing per client using GHL SaaS mode
- **Acceptance Criteria**:
  - Set monthly fee per sub-account (e.g., $299, $499, $799)
  - Configure usage-based pricing (SMS, email, phone)
  - Add markup to GHL costs (e.g., $0.02 per SMS)
  - Automated billing via GHL + Stripe
- **Priority**: P0 (Critical)
- **Rationale**: Use GHL's rebilling instead of custom billing

#### FR-GHL-8: Landing Page Builder Integration
- **Requirement**: Use GHL's native page builder for customer landing pages
- **Acceptance Criteria**:
  - Customers can create landing pages via GHL UI
  - Page submissions trigger playbook execution
  - Page analytics integrated with playbook intelligence
  - Form data synced to playbook context
- **Priority**: P1 (High)
- **Rationale**: Leverage GHL's existing page builder (free capability)

#### FR-GHL-9: Form & Survey Integration
- **Requirement**: Use GHL's native form builder for data collection
- **Acceptance Criteria**:
  - Forms trigger playbook execution
  - Form data synced to playbook context
  - Multi-step forms supported
  - Conditional logic in forms
- **Priority**: P1 (High)
- **Rationale**: Leverage GHL's existing form builder (free capability)

#### FR-GHL-10: Calendar & Appointment Integration
- **Requirement**: Use GHL's native calendar for appointment scheduling
- **Acceptance Criteria**:
  - Appointments trigger playbook stages
  - Calendar availability synced with voice AI
  - Automated reminders via playbook
  - Booking confirmation triggers playbook action
- **Priority**: P2 (Medium)
- **Rationale**: Leverage GHL's existing calendar (free capability)

---

### 3.2 Playbook Engine (`playbook-engine`)

#### FR-PB-1: Deterministic Execution
- **Requirement**: Playbooks execute exactly as defined, every time
- **Acceptance Criteria**:
  - Same inputs → same outputs (no non-deterministic behavior)
  - Execution logs capture every decision point
  - Rollback to any previous execution state
- **Priority**: P0 (Critical)

#### FR-PB-2: Governance Enforcement
- **Requirement**: Business rules enforced automatically
- **Acceptance Criteria**:
  - Rules defined in YAML/JSON format
  - Violations block execution (cannot override)
  - Audit trail of all rule evaluations
- **Priority**: P1 (High)

#### FR-PB-3: Intelligence Layer
- **Requirement**: AI-enhanced decision making within playbooks
- **Acceptance Criteria**:
  - Pattern recognition (e.g., "high-intent lead" classification)
  - Predictive next actions
  - Explainable AI (why was this decision made?)
- **Priority**: P2 (Medium)

#### FR-PB-4: Version Control
- **Requirement**: Playbooks are versioned like code
- **Acceptance Criteria**:
  - Git-like version history
  - Rollback to previous version
  - Diff between versions
- **Priority**: P1 (High)

---

### 3.3 Voice Orchestration (`voice-orchestration`)

#### FR-VO-1: Call Routing
- **Requirement**: Route inbound/outbound calls to appropriate voice AI provider
- **Acceptance Criteria**:
  - Support multiple providers (Bland, Vapi, ElevenLabs)
  - Routing rules based on caller ID, time of day, playbook logic
  - Failover if primary provider unavailable
- **Priority**: P0 (Critical)

#### FR-VO-2: Context Injection
- **Requirement**: Load CRM context before AI conversation starts
- **Acceptance Criteria**:
  - Retrieve contact from GHL by phone number
  - Inject custom fields into AI prompt
  - Context available within 500ms of call initiation
- **Priority**: P0 (Critical)

#### FR-VO-3: Post-Call Analysis
- **Requirement**: Analyze call transcripts for insights
- **Acceptance Criteria**:
  - Sentiment analysis (positive/negative/neutral)
  - Intent classification (appointment booked, callback requested, etc.)
  - Action items extracted automatically
- **Priority**: P2 (Medium)

---

### 3.4 Platform Services

#### FR-PS-1: Multi-Tenancy (DEPRECATED - Use GHL Sub-Accounts)
- **Status**: ❌ DEPRECATED
- **Rationale**: Use GHL's native sub-account system instead of building custom multi-tenancy
- **Migration**: Each NeuronX customer = 1 GHL sub-account (location)
- **See**: FR-GHL-5 (Sub-Account Management)

#### FR-PS-2: Billing & Entitlements (`billing-entitlements`)
- **Requirement**: Track usage and enforce subscription limits
- **Acceptance Criteria**:
  - Usage metering (playbook executions, API calls)
  - Subscription tiers (Starter, Growth, Enterprise)
  - Soft limits (warn) and hard limits (block)
- **Priority**: P1 (High)

#### FR-PS-3: AI Gateway (`ollama-gateway`)
- **Requirement**: Centralized AI inference with rate limiting
- **Acceptance Criteria**:
  - Support multiple AI models (GPT-4, Claude, local Ollama)
  - Rate limiting per workspace
  - Cost tracking per AI call
- **Priority**: P2 (Medium)

---

## 4. Quality Bars

### 4.1 Reliability

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Uptime** | 99.9% | GHL webhook processing |
| **Error Rate** | \<0.1% | Playbook execution failures |
| **Data Loss** | 0% | CRM sync accuracy |
| **Recovery Time** | \<5 min | System restart time |

### 4.2 Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| **GHL Sync Latency** | \<30s | Contact update propagation |
| **Voice Context Load** | \<500ms | CRM data retrieval for call |
| **Playbook Execution** | \<2s | Average execution time |
| **Snapshot Deployment** | \<5 min | Full GHL workspace setup |

### 4.3 Security

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Data Encryption** | AES-256 | At rest and in transit |
| **Authentication** | OAuth 2.0 + MFA | User login |
| **Audit Logs** | 100% coverage | All writes to CRM/DB |
| **Secret Management** | Zero hardcoded secrets | Vault-based storage |

### 4.4 User Experience

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Time to First Value** | \<1 hour | New user → first playbook deployed |
| **Setup Complexity** | \<10 clicks | Deploy standard client |
| **Error Messages** | Actionable | "What to do next" always provided |

### 4.5 Test Coverage

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Unit Test Coverage** | ≥90% | Lines, functions, branches, statements |
| **Integration Test Coverage** | ≥80% | Critical user journeys |
| **E2E Test Coverage** | ≥70% | Happy paths + error scenarios |
| **Coverage Enforcement** | CI blocks PRs | Fail if coverage drops below target |

---

## 5. Compliance & Security Requirements

### 5.1 Data Handling

- **PII Protection**: Customer contact data encrypted at rest (AES-256)
- **Data Residency**: Default US region, EU option for GDPR
- **Data Retention**: 90-day playbook execution logs, configurable
- **Right to Deletion**: GDPR-compliant data deletion within 30 days

### 5.2 Authentication & Authorization

- **User Auth**: OAuth 2.0 (Google, Microsoft) + password
- **API Auth**: API keys with workspace-level scoping
- **MFA**: Required for admin roles
- **RBAC**: Admin, Operator, Viewer roles per workspace

### 5.3 Audit & Compliance

- **Audit Logs**: All CRM writes, playbook executions, config changes
- **Immutability**: Append-only (cannot be modified once written)
- **Retention**: Audit logs retained 7 years (SOC 2/compliance); execution logs 90 days (configurable)
- **Deletion**: GDPR right-to-deletion applies to PII fields only (cryptographic tombstone, not physical deletion of audit trail)
- **Compliance Reports**: SOC 2 readiness (Year 2 target)
- **Webhook Security**: HMAC signature verification for GHL webhooks

---

## 6. Non-Goals

What NeuronX explicitly **will not** do in MVP (Year 1):

❌ **Not a CRM**: We orchestrate GHL, we don't replace it  
❌ **Not a Voice Provider**: We route to Bland/Vapi/etc., we don't provide TTS/STT  
❌ **Not Multi-CRM** (Year 1): GHL-only until proven, then expand to HubSpot/Salesforce  
❌ **Not On-Premise**: Cloud-only for Year 1  
❌ **Not Open Source**: Core IP is proprietary  
❌ **Not a Marketplace** (Year 1): Playbook templates are curated, not user-submitted  
❌ **Not SOC 2 Certified** (Year 1): Targeting Year 2  

---

## 7. Success Metrics

### Product-Market Fit Indicators

| Metric | Target (Year 1) | Measurement |
|--------|-----------------|-------------|
| **Time to Deploy Client** | \<1 hour (vs 3 days) | User survey |
| **Playbook Reuse** | 5x per playbook | System analytics |
| **Voice+CRM Workflows** | 80% uptime | Error rate monitoring |
| **Drift Detection** | 95% catch rate | Alert accuracy |
| **Customer Satisfaction** | "Essential" rating | NPS 50+ |

### Business Metrics

| Metric | Year 1 | Year 3 |
|--------|--------|--------|
| **Customers** | 100 agencies | 1,000+ |
| **ARR** | $500K | $10M+ |
| **NRR** | 110% | 130% |
| **CAC Payback** | \<6 months | \<3 months |
| **Gross Margin** | 70% | 85% |

---

## 8. Roadmap Alignment

This PRD supports the following roadmap phases (see [ROADMAP.md](file:///Users/ranjansingh/Desktop/NeuronX/PRODUCT/ROADMAP.md)):

- **MVP (Q1-Q2 2026)**: GHL integration + basic playbook engine
- **V1 (Q3 2026)**: Voice orchestration + drift detection
- **V2 (Q4 2026)**: Curated playbook library + intelligence layer
- **Enterprise (2027)**: White-label + SOC 2 certification
- **Multi-CRM (2028+)**: HubSpot, Salesforce adapters

---

## 9. Dependencies & Constraints

### Technical Dependencies

- **GHL API Stability**: Reliant on GoHighLevel API uptime and versioning
- **Voice Provider APIs**: Bland/Vapi availability and latency
- **Ollama Gateway**: AI inference for intelligence layer

### Business Constraints

- **Pricing Pressure**: Must stay \<$500/month for agency ICP
- **Support Capacity**: Limited customer success resources (Year 1)
- **Compliance Timeline**: SOC 2 requires 6-12 months prep

### Known Risks

- 🚨 **GHL API Changes**: Breaking changes could disrupt service
- 🚨 **Voice Provider Lock-In**: Over-reliance on single provider
- ⚠️ **Playbook Complexity**: Balance power vs ease-of-use
- ⚠️ **Market Education**: "Orchestration" is new concept for agencies

---

## 10. Open Questions

Questions requiring founder/stakeholder input:

1. **Pricing Model**: Per-workspace or per-execution? Freemium tier?
2. **Voice Provider Strategy**: Build own TTS/STT or always use third-party?
3. **Multi-CRM Priority**: When to expand beyond GHL? (2028+ vs later; gated by PMF/ARR)
4. **Enterprise vs SMB Focus**: Double down on agencies or chase enterprise?
5. **Playbook IP**: Are templates proprietary or community-contributed?

---

## Governance

**Document Authority**: CANONICAL

**Modification Process**:
1. Product changes require alignment with [Vision Canon](file:///Users/ranjansingh/Desktop/NeuronX/PRODUCT/VISION_CANON.md)
2. Functional requirement changes require Trae review
3. Founder approval for priority changes (P0/P1/P2)
4. Version increment for major changes

**Version History**:
- v2.0 (2026-01-29): Canonical PRD with comprehensive requirements
- v1.0 (previous): Basic architectural overview (rehydrated)

---

**Status**: CANONICAL  
**Next Review**: 2026-04-29 (quarterly, aligned with Vision Canon)
