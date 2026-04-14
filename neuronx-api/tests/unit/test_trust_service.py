"""
Unit Tests — Trust Service

Tests the trust boundary enforcement: escalation trigger detection and
AI violation scanning. Patterns loaded from config/trust.yaml.
"""

import pytest
from app.services.trust_service import TrustService


@pytest.fixture
def trust():
    return TrustService()


# ── Escalation Triggers ──────────────────────────────────────────────


@pytest.mark.unit
class TestEscalationTriggers:
    """Tests for the 6 escalation trigger categories."""

    @pytest.mark.parametrize("phrase", [
        "Am I eligible for Express Entry?",
        "Do I qualify for PR?",
        "Can I apply for citizenship?",
        "Will I get approved?",
        "What are my chances of getting a visa?",
    ])
    def test_eligibility_question_triggers(self, trust, phrase):
        """Eligibility questions trigger escalation."""
        result = trust.check_transcript(phrase, contact_id="t1")
        assert result.requires_escalation is True
        assert "eligibility_question" in result.flags

    @pytest.mark.parametrize("phrase", [
        "I was deported last year.",
        "I have a removal order.",
        "They started deportation proceedings.",
        "The removal process has begun.",
        "I am being removed from the country.",
    ])
    def test_deportation_removal_triggers(self, trust, phrase):
        """Deportation/removal mentions trigger escalation."""
        result = trust.check_transcript(phrase, contact_id="t2")
        assert result.requires_escalation is True
        assert "deportation_removal" in result.flags

    @pytest.mark.parametrize("phrase", [
        "I was found inadmissible.",
        "I am banned from Canada.",
        "I have a visa ban.",
        "I am criminally inadmissible.",
    ])
    def test_inadmissibility_triggers(self, trust, phrase):
        """Inadmissibility mentions trigger escalation."""
        result = trust.check_transcript(phrase, contact_id="t3")
        assert result.requires_escalation is True
        assert "inadmissibility" in result.flags

    @pytest.mark.parametrize("phrase", [
        "I submitted a fake document.",
        "They said it was a false document.",
        "I was accused of misrepresentation.",
        "There is a fraud investigation.",
        "Should I lie on my application?",
    ])
    def test_fraud_misrepresentation_triggers(self, trust, phrase):
        """Fraud/misrepresentation mentions trigger escalation."""
        result = trust.check_transcript(phrase, contact_id="t4")
        assert result.requires_escalation is True
        assert "fraud_misrepresentation" in result.flags

    @pytest.mark.parametrize("phrase", [
        "I am desperate for help.",
        "I was crying all night.",
        "I feel suicidal about this.",
        "I am very scared about the outcome.",
        "I am terrified of being deported.",
        "Please help me, I have no one.",
    ])
    def test_emotional_distress_triggers(self, trust, phrase):
        """Emotional distress indicators trigger escalation."""
        result = trust.check_transcript(phrase, contact_id="t5")
        assert result.requires_escalation is True
        assert "emotional_distress" in result.flags

    @pytest.mark.parametrize("phrase", [
        "I want to speak to a human.",
        "Let me talk to a person.",
        "Can I speak to a real person?",
        "You are not a robot, right?",
        "I want a human agent.",
        "Transfer me to someone.",
    ])
    def test_explicit_human_request_triggers(self, trust, phrase):
        """Explicit human requests trigger escalation."""
        result = trust.check_transcript(phrase, contact_id="t6")
        assert result.requires_escalation is True
        assert "explicit_human_request" in result.flags


# ── AI Violations ────────────────────────────────────────────────────


@pytest.mark.unit
class TestAIViolations:
    """Tests for the 3 AI violation categories."""

    @pytest.mark.parametrize("phrase", [
        "You are eligible for Express Entry.",
        "You would be eligible for PR.",
        "You qualify for the skilled worker program.",
        "You should apply for work permit.",
        "Your chances are very good.",
        "You will likely get approved.",
        "You will probably get approved for PR.",
    ])
    def test_eligibility_assessment_violations(self, trust, phrase):
        """AI stating eligibility is a violation."""
        result = trust.check_transcript(phrase, contact_id="v1")
        assert result.compliant is False
        assert "eligibility_assessment" in result.violations

    @pytest.mark.parametrize("phrase", [
        "The law says you need to apply within 90 days.",
        "Legally you must have a valid work permit.",
        "According to immigration law, you need a sponsor.",
        "IRCC requires you to submit biometrics.",
    ])
    def test_legal_advice_violations(self, trust, phrase):
        """AI giving legal advice is a violation."""
        result = trust.check_transcript(phrase, contact_id="v2")
        assert result.compliant is False
        assert "legal_advice" in result.violations

    @pytest.mark.parametrize("phrase", [
        "I guarantee you will get PR.",
        "We have 100% success rate.",
        "You will definitely get approved.",
        "Your application will be approved for sure.",
    ])
    def test_outcome_promise_violations(self, trust, phrase):
        """AI making outcome promises is a violation."""
        result = trust.check_transcript(phrase, contact_id="v3")
        assert result.compliant is False
        assert "outcome_promises" in result.violations


# ── Clean Transcripts ────────────────────────────────────────────────


@pytest.mark.unit
class TestCleanTranscripts:
    """Tests for transcripts with no issues."""

    def test_clean_transcript_no_flags(self, trust):
        """Clean transcript has no escalation flags."""
        result = trust.check_transcript(
            "Hello, I am interested in immigrating to Canada. I want to learn about Express Entry.",
            contact_id="clean1",
        )
        assert result.requires_escalation is False
        assert result.flags == []

    def test_clean_transcript_no_violations(self, trust):
        """Clean transcript has no violations."""
        result = trust.check_transcript(
            "I can help you book a consultation with our licensed consultant.",
            contact_id="clean2",
        )
        assert result.compliant is True
        assert result.violations == []

    def test_clean_transcript_full_result(self, trust):
        """Clean transcript returns a complete, correct result."""
        result = trust.check_transcript(
            "Welcome to NeuronX. How can I assist you today?",
            contact_id="clean3",
            call_id="call-clean",
        )
        assert result.contact_id == "clean3"
        assert result.call_id == "call-clean"
        assert result.requires_escalation is False
        assert result.compliant is True
        assert result.escalation_reason is None
        assert result.flags == []
        assert result.violations == []


# ── Mixed Transcripts ────────────────────────────────────────────────


@pytest.mark.unit
class TestMixedTranscripts:
    """Tests for transcripts with both escalation triggers and violations."""

    def test_escalation_and_violation_both_detected(self, trust):
        """Transcript with both a prospect trigger and an AI violation."""
        transcript = (
            "Prospect: Am I eligible for Express Entry?\n"
            "AI: You are eligible for Express Entry."
        )
        result = trust.check_transcript(transcript, contact_id="mix1")
        assert result.requires_escalation is True
        assert "eligibility_question" in result.flags
        assert result.compliant is False
        assert "eligibility_assessment" in result.violations

    def test_multiple_escalation_categories(self, trust):
        """Transcript hitting multiple escalation categories."""
        transcript = (
            "I was deported from Canada. I am desperate for help. "
            "Please transfer me to a human agent."
        )
        result = trust.check_transcript(transcript, contact_id="mix2")
        assert result.requires_escalation is True
        # Should flag deportation, emotional_distress, explicit_human_request
        assert len(result.flags) >= 3

    def test_escalation_reason_string(self, trust):
        """Escalation reason contains trigger names."""
        transcript = "Am I eligible for Express Entry?"
        result = trust.check_transcript(transcript, contact_id="mix3")
        assert result.escalation_reason is not None
        assert "eligibility_question" in result.escalation_reason


# ── Case Sensitivity ─────────────────────────────────────────────────


@pytest.mark.unit
class TestCaseSensitivity:
    """Patterns are matched case-insensitively."""

    def test_uppercase_escalation(self, trust):
        """Uppercase text still triggers escalation."""
        result = trust.check_transcript(
            "AM I ELIGIBLE FOR PR?",
            contact_id="case1",
        )
        assert result.requires_escalation is True

    def test_mixed_case_violation(self, trust):
        """Mixed case text still detects violations."""
        result = trust.check_transcript(
            "You Are Eligible for Express Entry.",
            contact_id="case2",
        )
        assert result.compliant is False

    def test_lowercase_works(self, trust):
        """Lowercase text matches patterns."""
        result = trust.check_transcript(
            "you are eligible for pr",
            contact_id="case3",
        )
        assert result.compliant is False


# ── Empty / Edge Cases ───────────────────────────────────────────────


@pytest.mark.unit
class TestEdgeCases:
    """Edge cases for trust checking."""

    def test_empty_transcript(self, trust):
        """Empty transcript -> clean result."""
        result = trust.check_transcript("", contact_id="edge1")
        assert result.requires_escalation is False
        assert result.compliant is True

    def test_contact_id_preserved(self, trust):
        """Contact ID is passed through."""
        result = trust.check_transcript("hello", contact_id="my-id-123")
        assert result.contact_id == "my-id-123"

    def test_call_id_preserved(self, trust):
        """Call ID is passed through."""
        result = trust.check_transcript("hello", contact_id="c1", call_id="call-999")
        assert result.call_id == "call-999"

    def test_call_id_none_by_default(self, trust):
        """Call ID defaults to None."""
        result = trust.check_transcript("hello", contact_id="c1")
        assert result.call_id is None

    def test_result_is_pydantic_model(self, trust):
        """Return type is TrustCheckResult pydantic model."""
        from app.services.trust_service import TrustCheckResult
        result = trust.check_transcript("hello", contact_id="c1")
        assert isinstance(result, TrustCheckResult)
