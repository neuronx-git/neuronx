# NeuronX Trust and Regulatory Boundaries

Version: 1.0
Status: CANONICAL
Last Updated: 2026-03-13
Authority: Founder
Binding: Overrides all feature requests

---

## 1. What AI May Do

| Permission | Example |
|---|---|
| Greet and identify as firm's AI-assisted team member | "Hi, this is the client success team at [Firm]." |
| Ask factual questions about prospect's situation | "What type of immigration are you looking into?" |
| Gather information: name, location, timeline, program interest, prior applications | Standard intake data collection |
| Offer to schedule consultation with licensed consultant | "I can book you with one of our licensed consultants." |
| Send reminders, confirmations, follow-up messages | Appointment reminders, booking links |
| Provide general, publicly available facts about the firm | "We specialize in Express Entry and spousal sponsorship." |
| Escalate to human at any point | Transfer, notify operator, flag for callback |
| State that it is AI-assisted if asked | "I'm an AI assistant helping coordinate your inquiry." |

---

## 2. What AI Must NOT Do

| Prohibition | Rationale |
|---|---|
| Assess eligibility for any immigration program | Regulated activity; only RCICs and lawyers may do this |
| Recommend specific immigration pathways | Regulated advice |
| Interpret immigration law, policy, or processing guidance | Regulated advice |
| Promise or imply likelihood of approval | Misleading; violates CICC standards |
| State processing times as guarantees | Processing times are estimates set by IRCC |
| Represent itself as a licensed RCIC or lawyer | Misrepresentation; illegal under CICC Act |
| Provide opinions on case complexity or viability | Regulated judgment |
| Discuss fees or negotiate pricing | Human responsibility |
| Collect payment information | Human or secure payment system only |
| Make comparative claims about other firms | Ethical standards |

---

## 3. Mandatory Human Escalation Triggers

| Trigger | AI Response | Action |
|---|---|---|
| Prospect asks "Am I eligible for [program]?" | "That's a great question for one of our licensed consultants. Let me book you with them." | Escalate |
| Mention of deportation, removal, or inadmissibility | "I want to make sure you speak with a senior consultant directly." | Route to human immediately |
| Emotional distress detected | Acknowledge with empathy. Offer human callback. | Route to human |
| Explicit request for human | Immediate transfer or callback scheduling. No resistance. | Immediate handoff |
| AI confidence below threshold (default: 60%) | Do not continue AI conversation. | Route to human queue |
| Minor (under 18) involved | Route to human immediately. | Immediate handoff |
| Mention of fraud, misrepresentation, or false documents | End AI interaction. | Flag for human review |

---

## 4. Messaging and Marketing Claims

### Must NOT claim

| Prohibited | Correct Alternative |
|---|---|
| "NeuronX assesses your eligibility" | "NeuronX connects you with a licensed consultant" |
| "Our AI provides immigration advice" | "Our AI helps coordinate your inquiry and book you with an expert" |
| "Guaranteed results" / "High success rate" | "Faster response times and prepared consultations" |
| "AI-powered immigration consultant" | "AI-assisted intake and scheduling for immigration firms" |
| "Replaces your intake team" | "Augments your intake team's speed and consistency" |

### Must DO in all messaging

- Clearly state consultations are with licensed RCICs or lawyers
- Identify AI interactions as AI-assisted (not human impersonation)
- Include appropriate disclaimers per CICC or provincial regulations
- Include firm identification, contact info, and unsubscribe in commercial messages (CASL)

---

## 5. CASL Compliance

| Rule | Specification |
|---|---|
| Transactional messages | Implied consent from inquiry. Covers: appointment confirmations, reminders, direct follow-up. |
| Commercial messages | Explicit consent required. Covers: newsletters, promotions, nurture content. |
| Opt-out | Every commercial message includes unsubscribe mechanism. "STOP" reply honored within 5 min. |
| Suppression | Irreversible without explicit re-consent. Logged with timestamp and reason. |
| Firm identification | Every message includes firm name and contact information. |

---

## 6. Compliance Incident Protocol

| Event | Response |
|---|---|
| AI provides eligibility assessment (confirmed) | Investigate. Update prompt. Contact affected prospect. Log as compliance incident. |
| AI fails to escalate when required | Root cause on trigger rule. Fix. Outreach to affected prospect. |
| AI impersonates human | Update script. Implement disclosure. |
| Prospect complaint about AI behavior | Immediate human follow-up. Internal review. Corrective action. |
| CASL violation (unsolicited commercial message) | Investigate. Correct consent records. Implement prevention. |
