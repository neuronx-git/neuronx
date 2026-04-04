"""
Document Generation Service

Uses python-docx-template (docxtpl) to generate .docx files from templates.
Templates live in /templates/ with Jinja2 variables ({{ variable_name }}).

Current templates:
- retainer_agreement.docx (17 variables) — retainer engagement letter
- assessment_report.docx (10 variables) — pre-consultation assessment

For Documenso integration (Block 2):
- Generate .docx → convert to PDF → send to Documenso API for e-signing
"""

import logging
from pathlib import Path
from io import BytesIO
from datetime import datetime, timezone
from typing import Optional

from app.services.ghl_client import GHLClient
from app.config_loader import load_yaml_config

logger = logging.getLogger("neuronx.documents")

TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


class DocumentService:
    """Generates .docx documents from templates using client data."""

    def __init__(self):
        self.firm_config = load_yaml_config("ircc_field_mappings").get("firm_defaults", {})

    async def generate_retainer(self, contact_id: str, retainer_amount: float = 3500.0,
                                 payment_schedule: str = "50% upfront, 50% on submission",
                                 hourly_rate: float = 350.0) -> Optional[bytes]:
        """
        Generate a retainer agreement .docx for a client.
        Pulls client data from GHL, fills the template, returns bytes.
        """
        try:
            from docxtpl import DocxTemplate
        except ImportError:
            logger.error("docxtpl not installed")
            return None

        template_path = TEMPLATES_DIR / "retainer_agreement.docx"
        if not template_path.exists():
            logger.error("Retainer template not found: %s", template_path)
            return None

        # Fetch client data from GHL
        ghl = GHLClient()
        contact = await ghl.get_contact(contact_id)

        # Extract custom fields
        custom = {}
        for field in contact.get("customFields", []):
            custom[field.get("id", "")] = field.get("value", "")

        # Determine program type
        program = ""
        for key, val in custom.items():
            if "program_interest" in key.lower():
                program = val
                break

        # Get processing times
        programs_config = load_yaml_config("programs")
        prog_data = programs_config.get("programs", {}).get(program, {})
        proc_times = prog_data.get("processing_months", {"min": 3, "max": 12})

        # Build scope description
        scope_map = {
            "Express Entry": "Federal Skilled Worker / Canadian Experience Class permanent residence application through IRCC Express Entry system",
            "Spousal Sponsorship": "Family class sponsorship application for spouse/common-law partner through IRCC",
            "Work Permit": "Temporary work permit application through IRCC",
            "Study Permit": "Study permit application through IRCC",
            "LMIA": "Labour Market Impact Assessment application through ESDC",
            "PR Renewal": "Permanent Resident card renewal through IRCC",
            "Citizenship": "Canadian citizenship application through IRCC",
            "Visitor Visa": "Temporary Resident Visa application through IRCC",
        }

        context = {
            "firm_name": self.firm_config.get("firm_name", "Immigration Consulting Services"),
            "rcic_license": self.firm_config.get("rcic_license", ""),
            "firm_address": self.firm_config.get("firm_address", ""),
            "firm_email": self.firm_config.get("firm_email", ""),
            "client_name": f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip(),
            "client_address": contact.get("address1", ""),
            "client_email": contact.get("email", ""),
            "client_phone": contact.get("phone", ""),
            "program_type": program,
            "scope_description": scope_map.get(program, f"{program} immigration application"),
            "retainer_amount": f"${retainer_amount:,.2f} CAD",
            "payment_schedule": payment_schedule,
            "processing_min": proc_times.get("min", 3),
            "processing_max": proc_times.get("max", 12),
            "hourly_rate": f"${hourly_rate:,.2f} CAD",
            "generated_date": datetime.now(tz=timezone.utc).strftime("%B %d, %Y"),
        }

        doc = DocxTemplate(str(template_path))
        doc.render(context)

        output = BytesIO()
        doc.save(output)
        output.seek(0)

        logger.info("Generated retainer agreement for %s (%s)", contact_id, program)
        return output.read()

    async def generate_assessment(self, contact_id: str) -> Optional[bytes]:
        """
        Generate an assessment report .docx for a client.
        Pulls scoring data from GHL custom fields.
        """
        try:
            from docxtpl import DocxTemplate
        except ImportError:
            logger.error("docxtpl not installed")
            return None

        template_path = TEMPLATES_DIR / "assessment_report.docx"
        if not template_path.exists():
            logger.error("Assessment template not found: %s", template_path)
            return None

        ghl = GHLClient()
        contact = await ghl.get_contact(contact_id)

        custom = {}
        for field in contact.get("customFields", []):
            custom[field.get("id", "")] = field.get("value", "")

        # Extract scoring fields
        score = 0
        outcome = "pending"
        program = ""
        for key, val in custom.items():
            if "readiness_score" in key.lower():
                try:
                    score = int(val)
                except (ValueError, TypeError):
                    pass
            elif "readiness_outcome" in key.lower():
                outcome = val
            elif "program_interest" in key.lower():
                program = val

        # Score tier
        if score >= 70:
            tier = "High"
        elif score >= 40:
            tier = "Medium"
        else:
            tier = "Low"

        # Get program checklist
        programs_config = load_yaml_config("programs")
        prog_data = programs_config.get("programs", {}).get(program, {})
        proc_times = prog_data.get("processing_months", {"min": 3, "max": 12})
        required_docs = prog_data.get("required_documents", [])

        context = {
            "client_name": f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip(),
            "client_email": contact.get("email", ""),
            "client_phone": contact.get("phone", ""),
            "assessment_date": datetime.now(tz=timezone.utc).strftime("%B %d, %Y"),
            "readiness_score": score,
            "score_tier": tier,
            "readiness_outcome": outcome,
            "flags_text": "None" if score >= 70 else "Review recommended",
            "r1_program_interest": program,
            "required_documents_text": "\n".join(f"- {doc}" for doc in required_docs) if required_docs else "To be determined during consultation",
            "processing_min": proc_times.get("min", 3),
            "processing_max": proc_times.get("max", 12),
            "generated_date": datetime.now(tz=timezone.utc).strftime("%B %d, %Y"),
        }

        doc = DocxTemplate(str(template_path))
        doc.render(context)

        output = BytesIO()
        doc.save(output)
        output.seek(0)

        logger.info("Generated assessment report for %s (score: %d)", contact_id, score)
        return output.read()
