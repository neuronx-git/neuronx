"""
Webhook Receiver
Handles inbound events from GHL and VAPI.

GHL Webhook: Form submissions, appointment events, tag changes.
VAPI Webhook: End-of-call reports with transcript + structured data.

Data flow:
  VAPI call ends → POST /webhooks/voice → extract R1-R5 → score → update GHL → trigger WF-04B
  GHL event      → POST /webhooks/ghl   → log + analytics
"""

from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
from datetime import datetime
import logging
import json
import hmac
import hashlib

from app.services.ghl_client import GHLClient
from app.services.scoring_service import ScoringService
from app.services.trust_service import TrustService
from app.utils.compliance_log import log_event
from app.config import settings

router = APIRouter()
logger = logging.getLogger("neuronx.webhooks")


# ── GHL Webhook ──

@router.post("/ghl")
async def receive_ghl_webhook(
    request: Request,
    x_ghl_signature: Optional[str] = Header(None),
):
    """
    Receive GHL events: form submissions, appointment updates, tag changes.
    NeuronX logs events and triggers briefings — GHL workflows handle the rest.
    """
    body = await request.body()
    payload = json.loads(body)

    event_type = payload.get("type", "unknown")
    contact_id = payload.get("contactId") or payload.get("contact_id")

    logger.info("GHL webhook: type=%s contact=%s", event_type, contact_id)
    log_event("ghl_webhook", {"type": event_type, "contact_id": contact_id})

    # Route by event type
    if event_type in ("ContactCreate", "ContactCreated"):
        return {"status": "ok", "action": "contact_logged"}

    if event_type in ("AppointmentCreate", "AppointmentBooked", "appointment.booked"):
        appointment_id = payload.get("appointmentId") or payload.get("id")
        logger.info("Appointment booked: %s — briefing will be triggered by scheduler", appointment_id)
        return {"status": "ok", "action": "appointment_logged", "appointment_id": appointment_id}

    if event_type in ("TagAdded", "tag.added", "ContactTagUpdate"):
        tag_name = payload.get("tag", payload.get("tags", [""])[0] if isinstance(payload.get("tags"), list) else "")
        if isinstance(tag_name, dict):
            tag_name = tag_name.get("name", "")
        logger.info("Tag event: contact=%s tag=%s", contact_id, tag_name)
        return {"status": "ok", "action": "tag_logged", "tag": tag_name}

    return {"status": "ok", "action": "no_handler", "type": event_type}


# ── VAPI Webhook ──

@router.post("/voice")
async def receive_voice_webhook(request: Request):
    """
    Receive VAPI webhook events.

    VAPI sends different event types during a call lifecycle:
    - assistant-request: VAPI asks for assistant config (for dynamic assistants)
    - function-call: VAPI invokes a server-side function (collect_readiness_data)
    - status-update: Call status changes (queued, ringing, in-progress, ended)
    - end-of-call-report: Final report with transcript, analysis, structured data
    - hang: Notification that call hung up
    - transcript: Real-time transcript updates

    The critical event is end-of-call-report — it contains:
    - message.transcript: Full conversation text
    - message.analysis.summary: LLM-generated call summary
    - message.analysis.structuredData: R1-R5 extracted data (via analysisPlan)
    - message.call.id: VAPI call ID
    - message.call.metadata.ghl_contact_id: GHL contact reference
    """
    body = await request.body()
    payload = json.loads(body)

    # VAPI wraps everything in a "message" object
    message = payload.get("message", payload)
    event_type = message.get("type", payload.get("type", "unknown"))

    logger.info("VAPI webhook: type=%s", event_type)

    # ── Function call (VAPI asks NeuronX to execute a function) ──
    if event_type == "function-call":
        return await _handle_function_call(message)

    # ── End of call report (the big one) ──
    if event_type == "end-of-call-report":
        return await _handle_end_of_call(message)

    # ── Status updates (log only) ──
    if event_type == "status-update":
        status = message.get("status", "unknown")
        call_id = message.get("call", {}).get("id", "unknown")
        logger.info("VAPI status: call=%s status=%s", call_id, status)
        log_event("vapi_status", {"call_id": call_id, "status": status})
        return {"status": "ok", "action": "status_logged"}

    # ── Transcript updates (log only, no action) ──
    if event_type in ("transcript", "conversation-update"):
        return {"status": "ok", "action": "transcript_logged"}

    # ── Assistant request (return assistant config if using dynamic) ──
    if event_type == "assistant-request":
        # For now, we use static assistant config in VAPI dashboard
        return {"status": "ok", "action": "not_using_dynamic_assistant"}

    log_event("vapi_unhandled", {"type": event_type})
    return {"status": "ok", "action": "no_handler", "type": event_type}


async def _handle_function_call(message: dict) -> dict:
    """
    Handle VAPI function-call events.
    VAPI calls this when the assistant invokes a server-side function.
    We must return the function result synchronously.
    """
    fn_call = message.get("functionCall", {})
    fn_name = fn_call.get("name", "")
    fn_params = fn_call.get("parameters", {})

    logger.info("VAPI function call: %s params=%s", fn_name, list(fn_params.keys()))

    if fn_name == "collect_readiness_data":
        # VAPI collected R1-R5 from the caller — acknowledge receipt
        log_event("vapi_readiness_collected", fn_params)
        return {
            "result": "Readiness data received. Thank you for providing that information. Let me check if we can schedule a consultation for you."
        }

    if fn_name == "book_consultation":
        # Return booking link for the caller
        booking_url = f"https://api.leadconnectorhq.com/widget/booking/{settings.ghl_calendar_id or 'To1U2KbcvJ0EAX0RGKHS'}"
        return {
            "result": f"I can help you book a consultation. You'll receive a text message with a link to choose a time that works for you. The booking link is: {booking_url}"
        }

    if fn_name == "transfer_to_human":
        log_event("vapi_human_transfer", fn_params)
        return {
            "result": "I'm transferring you to a team member now. Please hold for a moment."
        }

    logger.warning("Unknown VAPI function: %s", fn_name)
    return {"result": "I'll make a note of that and have our team follow up."}


async def _handle_end_of_call(message: dict) -> dict:
    """
    Process VAPI end-of-call-report.

    This is where we:
    1. Extract structured data (R1-R5) from the call analysis
    2. Run trust boundary check on transcript
    3. Score the lead's readiness
    4. Update GHL contact with fields + tags
    5. Add call summary as GHL note
    """
    call_data = message.get("call", {})
    call_id = call_data.get("id", "unknown")
    metadata = call_data.get("metadata", {})
    contact_id = metadata.get("ghl_contact_id")

    # Transcript
    transcript = message.get("transcript", "")
    if not transcript:
        # Some VAPI versions nest transcript differently
        artifact = message.get("artifact", {})
        transcript = artifact.get("transcript", "")

    # Analysis (LLM-processed)
    analysis = message.get("analysis", {})
    summary = analysis.get("summary", "No summary available")

    # Structured data: R1-R5 extracted by VAPI's analysisPlan
    structured_data = analysis.get("structuredData", {})

    logger.info(
        "VAPI end-of-call: call_id=%s contact=%s structured_keys=%s",
        call_id, contact_id, list(structured_data.keys()),
    )

    log_event("vapi_end_of_call", {
        "call_id": call_id,
        "contact_id": contact_id,
        "has_transcript": bool(transcript),
        "has_structured_data": bool(structured_data),
        "summary_length": len(summary),
    })

    if not contact_id:
        logger.warning("No ghl_contact_id in VAPI call metadata — call_id=%s", call_id)
        return {"status": "warning", "message": "no_contact_id", "call_id": call_id}

    # 1. Trust boundary check
    trust_service = TrustService()
    trust_result = trust_service.check_transcript(transcript, contact_id, call_id)

    if trust_result.requires_escalation:
        logger.warning("Trust escalation: contact=%s flags=%s", contact_id, trust_result.flags)
        ghl = GHLClient()
        await ghl.add_tag(contact_id, "nx:human_escalation")
        await ghl.add_note(
            contact_id,
            f"[AI ESCALATION] Call {call_id}\n"
            f"Triggers: {', '.join(trust_result.flags)}\n"
            f"Requires RCIC review before proceeding."
        )
        # Still score the lead but mark as complex
        # Fall through to scoring below

    if trust_result.violations:
        logger.error("TRUST VIOLATION in call %s: %s", call_id, trust_result.violations)
        await GHLClient().add_note(
            contact_id,
            f"[TRUST VIOLATION] Call {call_id}\n"
            f"Violations: {', '.join(trust_result.violations)}\n"
            f"Review required — AI may have provided unauthorized advice."
        )

    # 2. Extract R1-R5 from structured data
    readiness_data = _extract_readiness(structured_data, transcript)

    # 3. Score readiness
    scoring_service = ScoringService()
    score = scoring_service.score(
        contact_id=contact_id,
        call_id=call_id,
        **readiness_data,
    )

    # If trust escalation already triggered, force complex outcome
    if trust_result.requires_escalation and score.outcome.value != "ready_complex":
        score.outcome = score.outcome.__class__("ready_complex")
        if "nx:human_escalation" not in score.ghl_tags_to_add:
            score.ghl_tags_to_add.append("nx:human_escalation")

    # 4. Update GHL
    ghl = GHLClient()
    await ghl.update_custom_fields(contact_id, score.ghl_fields_to_update)
    await ghl.add_tags(contact_id, score.ghl_tags_to_add + ["nx:contacted"])

    # 5. Add call summary note
    await ghl.add_note(
        contact_id,
        f"AI Call Summary — {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC\n"
        f"Call ID: {call_id}\n"
        f"{'─' * 40}\n"
        f"{summary}\n"
        f"{'─' * 40}\n"
        f"Readiness: {score.outcome.value} (score: {score.score}/10)\n"
        f"Flags: {', '.join(score.flags) if score.flags else 'None'}\n"
        f"Confidence: {score.confidence:.0%}"
    )

    log_event("call_processed", {
        "call_id": call_id,
        "contact_id": contact_id,
        "outcome": score.outcome.value,
        "score": score.score,
        "flags": score.flags,
        "trust_escalation": trust_result.requires_escalation,
        "trust_violations": trust_result.violations,
    })

    return {
        "status": "ok",
        "action": "scored",
        "call_id": call_id,
        "contact_id": contact_id,
        "outcome": score.outcome.value,
        "score": score.score,
        "tags_added": score.ghl_tags_to_add,
    }


def _extract_readiness(structured_data: dict, transcript: str) -> dict:
    """
    Extract R1-R5 readiness data from VAPI structured data.

    VAPI's analysisPlan.structuredDataPlan extracts these fields post-call:
    - program_interest: str (mapped from caller's stated interest)
    - current_location: str (in_canada / outside_canada)
    - timeline_urgency: str (urgent / near_term / medium / long_term)
    - prior_applications: str (none / approved / has_refusal / complex)
    - budget_awareness: str (aware / unaware / unclear)
    """
    if not structured_data:
        return {"transcript_excerpt": transcript[:1000] if transcript else None}

    return {
        "r1_program_interest": structured_data.get("program_interest"),
        "r2_current_location": structured_data.get("current_location"),
        "r3_timeline_urgency": structured_data.get("timeline_urgency"),
        "r4_prior_applications": structured_data.get("prior_applications"),
        "r5_budget_awareness": structured_data.get("budget_awareness"),
        "transcript_excerpt": transcript[:1000] if transcript else None,
    }
