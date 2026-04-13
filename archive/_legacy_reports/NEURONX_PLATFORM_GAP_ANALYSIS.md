# NeuronX Platform Gap Analysis

## Overview
This document compares the theoretical capabilities of our chosen platforms (GoHighLevel, Vapi, Make, Skyvern) against the current v1 MVP implementation of NeuronX, identifying gaps where we are leaving value on the table.

## 1. Unused Features (Left on the table)

**GHL Smart Lists & Targeted Broadcasts**
- *Capability*: GHL can dynamically group contacts based on Custom Fields (e.g., all leads with `ai_program_interest` = "Express Entry" AND `ai_lead_score` > 60).
- *Gap*: Currently, we only use linear workflows. We are missing the opportunity to run targeted batch email campaigns when IRCC announces a new Express Entry draw.

**Vapi Inbound Routing**
- *Capability*: Vapi numbers can receive inbound calls, not just make outbound speed-to-lead calls.
- *Gap*: The current setup only triggers an AI call when a form is submitted. If a lead calls the firm's main number directly, they get a traditional human voicemail.
- *Recommendation*: Route the firm's main Twilio/GHL number to the Vapi assistant for after-hours inbound answering.

**Make.com LLM Formatting**
- *Capability*: Make can pass webhook data through OpenAI before sending it to GHL.
- *Gap*: We are currently dumping raw JSON strings into GHL notes. 
- *Recommendation*: Use the Make.com OpenAI module to rewrite the Vapi `summary` into a highly professional, bulleted "Consultant Briefing" document.

## 2. Features that Increase Conversion

**Vapi Dynamic Prompt Injection**
- *Capability*: Vapi allows passing `assistantOverrides` in the outbound webhook.
- *Gap*: We currently only pass `first_name`. 
- *Recommendation*: If the lead filled out a longer form, pass their `country_of_origin` or `specific_question` into the prompt so the AI can say: "Hi John, I saw you were asking about bringing your spouse from Brazil..."

**GHL Conversational AI (SMS)**
- *Capability*: GHL has a native bot for SMS booking.
- *Gap*: We turned this off due to UPL (Unauthorized Practice of Law) fears.
- *Recommendation*: Turn it on in "Suggest" mode. Let the AI draft the SMS reply, but require the human consultant to click "Approve" before sending.

## 3. Features that Improve SaaS Scalability

**Vapi Sub-Accounts (Agency API)**
- *Capability*: Vapi allows the creation of programmatic sub-accounts with hard spend limits.
- *Gap*: Currently, we are using the founder's master Vapi account. If we onboard 10 clients, they all share the same bucket and billing.
- *Recommendation*: Use the Vapi `/org/subaccount` API to provision a dedicated Vapi environment for every new GHL Location.

**Make.com Scenario Cloning API**
- *Capability*: Make.com has an API to duplicate scenarios.
- *Gap*: The Make.com webhook catching the Vapi payload currently has a hardcoded GHL API key.
- *Recommendation*: Productize this. When a new tenant is created, use the Make API to clone the scenario and inject the tenant's specific GHL OAuth token.

## 4. Features that Improve Automation Reliability

**Skyvern Session Manager**
- *Capability*: Skyvern can persist auth state.
- *Gap*: Currently, our scripts (`authenticateVapi.ts`) require manual execution via the CLI when a session expires.
- *Recommendation*: Build a central Node service that pings the SaaS dashboards daily to keep the session cookies alive, reducing the frequency of founder intervention.