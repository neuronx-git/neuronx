"""
Consultation Preparation Briefing Endpoint
POST /briefing/generate

Assembles pre-consultation briefing from GHL data and delivers via email + GHL note.
See: docs/01_product/prd.md FC-NX-04
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import logging

from app.services.briefing_service import BriefingService

router = APIRouter()
logger = logging.getLogger("neuronx.briefings")


class BriefingRequest(BaseModel):
    contact_id: str
    appointment_id: str
    consultant_email: str
    delivery_method: str = "email_and_note"  # "email_only" | "note_only" | "email_and_note"


class BriefingResponse(BaseModel):
    status: str
    contact_id: str
    appointment_id: str
    briefing_summary: str
    delivered_to: list[str]


@router.post("/generate", response_model=BriefingResponse)
async def generate_briefing(payload: BriefingRequest, background_tasks: BackgroundTasks):
    """
    Generate and deliver pre-consultation briefing for an upcoming appointment.
    Pulls contact data from GHL, assembles structured briefing, delivers via email + GHL note.
    Typically triggered 30 minutes before appointment.
    """
    logger.info(
        "Generating briefing for contact=%s appointment=%s",
        payload.contact_id,
        payload.appointment_id,
    )

    service = BriefingService()
    try:
        result = await service.generate_and_deliver(
            contact_id=payload.contact_id,
            appointment_id=payload.appointment_id,
            consultant_email=payload.consultant_email,
            delivery_method=payload.delivery_method,
        )
        return result
    except Exception as e:
        logger.error("Briefing error for contact=%s: %s", payload.contact_id, str(e))
        raise HTTPException(status_code=500, detail=str(e))
