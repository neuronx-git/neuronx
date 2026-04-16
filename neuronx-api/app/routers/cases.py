"""
Case Processing Endpoints
POST /cases/initiate       — Start new case after retainer signed
POST /cases/stage          — Update case stage
POST /cases/submission     — Record IRCC submission
POST /cases/decision       — Record IRCC decision
GET  /cases/forms          — Get IRCC forms for a program
GET  /cases/timeline       — Get estimated processing time
GET  /cases/questionnaire  — Smart onboarding questionnaire (program-specific)
GET  /cases/status         — Client-facing case status
GET  /cases/onboarding-url — Generate pre-filled onboarding URL from Phase 1 data
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from urllib.parse import urlencode, quote_plus
import logging

from app.services.ghl_client import GHLClient
from app.services.case_service import CaseService
from app.config_loader import load_yaml_config

router = APIRouter()
logger = logging.getLogger("neuronx.cases")


class CaseInitiateRequest(BaseModel):
    contact_id: str
    program_type: str
    assigned_rcic: str = "Unassigned"


class CaseStageRequest(BaseModel):
    contact_id: str
    stage: str = Field(..., description="onboarding|doc_collection|docs_complete|form_prep|under_review|submitted|processing|rfi|decision|closed")
    notes: Optional[str] = None


class SubmissionRequest(BaseModel):
    contact_id: str
    receipt_number: str
    submission_date: Optional[str] = None


class DecisionRequest(BaseModel):
    contact_id: str
    decision: str = Field(..., description="Approved|Refused|Withdrawn|Returned")
    decision_date: Optional[str] = None
    notes: Optional[str] = None


@router.post("/initiate")
async def initiate_case(payload: CaseInitiateRequest):
    """
    Start a new immigration case after retainer is signed.
    Creates case record in GHL, generates doc checklist, sets deadlines.
    """
    service = CaseService()
    try:
        result = await service.initiate_case(
            contact_id=payload.contact_id,
            program_type=payload.program_type,
            assigned_rcic=payload.assigned_rcic,
        )
        return result
    except Exception as e:
        logger.error("Case initiation failed for %s: %s", payload.contact_id, e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stage")
async def update_case_stage(payload: CaseStageRequest):
    """Update case to a new processing stage."""
    service = CaseService()
    result = await service.update_stage(
        contact_id=payload.contact_id,
        new_stage=payload.stage,
        notes=payload.notes,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/submission")
async def record_submission(payload: SubmissionRequest):
    """Record IRCC application submission with receipt number."""
    service = CaseService()
    return await service.record_submission(
        contact_id=payload.contact_id,
        receipt_number=payload.receipt_number,
        submission_date=payload.submission_date,
    )


@router.post("/decision")
async def record_decision(payload: DecisionRequest):
    """Record IRCC decision (Approved, Refused, Withdrawn, Returned)."""
    if payload.decision not in ("Approved", "Refused", "Withdrawn", "Returned"):
        raise HTTPException(status_code=400, detail=f"Invalid decision: {payload.decision}")
    service = CaseService()
    return await service.record_decision(
        contact_id=payload.contact_id,
        decision=payload.decision,
        decision_date=payload.decision_date,
        notes=payload.notes,
    )


@router.get("/forms/{program_type}")
async def get_ircc_forms(program_type: str):
    """Get required IRCC forms for a program type."""
    service = CaseService()
    forms = service.get_ircc_forms(program_type)
    if not forms:
        return {"program_type": program_type, "forms": [], "note": "No pre-mapped forms. RCIC determines manually."}
    return {
        "program_type": program_type,
        "forms": forms,
        "total_required": len([f for f in forms if f["required"]]),
        "total_optional": len([f for f in forms if not f["required"]]),
    }


@router.get("/timeline/{program_type}")
async def get_processing_timeline(program_type: str):
    """Get estimated IRCC processing time for a program."""
    service = CaseService()
    estimate = service.get_processing_estimate(program_type)
    return {
        "program_type": program_type,
        "estimated_months": estimate,
        "disclaimer": "Processing times are estimates based on IRCC averages. Actual times may vary.",
    }


@router.get("/questionnaire/{program_type}")
async def get_onboarding_questionnaire(program_type: str):
    """
    Returns program-specific onboarding questionnaire.
    Common questions + program-specific questions combined.
    Used by GHL form or Next.js portal to render the smart intake form.
    """
    config = load_yaml_config("questionnaires")
    if not config:
        raise HTTPException(status_code=500, detail="Questionnaire config not found")

    common = config.get("common_questions", [])
    programs = config.get("programs", {})

    # Normalize slug to display name (express-entry → Express Entry)
    slug_map = {p.lower().replace(" ", "-").replace("/", "-"): p for p in programs.keys()}
    display_name = slug_map.get(program_type, program_type)
    program_config = programs.get(display_name)
    if not program_config:
        # Return common questions only for unknown programs
        return {
            "program_type": program_type,
            "sections": ["Personal Information", "Contact", "Family", "Background"],
            "questions": common,
            "total_questions": len(common),
            "note": f"No program-specific questions for '{program_type}'. Using common questions only.",
        }

    program_questions = program_config.get("questions", [])
    program_sections = program_config.get("sections", [])

    # Combine common + program-specific
    all_questions = common + program_questions
    all_sections = ["Personal Information", "Contact", "Family", "Background"] + program_sections

    return {
        "program_type": display_name,
        "sections": all_sections,
        "questions": all_questions,
        "total_questions": len(all_questions),
        "common_count": len(common),
        "program_specific_count": len(program_questions),
    }


@router.get("/status/{contact_id}")
async def get_case_status(contact_id: str):
    """
    Client-facing case status. Returns current stage, timeline,
    outstanding docs, and next steps — safe for client portal display.
    """
    service = CaseService()
    ghl = service._get_ghl_client()

    try:
        contact = await ghl.get_contact(contact_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Extract case fields from contact custom fields
    custom = {}
    for field in contact.get("customFields", []):
        custom[field.get("id", "")] = field.get("value", "")

    # Map stage tags to human-readable status
    tags = contact.get("tags", [])
    stage = "Unknown"
    stage_map = {
        "nx:case:onboarding": "Onboarding — We're setting up your case",
        "nx:case:docs_pending": "Document Collection — Waiting for your documents",
        "nx:case:docs_complete": "Documents Received — All documents collected",
        "nx:case:form_prep": "Form Preparation — Your RCIC is preparing your application",
        "nx:case:under_review": "Internal Review — Quality check in progress",
        "nx:case:submitted": "Submitted to IRCC — Your application is with Immigration Canada",
        "nx:case:processing": "Processing — IRCC is reviewing your application",
        "nx:case:rfi": "Additional Information Required — IRCC needs more documents",
        "nx:case:decision": "Decision Received — IRCC has made a decision",
        "nx:case:closed": "Case Closed",
    }
    for tag, label in stage_map.items():
        if tag in tags:
            stage = label

    return {
        "contact_id": contact_id,
        "name": f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip(),
        "current_stage": stage,
        "program_type": next((f.get("value") for f in contact.get("customFields", []) if "case_program_type" in str(f.get("id", ""))), "Unknown"),
        "safe_for_client_display": True,
        "disclaimer": "For detailed case updates, please contact your assigned consultant.",
    }


@router.get("/onboarding-url/{contact_id}")
async def generate_onboarding_url(contact_id: str, base_url: str = "https://www.neuronx.co/intake/vmc/onboarding"):
    """
    Generate a pre-filled onboarding URL using Phase 1 data.

    Fetches all known data from GHL (inquiry form + VAPI call + scoring)
    and encodes it as Typebot URL parameters. The client clicks the link
    and the form is already pre-filled with their name, email, phone,
    program interest, and other known fields.

    Used in: WF-CP-01 (retainer signed → send onboarding link)
    """
    ghl = GHLClient()
    try:
        contact = await ghl.get_contact(contact_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Extract custom fields into a flat dict
    custom = {}
    for field in contact.get("customFields", []):
        field_key = field.get("id", "")
        field_val = field.get("value", "")
        if field_val:
            custom[field_key] = field_val

    # Map GHL data → Typebot form variables
    prefill = {}

    # From GHL contact record (Phase 1 inquiry form)
    first = contact.get("firstName", "")
    last = contact.get("lastName", "")
    if first or last:
        prefill["full_name"] = f"{first} {last}".strip()
    if contact.get("email"):
        prefill["email"] = contact["email"]
    if contact.get("phone"):
        prefill["phone"] = contact["phone"]
    if contact.get("country"):
        prefill["country_of_citizenship"] = contact["country"]

    # From VAPI call (R1-R5 structured data, stored in GHL custom fields)
    ghl_to_form = {
        "ai_program_interest": "program_interest",
        "ai_current_location": "current_country",
    }
    for ghl_key, form_key in ghl_to_form.items():
        val = custom.get(ghl_key, "")
        if val:
            # Normalize values
            if ghl_key == "ai_current_location":
                val = "Canada" if "canada" in val.lower() else val.replace("_", " ").title()
            prefill[form_key] = val

    # From scoring (useful context, prefill if applicable)
    if custom.get("ai_prior_applications"):
        val = custom["ai_prior_applications"]
        if "refusal" in val.lower() or "complex" in val.lower():
            prefill["previous_refusal"] = "Yes"
        elif val.lower() in ("none", "no"):
            prefill["previous_refusal"] = "No"

    # Build client-specific URL: /intake/vmc/onboarding?contact_id=X&field=Y
    # The contact_id in query params ensures Typebot webhook can identify the contact
    prefill["contact_id"] = contact_id
    url = f"{base_url}?{urlencode(prefill, quote_via=quote_plus)}"

    # Calculate actual field count for the program (fully dynamic from YAML)
    program_interest = prefill.get("program_interest", "")
    q_config = load_yaml_config("questionnaires")
    total_fields = len(q_config.get("common_questions", [])) if q_config else 19
    if program_interest and q_config:
        programs_q = q_config.get("programs", {})
        slug_map = {p.lower().replace(" ", "-"): p for p in programs_q.keys()}
        display = slug_map.get(program_interest.lower().replace(" ", "-"), program_interest)
        prog = programs_q.get(display, {})
        total_fields += len(prog.get("questions", []))

    logger.info("Generated onboarding URL for %s with %d prefilled fields", contact_id, len(prefill))

    return {
        "contact_id": contact_id,
        "onboarding_url": url,
        "prefilled_fields": list(prefill.keys()),
        "prefill_count": len(prefill),
        "total_form_fields": total_fields,
        "fields_client_still_needs": total_fields - len(prefill),
        "ghl_workflow_template": (
            f"Hi {{{{contact.firstName}}}}, your retainer is confirmed! 🎉\n\n"
            f"Complete your onboarding assessment here:\n{url}\n\n"
            f"This takes ~10 minutes. Your consultant will review everything within 2 business days.\n\n"
            f"— Visa Master Canada"
        ),
    }
