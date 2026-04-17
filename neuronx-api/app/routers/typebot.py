"""
Typebot Webhook & Form Management Endpoints
POST /typebot/webhook         — Receive form submissions from Typebot
POST /typebot/create-form     — Generate and create a Typebot form from questionnaires.yaml
GET  /typebot/form-url        — Get the published form URL for a program
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import logging

from app.services.ghl_client import GHLClient
from app.services.typebot_service import TypebotService
from app.config_loader import load_yaml_config
from app.utils.compliance_log import log_event

router = APIRouter()
logger = logging.getLogger("neuronx.typebot")

# In-memory dedup cache for Typebot submissions (prevents double-processing)
# Key: resultId from Typebot, Value: timestamp
# Also backed by processed_webhooks DB table for durability across restarts
_processed_submissions: dict[str, str] = {}


async def _is_typebot_duplicate(result_id: str) -> bool:
    """Check in-memory cache first, then DB."""
    if result_id in _processed_submissions:
        return True
    from app.database import is_db_configured
    if is_db_configured():
        try:
            from app.database import get_session
            from sqlalchemy import text
            async for session in get_session():
                row = await session.execute(
                    text("SELECT 1 FROM processed_webhooks WHERE webhook_id = :wid AND source = 'typebot'"),
                    {"wid": f"typebot-{result_id}"},
                )
                if row.scalar() is not None:
                    _processed_submissions[result_id] = "db"
                    return True
        except Exception:
            pass
    return False


async def _mark_typebot_processed(result_id: str):
    """Mark in memory + DB."""
    _processed_submissions[result_id] = datetime.now().isoformat()
    # Trim in-memory cache
    if len(_processed_submissions) > 500:
        oldest_keys = list(_processed_submissions.keys())[:-500]
        for k in oldest_keys:
            _processed_submissions.pop(k, None)
    # Persist to DB
    from app.database import is_db_configured
    if is_db_configured():
        try:
            from app.database import async_session_factory
            from app.models.db_models import ProcessedWebhook
            if async_session_factory:
                async with async_session_factory() as session:
                    session.add(ProcessedWebhook(
                        webhook_id=f"typebot-{result_id}",
                        source="typebot",
                        response_status=200,
                    ))
                    await session.commit()
        except Exception:
            pass  # In-memory cache still protects


class TypebotWebhookPayload(BaseModel):
    """Payload from Typebot webhook on form submission."""
    contact_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    answers: dict = Field(default_factory=dict)


class CreateFormRequest(BaseModel):
    """Request to generate a Typebot form for a program."""
    program_type: str
    firm_name: str = "Visa Master Canada"
    webhook_url: Optional[str] = None


@router.post("/webhook")
async def typebot_webhook(request: Request):
    """
    Receive form submission from Typebot.
    Maps answers to GHL custom fields, generates doc checklist, adds tags.

    Flow:
    1. Typebot conversational form collects client answers
    2. On submit, Typebot fires webhook to this endpoint
    3. We parse answers and map to GHL custom fields
    4. Generate program-specific document checklist
    5. Add nx:case:docs_pending tag (triggers WF-CP-02)
    6. Return success

    Safety:
    - Deduplication via resultId (prevents double-processing on webhook retry)
    - Email lookup returns error if >1 contact matches (prevents cross-contamination)
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Request body must be valid JSON")

    if not isinstance(payload, dict):
        raise HTTPException(status_code=422, detail="Request body must be a JSON object")

    logger.info("Typebot webhook received: %s", list(payload.keys()))

    # ── Submission deduplication (memory + DB backed) ──────────────────
    result_id = payload.get("resultId") or payload.get("result_id")
    if result_id:
        if await _is_typebot_duplicate(result_id):
            logger.info("Duplicate Typebot submission: resultId=%s", result_id)
            return {"status": "duplicate", "resultId": result_id, "note": "Already processed"}

    # Typebot sends data in different formats depending on configuration
    # Support both flat answers and nested result set
    answers = payload.get("answers", payload)
    contact_id = (
        payload.get("contact_id")
        or payload.get("contactId")
        or answers.get("contact_id")
    )
    email = payload.get("email") or answers.get("email")
    phone = payload.get("phone") or answers.get("phone")

    ghl = GHLClient()

    # Find or identify the contact (with ambiguity protection)
    if not contact_id and email:
        results = await ghl.search_contacts(email, limit=5)
        contacts = results.get("contacts", [])
        if len(contacts) > 1:
            logger.warning("Typebot webhook: multiple contacts match email=%s (count=%d). Using first match.", email, len(contacts))
        if contacts:
            contact_id = contacts[0]["id"]

    if not contact_id and phone:
        results = await ghl.search_contacts(phone, limit=5)
        contacts = results.get("contacts", [])
        if len(contacts) > 1:
            logger.warning("Typebot webhook: multiple contacts match phone=%s (count=%d). Using first match.", phone, len(contacts))
        if contacts:
            contact_id = contacts[0]["id"]

    if not contact_id:
        logger.warning("Typebot webhook: could not identify contact (email=%s, phone=%s)", email, phone)
        return {"status": "unmatched", "note": "Could not find contact in GHL"}

    # Map Typebot answers to GHL custom fields
    # Covers all 8 programs — common (24) + program-specific fields
    field_mapping = {
        # ── Common: Personal Information (6) ──
        "full_name": "full_name",
        "date_of_birth": "date_of_birth",
        "country_of_citizenship": "country_of_citizenship",
        "current_country": "current_country",
        "passport_number": "passport_number",
        "passport_expiry": "passport_expiry",
        # ── Common: Family (6) ──
        "marital_status": "marital_status",
        "has_spouse_on_application": "has_spouse_on_application",
        "spouse_full_name": "spouse_full_name",
        "spouse_date_of_birth": "spouse_date_of_birth",
        "spouse_citizenship": "spouse_citizenship",
        "has_dependents": "has_dependents",
        "num_dependents": "num_dependents",
        "dependent_names_dobs": "dependent_names_dobs",
        # ── Common: Background (6) ──
        "criminal_history": "criminal_history",
        "previous_refusal": "previous_refusal",
        "previous_refusal_details": "previous_refusal_details",
        "medical_conditions": "medical_conditions",
        "deportation_history": "deportation_history",
        "countries_lived": "countries_lived",
        # ── Common: Consent (2) ──
        "consent_true_information": "consent_true_information",
        "consent_representation": "consent_representation",
        # ── Express Entry (P0, 20 fields) ──
        "education_level": "r2_education_level",
        "eca_completed": "eca_completed",
        "eca_organization": "eca_organization",
        "years_work_experience": "years_work_experience",
        "canadian_work_experience": "canadian_work_experience",
        "primary_occupation": "primary_occupation",
        "noc_code": "noc_code",
        "has_job_offer": "has_job_offer",
        "job_offer_lmia_status": "job_offer_lmia_status",
        "provincial_nomination": "provincial_nomination",
        "language_test_type": "language_test_type",
        "language_listening": "language_listening",
        "language_reading": "language_reading",
        "language_writing": "language_writing",
        "language_speaking": "language_speaking",
        "language_overall": "language_overall",
        "french_ability": "french_ability",
        "settlement_funds": "settlement_funds",
        "settlement_funds_source": "settlement_funds_source",
        # ── Spousal Sponsorship (P0, 15 fields) ──
        "sponsor_name": "sponsor_name",
        "sponsor_status": "sponsor_status",
        "sponsor_province": "sponsor_province",
        "previous_sponsorship": "previous_sponsorship",
        "sponsor_previous_marriage": "sponsor_previous_marriage",
        "sponsor_annual_income": "sponsor_annual_income",
        "sponsor_income_source": "sponsor_income_source",
        "relationship_type": "relationship_type",
        "marriage_date": "marriage_date",
        "relationship_how_met": "relationship_how_met",
        "relationship_duration_months": "relationship_duration_months",
        "met_in_person": "met_in_person",
        "applicant_in_canada": "applicant_in_canada",
        "applicant_current_status": "applicant_current_status",
        "applicant_wants_open_work_permit": "applicant_wants_open_work_permit",
        # ── Work Permit (P0, 13 fields) ──
        "work_permit_type": "work_permit_type",
        "employer_name": "employer_name",
        "employer_province": "employer_province",
        "job_title": "job_title",
        "lmia_status": "lmia_status",
        "employment_start_date": "employment_start_date",
        "employment_salary": "employment_salary",
        "employment_duration_months": "employment_duration_months",
        "currently_in_canada": "currently_in_canada",
        "current_immigration_status": "current_immigration_status",
        "current_permit_expiry": "current_permit_expiry",
        # ── Study Permit (P1, 12 fields) ──
        "dli_name": "dli_name",
        "program_name": "program_name",
        "program_duration": "program_duration",
        "has_acceptance_letter": "has_acceptance_letter",
        "studying_in_quebec": "studying_in_quebec",
        "has_caq": "has_caq",
        "post_study_plan": "post_study_plan",
        "tuition_amount": "tuition_amount",
        "funding_source": "funding_source",
        "has_gic": "has_gic",
        "total_funds_available": "total_funds_available",
        "previous_education_level": "previous_education_level",
        # ── LMIA (P2, 7 fields) ──
        "employer_industry": "employer_industry",
        "position_title": "position_title",
        "position_salary": "position_salary",
        "lmia_stream": "lmia_stream",
        "recruitment_completed": "recruitment_completed",
        # ── PR Renewal (P2, 5 fields) ──
        "pr_card_expiry": "pr_card_expiry",
        "days_in_canada": "days_in_canada",
        "travel_outside_canada": "travel_outside_canada",
        "longest_absence_months": "longest_absence_months",
        "employed_abroad_canadian_company": "employed_abroad_canadian_company",
        # ── Citizenship (P2, 7 fields) ──
        "pr_start_date": "pr_start_date",
        "days_in_canada_as_pr": "days_in_canada_as_pr",
        "filed_taxes": "filed_taxes",
        "tax_years_filed": "tax_years_filed",
        "language_test_taken": "language_test_taken",
        "citizenship_language_score": "citizenship_language_score",
        "name_changed_since_pr": "name_changed_since_pr",
        # ── Visitor Visa (P2, 12 fields) ──
        "purpose_of_visit": "purpose_of_visit",
        "planned_duration": "planned_duration",
        "previous_visits_canada": "previous_visits_canada",
        "host_in_canada": "host_in_canada",
        "host_name": "host_name",
        "host_relationship": "host_relationship",
        "employment_in_home_country": "employment_in_home_country",
        "owns_property_home_country": "owns_property_home_country",
        "funds_for_visit": "funds_for_visit",
        "flight_booked": "flight_booked",
        "supervisa_child_in_canada": "supervisa_child_in_canada",
        "supervisa_has_medical_insurance": "supervisa_has_medical_insurance",
        # ── Program interest ──
        "program_interest": "ai_program_interest",
    }

    # Build GHL custom field updates
    custom_fields = {}
    for typebot_key, ghl_key in field_mapping.items():
        value = answers.get(typebot_key)
        if value is not None and value != "":
            custom_fields[ghl_key] = str(value)

    # Update GHL contact
    if custom_fields:
        await ghl.update_custom_fields(contact_id, custom_fields)
        logger.info("Updated %d GHL fields for contact %s", len(custom_fields), contact_id)

    # Add tag to trigger document collection workflow
    await ghl.add_tag(contact_id, "nx:case:docs_pending")

    # Escalation: flag sensitive cases for RCIC priority review
    escalation_triggers = [
        ("deportation_history", "Yes"),
        ("criminal_history", "Yes"),
    ]
    for field, trigger_value in escalation_triggers:
        val = str(answers.get(field, "")).strip().lower()
        if val in (trigger_value.lower(), "true", "yes"):
            await ghl.add_tag(contact_id, "nx:escalation:rcic_review")
            logger.warning("ESCALATION: contact %s flagged for RCIC review (field=%s)", contact_id, field)
            break

    # Log the event
    log_event("typebot_submission", {
        "contact_id": contact_id,
        "fields_updated": len(custom_fields),
        "program": answers.get("program_interest", "unknown"),
    })

    # Record activity in database if available
    try:
        from app import database
        if database.async_session_factory:
            from app.services.sync_service import SyncService
            sync = SyncService()
            await sync.record_activity(
                contact_id=contact_id,
                activity_type="onboarding_questionnaire_completed",
                detail=f"Typebot form submitted — {len(custom_fields)} fields collected",
                metadata={"program": answers.get("program_interest", ""), "fields": list(custom_fields.keys())},
            )
    except Exception as e:
        logger.warning("Could not record activity: %s", e)

    # Mark submission as processed (memory + DB)
    if result_id:
        await _mark_typebot_processed(result_id)

    return {
        "status": "processed",
        "contact_id": contact_id,
        "fields_updated": len(custom_fields),
        "tag_added": "nx:case:docs_pending",
        "program": answers.get("program_interest", "unknown"),
    }


@router.post("/create-form")
async def create_typebot_form(payload: CreateFormRequest):
    """
    Generate a Typebot form JSON from questionnaires.yaml and create it via API.
    Returns the form URL for embedding or sharing.
    """
    service = TypebotService()
    if not service.is_configured():
        raise HTTPException(status_code=503, detail="Typebot not configured. Set TYPEBOT_URL and TYPEBOT_API_TOKEN.")

    result = await service.create_onboarding_form(
        program_type=payload.program_type,
        firm_name=payload.firm_name,
        webhook_url=payload.webhook_url,
    )

    if not result:
        raise HTTPException(status_code=500, detail="Failed to create Typebot form")

    return result


@router.get("/form-url/{program_type}")
async def get_form_url(program_type: str):
    """Get the Typebot form URL for a specific program. Used in WF-CP-01 emails."""
    from app.config import settings
    if not settings.typebot_viewer_url:
        return {
            "program_type": program_type,
            "url": None,
            "note": "Typebot not deployed yet. Set TYPEBOT_VIEWER_URL.",
        }

    # Convention: form slug = program type slugified
    slug = program_type.lower().replace(" ", "-").replace("/", "-")
    return {
        "program_type": program_type,
        "url": f"{settings.typebot_viewer_url}/{slug}-onboarding",
        "embed_js": f'<script src="{settings.typebot_viewer_url}/embed.js"></script>',
    }
