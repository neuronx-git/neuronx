#!/usr/bin/env python3
"""Push unified NeuronX-themed HTML to all 11 VMC email templates via GHL API."""

import json
import urllib.request
import urllib.parse
import time

# ─── Config ──────────────────────────────────────────────────────────────
TOKEN_FILE = "/Users/ranjansingh/Desktop/NeuronX/tools/ghl-lab/.tokens.json"
LOC = "FlRL82M0D6nclmKT7eXH"

with open(TOKEN_FILE) as f:
    TOKEN = json.load(f)["access_token"]

# ─── Unified Theme ───────────────────────────────────────────────────────
# Colors: NeuronX Red #E8380D, Dark #1a1a1a, Accent Blue #0284c7
# Font: Inter (system fallback)
# Layout: 600px max-width, 8px border-radius, consistent footer

def build_email(header_color, header_icon, header_title, header_subtitle, body_html, footer_note=""):
    """Build a themed email with consistent NeuronX/VMC branding."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#f0f0f0;font-family:'Inter','Helvetica Neue',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f0f0;padding:32px 16px;">
<tr><td align="center">

<!-- Main card -->
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.08);">

  <!-- Header -->
  <tr><td style="background:{header_color};padding:28px 32px;text-align:center;">
    <p style="margin:0 0 8px;font-size:28px;">{header_icon}</p>
    <h1 style="margin:0;font-size:20px;color:#ffffff;font-weight:700;letter-spacing:-0.3px;">{header_title}</h1>
    <p style="margin:6px 0 0;font-size:13px;color:rgba(255,255,255,0.8);">{header_subtitle}</p>
  </td></tr>

  <!-- Body -->
  <tr><td style="padding:32px;">
    {body_html}
  </td></tr>

  <!-- Footer -->
  <tr><td style="background-color:#fafafa;padding:20px 32px;border-top:1px solid #eee;">
    <table width="100%" cellpadding="0" cellspacing="0"><tr>
      <td style="font-size:12px;color:#999;line-height:1.5;">
        <strong style="color:#666;">Visa Master Canada</strong><br>
        Licensed Immigration Consulting &bull; CICC Regulated<br>
        <a href="mailto:rcic@neuronx.co" style="color:#E8380D;text-decoration:none;">rcic@neuronx.co</a>
        {f'<br><br><span style="color:#bbb;font-size:11px;">{footer_note}</span>' if footer_note else ''}
      </td>
      <td align="right" valign="top" style="font-size:11px;color:#ccc;">
        <a href="{{{{unsubscribe_link}}}}" style="color:#ccc;text-decoration:underline;">Unsubscribe</a>
      </td>
    </tr></table>
  </td></tr>

</table>
<!-- /Main card -->

</td></tr>
</table>
</body>
</html>'''


def cta_button(text, url, color="#E8380D"):
    return f'''<table width="100%" cellpadding="0" cellspacing="0" style="margin:24px 0;">
      <tr><td align="center">
        <a href="{url}" style="display:inline-block;background-color:{color};color:#ffffff;font-size:15px;font-weight:600;text-decoration:none;padding:13px 36px;border-radius:6px;letter-spacing:0.2px;">{text}</a>
      </td></tr>
    </table>'''

def outline_button(text, url, color="#E8380D"):
    return f'''<table width="100%" cellpadding="0" cellspacing="0" style="margin:12px 0;">
      <tr><td align="center">
        <a href="{url}" style="display:inline-block;background:#fff;color:{color};font-size:14px;font-weight:600;text-decoration:none;padding:10px 28px;border-radius:6px;border:2px solid {color};">{text}</a>
      </td></tr>
    </table>'''

def info_box(content, border_color="#E8380D", bg_color="#FFF7ED"):
    return f'''<table width="100%" cellpadding="14" cellspacing="0" style="background:{bg_color};border-left:4px solid {border_color};border-radius:4px;margin:20px 0;">
      <tr><td style="font-size:14px;color:#333;line-height:1.7;">{content}</td></tr>
    </table>'''

def p(text):
    return f'<p style="margin:0 0 16px;font-size:15px;color:#333;line-height:1.7;">{text}</p>'

def greeting(name_field="{{{{contact.first_name}}}}"):
    return p(f"Hi {name_field},")


# ─── All 11 Templates ────────────────────────────────────────────────────

TEMPLATES = {
    # 1. Inquiry Received
    "69c131e926a76b29f946fa4b": build_email(
        "#E8380D", "&#x2709;&#xFE0F;", "Inquiry Received", "Visa Master Canada",
        greeting() +
        p("Thank you for reaching out to Visa Master Canada! We've received your inquiry and a member of our team will be in touch <strong>within 5 minutes</strong>.") +
        info_box(
            "<strong>What happens next:</strong><br>"
            "1. A brief intake call to understand your situation<br>"
            "2. A readiness assessment of your immigration goals<br>"
            "3. A complimentary 15-minute consultation with a licensed RCIC"
        ) +
        p("In the meantime, if you'd like to book your free consultation right away:") +
        cta_button("Book Free Consultation", "https://api.leadconnectorhq.com/widget/booking/To1U2KbcvJ0EAX0RGKHS") +
        p("We look forward to helping you with your Canadian immigration journey.") +
        p("Warm regards,<br><strong>The Visa Master Canada Team</strong>")
    ),

    # 2. Consultation Confirmed
    "69c1325926a76b2c5b46fe5d": build_email(
        "#16a34a", "&#x2705;", "Consultation Confirmed", "Your appointment is booked",
        greeting() +
        p("Great news — your immigration consultation has been confirmed!") +
        info_box(
            "<strong>Appointment Details:</strong><br>"
            "&#x1F4C5; Date: {{{{contact.appointment_date}}}}<br>"
            "&#x23F0; Duration: 15 minutes<br>"
            "&#x1F4DE; Method: Phone / Video Call<br>"
            "&#x1F464; With: Licensed RCIC",
            "#16a34a", "#f0fdf4"
        ) +
        p("<strong>Please prepare:</strong>") +
        p("&#x2022; Your passport or travel document details<br>"
          "&#x2022; Current immigration status information<br>"
          "&#x2022; Questions about your immigration goals<br>"
          "&#x2022; Timeline expectations") +
        p("Need to reschedule? No problem — click below:") +
        outline_button("Reschedule Appointment", "https://api.leadconnectorhq.com/widget/booking/To1U2KbcvJ0EAX0RGKHS", "#16a34a") +
        p("See you soon!<br><strong>Visa Master Canada</strong>")
    ),

    # 3. Consultation Reminder
    "69c13298723a79284163f96c": build_email(
        "#E8380D", "&#x23F0;", "Reminder: Tomorrow", "Your consultation is coming up",
        greeting() +
        p("Just a friendly reminder — your immigration consultation is <strong>tomorrow</strong>.") +
        info_box(
            "&#x1F4C5; <strong>{{{{contact.appointment_date}}}}</strong><br>"
            "&#x23F0; Duration: 15 minutes<br>"
            "&#x1F4DE; Phone / Video Call",
            "#E8380D", "#FFF7ED"
        ) +
        p("<strong>Quick checklist:</strong>") +
        p("&#x2611; Passport or ID ready<br>"
          "&#x2611; Questions prepared<br>"
          "&#x2611; Quiet space for the call") +
        p("Can't make it? Reschedule with one click:") +
        outline_button("Reschedule", "https://api.leadconnectorhq.com/widget/booking/To1U2KbcvJ0EAX0RGKHS") +
        p("See you tomorrow!<br><strong>Visa Master Canada</strong>")
    ),

    # 4. No-Show Recovery
    "69c132f7c3143084391c06ef": build_email(
        "#1a1a1a", "&#x1F44B;", "We Missed You", "Let's reschedule your consultation",
        greeting() +
        p("We noticed you weren't able to make your consultation today. No worries at all — we understand that life gets busy.") +
        p("Your immigration goals are still important to us, and we'd love to find a time that works better for you.") +
        cta_button("Reschedule Now", "https://api.leadconnectorhq.com/widget/booking/To1U2KbcvJ0EAX0RGKHS") +
        p("If you're having trouble finding a time or have any questions, feel free to reply to this email or call us directly.") +
        p("We're here whenever you're ready.<br><strong>Visa Master Canada</strong>"),
        "If you no longer need immigration assistance, simply ignore this email."
    ),

    # 5. Retainer Proposal
    "69c13337088cc77b462ec407": build_email(
        "#E8380D", "&#x1F4CB;", "Your Immigration Proposal", "Review and sign to get started",
        greeting() +
        p("Thank you for your consultation. Based on our discussion, we've prepared a personalized immigration proposal for you.") +
        info_box(
            "<strong>Your Consultation Summary:</strong><br>"
            "&#x1F30D; Program: {{{{contact.ai_program_interest}}}}<br>"
            "&#x23F3; Timeline: {{{{contact.ai_timeline_urgency}}}}<br>"
            "&#x1F4B0; Fee Structure: Transparent, fixed-fee",
            "#E8380D", "#FFF7ED"
        ) +
        p("Your retainer agreement outlines:<br>"
          "&#x2022; Recommended immigration pathway<br>"
          "&#x2022; Complete fee breakdown<br>"
          "&#x2022; Expected timeline and milestones<br>"
          "&#x2022; What we handle vs. what you provide") +
        cta_button("Review &amp; Sign Retainer", "{{{{contact.retainer_link}}}}") +
        p("<strong>Your $200 consultation fee is credited toward the retainer.</strong>") +
        p("Questions? Reply to this email or book a follow-up:") +
        outline_button("Book Follow-up Call", "https://api.leadconnectorhq.com/widget/booking/bHYTHjSMXjuKULrawXNM") +
        p("Best regards,<br><strong>Rajiv Mehta, RCIC</strong><br>Visa Master Canada")
    ),

    # 6. PIPEDA Acknowledgement
    "69c133735c49a40a952e4985": build_email(
        "#1a1a1a", "&#x1F512;", "Privacy Request Received", "Your data request is being processed",
        greeting() +
        p("We've received your personal data request under the <strong>Personal Information Protection and Electronic Documents Act (PIPEDA)</strong>.") +
        info_box(
            "<strong>What happens next:</strong><br>"
            "&#x2705; Request logged with our compliance team<br>"
            "&#x2705; Processing within 30 calendar days<br>"
            "&#x2705; Written confirmation upon completion",
            "#0284c7", "#f0f9ff"
        ) +
        p("If you have any questions about this process, please don't hesitate to contact us.") +
        p("Sincerely,<br><strong>Visa Master Canada</strong><br><span style='color:#666;font-size:13px;'>Privacy &amp; Compliance</span>"),
        "PIPEDA compliance notification. Reference: {{contact.id}}"
    ),

    # 7. Monthly Nurture
    "69c133a626a76b11de470b8d": build_email(
        "#E8380D", "&#x1F4E8;", "Immigration Insights", "Monthly Update from Visa Master Canada",
        greeting() +
        p("Your Canadian immigration journey matters to us — even if the timing isn't right just yet. Here's what's new this month:") +
        info_box(
            "&#x1F4A1; <strong>Monthly Immigration Highlights</strong><br><br>"
            "&#x2022; Latest Express Entry draw results and CRS trends<br>"
            "&#x2022; Provincial Nominee Program updates<br>"
            "&#x2022; Processing time changes across categories<br>"
            "&#x2022; New pathways and pilot programs",
            "#E8380D", "#FFF7ED"
        ) +
        p("Immigration programs evolve constantly. When you're ready to take the next step, we're here to help with a free assessment.") +
        cta_button("Book Free Assessment", "https://api.leadconnectorhq.com/widget/booking/To1U2KbcvJ0EAX0RGKHS") +
        p("Until next month,<br><strong>The Visa Master Canada Team</strong>")
    ),

    # 8. Complex Case Alert (internal)
    "69ca6ee3f608ce36288d16d2": build_email(
        "#DC2626", "&#x1F6A8;", "COMPLEX CASE FLAGGED", "Immediate RCIC Review Required",
        '<p style="margin:0 0 16px;font-size:15px;color:#333;line-height:1.7;">The NeuronX AI intake system has flagged a new case as <strong>complex</strong> requiring manual RCIC review.</p>' +
        info_box(
            "<strong>Contact:</strong> {{{{contact.full_name}}}}<br>"
            "<strong>Email:</strong> {{{{contact.email}}}}<br>"
            "<strong>Phone:</strong> {{{{contact.phone}}}}<br>"
            "<strong>Program:</strong> {{{{contact.ai_program_interest}}}}<br>"
            "<strong>Prior Apps:</strong> <span style='color:#DC2626;font-weight:600;'>{{{{contact.ai_prior_applications}}}}</span><br>"
            "<strong>Escalation Reason:</strong> <span style='color:#DC2626;font-weight:600;'>{{{{contact.ai_escalation_reason}}}}</span>",
            "#DC2626", "#FEF2F2"
        ) +
        p("<strong>Required Actions:</strong><br>"
          "1. Review the AI call transcript<br>"
          "2. Check for conflicts of interest<br>"
          "3. Determine if case requires lawyer referral<br>"
          "4. If accepting: manually confirm Strategy Session<br>"
          "5. If referring out: update status and notify prospect") +
        cta_button("View Contact Record", "{{{{contact.contact_link}}}}", "#DC2626"),
        "Internal notification — do not forward to prospect. Tag: nx:human_escalation"
    ),

    # 9. PIPEDA Deletion Confirmation
    "69ca6ee5874f3b25f8baab99": build_email(
        "#1a1a1a", "&#x1F5D1;", "Data Deleted", "Your personal data has been permanently removed",
        greeting() +
        p("In accordance with your request under <strong>PIPEDA</strong>, we confirm that your personal data has been permanently deleted from our systems.") +
        info_box(
            "<strong>What was deleted:</strong><br>"
            "&#x2022; Contact information (name, email, phone, address)<br>"
            "&#x2022; Intake form submissions and AI call transcripts<br>"
            "&#x2022; Assessment notes and consultation records<br>"
            "&#x2022; Pipeline and opportunity data<br>"
            "&#x2022; All associated tags, notes, and activity history",
            "#0284c7", "#f0f9ff"
        ) +
        p("<strong>Deletion Reference:</strong> DEL-{{{{contact.id}}}}<br><strong>Date Processed:</strong> {{{{date}}}}") +
        p("Certain records may be retained where required by law (e.g., financial transaction records under CRA requirements).") +
        p("If you wish to re-engage our services in the future, please don't hesitate to contact us.") +
        p("Sincerely,<br><strong>Visa Master Canada</strong>"),
        "PIPEDA data deletion confirmation"
    ),

    # 10. Retainer Follow-up 7-day
    "69ca6ee6b3bc887b18efaaf3": build_email(
        "#E8380D", "&#x1F4EC;", "Following Up", "Your retainer agreement is ready",
        greeting() +
        p("I wanted to follow up on the retainer agreement we sent after your consultation. We understand immigration decisions involve careful consideration.") +
        info_box(
            "<strong>Quick Recap:</strong><br>"
            "&#x1F30D; Program: {{{{contact.ai_program_interest}}}}<br>"
            "&#x23F3; Your timeline: {{{{contact.ai_timeline_urgency}}}}<br>"
            "&#x2705; Next step: Review and sign the retainer",
            "#E8380D", "#FFF7ED"
        ) +
        p("<strong>Why act soon?</strong> Immigration processing times and program requirements can change. Starting now helps ensure you meet current eligibility criteria.") +
        cta_button("Review Retainer Agreement", "{{{{contact.retainer_link}}}}") +
        p("Have concerns? Let's talk:") +
        outline_button("Book Quick Follow-up Call", "https://api.leadconnectorhq.com/widget/booking/bHYTHjSMXjuKULrawXNM") +
        p("Looking forward to helping you,<br><strong>Rajiv Mehta, RCIC</strong><br>Visa Master Canada")
    ),

    # 11. Win-Back Nurture 30-day
    "69ca6ee7b3bc8814acefab0b": build_email(
        "#E8380D", "&#x1F331;", "Let's Reconnect", "Your immigration plans, revisited",
        greeting() +
        p("It's been a little while since we last connected about your immigration plans. We understand that timing is everything.") +
        info_box(
            "&#x1F4A1; <strong>What's New:</strong><br>"
            "&#x2022; Updated Express Entry draws with new CRS thresholds<br>"
            "&#x2022; Provincial Nominee Program streams with new occupation lists<br>"
            "&#x2022; Changes to processing times across categories<br>"
            "&#x2022; New pathways and pilot programs you may qualify for",
            "#16a34a", "#f0fdf4"
        ) +
        p("What wasn't the right fit 30 days ago could be a strong option today. We'd love to reassess your situation — no obligation.") +
        '<table width="100%" cellpadding="16" cellspacing="0" style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;margin:20px 0;text-align:center;">'
        '<tr><td>'
        '<p style="margin:0 0 6px;font-size:18px;font-weight:700;color:#1e40af;">Complimentary Follow-up Assessment</p>'
        '<p style="margin:0 0 14px;font-size:14px;color:#3b82f6;">15 minutes with a licensed RCIC — completely free</p>'
        '</td></tr></table>' +
        cta_button("Book Free Assessment", "https://api.leadconnectorhq.com/widget/booking/To1U2KbcvJ0EAX0RGKHS") +
        p("Wishing you the best,<br><strong>The Visa Master Canada Team</strong>"),
        "You previously inquired about immigration services."
    ),
}


# ─── Push to GHL ──────────────────────────────────────────────────────────
def patch_template(template_id, html):
    data = json.dumps({
        "locationId": LOC,
        "htmlData": html
    }).encode("utf-8")

    req = urllib.request.Request(
        f"https://services.leadconnectorhq.com/emails/builder/{template_id}",
        data=data,
        method="PATCH",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Version": "2021-07-28",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        return result.get("ok", False), result.get("name", "?")


if __name__ == "__main__":
    print("=== Pushing Unified NeuronX Theme to All 11 Templates ===\n")

    success = 0
    failed = 0

    for tid, html in TEMPLATES.items():
        try:
            ok, name = patch_template(tid, html)
            icon = "✅" if ok else "❌"
            print(f"  {icon} {name}")
            if ok:
                success += 1
            else:
                failed += 1
            time.sleep(0.5)  # Rate limit
        except Exception as e:
            print(f"  ❌ {tid}: {e}")
            failed += 1

    print(f"\nDone: {success} success, {failed} failed")
