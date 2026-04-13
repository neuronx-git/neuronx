"""
IRCC Form Auto-Population Service

Fills official IRCC PDF forms with client data from the onboarding questionnaire.
Uses pypdf to read/write AcroForm fields in government PDFs.

Architecture:
1. Official IRCC PDFs stored in templates/ircc/ (downloaded once from canada.ca)
2. Field mappings in config/ircc_field_mappings.yaml (questionnaire key → PDF field name)
3. Client data from GHL custom fields or questionnaire submission
4. Output: filled PDF bytes ready for download or Documenso signing

When IRCC changes a form:
1. Download new PDF to templates/ircc/
2. Run field discovery: python3 -c "from pypdf import PdfReader; print(PdfReader('form.pdf').get_form_text_fields())"
3. Update config/ircc_field_mappings.yaml with new field names
4. Push → auto-deploy. No code changes.
"""

import logging
from pathlib import Path
from typing import Optional
from io import BytesIO

from app.config_loader import load_yaml_config

logger = logging.getLogger("neuronx.ircc_forms")

TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates" / "ircc"


class IRCCFormService:
    """Fills IRCC PDF forms with client questionnaire data."""

    def __init__(self):
        self.config = load_yaml_config("ircc_field_mappings")
        self.common_fields = self.config.get("common_fields", {})
        self.forms = self.config.get("forms", {})
        self.transformers = self.config.get("transformers", {})
        self.firm_defaults = self.config.get("firm_defaults", {})

    def list_available_forms(self, program_type: str) -> list:
        """List IRCC forms available for auto-fill for a given program."""
        available = []
        for form_key, form_config in self.forms.items():
            if program_type in form_config.get("programs", []):
                pdf_path = TEMPLATES_DIR / f"{form_key}.pdf"
                available.append({
                    "form_key": form_key,
                    "form_code": form_config["form_code"],
                    "form_name": form_config["form_name"],
                    "source_url": form_config.get("source_url", ""),
                    "pdf_available": pdf_path.exists(),
                    "notes": form_config.get("notes", ""),
                })
        return available

    def discover_pdf_fields(self, form_key: str) -> dict:
        """Discover fillable field names in an IRCC PDF. Used for mapping setup."""
        try:
            from pypdf import PdfReader
        except ImportError:
            return {"error": "pypdf not installed. Run: pip install pypdf"}

        pdf_path = TEMPLATES_DIR / f"{form_key}.pdf"
        if not pdf_path.exists():
            return {"error": f"PDF not found: {pdf_path}"}

        reader = PdfReader(str(pdf_path))
        fields = {}

        if reader.get_form_text_fields():
            fields["text_fields"] = reader.get_form_text_fields()

        # Also check for all field types
        if reader.get_fields():
            all_fields = {}
            for name, field in reader.get_fields().items():
                all_fields[name] = {
                    "type": str(field.get("/FT", "Unknown")),
                    "value": str(field.get("/V", "")),
                }
            fields["all_fields"] = all_fields

        fields["total_pages"] = len(reader.pages)
        return fields

    def fill_form(self, form_key: str, client_data: dict) -> Optional[bytes]:
        """
        Fill an IRCC PDF form with client data.

        Args:
            form_key: e.g., "IMM_0008"
            client_data: dict of questionnaire answers (keys match questionnaires.yaml)

        Returns:
            Filled PDF as bytes, or None if form not available.
        """
        try:
            from pypdf import PdfReader, PdfWriter
        except ImportError:
            logger.error("pypdf not installed")
            return None

        pdf_path = TEMPLATES_DIR / f"{form_key}.pdf"
        if not pdf_path.exists():
            logger.warning("IRCC PDF template not found: %s", pdf_path)
            return None

        form_config = self.forms.get(form_key)
        if not form_config:
            logger.warning("No field mapping for form: %s", form_key)
            return None

        field_mappings = form_config.get("field_mappings", {})

        # Build fill data: questionnaire key → PDF field name → value
        fill_data = {}

        for q_key, pdf_field_name in field_mappings.items():
            value = client_data.get(q_key, "")
            if value:
                # Apply transformer if exists
                value = self._transform_value(q_key, value)
                fill_data[pdf_field_name] = value

        # Add firm defaults for representative forms
        if form_key == "IMM_5476":
            for firm_key, firm_value in self.firm_defaults.items():
                # Map firm defaults to common representative field names
                firm_field_map = {
                    "firm_name": "RepFirmName",
                    "rcic_name": "RepName",
                    "rcic_license": "RepMemberID",
                    "firm_address": "RepAddress",
                    "firm_phone": "RepPhone",
                    "firm_email": "RepEmail",
                }
                if firm_key in firm_field_map:
                    fill_data[firm_field_map[firm_key]] = firm_value

        if not fill_data:
            logger.warning("No data to fill for form %s", form_key)
            return None

        # Fill the PDF (with encrypted form fallback)
        try:
            reader = PdfReader(str(pdf_path))

            # Try to decrypt if encrypted (IRCC forms often have owner password)
            if reader.is_encrypted:
                try:
                    reader.decrypt("")  # Try empty password (common for IRCC forms)
                    logger.info("Decrypted %s with empty password", form_key)
                except Exception as de:
                    logger.warning("Cannot decrypt %s (%s) — generating data sheet instead", form_key, de)
                    return self._generate_data_sheet(form_key, form_config, fill_data)

            # Check if form has fillable fields
            if not reader.get_form_text_fields() and not reader.get_fields():
                logger.warning("No fillable fields in %s — generating data sheet", form_key)
                return self._generate_data_sheet(form_key, form_config, fill_data)

            writer = PdfWriter()
            writer.clone_reader_document_root(reader)

            # Update form fields
            for page in writer.pages:
                writer.update_page_form_field_values(page, fill_data)

            # Write to bytes
            output = BytesIO()
            writer.write(output)
            output.seek(0)

            logger.info("Filled IRCC form %s with %d fields", form_key, len(fill_data))
            return output.read()

        except Exception as e:
            logger.warning("Failed to fill %s directly (%s) — generating data sheet", form_key, e)
            return self._generate_data_sheet(form_key, form_config, fill_data)

    def _generate_data_sheet(self, form_key: str, form_config: dict, fill_data: dict) -> bytes:
        """
        Generate a printable HTML data sheet when PDF auto-fill fails.
        The RCIC uses this as a reference to manually fill the encrypted form.
        Saves 20-30 minutes per form vs looking up each value.
        """
        form_code = form_config.get("form_code", form_key)
        form_name = form_config.get("form_name", "")

        rows = ""
        for pdf_field, value in fill_data.items():
            rows += f"<tr><td style='padding:8px;border:1px solid #ddd;font-weight:600'>{pdf_field}</td><td style='padding:8px;border:1px solid #ddd'>{value}</td></tr>\n"

        html = f"""<!DOCTYPE html>
<html>
<head><meta charset='utf-8'><title>{form_code} — Pre-filled Data Sheet</title></head>
<body style='font-family:Inter,Arial,sans-serif;max-width:800px;margin:40px auto;padding:20px'>
<div style='background:#4F46E5;color:white;padding:20px;border-radius:8px;margin-bottom:24px'>
  <h1 style='margin:0;font-size:24px'>NeuronX — IRCC Form Data Sheet</h1>
  <p style='margin:8px 0 0;opacity:0.9'>Auto-generated from client questionnaire</p>
</div>
<table style='width:100%;margin-bottom:16px'>
  <tr><td><strong>Form:</strong> {form_code} — {form_name}</td></tr>
  <tr><td><strong>Generated:</strong> {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')} UTC</td></tr>
  <tr><td style='color:#E53E3E'><strong>Note:</strong> This form is encrypted and cannot be auto-filled. Use these values to manually complete the PDF.</td></tr>
</table>
<table style='width:100%;border-collapse:collapse;margin-top:16px'>
  <thead><tr style='background:#F3F4F6'>
    <th style='padding:8px;border:1px solid #ddd;text-align:left'>PDF Field Name</th>
    <th style='padding:8px;border:1px solid #ddd;text-align:left'>Value</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>
<p style='color:#666;font-size:12px;margin-top:24px'>Generated by NeuronX. Download the original form from canada.ca and fill using these values.</p>
</body></html>"""

        return html.encode("utf-8")

    def fill_all_forms(self, program_type: str, client_data: dict) -> list:
        """
        Fill ALL required IRCC forms for a program.

        Returns list of dicts with form_code, form_name, and filled PDF bytes.
        Only returns forms that have PDF templates available.
        """
        results = []
        for form_key, form_config in self.forms.items():
            if program_type not in form_config.get("programs", []):
                continue

            pdf_bytes = self.fill_form(form_key, client_data)
            if pdf_bytes:
                results.append({
                    "form_key": form_key,
                    "form_code": form_config["form_code"],
                    "form_name": form_config["form_name"],
                    "pdf_bytes": pdf_bytes,
                    "size_bytes": len(pdf_bytes),
                })
            else:
                results.append({
                    "form_key": form_key,
                    "form_code": form_config["form_code"],
                    "form_name": form_config["form_name"],
                    "pdf_bytes": None,
                    "error": "PDF template not available or no matching data",
                })

        return results

    def _transform_value(self, key: str, value) -> str:
        """Apply value transformers (e.g., marital status code mapping)."""
        if key == "marital_status" and "marital_status" in self.transformers:
            return self.transformers["marital_status"].get(str(value), str(value))

        if isinstance(value, bool):
            bool_map = self.transformers.get("boolean_to_yesno", {})
            return bool_map.get(value, str(value))

        return str(value)

    def get_mapping_coverage(self, form_key: str, client_data: dict) -> dict:
        """
        Check how many form fields can be filled with available client data.
        Useful for showing completion percentage to RCIC.
        """
        form_config = self.forms.get(form_key)
        if not form_config:
            return {"error": f"Unknown form: {form_key}"}

        field_mappings = form_config.get("field_mappings", {})
        total = len(field_mappings)
        filled = sum(1 for q_key in field_mappings if client_data.get(q_key))

        return {
            "form_code": form_config["form_code"],
            "total_fields": total,
            "fillable_from_data": filled,
            "coverage_percent": round((filled / total * 100) if total > 0 else 0),
            "missing_fields": [q_key for q_key in field_mappings if not client_data.get(q_key)],
        }
