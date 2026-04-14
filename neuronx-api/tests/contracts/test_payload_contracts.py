"""
Payload Contract Tests

Validates that JSON fixture shapes used in tests match the actual external
API payload schemas. If an external provider changes their payload format,
these tests catch it before production breaks.

Contracts:
  - GHL Webhook (ContactCreate, event types)
  - VAPI Webhook (end-of-call-report, function-call)
  - Typebot Submission (answers, variables)
  - Claude OCR Response (passport, IELTS)
  - GHL API Response (mock_ghl fixture shape)
"""

import json
from pathlib import Path

import pytest

# Mark every test in this module as contract
pytestmark = pytest.mark.contract


# ---------------------------------------------------------------------------
# GHL Webhook Contract
# ---------------------------------------------------------------------------

class TestGHLWebhookContract:
    """Validate ghl_contact_created.json matches what webhooks.py expects."""

    KNOWN_GHL_EVENT_TYPES = {
        "ContactCreate",
        "ContactCreated",
        "AppointmentCreate",
        "AppointmentBooked",
        "appointment.booked",
        "TagAdded",
        "tag.added",
        "ContactTagUpdate",
    }

    def test_fixture_has_required_fields(self, fixture_loader):
        """GHL ContactCreate fixture has all fields the handler reads."""
        payload = fixture_loader("ghl_contact_created")

        assert "type" in payload
        assert "locationId" in payload
        assert "id" in payload
        assert "firstName" in payload
        assert "lastName" in payload
        assert "email" in payload

    def test_fixture_has_contact_communication_fields(self, fixture_loader):
        """GHL payload includes phone and source for downstream use."""
        payload = fixture_loader("ghl_contact_created")

        assert "phone" in payload
        assert "source" in payload

    def test_fixture_type_is_known_event(self, fixture_loader):
        """Fixture event type is a known GHL event handled by webhooks.py."""
        payload = fixture_loader("ghl_contact_created")

        assert payload["type"] in self.KNOWN_GHL_EVENT_TYPES

    def test_fixture_has_tags_as_list(self, fixture_loader):
        """GHL payload tags field is a list (even if empty)."""
        payload = fixture_loader("ghl_contact_created")

        assert "tags" in payload
        assert isinstance(payload["tags"], list)

    def test_fixture_has_custom_fields_as_list(self, fixture_loader):
        """GHL payload customFields is a list (even if empty)."""
        payload = fixture_loader("ghl_contact_created")

        assert "customFields" in payload
        assert isinstance(payload["customFields"], list)

    def test_fixture_location_id_is_string(self, fixture_loader):
        """locationId must be a non-empty string."""
        payload = fixture_loader("ghl_contact_created")

        assert isinstance(payload["locationId"], str)
        assert len(payload["locationId"]) > 0

    def test_fixture_email_format(self, fixture_loader):
        """Email field should contain an '@' character."""
        payload = fixture_loader("ghl_contact_created")

        assert "@" in payload["email"]

    def test_conftest_payload_matches_fixture_shape(self, ghl_contact_payload, fixture_loader):
        """The conftest payload fixture has the same keys as the JSON file."""
        file_fixture = fixture_loader("ghl_contact_created")
        conftest_keys = set(ghl_contact_payload.keys())
        file_keys = set(file_fixture.keys())

        # conftest fixture should have at least the core keys
        core_keys = {"type", "locationId", "id", "firstName", "lastName", "email"}
        assert core_keys.issubset(conftest_keys)
        assert core_keys.issubset(file_keys)


# ---------------------------------------------------------------------------
# VAPI Webhook Contract
# ---------------------------------------------------------------------------

class TestVAPIWebhookContract:
    """Validate vapi_end_of_call.json and vapi_function_call.json structures."""

    def test_eoc_has_message_wrapper(self, fixture_loader):
        """VAPI end-of-call payload wraps everything in 'message' object."""
        payload = fixture_loader("vapi_end_of_call")

        assert "message" in payload
        assert isinstance(payload["message"], dict)

    def test_eoc_has_type_field(self, fixture_loader):
        """message.type is 'end-of-call-report'."""
        payload = fixture_loader("vapi_end_of_call")

        assert payload["message"]["type"] == "end-of-call-report"

    def test_eoc_has_call_id(self, fixture_loader):
        """message.call.id exists for call identification."""
        payload = fixture_loader("vapi_end_of_call")

        call = payload["message"]["call"]
        assert "id" in call
        assert isinstance(call["id"], str)
        assert len(call["id"]) > 0

    def test_eoc_has_analysis_structured_data(self, fixture_loader):
        """message.analysis.structuredData contains R1-R5 fields."""
        payload = fixture_loader("vapi_end_of_call")

        analysis = payload["message"]["analysis"]
        assert "structuredData" in analysis

        sd = analysis["structuredData"]
        assert isinstance(sd, dict)

    def test_eoc_structured_data_has_r1_r5(self, fixture_loader):
        """structuredData has all 5 readiness dimension keys."""
        payload = fixture_loader("vapi_end_of_call")
        sd = payload["message"]["analysis"]["structuredData"]

        r_keys = [
            "program_interest",
            "current_location",
            "timeline_urgency",
            "prior_applications",
            "budget_awareness",
        ]
        for key in r_keys:
            assert key in sd, f"Missing R field: {key}"
            assert isinstance(sd[key], str), f"R field {key} should be string"

    def test_eoc_has_transcript(self, fixture_loader):
        """message.artifact.transcript exists and is a non-empty string."""
        payload = fixture_loader("vapi_end_of_call")

        artifact = payload["message"]["artifact"]
        assert "transcript" in artifact
        assert isinstance(artifact["transcript"], str)
        assert len(artifact["transcript"]) > 0

    def test_eoc_has_analysis_summary(self, fixture_loader):
        """message.analysis.summary exists for call summary."""
        payload = fixture_loader("vapi_end_of_call")

        assert "summary" in payload["message"]["analysis"]
        assert isinstance(payload["message"]["analysis"]["summary"], str)

    def test_eoc_has_customer(self, fixture_loader):
        """message.customer.number exists for phone identification."""
        payload = fixture_loader("vapi_end_of_call")

        assert "customer" in payload["message"]
        assert "number" in payload["message"]["customer"]

    def test_function_call_has_message_wrapper(self, fixture_loader):
        """VAPI function-call payload wraps in 'message' object."""
        payload = fixture_loader("vapi_function_call")

        assert "message" in payload
        assert payload["message"]["type"] == "function-call"

    def test_function_call_has_function_details(self, fixture_loader):
        """message.functionCall contains name and parameters."""
        payload = fixture_loader("vapi_function_call")

        fc = payload["message"]["functionCall"]
        assert "name" in fc
        assert "parameters" in fc
        assert isinstance(fc["name"], str)
        assert isinstance(fc["parameters"], dict)

    def test_function_call_has_call_id(self, fixture_loader):
        """Function call payload includes call.id for correlation."""
        payload = fixture_loader("vapi_function_call")

        assert "call" in payload["message"]
        assert "id" in payload["message"]["call"]

    def test_conftest_vapi_matches_fixture_shape(self, vapi_end_of_call_payload, fixture_loader):
        """Conftest VAPI payload has same top-level structure as fixture file."""
        file_fix = fixture_loader("vapi_end_of_call")

        # Both must have message.type == end-of-call-report
        assert vapi_end_of_call_payload["message"]["type"] == file_fix["message"]["type"]
        # Both must have analysis.structuredData
        assert "structuredData" in vapi_end_of_call_payload["message"]["analysis"]
        assert "structuredData" in file_fix["message"]["analysis"]


# ---------------------------------------------------------------------------
# Typebot Submission Contract
# ---------------------------------------------------------------------------

class TestTypebotSubmissionContract:
    """Validate typebot_submission.json matches webhook handler expectations."""

    def test_has_required_top_level_fields(self, fixture_loader):
        """Typebot submission has resultId, answers, variables."""
        payload = fixture_loader("typebot_submission")

        assert "resultId" in payload
        assert "answers" in payload
        assert "variables" in payload

    def test_answers_is_list(self, fixture_loader):
        """answers field is a list."""
        payload = fixture_loader("typebot_submission")
        assert isinstance(payload["answers"], list)

    def test_each_answer_has_required_keys(self, fixture_loader):
        """Each answer object has blockId, variableId, content."""
        payload = fixture_loader("typebot_submission")

        for i, answer in enumerate(payload["answers"]):
            assert "blockId" in answer, f"Answer {i} missing blockId"
            assert "variableId" in answer, f"Answer {i} missing variableId"
            assert "content" in answer, f"Answer {i} missing content"

    def test_variables_is_list(self, fixture_loader):
        """variables field is a list."""
        payload = fixture_loader("typebot_submission")
        assert isinstance(payload["variables"], list)

    def test_each_variable_has_required_keys(self, fixture_loader):
        """Each variable object has id, name, value."""
        payload = fixture_loader("typebot_submission")

        for i, var in enumerate(payload["variables"]):
            assert "id" in var, f"Variable {i} missing id"
            assert "name" in var, f"Variable {i} missing name"
            assert "value" in var, f"Variable {i} missing value"

    def test_typebot_id_present(self, fixture_loader):
        """Typebot submission includes typebot.id for bot identification."""
        payload = fixture_loader("typebot_submission")

        assert "typebot" in payload
        assert "id" in payload["typebot"]

    def test_conftest_typebot_matches_fixture_keys(self, typebot_submission_payload, fixture_loader):
        """Conftest and fixture file Typebot payloads share same structure."""
        file_fix = fixture_loader("typebot_submission")

        assert set(typebot_submission_payload.keys()) == set(file_fix.keys())
        # Both have answers with same shape
        for key in ("blockId", "variableId", "content"):
            assert key in typebot_submission_payload["answers"][0]
            assert key in file_fix["answers"][0]


# ---------------------------------------------------------------------------
# Claude OCR Response Contract
# ---------------------------------------------------------------------------

class TestClaudeOCRResponseContract:
    """Validate claude_ocr_passport.json and claude_ocr_ielts.json structure."""

    def test_passport_has_content_block(self, fixture_loader):
        """Claude response has content[0].text with parseable JSON."""
        resp = fixture_loader("claude_ocr_passport")

        assert "content" in resp
        assert isinstance(resp["content"], list)
        assert len(resp["content"]) > 0
        assert "text" in resp["content"][0]

    def test_passport_text_is_parseable_json(self, fixture_loader):
        """content[0].text contains a JSON code block with passport fields."""
        resp = fixture_loader("claude_ocr_passport")
        text = resp["content"][0]["text"]

        # Claude wraps JSON in ```json ... ``` markdown
        if "```json" in text:
            start = text.index("```json") + 7
            end = text.index("```", start)
            json_str = text[start:end].strip()
        else:
            json_str = text

        parsed = json.loads(json_str)
        assert isinstance(parsed, dict)

    def test_passport_extracted_fields(self, fixture_loader):
        """Parsed passport JSON has required identity fields."""
        resp = fixture_loader("claude_ocr_passport")
        text = resp["content"][0]["text"]

        if "```json" in text:
            start = text.index("```json") + 7
            end = text.index("```", start)
            json_str = text[start:end].strip()
        else:
            json_str = text

        parsed = json.loads(json_str)

        assert "full_name" in parsed
        assert "date_of_birth" in parsed
        assert "passport_number" in parsed
        assert "passport_expiry" in parsed
        assert "country_of_citizenship" in parsed or "nationality" in parsed

    def test_passport_response_metadata(self, fixture_loader):
        """Claude response has model and stop_reason metadata."""
        resp = fixture_loader("claude_ocr_passport")

        assert "model" in resp
        assert "stop_reason" in resp
        assert resp["type"] == "message"
        assert resp["role"] == "assistant"

    def test_ielts_has_content_block(self, fixture_loader):
        """IELTS Claude response has content[0].text."""
        resp = fixture_loader("claude_ocr_ielts")

        assert "content" in resp
        assert len(resp["content"]) > 0
        assert "text" in resp["content"][0]

    def test_ielts_text_is_parseable_json(self, fixture_loader):
        """IELTS content text is valid JSON."""
        resp = fixture_loader("claude_ocr_ielts")
        text = resp["content"][0]["text"]

        parsed = json.loads(text)
        assert isinstance(parsed, dict)

    def test_ielts_has_score_fields(self, fixture_loader):
        """Parsed IELTS JSON has all 4 component scores and overall."""
        resp = fixture_loader("claude_ocr_ielts")
        text = resp["content"][0]["text"]
        parsed = json.loads(text)

        assert "listening_score" in parsed
        assert "reading_score" in parsed
        assert "writing_score" in parsed
        assert "speaking_score" in parsed
        assert "overall_score" in parsed

    def test_ielts_has_test_metadata(self, fixture_loader):
        """IELTS result includes test_type and test_date."""
        resp = fixture_loader("claude_ocr_ielts")
        text = resp["content"][0]["text"]
        parsed = json.loads(text)

        assert "test_type" in parsed
        assert "test_date" in parsed


# ---------------------------------------------------------------------------
# GHL API Response Contract (mock_ghl fixture)
# ---------------------------------------------------------------------------

class TestGHLAPIResponseContract:
    """Validate mock_ghl fixture returns shapes matching real GHL API."""

    @pytest.mark.asyncio
    async def test_get_contact_shape(self, mock_ghl):
        """get_contact returns dict with 'contact' key and nested fields."""
        result = await mock_ghl.get_contact("test-id")

        assert "contact" in result
        contact = result["contact"]
        assert "id" in contact
        assert "firstName" in contact
        assert "lastName" in contact
        assert "email" in contact
        assert "phone" in contact
        assert "tags" in contact
        assert isinstance(contact["tags"], list)
        assert "customFields" in contact
        assert isinstance(contact["customFields"], list)

    @pytest.mark.asyncio
    async def test_add_tag_returns_tags(self, mock_ghl):
        """add_tag returns dict with 'tags' list."""
        result = await mock_ghl.add_tag("test-id", "nx:test")

        assert "tags" in result
        assert isinstance(result["tags"], list)

    @pytest.mark.asyncio
    async def test_add_tags_returns_tags(self, mock_ghl):
        """add_tags returns dict with 'tags' list (multiple tags)."""
        result = await mock_ghl.add_tags("test-id", ["nx:a", "nx:b"])

        assert "tags" in result
        assert isinstance(result["tags"], list)

    @pytest.mark.asyncio
    async def test_add_note_returns_note(self, mock_ghl):
        """add_note returns dict with 'note' key containing 'id'."""
        result = await mock_ghl.add_note("test-id", "Test note")

        assert "note" in result
        assert "id" in result["note"]

    @pytest.mark.asyncio
    async def test_update_contact_returns_contact(self, mock_ghl):
        """update_contact returns dict with 'contact' key."""
        result = await mock_ghl.update_contact("test-id", {"firstName": "Updated"})

        assert "contact" in result
        assert "id" in result["contact"]

    @pytest.mark.asyncio
    async def test_get_appointment_shape(self, mock_ghl):
        """get_appointment returns appointment with expected keys."""
        result = await mock_ghl.get_appointment("appt-id")

        assert "id" in result
        assert "calendarId" in result
        assert "contactId" in result
        assert "status" in result
        assert "startTime" in result
        assert "endTime" in result
