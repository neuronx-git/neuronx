"""
Lead Readiness Scoring Endpoints

POST /score/lead  — Full R1-R5 scoring (used by VAPI end-of-call)
POST /score/form  — Preliminary scoring from form data only (R1-R3)

See: docs/02_operating_system/operating_spec.md for scoring logic.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging

from app.models.readiness import ReadinessInput, ReadinessScore
from app.services.scoring_service import ScoringService

router = APIRouter()
logger = logging.getLogger("neuronx.scoring")


@router.post("/lead", response_model=ReadinessScore)
async def score_lead(payload: ReadinessInput):
    """
    Score a lead's readiness based on R1-R5 dimensions.
    Primary path: called after VAPI end-of-call with full structured data.
    """
    service = ScoringService()
    try:
        result = service.score(
            contact_id=payload.contact_id,
            r1_program_interest=payload.r1_program_interest,
            r2_current_location=payload.r2_current_location,
            r3_timeline_urgency=payload.r3_timeline_urgency,
            r4_prior_applications=payload.r4_prior_applications,
            r5_budget_awareness=payload.r5_budget_awareness,
            transcript_excerpt=payload.transcript_excerpt,
            call_id=payload.call_id,
        )
        logger.info("Scored lead %s: %s (score=%d)", payload.contact_id, result.outcome, result.score)
        return result
    except Exception as e:
        logger.error("Scoring error for %s: %s", payload.contact_id, str(e))
        raise HTTPException(status_code=500, detail=str(e))


class FormScoreInput(BaseModel):
    """Scoring input from form submission (R1-R3 only)."""
    contact_id: str
    program_interest: Optional[str] = Field(None, description="Form field: Program Interest dropdown")
    current_location: Optional[str] = Field(None, description="Form field: Current Location dropdown")
    timeline: Optional[str] = Field(None, description="Form field: Timeline dropdown")


class FormScoreOutput(BaseModel):
    contact_id: str
    preliminary_score: int = Field(..., ge=0, le=100)
    score_source: str = "form"
    dimensions_captured: int
    max_possible: int = 48
    can_upgrade: bool = True
    ghl_tags_to_add: list[str]
    ghl_fields_to_update: dict
    note: str


@router.post("/form", response_model=FormScoreOutput)
async def score_from_form(payload: FormScoreInput):
    """
    Preliminary scoring from form submission data only.

    Form captures R1 (program), R2 (location), R3 (timeline) — max score 48/100.
    This provides an immediate directional score while VAPI call is pending.

    Flow:
      Form submitted → WF-01 fires → webhook to NeuronX → /score/form
      → Preliminary score + tags set
      → VAPI call happens (WF-02) → /webhooks/voice upgrades to full score

    The form score is NEVER final if a VAPI call succeeds — it's a fallback
    for unreachable leads after WF-02 exhausts all 7 contact attempts.
    """
    service = ScoringService()

    result = service.score(
        contact_id=payload.contact_id,
        r1_program_interest=payload.program_interest,
        r2_current_location=payload.current_location,
        r3_timeline_urgency=payload.timeline,
    )

    # Form scoring is always preliminary — cap at 48 and mark as upgradeable
    form_score = min(result.score, 48)
    dims = sum(1 for v in [payload.program_interest, payload.current_location, payload.timeline] if v)

    # Only add form-specific tags, not score tier tags (wait for VAPI)
    form_tags = ["nx:form_scored"]
    if dims >= 2:
        form_tags.append("nx:form_qualified")

    # Fields to set immediately (VAPI will overwrite these if call succeeds)
    fields = {}
    if payload.program_interest:
        fields["ai_program_interest"] = payload.program_interest
    if payload.current_location:
        fields["ai_current_location"] = payload.current_location
    if payload.timeline:
        fields["ai_timeline_urgency"] = payload.timeline
    fields["form_score"] = str(form_score)

    logger.info(
        "Form-scored %s: %d/48 (%d dims). VAPI call pending.",
        payload.contact_id, form_score, dims,
    )

    return FormScoreOutput(
        contact_id=payload.contact_id,
        preliminary_score=form_score,
        dimensions_captured=dims,
        ghl_tags_to_add=form_tags,
        ghl_fields_to_update=fields,
        note=f"Preliminary form score ({dims}/3 dimensions). Full score pending VAPI call.",
    )
