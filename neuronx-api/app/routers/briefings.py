"""
Consultation Preparation Briefing Endpoint
POST /briefing/generate

Assembles pre-consultation briefing from GHL data and delivers via email + GHL note.
See: docs/01_product/prd.md FC-NX-04
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Literal
import logging

from app.services.briefing_service import BriefingService

router = APIRouter()
logger = logging.getLogger("neuronx.briefings")


class BriefingRequest(BaseModel):
    contact_id: str = Field(..., min_length=1, max_length=100)
    appointment_id: str = Field(..., min_length=1, max_length=100)
    consultant_email: str = Field(..., min_length=3, max_length=255)
    delivery_method: Literal["email_only", "note_only", "email_and_note"] = "email_and_note"

    @field_validator("consultant_email")
    @classmethod
    def _valid_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v


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
    except HTTPException:
        raise
    except Exception as e:
        err_str = str(e)
        logger.error("Briefing error for contact=%s: %s", payload.contact_id, err_str)
        # Map upstream errors to proper HTTP codes without leaking internals
        if "404" in err_str or "not found" in err_str.lower():
            raise HTTPException(status_code=404, detail="Contact or appointment not found")
        if "401" in err_str or "403" in err_str:
            raise HTTPException(status_code=502, detail="Upstream service authentication failed")
        raise HTTPException(status_code=500, detail="Briefing generation failed")
