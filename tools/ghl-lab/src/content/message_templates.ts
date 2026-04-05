export const PREMIUM_TEMPLATES = {
  // WF-01: Inquiry Received
  wf01_sms_1: `Hello {{contact.first_name}},

Thank you for contacting our immigration advisory team.
We’ve received your inquiry and a specialist will review your details shortly.

If your matter is urgent, you may reply to this message and our team will assist you.

– NeuronX Immigration Advisory
Reply STOP to opt out`,

  wf01_email_1_subject: `Your Immigration Inquiry – Next Steps`,
  wf01_email_1_body: `Hello {{contact.first_name}},

Thank you for reaching out to our immigration advisory team.

We have received your inquiry and one of our specialists will review your information shortly.

If you wish to schedule a consultation immediately, you may use the link below:
{{trigger.link_or_calendar_link}}

Kind regards,

NeuronX Immigration Advisory`,

  // WF-02: Contact Attempt Sequence
  wf02_sms_1: `Hello {{contact.first_name}},

Our team attempted to reach you regarding your immigration inquiry.

If you would like to proceed with a consultation, you may reply here or schedule directly using the link below:
{{trigger.link}}

– NeuronX Immigration Advisory
Reply STOP to opt out`,

  wf02_email_final_subject: `Regarding your immigration inquiry`,
  wf02_email_final_body: `Hello {{contact.first_name}},

We have attempted to reach you several times regarding your immigration inquiry but haven't been able to connect.

We understand life gets busy. If you are still seeking immigration advice, please feel free to book a consultation at your convenience using the link below:
{{trigger.link}}

If you no longer require assistance, no action is needed.

Kind regards,

NeuronX Immigration Advisory`,

  // WF-04: Readiness Complete (Invite to Book)
  wf04_sms_invite: `Hello {{contact.first_name}},

Based on your assessment, we are pleased to invite you to schedule a consultation with our immigration advisory team.

Please select a time that works for you here:
{{trigger.link}}

– NeuronX Immigration Advisory
Reply STOP to opt out`,

  wf04_email_invite_subject: `Invitation to Schedule Consultation`,
  wf04_email_invite_body: `Hello {{contact.first_name}},

We have reviewed your assessment details and are pleased to invite you to schedule a formal consultation with our immigration advisory team.

During this session, a licensed consultant will review your specific case, discuss your eligibility, and outline your potential pathways.

Please select a convenient time here:
{{trigger.link}}

We look forward to speaking with you.

Kind regards,

NeuronX Immigration Advisory`,

  // WF-05: Consultation Confirmed
  wf05_sms_confirm: `Hello {{contact.first_name}},

Your consultation with our immigration advisory team has been confirmed.

Date: {{appointment.start_time}}

You will receive the meeting details shortly. Please ensure you are available at the scheduled time.

If you need to reschedule, reply to this message.

– NeuronX Immigration Advisory
Reply STOP to opt out`,

  wf05_email_confirm_subject: `Consultation Confirmed: {{appointment.start_time}}`,
  wf05_email_confirm_body: `Hello {{contact.first_name}},

Your consultation with NeuronX Immigration Advisory has been confirmed.

Date: {{appointment.start_time}}
Time Zone: {{appointment.timezone}}
Format: Video Call (Link provided in calendar invite)

Please ensure you are in a quiet place with a stable internet connection for this call.

If you need to reschedule, please use the link below or reply to this email at least 24 hours in advance.
{{appointment.reschedule_link}}

Kind regards,

NeuronX Immigration Advisory`,

  wf05_sms_reminder_48h: `Hello {{contact.first_name}}, reminder: your immigration consultation is in 48 hours ({{appointment.start_time}}). Reply YES to confirm your attendance. – NeuronX Immigration Advisory`,
  
  wf05_sms_reminder_24h: `Hello {{contact.first_name}}, your consultation is tomorrow at {{appointment.start_time}}. Please check your email for the meeting link. – NeuronX Immigration Advisory`,
  
  wf05_sms_reminder_2h: `Hello {{contact.first_name}}, your consultation starts in 2 hours. We look forward to speaking with you. – NeuronX Immigration Advisory`,

  // WF-06: No-Show Recovery
  wf06_sms_recovery: `Hello {{contact.first_name}}, we missed you at your scheduled consultation today. We hope everything is okay.

To reschedule, please use this link:
{{trigger.link}}

– NeuronX Immigration Advisory
Reply STOP to opt out`,

  // WF-09: Retainer Follow-up
  wf09_email_retainer_subject: `Retainer Agreement & Next Steps`,
  wf09_email_retainer_body: `Hello {{contact.first_name}},

Thank you for choosing NeuronX Immigration Advisory. We are honored to assist you with your immigration journey.

Please find attached your Retainer Agreement and the initial Document Checklist.

Next Steps:
1. Review and sign the Retainer Agreement (Link: {{trigger.link}})
2. Complete the initial payment.
3. Begin gathering the documents listed in the checklist.

Once we receive the signed agreement, we will formally open your file and begin work.

Kind regards,

NeuronX Immigration Advisory`,

  // WF-10: Post-Consult Follow-up (Undecided)
  wf10_email_summary_subject: `Consultation Summary`,
  wf10_email_summary_body: `Hello {{contact.first_name}},

Thank you for speaking with us today.

To recap, we discussed your eligibility for [Program Name] and the steps required to proceed.

If you are ready to move forward, please let us know and we will prepare the retainer agreement.

If you have further questions, feel free to reply to this email.

Kind regards,

NeuronX Immigration Advisory`,

  // WF-11: Nurture
  wf11_email_nurture_subject: `Immigration Update: Monthly Insights`,
  wf11_email_nurture_body: `Hello {{contact.first_name}},

Here are the latest updates from Canadian Immigration this month...

[Content Placeholder]

If you are ready to restart your application process, you can book a consultation here:
{{trigger.link}}

Kind regards,

NeuronX Immigration Advisory`
};
