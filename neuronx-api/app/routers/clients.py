"""
Client Data Endpoints (for Chrome Extension + Data Sheets)
GET  /clients/{contact_id}/form-data    — Client data mapped for IRCC form filling
GET  /clients/{contact_id}/data-sheet   — Full data sheet organized by IRCC sections
GET  /clients/{contact_id}/validate     — Pre-submission completeness validation
GET  /clients/{contact_id}/copy-paste   — Copy-paste-ready text for IRCC portal
GET  /clients/search                    — Search clients by name/email/phone
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging
from datetime import datetime, timezone

from app.services.ghl_client import GHLClient
from app.config_loader import load_yaml_config, load_programs_config

router = APIRouter()
logger = logging.getLogger("neuronx.clients")


@router.get("/search")
async def search_clients(q: str = Query(..., min_length=2)):
    """Search GHL contacts by name, email, or phone."""
    ghl = GHLClient()
    try:
        results = await ghl.search_contacts(q, limit=10)
    except Exception as e:
        logger.warning("Client search failed (GHL unavailable): %s", e)
        raise HTTPException(
            status_code=503,
            detail="Client search unavailable — GHL access token not configured or expired",
        )
    contacts = results.get("contacts", [])
    return {
        "query": q,
        "results": [
            {
                "id": c.get("id"),
                "name": f"{c.get('firstName', '')} {c.get('lastName', '')}".strip(),
                "email": c.get("email", ""),
                "phone": c.get("phone", ""),
                "tags": c.get("tags", []),
            }
            for c in contacts
        ],
        "total": len(contacts),
    }


@router.get("/{contact_id}/form-data")
async def get_form_data(contact_id: str):
    """
    Return client data mapped for IRCC form auto-fill.
    Used by the Chrome extension to populate form fields.
    """
    ghl = GHLClient()
    try:
        contact = await ghl.get_contact(contact_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Extract custom fields
    custom = {}
    for field in contact.get("customFields", []):
        key = field.get("id", "")
        val = field.get("value", "")
        if val:
            custom[key] = val

    # Get firm defaults
    firm_config = load_yaml_config("ircc_field_mappings").get("firm_defaults", {})

    # Build form data organized for auto-fill
    form_data = {
        # Client personal info
        "full_name": contact.get("lastName", ""),
        "given_name": contact.get("firstName", ""),
        "date_of_birth": _get_custom(custom, "date_of_birth"),
        "country_of_citizenship": _get_custom(custom, "country_of_citizenship"),
        "passport_number": _get_custom(custom, "passport_number"),
        "email": contact.get("email", ""),
        "phone": contact.get("phone", ""),
        "marital_status": _get_custom(custom, "marital_status"),

        # Program info
        "program_interest": _get_custom(custom, "program_interest", "ai_program_interest"),

        # Express Entry
        "education_level": _get_custom(custom, "education_level", "r2_education_level"),
        "work_experience": _get_custom(custom, "work_experience", "years_work_experience"),
        "language_test": _get_custom(custom, "language_test", "language_test_type"),
        "noc_code": _get_custom(custom, "noc_code"),
        "settlement_funds": _get_custom(custom, "settlement_funds"),

        # Spousal
        "sponsor_name": _get_custom(custom, "sponsor_name"),
        "sponsor_status": _get_custom(custom, "sponsor_status"),
        "relationship_type": _get_custom(custom, "relationship_type"),
        "marriage_date": _get_custom(custom, "marriage_date"),

        # Work Permit
        "employer_name": _get_custom(custom, "employer_name"),
        "job_title": _get_custom(custom, "job_title"),
        "lmia_status": _get_custom(custom, "lmia_status"),

        # Representative (firm) defaults
        "firm_defaults": {
            "rep_family_name": firm_config.get("rcic_name", "").split()[-1] if firm_config.get("rcic_name") else "",
            "rep_given_name": firm_config.get("rcic_name", "").split()[0] if firm_config.get("rcic_name") else "",
            "rep_organization": firm_config.get("firm_name", ""),
            "rep_member_id": firm_config.get("rcic_license", ""),
            "rep_email": firm_config.get("firm_email", ""),
            "rep_phone": firm_config.get("firm_phone", ""),
        },

        # Metadata
        "contact_id": contact_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    return form_data


@router.get("/{contact_id}/data-sheet")
async def get_data_sheet(contact_id: str):
    """
    Generate a comprehensive data sheet organized by IRCC form sections.
    RCIC can use this as a reference when filling IRCC portal manually.
    """
    ghl = GHLClient()
    try:
        contact = await ghl.get_contact(contact_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Contact not found")

    custom = {}
    for field in contact.get("customFields", []):
        key = field.get("id", "")
        val = field.get("value", "")
        if val:
            custom[key] = val

    program = _get_custom(custom, "program_interest", "ai_program_interest") or "Unknown"

    # Get program-specific requirements
    programs_config = load_programs_config()
    prog_data = programs_config.get(program, {})
    ircc_forms = prog_data.get("ircc_forms", [])
    required_docs = prog_data.get("required_documents", [])
    conditional_docs = prog_data.get("conditional_documents", [])
    processing = prog_data.get("processing_months", {"min": "?", "max": "?"})

    data_sheet = {
        "title": f"CLIENT DATA SHEET — {contact.get('firstName', '')} {contact.get('lastName', '')}",
        "program": program,
        "generated_at": datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC"),
        "contact_id": contact_id,

        "sections": {
            "1_personal_information": {
                "title": "Section 1: Personal Information",
                "fields": {
                    "Family Name": contact.get("lastName", ""),
                    "Given Name(s)": contact.get("firstName", ""),
                    "Date of Birth": _get_custom(custom, "date_of_birth"),
                    "Country of Citizenship": _get_custom(custom, "country_of_citizenship"),
                    "Current Country of Residence": _get_custom(custom, "current_country"),
                    "Passport Number": _get_custom(custom, "passport_number"),
                    "Passport Expiry": _get_custom(custom, "passport_expiry"),
                },
            },
            "2_contact_information": {
                "title": "Section 2: Contact Information",
                "fields": {
                    "Email": contact.get("email", ""),
                    "Phone": contact.get("phone", ""),
                    "Address": contact.get("address1", ""),
                },
            },
            "3_family_information": {
                "title": "Section 3: Family Information",
                "fields": {
                    "Marital Status": _get_custom(custom, "marital_status"),
                    "Dependents": _get_custom(custom, "has_dependents"),
                    "Number of Dependents": _get_custom(custom, "num_dependents"),
                },
            },
            "4_program_specific": {
                "title": f"Section 4: {program} Details",
                "fields": _get_program_fields(custom, program),
            },
            "5_background": {
                "title": "Section 5: Background Declarations",
                "fields": {
                    "Criminal History": _get_custom(custom, "criminal_history"),
                    "Previous Refusals": _get_custom(custom, "previous_refusal"),
                    "Medical Conditions": _get_custom(custom, "medical_conditions"),
                },
            },
        },

        "ircc_forms_required": [
            {"code": f.get("code", ""), "name": f.get("name", ""), "required": f.get("required", True)}
            for f in ircc_forms
        ],

        "document_checklist": {
            "required": required_docs,
            "conditional": conditional_docs,
        },

        "processing_estimate": {
            "min_months": processing.get("min", "?"),
            "max_months": processing.get("max", "?"),
            "disclaimer": "Processing times are estimates based on IRCC averages and may vary.",
        },
    }

    return data_sheet


@router.get("/{contact_id}/validate")
async def validate_completeness(contact_id: str):
    """
    Check if all required data and documents are collected for submission.
    Returns pass/fail with list of missing items.
    """
    ghl = GHLClient()
    try:
        contact = await ghl.get_contact(contact_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Contact not found")

    custom = {}
    for field in contact.get("customFields", []):
        key = field.get("id", "")
        val = field.get("value", "")
        if val:
            custom[key] = val

    program = _get_custom(custom, "program_interest", "ai_program_interest")

    # Required fields for ALL programs
    required_fields = {
        "Full Name": bool(contact.get("lastName")),
        "Given Name": bool(contact.get("firstName")),
        "Email": bool(contact.get("email")),
        "Phone": bool(contact.get("phone")),
        "Country of Citizenship": bool(_get_custom(custom, "country_of_citizenship")),
        "Passport Number": bool(_get_custom(custom, "passport_number")),
        "Marital Status": bool(_get_custom(custom, "marital_status")),
        "Program Interest": bool(program),
        "Criminal History Declaration": bool(_get_custom(custom, "criminal_history")),
        "Previous Refusal Declaration": bool(_get_custom(custom, "previous_refusal")),
    }

    # Program-specific required fields
    if program == "Express Entry":
        required_fields.update({
            "Education Level": bool(_get_custom(custom, "education_level", "r2_education_level")),
            "Work Experience": bool(_get_custom(custom, "work_experience", "years_work_experience")),
            "Language Test": bool(_get_custom(custom, "language_test", "language_test_type")),
        })
    elif program == "Spousal Sponsorship":
        required_fields.update({
            "Sponsor Status": bool(_get_custom(custom, "sponsor_status")),
            "Relationship Type": bool(_get_custom(custom, "relationship_type")),
        })
    elif program == "Work Permit":
        required_fields.update({
            "Employer Name": bool(_get_custom(custom, "employer_name")),
            "LMIA Status": bool(_get_custom(custom, "lmia_status")),
        })

    missing = [name for name, present in required_fields.items() if not present]
    total = len(required_fields)
    filled = total - len(missing)

    return {
        "contact_id": contact_id,
        "program": program or "Not specified",
        "is_complete": len(missing) == 0,
        "total_fields": total,
        "filled_fields": filled,
        "missing_count": len(missing),
        "missing_fields": missing,
        "completeness_percent": round((filled / total * 100) if total > 0 else 0),
        "ready_for_submission": len(missing) == 0,
    }


@router.get("/{contact_id}/copy-paste")
async def get_copy_paste_guide(contact_id: str):
    """
    Generate copy-paste-ready text blocks for IRCC portal.
    Each block matches an IRCC portal page section.
    """
    ghl = GHLClient()
    try:
        contact = await ghl.get_contact(contact_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Contact not found")

    custom = {}
    for field in contact.get("customFields", []):
        key = field.get("id", "")
        val = field.get("value", "")
        if val:
            custom[key] = val

    first = contact.get("firstName", "")
    last = contact.get("lastName", "")
    program = _get_custom(custom, "program_interest", "ai_program_interest") or "Unknown"
    firm_config = load_yaml_config("ircc_field_mappings").get("firm_defaults", {})

    guide = {
        "title": f"IRCC Portal Copy-Paste Guide — {first} {last}",
        "program": program,
        "instructions": "Copy each value and paste into the corresponding IRCC portal field.",

        "personal_details": {
            "Family name / Last name": last,
            "Given name(s) / First name": first,
            "Date of birth": _get_custom(custom, "date_of_birth"),
            "Country of birth": _get_custom(custom, "country_of_citizenship"),
            "Country of citizenship": _get_custom(custom, "country_of_citizenship"),
            "Current country of residence": _get_custom(custom, "current_country"),
        },

        "passport_travel_document": {
            "Passport/travel document number": _get_custom(custom, "passport_number"),
            "Passport expiry date": _get_custom(custom, "passport_expiry"),
            "Country of issue": _get_custom(custom, "country_of_citizenship"),
        },

        "contact_information": {
            "Email address": contact.get("email", ""),
            "Telephone number": contact.get("phone", ""),
            "Current mailing address": contact.get("address1", ""),
        },

        "family_information": {
            "Marital status": _get_custom(custom, "marital_status"),
            "Number of dependants": _get_custom(custom, "num_dependents") or "0",
        },

        "representative_information": {
            "Representative type": "Paid representative — RCIC",
            "Family name": firm_config.get("rcic_name", "").split()[-1] if firm_config.get("rcic_name") else "",
            "Given name": firm_config.get("rcic_name", "").split()[0] if firm_config.get("rcic_name") else "",
            "Organization": firm_config.get("firm_name", ""),
            "Membership ID": firm_config.get("rcic_license", ""),
            "Email": firm_config.get("firm_email", ""),
            "Phone": firm_config.get("firm_phone", ""),
        },
    }

    return guide


def _get_custom(custom: dict, *keys) -> str:
    """Get a custom field value by trying multiple possible key names."""
    for key in keys:
        for field_id, value in custom.items():
            if key.lower() in field_id.lower():
                return str(value)
    return ""


def _get_program_fields(custom: dict, program: str) -> dict:
    """Get program-specific fields for the data sheet."""
    if program == "Express Entry":
        return {
            "Education Level": _get_custom(custom, "education_level", "r2_education_level"),
            "ECA Completed": _get_custom(custom, "eca_completed"),
            "Years of Work Experience": _get_custom(custom, "work_experience", "years_work_experience"),
            "Canadian Work Experience": _get_custom(custom, "canadian_work_experience"),
            "Primary Occupation": _get_custom(custom, "primary_occupation"),
            "NOC Code": _get_custom(custom, "noc_code"),
            "Language Test Type": _get_custom(custom, "language_test", "language_test_type"),
            "Language Scores": _get_custom(custom, "language_scores"),
            "French Ability": _get_custom(custom, "french_ability"),
            "Settlement Funds (CAD)": _get_custom(custom, "settlement_funds"),
            "Job Offer": _get_custom(custom, "has_job_offer"),
            "Provincial Nomination": _get_custom(custom, "provincial_nomination"),
        }
    elif program == "Spousal Sponsorship":
        return {
            "Sponsor Name": _get_custom(custom, "sponsor_name"),
            "Sponsor Immigration Status": _get_custom(custom, "sponsor_status"),
            "Sponsor Province": _get_custom(custom, "sponsor_province"),
            "Relationship Type": _get_custom(custom, "relationship_type"),
            "Marriage/Relationship Date": _get_custom(custom, "marriage_date"),
            "Met in Person": _get_custom(custom, "met_in_person"),
            "Applicant in Canada": _get_custom(custom, "applicant_in_canada"),
            "Applicant Current Status": _get_custom(custom, "applicant_current_status"),
        }
    elif program == "Work Permit":
        return {
            "Employer Name": _get_custom(custom, "employer_name"),
            "Job Title": _get_custom(custom, "job_title"),
            "NOC Code": _get_custom(custom, "noc_code"),
            "LMIA Status": _get_custom(custom, "lmia_status"),
            "Work Permit Type": _get_custom(custom, "work_permit_type"),
            "Currently in Canada": _get_custom(custom, "currently_in_canada"),
        }
    elif program == "Study Permit":
        return {
            "DLI Name": _get_custom(custom, "dli_name"),
            "Program of Study": _get_custom(custom, "program_name"),
            "Program Duration": _get_custom(custom, "program_duration"),
            "Acceptance Letter": _get_custom(custom, "has_acceptance_letter"),
            "Tuition Amount": _get_custom(custom, "tuition_amount"),
            "Funding Source": _get_custom(custom, "funding_source"),
        }
    return {"Note": "Program-specific fields collected during consultation"}
