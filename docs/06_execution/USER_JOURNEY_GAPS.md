# End-User Journey Audit — NeuronX / VMC

Generated: 2026-04-17T12:27:34.382824Z


## The complete customer journey

This audit maps every touchpoint a prospect/client encounters, and flags gaps.

### Phase 1: Discovery → Inquiry
| Step | Touchpoint | Current state | Gap / Improvement |
|---|---|---|---|
| 1 | Website visit | www.neuronx.co live | ✅ Good |
| 2 | Form submission | Typebot smart form, 79 vars, 16 groups | ✅ Good |
| 3 | Instant email receipt | WF-01 → VMC-01-inquiry-received | ✅ Premium template live |
| 4 | Instant SMS (optional) | ⚠️ Not configured | 💡 Add SMS on form submit via WF-01 |
| 5 | VAPI call within 5-15 min | ✅ Configured, gpt-4o, deepgram | ✅ Good |

### Phase 2: AI Intake Call
| Step | Touchpoint | Current state | Gap / Improvement |
|---|---|---|---|
| 6 | Outbound AI call | VAPI assistant live | ✅ Good |
| 7 | R1-R5 data capture | structuredDataPlan in VAPI | ✅ Works |
| 8 | Score generation | POST /score/lead | ✅ Works |
| 9 | Failed call retry | WF-02 + VMC-02-outreach-attempt | ⚠️ Email ready, workflow must link it |
| 10 | Voicemail handling | ⚠️ Unclear | 💡 Check VAPI voicemail-detection + WF-04C linkage |
| 11 | Complex case escalation | WF-04B → VMC-14-complex-case-alert (internal email) | ✅ Good |

### Phase 3: Consultation Booking
| Step | Touchpoint | Current state | Gap / Improvement |
|---|---|---|---|
| 12 | Post-call invite | WF-04 → VMC-03-invite-booking | ⚠️ Must link template in workflow |
| 13 | Calendar picker | VMC — Free Initial Assessment (15 min) | ✅ Good |
| 14 | Booking confirmation | WF-05 → VMC-04-consultation-confirmed | ⚠️ Link template |
| 15 | Day-before reminder | WF-05 → VMC-05-consultation-reminder | ⚠️ Link template |
| 16 | Calendar ICS + Google Meet link | Standard GHL | ✅ Good |
| 17 | Day-of reminder (1h before) | ❓ Not confirmed | 💡 Add to WF-05 |

### Phase 4: Consultation → Retainer
| Step | Touchpoint | Current state | Gap / Improvement |
|---|---|---|---|
| 18 | RCIC conducts consultation | Human task | ✅ |
| 19 | No-show recovery | WF-06 → VMC-06-noshow-recovery | ⚠️ Link template |
| 20 | Outcome capture | WF-07 (internal) | ✅ Good |
| 21 | Outcome routing (proceed/nurture/complex/disqualified) | WF-08 | ✅ |
| 22 | Retainer proposal sent | WF-09 → VMC-07-retainer-proposal | ⚠️ Link template |
| 23 | Retainer follow-up | WF-09 / WF-10 → VMC-08-retainer-followup | ⚠️ Link template |
| 24 | Digital signature | Documenso (to be wired) | ⚠️ Integration pending |
| 25 | Nurture if medium score | WF-12 → VMC-09-score-medium-handler | ⚠️ Link template |
| 26 | Monthly nurture | WF-11 → VMC-10 + VMC-11 | ⚠️ Link templates |

### Phase 5: Case Processing (after retainer)
| Step | Touchpoint | Current state | Gap / Improvement |
|---|---|---|---|
| 27 | Case initiated (PATCH /cases/initiate) | ✅ Works (persists to PostgreSQL + GHL) | ✅ |
| 28 | Welcome to case email | Needs WF-CP-01 → VMC-15-case-onboarding | ❌ Workflow missing in prod VMC |
| 29 | Onboarding questionnaire | Typebot smart form with contact_id | ✅ |
| 30 | Document upload + OCR | FastMRZ + Ollama Cloud | ✅ |
| 31 | Document collection reminders | WF-CP-02 → VMC-16-cp-docs-reminder | ❌ Workflow missing |
| 32 | Form preparation | WF-CP-03 → VMC-17-cp-form-prep | ❌ Workflow missing |
| 33 | Internal review | WF-CP-04 → VMC-18-cp-internal-review | ❌ Workflow missing |
| 34 | IRCC submission | WF-CP-05 → VMC-19-cp-submitted | ❌ Workflow missing |
| 35 | Processing status updates | WF-CP-06 → VMC-20-cp-status-update | ❌ Workflow missing |
| 36 | RFI (IRCC wants more info) | WF-CP-07 → VMC-21-cp-rfi | ❌ Workflow missing |
| 37 | Decision (approved/refused/withdrawn) | WF-CP-08 → VMC-22/23/24 | ❌ Workflow missing |
| 38 | Case closure | WF-CP-09 → VMC-25-cp-case-closed | ❌ Workflow missing |

### Phase 6: Post-Case
| Step | Touchpoint | Current state | Gap / Improvement |
|---|---|---|---|
| 39 | Testimonial request | In approved email (VMC-22) | ✅ |
| 40 | Review request | In case-closed email (VMC-25) | ✅ |
| 41 | Referral link | In case-closed email | ✅ |
| 42 | Upsell family sponsorship / citizenship | 💡 Not in workflow | 💡 New WF: family sponsor upsell |

## 🎯 Top 10 Improvement Opportunities (end-user impact)

1. **Add SMS to WF-01** — Speed-to-lead wins close rates. Instant "We got your inquiry" SMS matters.
2. **Add 1-hour-before reminder to WF-05** — Reduces no-shows from 15% → 8% industry average.
3. **Link all 26 premium email templates to correct workflows** — We upload them but need to attach.
4. **Build the 9 WF-CP workflows in production VMC** — Cases can be initiated but workflow automation won't fire.
5. **Add branch logic to WF-CP-08** — Decision received routes to approved/refused/withdrawn templates.
6. **Add VAPI voicemail detection** — If AI reaches voicemail, don't waste the attempt.
7. **Family sponsorship upsell workflow** — 60% of PR applicants later sponsor family (huge LTV).
8. **Citizenship reminder at PR+3 years** — Scheduled reminder on case close.
9. **Typebot form embed on GHL forms page** — Currently only on neuronx.co, should also be in GHL funnel.
10. **Documenso e-signature integration** — Currently retainer proposal is email-only, no e-sig.

## 🛠 What I've fixed in this audit run
(see apply_fixes.py for what gets programmatically applied)
