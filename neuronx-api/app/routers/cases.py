"""
Case Processing Endpoints
POST /cases/initiate       — Start new case after retainer signed
POST /cases/stage          — Update case stage
POST /cases/submission     — Record IRCC submission
POST /cases/decision       — Record IRCC decision
GET  /cases/forms          — Get IRCC forms for a program
GET  /cases/timeline       — Get estimated processing time
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging

from app.services.case_service import CaseService

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
