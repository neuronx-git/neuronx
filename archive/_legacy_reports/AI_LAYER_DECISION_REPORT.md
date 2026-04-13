# AI Layer Decision Report

## Executive Summary
This report evaluates the optimal path for implementing the NeuronX AI calling layer. The objective is to achieve a sub-5-minute speed-to-lead voice response that qualifies prospects without giving legal advice, while minimizing custom engineering and preserving GoHighLevel (GHL) as the system of record.

## Platform Comparison

### 1. GHL Native Voice AI
- **Speed to Implement**: 10/10 (Native)
- **Engineering Effort**: Zero
- **Reliability**: 7/10 (Beta/evolving)
- **Configurability**: 4/10 (Limited branching and strict compliance guardrails)
- **Billing Complexity**: 10/10 (Seamless SaaS rebilling)
- **Tenant Deployment**: 10/10 (Included in snapshot)
- **Compliance Suitability**: 3/10 (High risk of hallucination; hard to prevent it from giving immigration advice)
- **Verdict**: Insufficient for highly regulated immigration triage.

### 2. Vapi
- **Speed to Implement**: 8/10
- **Engineering Effort**: Low (Webhook/Make.com integration)
- **Reliability**: 9/10
- **Configurability**: 10/10 (Excellent system prompting, function calling, and conversation flow control)
- **Billing Complexity**: 6/10 (Requires API key management per tenant or usage tracking)
- **Tenant Deployment**: 7/10 (Requires external account setup)
- **Compliance Suitability**: 9/10 (Strict guardrails and human-handoff functions work reliably)
- **Verdict**: Strong contender due to advanced conversational control and low latency.

### 3. Bland AI
- **Speed to Implement**: 9/10 (Has native/easy GHL integration apps)
- **Engineering Effort**: Low (Pre-built GHL webhooks)
- **Reliability**: 8/10
- **Configurability**: 8/10 (Conversational pathways are easy to build)
- **Billing Complexity**: 7/10 (Agency models available)
- **Tenant Deployment**: 8/10 (Easier GHL connection)
- **Compliance Suitability**: 8/10 (Good guardrails)
- **Verdict**: Strong contender, specifically optimized for sales/booking.

### 4. Retell AI
- **Speed to Implement**: 7/10
- **Engineering Effort**: Medium (Requires custom webhook server or Make.com)
- **Reliability**: 9/10
- **Configurability**: 9/10 (Excellent voice realism and latency)
- **Billing Complexity**: 6/10
- **Tenant Deployment**: 6/10 (Manual setup)
- **Compliance Suitability**: 9/10
- **Verdict**: Best voice quality, but slightly more integration friction than Vapi/Bland.

### 5. Custom Engineering (Twilio + OpenAI Realtime API)
- **Speed to Implement**: 2/10
- **Engineering Effort**: High (Requires full voice server, websocket management, state handling)
- **Reliability**: 8/10 (Depends on infrastructure)
- **Configurability**: 10/10
- **Verdict**: Discard. Violates the "lowest-engineering" principle.

## Final Recommendation

**Implement Now: Vapi (or Bland AI as backup) via Thin Webhook Integration**
- **Why**: Immigration requires absolute strictness to avoid giving legal advice (UPL - Unauthorized Practice of Law). Vapi allows for precise system prompts, strict guardrails, and structured data extraction (function calling) to push exact fields (Program, Urgency, etc.) back to GHL.
- **Integration**: GHL Workflow -> Webhook to Vapi -> Vapi makes call -> Vapi triggers End-of-Call Webhook -> GHL (updates Custom Fields & Tags). This requires zero custom backend code if routed through a no-code tool like Make.com, or a very thin serverless function.

**Defer: GHL Native Voice AI**
- **Why**: Until GHL native Voice AI supports complex, multi-turn data extraction with strict hallucination guardrails suitable for legal/immigration contexts, it is too risky to deploy as the first touchpoint.

**Safest & Lowest-Engineering Path**: 
Use GHL to trigger the call via a simple outbound Webhook, and use a standard Make.com scenario (or Vapi's native GHL app) to catch the post-call payload and update the GHL Contact record.