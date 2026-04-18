# NeuronX Telephony Setup — Buy, Connect, and Use Phone Numbers

**Version**: 1.0
**Date**: 2026-04-18
**Owner**: Founder (Ranjan Singh)
**Status**: CANONICAL — go-to-market playbook
**Audience**: Founder + onboarding engineer configuring a new RCIC firm on NeuronX

---

## TL;DR — The Recommendation

**For every new NeuronX customer firm, buy ONE Canadian local 10DLC number inside their GHL sub-account via LC Phone.** Then, if they need AI voice calls, **import that same number into VAPI via BYOC (SIP trunk)** — do NOT buy a separate VAPI-native number per firm. This gives you:

- One number for SMS, one number for AI calls, one number on business cards
- Billing consolidated in GHL (we rebill at +30% margin)
- A2P registration handled once per firm through GHL's flow
- PIPEDA/CASL compliance assured because GHL+Twilio are already compliant
- Portability preserved — if the firm leaves NeuronX, the number goes with them

**Skip**: VAPI-native numbers (no SMS, poor portability), standalone Twilio BYOC (operational overhead not worth the $0.002/min savings), multiple numbers per firm (confuses clients, doubles A2P registration fees).

Full reasoning below.

---

## Section 1: Provider Comparison (April 2026)

### The Four Options

| Option | Provider | SMS | Voice | AI Integration | CA DIDs | Port-out |
|--------|----------|-----|-------|----------------|---------|----------|
| **A. GHL LC Phone** | Twilio via GHL | Yes | Yes | Via BYOC to VAPI | Yes | Yes (to Twilio) |
| **B. Direct Twilio → BYOC GHL** | Twilio | Yes | Yes | Via BYOC to VAPI | Yes | Yes |
| **C. VAPI + Twilio BYOC** | Twilio via VAPI | No | Yes | Native | Yes | Yes |
| **D. VAPI-native number** | Telnyx (under VAPI) | No | Yes | Native | Limited | Painful |

### Cost Breakdown (per firm, per number, per month)

#### Option A — GHL LC Phone (Recommended)

| Item | Cost |
|------|------|
| CA local number rental | ~$1.15/mo |
| Outbound SMS (CA→CA) | $0.0200/segment |
| Inbound SMS | $0.0100/segment |
| Outbound voice (CA local) | $0.0180/min |
| Inbound voice | $0.0085/min |
| GHL markup | ~20% built-in |
| A2P 10DLC brand registration | $44 one-time (standard) or $4 (sole prop) |
| A2P campaign registration | $15 one-time + $1.50–$10/mo |
| US-10% discount | Applied automatically |

**Source**: [LC Phone Pricing Billing Guide](https://help.gohighlevel.com/support/solutions/articles/48001223556-lc-phone-pricing-billing-guide)

#### Option B — Direct Twilio + BYOC into GHL

| Item | Cost |
|------|------|
| CA local number rental | $1.00/mo |
| Outbound SMS CA→CA | $0.0075/segment (at Twilio list) |
| Outbound voice CA | $0.013/min |
| **PLUS** GHL platform pass-through fees | +$0.005/min, +$0.005/SMS |
| A2P fees | Same as Option A |
| Operational overhead | HIGH — two consoles, two bills, two compliance flows |

Saves ~15% per-unit but adds ~2 hrs/month of billing ops per firm. Not worth it below 100 firms.

#### Option C — VAPI + Twilio BYOC (AI calls only, separate number)

| Item | Cost |
|------|------|
| Twilio number rental | $1.00/mo |
| Twilio inbound voice | $0.0085/min |
| VAPI platform fee | $0.05/min |
| LLM (GPT-4o) | ~$0.06–$0.10/min |
| STT (Deepgram nova-2) | $0.01/min |
| TTS (ElevenLabs Turbo) | ~$0.08–$0.12/min |
| **All-in AI call cost** | **$0.25–$0.33/min** |

**Source**: [Vapi AI Pricing 2026](https://www.retellai.com/blog/vapi-ai-review)

#### Option D — VAPI-native number

| Item | Cost |
|------|------|
| Number rental | $2.00/mo (Telnyx markup) |
| Per-minute cost | Same as Option C but +$0.005 |
| No SMS | N/A — blocks use of single-number strategy |
| Portability | Not portable out of VAPI easily |

### Quality / Call Experience

- **GHL LC Phone**: Same quality as Twilio (it IS Twilio). 99.95% uptime. Native CNAM support.
- **Twilio direct**: Identical quality. Full control over edge cases (e.g., SIP REFER).
- **VAPI on Twilio BYOC**: Excellent — sub-second STT latency with Deepgram nova-2.
- **VAPI-native (Telnyx)**: Good but occasional jitter on Canadian trunks; CNAM less reliable.

### Verdict

**Recommend Option A (GHL LC Phone) as primary number per firm. If firm needs AI intake calls, IMPORT that number into VAPI via BYOC (Option C pattern, but re-using the GHL-owned DID).** This means:

- One Canadian DID per firm (e.g., 647-XXX-XXXX)
- Used for: outbound SMS, inbound client calls, outbound RCIC calls via GHL "Click to Call"
- During business hours: routes to GHL (IVR → staff)
- During prospect intake workflow: VAPI initiates outbound calls using the same DID as caller ID (via BYOC SIP trunk back to Twilio)

Sources: [LC Phone vs Twilio 2026](https://www.centripe.ai/lc-phone-vs-twilio), [GHL SMS Pricing 2026](https://autogencrm.com/gohighlevel-sms-pricing/)

---

## Section 2: A2P 10DLC + CASL Compliance

### Short version for RCIC firms

| Scenario | Registration Required? | Cost |
|----------|------------------------|------|
| CA firm messaging CA clients only, number bought **before 2025-03-26** | No | $0 |
| CA firm messaging CA clients only, number bought **after 2025-03-26** | Yes (A2P Canadian brand) | $44 + $15 + $1.50–$10/mo |
| CA firm messaging **US recipients** (any number age) | Yes (US A2P 10DLC) | Same as above |
| Sole proprietor RCIC (Canadian BN-9) | Yes, sole-prop tier | $4 + $15 + $1.50–$10/mo |

**Source**: [Updated Messaging Policies for Canadian 10DLC](https://help.gohighlevel.com/support/solutions/articles/155000004915-updated-messaging-policies-for-canadian-10dlc-numbers-a2p-registration-requirements)

### Canadian carrier filtering reality

Bell, Rogers, and Telus aggressively block unregistered A2P traffic in 2026. Unregistered numbers see **sub-70% delivery rates** to those carriers. A2P-registered numbers see **>95% delivery**.

**Rule**: every NeuronX firm gets A2P-registered during onboarding, even if all their clients are Canadian. No exceptions.

### CASL (Canada Anti-Spam Law)

Every commercial SMS must include:

1. **Identification**: RCIC firm name + contact info
2. **Consent**: Express (form checkbox) or implied (existing business relationship within 24 months)
3. **Unsubscribe**: "Reply STOP to opt out" in every broadcast message

**Fines**: up to $10M per violation. Track consent timestamps in GHL custom fields (`nx:consent_sms_timestamp`).

Sources: [CASL Compliance Guide 2026](https://www.telair.net/resources/knowledge-base/guides/casl-sms-compliance/), [SMS Messaging Regulation in Canada 2025](https://talk-q.com/sms-messaging-regulation-in-canada)

### What 500 SMS/month looks like at the firm level

- 500 outbound @ $0.02 = $10/mo
- A2P amortized: $44/12 + $15/12 + $5/mo = $10/mo
- **Total SMS cost per firm ≈ $20/mo**

We charge the firm **$50/mo "Communications bundle"** → $30 gross margin per firm on SMS alone.

---

## Section 3: Number Procurement Workflow (New Customer Onboarding)

**Total time**: 45 minutes (26 min active, 19 min waiting on A2P). Can complete in one onboarding session with the firm.

### Step 1 — Confirm the recommendation

Tell the firm: "We recommend one Canadian local number in your area code. It handles SMS, inbound calls, outbound calls from your staff, and (if you opt in) AI intake calls. $50/mo all-in."

### Step 2 — Buy the number in GHL sub-account

**URL**: `https://app.gohighlevel.com/v2/location/{SUB_ACCOUNT_ID}/settings/phone_number`

1. Log in as Agency owner → Switch to sub-account
2. Settings → Phone Numbers → **Add Number**
3. Country: **Canada**
4. Type: **Local**
5. Area code: Enter firm's city code (Toronto 647/416/437, Vancouver 604/778, Calgary 403, Ottawa 613, Montreal 514/438)
6. Click **Search** → pick a number → **Buy $1.15/mo**
7. Confirm — number is provisioned in ~10 seconds

**Time**: 3 min.

### Step 3 — A2P 10DLC Brand + Campaign registration

**URL**: Sub-account → Settings → **Phone Numbers → Trust Center**

1. **Brand registration** (~5 min form, 1-3 day approval):
   - Business type: select **Sole Proprietor** (BN-9 only) OR **Standard**
   - Canadian BN-9 (first 9 digits of Business Number)
   - Legal business name (match CRA records exactly)
   - Website URL, support email
   - Authorized representative
2. **Campaign registration** (after brand approval):
   - Use case: **Customer Care** (best for RCIC firms — appointment reminders, doc requests)
   - Sample messages (3): supply CASL-compliant templates
   - Opt-in flow: "Website form with consent checkbox"
   - Submit

**Cost**: $4 (sole-prop) or $44 (standard) + $15 campaign + $1.50–$10/mo
**Time**: 10 min active, 1-3 days waiting.

Source: [A2P Sole Proprietor Brand Registration](https://help.gohighlevel.com/support/solutions/articles/155000000340-a2p-sole-proprietor-brand-registration-for-10dlc)

### Step 4 — Configure inbound call routing in GHL

**URL**: Sub-account → Settings → Phone Numbers → **{number} → Configure**

1. **Inbound call behavior**: Forward to Ring Group (firm's RCIC cell phones) OR Voicemail
2. **Voicemail greeting**: Upload MP3 or use text-to-speech: "You've reached {Firm Name}. Please leave a message or text this number and we'll respond within 1 business day."
3. **Call recording**: ON (PIPEDA requires consent notice — add to voicemail greeting: "Calls may be recorded for quality.")
4. **Business hours**: 9-5 ET Mon-Fri (firm-specific)

**Time**: 5 min.

### Step 5 — (Optional) Import number into VAPI for AI outbound intake

Only if firm opts into AI intake (most will). Uses **BYOC** — same DID, no second number.

**URL**: `https://dashboard.vapi.ai/phone-numbers` → **Import Twilio Number**

1. In GHL: Settings → Phone Numbers → **{number} → SIP credentials** (reveal Twilio subaccount SID + auth token from GHL support if not exposed; alternatively use VAPI's "Bring Your Own Carrier" with SIP trunk to `sip.twilio.com`)
2. In VAPI: **Import Phone Number** → paste Twilio account SID + auth token + number
3. Assign to assistant: `289a9701-9199-4d03-9416-49d18bec2f69` (NeuronX Intake Agent)
4. Set outbound caller ID: same number
5. VAPI uses number for outbound calls; inbound continues to hit GHL

**Alternative (easier, pre-production default)**: keep VAPI on its own DID during pilot. Move to BYOC once firm has 50+ calls/month (enough volume to matter).

**Time**: 8 min.

### Step 6 — Test

| Test | How | Expected |
|------|-----|----------|
| Inbound call | Call number from your cell | Rings in GHL or routes to RCIC |
| Outbound call | GHL contact → Click-to-Call | Call connects, caller ID shows number |
| Inbound SMS | Text "hello" to number from cell | Appears in GHL Conversations |
| Outbound SMS | GHL → send test SMS | Delivered to cell within 10 sec |
| AI outbound (if VAPI) | `POST https://api.vapi.ai/call` with customer.number = your cell | VAPI calls you, runs intake script |
| Voicemail | Don't answer inbound call | Hits greeting, records message, appears in GHL |

**Outbound VAPI call test command** (run from laptop, not in sandbox):
```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "289a9701-9199-4d03-9416-49d18bec2f69",
    "phoneNumberId": "ea133993-7c18-4437-88a6-fa7a2d15efbe",
    "customer": {"number": "+1YOURCELL"}
  }'
```

**Time**: 5 min.

---

## Section 4: Current NeuronX + VMC Setup Audit

### Phone inventory (pulled from VAPI API 2026-04-18)

| Number | Provider | VAPI Phone ID | Assistant | Location |
|--------|----------|---------------|-----------|----------|
| **+1 647 931 5181** | Twilio (BYOC) | `ea133993-7c18-4437-88a6-fa7a2d15efbe` | NeuronX Intake Agent | Toronto/GTA (area 647) |
| **+1 447 766 9795** | VAPI-native | `43e01c63-f342-4a5c-84e8-5cd54810dd68` | NeuronX Intake Agent | GTA overlay (area 447, intro 2023) |

Both numbers point to assistant `289a9701-9199-4d03-9416-49d18bec2f69` ("NeuronX Intake Agent", GPT-4o + Deepgram nova-2 + ElevenLabs voice `EXAVITQu4vr4xnSDxMaL`).

### Configuration observations

- **Forwarding number**: `+16479315181` — live human transfer target configured on assistant
- **Voicemail message**: Configured with `{{first_name}}` template, redirects to scheduling
- **Recording**: Enabled (`artifactPlan.recordingEnabled: true`) — PIPEDA requires disclosure in opening script
- **First message**: "Hi, this is NeuronX Immigration Advisory..." — language-choice prompt is excellent
- **Server URL**: `https://neuronx-production-62f9.up.railway.app/webhooks/voice` — webhook receiver is live (confirmed in `neuronx-api/app/routers/webhooks.py:143`)
- **End-of-call report**: Extracts structured data (R1–R5) + summary via `analysisPlan` and POSTs to Railway webhook
- **Silence timeout**: 30s — reasonable
- **Response delay**: 0.8s — feels human-like
- **Max duration**: 600s (10min) — appropriate for intake

### Tests you should run (manual, from your laptop)

```bash
# 1. VAPI outbound call (replace +1YOURCELL)
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer cb69d6fc-baf7-4881-8bff-20c7df251437" \
  -H "Content-Type: application/json" \
  -d '{"assistantId":"289a9701-9199-4d03-9416-49d18bec2f69","phoneNumberId":"ea133993-7c18-4437-88a6-fa7a2d15efbe","customer":{"number":"+1YOURCELL"}}'

# 2. GHL outbound SMS via API
curl -X POST https://services.leadconnectorhq.com/conversations/messages \
  -H "Authorization: Bearer $GHL_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Version: 2021-04-15" \
  -d '{"type":"SMS","contactId":"{contactId}","message":"Test from NeuronX"}'

# 3. Check inbound: text the number from your cell, watch GHL Conversations
```

### Gaps to fix

1. **One number is VAPI-native (+1 447)** — not portable to customer firms, remove or repurpose for internal demo
2. **GHL sub-account (VMC)** — verify the +1 647 number is visible under LC Phone in VMC sub-account. If not, re-import via BYOC
3. **PIPEDA recording disclosure** — add explicit line to `firstMessage`: "This call may be recorded for quality and training."
4. **Voicemail configured at VAPI level only** — also configure GHL LC Phone voicemail as fallback
5. **No per-sub-account number yet** — numbers currently live in VAPI account (NeuronX org), NOT in per-firm GHL sub-accounts. This is wrong for production multi-tenant. Fix during snapshot onboarding process.

### Per-sub-account vs. shared numbers

**Current state**: shared (all at NeuronX org level in VAPI).
**Target state**: per-sub-account. Each RCIC firm owns their own DID inside their GHL sub-account, imported into VAPI with a distinct `phoneNumberId`. Assistant stays shared (single `NeuronX Intake Agent`), but we pass firm context via `assistantOverrides.variableValues` on each outbound call.

---

## Section 5: Cost Analysis @ 50 Firms Scale

Assumptions: each firm uses **500 SMS + 200 voice minutes** per month. 20% of voice minutes are AI-driven (VAPI intake); 80% are human (GHL LC Phone staff calls).

### Per-firm cost (monthly)

| Line item | Qty | Rate | Cost |
|-----------|-----|------|------|
| Number rental | 1 | $1.15 | $1.15 |
| Outbound SMS | 400 | $0.020 | $8.00 |
| Inbound SMS | 100 | $0.010 | $1.00 |
| Human voice (GHL) | 160 min | $0.018 | $2.88 |
| AI voice (VAPI all-in) | 40 min | $0.30 | $12.00 |
| A2P amortized | 1 | — | $6.00 |
| **Total COGS / firm** | | | **$31.03** |

### At 50 firms

| | Monthly | Annual |
|---|---------|--------|
| NeuronX COGS (telephony only) | $1,552 | $18,620 |
| Revenue at $50/firm bundle | $2,500 | $30,000 |
| **Gross margin** | **$948 (38%)** | **$11,380** |

### Pricing recommendation

**Include telephony in base SaaS price, not as line item.** Market $50/mo "Communications" as bundled. Firms hate seeing per-SMS charges.

Tiers:

- **Starter ($500/mo total)**: 200 SMS, 100 voice min, 50 AI min included — overage $0.15/SMS, $0.50/min
- **Growth ($1,000/mo total)**: 1,000 SMS, 500 voice min, 200 AI min included — overage as above
- **Scale ($1,500/mo total)**: unlimited SMS + 1,000 voice min + 500 AI min — overage on AI voice only

**Why mark up**: we absorb A2P registration friction, consolidated billing, 24/7 support, VAPI prompt engineering. Firms save ~4 hours/month vs. rolling their own. That's worth $50-$100/mo.

---

## Section 6: Integration Architecture

```
                         ┌──────────────────────────────┐
                         │   PROSPECT (mobile phone)    │
                         └──────────────┬───────────────┘
                                        │
                   (1) Form submission  │  (2) Inbound call  (3) Inbound SMS
                                        │
                      ┌─────────────────┴─────────────────┐
                      │                                   │
                      ▼                                   ▼
         ┌────────────────────────┐        ┌──────────────────────────┐
         │  GHL Form / Funnel     │        │  GHL LC Phone (Twilio)   │
         │  (landing page V1)     │        │  DID: +1 647-XXX-XXXX    │
         └────────────┬───────────┘        └────────┬─────────────────┘
                      │                             │
                      │ WF-01 trigger               │ Inbound: route to RCIC
                      ▼                             │ (business hours) OR VM
         ┌────────────────────────┐                 │
         │  GHL Workflow (WF-02)  │                 │
         │  5-min contact attempt │                 │
         └────────────┬───────────┘                 │
                      │                             │
                      │ POST /call (outbound AI)    │
                      ▼                             │
         ┌────────────────────────┐                 │
         │   VAPI Outbound Call   │                 │
         │   (same DID caller ID) │                 │
         │   Assistant: 289a970.. │                 │
         └────────────┬───────────┘                 │
                      │                             │
                      │ Real-time conversation      │
                      │                             │
                      │ end-of-call-report          │
                      ▼                             │
         ┌────────────────────────────┐             │
         │  NeuronX API (Railway)     │◄────────────┘
         │  POST /webhooks/voice      │   (also /webhooks/ghl for SMS/form)
         │  - Trust boundary check    │
         │  - R1-R5 extraction        │
         │  - Readiness scoring       │
         │  - Update GHL contact      │
         └────────────┬───────────────┘
                      │
                      │ PATCH /contacts/{id}  +  tags + notes
                      ▼
         ┌────────────────────────────┐
         │  GHL Contact + Pipeline    │
         │  Opportunity auto-advances │
         └────────────┬───────────────┘
                      │
                      │ WF-04 (book consultation)
                      ▼
         ┌────────────────────────────┐
         │  GHL Calendar Booking Link │
         │  SMS + Email sent to client│
         └────────────────────────────┘
```

### Four key flows

**Flow 1 — Inbound prospect call**
`+1 647-XXX-XXXX` → GHL LC Phone → (hours) Ring RCIC group / (after hours) Voicemail → transcription to GHL note. No VAPI (too risky for unknown inbound).

**Flow 2 — Outbound AI intake**
Form submit → WF-01 → `POST /call` VAPI with contact metadata → VAPI calls prospect within 5 min → 3–5 min conversation → end-of-call webhook → Railway API scores, updates GHL, tags `nx:assessment:complete`.

**Flow 3 — RCIC outbound (human)**
GHL contact → "Click to Call" → LC Phone dials from firm's DID → connects to RCIC's cell → call recording saved to contact.

**Flow 4 — SMS (appointment reminder)**
GHL workflow trigger (e.g., 24h before consultation) → template SMS → LC Phone sends → client receives → replies hit GHL Conversations → optionally trigger WF on reply keyword.

**AI-to-human handoff**: inside VAPI, if assistant detects complexity (see `trust_boundaries.md` triggers), it invokes `transfer_to_human` function → NeuronX API responds with transfer TwiML → VAPI initiates SIP REFER back to GHL ring group → RCIC picks up live. Logged as `vapi_human_transfer` event.

---

## Section 7: Risks + Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| **Number blocklisted by Bell/Rogers/Telus** | Medium | High — SMS deliverability drops to <60% | (1) A2P-register every number at onboarding. (2) Monitor delivery rates weekly via GHL dashboards. (3) If blocked: open carrier case through Twilio (takes 5-10 days), cycle to new DID as interim. Keep 2 spare DIDs per firm in reserve for >50-firm tier. |
| **Spam score high (AI calls from unknown numbers)** | High | Medium — 30% call answer rate instead of 60% | (1) Register number with CNAM as firm name (not "NeuronX"). (2) SMS first, then call — `"Hi, {firm} calling about your inquiry — expect a call in 2 min from {number}"` triples pickup. (3) Avoid calling before 9am or after 7pm local. (4) Rotate caller ID across 2-3 DIDs if volume >100/day. |
| **Number porting out (firm leaves NeuronX)** | Low | Medium | Pre-agreed in MSA: firm owns DID, we LOA-port it to their new provider within 10 business days, charge $100 admin fee. Since GHL uses Twilio, port-out is standard Twilio LOA. |
| **PIPEDA violation — call recording without consent** | Medium | Catastrophic — CRTC fine + firm lawsuit | (1) VAPI `firstMessage` MUST include "This call may be recorded for quality purposes." (2) Human GHL calls: voicemail greeting includes same notice. (3) Store recordings in region (Twilio `ca1` region) not US. (4) Retain 90 days max unless litigation hold. |
| **CASL SMS violation** | Medium | Up to $10M fine | (1) Every broadcast SMS: firm ID + STOP instructions. (2) Track consent in `nx:consent_sms_timestamp`. (3) Never SMS a number that hasn't form-opted-in or called us first. (4) Honor STOP within 10s (GHL does automatically). |
| **A2P registration rejected** | Medium | High — can't send SMS for 2-4 wks | (1) Pre-collect firm's exact CRA legal name + BN-9 before registration. (2) Use **sole-prop** tier for solo RCICs (cheaper, faster). (3) Provide 3 sample messages that match actual use (appointment reminders, doc requests). (4) If rejected: resubmit with corrections within 48 hrs. |
| **VAPI platform outage** | Low | High during outage | (1) Inbound calls go to GHL first (not VAPI) — outage only affects outbound AI intake. (2) Fallback: WF-02 queues calls, retries when VAPI healthy. (3) Monitor VAPI status page; failover to GHL voice AI (OD-01 in docs) possible long-term. |
| **Twilio rate limits hit** | Low | Medium | 100 SMS/sec default; raise via Twilio ticket if needed. Stay below 1 SMS/sec from any single firm. GHL workflows throttle automatically. |
| **Number toll-fraud / stolen credentials** | Low | High — can rack $1000s in a weekend | (1) Twilio geo-permissions: allow only CA + US. (2) Alerts on >$50/day spend per firm. (3) VAPI API key rotation quarterly. (4) No credentials in code (already .env). |

---

## Appendix A — Canadian Area Codes Cheat Sheet

| City/Region | Area Codes |
|-------------|------------|
| Toronto / GTA | 416, 647, 437, 447, 942 (overlay) |
| Vancouver | 604, 778, 236, 672 |
| Calgary | 403, 587, 825 |
| Edmonton | 780, 587, 825 |
| Ottawa | 613, 343 |
| Montreal | 514, 438, 263 |
| Halifax | 902, 782 |
| Winnipeg | 204, 431 |

Source: [647 Area Code](https://en.wikipedia.org/wiki/Area_codes_416,_647,_437,_and_942)

Ask the firm for their client base's dominant province. Toronto-based firm serving Ontario clients → get a 416 or 647 (familiar trust). Vancouver firm → 604.

---

## Appendix B — Useful URLs for Onboarding

| Purpose | URL |
|---------|-----|
| GHL LC Phone pricing (authoritative) | https://help.gohighlevel.com/support/solutions/articles/48001223556 |
| A2P sole-prop registration guide | https://help.gohighlevel.com/support/solutions/articles/155000000340 |
| A2P standard registration guide | https://help.gohighlevel.com/support/solutions/articles/48001225526 |
| Canadian 10DLC messaging policies | https://help.gohighlevel.com/support/solutions/articles/155000004915 |
| Twilio pricing | https://www.twilio.com/en-us/pricing |
| VAPI dashboard | https://dashboard.vapi.ai |
| VAPI API docs | https://docs.vapi.ai |
| CASL official (Government of Canada) | https://crtc.gc.ca/eng/com500/faq500.htm |
| CRTC complaints | https://crtc.gc.ca/eng/contact.htm |

---

## Appendix C — Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-18 | Recommend GHL LC Phone as primary, VAPI BYOC for AI | Single DID per firm simplifies client experience + billing |
| 2026-04-18 | A2P-register every number at onboarding (no exceptions) | Canadian carriers block unregistered traffic — cost is negligible vs delivery risk |
| 2026-04-18 | Bundle telephony into SaaS tiers, don't line-item | RCIC firms hate per-SMS charges; bundling improves perceived value |
| 2026-04-18 | Keep VAPI `+1 447` as internal demo number; migrate VMC to per-sub-account model | Current setup is single-tenant — wrong for production at >2 firms |

---

**Owner actions (this week)**:
1. Add PIPEDA recording disclosure to VAPI `firstMessage` and GHL voicemail greeting
2. Confirm `+1 647-931-5181` is imported into VMC GHL sub-account (not just NeuronX VAPI org)
3. Document the BYOC SIP-trunk import procedure in `tools/ghl-lab/README.md` so it's repeatable per firm
4. Begin A2P brand registration for VMC (BN-9 lookup + CRA legal name)
5. Retire or repurpose `+1 447-766-9795` — it serves no production role

**Sources**:
- [LC Phone Pricing & Billing Guide](https://help.gohighlevel.com/support/solutions/articles/48001223556-lc-phone-pricing-billing-guide)
- [LC Phone vs Twilio 2026](https://www.centripe.ai/lc-phone-vs-twilio)
- [GoHighLevel SMS Pricing 2026](https://autogencrm.com/gohighlevel-sms-pricing/)
- [Twilio Pricing](https://www.twilio.com/en-us/pricing)
- [A2P 10DLC Pricing and Carrier Fees](https://help.gohighlevel.com/support/solutions/articles/155000005200)
- [Vapi AI Review 2026 — Retell](https://www.retellai.com/blog/vapi-ai-review)
- [Vapi AI Pricing 2026 — Ringg](https://www.ringg.ai/blogs/vapi-ai-pricing)
- [Updated Messaging Policies for Canadian 10DLC](https://help.gohighlevel.com/support/solutions/articles/155000004915)
- [Complete Guide to CASL-Compliant SMS 2026](https://www.telair.net/resources/knowledge-base/guides/casl-sms-compliance/)
- [SMS Messaging Regulation in Canada 2025 — TALK-Q](https://talk-q.com/sms-messaging-regulation-in-canada)
- [Sending SMS to Canada: Do You Need A2P 10DLC? (2026)](https://www.pingram.io/blog/sending-sms-to-canada-a2p-10dlc)
- [Area codes 416, 647, 437, 942 — Wikipedia](https://en.wikipedia.org/wiki/Area_codes_416,_647,_437,_and_942)
- [447 Area Code — pixelsseo](https://pixelsseo.com/447-area-code/)
