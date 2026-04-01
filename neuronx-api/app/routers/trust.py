"""
Trust Boundary Enforcement Endpoint
POST /trust/check  — Audit AI interaction for compliance violations
GET  /trust/log    — Query compliance audit log

BINDING: docs/04_compliance/trust_boundaries.md
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
import logging

from app.services.trust_service import TrustService, TrustCheckResult

router = APIRouter()
logger = logging.getLogger("neuronx.trust")


class TrustCheckRequest(BaseModel):
    transcript: str
    contact_id: str
    call_id: Optional[str] = None
    ai_response: Optional[str] = None


@router.post("/check", response_model=TrustCheckResult)
async def check_trust_boundaries(payload: TrustCheckRequest):
    """
    Check an AI interaction transcript for trust boundary violations.
    Returns escalation flags and any violations detected.

    This must be called after every AI call transcript is received.
    """
    service = TrustService()
    result = service.check_transcript(
        transcript=payload.transcript,
        contact_id=payload.contact_id,
        call_id=payload.call_id,
    )

    if result.requires_escalation:
        logger.warning(
            "Trust boundary escalation: contact=%s flags=%s",
            payload.contact_id,
            result.flags,
        )

    return result


@router.get("/log")
async def get_compliance_log(
    contact_id: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
):
    """
    Query the compliance audit log.
    Used for regulatory reporting and incident investigation.
    """
    service = TrustService()
    return await service.get_audit_log(contact_id=contact_id, limit=limit)
