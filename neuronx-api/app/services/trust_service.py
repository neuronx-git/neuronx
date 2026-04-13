"""
Trust Boundary Enforcement Service

Scans AI transcripts for compliance violations and escalation triggers.
BINDING: docs/04_compliance/trust_boundaries.md

Patterns loaded from config/trust.yaml — single source of truth.
This service is the last line of defense before AI interaction data is used.
"""

from pydantic import BaseModel
from typing import Optional
import re
import logging

from app.utils.compliance_log import log_event
from app.config_loader import load_yaml_config

logger = logging.getLogger("neuronx.trust")


def _load_trust_patterns() -> tuple[dict, dict]:
    """Load escalation and violation patterns from config/trust.yaml."""
    try:
        cfg = load_yaml_config("trust")
        escalation = cfg.get("escalation_triggers", {})
        violations = cfg.get("ai_violations", {})
        return escalation, violations
    except Exception as e:
        logger.error("Failed to load trust config: %s — using empty patterns (UNSAFE)", e)
        return {}, {}


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

    Patterns are loaded from config/trust.yaml (not hardcoded).
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

        escalation_patterns, violation_patterns = _load_trust_patterns()

        # Check prospect statements for escalation triggers
        for trigger_type, patterns in escalation_patterns.items():
            for pattern in patterns:
                if re.search(pattern, transcript_lower):
                    flags.append(trigger_type)
                    break

        # Check AI responses for violations
        for violation_type, patterns in violation_patterns.items():
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
        """Query compliance audit log from PostgreSQL activities table."""
        # TODO: Query activities table for trust_check events
        return []
