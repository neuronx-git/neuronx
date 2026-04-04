"""
Document Generation Endpoints
POST /documents/retainer     — Generate retainer agreement from GHL contact data
POST /documents/assessment   — Generate assessment report from scoring data
POST /documents/checklist    — Generate program-specific document checklist

Uses python-docx-template (docxtpl) for .docx generation.
Falls back to HTML generation if no .docx template exists.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
import logging

from app.services.ghl_client import GHLClient
from app.config_loader import load_programs_config
from app.utils.compliance_log import log_event

router = APIRouter()
logger = logging.getLogger("neuronx.documents")


# ── Document Checklists by Program ──

PROGRAM_CHECKLISTS = {
    "Express Entry": {
        "required": [
            "Valid passport (all pages)",
            "Educational Credential Assessment (ECA) from WES or equivalent",
            "IELTS or CELPIP language test results (General Training)",
            "Reference letters from all employers (last 10 years)",
            "Police clearance certificates (from all countries lived 6+ months)",
            "Proof of funds (bank statements, investments — last 6 months)",
            "Digital photo (IRCC specifications)",
            "Medical exam results (from IRCC-designated panel physician)",
        ],
        "conditional": [
            "Provincial nomination certificate (if PNP stream)",
            "Job offer letter with LMIA (if applicable)",
            "Spouse/partner documents (if applicable)",
            "Dependent children documents (birth certificates, custody)",
            "TEF results (if claiming French language points)",
        ],
    },
    "Spousal Sponsorship": {
        "required": [
            "Valid passport (sponsor + applicant)",
            "Marriage certificate or proof of common-law (12+ months cohabitation)",
            "Relationship evidence package (photos, communications, travel, joint finances)",
            "IMM 5532 — Relationship information and sponsorship evaluation",
            "Police clearance certificates",
            "Medical exam results",
            "Proof of sponsor's income (NOA, T4, employment letter)",
            "Digital photos (both parties)",
        ],
        "conditional": [
            "Divorce decree (if previously married)",
            "Children's birth certificates and custody documents",
            "Statutory declarations from friends/family attesting to relationship",
            "Open work permit application (if applicant in Canada)",
        ],
    },
    "Work Permit": {
        "required": [
            "Valid passport",
            "Job offer letter from Canadian employer",
            "Employment contract with terms and conditions",
            "Resume/CV",
            "Educational credentials relevant to position",
            "Police clearance certificates",
            "Medical exam (if applicable)",
            "Digital photo",
        ],
        "conditional": [
            "LMIA confirmation (if employer-specific)",
            "LMIA exemption documentation (if IMP/CUSMA/intra-company)",
            "Provincial nomination (if PNP work permit)",
            "Proof of current immigration status (if in Canada)",
            "Spousal open work permit docs (if applicable)",
        ],
    },
    "Study Permit": {
        "required": [
            "Valid passport",
            "Letter of acceptance from Designated Learning Institution (DLI)",
            "Proof of financial support (tuition + living expenses for 1 year)",
            "Statement of purpose / study plan",
            "Transcripts from previous education",
            "Language test results (if applicable)",
            "Police clearance certificates",
            "Medical exam results",
            "Digital photo",
        ],
        "conditional": [
            "Custodianship declaration (if minor)",
            "Quebec Acceptance Certificate (CAQ) (if studying in Quebec)",
            "GIC receipt (if SDS stream)",
            "Scholarship/funding letters",
        ],
    },
    "LMIA": {
        "required": [
            "Employer's business registration documents",
            "Job description with NOC code",
            "Proof of recruitment efforts (4 weeks advertising evidence)",
            "Prevailing wage documentation",
            "Business financial statements",
            "Transition plan (for high-wage LMIA)",
            "Employer compliance history",
        ],
        "conditional": [
            "Provincial assessment (if required by province)",
            "Union consultation results (if unionized workplace)",
            "Caregiver-specific documents (if caregiver stream)",
            "Agricultural stream documents (if SAWP/agricultural)",
        ],
    },
    "PR Renewal": {
        "required": [
            "Current PR card (both sides)",
            "Valid passport",
            "Residency calculation — proof of 730+ days in Canada in last 5 years",
            "Travel history (entry/exit records, passport stamps)",
            "IMM 5644 application form",
            "Digital photos (2)",
            "Processing fee payment receipt",
        ],
        "conditional": [
            "Employment letters (if counting time abroad with Canadian employer)",
            "Spouse's Canadian citizenship certificate (if counting spousal time)",
            "CBSA traveller records (from CBSA ATIP request)",
        ],
    },
    "Citizenship": {
        "required": [
            "Valid PR card or proof of PR status",
            "Valid passport",
            "Physical presence calculator (1,095+ days in last 5 years as PR)",
            "Tax returns (NOA) for 3 of last 5 years",
            "Language test results (CLB 4+ for ages 18-54)",
            "Police clearance (if applicable)",
            "Digital photos (2)",
            "Processing fee payment receipt",
        ],
        "conditional": [
            "Name change documents (if applicable)",
            "Permanent Resident Travel Document (if PR card expired)",
            "Military service records (if applicable)",
            "Prohibition order documentation (if previously prohibited)",
        ],
    },
    "Visitor Visa": {
        "required": [
            "Valid passport (6+ months validity beyond planned stay)",
            "Digital photo",
            "Purpose of visit letter",
            "Proof of ties to home country (employment, property, family)",
            "Proof of financial means for the visit",
            "Travel itinerary",
            "Invitation letter from Canadian host (if visiting someone)",
        ],
        "conditional": [
            "Hotel/accommodation bookings",
            "Return flight booking",
            "Business meeting details (if business visit)",
            "Super Visa requirements (if parent/grandparent — medical + insurance)",
            "Event registration (if attending conference/event)",
        ],
    },
}


class ChecklistRequest(BaseModel):
    contact_id: str
    program_type: str


class ChecklistResponse(BaseModel):
    contact_id: str
    program_type: str
    required_documents: list[str]
    conditional_documents: list[str]
    total_required: int
    generated_at: str


@router.post("/checklist", response_model=ChecklistResponse)
async def generate_checklist(payload: ChecklistRequest):
    """Generate program-specific document checklist. Reads from config/programs.yaml."""
    programs = load_programs_config()
    program = payload.program_type
    prog_data = programs.get(program)

    if not prog_data:
        # Fuzzy match
        for key in programs:
            if key.lower() in program.lower() or program.lower() in key.lower():
                prog_data = programs[key]
                program = key
                break

    # Fallback to hardcoded if config doesn't have it
    if not prog_data:
        checklist = PROGRAM_CHECKLISTS.get(program)
        if not checklist:
            for key in PROGRAM_CHECKLISTS:
                if key.lower() in program.lower() or program.lower() in key.lower():
                    checklist = PROGRAM_CHECKLISTS[key]
                    program = key
                    break
        if not checklist:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown program type: {payload.program_type}. Valid: {list(programs.keys())}",
            )
    else:
        checklist = {
            "required": prog_data.get("required_documents", []),
            "conditional": prog_data.get("conditional_documents", []),
        }

    log_event("checklist_generated", {
        "contact_id": payload.contact_id,
        "program_type": program,
    })

    return ChecklistResponse(
        contact_id=payload.contact_id,
        program_type=program,
        required_documents=checklist["required"],
        conditional_documents=checklist["conditional"],
        total_required=len(checklist["required"]),
        generated_at=datetime.now(tz=timezone.utc).isoformat(),
    )


class AssessmentReportRequest(BaseModel):
    contact_id: str


@router.post("/assessment")
async def generate_assessment_report(payload: AssessmentReportRequest):
    """
    Generate assessment report from GHL contact data + scoring results.
    Returns structured HTML report.
    """
    ghl = GHLClient()
    try:
        contact = await ghl.get_contact(payload.contact_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Contact not found: {e}")

    custom_fields = {}
    for f in contact.get("customFields", []):
        key = f.get("id") or f.get("key")
        val = f.get("value") or f.get("fieldValue")
        if key and val:
            custom_fields[key] = val

    name = f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip()
    program = custom_fields.get("ai_program_interest", "Not assessed")
    location = custom_fields.get("ai_current_location", "Not assessed")
    urgency = custom_fields.get("ai_timeline_urgency", "Not assessed")
    prior = custom_fields.get("ai_prior_applications", "Not assessed")
    budget = custom_fields.get("ai_budget_awareness", "Not assessed")
    outcome = custom_fields.get("ai_readiness_outcome", "Not scored")
    score = custom_fields.get("ai_readiness_score", "N/A")

    tags = [t if isinstance(t, str) else t.get("name", "") for t in contact.get("tags", [])]

    flags = []
    if "nx:human_escalation" in tags:
        flags.append("Complex case — senior review required")
    if "nx:urgent" in tags:
        flags.append("Urgent timeline — under 30 days")

    report = {
        "contact_id": payload.contact_id,
        "name": name,
        "email": contact.get("email", ""),
        "phone": contact.get("phone", ""),
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "readiness_assessment": {
            "program_interest": program,
            "current_location": location,
            "timeline_urgency": urgency,
            "prior_applications": prior,
            "budget_awareness": budget,
            "outcome": outcome,
            "score": score,
            "flags": flags,
        },
        "checklist": PROGRAM_CHECKLISTS.get(program, {"required": [], "conditional": []}),
    }

    log_event("assessment_report_generated", {
        "contact_id": payload.contact_id,
        "program": program,
    })

    return report
