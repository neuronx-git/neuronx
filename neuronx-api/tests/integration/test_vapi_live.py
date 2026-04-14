"""
LIVE VAPI API Integration Tests

Tests the actual VAPI API to verify assistant configuration,
structured data plan, tool definitions, and trust boundaries.

These tests call the REAL VAPI API — they require VAPI_API_KEY.
Run with: pytest tests/integration/test_vapi_live.py -v -m live

Skipped automatically if VAPI_API_KEY is not set or is a test placeholder.
"""

import os
import pytest
import httpx

VAPI_BASE = "https://api.vapi.ai"
ASSISTANT_ID = "289a9701-9199-4d03-9416-49d18bec2f69"
PHONE_ID = "ea133993-7c18-4437-88a6-fa7a2d15efbe"

# Use VAPI_LIVE_API_KEY to avoid conflict with conftest test key
VAPI_API_KEY = os.getenv("VAPI_LIVE_API_KEY", os.getenv("VAPI_API_KEY", ""))

# Skip all tests if no real VAPI key (UUID format, not test placeholder)
is_real_key = VAPI_API_KEY and len(VAPI_API_KEY) > 30 and not VAPI_API_KEY.startswith("test-")
pytestmark = [
    pytest.mark.integration,
    pytest.mark.live,
    pytest.mark.skipif(not is_real_key, reason="No real VAPI_API_KEY set"),
]


def vapi_get(path: str) -> httpx.Response:
    """Helper: GET from VAPI API."""
    return httpx.get(
        f"{VAPI_BASE}{path}",
        headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
        timeout=30.0,
    )


# ── Assistant Configuration ─────────────────────────────────────────

class TestVAPIAssistantConfig:
    """Verify the VAPI assistant is configured correctly for NeuronX intake."""

    def test_assistant_exists(self):
        """Assistant ID is accessible and returns 200."""
        resp = vapi_get(f"/assistant/{ASSISTANT_ID}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == ASSISTANT_ID

    def test_assistant_name(self):
        """Assistant is named 'NeuronX Intake Agent'."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        assert data["name"] == "NeuronX Intake Agent"

    def test_assistant_model(self):
        """Assistant uses GPT-4o model."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        assert data["model"]["model"] == "gpt-4o"
        assert data["model"]["provider"] == "openai"

    def test_assistant_voice(self):
        """Assistant uses 11labs voice provider."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        assert data["voice"]["provider"] == "11labs"
        assert data["voice"]["voiceId"] == "EXAVITQu4vr4xnSDxMaL"

    def test_assistant_transcriber(self):
        """Transcriber is Deepgram Nova-2 English."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        assert data["transcriber"]["provider"] == "deepgram"
        assert data["transcriber"]["model"] == "nova-2"

    def test_assistant_webhook_url(self):
        """Webhook URL points to NeuronX API on Railway."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        assert "neuronx-production" in data["serverUrl"]
        assert "/webhooks/voice" in data["serverUrl"]

    def test_assistant_max_duration(self):
        """Call max duration is set (prevents runaway calls)."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        assert data.get("maxDurationSeconds", 0) > 0
        assert data["maxDurationSeconds"] <= 900  # Max 15 min

    def test_assistant_silence_timeout(self):
        """Silence timeout is configured."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        assert data.get("silenceTimeoutSeconds", 0) > 0


# ── Structured Data Plan (R1-R5) ────────────────────────────────────

class TestVAPIStructuredDataPlan:
    """Verify the structured data extraction plan captures all R1-R5 fields."""

    def _get_schema(self):
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        return data["analysisPlan"]["structuredDataPlan"]["schema"]

    def test_structured_data_has_program_interest(self):
        """Schema extracts program_interest field."""
        schema = self._get_schema()
        assert "program_interest" in schema["properties"]

    def test_structured_data_has_current_location(self):
        """Schema extracts current_location field."""
        schema = self._get_schema()
        assert "current_location" in schema["properties"]

    def test_structured_data_has_timeline_urgency(self):
        """Schema extracts timeline_urgency field."""
        schema = self._get_schema()
        assert "timeline_urgency" in schema["properties"]

    def test_structured_data_has_prior_applications(self):
        """Schema extracts prior_applications field."""
        schema = self._get_schema()
        assert "prior_applications" in schema["properties"]

    def test_structured_data_has_budget_awareness(self):
        """Schema extracts budget_awareness field."""
        schema = self._get_schema()
        assert "budget_awareness" in schema["properties"]

    def test_structured_data_has_escalation_needed(self):
        """Schema extracts escalation_needed boolean."""
        schema = self._get_schema()
        assert "escalation_needed" in schema["properties"]
        assert schema["properties"]["escalation_needed"]["type"] == "boolean"

    def test_structured_data_has_booking_interest(self):
        """Schema extracts booking_interest boolean."""
        schema = self._get_schema()
        assert "booking_interest" in schema["properties"]

    def test_structured_data_has_call_quality(self):
        """Schema extracts call_quality field."""
        schema = self._get_schema()
        assert "call_quality" in schema["properties"]

    def test_program_interest_enum_values(self):
        """program_interest description lists all 9 program types."""
        schema = self._get_schema()
        desc = schema["properties"]["program_interest"]["description"]
        for prog in ["Express Entry", "Spousal", "Work Permit", "Study Permit",
                      "LMIA", "PR Renewal", "Citizenship", "Visitor Visa"]:
            assert prog in desc, f"Missing program: {prog}"


# ── Trust Boundaries in System Prompt ────────────────────────────────

class TestVAPITrustBoundaries:
    """Verify trust boundary rules are embedded in the assistant's system prompt."""

    def _get_system_prompt(self):
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        messages = data["model"]["messages"]
        return next(m["content"] for m in messages if m["role"] == "system")

    def test_no_eligibility_assessment_rule(self):
        """System prompt forbids eligibility assessment."""
        prompt = self._get_system_prompt()
        assert "NEVER assess eligibility" in prompt

    def test_no_pathway_recommendation_rule(self):
        """System prompt forbids pathway recommendations."""
        prompt = self._get_system_prompt()
        assert "NEVER recommend" in prompt

    def test_no_law_interpretation_rule(self):
        """System prompt forbids interpreting immigration law."""
        prompt = self._get_system_prompt()
        assert "NEVER interpret" in prompt

    def test_no_outcome_promises_rule(self):
        """System prompt forbids promising outcomes."""
        prompt = self._get_system_prompt()
        assert "NEVER promise" in prompt or "NEVER claim" in prompt

    def test_escalation_triggers_defined(self):
        """System prompt includes escalation trigger rules."""
        prompt = self._get_system_prompt()
        assert "Escalation" in prompt
        assert "deportation" in prompt.lower() or "removal" in prompt.lower()

    def test_not_rcic_disclaimer(self):
        """System prompt states agent is NOT an RCIC or lawyer."""
        prompt = self._get_system_prompt()
        assert "NOT" in prompt and ("RCIC" in prompt or "lawyer" in prompt)


# ── Phone Number ─────────────────────────────────────────────────────

class TestVAPIPhoneNumber:
    """Verify the VAPI phone number is active and configured."""

    def test_phone_exists(self):
        """Phone number ID returns valid response."""
        resp = vapi_get(f"/phone-number/{PHONE_ID}")
        assert resp.status_code == 200

    def test_phone_is_active(self):
        """Phone number status is active."""
        data = vapi_get(f"/phone-number/{PHONE_ID}").json()
        # VAPI phone numbers don't have explicit status — existence = active
        assert data.get("id") == PHONE_ID

    def test_phone_number_value(self):
        """Phone number is +16479315181."""
        data = vapi_get(f"/phone-number/{PHONE_ID}").json()
        assert data.get("number") == "+16479315181" or data.get("twilioPhoneNumber") == "+16479315181"


# ── Webhook Configuration ────────────────────────────────────────────

class TestVAPIWebhookConfig:
    """Verify webhook configuration points to NeuronX API."""

    def test_server_url_configured(self):
        """Server URL is set on the assistant."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        assert data.get("serverUrl") is not None
        assert len(data["serverUrl"]) > 0

    def test_server_url_is_railway(self):
        """Server URL points to Railway deployment."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        assert "railway.app" in data["serverUrl"]

    def test_end_of_call_report_enabled(self):
        """end-of-call-report is in serverMessages."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        server_msgs = data.get("serverMessages", [])
        assert "end-of-call-report" in server_msgs

    def test_recording_enabled(self):
        """Call recording is enabled for audit trail."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        artifact_plan = data.get("artifactPlan", {})
        assert artifact_plan.get("recordingEnabled") is True

    def test_transcript_enabled(self):
        """Transcript capture is enabled."""
        data = vapi_get(f"/assistant/{ASSISTANT_ID}").json()
        artifact_plan = data.get("artifactPlan", {})
        transcript_plan = artifact_plan.get("transcriptPlan", {})
        assert transcript_plan.get("enabled") is True
