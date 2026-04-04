"""
Generate 8 program-specific nurture email templates for WF-11.
Uses the same unified VMC/NeuronX theme as Block 2B templates.
"""

import os

PROGRAMS = {
    "express-entry": {
        "title": "Express Entry",
        "emoji": "&#x1F4CA;",
        "subject": "Express Entry Update — New CRS Draws & Opportunities",
        "intro": "Express Entry remains one of the fastest pathways to Canadian permanent residency. Here are some updates relevant to your profile:",
        "bullets": [
            "Recent Express Entry draws have seen CRS cutoff scores adjust — new opportunities may have opened up for you",
            "Category-based selection rounds are now targeting specific occupations and French-language proficiency",
            "Processing times for most Express Entry applications are currently averaging 6-8 months",
            "Provincial Nominee Programs (PNPs) continue to offer additional pathways with lower CRS requirements",
        ],
        "cta_text": "Reassess My Express Entry Profile",
        "tip": "Your CRS score can change as IRCC adjusts program criteria. A quick reassessment takes just 15 minutes and could reveal new options.",
    },
    "spousal-sponsorship": {
        "title": "Spousal Sponsorship",
        "emoji": "&#x1F491;",
        "subject": "Spousal Sponsorship Update — Processing Times & Requirements",
        "intro": "Family reunification is a priority for IRCC. Here's what's new for spousal sponsorship applicants:",
        "bullets": [
            "Spousal sponsorship processing times are being reviewed — some applications are moving faster than expected",
            "Open work permits for sponsored spouses in Canada continue to be available during processing",
            "Proof of relationship requirements remain thorough — gather photos, communications, and joint financial documents early",
            "Common-law and conjugal partnerships have specific documentation requirements that differ from marriage-based applications",
        ],
        "cta_text": "Review My Sponsorship Eligibility",
        "tip": "Starting your document collection early is the single best thing you can do to avoid delays. Our team can provide a personalized checklist.",
    },
    "work-permit": {
        "title": "Work Permit",
        "emoji": "&#x1F4BC;",
        "subject": "Work Permit Update — New Pathways & Employer Programs",
        "intro": "Canada's work permit programs continue to evolve. Here's what matters for your situation:",
        "bullets": [
            "Employer-specific work permits remain the most common pathway — your job offer is key",
            "The Global Talent Stream offers expedited processing for certain tech and specialized occupations",
            "International Mobility Program (IMP) exemptions may apply depending on your country of citizenship",
            "LMIA-exempt work permit categories are expanding in some sectors like healthcare and trades",
        ],
        "cta_text": "Explore Work Permit Options",
        "tip": "Work permits often serve as a stepping stone to permanent residency. Understanding how your work experience contributes to future PR applications can be valuable.",
    },
    "study-permit": {
        "title": "Study Permit",
        "emoji": "&#x1F393;",
        "subject": "Study Permit Update — Program Changes & Opportunities",
        "intro": "Planning to study in Canada? The study permit landscape has some important developments:",
        "bullets": [
            "Designated Learning Institution (DLI) requirements continue to be enforced — verify your school's status",
            "Post-Graduation Work Permit (PGWP) eligibility depends on your program length and type",
            "Proof of financial support requirements may have been updated — confirm current amounts",
            "Study-to-PR pathways through Canadian Experience Class remain available after gaining Canadian work experience",
        ],
        "cta_text": "Plan My Study Pathway",
        "tip": "Choosing the right program and institution can significantly impact your post-graduation immigration options. A 15-minute consultation can help you plan ahead.",
    },
    "lmia": {
        "title": "LMIA",
        "emoji": "&#x1F3E2;",
        "subject": "LMIA Update — Employer Requirements & Processing Changes",
        "intro": "If your immigration pathway involves an employer-sponsored LMIA, here are relevant updates:",
        "bullets": [
            "Labour Market Impact Assessment processing times vary by stream — some categories are moving faster",
            "Advertising requirements for employers remain strict — proper documentation is essential",
            "Wage requirements are tied to prevailing wage data that updates periodically",
            "Certain LMIA-exempt categories may apply, potentially simplifying your employer's process",
        ],
        "cta_text": "Review My LMIA Requirements",
        "tip": "LMIA applications require coordination between you and your employer. We can guide both parties through the process to avoid common pitfalls.",
    },
    "pr-renewal": {
        "title": "PR Renewal",
        "emoji": "&#x1F4C4;",
        "subject": "PR Card Renewal — Important Residency Obligation Reminder",
        "intro": "Maintaining your permanent resident status requires meeting residency obligations. Here's what to keep in mind:",
        "bullets": [
            "You must have been physically present in Canada for at least 730 days in the last 5 years",
            "PR card processing times have been fluctuating — apply well before your card expires if you plan to travel",
            "Travel documents (PRTD) are available if your PR card expires while you're outside Canada",
            "Time spent outside Canada may count toward residency obligations in certain circumstances (e.g., accompanying a Canadian citizen spouse)",
        ],
        "cta_text": "Check My Residency Obligation",
        "tip": "Keep detailed records of your travel history. Immigration Canada may request proof of your physical presence in Canada at any time.",
    },
    "citizenship": {
        "title": "Citizenship",
        "emoji": "&#x1F1E8;&#x1F1E6;",
        "subject": "Canadian Citizenship — Eligibility Updates & Test Prep",
        "intro": "Becoming a Canadian citizen is a significant milestone. Here's what's current:",
        "bullets": [
            "Physical presence requirements: 1,095 days in the last 5 years as a PR",
            "Language requirements: CLB Level 4 or higher in English or French for applicants aged 18-54",
            "The citizenship test covers Canadian history, geography, rights, and responsibilities",
            "Processing times vary — current average timelines can be checked on the IRCC website",
        ],
        "cta_text": "Assess My Citizenship Eligibility",
        "tip": "You can use time as a temporary resident or protected person toward your citizenship requirement (up to 365 days, counting as half days).",
    },
    "visitor-visa": {
        "title": "Visitor Visa",
        "emoji": "&#x2708;&#xFE0F;",
        "subject": "Visitor Visa Update — Application Tips & Processing Times",
        "intro": "Planning to visit Canada? Here are updates for visitor visa applicants:",
        "bullets": [
            "Temporary Resident Visa (TRV) processing times vary by country of residence",
            "Strong ties to your home country (job, property, family) remain the most important factor",
            "Super Visa for parents and grandparents offers multi-year, multi-entry access with extended stays",
            "Electronic Travel Authorization (eTA) may be sufficient if you're from a visa-exempt country",
        ],
        "cta_text": "Check If I Need a Visitor Visa",
        "tip": "A well-prepared application with clear purpose of travel and proof of ties to your home country significantly increases approval chances.",
    },
}


def build_template(key, program):
    booking_url = "https://api.leadconnectorhq.com/widget/booking/To1U2KbcvJ0EAX0RGKHS"

    bullets_html = "".join(
        f'<li style="margin-bottom:8px;">{b}</li>' for b in program["bullets"]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#f0f0f0;font-family:'Inter','Helvetica Neue',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f0f0;padding:32px 16px;">
<tr><td align="center">

<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.08);">

  <!-- Header -->
  <tr><td style="background:#E8380D;padding:28px 32px;text-align:center;">
    <p style="margin:0 0 8px;font-size:28px;">{program["emoji"]}</p>
    <h1 style="margin:0;font-size:20px;color:#ffffff;font-weight:700;">{program["title"]} Update</h1>
    <p style="margin:6px 0 0;font-size:13px;color:rgba(255,255,255,0.8);">Monthly Insights from Visa Master Canada</p>
  </td></tr>

  <!-- Body -->
  <tr><td style="padding:32px;">
    <p style="margin:0 0 16px;font-size:15px;color:#333;line-height:1.7;">Hi {{{{contact.first_name}}}},</p>

    <p style="margin:0 0 16px;font-size:15px;color:#333;line-height:1.7;">{program["intro"]}</p>

    <!-- Updates box -->
    <table width="100%" cellpadding="14" cellspacing="0" style="background:#f0fdf4;border-left:4px solid #16a34a;border-radius:4px;margin:20px 0;">
    <tr><td>
      <p style="margin:0 0 8px;font-size:14px;font-weight:600;color:#16a34a;">What's New:</p>
      <ul style="margin:0;padding-left:18px;font-size:14px;color:#333;line-height:1.8;">{bullets_html}</ul>
    </td></tr>
    </table>

    <!-- Tip box -->
    <table width="100%" cellpadding="14" cellspacing="0" style="background:#FFF7ED;border-left:4px solid #E8380D;border-radius:4px;margin:20px 0;">
    <tr><td>
      <p style="margin:0;font-size:14px;color:#333;line-height:1.7;"><strong style="color:#E8380D;">Tip:</strong> {program["tip"]}</p>
    </td></tr>
    </table>

    <!-- CTA -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:24px 0;">
    <tr><td align="center">
      <a href="{booking_url}" style="display:inline-block;background-color:#E8380D;color:#ffffff;font-size:15px;font-weight:600;text-decoration:none;padding:14px 36px;border-radius:6px;">{program["cta_text"]}</a>
    </td></tr>
    </table>

    <p style="margin:24px 0 0;font-size:15px;color:#333;line-height:1.7;">
      Warm regards,<br>
      <strong>The Visa Master Canada Team</strong><br>
      <span style="font-size:13px;color:#666;">Licensed Immigration Consulting</span>
    </p>
  </td></tr>

  <!-- Footer -->
  <tr><td style="background:#f9f9f9;padding:16px 32px;border-top:1px solid #e5e5e5;">
    <p style="margin:0;font-size:12px;color:#999;text-align:center;line-height:1.6;">
      Visa Master Canada &bull; Licensed Immigration Consulting<br>
      You're receiving this because you previously inquired about {program["title"].lower()} services.<br>
      <a href="{{{{unsubscribe_link}}}}" style="color:#999;text-decoration:underline;">Unsubscribe</a> &bull;
      <a href="mailto:rcic@neuronx.co" style="color:#999;text-decoration:underline;">Contact Us</a>
    </p>
  </td></tr>

</table>
</td></tr></table>
</body></html>"""


# Generate all 8
output_dir = os.path.dirname(os.path.abspath(__file__))
for key, program in PROGRAMS.items():
    filename = f"{key}.html"
    filepath = os.path.join(output_dir, filename)
    html = build_template(key, program)
    with open(filepath, "w") as f:
        f.write(html)
    print(f"  {filename} ({len(html)} chars)")

print(f"\nGenerated {len(PROGRAMS)} nurture templates in {output_dir}/")
