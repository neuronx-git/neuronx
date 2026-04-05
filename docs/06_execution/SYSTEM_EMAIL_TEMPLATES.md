# NeuronX — System Email Templates (GHL Configuration)

These are the **system-level** email templates configured at the sub-account level.
The 7 VMC-branded workflow email templates were already imported in the prior session.

---

## Template 1: Welcome / Account Created

**Subject**: Welcome to {{location.name}}
**From**: {{location.name}} <{{location.email}}>

```
Hi {{contact.first_name}},

Welcome to {{location.name}}. Your inquiry has been received and our team is reviewing your information.

What happens next:
1. A member of our team will reach out within the next few minutes.
2. We'll ask a few questions to understand your immigration goals.
3. If appropriate, we'll book a consultation with a licensed RCIC.

If you have any urgent questions, please call us at {{location.phone}}.

Warm regards,
The {{location.name}} Team

---
{{location.name}}
Licensed RCIC Immigration Consultants
{{location.phone}}
{{location.website}}
```

---

## Template 2: Consultation Booking Confirmed

**Subject**: Your consultation is confirmed — {{appointment.date}}
**From**: {{location.name}} <{{location.email}}>

```
Hi {{contact.first_name}},

Your immigration consultation has been booked:

Date: {{appointment.date}}
Time: {{appointment.time}}
Duration: 30 minutes
With: {{appointment.calendar_name}}

To prepare for your consultation:
- Have your passport/travel documents handy
- Note any previous immigration applications or refusals
- Prepare questions about your immigration goals

If you need to reschedule, please reply to this email or call {{location.phone}}.

Looking forward to speaking with you.

Best regards,
The {{location.name}} Team

---
{{location.name}}
Licensed RCIC Immigration Consultants
{{location.phone}}
{{location.website}}
```

---

## Template 3: Consultation Reminder (24 Hours)

**Subject**: Reminder: Your consultation is tomorrow
**From**: {{location.name}} <{{location.email}}>

```
Hi {{contact.first_name}},

This is a friendly reminder that your immigration consultation is scheduled for tomorrow:

Date: {{appointment.date}}
Time: {{appointment.time}}

Please have the following ready:
- Valid passport or travel documents
- Details of any previous applications or refusals
- Your questions about immigration pathways

If you can't make it, please let us know as soon as possible so we can reschedule.

See you tomorrow,
The {{location.name}} Team

---
{{location.name}}
{{location.phone}} | {{location.website}}
```

---

## Template 4: No-Show Recovery

**Subject**: We missed you — let's reschedule
**From**: {{location.name}} <{{location.email}}>

```
Hi {{contact.first_name}},

We noticed you weren't able to make your consultation today. We understand things come up.

Your file is still active and we'd love to help you with your immigration goals. You can reschedule at a time that works better for you:

[Book New Time] → {{calendar.booking_link}}

If your plans have changed, just reply and let us know. No pressure.

Best regards,
The {{location.name}} Team

---
{{location.name}}
{{location.phone}} | {{location.website}}
```

---

## Template 5: Retainer Proposal

**Subject**: Your immigration consultation summary & next steps
**From**: {{location.name}} <{{location.email}}>

```
Hi {{contact.first_name}},

Thank you for your consultation with {{location.name}}. It was a pleasure learning about your immigration goals.

Based on our discussion, we've prepared a summary of the recommended next steps and our service proposal for your review.

[View Your Proposal] → {{custom_field.proposal_link}}

This proposal is valid for 14 days. If you have any questions, don't hesitate to reach out.

We look forward to helping you on your immigration journey.

Warm regards,
The {{location.name}} Team

---
{{location.name}}
Licensed RCIC Immigration Consultants
{{location.phone}} | {{location.website}}
```

---

## Template 6: Monthly Nurture

**Subject**: Immigration updates from {{location.name}}
**From**: {{location.name}} <{{location.email}}>

```
Hi {{contact.first_name}},

We're reaching out with the latest immigration updates that may be relevant to your situation.

[Personalized content based on program interest — configured per workflow]

If your circumstances have changed or you're ready to move forward, our team is here to help:

[Book a Consultation] → {{calendar.booking_link}}

Stay informed,
The {{location.name}} Team

---
{{location.name}}
Licensed RCIC Immigration Consultants
{{location.phone}} | {{location.website}}

Unsubscribe: {{unsubscribe_link}}
```

---

## Template 7: PIPEDA Data Acknowledgement

**Subject**: Privacy acknowledgement — {{location.name}}
**From**: {{location.name}} <{{location.email}}>

```
Hi {{contact.first_name}},

This email confirms that {{location.name}} has received and securely stores your personal information in accordance with the Personal Information Protection and Electronic Documents Act (PIPEDA).

Your data is used solely for the purpose of providing immigration consulting services. You may request access to, correction of, or deletion of your personal information at any time.

To make a data request, reply to this email or contact us at {{location.phone}}.

Regards,
The {{location.name}} Team

---
{{location.name}}
Licensed RCIC Immigration Consultants
Privacy Policy: {{location.website}}/privacy
```

---

## Configuration Notes

- All templates use `{{location.*}}` merge fields so they work across ALL sub-accounts (white-label ready).
- `{{contact.*}}` fields pull from GHL contact record.
- `{{appointment.*}}` fields pull from GHL calendar booking.
- `{{custom_field.*}}` fields pull from NeuronX custom fields.
- Templates should be created in the Gold sub-account BEFORE snapshot creation so they propagate to all clients.
