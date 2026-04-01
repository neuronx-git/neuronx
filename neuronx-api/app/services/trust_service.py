"""
Trust Boundary Enforcement Service

Scans AI transcripts for compliance violations and escalation triggers.
BINDING: docs/04_compliance/trust_boundaries.md

This service is the last line of defense before AI interaction data is used.
"""

from pydantic import BaseModel
from typing import Optional
import re
import logging

from app.utils.compliance_log import log_event

logger = logging.getLogger("neuronx.trust")


# Mandatory escalation triggers (from trust_boundaries.md Section 3)
ESCALATION_PATTERNS = {
    "eligibility_question": [
        r"am i eligible",
        r"do i qualify",
        r"can i apply",
        r"will i get approved",
        r"what are my chances",
    ],
    "deportation_removal": [
        r"deport",
        r"removal order",
        r"deportation",
        r"removal process",
        r"being removed",
    ],
    "inadmissibility": [
        r"inadmissib",
        r"banned from canada",
        r"visa ban",
        r"criminally inadmissible",
    ],
    "fraud_misrepresentation": [
        r"fake document",
        r"false document",
        r"misrepresentation",
        r"fraud",
        r"lie on",
    ],
    "emotional_distress": [
        r"desperate",
        r"crying",
        r"suicidal",
        r"very scared",
        r"terrified",
        r"please help me",
    ],
    "explicit_human_request": [
        r"speak to a human",
        r"talk to a person",
        r"real person",
        r"not a robot",
        r"human agent",
        r"transfer me",
    ],
}

# AI response violations — AI should never say these
AI_VIOLATION_PATTERNS = {
    "eligibility_assessment": [
        r"you (are|would be) eligible",
        r"you qualify for",
        r"you should apply for",
        r"your chances are",
        r"you will (likely |probably )?get approved",
    ],
    "legal_advice": [
        r"the law says",
        r"legally you",
        r"according to immigration law",
        r"ircc requires you to",
    ],
    "outcome_promises": [
        r"guarantee",
        r"100% success",
        r"definitely get",
        r"will be approved",
    ],
}


class TrustCheckResult(BaseModel):
    contact_id: str
    call_id: Optional[str] = None
    requires_escalation: bool
    flags: list[str]
    violations: list[str]  # AI response violations
    escalation_reason: Optional[str] = None
    compliant: bool


class TrustService:
    """
    Checks transcripts for compliance with trust_boundaries.md.
    Must be called after every AI interaction.
    """

    def check_transcript(
        self,
        transcript: str,
        contact_id: str,
        call_id: Optional[str] = None,
    ) -> TrustCheckResult:
        transcript_lower = transcript.lower()
        flags = []
        violations = []

        # Check prospect statements for escalation triggers
        for trigger_type, patterns in ESCALATION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, transcript_lower):
                    flags.append(trigger_type)
                    break

        # Check AI responses for violations
        for violation_type, patterns in AI_VIOLATION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, transcript_lower):
                    violations.append(violation_type)
                    logger.error(
                        "TRUST VIOLATION: %s detected in transcript for contact=%s call=%s",
                        violation_type, contact_id, call_id
                    )
                    break

        requires_escalation = len(flags) > 0
        escalation_reason = f"Triggers: {', '.join(flags)}" if flags else None

        result = TrustCheckResult(
            contact_id=contact_id,
            call_id=call_id,
            requires_escalation=requires_escalation,
            flags=flags,
            violations=violations,
            escalation_reason=escalation_reason,
            compliant=len(violations) == 0,
        )

        log_event("trust_check", {
            "contact_id": contact_id,
            "call_id": call_id,
            "requires_escalation": requires_escalation,
            "flags": flags,
            "violations": violations,
        })

        return result

    async def get_audit_log(self, contact_id: Optional[str], limit: int) -> list:
        """Query compliance audit log. Full implementation in Week 4."""
        # TODO: Implement proper log storage (SQLite or PostgreSQL)
        return []
