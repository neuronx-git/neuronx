# Voice AI Billing Architecture

## The Challenge
Voice AI introduces variable per-minute costs (~$0.12 - $0.15/min). Scaling this across dozens of sub-accounts (tenants) without destroying profit margins or creating massive support overhead is the primary architectural challenge.

---

## Model 1: Master Account Model (NeuronX Pays)
*NeuronX holds one master Vapi/ElevenLabs account and one Twilio account. All tenant traffic routes through this single account.*
- **Implementation**: Easiest. Just point the GHL webhooks to the master API key.
- **Client Experience**: Best. "It just works."
- **Risk**: A single client going viral (or suffering a bot attack) could rack up thousands of dollars in API costs on NeuronX's credit card.
- **Mitigation**: Requires building a custom middleware layer to count minutes per `location_id` and sever the connection if a fair-use limit is breached.

## Model 2: Client-Owned Account Model (BYO-Key)
*Each client creates their own Vapi/ElevenLabs and Twilio accounts and pastes their API keys into GoHighLevel Custom Values.*
- **Implementation**: Hard for the client.
- **Client Experience**: Terrible. Requires them to manage 3 different software subscriptions and credit cards just to make the phone ring.
- **Risk**: Lowest financial risk to NeuronX. High churn risk due to setup friction.

## Model 3: Hybrid SaaS Re-Billing (Stripe Metered)
*NeuronX holds the master accounts, but builds a billing engine that tracks usage per `location_id` and automatically bills the client's Stripe card on file.*
- **Implementation**: Hardest for NeuronX. Requires significant custom backend engineering (tracking webhooks, aggregating minutes, pushing to Stripe Metered API).
- **Client Experience**: Good. They pay one vendor (NeuronX) but have variable costs.
- **Risk**: Moderate. If a client's card declines, NeuronX is still on the hook for the API bill.

---

## Architectural Comparison by Platform

### Option A (Vapi) Billing
Vapi supports an "Agency" model. You can programmatically create sub-accounts via API and set hard spending limits per sub-account. 
- **Advantage**: NeuronX can use the Master Account Model safely by utilizing Vapi's native spend limits. No custom middleware required to prevent overages.

### Option B (ElevenLabs + Twilio) Billing
To achieve isolation, NeuronX would have to programmatically provision Twilio Sub-Accounts and manage ElevenLabs concurrency limits.
- **Advantage**: None. This is highly complex and requires significant custom code to track minutes accurately across two separate platforms.

## Conclusion
Vapi's native sub-account and spend-limit API makes it the clear winner for scaling a SaaS product, allowing NeuronX to offer a frictionless "Master Account" experience without taking on unlimited financial risk.