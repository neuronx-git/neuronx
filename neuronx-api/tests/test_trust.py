"""
Tests for Trust Boundary Enforcement
These must pass before any AI call integration goes live.
"""

import pytest
from app.services.trust_service import TrustService


def test_eligibility_question_triggers_escalation():
    service = TrustService()
    result = service.check_transcript(
        transcript="Prospect: Am I eligible for Express Entry? AI: Let me check that for you...",
        contact_id="test-001",
    )
    assert result.requires_escalation is True
    assert "eligibility_question" in result.flags


def test_deportation_mention_triggers_escalation():
    service = TrustService()
    result = service.check_transcript(
        transcript="I was deported from Canada 2 years ago. Can I come back?",
        contact_id="test-002",
    )
    assert result.requires_escalation is True
    assert "deportation_removal" in result.flags


def test_explicit_human_request_triggers_escalation():
    service = TrustService()
    result = service.check_transcript(
        transcript="I want to speak to a human agent please.",
        contact_id="test-003",
    )
    assert result.requires_escalation is True
    assert "explicit_human_request" in result.flags


def test_clean_transcript_passes():
    service = TrustService()
    result = service.check_transcript(
        transcript="Hi, I'm interested in Express Entry. I'm currently in Canada and want to apply in 3 months.",
        contact_id="test-004",
    )
    assert result.requires_escalation is False
    assert result.flags == []
    assert result.compliant is True


def test_ai_eligibility_assessment_violation():
    service = TrustService()
    result = service.check_transcript(
        transcript="AI: Based on your profile, you are eligible for Express Entry!",
        contact_id="test-005",
    )
    assert result.compliant is False
    assert "eligibility_assessment" in result.violations


def test_fraud_mention_triggers_escalation():
    service = TrustService()
    result = service.check_transcript(
        transcript="My agent told me to use fake documents on my application.",
        contact_id="test-006",
    )
    assert result.requires_escalation is True
    assert "fraud_misrepresentation" in result.flags
