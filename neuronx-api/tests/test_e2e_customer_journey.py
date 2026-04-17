"""
E2E Customer Journey Tests — covers happy path, alternate flows, and edge cases.

Tests the full customer lifecycle:
  Inquiry → Score → Case Initiation → Stage Transitions → Decision → Close

Tests against the FastAPI TestClient (no external services required).
GHL calls are mocked.
"""

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


# ── Happy Path ────────────────────────────────────────────────────────────


class TestHappyPath:
    """Full customer journey: inquiry → scoring → case → lifecycle → close."""

    def test_scoring_full_r1_r5(self, client):
        """Score a lead with all 5 dimensions."""
        r = client.post("/score/lead", json={
            "contact_id": "test-001",
            "r1_program_interest": "Express Entry",
            "r2_current_location": "Outside Canada",
            "r3_timeline_urgency": "Near-term",
            "r4_prior_applications": "None",
            "r5_budget_awareness": "Aware",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["outcome"] == "ready_standard"
        assert data["score"] >= 70
        assert data["confidence"] == 1.0
        assert "nx:score:high" in data["ghl_tags_to_add"]
        assert "nx:assessment:complete" in data["ghl_tags_to_add"]

    def test_scoring_urgent_lead(self, client):
        """Urgent timeline should produce ready_urgent outcome."""
        r = client.post("/score/lead", json={
            "contact_id": "test-002",
            "r1_program_interest": "Work Permit",
            "r2_current_location": "In Canada",
            "r3_timeline_urgency": "Urgent",
            "r4_prior_applications": "None",
            "r5_budget_awareness": "Aware",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["outcome"] == "ready_urgent"
        assert "nx:urgent" in data["ghl_tags_to_add"]

    def test_form_scoring_preliminary(self, client):
        """Form scoring should cap at 48 and mark as upgradeable."""
        r = client.post("/score/form", json={
            "contact_id": "test-003",
            "program_interest": "Study Permit",
            "current_location": "Outside Canada",
            "timeline": "Medium",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["preliminary_score"] <= 48
        assert data["score_source"] == "form"
        assert data["can_upgrade"] is True
        assert data["dimensions_captured"] == 3

    def test_case_initiate_invalid_program(self, client):
        """Initiating a case with invalid program should fail."""
        with patch("app.services.case_service.GHLClient") as mock_ghl:
            mock_ghl.return_value = AsyncMock()
            r = client.post("/cases/initiate", json={
                "contact_id": "test-001",
                "program_type": "Martian Visa",
            })
        assert r.status_code == 400
        assert "Unknown program_type" in r.json()["detail"]

    def test_transitions_complete(self, client):
        """State machine should have exactly 10 stages."""
        r = client.get("/cases/transitions")
        data = r.json()
        assert len(data["stages"]) == 10
        assert data["transitions"]["closed"] == []
        # Every non-closed stage should allow closing
        for stage, transitions in data["transitions"].items():
            if stage != "closed":
                assert "closed" in transitions, f"{stage} should allow transition to closed"

    def test_program_forms_all_programs(self, client):
        """Every configured program should return IRCC forms."""
        programs = ["Express Entry", "Spousal Sponsorship", "Work Permit",
                     "Study Permit", "LMIA", "PR Renewal", "Citizenship", "Visitor Visa"]
        for prog in programs:
            r = client.get(f"/cases/forms/{prog}")
            assert r.status_code == 200, f"Failed for {prog}"
            data = r.json()
            assert len(data["forms"]) > 0, f"No forms for {prog}"

    def test_questionnaire_slug_normalization(self, client):
        """Slug 'express-entry' should resolve to 'Express Entry'."""
        r = client.get("/cases/questionnaire/express-entry")
        assert r.status_code == 200
        assert r.json()["program_type"] == "Express Entry"

    def test_questionnaire_all_programs(self, client):
        """All 8 programs should return questionnaires with common + specific questions."""
        slugs = ["express-entry", "spousal-sponsorship", "work-permit",
                  "study-permit", "lmia", "pr-renewal", "citizenship", "visitor-visa"]
        for slug in slugs:
            r = client.get(f"/cases/questionnaire/{slug}")
            assert r.status_code == 200, f"Failed for {slug}"
            data = r.json()
            assert data["common_count"] > 0
            assert data["program_specific_count"] > 0
            assert data["total_questions"] == data["common_count"] + data["program_specific_count"]


# ── Edge Cases ────────────────────────────────────────────────────────────


class TestEdgeCases:
    """Edge cases and error handling."""

    def test_scoring_empty_dimensions(self, client):
        """Scoring with no dimensions should return not_ready."""
        r = client.post("/score/lead", json={"contact_id": "test-empty"})
        assert r.status_code == 200
        data = r.json()
        assert data["outcome"] == "not_ready"
        assert data["confidence"] == 0.0

    def test_scoring_invalid_enum(self, client):
        """Invalid enum values should be rejected by Pydantic."""
        r = client.post("/score/lead", json={
            "contact_id": "test-bad",
            "r1_program_interest": "Martian Visa",
        })
        assert r.status_code == 422  # Pydantic validation error

    def test_scoring_complex_refusal(self, client):
        """Refusal flag should trigger complexity detection."""
        r = client.post("/score/lead", json={
            "contact_id": "test-complex",
            "r1_program_interest": "Express Entry",
            "r4_prior_applications": "Has Refusal",
            "r5_budget_awareness": "Aware",
        })
        assert r.status_code == 200
        data = r.json()
        assert "prior_refusal" in data["flags"] or data["score"] < 70

    def test_scoring_transcript_too_long(self, client):
        """Transcript exceeding 50k chars should be rejected."""
        r = client.post("/score/lead", json={
            "contact_id": "test-long",
            "transcript_excerpt": "a" * 60000,
        })
        assert r.status_code == 422  # Pydantic max_length validation

    def test_case_list_bad_stage(self, client):
        """Invalid stage filter should return 400."""
        r = client.get("/cases/list?stage=flying_unicorn")
        assert r.status_code == 400

    def test_case_list_limit_bounds(self, client):
        """Limit > 200 should be rejected."""
        r = client.get("/cases/list?limit=500")
        assert r.status_code == 422

    def test_unknown_program_forms(self, client):
        """Unknown program should return empty forms list gracefully."""
        r = client.get("/cases/forms/Martian Visa")
        assert r.status_code == 200
        data = r.json()
        assert data["forms"] == []
        assert "note" in data

    def test_analytics_days_bounds(self, client):
        """Analytics days param should be bounded (1-365)."""
        r = client.get("/analytics/pipeline?days=0")
        assert r.status_code == 422
        r = client.get("/analytics/pipeline?days=999")
        assert r.status_code == 422

    def test_stuck_threshold_bounds(self, client):
        """Stuck threshold should be bounded (1-90)."""
        r = client.get("/analytics/stuck?threshold_days=0")
        assert r.status_code == 422
        r = client.get("/analytics/stuck?threshold_days=100")
        assert r.status_code == 422

    def test_client_search_too_short(self, client):
        """Search query < 2 chars should be rejected."""
        r = client.get("/clients/search?q=a")
        assert r.status_code in (400, 422)

    def test_invalid_decision_enum(self, client):
        """Invalid IRCC decision should be rejected."""
        r = client.post("/cases/decision", json={
            "contact_id": "test",
            "decision": "Maybe",
        })
        assert r.status_code == 400

    def test_health_endpoints_always_200(self, client):
        """Health endpoints should always return 200."""
        for path in ["/health", "/health/deep", "/health/smoke"]:
            r = client.get(path)
            assert r.status_code == 200, f"{path} returned {r.status_code}"

    def test_ocr_types_returns_all(self, client):
        """OCR types endpoint should list all 7 document types."""
        r = client.get("/extract/types")
        assert r.status_code == 200
        types = r.json()["supported_types"]
        assert len(types) >= 7

    def test_form_serving_unknown_tenant(self, client):
        """Unknown tenant should return 404."""
        r = client.get("/form/unknown-tenant/onboarding")
        assert r.status_code == 404

    def test_form_serving_valid_tenant(self, client):
        """Valid tenant (vmc) should return 200 HTML."""
        r = client.get("/form/vmc/onboarding")
        assert r.status_code == 200
        assert "text/html" in r.headers.get("content-type", "")

    def test_demo_summary_runs(self, client):
        """Demo summary should not crash even without DB."""
        r = client.get("/demo/summary")
        # May return error dict if no DB, but should not 500
        assert r.status_code == 200

    def test_negative_limit_rejected(self, client):
        """Negative limit on /cases/list should return 422, not 500."""
        r = client.get("/cases/list?limit=-1")
        assert r.status_code == 422

    def test_typebot_empty_body_rejected(self, client):
        """Typebot webhook with no body should return 422, not 500."""
        r = client.post("/typebot/webhook")
        assert r.status_code == 422

    def test_typebot_array_body_rejected(self, client):
        """Typebot webhook with JSON array (not object) should return 422."""
        r = client.post("/typebot/webhook", json=[1, 2, 3])
        assert r.status_code == 422

    def test_briefing_invalid_email_rejected(self, client):
        """Briefing with invalid email format should return 422."""
        r = client.post("/briefing/generate", json={
            "contact_id": "test",
            "appointment_id": "apt-1",
            "consultant_email": "not-an-email",
        })
        assert r.status_code == 422

    def test_briefing_empty_fields_rejected(self, client):
        """Briefing with empty required strings should return 422."""
        r = client.post("/briefing/generate", json={
            "contact_id": "",
            "appointment_id": "",
            "consultant_email": "test@example.com",
        })
        assert r.status_code == 422

    def test_briefing_invalid_delivery_method(self, client):
        """Briefing with invalid delivery_method should return 422."""
        r = client.post("/briefing/generate", json={
            "contact_id": "test",
            "appointment_id": "apt-1",
            "consultant_email": "test@example.com",
            "delivery_method": "carrier_pigeon",
        })
        assert r.status_code == 422

    def test_dependent_invalid_relationship(self, client):
        """Dependent with invalid relationship enum should return 422."""
        r = client.post("/dependents/", json={
            "case_id": "NX-TEST",
            "contact_id": "c1",
            "full_name": "Test",
            "relationship": "pet",
        })
        assert r.status_code == 422

    def test_dependent_empty_name(self, client):
        """Dependent with empty full_name should return 422."""
        r = client.post("/dependents/", json={
            "case_id": "NX-TEST",
            "contact_id": "c1",
            "full_name": "",
            "relationship": "spouse",
        })
        assert r.status_code == 422


# ── Alternate Flows ───────────────────────────────────────────────────────


class TestAlternateFlows:
    """Alternate paths through the customer journey."""

    def test_scoring_not_ready_low_info(self, client):
        """Lead with only 1 dimension should be not_ready."""
        r = client.post("/score/lead", json={
            "contact_id": "test-low",
            "r1_program_interest": "Express Entry",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["outcome"] == "not_ready"
        assert data["confidence"] < 0.5

    def test_scoring_complexity_keywords_in_transcript(self, client):
        """Transcript with complexity keywords should flag."""
        r = client.post("/score/lead", json={
            "contact_id": "test-complex",
            "r1_program_interest": "Express Entry",
            "r2_current_location": "In Canada",
            "r3_timeline_urgency": "Near-term",
            "r4_prior_applications": "None",
            "r5_budget_awareness": "Aware",
            "transcript_excerpt": "I was deported from Canada last year and had a removal order",
        })
        assert r.status_code == 200
        data = r.json()
        assert "requires_human_escalation" in data["flags"] or data["outcome"] == "ready_complex"

    def test_form_scoring_single_dimension(self, client):
        """Form with only 1 dimension should still score."""
        r = client.post("/score/form", json={
            "contact_id": "test-single",
            "program_interest": "LMIA",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["dimensions_captured"] == 1
        assert data["preliminary_score"] > 0
        assert "nx:form_scored" in data["ghl_tags_to_add"]

    def test_form_scoring_no_dimensions(self, client):
        """Form with no dimensions should still respond (score 0)."""
        r = client.post("/score/form", json={"contact_id": "test-none"})
        assert r.status_code == 200
        data = r.json()
        assert data["dimensions_captured"] == 0
        assert data["preliminary_score"] == 0

    def test_program_timeline_all_programs(self, client):
        """All programs should have processing time estimates."""
        programs = ["Express Entry", "Spousal Sponsorship", "Work Permit",
                     "Study Permit", "LMIA", "PR Renewal", "Citizenship", "Visitor Visa"]
        for prog in programs:
            r = client.get(f"/cases/timeline/{prog}")
            assert r.status_code == 200, f"Failed for {prog}"
            data = r.json()
            assert "estimated_months" in data
            assert "disclaimer" in data

    def test_trust_check_clean_transcript(self, client):
        """Clean transcript should not trigger escalation."""
        r = client.post("/trust/check", json={
            "transcript": "Hello, I'm interested in Express Entry. Can I book a consultation?",
            "contact_id": "test-clean",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["requires_escalation"] is False

    def test_trust_check_escalation_trigger(self, client):
        """Transcript with deportation mention should trigger escalation."""
        r = client.post("/trust/check", json={
            "transcript": "I was deported from Canada and have a removal order. Am I eligible to come back?",
            "contact_id": "test-escalate",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["requires_escalation"] is True
        assert len(data["flags"]) > 0
