# AI Layer Billing & Deployment Model

## Objective
Determine the safest, most scalable commercial model for deploying the AI calling layer to immigration firms, considering implementation friction, support overhead, and profit margins.

---

## Model A: Client Brings Their Own AI Account (BYO)
*The firm creates their own Vapi/Bland account, enters their credit card, and provides NeuronX with the API key.*
- **Implementation Friction**: High. Firm owners don't want to learn new AI platforms or manage multiple bills.
- **Support Overhead**: High. API keys expire, credit cards fail, and NeuronX has to troubleshoot third-party billing.
- **Margin**: Zero on usage.
- **Verdict**: Poor user experience. Defeats the purpose of a "done-for-you" OS.

## Model B: NeuronX Resells AI (Pass-Through Usage)
*NeuronX holds a master Vapi/Bland account. Firm usage is tracked and rebilled (with or without markup) via Stripe Metered Billing.*
- **Implementation Friction**: Medium. Requires setting up Stripe usage meters and explaining variable costs to clients.
- **Support Overhead**: Medium. NeuronX handles top-level billing, but must dispute discrepancies if a client overuses.
- **Margin**: Good (can mark up minutes 2x-3x).
- **Verdict**: Excellent for scaling, but complex to build for the first 10 customers.

## Model C: Hybrid Model (Flat Fee with Fair Use Limit)
*NeuronX holds the master AI account. AI minutes are "baked in" to the premium monthly subscription (e.g., $797/mo includes up to 500 AI calls). Overage is billed separately.*
- **Implementation Friction**: Lowest. Client pays one flat fee, NeuronX provisions everything on the backend.
- **Support Overhead**: Low. NeuronX monitors aggregate usage. 
- **Margin**: Excellent. Most firms will use ~100 calls/month (costing NeuronX ~$10-15/mo in API fees), leaving massive margin on a $797 subscription.
- **Verdict**: Best for early go-to-market.

---

## Deployment Recommendation

### For First 10 Customers (Validation Phase)
**Use Model C (Flat Fee / Baked-In)**
- Do not build complex metered billing infrastructure yet.
- Charge a premium SaaS fee (e.g., $497 - $797/mo).
- NeuronX pays the Vapi/Bland API costs out of pocket. 
- Set a "Fair Use" policy in the contract (e.g., max 300 minutes/month).
- **Why**: Zero onboarding friction for the customer. Extremely fast to deploy (just point the GHL webhook to the master AI account, appending the `location_id` for tracking).

### For Customers 11–50 (Growth Phase)
**Transition to Model B (Stripe Metered Re-billing)**
- As volume increases, aggregate API costs become a risk.
- Integrate Stripe Metered Billing. 
- The base subscription (e.g., $497/mo) covers the OS, and AI minutes are billed as a line item at $0.15/minute.
- **Why**: Protects NeuronX margins from high-volume firms while keeping the software base price attractive.

### For Customers 50+ (Scale Phase)
**Agency White-Label Infrastructure**
- Build a multi-tenant routing layer where NeuronX automatically provisions sub-accounts in the AI provider's API, isolating billing limits and audio logs per client automatically.