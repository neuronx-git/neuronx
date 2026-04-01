"""
Consultation Preparation Briefing Service

Assembles pre-consultation briefing for RCICs using GHL contact data.
Delivers via email + GHL note 30 minutes before appointment.

See: docs/01_product/prd.md FC-NX-04
See: docs/02_operating_system/operating_spec.md Briefing Template
"""

import logging
from datetime import datetime
from typing import Optional

from app.services.ghl_client import GHLClient
from app.utils.compliance_log import log_event

logger = logging.getLogger("neuronx.briefings")


class BriefingService:
    async def generate_and_deliver(
        self,
        contact_id: str,
        appointment_id: str,
        consultant_email: str,
        delivery_method: str = "email_and_note",
    ) -> dict:
        ghl = GHLClient()

        contact = await ghl.get_contact(contact_id)
        appointment = await ghl.get_appointment(appointment_id)
        opportunities = await ghl.get_opportunities_by_contact(contact_id)

        custom_fields = {}
        for f in contact.get("customFields", []):
            key = f.get("id") or f.get("key")
            val = f.get("value") or f.get("fieldValue")
            if key and val:
                custom_fields[key] = val

        briefing = self._assemble_briefing(contact, appointment, custom_fields, opportunities)

        delivered_to = []

        if delivery_method in ("email_only", "email_and_note"):
            name = f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip()
            try:
                await ghl.send_email(
                    contact_id=contact_id,
                    subject=f"[NeuronX Briefing] {name} — Consultation Prep",
                    body=briefing["html"],
                )
                delivered_to.append(f"email:{consultant_email}")
            except Exception as e:
                logger.warning("Email delivery failed (sandbox?): %s", e)

        if delivery_method in ("note_only", "email_and_note"):
            await ghl.add_note(contact_id, briefing["plain_text"])
            delivered_to.append(f"ghl_note:{contact_id}")

        log_event("briefing_delivered", {
            "contact_id": contact_id,
            "appointment_id": appointment_id,
            "delivered_to": delivered_to,
        })

        return {
            "status": "delivered",
            "contact_id": contact_id,
            "appointment_id": appointment_id,
            "briefing_summary": briefing["summary"],
            "delivered_to": delivered_to,
        }

    def _assemble_briefing(self, contact, appointment, custom_fields, opportunities):
        name = f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip() or "Unknown"
        phone = contact.get("phone", "—")
        email = contact.get("email", "—")
        source = contact.get("source", "Unknown")
        tags = [t if isinstance(t, str) else t.get("name", "") for t in contact.get("tags", [])]

        appt_time = appointment.get("startTime", appointment.get("start_time", "TBD"))

        program = custom_fields.get("ai_program_interest", "Not captured")
        location = custom_fields.get("ai_current_location", "Not captured")
        urgency = custom_fields.get("ai_timeline_urgency", "Not captured")
        prior = custom_fields.get("ai_prior_applications", "Not captured")
        budget = custom_fields.get("ai_budget_awareness", "Not captured")
        outcome = custom_fields.get("ai_readiness_outcome", "Not scored")
        score_val = custom_fields.get("ai_readiness_score", "N/A")

        # Flags
        alert_flags = []
        if "nx:human_escalation" in tags:
            alert_flags.append("COMPLEX CASE — requires senior consultant review")
        if "nx:urgent" in tags:
            alert_flags.append("URGENT — prospect needs help within 30 days")
        if "nx:score:low" in tags:
            alert_flags.append("LOW SCORE — may not be ready for consultation")

        # Score color
        try:
            score_num = int(score_val)
            score_color = "#16a34a" if score_num >= 70 else "#d97706" if score_num >= 40 else "#dc2626"
            score_label = "HIGH" if score_num >= 70 else "MED" if score_num >= 40 else "LOW"
        except (ValueError, TypeError):
            score_color = "#6b7280"
            score_label = "N/A"
            score_num = None

        # Recent notes
        notes = contact.get("notes", [])
        notes_text = "\n".join(f"  - {n.get('body', '')[:200]}" for n in notes[:5]) if notes else "  No notes recorded"

        # ── Plain text version ──
        plain_text = f"""
NeuronX Pre-Consultation Briefing
{'=' * 50}
APPOINTMENT: {appt_time}
{'=' * 50}

PROSPECT: {name}
Phone: {phone} | Email: {email}
Source: {source}

READINESS ASSESSMENT
{'─' * 30}
Program Interest (R1): {program}
Current Location (R2): {location}
Timeline Urgency (R3): {urgency}
Prior Applications (R4): {prior}
Budget Awareness (R5): {budget}

Score: {score_val}/100 ({score_label}) | Outcome: {outcome.upper()}

{('⚠️  ALERTS:' + chr(10) + chr(10).join('  ' + f for f in alert_flags)) if alert_flags else '✅ No escalation flags'}

RECENT INTERACTIONS
{'─' * 30}
{notes_text}

SUGGESTED APPROACH
{'─' * 30}
• {'Senior review required' if 'nx:human_escalation' in tags else 'Standard consultation flow'}
• {'Probe timeline — urgent need' if 'nx:urgent' in tags else 'Standard timeline discussion'}
• Confirm any dimensions not captured by AI
• Focus on {program} pathway specifics
• Close with clear next steps

IMPORTANT: AI has NOT assessed eligibility. All assessments are your professional judgment.
{'=' * 50}
Generated by NeuronX at {datetime.now(tz=__import__('datetime').timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC
""".strip()

        # ── HTML version ──
        flags_html = ""
        if alert_flags:
            flags_items = "".join(f'<li style="color:#dc2626;font-weight:600;">{f}</li>' for f in alert_flags)
            flags_html = f'<div style="background:#fef2f2;border-left:4px solid #dc2626;padding:12px 16px;margin:16px 0;border-radius:4px;"><strong>⚠️ Alerts</strong><ul style="margin:8px 0 0;padding-left:18px;">{flags_items}</ul></div>'
        else:
            flags_html = '<div style="background:#f0fdf4;border-left:4px solid #16a34a;padding:12px 16px;margin:16px 0;border-radius:4px;"><strong>✅ No escalation flags</strong></div>'

        notes_html = "".join(f'<li style="font-size:13px;color:#555;margin-bottom:4px;">{n.get("body", "")[:200]}</li>' for n in notes[:5]) if notes else '<li style="color:#999;">No notes recorded</li>'

        html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Inter,Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:20px 0;"><tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;overflow:hidden;">
<tr><td style="background:#1a1a1a;padding:16px 24px;">
  <h1 style="margin:0;font-size:18px;color:#fff;">NeuronX Pre-Consultation Briefing</h1>
  <p style="margin:4px 0 0;font-size:13px;color:#999;">Appointment: {appt_time}</p>
</td></tr>
<tr><td style="padding:24px;">
  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:20px;">
  <tr>
    <td style="width:60%;">
      <h2 style="margin:0 0 4px;font-size:20px;color:#1a1a1a;">{name}</h2>
      <p style="margin:0;font-size:13px;color:#666;">{phone} &bull; {email}</p>
      <p style="margin:4px 0 0;font-size:12px;color:#999;">Source: {source}</p>
    </td>
    <td style="text-align:right;vertical-align:top;">
      <div style="display:inline-block;background:{score_color};color:#fff;font-size:24px;font-weight:700;padding:8px 16px;border-radius:8px;">
        {score_val}
      </div>
      <p style="margin:4px 0 0;font-size:12px;color:{score_color};font-weight:600;">{score_label} — {outcome.upper()}</p>
    </td>
  </tr></table>

  {flags_html}

  <h3 style="margin:20px 0 8px;font-size:14px;color:#1a1a1a;text-transform:uppercase;letter-spacing:0.5px;">Readiness Assessment (R1–R5)</h3>
  <table width="100%" cellpadding="8" cellspacing="0" style="font-size:14px;border:1px solid #e5e5e5;border-radius:4px;">
    <tr style="background:#f9f9f9;"><td style="font-weight:600;width:40%;">Program Interest (R1)</td><td>{program}</td></tr>
    <tr><td style="font-weight:600;">Current Location (R2)</td><td>{location}</td></tr>
    <tr style="background:#f9f9f9;"><td style="font-weight:600;">Timeline Urgency (R3)</td><td>{urgency}</td></tr>
    <tr><td style="font-weight:600;">Prior Applications (R4)</td><td>{prior}</td></tr>
    <tr style="background:#f9f9f9;"><td style="font-weight:600;">Budget Awareness (R5)</td><td>{budget}</td></tr>
  </table>

  <h3 style="margin:20px 0 8px;font-size:14px;color:#1a1a1a;text-transform:uppercase;letter-spacing:0.5px;">Recent Interactions</h3>
  <ul style="padding-left:18px;margin:0;">{notes_html}</ul>

  <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:4px;padding:12px 16px;margin:20px 0;font-size:12px;color:#92400e;">
    <strong>Reminder:</strong> AI has NOT assessed eligibility. All assessments are your professional judgment as a licensed RCIC.
  </div>
</td></tr>
<tr><td style="background:#f9f9f9;padding:12px 24px;border-top:1px solid #e5e5e5;">
  <p style="margin:0;font-size:11px;color:#999;text-align:center;">
    Generated by NeuronX at {datetime.now(tz=__import__('datetime').timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC
  </p>
</td></tr>
</table></td></tr></table></body></html>"""

        summary = f"{name} | {program} | {outcome} | Score: {score_val}/100"
        return {"plain_text": plain_text, "html": html, "summary": summary}
