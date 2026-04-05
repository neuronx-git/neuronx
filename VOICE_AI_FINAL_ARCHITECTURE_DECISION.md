# Voice AI Final Architecture Decision

## The Challenge Context
NeuronX requires an AI layer that can triage inbound immigration leads in under 5 minutes, extract structured qualification data (Program, Urgency, Complexity), and route the lead in GoHighLevel—all without *ever* giving legal advice.

We compared **Option A (Vapi)** against **Option B (ElevenLabs Conversational AI + Twilio + Make.com)**.

---

## Final Recommendation: Option A (Vapi)

While ElevenLabs represents the absolute bleeding edge of raw vocal quality, **Vapi is the undeniably superior architectural choice** for a B2B SaaS operating in a highly regulated industry (immigration).

### Why Vapi Wins for NeuronX:

**1. Lowest Engineering Effort (Speed to Market)**
Vapi abstracts telephony (Twilio) and LLM orchestration into a single platform. Building Option B requires stringing together GHL -> Make -> Twilio -> ElevenLabs -> Make -> GHL. Vapi reduces this to GHL -> Vapi -> Make -> GHL.

**2. Strict Guardrail Enforcement (UPL Compliance)**
Immigration consultants risk losing their license if their staff (or AI) gives incorrect legal advice (Unauthorized Practice of Law). Vapi's architecture is explicitly built around "State Machines" and "Function Calling." We can force the AI to execute the `escalate_to_human` function the millisecond a user says the word "Deportation." ElevenLabs Conversational AI is slightly more "free-flowing," which is great for customer service, but dangerous for legal intake.

**3. Structured Data Extraction**
NeuronX's core value is moving pipeline stages based on AI data (`ai_program_interest`, `ai_urgency`). Vapi natively outputs a clean JSON object at the end of the call based on our defined schema. Option B requires passing the raw transcript back to an LLM via Make.com to extract this data, adding latency, cost, and a point of failure.

**4. Scalable Billing (The Master Account Model)**
Vapi allows NeuronX to programmatically create Sub-Accounts with hard spend limits. This allows NeuronX to offer a "Done-For-You" flat-fee subscription to the first 10-50 customers without risking massive credit card overages if a client gets bot-spammed. Option B requires complex custom billing logic to track Twilio and ElevenLabs usage separately.

---

## Phased Rollout Plan

### For the First 10 Customers (Validation)
- **Architecture**: Vapi (Master Account) -> Make.com (Data Parsing) -> GHL (System of Record).
- **Billing**: Flat SaaS fee (e.g., $797/mo). NeuronX pays the Vapi bill out of pocket. Cap usage at 300 minutes/month via Vapi dashboard limits.
- **Goal**: Prove the AI increases lead-to-consultation conversion rates without requiring any engineering from the founder.

### For the First 50 Customers (Growth)
- **Architecture**: Same as above.
- **Billing**: Transition to Stripe Metered Billing. NeuronX tracks the Vapi webhooks and bills the client $0.15/minute for usage over their base limit.

### Long-Term Scaling (100+ Customers)
- **Architecture**: Build a custom webhook receiver (e.g., Node.js on AWS/Vercel) to replace Make.com. This reduces Make.com operation costs and allows for more complex, multi-tenant database logging outside of GHL if required. 

**Decision**: Proceed with the **Vapi** architecture as originally designed. It perfectly aligns with the "Configuration First, Minimal Engineering" core principle.