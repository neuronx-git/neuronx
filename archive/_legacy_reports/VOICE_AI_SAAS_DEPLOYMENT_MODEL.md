# Voice AI SaaS Deployment Model

## The Challenge
NeuronX is a multi-tenant B2B SaaS. We cannot have 50 immigration firms sharing the same phone number, the same GHL Location, or the same API usage limits.

## The Deployment Architecture

### 1. The Vapi Layer (Master Account + Sub-Accounts)
- NeuronX owns **one** master Vapi account (and pays the Vapi credit card bill).
- When a new tenant signs up, NeuronX uses the Vapi API (`POST /org/subaccount`) to create an isolated workspace for that tenant.
- A new Vapi Assistant and Phone Number are purchased *inside* that sub-account.
- **Why**: This ensures data privacy between firms and allows NeuronX to set hard spending limits (e.g., $50/month) per tenant so a viral video doesn't bankrupt NeuronX.

### 2. The Make.com Layer (Cloned Scenarios)
- NeuronX maintains one "Gold Standard" Make.com scenario that catches the Vapi webhook and pushes to GHL.
- When a new tenant is provisioned, NeuronX duplicates this scenario.
- The duplicated scenario is injected with the specific GHL OAuth token for that tenant's Sub-Account.

### 3. The GoHighLevel Layer (Snapshots)
- NeuronX pushes the "Gold Snapshot" to the new tenant's sub-account.
- A script updates the Webhook URL in `WF-01A` to point to the tenant's newly generated Vapi phone number.

## Billing Model

**The "Baked-In" Model (First 10-50 Customers)**
- **Pricing**: $797/month flat fee.
- **Inclusions**: GHL CRM, Automations, + 200 minutes of AI Calling per month.
- **Cost Control**: Vapi Sub-Account is hard-capped at $30/month (200 mins * $0.15). If the firm hits the limit, the AI stops calling and defaults to the standard GHL SMS workflow until the next billing cycle.
- **Why**: This completely removes the friction of metered billing for early adopters while protecting NeuronX's margins.

**The Metered Model (Scale Phase)**
- **Pricing**: $497/month + $0.25/minute.
- **Mechanics**: NeuronX catches the end-of-call webhooks, aggregates the `call.duration`, and uses the Stripe Metered Billing API to charge the client at the end of the month. NeuronX pockets the $0.10 margin arbitrage.