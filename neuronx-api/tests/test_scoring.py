"""
Tests for Lead Readiness Scoring Service.
Score is 0-100 with WF-04B routing: >=70 high, 40-69 med, <40 low.
"""

import pytest
from app.services.scoring_service import ScoringService
from app.models.readiness import ReadinessOutcome


@pytest.fixture
def scorer():
    return ScoringService()


def test_fully_answered_standard_lead(scorer):
    """All 5 dimensions answered, medium timeline, budget aware → high score."""
    result = scorer.score(
        contact_id="test-001",
        r1_program_interest="Express Entry",
        r2_current_location="In Canada",
        r3_timeline_urgency="Medium",
        r4_prior_applications="None",
        r5_budget_awareness="Aware",
    )
    assert result.outcome == ReadinessOutcome.READY_STANDARD
    assert result.score >= 70
    assert "nx:score:high" in result.ghl_tags_to_add
    assert "nx:assessment:complete" in result.ghl_tags_to_add
    assert result.confidence == 1.0


def test_urgent_timeline_lead(scorer):
    """Urgent timeline → READY_URGENT with urgency bonus."""
    result = scorer.score(
        contact_id="test-002",
        r1_program_interest="Spousal Sponsorship",
        r2_current_location="Outside Canada",
        r3_timeline_urgency="Urgent",
        r4_prior_applications="None",
        r5_budget_awareness="Aware",
    )
    assert result.outcome == ReadinessOutcome.READY_URGENT
    assert result.score >= 70
    assert "nx:assessment:complete" in result.ghl_tags_to_add
    assert "nx:urgent" in result.ghl_tags_to_add
    assert "urgent_timeline" in result.flags


def test_complexity_keyword_escalation(scorer):
    """Deportation in transcript → human escalation regardless of score."""
    result = scorer.score(
        contact_id="test-003",
        r1_program_interest="Express Entry",
        r2_current_location="In Canada",
        r3_timeline_urgency="Urgent",
        r4_prior_applications="Has Refusal",
        r5_budget_awareness="Aware",
        transcript_excerpt="I was deported from Canada 3 years ago and want to come back.",
    )
    assert result.outcome == ReadinessOutcome.READY_COMPLEX
    assert "nx:human_escalation" in result.ghl_tags_to_add
    assert "requires_human_escalation" in result.flags


def test_insufficient_dimensions_not_ready(scorer):
    """Only 1 dimension → low score, not ready."""
    result = scorer.score(
        contact_id="test-004",
        r1_program_interest="Other",
    )
    assert result.outcome == ReadinessOutcome.NOT_READY
    assert result.score < 40
    assert result.confidence < 0.5
    assert "nx:score:low" in result.ghl_tags_to_add
    assert "nx:not_ready" in result.ghl_tags_to_add


def test_medium_score_lead(scorer):
    """3 dimensions with long-term timeline → medium score range."""
    result = scorer.score(
        contact_id="test-005",
        r1_program_interest="Work Permit",
        r2_current_location="Outside Canada",
        r3_timeline_urgency="Long-term",
    )
    # 16 + 16 + 16 - 5 = 43
    assert 40 <= result.score < 70
    assert "nx:score:med" in result.ghl_tags_to_add


def test_ghl_fields_populated(scorer):
    """GHL custom fields are populated correctly."""
    result = scorer.score(
        contact_id="test-006",
        r1_program_interest="Study Permit",
        r2_current_location="Outside Canada",
        r3_timeline_urgency="Near-term",
        r4_prior_applications="None",
        r5_budget_awareness="Unaware",
    )
    fields = result.ghl_fields_to_update
    assert fields["ai_program_interest"] == "Study Permit"
    assert fields["ai_current_location"] == "Outside Canada"
    assert fields["ai_readiness_outcome"] in [o.value for o in ReadinessOutcome]
    assert "ai_readiness_score" in fields
    assert "assessment_completed_at" in fields
    assert fields["assessed_by"] == "neuronx-api"


def test_no_dimensions(scorer):
    """No dimensions at all → 0 score, not ready."""
    result = scorer.score(contact_id="test-007")
    assert result.score == 0
    assert result.outcome == ReadinessOutcome.NOT_READY
    assert result.confidence == 0.0


def test_prior_refusal_penalty(scorer):
    """Prior refusal reduces score vs clean history."""
    result_clean = scorer.score(
        contact_id="test-008a",
        r1_program_interest="PR Renewal",
        r2_current_location="In Canada",
        r3_timeline_urgency="Medium",
        r4_prior_applications="None",
        r5_budget_awareness="Aware",
    )
    result_refusal = scorer.score(
        contact_id="test-008b",
        r1_program_interest="PR Renewal",
        r2_current_location="In Canada",
        r3_timeline_urgency="Medium",
        r4_prior_applications="Has Refusal",
        r5_budget_awareness="Aware",
    )
    assert result_refusal.score < result_clean.score
    assert "prior_refusal" in result_refusal.flags


def test_budget_aware_bonus(scorer):
    """Budget aware gets bonus vs unaware."""
    result_aware = scorer.score(
        contact_id="test-009a",
        r1_program_interest="Express Entry",
        r2_current_location="In Canada",
        r5_budget_awareness="Aware",
    )
    result_unaware = scorer.score(
        contact_id="test-009b",
        r1_program_interest="Express Entry",
        r2_current_location="In Canada",
        r5_budget_awareness="Unaware",
    )
    assert result_aware.score > result_unaware.score
    assert "budget_education_needed" in result_unaware.flags
