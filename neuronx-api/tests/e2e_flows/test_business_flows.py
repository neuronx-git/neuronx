"""
E2E Business Flow Tests

Tests simulate complete business journeys through the NeuronX API.
Each flow chains multiple endpoint calls. All external services (GHL, VAPI,
Claude, Documenso) are mocked — only internal logic chains are tested.

Flows:
  1. VAPI Call -> Scoring -> GHL Update
  2. GHL Contact Created -> Processing
  3. Lead Scoring via /score/lead and /score/form
  4. Document OCR -> Extraction
  5. Multi-Tenant Form Serving
  6. Health + Admin
  7. Failure Handling
"""

import json
import io
import copy
from unittest.mock import patch, AsyncMock, MagicMock

import pytest

# Mark every test in this module as e2e
pytestmark = pytest.mark.e2e


# ---------------------------------------------------------------------------
# Flow 1: VAPI Call -> Scoring -> GHL Update
# ---------------------------------------------------------------------------

class TestVAPICallScoringFlow:
    """End-to-end: VAPI end-of-call-report -> scoring -> GHL update."""

    def test_standard_outcome_full_flow(self, client, patch_ghl, vapi_end_of_call_payload):
        """
        Happy path: all R1-R5 answered, no complexity flags.
        Expects ready_standard outcome, GHL tags and fields updated.
        """
        payload = vapi_end_of_call_payload
        # Add ghl_contact_id in call metadata so the handler finds the contact
        payload["message"]["call"]["metadata"] = {"ghl_contact_id": "test-contact-123"}

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["status"] == "ok"
        assert data["action"] == "scored"
        assert data["contact_id"] == "test-contact-123"
        assert data["outcome"] in ("ready_standard", "ready_urgent")
        assert data["score"] > 0
        assert isinstance(data["tags_added"], list)
        assert len(data["tags_added"]) > 0

        # Verify GHL interactions
        patch_ghl.update_custom_fields.assert_called_once()
        patch_ghl.add_tags.assert_called()
        patch_ghl.add_note.assert_called()

    def test_urgent_outcome(self, client, patch_ghl, vapi_end_of_call_payload):
        """R3 = Urgent (30 days) triggers ready_urgent + nx:urgent tag."""
        payload = vapi_end_of_call_payload
        payload["message"]["call"]["metadata"] = {"ghl_contact_id": "test-contact-123"}
        payload["message"]["analysis"]["structuredData"]["timeline_urgency"] = "Urgent (30 days)"

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["outcome"] == "ready_urgent"
        assert "nx:urgent" in data["tags_added"]

    def test_complex_outcome_with_refusal_keywords(self, client, patch_ghl, vapi_end_of_call_payload):
        """Transcript contains complexity keywords -> ready_complex."""
        payload = vapi_end_of_call_payload
        payload["message"]["call"]["metadata"] = {"ghl_contact_id": "test-contact-123"}
        payload["message"]["artifact"]["transcript"] = (
            "Prospect: I was previously deported from Canada and had a removal order."
        )

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["outcome"] == "ready_complex"
        assert "nx:human_escalation" in data["tags_added"]

    def test_not_ready_minimal_data(self, client, patch_ghl, vapi_end_of_call_payload):
        """No structured data at all -> not_ready or minimal score."""
        payload = vapi_end_of_call_payload
        payload["message"]["call"]["metadata"] = {"ghl_contact_id": "test-contact-123"}
        payload["message"]["analysis"]["structuredData"] = {}

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        # With 0 dimensions answered, outcome should be not_ready
        assert data["outcome"] == "not_ready"

    def test_no_contact_id_warning(self, client, patch_ghl, vapi_end_of_call_payload):
        """Missing ghl_contact_id in call metadata -> returns warning, no GHL calls."""
        payload = vapi_end_of_call_payload
        # No metadata.ghl_contact_id
        payload["message"]["call"]["metadata"] = {}

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["status"] == "warning"
        assert data["message"] == "no_contact_id"

        # GHL should NOT be called
        patch_ghl.update_custom_fields.assert_not_called()

    def test_function_call_collect_readiness(self, client, patch_ghl, fixture_loader):
        """VAPI function-call event: collect_readiness_data returns result string."""
        payload = fixture_loader("vapi_function_call")

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert "result" in data
        assert "Readiness data received" in data["result"]

    def test_function_call_book_consultation(self, client, patch_ghl):
        """VAPI function-call: book_consultation returns booking info."""
        payload = {
            "message": {
                "type": "function-call",
                "functionCall": {
                    "name": "book_consultation",
                    "parameters": {},
                },
                "call": {"id": "call-003", "type": "outboundPhoneCall", "status": "in-progress"},
            }
        }

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert "result" in data
        assert "consultation" in data["result"].lower() or "booking" in data["result"].lower()

    def test_function_call_transfer_to_human(self, client, patch_ghl):
        """VAPI function-call: transfer_to_human returns transfer message."""
        payload = {
            "message": {
                "type": "function-call",
                "functionCall": {
                    "name": "transfer_to_human",
                    "parameters": {"reason": "complex case"},
                },
                "call": {"id": "call-004", "type": "outboundPhoneCall", "status": "in-progress"},
            }
        }

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert "result" in data
        assert "transfer" in data["result"].lower()

    def test_status_update_logged(self, client, patch_ghl):
        """VAPI status-update event is logged without error."""
        payload = {
            "message": {
                "type": "status-update",
                "status": "ringing",
                "call": {"id": "call-005"},
            }
        }

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200
        assert resp.json()["action"] == "status_logged"

    def test_transcript_event_acknowledged(self, client, patch_ghl):
        """VAPI transcript event is accepted without processing."""
        payload = {
            "message": {
                "type": "transcript",
                "call": {"id": "call-006"},
            }
        }

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200
        assert resp.json()["action"] == "transcript_logged"


# ---------------------------------------------------------------------------
# Flow 2: GHL Contact Created -> Processing
# ---------------------------------------------------------------------------

class TestGHLContactCreatedFlow:
    """End-to-end: GHL ContactCreate webhook -> log -> ack."""

    def test_contact_create_logged(self, client, patch_ghl, ghl_contact_payload):
        """GHL ContactCreate event is processed and acknowledged."""
        resp = client.post("/webhooks/ghl", json=ghl_contact_payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["status"] == "ok"
        assert data["action"] == "contact_logged"

    def test_appointment_booked_logged(self, client, patch_ghl):
        """GHL AppointmentCreate event is logged with appointment ID."""
        payload = {
            "type": "AppointmentCreate",
            "locationId": "test-location-id",
            "contactId": "test-contact-123",
            "appointmentId": "appt-999",
            "id": "appt-999",
        }

        resp = client.post("/webhooks/ghl", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["action"] == "appointment_logged"
        assert data["appointment_id"] == "appt-999"

    def test_tag_added_logged(self, client, patch_ghl):
        """GHL TagAdded event is processed and tag is captured."""
        payload = {
            "type": "TagAdded",
            "locationId": "test-location-id",
            "contactId": "test-contact-123",
            "id": "tag-event-001",
            "tag": "nx:score:high",
        }

        resp = client.post("/webhooks/ghl", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["action"] == "tag_logged"
        assert data["tag"] == "nx:score:high"

    def test_unknown_event_no_handler(self, client, patch_ghl):
        """Unknown GHL event type returns no_handler."""
        payload = {
            "type": "SomeNewEventType",
            "locationId": "test-location-id",
            "id": "unknown-event-001",
        }

        resp = client.post("/webhooks/ghl", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["action"] == "no_handler"
        assert data["type"] == "SomeNewEventType"

    def test_contact_create_alternate_type(self, client, patch_ghl, ghl_contact_payload):
        """GHL also sends 'ContactCreated' (past tense) — both handled."""
        payload = ghl_contact_payload.copy()
        payload["type"] = "ContactCreated"

        resp = client.post("/webhooks/ghl", json=payload)
        assert resp.status_code == 200
        assert resp.json()["action"] == "contact_logged"


# ---------------------------------------------------------------------------
# Flow 3: Lead Scoring
# ---------------------------------------------------------------------------

class TestLeadScoringFlow:
    """POST /score/lead and /score/form — readiness scoring.

    NOTE: /score/lead uses Pydantic enums (ReadinessInput) which require
    exact enum values like "Express Entry", "Near-term" (not the longer
    descriptive forms like "Near-term (1-3 months)").
    """

    def test_score_lead_standard(self, client):
        """Standard lead: all 5 dims answered, no flags -> ready_standard."""
        payload = {
            "contact_id": "test-contact-123",
            "r1_program_interest": "Express Entry",
            "r2_current_location": "Outside Canada",
            "r3_timeline_urgency": "Near-term",
            "r4_prior_applications": "None",
            "r5_budget_awareness": "Aware",
        }
        resp = client.post("/score/lead", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["contact_id"] == "test-contact-123"
        assert data["outcome"] == "ready_standard"
        assert data["score"] >= 70
        assert data["confidence"] == 1.0
        assert "nx:assessment:complete" in data["ghl_tags_to_add"]

    def test_score_lead_urgent(self, client):
        """Urgent lead: R3 = Urgent -> ready_urgent + nx:urgent."""
        payload = {
            "contact_id": "test-contact-urgent",
            "r1_program_interest": "Spousal Sponsorship",
            "r2_current_location": "In Canada",
            "r3_timeline_urgency": "Urgent",
            "r4_prior_applications": "None",
            "r5_budget_awareness": "Aware",
        }
        resp = client.post("/score/lead", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["outcome"] == "ready_urgent"
        assert "nx:urgent" in data["ghl_tags_to_add"]
        assert "urgent_timeline" in data["flags"]

    def test_score_lead_complex(self, client):
        """Complex lead: refusal keywords -> ready_complex + nx:human_escalation."""
        payload = {
            "contact_id": "test-contact-complex",
            "r1_program_interest": "Express Entry",
            "r2_current_location": "Outside Canada",
            "r3_timeline_urgency": "Near-term",
            "r4_prior_applications": "Has Refusal",
            "r5_budget_awareness": "Aware",
            "transcript_excerpt": "I was previously deported from Canada and had a removal order.",
        }
        resp = client.post("/score/lead", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["outcome"] == "ready_complex"
        assert "nx:human_escalation" in data["ghl_tags_to_add"]
        assert any("complexity:" in f for f in data["flags"])

    def test_score_lead_minimal_not_ready(self, client):
        """Only 1 dimension answered (below min_dimensions_for_ready) -> not_ready."""
        payload = {
            "contact_id": "test-contact-minimal",
            "r1_program_interest": "Express Entry",
        }
        resp = client.post("/score/lead", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["outcome"] == "not_ready"
        assert data["confidence"] == 0.2
        assert "nx:not_ready" in data["ghl_tags_to_add"]

    def test_score_form_preliminary(self, client):
        """POST /score/form with R1-R3 returns preliminary score capped at 48."""
        payload = {
            "contact_id": "test-contact-form",
            "program_interest": "Express Entry",
            "current_location": "Outside Canada",
            "timeline": "Near-term",
        }

        resp = client.post("/score/form", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["contact_id"] == "test-contact-form"
        assert data["preliminary_score"] <= 48
        assert data["score_source"] == "form"
        assert data["dimensions_captured"] == 3
        assert data["can_upgrade"] is True
        assert "nx:form_scored" in data["ghl_tags_to_add"]
        assert "nx:form_qualified" in data["ghl_tags_to_add"]

    def test_score_form_partial(self, client):
        """POST /score/form with only R1 -> 1 dimension."""
        payload = {
            "contact_id": "test-contact-partial",
            "program_interest": "Spousal Sponsorship",
        }

        resp = client.post("/score/form", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert data["dimensions_captured"] == 1
        assert "nx:form_scored" in data["ghl_tags_to_add"]
        # Only 1 dim, should not get form_qualified
        assert "nx:form_qualified" not in data["ghl_tags_to_add"]

    def test_score_fields_populated(self, client):
        """Verify GHL fields map is populated with R1-R5 values."""
        payload = {
            "contact_id": "test-contact-fields",
            "r1_program_interest": "Express Entry",
            "r2_current_location": "Outside Canada",
            "r3_timeline_urgency": "Near-term",
            "r4_prior_applications": "None",
            "r5_budget_awareness": "Aware",
        }
        resp = client.post("/score/lead", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        fields = data["ghl_fields_to_update"]
        assert "ai_program_interest" in fields
        assert "ai_readiness_outcome" in fields
        assert "ai_readiness_score" in fields
        assert "assessment_completed_at" in fields
        assert fields["assessed_by"] == "neuronx-api"


# ---------------------------------------------------------------------------
# Flow 4: Document OCR -> Extraction
# ---------------------------------------------------------------------------

class TestDocumentOCRFlow:
    """POST /extract/upload -> OCR extraction pipeline."""

    def test_upload_and_extract_passport(self, client, patch_ghl):
        """Upload file, mock OCR, verify extraction response."""
        mock_result = {
            "method": "fastmrz",
            "extracted_fields": {
                "full_name": "SANTOS MARIA",
                "date_of_birth": "1990-03-15",
                "passport_number": "AB1234567",
                "passport_expiry": "2031-03-14",
                "country_of_citizenship": "India",
                "sex": "F",
            },
            "field_count": 6,
            "confidence": "high",
        }

        with patch("app.routers.doc_extract.DocOCRService") as MockOCR:
            instance = MockOCR.return_value
            instance.extract = AsyncMock(return_value=mock_result)

            file_data = b"fake-passport-image-bytes"
            resp = client.post(
                "/extract/upload",
                files={"file": ("passport.jpg", io.BytesIO(file_data), "image/jpeg")},
                data={"doc_type": "passport"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["field_count"] == 6
        assert data["extracted_fields"]["passport_number"] == "AB1234567"
        assert data["confidence"] == "high"

    def test_upload_dedup_cache(self, client, patch_ghl):
        """Same file uploaded twice returns cached result with duplicate flag."""
        # We need to clear the module-level cache in doc_extract
        from app.routers import doc_extract
        doc_extract._processed_hashes.clear()

        mock_result = {
            "method": "claude",
            "extracted_fields": {"full_name": "TEST"},
            "field_count": 1,
            "confidence": "medium",
        }

        with patch("app.routers.doc_extract.DocOCRService") as MockOCR:
            instance = MockOCR.return_value
            instance.extract = AsyncMock(return_value=mock_result)

            file_data = b"identical-file-content-for-dedup-test"

            # First upload
            resp1 = client.post(
                "/extract/upload",
                files={"file": ("doc.jpg", io.BytesIO(file_data), "image/jpeg")},
                data={"doc_type": "general"},
            )
            assert resp1.status_code == 200

            # Second upload of identical content -> cached
            resp2 = client.post(
                "/extract/upload",
                files={"file": ("doc.jpg", io.BytesIO(file_data), "image/jpeg")},
                data={"doc_type": "general"},
            )
            assert resp2.status_code == 200
            data2 = resp2.json()
            assert data2.get("duplicate") is True

        # Clean up
        doc_extract._processed_hashes.clear()

    def test_upload_empty_file_rejected(self, client, patch_ghl):
        """Empty file upload returns 400."""
        resp = client.post(
            "/extract/upload",
            files={"file": ("empty.jpg", io.BytesIO(b""), "image/jpeg")},
        )
        assert resp.status_code == 400

    def test_upload_too_large_rejected(self, client, patch_ghl):
        """File exceeding 10MB returns 413."""
        large_data = b"x" * (11 * 1024 * 1024)
        resp = client.post(
            "/extract/upload",
            files={"file": ("huge.jpg", io.BytesIO(large_data), "image/jpeg")},
        )
        assert resp.status_code == 413

    def test_extract_types_endpoint(self, client):
        """GET /extract/types returns supported document types."""
        resp = client.get("/extract/types")
        assert resp.status_code == 200
        data = resp.json()
        assert "supported_types" in data
        types = [t["type"] for t in data["supported_types"]]
        assert "passport" in types
        assert "ielts" in types
        assert "eca" in types


# ---------------------------------------------------------------------------
# Flow 5: Multi-Tenant Form Serving
# ---------------------------------------------------------------------------

class TestMultiTenantFormServing:
    """GET /form/{tenant}/{form} -> branded HTML form."""

    def test_serve_vmc_onboarding_form(self, client):
        """GET /form/vmc/onboarding returns branded HTML."""
        with patch("app.routers.forms.load_yaml_config") as mock_cfg:
            mock_cfg.return_value = {
                "tenants": {
                    "vmc": {
                        "name": "Visa Master Canada",
                        "bot_name": "VMC Assistant",
                        "bot_status": "Online",
                        "avatar_url": "/static/vmc-avatar.png",
                        "branding": {
                            "primary": "#1E3A5F",
                            "accent": "#E8380D",
                        },
                        "forms": {
                            "onboarding": {
                                "title": "Immigration Assessment",
                                "typebot_id": "typebot-vmc-001",
                            }
                        },
                        "typebot_viewer_url": "https://viewer.example.com",
                    }
                }
            }
            with patch("app.routers.forms.jinja_env") as mock_jinja:
                mock_template = MagicMock()
                mock_template.render.return_value = "<html><body>VMC Form</body></html>"
                mock_jinja.get_template.return_value = mock_template

                resp = client.get("/form/vmc/onboarding")
                assert resp.status_code == 200
                assert "VMC Form" in resp.text

                # Verify template was called with correct tenant branding
                call_kwargs = mock_template.render.call_args
                assert call_kwargs.kwargs["tenant_name"] == "Visa Master Canada"
                assert call_kwargs.kwargs["primary"] == "#1E3A5F"

    def test_different_tenant_branding(self, client):
        """Different tenants get different branding in rendered HTML."""
        with patch("app.routers.forms.load_yaml_config") as mock_cfg:
            mock_cfg.return_value = {
                "tenants": {
                    "abc_immigration": {
                        "name": "ABC Immigration Inc",
                        "branding": {
                            "primary": "#FF0000",
                            "accent": "#00FF00",
                        },
                        "forms": {
                            "intake": {
                                "title": "ABC Intake Form",
                                "typebot_id": "typebot-abc-001",
                            }
                        },
                        "typebot_viewer_url": "https://viewer.example.com",
                    }
                }
            }
            with patch("app.routers.forms.jinja_env") as mock_jinja:
                mock_template = MagicMock()
                mock_template.render.return_value = "<html>ABC</html>"
                mock_jinja.get_template.return_value = mock_template

                resp = client.get("/form/abc_immigration/intake")
                assert resp.status_code == 200

                call_kwargs = mock_template.render.call_args
                assert call_kwargs.kwargs["tenant_name"] == "ABC Immigration Inc"
                assert call_kwargs.kwargs["primary"] == "#FF0000"

    def test_unknown_tenant_404(self, client):
        """Request for unknown tenant returns 404."""
        with patch("app.routers.forms.load_yaml_config") as mock_cfg:
            mock_cfg.return_value = {"tenants": {}}

            resp = client.get("/form/nonexistent/onboarding")
            assert resp.status_code == 404

    def test_unknown_form_404(self, client):
        """Request for unknown form slug returns 404 with available forms."""
        with patch("app.routers.forms.load_yaml_config") as mock_cfg:
            mock_cfg.return_value = {
                "tenants": {
                    "vmc": {
                        "name": "VMC",
                        "forms": {
                            "onboarding": {"title": "Onboarding"},
                        }
                    }
                }
            }

            resp = client.get("/form/vmc/nonexistent")
            assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Flow 6: Health + Admin
# ---------------------------------------------------------------------------

class TestHealthAndAdmin:
    """GET /health and POST /admin/reload-config."""

    def test_health_returns_ok(self, client):
        """GET /health returns service status with version."""
        resp = client.get("/health")
        assert resp.status_code == 200

        data = resp.json()
        assert data["status"] == "ok"
        assert data["service"] == "neuronx-api"
        assert data["version"] == "0.4.0"
        assert "database" in data

    def test_admin_reload_valid_key(self, client):
        """POST /admin/reload-config with valid key returns 200."""
        resp = client.post(
            "/admin/reload-config",
            headers={"X-Admin-Key": "neuronx-admin-dev"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_admin_reload_invalid_key(self, client):
        """POST /admin/reload-config with invalid key returns 401."""
        resp = client.post(
            "/admin/reload-config",
            headers={"X-Admin-Key": "wrong-key"},
        )
        assert resp.status_code == 401

    def test_admin_reload_missing_key(self, client):
        """POST /admin/reload-config without key returns 422."""
        resp = client.post("/admin/reload-config")
        assert resp.status_code == 422

    def test_root_endpoint(self, client):
        """GET / returns service info with docs link."""
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["service"] == "NeuronX API"
        assert "docs" in data


# ---------------------------------------------------------------------------
# Flow 7: Failure Handling
# ---------------------------------------------------------------------------

class TestFailureHandling:
    """Error scenarios: malformed payloads, GHL failures, DLQ capture."""

    def test_voice_malformed_payload(self, client, patch_ghl):
        """Malformed VAPI payload that does not crash the API."""
        payload = {"message": {"type": "end-of-call-report"}}

        resp = client.post("/webhooks/voice", json=payload)
        # Should not crash - either returns warning or processes with defaults
        assert resp.status_code == 200
        data = resp.json()
        # No contact_id -> should return warning
        assert data["status"] == "warning" or data["status"] == "ok"

    def test_ghl_webhook_missing_type(self, client, patch_ghl):
        """GHL webhook with missing type returns no_handler for 'unknown'."""
        payload = {"locationId": "test-location-id", "id": "no-type-001"}

        resp = client.post("/webhooks/ghl", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["action"] == "no_handler"

    def test_ghl_api_error_during_voice_processing(self, client, patch_ghl, vapi_end_of_call_payload):
        """GHL API error during end-of-call processing -> error captured."""
        payload = vapi_end_of_call_payload
        payload["message"]["call"]["metadata"] = {"ghl_contact_id": "test-contact-123"}

        # Make GHL fail on update_custom_fields
        patch_ghl.update_custom_fields.side_effect = Exception("GHL API timeout")

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        # Should indicate error and DLQ save attempt
        assert data["status"] == "error"
        assert "retry" in data["message"].lower() or "failed" in data["message"].lower()

    def test_score_lead_invalid_enum(self, client):
        """POST /score/lead with invalid enum value returns 422."""
        payload = {
            "contact_id": "test",
            "r1_program_interest": "InvalidProgram",
        }
        resp = client.post("/score/lead", json=payload)
        assert resp.status_code == 422

    def test_voice_unknown_function_call(self, client, patch_ghl):
        """Unknown function name returns generic fallback response."""
        payload = {
            "message": {
                "type": "function-call",
                "functionCall": {
                    "name": "unknown_function",
                    "parameters": {},
                },
                "call": {"id": "call-unknown"},
            }
        }

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "result" in data

    def test_voice_assistant_request_event(self, client, patch_ghl):
        """assistant-request event returns not_using_dynamic_assistant."""
        payload = {
            "message": {
                "type": "assistant-request",
                "call": {"id": "call-ar-001"},
            }
        }

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200
        assert resp.json()["action"] == "not_using_dynamic_assistant"

    def test_voice_unhandled_event_type(self, client, patch_ghl):
        """Completely unknown VAPI event type returns no_handler."""
        payload = {
            "message": {
                "type": "some-future-event",
                "call": {"id": "call-future-001"},
            }
        }

        resp = client.post("/webhooks/voice", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["action"] == "no_handler"
        assert data["type"] == "some-future-event"
