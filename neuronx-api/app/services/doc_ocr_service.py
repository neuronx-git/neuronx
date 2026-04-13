"""
Document OCR Extraction Service

Hybrid approach:
1. Passport: FastMRZ (free, unlimited) — extracts from MRZ strip
2. All other documents: Claude API structured extraction — extracts relevant fields

Flow:
  Client uploads document → detect type → extract fields → return structured JSON
  Fields are then used to auto-fill GHL custom fields and form inputs.

No per-page cost. FastMRZ is open-source. Claude API uses existing Anthropic key.
"""

import logging
import base64
import json
import tempfile
import os
from pathlib import Path
from typing import Optional

import httpx
from app.config import settings

logger = logging.getLogger("neuronx.doc_ocr")


# Document type definitions with extraction prompts
DOCUMENT_TYPES = {
    "passport": {
        "label": "Passport",
        "method": "fastmrz",
        "fields": ["full_name", "date_of_birth", "passport_number", "passport_expiry", "nationality", "sex"],
    },
    "ielts": {
        "label": "IELTS / CELPIP Score Sheet",
        "method": "claude",
        "fields": ["listening_score", "reading_score", "writing_score", "speaking_score", "overall_score", "test_date", "candidate_name"],
        "prompt": (
            "Extract the following from this IELTS or CELPIP language test score sheet. "
            "Return ONLY a JSON object with these fields:\n"
            "- candidate_name: full name of the test taker\n"
            "- listening_score: numeric score\n"
            "- reading_score: numeric score\n"
            "- writing_score: numeric score\n"
            "- speaking_score: numeric score\n"
            "- overall_score: overall band/CLB score\n"
            "- test_date: date of test (YYYY-MM-DD format)\n"
            "- test_type: IELTS General / IELTS Academic / CELPIP General\n"
            "If a field is not visible, set it to null."
        ),
    },
    "eca": {
        "label": "Educational Credential Assessment (ECA)",
        "method": "claude",
        "fields": ["organization", "credential_level", "canadian_equivalent", "assessment_date", "reference_number"],
        "prompt": (
            "Extract the following from this Educational Credential Assessment (ECA) certificate. "
            "Return ONLY a JSON object with these fields:\n"
            "- candidate_name: full name\n"
            "- organization: assessing organization (WES, IQAS, CES, etc.)\n"
            "- credential_level: original credential (e.g., Bachelor's Degree)\n"
            "- canadian_equivalent: Canadian equivalent (e.g., Bachelor's Degree - Four-Year)\n"
            "- assessment_date: date (YYYY-MM-DD format)\n"
            "- reference_number: ECA reference/report number\n"
            "If a field is not visible, set it to null."
        ),
    },
    "employment_letter": {
        "label": "Employment / Reference Letter",
        "method": "claude",
        "fields": ["employer_name", "job_title", "noc_code", "start_date", "end_date", "hours_per_week", "salary"],
        "prompt": (
            "Extract the following from this employment or reference letter. "
            "Return ONLY a JSON object with these fields:\n"
            "- employee_name: full name of the employee\n"
            "- employer_name: company/organization name\n"
            "- job_title: position/title held\n"
            "- noc_code: NOC code if mentioned (null if not)\n"
            "- start_date: employment start date (YYYY-MM-DD)\n"
            "- end_date: employment end date or 'Present' (YYYY-MM-DD)\n"
            "- hours_per_week: weekly hours if mentioned\n"
            "- salary: salary/wage if mentioned\n"
            "- duties: brief list of main duties/responsibilities\n"
            "If a field is not visible, set it to null."
        ),
    },
    "marriage_certificate": {
        "label": "Marriage Certificate",
        "method": "claude",
        "fields": ["spouse1_name", "spouse2_name", "marriage_date", "jurisdiction"],
        "prompt": (
            "Extract the following from this marriage certificate. "
            "Return ONLY a JSON object with these fields:\n"
            "- spouse1_name: full name of first spouse\n"
            "- spouse2_name: full name of second spouse\n"
            "- marriage_date: date of marriage (YYYY-MM-DD)\n"
            "- jurisdiction: city/province/country where married\n"
            "- certificate_number: registration/certificate number\n"
            "If a field is not visible, set it to null."
        ),
    },
    "bank_statement": {
        "label": "Bank Statement / Proof of Funds",
        "method": "claude",
        "fields": ["account_holder", "institution", "balance", "currency", "statement_date"],
        "prompt": (
            "Extract the following from this bank statement or proof of funds. "
            "Return ONLY a JSON object with these fields:\n"
            "- account_holder: name on the account\n"
            "- institution: bank/financial institution name\n"
            "- balance: current balance (numeric, no currency symbol)\n"
            "- currency: currency code (CAD, USD, INR, etc.)\n"
            "- statement_date: date of statement (YYYY-MM-DD)\n"
            "If a field is not visible, set it to null."
        ),
    },
    "police_clearance": {
        "label": "Police Clearance Certificate",
        "method": "claude",
        "fields": ["applicant_name", "country", "issue_date", "result"],
        "prompt": (
            "Extract the following from this police clearance or criminal record check certificate. "
            "Return ONLY a JSON object with these fields:\n"
            "- applicant_name: full name\n"
            "- country: issuing country\n"
            "- issue_date: date issued (YYYY-MM-DD)\n"
            "- result: result (e.g., 'No criminal record', 'Clear', etc.)\n"
            "- certificate_number: reference number if visible\n"
            "If a field is not visible, set it to null."
        ),
    },
    "general": {
        "label": "General Document",
        "method": "claude",
        "fields": [],
        "prompt": (
            "This is an immigration-related document. Extract ALL relevant personal information "
            "and document details. Return ONLY a JSON object with any fields you find, such as:\n"
            "- document_type: what type of document this is\n"
            "- person_name: name of the person\n"
            "- dates: any relevant dates\n"
            "- numbers: any reference/ID numbers\n"
            "- key_details: other important information\n"
            "Be thorough but only extract factual data visible in the document."
        ),
    },
}


class DocOCRService:
    """Extracts structured data from uploaded immigration documents."""

    async def extract(self, file_bytes: bytes, filename: str, doc_type: str = "auto") -> dict:
        """
        Extract structured data from a document.

        Args:
            file_bytes: Raw file content (PDF, JPG, PNG)
            filename: Original filename
            doc_type: Document type hint (passport, ielts, eca, etc.) or "auto"

        Returns:
            Dict with extracted fields, confidence, and doc_type
        """
        # Auto-detect document type from filename if not specified
        if doc_type == "auto":
            doc_type = self._detect_type(filename)

        config = DOCUMENT_TYPES.get(doc_type, DOCUMENT_TYPES["general"])
        method = config["method"]

        logger.info("Extracting from %s (type=%s, method=%s, size=%d bytes)",
                     filename, doc_type, method, len(file_bytes))

        if method == "fastmrz":
            result = await self._extract_passport(file_bytes, filename)
        else:
            result = await self._extract_with_claude(file_bytes, filename, config)

        result["doc_type"] = doc_type
        result["doc_type_label"] = config["label"]
        result["filename"] = filename

        return result

    def _detect_type(self, filename: str) -> str:
        """Guess document type from filename."""
        name = filename.lower()
        if any(w in name for w in ["passport", "passeport"]):
            return "passport"
        if any(w in name for w in ["ielts", "celpip", "tef", "tcf", "language"]):
            return "ielts"
        if any(w in name for w in ["eca", "wes", "iqas", "credential"]):
            return "eca"
        if any(w in name for w in ["employ", "reference", "job", "work"]):
            return "employment_letter"
        if any(w in name for w in ["marriage", "wedding", "union"]):
            return "marriage_certificate"
        if any(w in name for w in ["bank", "statement", "funds", "balance"]):
            return "bank_statement"
        if any(w in name for w in ["police", "clearance", "criminal", "pcc"]):
            return "police_clearance"
        return "general"

    async def _extract_passport(self, file_bytes: bytes, filename: str) -> dict:
        """Extract passport data using FastMRZ (free, unlimited)."""
        try:
            from fastmrz import FastMRZ

            # Save to temp file (FastMRZ needs file path)
            suffix = Path(filename).suffix or ".jpg"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            try:
                mrz = FastMRZ()
                result = mrz.get_mrz(tmp_path)

                if not result:
                    logger.warning("FastMRZ: No MRZ found in %s", filename)
                    # Fall back to Claude for non-MRZ passport images
                    return await self._extract_with_claude(
                        file_bytes, filename, DOCUMENT_TYPES["general"]
                    )

                # Map MRZ fields to our form fields
                extracted = {
                    "full_name": f"{result.get('given_name', '')} {result.get('surname', '')}".strip(),
                    "date_of_birth": result.get("date_of_birth", ""),
                    "passport_number": result.get("document_number", ""),
                    "passport_expiry": result.get("expiry_date", ""),
                    "country_of_citizenship": result.get("nationality", ""),
                    "sex": result.get("sex", ""),
                }

                # Clean up empty values
                extracted = {k: v for k, v in extracted.items() if v}

                return {
                    "method": "fastmrz",
                    "extracted_fields": extracted,
                    "field_count": len(extracted),
                    "confidence": "high" if len(extracted) >= 4 else "medium",
                    "raw_mrz": result,
                }
            finally:
                os.unlink(tmp_path)

        except Exception as e:
            logger.error("FastMRZ extraction failed: %s — falling back to Claude", e)
            return await self._extract_with_claude(
                file_bytes, filename, DOCUMENT_TYPES["general"]
            )

    async def _extract_with_claude(self, file_bytes: bytes, filename: str, config: dict) -> dict:
        """Extract document data using Claude API vision (any document type)."""
        api_key = settings.anthropic_api_key
        if not api_key:
            return {
                "method": "claude",
                "error": "Anthropic API key not configured",
                "extracted_fields": {},
                "field_count": 0,
                "confidence": "none",
            }

        # Determine media type
        suffix = Path(filename).suffix.lower()
        media_types = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".gif": "image/gif",
            ".webp": "image/webp", ".pdf": "application/pdf",
        }
        media_type = media_types.get(suffix, "image/jpeg")

        # Encode file as base64
        b64_data = base64.b64encode(file_bytes).decode("utf-8")

        # Build Claude API request with vision
        prompt = config.get("prompt", DOCUMENT_TYPES["general"]["prompt"])

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": settings.briefing_model or "claude-sonnet-4-6",
                        "max_tokens": 1024,
                        "messages": [{
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": media_type,
                                        "data": b64_data,
                                    },
                                },
                                {
                                    "type": "text",
                                    "text": prompt,
                                },
                            ],
                        }],
                    },
                )

            if response.status_code != 200:
                logger.error("Claude API error: %d — %s", response.status_code, response.text[:200])
                return {
                    "method": "claude",
                    "error": f"Claude API error: {response.status_code}",
                    "extracted_fields": {},
                    "field_count": 0,
                    "confidence": "none",
                }

            result = response.json()
            content = result.get("content", [{}])[0].get("text", "")

            # Parse JSON from Claude's response
            extracted = self._parse_json_from_response(content)

            return {
                "method": "claude",
                "extracted_fields": extracted,
                "field_count": len(extracted),
                "confidence": "high" if len(extracted) >= 3 else "medium" if extracted else "low",
            }

        except Exception as e:
            logger.error("Claude extraction failed: %s", e)
            return {
                "method": "claude",
                "error": str(e),
                "extracted_fields": {},
                "field_count": 0,
                "confidence": "none",
            }

    def _parse_json_from_response(self, text: str) -> dict:
        """Extract JSON object from Claude's response text."""
        # Try direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try finding JSON in markdown code block
        if "```json" in text:
            start = text.index("```json") + 7
            end = text.index("```", start)
            try:
                return json.loads(text[start:end].strip())
            except (json.JSONDecodeError, ValueError):
                pass

        # Try finding any {...} block
        if "{" in text and "}" in text:
            start = text.index("{")
            end = text.rindex("}") + 1
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass

        logger.warning("Could not parse JSON from Claude response: %s", text[:200])
        return {}

    def get_supported_types(self) -> list:
        """Return list of supported document types with labels."""
        return [
            {"type": key, "label": config["label"], "fields": config["fields"]}
            for key, config in DOCUMENT_TYPES.items()
            if key != "general"
        ]
