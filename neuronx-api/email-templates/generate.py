"""
Generate all 26 premium email templates for NeuronX/VMC.

Uses the ACTUAL Postmark Transactional Email Templates (MIT licensed, 5k+ GitHub stars,
used by millions of emails in production) as the base — NOT custom HTML.

Source: https://github.com/ActiveCampaign/postmark-templates
License: MIT — commercial use OK

Strategy:
1. Use Postmark's "welcome" template for info/notification emails
2. Use Postmark's "password-reset" template for action/CTA emails
3. Only customize:
   - Brand color (Postmark #3869D4 → VMC #E8380D)
   - Product name (Postmark → Visa Master Canada)
   - Content (subject, body, CTA text/URL)
4. Keep all other structure as-is (proven across 70+ email clients)

Usage:
    python email-templates/generate.py
"""
from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).parent
OUT_DIR = BASE_DIR / "rendered"
OUT_DIR.mkdir(exist_ok=True)

# Load Postmark bases (MIT licensed)
POSTMARK_WELCOME = (BASE_DIR / "postmark-base.html").read_text()
POSTMARK_ACTION = (BASE_DIR / "postmark-action-base.html").read_text()


# VMC logo — served from Railway static + CDN-mirrored
# Width 160px renders crisp at 2x DPI (Retina); natural size 785×318
VMC_LOGO_URL = "https://neuronx-production-62f9.up.railway.app/static/vmc-logo.png"
VMC_LOGO_HTML = (
    '<img src="' + VMC_LOGO_URL + '" '
    'alt="Visa Master Canada" '
    'width="160" '
    'style="width:160px;max-width:160px;height:auto;display:block;margin:0 auto 8px;" />'
)


def customize_branding(html: str) -> str:
    """Replace Postmark branding with VMC branding — minimal changes, proven structure."""
    # Brand color: Postmark blue → VMC red (primary CTA color)
    html = html.replace("#3869D4", "#E8380D")
    # Button hover/border color (Postmark uses the same blue)
    html = html.replace("3869d4", "e8380d")  # lowercase variant
    # Masthead: replace the Postmark wordmark <a> element with the VMC logo <img>.
    # Base HTML emits:
    #   <a href="https://example.com" class="f-fallback email-masthead_name" style="...">
    #     [Product Name]
    #   </a>
    html = re.sub(
        r'<a\s+href="https://example\.com"\s+class="f-fallback email-masthead_name"[^>]*>\s*\[Product Name\]\s*</a>',
        VMC_LOGO_HTML,
        html,
        flags=re.DOTALL,
    )
    # Catch any stragglers that didn't match the href attribute exactly.
    html = html.replace("[Product Name]", "Visa Master Canada")
    html = html.replace("[Product]", "Visa Master Canada")
    html = html.replace("Product Name", "Visa Master Canada")
    # Contact details in footer
    html = html.replace("[Company Address]", "Toronto, ON, Canada")
    html = html.replace("[Sender Name]", "The Visa Master Canada Team")
    html = html.replace("The Product Team", "The Visa Master Canada Team")
    return html


def build_welcome_style(subject, preheader, h1, body_paragraphs, signature="The Visa Master Canada Team"):
    """Build an email using Postmark's welcome template style (info/notification, no prominent CTA)."""
    html = customize_branding(POSTMARK_WELCOME)

    # Replace title
    html = re.sub(r"<title>[^<]*</title>", f"<title>{subject}</title>", html)

    # Postmark welcome has a specific content structure — find and replace main content block
    # Looking for the <h1> tag onward
    new_content = f"<h1>{h1}</h1>\n"
    for para in body_paragraphs:
        if para.startswith("<"):
            new_content += f"{para}\n"
        else:
            new_content += f'<p>{para}</p>\n'
    new_content += f'<p>Thanks,<br>{signature}</p>'

    # Replace the welcome body - Postmark welcome template has specific content
    # Find the main content container and replace
    html = re.sub(
        r'(<h1[^>]*>).*?(<p>Thanks,<br>.*?</p>)',
        f'\\1{h1}</h1>\n' + "\n".join(
            p if p.startswith('<') else f'<p>{p}</p>' for p in body_paragraphs
        ) + f'\n<p>Thanks,<br>{signature}</p>',
        html,
        flags=re.DOTALL,
    )

    # Set preheader (often stored in a hidden span)
    html = re.sub(r'<span class="preheader"[^>]*>[^<]*</span>',
                  f'<span class="preheader">{preheader}</span>', html)

    return html


def build_action_style(subject, preheader, h1, body_paragraphs, cta_text, cta_url,
                       post_cta_paragraphs=None, signature="The Visa Master Canada Team"):
    """Build an email using Postmark's action template style (has CTA button)."""
    html = customize_branding(POSTMARK_ACTION)

    # Title
    html = re.sub(r"<title>[^<]*</title>", f"<title>{subject}</title>", html)

    # Content replacement — Postmark password-reset has h1 + paragraphs + button + trouble-text
    body_html = "".join(
        p if p.startswith('<') else f'<p>{p}</p>' for p in body_paragraphs
    )
    post_cta_html = ""
    if post_cta_paragraphs:
        post_cta_html = "".join(
            p if p.startswith('<') else f'<p>{p}</p>' for p in post_cta_paragraphs
        )

    # The password-reset template has this general structure:
    # <h1>You have received this email...</h1>
    # <p>Click...</p>
    # <table role="presentation" class="body-action" ...>
    #   <tr><td><a href="...">Reset your password</a></td></tr>
    # </table>
    # <p>...valid for 1 hour...</p>
    # <p>Thanks,<br>Product Team</p>

    # Replace h1
    html = re.sub(r'<h1>[^<]*</h1>', f'<h1>{h1}</h1>', html, count=1)
    # Replace the CTA button href + text (Postmark uses class="button" or anchor inside body-action)
    html = re.sub(
        r'<a\s+href="\{\{[^}]+\}\}"\s+class="button[^"]*"[^>]*>[^<]*</a>',
        f'<a href="{cta_url}" class="f-fallback button button--red" target="_blank" '
        f'style="color: #FFF; border-color: #E8380D; border-style: solid; border-width: 10px 18px; '
        f'background-color: #E8380D; display: inline-block; text-decoration: none; '
        f'border-radius: 3px; box-shadow: 0 2px 3px rgba(0,0,0,0.16); '
        f'-webkit-text-size-adjust: none; box-sizing: border-box;">{cta_text}</a>',
        html, count=1,
    )

    # Replace content between <h1> and first </p> after button
    # Simpler: find the content td and replace its entire body
    content_pattern = re.compile(
        r'(<td class="content-cell">)(.*?)(</td>\s*</tr>\s*</table>\s*</td>\s*</tr>\s*<!-- Sub copy)',
        re.DOTALL,
    )
    replacement_content = f"""<h1>{h1}</h1>
{body_html}
<table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body-action" align="center" width="100%" style="width: 100%;">
  <tr>
    <td align="center">
      <table border="0" cellpadding="0" cellspacing="0" role="presentation">
        <tr>
          <td>
            <a href="{cta_url}" target="_blank"
              style="background: #E8380D; border-radius: 3px; box-shadow: 0 2px 3px rgba(0,0,0,0.16); color: #FFF; display: inline-block; text-decoration: none; font-weight: bold; padding: 12px 24px; font-size: 15px;">
              {cta_text}
            </a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
{post_cta_html}
<p>Thanks,<br>{signature}</p>
<p class="sub">If you're having trouble with the button above, copy and paste the URL below into your web browser.</p>
<p class="sub"><a href="{cta_url}">{cta_url}</a></p>
"""
    new_html, n = content_pattern.subn(r'\1' + replacement_content + r'\3', html)
    if n > 0:
        html = new_html
    else:
        # Fallback — just swap button href
        html = re.sub(r'<a href="https?://[^"]*"([^>]*class="[^"]*button[^"]*")',
                      f'<a href="{cta_url}"\\1', html, count=1)

    # Preheader
    html = re.sub(r'<span class="preheader"[^>]*>[^<]*</span>',
                  f'<span class="preheader">{preheader}</span>', html)

    return html


def render(slug, subject, preheader, category, html):
    """Save rendered template."""
    (OUT_DIR / f"{slug}.html").write_text(html)
    return {
        "slug": slug, "subject": subject, "preheader": preheader,
        "category": category, "path": str(OUT_DIR / f"{slug}.html"),
        "size": len(html),
    }


# Merge-tag helper
T = lambda k: "{{" + k + "}}"

templates = []

# ═══════════════════════════════════════════════════════════════════════════
# INTAKE FUNNEL — 14 templates
# ═══════════════════════════════════════════════════════════════════════════

# 01 — Inquiry received (WF-01)
html = build_action_style(
    subject=f"We received your inquiry, {T('contact.first_name')} — next steps inside",
    preheader="Our AI-assisted intake will call you in 5-15 minutes. Here's what to expect.",
    h1=f"Thanks for reaching out, {T('contact.first_name')}!",
    body_paragraphs=[
        "We've received your immigration inquiry and a licensed RCIC will review your situation within the next 2 business hours.",
        "<strong>What happens next:</strong> In 5–15 minutes, you'll receive a short call from our AI-assisted intake assistant to gather a few key details. This helps us match you with the right consultant.",
    ],
    cta_text="View your inquiry status",
    cta_url=f"https://www.neuronx.co/intake/vmc/onboarding?contact_id={T('contact.id')}",
    post_cta_paragraphs=[
        "<strong>Your submission</strong>",
        f"Program interest: {T('contact.ai_program_interest')}<br>Current location: {T('contact.ai_current_location')}",
        "Questions? Reply to this email — a real person reads every message.",
    ],
)
templates.append(render("01-inquiry-received",
    f"We received your inquiry, {T('contact.first_name')} — next steps inside",
    "Our AI-assisted intake will call you in 5-15 minutes.", "INQUIRY RECEIVED", html))

# 02 — Outreach attempt (WF-02) — NEW
html = build_action_style(
    subject=f"{T('contact.first_name')}, we couldn't reach you — let's schedule",
    preheader="Pick a time that works. A licensed RCIC is holding your file.",
    h1=f"We tried calling you, {T('contact.first_name')}",
    body_paragraphs=[
        "We attempted to reach you about your Canadian immigration inquiry but couldn't get through.",
        "Your inquiry is still active. A licensed RCIC is holding your file — please pick a time that works for you.",
    ],
    cta_text="Book a 15-minute assessment",
    cta_url=f"https://www.neuronx.co/intake/vmc/onboarding?contact_id={T('contact.id')}",
    post_cta_paragraphs=[
        "Or reply to this email with 2–3 times that work for you, and we'll make it happen.",
        "<em>If you've changed your mind about pursuing immigration, just reply STOP and we won't contact you again.</em>",
    ],
)
templates.append(render("02-outreach-attempt",
    f"{T('contact.first_name')}, we couldn't reach you — let's schedule",
    "Pick a time that works. A licensed RCIC is holding your file.", "FOLLOW-UP", html))

# 03 — Invite to book (WF-04) — NEW
html = build_action_style(
    subject=f"{T('contact.first_name')}, you're ready — book your free consultation",
    preheader="A licensed RCIC is ready to discuss your case. Free 15-minute consultation.",
    h1=f"Your assessment is complete, {T('contact.first_name')}",
    body_paragraphs=[
        "Based on the information you shared, we've prepared an initial readiness profile. A licensed RCIC is ready to discuss your case in detail.",
        f"Program interest: <strong>{T('contact.ai_program_interest')}</strong><br>"
        f"Timeline: <strong>{T('contact.ai_timeline_urgency')}</strong><br>"
        f"Readiness score: <strong>{T('contact.ai_readiness_score')} / 100</strong>",
    ],
    cta_text="Book my free consultation",
    cta_url=f"https://api.leadconnectorhq.com/widget/booking/{T('contact.booking_slug')}",
    post_cta_paragraphs=[
        "<strong>What to prepare:</strong>",
        "• Current passport (any country)<br>• Previous visa or work permit details<br>"
        "• Educational credentials (if applying for Express Entry)<br>• Language test results (if available)",
    ],
)
templates.append(render("03-invite-booking",
    f"{T('contact.first_name')}, you're ready — book your free consultation",
    "A licensed RCIC is ready to discuss your case.", "ACTION REQUIRED", html))

# 04 — Consultation confirmed (WF-05)
html = build_action_style(
    subject=f"✅ Your consultation is confirmed, {T('contact.first_name')}",
    preheader="Your immigration consultation is booked. Details inside.",
    h1=f"Your consultation is confirmed, {T('contact.first_name')}!",
    body_paragraphs=[
        "We're looking forward to speaking with you about your Canadian immigration journey.",
        f"<strong>Date:</strong> {T('appointment.start_date')}<br>"
        f"<strong>Time:</strong> {T('appointment.start_time')} {T('appointment.timezone')}<br>"
        f"<strong>Consultant:</strong> {T('appointment.assigned_user_name')}, RCIC<br>"
        f"<strong>Duration:</strong> {T('appointment.duration')} minutes<br>"
        f"<strong>Format:</strong> Video call (Google Meet)",
    ],
    cta_text="Join the Google Meet",
    cta_url=T('appointment.meeting_url'),
    post_cta_paragraphs=[
        "<strong>Before your call:</strong>",
        "• Have your passport nearby<br>• Think of 2–3 specific questions<br>• Test your camera and microphone",
        f"Need to reschedule? <a href=\"{T('appointment.reschedule_url')}\">Click here</a> — we'll find a new time.",
    ],
)
templates.append(render("04-consultation-confirmed",
    f"✅ Your consultation is confirmed, {T('contact.first_name')}",
    "Your immigration consultation is booked.", "BOOKING CONFIRMED", html))

# 05 — Consultation reminder (WF-05)
html = build_action_style(
    subject=f"⏰ Reminder: your consultation is tomorrow, {T('contact.first_name')}",
    preheader="Your immigration consultation is tomorrow. Quick checklist inside.",
    h1="Your consultation is tomorrow",
    body_paragraphs=[
        f"Just a friendly reminder — your immigration consultation with <strong>{T('appointment.assigned_user_name')}, RCIC</strong> is tomorrow.",
        f"<strong>Date:</strong> {T('appointment.start_date')}<br>"
        f"<strong>Time:</strong> {T('appointment.start_time')} {T('appointment.timezone')}<br>"
        f"<strong>Format:</strong> Video (Google Meet)",
    ],
    cta_text="Add to my calendar",
    cta_url=T('appointment.ics_url'),
    post_cta_paragraphs=[
        "<strong>Quick pre-call checklist:</strong>",
        "• Passport ready for reference<br>• Questions written down<br>• Camera & mic tested<br>• Quiet location with good internet",
        f"Can't make it? <a href=\"{T('appointment.reschedule_url')}\">Reschedule in 10 seconds</a>.",
    ],
)
templates.append(render("05-consultation-reminder",
    f"⏰ Reminder: your consultation is tomorrow, {T('contact.first_name')}",
    "Your immigration consultation is tomorrow.", "REMINDER", html))

# 06 — No-show recovery (WF-06)
html = build_action_style(
    subject="👋 We missed you — let's reschedule",
    preheader="Quick 30-second rescheduling link. No pressure.",
    h1=f"We missed you, {T('contact.first_name')}",
    body_paragraphs=[
        "We noticed you weren't able to make your consultation today. No worries at all — life happens.",
        "A licensed RCIC still has your file and is ready to help whenever you are.",
    ],
    cta_text="Reschedule in 30 seconds",
    cta_url=T('appointment.reschedule_url'),
    post_cta_paragraphs=[
        "If we don't hear from you within 7 days, we'll move your file to our nurture program — you'll still get monthly updates on immigration pathways relevant to you.",
        "<em>Not the right time anymore? No problem — just reply STOP and we'll respectfully step back.</em>",
    ],
)
templates.append(render("06-noshow-recovery", "👋 We missed you — let's reschedule",
    "Quick 30-second rescheduling link.", "MISSED APPOINTMENT", html))

# 07 — Retainer proposal (WF-09)
html = build_action_style(
    subject=f"📋 Your immigration proposal is ready, {T('contact.first_name')}",
    preheader="Review and sign your retainer agreement. Fees held in ICCRC trust account.",
    h1="Your immigration proposal is ready",
    body_paragraphs=[
        "Thank you for your consultation with us. Based on our discussion, we've prepared a personalized retainer agreement.",
        f"<strong>Program:</strong> {T('contact.case_program_type')}<br>"
        f"<strong>Estimated timeline:</strong> {T('contact.case_estimated_months')} months<br>"
        f"<strong>Fixed professional fees:</strong> CAD {T('contact.retainer_amount')}<br>"
        f"<strong>Government fees:</strong> CAD {T('contact.govt_fees_estimate')}<br>"
        f"<strong>Your RCIC:</strong> {T('contact.assigned_rcic')}",
        "<strong>What's included:</strong> Full case strategy, all IRCC form preparation, submission to IRCC, response management for any RFI, unlimited email + monthly check-ins.",
    ],
    cta_text="Review and sign the proposal",
    cta_url=T('contact.proposal_url'),
    post_cta_paragraphs=[
        "<em>Payment is held in an ICCRC-regulated trust account. You only pay government fees when your application is ready to submit.</em>",
    ],
)
templates.append(render("07-retainer-proposal",
    f"📋 Your immigration proposal is ready, {T('contact.first_name')}",
    "Review and sign your retainer agreement.", "PROPOSAL", html))

# 08 — Retainer follow-up (WF-09/10)
html = build_action_style(
    subject="📬 Quick follow-up on your immigration proposal",
    preheader="I'm here to answer any questions about the retainer.",
    h1="Following up on your proposal",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, I wanted to follow up on the retainer agreement we sent after your consultation.",
        "I know immigration decisions are significant, so please take whatever time you need. If you have questions, I'm happy to jump on a quick call.",
    ],
    cta_text="Review the proposal",
    cta_url=T('contact.proposal_url'),
    post_cta_paragraphs=[
        "<strong>Common questions at this stage:</strong>",
        '<em>"Can you clarify the fee structure?"</em><br>All professional fees are flat — no hourly surprises. Government fees (listed separately) are paid directly to IRCC.',
        '<em>"What if my circumstances change?"</em><br>You can pause or withdraw anytime in the first 14 days for a full refund.',
        '<em>"Can I speak to your consultant again?"</em><br>Absolutely — reply to this email and I\'ll set up a 10-minute call.',
    ],
)
templates.append(render("08-retainer-followup", "📬 Quick follow-up on your immigration proposal",
    "I'm here to answer any questions about the retainer.", "FOLLOW-UP", html))

# 09 — Score medium handler (WF-12) — NEW
html = build_action_style(
    subject="🌱 Your immigration roadmap — let's build it together",
    preheader="Strong potential, some prep needed. Monthly updates + profile strengthening guide.",
    h1=f"Let's build your pathway, {T('contact.first_name')}",
    body_paragraphs=[
        "Based on what you shared, your situation has strong potential but some elements may need preparation before you're ready to file.",
        "<strong>Good news:</strong> Canadian immigration rules reward preparation. Most successful applicants spent 3–6 months strengthening their profile before applying.",
        "<strong>How we can help from here:</strong><br>"
        "• Monthly email updates — program changes, eligibility tips<br>"
        "• Profile strengthening roadmap — specific steps for your case<br>"
        "• Priority rebook — when you're ready, we'll prioritize your consultation",
    ],
    cta_text="Read the Express Entry 2026 guide",
    cta_url="https://www.neuronx.co/guides/express-entry-2026",
    post_cta_paragraphs=[
        "<em>No pressure, no sales calls — just useful information. Unsubscribe anytime from the footer.</em>",
    ],
)
templates.append(render("09-score-medium-handler", "🌱 Your immigration roadmap — let's build it together",
    "Strong potential, some prep needed.", "ROADMAP", html))

# 10 — Monthly nurture (WF-11)
html = build_welcome_style(
    subject=f"📨 {T('nurture.month')} — Canadian immigration update",
    preheader="This month's IRCC changes, program spotlight, and one actionable tip.",
    h1=f"{T('nurture.month')} Immigration Update",
    body_paragraphs=[
        "Your Canadian immigration journey matters to us — even if the timing isn't right. Here's what changed this month:",
        f"<strong>🇨🇦 IRCC This Month:</strong> {T('nurture.ircc_news')}",
        f"<strong>🏆 Program Spotlight — {T('nurture.program_spotlight_name')}:</strong> {T('nurture.program_spotlight_text')}",
        f'Read the full article: <a href="{T("nurture.article_url")}">{T("nurture.article_url")}</a>',
        f"<strong>💡 Tip of the month:</strong> {T('nurture.tip_text')}",
        'Ready to revisit your options? <a href="https://www.neuronx.co/intake/vmc/onboarding">Book a fresh 15-minute assessment</a> — still free.',
    ],
)
templates.append(render("10-monthly-nurture",
    f"📨 {T('nurture.month')} — Canadian immigration update",
    "This month's IRCC changes, program spotlight, and one tip.", "MONTHLY UPDATE", html))

# 11 — Win-back nurture (WF-11)
html = build_action_style(
    subject=f"🌱 A lot has changed in Canadian immigration, {T('contact.first_name')}",
    preheader="CRS cutoffs at multi-year lows. PNP streams expanded. Worth a fresh look?",
    h1=f"Let's reconnect, {T('contact.first_name')}",
    body_paragraphs=[
        "It's been a little while since we last connected about your immigration plans. A lot has changed in Canadian immigration since then.",
        "<strong>What's new that might affect your case:</strong><br>"
        "• Express Entry CRS cutoffs are at multi-year lows<br>"
        "• PNP streams across provinces have expanded eligibility<br>"
        "• Family reunification processing has sped up significantly<br>"
        "• Category-based draws favor healthcare, STEM, and trades",
        "Your situation may be more viable today than when we last spoke.",
    ],
    cta_text="15-minute refresh call — free",
    cta_url="https://www.neuronx.co/intake/vmc/onboarding",
    post_cta_paragraphs=[
        "<em>If this isn't the right time, no pressure — reply STOP and we'll respectfully step back.</em>",
    ],
)
templates.append(render("11-winback-nurture",
    f"🌱 A lot has changed in Canadian immigration, {T('contact.first_name')}",
    "CRS cutoffs at multi-year lows. Worth a fresh look?", "RECONNECT", html))

# 12 — PIPEDA ack (WF-13)
html = build_welcome_style(
    subject="🔒 Privacy request received — we're on it",
    preheader="Your PIPEDA request is being processed. 30-day response guaranteed.",
    h1="Privacy request received",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, we've received your personal data request under the Personal Information Protection and Electronic Documents Act (PIPEDA).",
        f"<strong>Request ID:</strong> {T('contact.pipeda_request_id')}<br>"
        f"<strong>Request type:</strong> {T('contact.pipeda_request_type')}<br>"
        f"<strong>Submitted:</strong> {T('contact.pipeda_submitted_at')}",
        "We will process your request within <strong>30 calendar days</strong> as required by law. You'll receive a confirmation email once the action is complete.",
        "<em>If your request involves account deletion, some records (IRCC-submitted applications, financial records) must be retained for regulatory compliance. We'll clarify retention requirements in our confirmation.</em>",
        "Questions about your privacy rights? Contact our Privacy Officer at privacy@visamasters.ca.",
    ],
)
templates.append(render("12-pipeda-ack", "🔒 Privacy request received — we're on it",
    "Your PIPEDA request is being processed.", "PRIVACY", html))

# 13 — PIPEDA deletion confirmed (WF-13)
html = build_welcome_style(
    subject="🗑 Your data has been permanently deleted",
    preheader="PIPEDA deletion complete. IRCC-submitted records retained per federal regulation.",
    h1="Your data has been deleted",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, in accordance with your request under PIPEDA, we confirm that your personal data has been <strong>permanently removed</strong> from our active systems.",
        "<strong>What was deleted:</strong><br>"
        "• Contact information (name, email, phone)<br>"
        "• Communication history (emails, SMS, call transcripts)<br>"
        "• Notes and consultation records<br>"
        "• Marketing preferences",
        "<strong>Retained for regulatory compliance:</strong> Any files actively submitted to IRCC must be retained for 7 years per federal regulations. These are stored encrypted and access is logged.",
        "Thank you for being part of the Visa Master Canada community. We wish you the best on your journey — whatever path you choose.",
    ],
)
templates.append(render("13-pipeda-deleted", "🗑 Your data has been permanently deleted",
    "PIPEDA deletion complete.", "PRIVACY", html))

# 14 — Complex case alert (internal)
html = build_welcome_style(
    subject="🚨 Complex case flagged — RCIC review needed",
    preheader="Internal alert: complex case requires manual review within 24h.",
    h1="🚨 Complex Case Flagged",
    body_paragraphs=[
        "The NeuronX AI intake system has flagged a new case as <strong>complex</strong>, requiring manual RCIC review.",
        f"<strong>Contact:</strong> {T('contact.full_name')}<br>"
        f"<strong>Email:</strong> {T('contact.email')}<br>"
        f"<strong>Phone:</strong> {T('contact.phone')}<br>"
        f"<strong>Program:</strong> {T('contact.ai_program_interest')}<br>"
        f"<strong>Flags:</strong> {T('contact.complexity_flags')}",
        f"<strong>Transcript excerpt:</strong> {T('contact.call_transcript_excerpt')}",
        "<strong>Action required within 24 hours:</strong> AI has paused automated outreach. This lead is in a hold state pending senior consultant review.",
        f'Open case in GHL: <a href="https://app.gohighlevel.com/v2/location/{T("location.id")}/contacts/{T("contact.id")}">Click here</a>',
    ],
    signature="NeuronX AI System",
)
templates.append(render("14-complex-case-alert", "🚨 Complex case flagged — RCIC review needed",
    "Internal alert: complex case.", "INTERNAL ALERT", html))

# ═══════════════════════════════════════════════════════════════════════════
# CASE PROCESSING — 12 templates
# ═══════════════════════════════════════════════════════════════════════════

# 15 — WF-CP-01 Welcome to case processing
html = build_action_style(
    subject=f"🎉 Welcome, {T('contact.first_name')} — your immigration case is open",
    preheader="Your retainer is signed. Here's what happens next + your onboarding link.",
    h1=f"Welcome to the Visa Master family, {T('contact.first_name')}!",
    body_paragraphs=[
        "Your retainer is signed and your case is officially open. Here's what happens next.",
        f"<strong>Case ID:</strong> {T('contact.case_id')}<br>"
        f"<strong>Program:</strong> {T('contact.case_program_type')}<br>"
        f"<strong>Your RCIC:</strong> {T('contact.case_assigned_rcic')}<br>"
        f"<strong>Estimated timeline:</strong> {T('contact.case_estimated_months')} months<br>"
        f"<strong>Document deadline:</strong> {T('contact.case_deadline_date')}",
        "<strong>Your next 14 days:</strong><br>"
        "• Today: Complete the onboarding questionnaire (15 min)<br>"
        "• Days 1–7: Upload required documents<br>"
        "• Days 7–14: Your RCIC reviews everything and begins form prep",
    ],
    cta_text="Start your onboarding questionnaire",
    cta_url=f"https://www.neuronx.co/intake/vmc/onboarding?contact_id={T('contact.id')}",
    post_cta_paragraphs=[
        "<strong>One link, works everywhere:</strong> This single link is yours for the entire case. Start it, stop, come back — your progress is saved automatically.",
    ],
)
templates.append(render("15-case-onboarding",
    f"🎉 Welcome, {T('contact.first_name')} — your immigration case is open",
    "Your retainer is signed. Here's what happens next.", "CASE OPEN", html))

# 16 — WF-CP-02 Document reminder
html = build_action_style(
    subject=f"📎 {T('contact.first_name')}, still need a few documents for your case",
    preheader="Document deadline reminder + list of outstanding items.",
    h1="Friendly reminder: documents needed",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, we're still waiting on a few items for your case. No rush — just want to make sure we stay on track.",
        f"<strong>Case:</strong> {T('contact.case_id')} — {T('contact.case_program_type')}<br>"
        f"<strong>Documents received:</strong> {T('contact.docs_received')} / {T('contact.docs_required')}<br>"
        f"<strong>Days until deadline:</strong> {T('contact.days_until_deadline')}",
        f"<strong>Still needed:</strong><br>{T('contact.outstanding_docs_html')}",
    ],
    cta_text="Upload remaining documents",
    cta_url=f"https://www.neuronx.co/intake/vmc/onboarding?contact_id={T('contact.id')}",
    post_cta_paragraphs=[
        "<em>Can't find a document? Reply to this email and your RCIC will help. We often have workarounds for tricky documents (lost degrees, expired passports, etc.).</em>",
    ],
)
templates.append(render("16-cp-docs-reminder",
    f"📎 {T('contact.first_name')}, still need a few documents for your case",
    "Document deadline reminder.", "DOCS PENDING", html))

# 17 — WF-CP-03 Form prep started
html = build_welcome_style(
    subject="✏️ Your IRCC forms are being prepared",
    preheader="All docs received. Your RCIC is now preparing your IRCC forms.",
    h1="Your IRCC forms are being prepared",
    body_paragraphs=[
        f"All your documents are in. Your RCIC, <strong>{T('contact.case_assigned_rcic')}</strong>, has officially started preparing your IRCC forms.",
        "<strong>What's happening now:</strong><br>"
        "• Completing all IRCC forms (IMM 0008, Schedule A, etc.)<br>"
        "• Cross-referencing your documents against IRCC requirements<br>"
        "• Checking for any optimization opportunities (PNP eligibility, dependent claims, etc.)<br>"
        "• Preparing your personalized cover letter",
        f"<strong>Case:</strong> {T('contact.case_id')}<br>"
        f"<strong>Stage:</strong> Form Preparation<br>"
        f"<strong>Estimated days until submission:</strong> {T('contact.days_until_submission')}",
        "<em>You don't need to do anything right now. We'll email you when forms are ready for your review and e-signature.</em>",
    ],
)
templates.append(render("17-cp-form-prep", "✏️ Your IRCC forms are being prepared",
    "All docs received. Your RCIC is preparing your IRCC forms.", "IN PREPARATION", html))

# 18 — WF-CP-04 Internal review
html = build_welcome_style(
    subject=f"🔍 {T('contact.first_name')}, your application is in final review",
    preheader="3-step QA in progress. Review + e-sign link coming in 2–3 days.",
    h1="Your application is in final review",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, great news — your forms are drafted and your application is now in our internal quality-assurance review.",
        "<strong>Our 3-step QA process:</strong><br>"
        "✓ Senior RCIC peer review (case strategy + form accuracy)<br>"
        "✓ Document cross-check (every field matched to supporting doc)<br>"
        "✓ Final compliance check (signatures, page counts, IRCC format)",
        f"<strong>Case:</strong> {T('contact.case_id')}<br>"
        f"<strong>Stage:</strong> Internal Review<br>"
        f"<strong>Next step:</strong> You review + e-sign, then we submit",
        "We'll send you the complete application package for your review within <strong>2–3 business days</strong>.",
        f'Questions? Your RCIC is <a href="mailto:{T("contact.case_assigned_rcic_email")}">{T("contact.case_assigned_rcic_email")}</a>.',
    ],
)
templates.append(render("18-cp-internal-review",
    f"🔍 {T('contact.first_name')}, your application is in final review",
    "3-step QA in progress.", "QUALITY REVIEW", html))

# 19 — WF-CP-05 Submitted!
html = build_welcome_style(
    subject=f"🚀 Submitted! Your IRCC receipt: {T('contact.ircc_receipt_number')}",
    preheader="Application submitted to IRCC. Receipt number + what to expect next.",
    h1="Submitted to IRCC!",
    body_paragraphs=[
        f"Your application has been officially submitted to Immigration, Refugees and Citizenship Canada. Congratulations on reaching this milestone, {T('contact.first_name')}!",
        f"<strong>IRCC Receipt Number:</strong> {T('contact.ircc_receipt_number')}<br>"
        f"<strong>Submission date:</strong> {T('contact.ircc_submission_date')}<br>"
        f"<strong>Program:</strong> {T('contact.case_program_type')}<br>"
        f"<strong>Expected processing time:</strong> {T('contact.case_estimated_months')} months",
        "<strong>What to expect now:</strong><br>"
        "• Week 1–2: IRCC acknowledgement of receipt (AOR)<br>"
        "• Month 1–3: Biometric instructions (if applicable)<br>"
        "• Month 3+: Possible request for additional information (RFI) or medical<br>"
        "• Processing end: Decision letter",
        f'<strong>Save your receipt number.</strong> You\'ll need it if you log into the <a href="https://ircc.canada.ca">IRCC portal</a> to check status.',
    ],
)
templates.append(render("19-cp-submitted",
    f"🚀 Submitted! Your IRCC receipt: {T('contact.ircc_receipt_number')}",
    "Application submitted to IRCC.", "MILESTONE", html))

# 20 — WF-CP-06 Monthly status
html = build_welcome_style(
    subject=f"📊 {T('nurture.month')} status — your IRCC application",
    preheader="Monthly status check + IRCC processing time tracker.",
    h1=f"Your case status — {T('nurture.month')} update",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, here's your monthly status update on your IRCC application.",
        f"<strong>Current stage:</strong> {T('contact.case_stage_friendly')}<br>"
        f"<strong>Time elapsed:</strong> {T('contact.days_since_submission')} days since submission<br>"
        f"<strong>Current IRCC average ({T('contact.case_program_type')}):</strong> {T('contact.ircc_current_average_months')} months<br>"
        f"<strong>Your estimated remaining:</strong> {T('contact.estimated_remaining_months')} months",
        f"<strong>What we're watching:</strong> {T('contact.monthly_watch_notes')}",
        "<strong>No action needed from you</strong> — IRCC is processing your file. We monitor daily and will reach out immediately if anything changes.",
    ],
)
templates.append(render("20-cp-status-update",
    f"📊 {T('nurture.month')} status — your IRCC application",
    "Monthly status check.", "STATUS UPDATE", html))

# 21 — WF-CP-07 RFI
html = build_action_style(
    subject="⚠️ URGENT: IRCC requested additional information",
    preheader=f"RFI received. Deadline {T('contact.rfi_deadline_date')}. Schedule a call.",
    h1="IRCC has requested additional information",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, IRCC has sent a request for information (RFI) on your file. This is a normal part of many applications — not a refusal or problem.",
        f"<strong>Response deadline:</strong> {T('contact.rfi_deadline_date')} — please respond as soon as possible. Missing the deadline can result in refusal.",
        f"<strong>What IRCC is asking for:</strong> {T('contact.rfi_request_summary')}",
        f"<strong>Case:</strong> {T('contact.case_id')}<br>"
        f"<strong>Deadline:</strong> {T('contact.rfi_deadline_date')}<br>"
        f"<strong>Days remaining:</strong> {T('contact.rfi_days_remaining')}",
    ],
    cta_text="Schedule an RFI call",
    cta_url=T('contact.rfi_booking_url'),
    post_cta_paragraphs=[
        "<strong>What happens next:</strong><br>"
        "• Your RCIC will call/email you to walk through the request (within 24h)<br>"
        "• Together you'll gather the requested documents<br>"
        "• We'll submit the response to IRCC on your behalf",
    ],
)
templates.append(render("21-cp-rfi", "⚠️ URGENT: IRCC requested additional information",
    "RFI received. Schedule a call.", "URGENT - RFI", html))

# 22 — Decision: APPROVED
html = build_action_style(
    subject=f"🎉 APPROVED — Congratulations, {T('contact.first_name')}!",
    preheader="IRCC approved your application. Next steps + testimonial request.",
    h1=f"APPROVED! Congratulations, {T('contact.first_name')}!",
    body_paragraphs=[
        "We are thrilled to share that IRCC has <strong>approved</strong> your application. This is the moment we've been working toward together.",
        f"<strong>Program:</strong> {T('contact.case_program_type')}<br>"
        f"<strong>Decision date:</strong> {T('contact.ircc_decision_date')}<br>"
        f"<strong>Next step:</strong> {T('contact.decision_next_step')}",
    ],
    cta_text="Download your decision package",
    cta_url=T('contact.decision_package_url'),
    post_cta_paragraphs=[
        "<strong>Next steps:</strong><br>"
        f"• {T('contact.next_step_1')}<br>"
        f"• {T('contact.next_step_2')}<br>"
        f"• {T('contact.next_step_3')}",
        f'<strong>We\'d love to celebrate your story.</strong> Would you consider sharing a short testimonial? It helps others with similar journeys. <a href="{T("contact.testimonial_url")}">Share my story →</a>',
        "Thank you for trusting us with your Canadian immigration journey. 🇨🇦",
    ],
)
templates.append(render("22-cp-decision-approved",
    f"🎉 APPROVED — Congratulations, {T('contact.first_name')}!",
    "IRCC approved your application.", "APPROVED", html))

# 23 — Decision: REFUSED
html = build_action_style(
    subject="Your IRCC decision — let's discuss",
    preheader="Application refused. We have options. Book a post-decision strategy call.",
    h1="Your IRCC decision — important update",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, IRCC has returned a decision on your application. Unfortunately, IRCC has <strong>refused</strong> the application.",
        "<strong>This is not the end.</strong> Many refusals can be overcome through reconsideration, judicial review, or a strengthened re-application. Your RCIC has already reviewed the refusal letter and has a plan.",
        f"<strong>Refusal reason (IRCC category):</strong> {T('contact.refusal_reason')}<br>"
        f"<strong>Decision date:</strong> {T('contact.ircc_decision_date')}<br>"
        f"<strong>Appeal deadline (if eligible):</strong> {T('contact.appeal_deadline_date')}",
        "<strong>Your options:</strong><br>"
        "• Reconsideration request — possible if decision appears procedurally incorrect<br>"
        "• Judicial review — Federal Court of Canada (60-day window)<br>"
        "• Re-application — with strengthened evidence addressing refusal reason",
    ],
    cta_text="Book a post-decision strategy call",
    cta_url=T('contact.strategy_call_url'),
    post_cta_paragraphs=[
        "<em>We stand with you. Our retainer includes one full post-decision consultation at no extra cost.</em>",
    ],
)
templates.append(render("23-cp-decision-refused", "Your IRCC decision — let's discuss",
    "Application refused. We have options.", "DECISION RECEIVED", html))

# 24 — Decision: WITHDRAWN
html = build_welcome_style(
    subject="📋 Your application withdrawal is confirmed",
    preheader="Withdrawal processed. Door is always open for re-application.",
    h1="Your withdrawal is confirmed",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, we've confirmed the withdrawal of your application to IRCC.",
        f"<strong>Program:</strong> {T('contact.case_program_type')}<br>"
        f"<strong>Withdrawal effective:</strong> {T('contact.ircc_decision_date')}<br>"
        f"<strong>IRCC fees refunded:</strong> {T('contact.ircc_refund_status')}",
        "<strong>Your options going forward:</strong><br>"
        "• Re-apply at any time when circumstances change<br>"
        "• Pursue a different Canadian immigration pathway<br>"
        "• Stay in our monthly nurture program (free)",
        'Explore other pathways: <a href="https://www.neuronx.co/intake/vmc/onboarding">book a fresh assessment</a>',
        "Whatever you decide, we're grateful you trusted us with part of your journey. The door is always open if you'd like to return.",
    ],
)
templates.append(render("24-cp-decision-withdrawn", "📋 Your application withdrawal is confirmed",
    "Withdrawal processed.", "WITHDRAWN", html))

# 25 — WF-CP-09 Case closed
html = build_action_style(
    subject="🏁 Your case is complete — final package inside",
    preheader="Case archive + how we can help again (family, citizenship, referrals).",
    h1="Your case is complete",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, your immigration case has been officially closed. Thank you for letting us be part of your journey.",
    ],
    cta_text="Download your complete case archive",
    cta_url=T('contact.case_archive_url'),
    post_cta_paragraphs=[
        "Your archive includes every form filed, every IRCC correspondence, and a PDF case summary — yours to keep forever.",
        "<strong>Stay in touch:</strong><br>"
        "• Family sponsorships: When you're ready to sponsor, we offer 25% off for existing clients<br>"
        "• Citizenship applications: Available 3 years after PR — we'll remind you<br>"
        f"• Referrals: <a href=\"{T('contact.referral_url')}\">Your referral link</a>",
        f'Would you share a quick Google review? <a href="{T("contact.review_url")}">Leave a review →</a>',
        "All the best in your Canadian chapter. 🇨🇦",
    ],
)
templates.append(render("25-cp-case-closed", "🏁 Your case is complete — final package inside",
    "Case archive + how we can help again.", "CASE CLOSED", html))

# 26 — Missed AI call recovery (WF-04C)
html = build_action_style(
    subject=f"📞 {T('contact.first_name')}, we tried calling — reply with 3 answers",
    preheader="5-minute readiness check missed. Reschedule OR just reply with 3 answers.",
    h1="We tried to call — quick rescheduling",
    body_paragraphs=[
        f"Hi {T('contact.first_name')}, our AI intake assistant tried calling to do a quick 5-minute readiness check, but didn't reach you.",
        "The assistant just gathers 5 quick details — program, location, timeline — so a licensed RCIC can best prepare for your consultation.",
    ],
    cta_text="Pick a call-back window",
    cta_url=f"https://www.neuronx.co/intake/vmc/onboarding?contact_id={T('contact.id')}",
    post_cta_paragraphs=[
        "Or if you prefer, just reply to this email with answers to these 3 questions:",
        "<strong>1.</strong> Which program interests you most? (Express Entry, Spousal Sponsorship, Work Permit, Study Permit, etc.)<br>"
        "<strong>2.</strong> Are you currently in Canada or outside?<br>"
        "<strong>3.</strong> What's your timeline? (Urgent / Within 3 months / 3–6 months / Longer)",
        "<em>We'll get you to a licensed RCIC as fast as possible.</em>",
    ],
)
templates.append(render("26-missed-ai-call",
    f"📞 {T('contact.first_name')}, we tried calling — reply with 3 answers",
    "5-minute readiness check missed.", "RESCHEDULE", html))

# Save manifest
(BASE_DIR / "manifest.json").write_text(json.dumps(templates, indent=2))

print(f"✓ Generated {len(templates)} templates using Postmark MIT-licensed base")
print(f"  Output: {OUT_DIR}/")
print(f"  Manifest: {BASE_DIR / 'manifest.json'}")
print()
for t in templates:
    print(f"  • {t['slug']}.html ({t['size']} bytes) — {t['subject'][:60]}")
