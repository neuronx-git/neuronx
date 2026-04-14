"""
Comprehensive router-level tests for coverage boost.
Covers: clients, cases, dependents, signatures, webhooks, typebot, demo,
        briefings, doc_extract, sync, analytics, documents, main
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from main import app
import json


@pytest.fixture
def client():
    return TestClient(app)


# ── Clients Router ──

class TestClientsRouter:
    @patch("app.routers.clients.GHLClient")
    def test_search_success(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.search_contacts.return_value = {
            "contacts": [
                {"id": "c1", "firstName": "Priya", "lastName": "Sharma",
                 "email": "p@test.com", "phone": "+1234", "tags": []},
            ]
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/search?q=Priya")
        assert r.status_code == 200
        assert r.json()["total"] == 1

    @patch("app.routers.clients.GHLClient")
    def test_search_ghl_error(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.search_contacts.side_effect = Exception("GHL down")
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/search?q=test")
        assert r.status_code == 503

    @patch("app.routers.clients.GHLClient")
    def test_form_data_success(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Wei", "lastName": "Chen",
            "email": "w@test.com", "phone": "+1",
            "address1": "123 Main St",
            "customFields": [
                {"id": "ai_program_interest", "value": "Express Entry"},
                {"id": "date_of_birth", "value": "1990-05-15"},
                {"id": "country_of_citizenship", "value": "China"},
                {"id": "passport_number", "value": "E12345678"},
            ],
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c1/form-data")
        assert r.status_code == 200
        data = r.json()
        assert data["email"] == "w@test.com"
        assert data["contact_id"] == "c1"

    @patch("app.routers.clients.GHLClient")
    def test_form_data_not_found(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.side_effect = Exception("Not found")
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c999/form-data")
        assert r.status_code == 404

    @patch("app.routers.clients.GHLClient")
    def test_data_sheet_success(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Test", "lastName": "User",
            "email": "t@t.com", "phone": "+1", "address1": "",
            "customFields": [
                {"id": "ai_program_interest", "value": "Work Permit"},
                {"id": "employer_name", "value": "Acme Corp"},
            ],
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c1/data-sheet")
        assert r.status_code == 200
        data = r.json()
        assert "sections" in data

    @patch("app.routers.clients.GHLClient")
    def test_data_sheet_not_found(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.side_effect = Exception("nope")
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c999/data-sheet")
        assert r.status_code == 404

    @patch("app.routers.clients.GHLClient")
    def test_validate_completeness(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "A", "lastName": "B",
            "email": "a@b.com", "phone": "+1",
            "customFields": [
                {"id": "ai_program_interest", "value": "Express Entry"},
                {"id": "country_of_citizenship", "value": "India"},
                {"id": "passport_number", "value": "J12345"},
                {"id": "marital_status", "value": "Single"},
                {"id": "criminal_history", "value": "None"},
                {"id": "previous_refusal", "value": "No"},
                {"id": "education_level", "value": "Masters"},
                {"id": "work_experience", "value": "5 years"},
                {"id": "language_test", "value": "IELTS"},
            ],
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c1/validate")
        assert r.status_code == 200
        data = r.json()
        assert data["is_complete"] is True

    @patch("app.routers.clients.GHLClient")
    def test_validate_incomplete(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "", "lastName": "", "email": "", "phone": "",
            "customFields": [],
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c1/validate")
        assert r.status_code == 200
        assert r.json()["is_complete"] is False

    @patch("app.routers.clients.GHLClient")
    def test_validate_spousal(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "A", "lastName": "B", "email": "a@b.com", "phone": "+1",
            "customFields": [
                {"id": "ai_program_interest", "value": "Spousal Sponsorship"},
                {"id": "country_of_citizenship", "value": "X"},
                {"id": "passport_number", "value": "Y"},
                {"id": "marital_status", "value": "Married"},
                {"id": "criminal_history", "value": "None"},
                {"id": "previous_refusal", "value": "No"},
                {"id": "sponsor_status", "value": "Citizen"},
                {"id": "relationship_type", "value": "Spouse"},
            ],
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c1/validate")
        assert r.status_code == 200

    @patch("app.routers.clients.GHLClient")
    def test_validate_work_permit(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "A", "lastName": "B", "email": "a@b.com", "phone": "+1",
            "customFields": [
                {"id": "ai_program_interest", "value": "Work Permit"},
                {"id": "country_of_citizenship", "value": "X"},
                {"id": "passport_number", "value": "Y"},
                {"id": "marital_status", "value": "Single"},
                {"id": "criminal_history", "value": "None"},
                {"id": "previous_refusal", "value": "No"},
                {"id": "employer_name", "value": "Acme"},
                {"id": "lmia_status", "value": "Approved"},
            ],
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c1/validate")
        assert r.status_code == 200

    @patch("app.routers.clients.GHLClient")
    def test_copy_paste_guide(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Test", "lastName": "User",
            "email": "t@t.com", "phone": "+1234",
            "address1": "123 St",
            "customFields": [
                {"id": "ai_program_interest", "value": "Express Entry"},
                {"id": "date_of_birth", "value": "1990-01-01"},
            ],
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c1/copy-paste")
        assert r.status_code == 200
        assert "personal_details" in r.json()

    @patch("app.routers.clients.GHLClient")
    def test_copy_paste_not_found(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.side_effect = Exception("nope")
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c999/copy-paste")
        assert r.status_code == 404

    @patch("app.routers.clients.GHLClient")
    def test_data_sheet_study_permit(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "S", "lastName": "P", "email": "", "phone": "",
            "address1": "",
            "customFields": [{"id": "ai_program_interest", "value": "Study Permit"}],
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/clients/c1/data-sheet")
        assert r.status_code == 200


# ── Briefings Router ──

class TestBriefingsRouter:
    @patch("app.routers.briefings.BriefingService")
    def test_generate_briefing_success(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.generate_and_deliver.return_value = {
            "status": "delivered", "contact_id": "c1",
            "appointment_id": "a1", "briefing_summary": "Test summary",
            "delivered_to": ["email:rcic@test.com"],
        }
        MockService.return_value = mock_svc
        r = client.post("/briefing/generate", json={
            "contact_id": "c1", "appointment_id": "a1",
            "consultant_email": "rcic@test.com",
        })
        assert r.status_code == 200
        assert r.json()["status"] == "delivered"

    @patch("app.routers.briefings.BriefingService")
    def test_generate_briefing_error(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.generate_and_deliver.side_effect = Exception("GHL down")
        MockService.return_value = mock_svc
        r = client.post("/briefing/generate", json={
            "contact_id": "c1", "appointment_id": "a1",
            "consultant_email": "rcic@test.com",
        })
        assert r.status_code == 500


# ── Doc Extract Router ──

class TestDocExtractRouter:
    @patch("app.routers.doc_extract.DocOCRService")
    def test_upload_success(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.extract.return_value = {
            "doc_type": "passport", "method": "fastmrz",
            "extracted_fields": {"full_name": "John Doe"},
            "field_count": 1, "confidence": "high",
        }
        MockService.return_value = mock_svc
        r = client.post(
            "/extract/upload",
            files={"file": ("passport.jpg", b"fake_image_data", "image/jpeg")},
            data={"doc_type": "passport"},
        )
        assert r.status_code == 200
        assert r.json()["doc_type"] == "passport"

    @patch("app.routers.doc_extract.DocOCRService")
    def test_upload_empty_file(self, MockService, client):
        r = client.post(
            "/extract/upload",
            files={"file": ("empty.jpg", b"", "image/jpeg")},
        )
        assert r.status_code == 400

    @patch("app.routers.doc_extract.DocOCRService")
    def test_upload_too_large(self, MockService, client):
        r = client.post(
            "/extract/upload",
            files={"file": ("big.jpg", b"x" * (11 * 1024 * 1024), "image/jpeg")},
        )
        assert r.status_code == 413


# ── Sync Router ──

class TestSyncRouter:
    def test_full_sync_no_db(self, client):
        r = client.post("/sync/full")
        data = r.json()
        assert "error" in data or "status" in data

    def test_sync_status_no_db(self, client):
        r = client.get("/sync/status")
        assert r.status_code == 200


# ── Analytics Router ──

class TestAnalyticsRouter:
    @patch("app.routers.analytics.AnalyticsService")
    def test_pipeline(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.get_pipeline_metrics.return_value = {
            "period_days": 30, "total_opportunities": 5,
            "stage_distribution": {"s1": 3, "s2": 2},
            "as_of": "2026-04-13", "north_star": {},
        }
        MockService.return_value = mock_svc
        r = client.get("/analytics/pipeline?days=30")
        assert r.status_code == 200

    @patch("app.routers.analytics.AnalyticsService")
    def test_stuck(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.get_stuck_leads.return_value = {
            "threshold_days": 3, "stuck_count": 0, "stuck_leads": [],
        }
        MockService.return_value = mock_svc
        r = client.get("/analytics/stuck?threshold_days=3")
        assert r.status_code == 200

    @patch("app.routers.analytics.AnalyticsService")
    def test_dashboard(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.get_daily_summary.return_value = {
            "date": "2026-04-13", "total_pipeline_opportunities": 10,
            "pipeline_id": "test",
        }
        MockService.return_value = mock_svc
        r = client.get("/analytics/dashboard")
        assert r.status_code == 200


# ── Signatures Router ──

class TestSignaturesRouter:
    @patch("app.routers.signatures.DocumensoClient")
    def test_send_no_documenso(self, MockDocumenso, client):
        mock = MagicMock()
        mock.is_configured.return_value = False
        MockDocumenso.return_value = mock
        r = client.post("/signatures/send", json={
            "contact_id": "c1", "retainer_amount": 3500,
        })
        assert r.status_code == 503

    @patch("app.routers.signatures.DocumensoClient")
    @patch("app.routers.signatures.DocumentService")
    @patch("app.routers.signatures.GHLClient")
    def test_send_success(self, MockGHL, MockDocSvc, MockDocumenso, client):
        mock_documenso = MagicMock()
        mock_documenso.is_configured.return_value = True
        mock_documenso.create_document = AsyncMock(return_value={"document_id": "d1", "status": "sent"})
        MockDocumenso.return_value = mock_documenso

        mock_doc_svc = AsyncMock()
        mock_doc_svc.generate_retainer.return_value = b"fake-docx-bytes"
        MockDocSvc.return_value = mock_doc_svc

        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Test", "lastName": "User", "email": "t@t.com",
        }
        MockGHL.return_value = mock_ghl

        with patch("app.routers.signatures.is_db_configured", return_value=False):
            r = client.post("/signatures/send", json={"contact_id": "c1"})
        assert r.status_code == 200
        assert r.json()["status"] == "sent"

    @patch("app.routers.signatures.DocumensoClient")
    @patch("app.routers.signatures.DocumentService")
    @patch("app.routers.signatures.GHLClient")
    def test_send_no_email(self, MockGHL, MockDocSvc, MockDocumenso, client):
        mock_documenso = MagicMock()
        mock_documenso.is_configured.return_value = True
        MockDocumenso.return_value = mock_documenso

        mock_doc_svc = AsyncMock()
        mock_doc_svc.generate_retainer.return_value = b"bytes"
        MockDocSvc.return_value = mock_doc_svc

        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {"firstName": "A", "lastName": "B", "email": ""}
        MockGHL.return_value = mock_ghl

        r = client.post("/signatures/send", json={"contact_id": "c1"})
        assert r.status_code == 400

    @patch("app.routers.signatures.DocumensoClient")
    @patch("app.routers.signatures.DocumentService")
    def test_send_generate_fails(self, MockDocSvc, MockDocumenso, client):
        mock_documenso = MagicMock()
        mock_documenso.is_configured.return_value = True
        MockDocumenso.return_value = mock_documenso

        mock_doc_svc = AsyncMock()
        mock_doc_svc.generate_retainer.return_value = None
        MockDocSvc.return_value = mock_doc_svc

        r = client.post("/signatures/send", json={"contact_id": "c1"})
        assert r.status_code == 500

    @patch("app.routers.signatures.GHLClient")
    def test_documenso_webhook_signed(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.search_contacts.return_value = {
            "contacts": [{"id": "c1"}]
        }
        MockGHL.return_value = mock_ghl

        with patch("app.routers.signatures.is_db_configured", return_value=False):
            r = client.post("/signatures/webhook", json={
                "event": "DOCUMENT_SIGNED",
                "data": {"recipients": [{"email": "test@test.com"}]},
            })
        assert r.status_code == 200
        assert r.json()["status"] == "processed"

    def test_documenso_webhook_unmatched(self, client):
        with patch("app.routers.signatures.GHLClient") as MockGHL:
            mock_ghl = AsyncMock()
            mock_ghl.search_contacts.return_value = {"contacts": []}
            MockGHL.return_value = mock_ghl
            r = client.post("/signatures/webhook", json={
                "event": "DOCUMENT_COMPLETED",
                "data": {"recipients": [{"email": "unknown@test.com"}]},
            })
        assert r.json()["status"] == "unmatched"

    def test_documenso_webhook_ignored_event(self, client):
        r = client.post("/signatures/webhook", json={
            "event": "DOCUMENT_OPENED", "data": {},
        })
        assert r.json()["status"] == "ignored"

    @patch("app.routers.signatures.DocumensoClient")
    def test_signature_status_no_documenso(self, MockDocumenso, client):
        mock = MagicMock()
        mock.is_configured.return_value = False
        MockDocumenso.return_value = mock
        r = client.get("/signatures/status/doc-1")
        assert r.status_code == 503

    @patch("app.routers.signatures.DocumensoClient")
    def test_signature_status_success(self, MockDocumenso, client):
        mock = MagicMock()
        mock.is_configured.return_value = True
        mock.get_document_status = AsyncMock(return_value={"status": "COMPLETED"})
        MockDocumenso.return_value = mock
        r = client.get("/signatures/status/doc-1")
        assert r.status_code == 200

    @patch("app.routers.signatures.DocumensoClient")
    def test_signature_status_not_found(self, MockDocumenso, client):
        mock = MagicMock()
        mock.is_configured.return_value = True
        mock.get_document_status = AsyncMock(return_value=None)
        MockDocumenso.return_value = mock
        r = client.get("/signatures/status/doc-1")
        assert r.status_code == 404


# ── Demo Router ──

class TestDemoRouter:
    def test_seed_no_db(self, client):
        r = client.post("/demo/seed")
        data = r.json()
        assert "error" in data

    def test_clear_no_db(self, client):
        r = client.post("/demo/clear")
        data = r.json()
        assert "error" in data


# ── Typebot Router ──

class TestTypebotRouter:
    @patch("app.routers.typebot.GHLClient")
    def test_webhook_with_contact_id(self, MockGHL, client):
        mock_ghl = AsyncMock()
        MockGHL.return_value = mock_ghl
        r = client.post("/typebot/webhook", json={
            "contact_id": "c1",
            "answers": {"program_interest": "Express Entry", "full_name": "John Doe"},
        })
        assert r.status_code == 200
        assert r.json()["status"] == "processed"

    @patch("app.routers.typebot.GHLClient")
    def test_webhook_search_by_email(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.search_contacts.return_value = {"contacts": [{"id": "c2"}]}
        MockGHL.return_value = mock_ghl
        r = client.post("/typebot/webhook", json={
            "email": "test@test.com",
            "answers": {"program_interest": "Work Permit"},
        })
        assert r.status_code == 200
        assert r.json()["contact_id"] == "c2"

    @patch("app.routers.typebot.GHLClient")
    def test_webhook_search_by_phone(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.search_contacts.side_effect = [
            {"contacts": []},  # email search
            {"contacts": [{"id": "c3"}]},  # phone search
        ]
        MockGHL.return_value = mock_ghl
        r = client.post("/typebot/webhook", json={
            "phone": "+14165551234",
            "answers": {},
        })
        assert r.status_code == 200

    @patch("app.routers.typebot.GHLClient")
    def test_webhook_unmatched(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.search_contacts.return_value = {"contacts": []}
        MockGHL.return_value = mock_ghl
        r = client.post("/typebot/webhook", json={"answers": {}})
        assert r.json()["status"] == "unmatched"

    def test_create_form_not_configured(self, client):
        with patch("app.routers.typebot.TypebotService") as MockSvc:
            mock_svc = MagicMock()
            mock_svc.is_configured.return_value = False
            MockSvc.return_value = mock_svc
            r = client.post("/typebot/create-form", json={
                "program_type": "Express Entry",
            })
            assert r.status_code == 503

    @patch("app.routers.typebot.TypebotService")
    def test_create_form_success(self, MockSvc, client):
        mock_svc = MagicMock()
        mock_svc.is_configured.return_value = True
        mock_svc.create_onboarding_form = AsyncMock(return_value={"url": "https://form.test/ee"})
        MockSvc.return_value = mock_svc
        r = client.post("/typebot/create-form", json={
            "program_type": "Express Entry",
            "firm_name": "Test Firm",
        })
        assert r.status_code == 200

    @patch("app.routers.typebot.TypebotService")
    def test_create_form_failure(self, MockSvc, client):
        mock_svc = MagicMock()
        mock_svc.is_configured.return_value = True
        mock_svc.create_onboarding_form = AsyncMock(return_value=None)
        MockSvc.return_value = mock_svc
        r = client.post("/typebot/create-form", json={"program_type": "X"})
        assert r.status_code == 500

    def test_form_url(self, client):
        r = client.get("/typebot/form-url/Express Entry")
        assert r.status_code == 200


# ── Documents Router (additional coverage) ──

class TestDocumentsRouterExtra:
    @patch("app.routers.documents.GHLClient")
    def test_assessment_report(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Test", "lastName": "User",
            "email": "t@t.com", "phone": "+1",
            "tags": ["nx:human_escalation", "nx:urgent"],
            "customFields": [
                {"id": "ai_program_interest", "value": "Express Entry"},
                {"id": "ai_readiness_score", "value": "72"},
                {"id": "ai_readiness_outcome", "value": "ready_standard"},
            ],
        }
        MockGHL.return_value = mock_ghl
        r = client.post("/documents/assessment", json={"contact_id": "c1"})
        assert r.status_code == 200
        data = r.json()
        assert data["readiness_assessment"]["score"] == "72"

    @patch("app.routers.documents.GHLClient")
    def test_assessment_report_not_found(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.side_effect = Exception("not found")
        MockGHL.return_value = mock_ghl
        r = client.post("/documents/assessment", json={"contact_id": "c999"})
        assert r.status_code == 404

    @patch("app.routers.documents.GHLClient")
    def test_ircc_coverage_with_contact(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "A", "lastName": "B",
            "email": "a@b.com", "phone": "+1",
            "customFields": [{"id": "full_name", "value": "Test"}],
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/documents/ircc-coverage/IMM_0008?contact_id=c1")
        assert r.status_code == 200

    @patch("app.routers.documents.GHLClient")
    def test_ircc_coverage_contact_error(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.side_effect = Exception("fail")
        MockGHL.return_value = mock_ghl
        r = client.get("/documents/ircc-coverage/IMM_0008?contact_id=c999")
        assert r.status_code == 200  # graceful degradation


# ── Webhooks Router (additional coverage) ──

class TestWebhooksRouterExtra:
    def test_ghl_tag_event(self, client):
        r = client.post("/webhooks/ghl", json={
            "type": "TagAdded",
            "contactId": "c1",
            "tag": "nx:score:high",
        })
        assert r.status_code == 200
        assert r.json()["action"] == "tag_logged"

    def test_ghl_tag_event_list_format(self, client):
        r = client.post("/webhooks/ghl", json={
            "type": "ContactTagUpdate",
            "contactId": "c1",
            "tags": ["nx:contacted"],
        })
        assert r.status_code == 200

    def test_ghl_unknown_event(self, client):
        r = client.post("/webhooks/ghl", json={
            "type": "SomeUnknownEvent",
            "contactId": "c1",
        })
        assert r.status_code == 200
        assert r.json()["action"] == "no_handler"

    def test_vapi_transcript_event(self, client):
        r = client.post("/webhooks/voice", json={
            "message": {"type": "transcript", "call": {"id": "call-1"}},
        })
        assert r.status_code == 200
        assert r.json()["action"] == "transcript_logged"

    def test_vapi_assistant_request(self, client):
        r = client.post("/webhooks/voice", json={
            "message": {"type": "assistant-request", "call": {"id": "call-1"}},
        })
        assert r.status_code == 200
        assert r.json()["action"] == "not_using_dynamic_assistant"

    def test_vapi_unknown_event(self, client):
        r = client.post("/webhooks/voice", json={
            "message": {"type": "some-unknown", "call": {"id": "call-1"}},
        })
        assert r.status_code == 200
        assert r.json()["action"] == "no_handler"

    def test_vapi_function_call_collect_readiness(self, client):
        r = client.post("/webhooks/voice", json={
            "message": {
                "type": "function-call",
                "call": {"id": "call-1"},
                "functionCall": {
                    "name": "collect_readiness_data",
                    "parameters": {"program_interest": "Express Entry"},
                },
            },
        })
        assert r.status_code == 200
        assert "result" in r.json()

    def test_vapi_function_call_book_consultation(self, client):
        r = client.post("/webhooks/voice", json={
            "message": {
                "type": "function-call",
                "call": {"id": "call-1"},
                "functionCall": {"name": "book_consultation", "parameters": {}},
            },
        })
        assert r.status_code == 200
        assert "booking" in r.json()["result"].lower()

    def test_vapi_function_call_transfer(self, client):
        r = client.post("/webhooks/voice", json={
            "message": {
                "type": "function-call",
                "call": {"id": "call-1"},
                "functionCall": {"name": "transfer_to_human", "parameters": {"reason": "emotional"}},
            },
        })
        assert r.status_code == 200

    def test_vapi_function_call_unknown(self, client):
        r = client.post("/webhooks/voice", json={
            "message": {
                "type": "function-call",
                "call": {"id": "call-1"},
                "functionCall": {"name": "unknown_function", "parameters": {}},
            },
        })
        assert r.status_code == 200

    @patch("app.routers.webhooks.GHLClient")
    def test_vapi_end_of_call_full(self, MockGHL, client):
        mock_ghl = AsyncMock()
        MockGHL.return_value = mock_ghl
        r = client.post("/webhooks/voice", json={
            "message": {
                "type": "end-of-call-report",
                "call": {"id": "call-eoc-1", "metadata": {"ghl_contact_id": "c1"}},
                "transcript": "Hello, I'm interested in Express Entry.",
                "analysis": {
                    "summary": "Client interested in Express Entry",
                    "structuredData": {
                        "program_interest": "Express Entry",
                        "current_location": "Outside Canada",
                        "timeline_urgency": "near_term",
                        "prior_applications": "none",
                        "budget_awareness": "aware",
                    },
                },
            },
        })
        assert r.status_code == 200
        data = r.json()
        assert data["action"] == "scored"

    @patch("app.routers.webhooks.GHLClient")
    def test_vapi_end_of_call_no_contact(self, MockGHL, client):
        mock_ghl = AsyncMock()
        MockGHL.return_value = mock_ghl
        r = client.post("/webhooks/voice", json={
            "message": {
                "type": "end-of-call-report",
                "call": {"id": "call-no-contact", "metadata": {}},
                "transcript": "test",
                "analysis": {"summary": "test", "structuredData": {}},
            },
        })
        assert r.status_code == 200
        assert r.json()["message"] == "no_contact_id"

    @patch("app.routers.webhooks.GHLClient")
    def test_vapi_end_of_call_with_escalation(self, MockGHL, client):
        mock_ghl = AsyncMock()
        MockGHL.return_value = mock_ghl
        r = client.post("/webhooks/voice", json={
            "message": {
                "type": "end-of-call-report",
                "call": {"id": "call-esc", "metadata": {"ghl_contact_id": "c1"}},
                "transcript": "Am I eligible for permanent residence? I might be deported.",
                "analysis": {
                    "summary": "Client asked about eligibility and deportation",
                    "structuredData": {"program_interest": "Express Entry"},
                },
            },
        })
        assert r.status_code == 200


# ── Main App ──

class TestMainApp:
    def test_health(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["service"] == "neuronx-api"
        assert r.json()["version"] == "0.4.0"

    def test_root(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert "NeuronX API" in r.json()["service"]

    def test_reload_config_no_key(self, client):
        r = client.post("/admin/reload-config")
        assert r.status_code == 422

    def test_reload_config_wrong_key(self, client):
        r = client.post("/admin/reload-config", headers={"X-Admin-Key": "wrong"})
        assert r.status_code == 401

    def test_reload_config_success(self, client):
        r = client.post("/admin/reload-config", headers={"X-Admin-Key": "neuronx-admin-dev"})
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_docs_available(self, client):
        r = client.get("/docs")
        assert r.status_code == 200


# ── Config Loader ──

class TestConfigLoader:
    def test_load_scoring_config(self):
        from app.config_loader import load_scoring_config, reload_all
        reload_all()
        cfg = load_scoring_config()
        assert "thresholds" in cfg

    def test_load_programs_config(self):
        from app.config_loader import load_programs_config, reload_all
        reload_all()
        cfg = load_programs_config()
        assert len(cfg) >= 1

    def test_load_trust_config(self):
        from app.config_loader import load_trust_config, reload_all
        reload_all()
        cfg = load_trust_config()
        assert "escalation_triggers" in cfg

    def test_load_yaml_nonexistent(self):
        from app.config_loader import load_yaml_config
        result = load_yaml_config("nonexistent_file_xyz")
        assert result == {}

    def test_reload_all(self):
        from app.config_loader import reload_all
        reload_all()  # should not raise


# ── Database ──

class TestDatabase:
    def test_is_db_configured(self):
        from app.database import is_db_configured
        # Returns based on current state
        result = is_db_configured()
        assert isinstance(result, bool)

    def test_get_session_no_factory(self):
        from app.database import get_session
        import app.database as db
        old = db.async_session_factory
        db.async_session_factory = None
        with pytest.raises(RuntimeError):
            # get_session is an async generator, need to iterate
            import asyncio
            asyncio.get_event_loop().run_until_complete(get_session().__anext__())
        db.async_session_factory = old


# ── Dependents Router ──

class TestDependentsRouter:
    def test_create_no_db(self, client):
        r = client.post("/dependents/", json={
            "case_id": "NX-123", "contact_id": "c1",
            "full_name": "Jane Doe", "relationship": "spouse",
        })
        assert r.status_code == 503

    def test_list_no_db(self, client):
        r = client.get("/dependents/NX-123")
        assert r.status_code == 503

    def test_update_no_db(self, client):
        r = client.put("/dependents/1", json={"full_name": "Updated"})
        assert r.status_code == 503

    def test_delete_no_db(self, client):
        r = client.delete("/dependents/1")
        assert r.status_code == 503


# ── Cases Router (additional) ──

class TestCasesRouterExtra:
    @patch("app.routers.cases.CaseService")
    def test_initiate_case(self, MockSvc, client):
        mock_svc = AsyncMock()
        mock_svc.initiate_case.return_value = {
            "case_id": "NX-20260413-ABC12345",
            "contact_id": "c1",
            "program_type": "Express Entry",
            "assigned_rcic": "Rajiv",
            "doc_deadline": "2026-04-27T00:00:00",
            "estimated_processing_months": {"min": 6, "max": 12},
            "ircc_forms": [],
            "status": "onboarding",
        }
        MockSvc.return_value = mock_svc
        r = client.post("/cases/initiate", json={
            "contact_id": "c1",
            "program_type": "Express Entry",
            "assigned_rcic": "Rajiv",
        })
        assert r.status_code == 200
        assert r.json()["status"] == "onboarding"

    @patch("app.routers.cases.CaseService")
    def test_update_case_stage(self, MockSvc, client):
        mock_svc = AsyncMock()
        mock_svc.update_stage.return_value = {
            "contact_id": "c1", "stage": "submitted", "tag_added": "nx:case:submitted",
        }
        MockSvc.return_value = mock_svc
        r = client.post("/cases/stage", json={
            "contact_id": "c1", "stage": "submitted",
        })
        assert r.status_code == 200

    @patch("app.routers.cases.CaseService")
    def test_record_submission(self, MockSvc, client):
        mock_svc = AsyncMock()
        mock_svc.record_submission.return_value = {
            "contact_id": "c1", "receipt_number": "E000123", "status": "submitted",
        }
        MockSvc.return_value = mock_svc
        r = client.post("/cases/submission", json={
            "contact_id": "c1", "receipt_number": "E000123",
        })
        assert r.status_code == 200

    @patch("app.routers.cases.CaseService")
    def test_record_decision(self, MockSvc, client):
        mock_svc = AsyncMock()
        mock_svc.record_decision.return_value = {
            "contact_id": "c1", "decision": "Approved", "status": "decision_recorded",
        }
        MockSvc.return_value = mock_svc
        r = client.post("/cases/decision", json={
            "contact_id": "c1", "decision": "Approved",
        })
        assert r.status_code == 200

    @patch("app.routers.cases.GHLClient")
    def test_onboarding_url(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Test", "lastName": "User",
            "email": "t@t.com", "phone": "+1",
            "customFields": [
                {"id": "ai_program_interest", "value": "Express Entry"},
            ],
        }
        MockGHL.return_value = mock_ghl
        r = client.get("/cases/onboarding-url/c1")
        assert r.status_code == 200

    @patch("app.routers.cases.CaseService")
    def test_case_status(self, MockSvc, client):
        mock_svc = MagicMock()
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "A", "lastName": "B",
            "tags": ["nx:case:onboarding"],
            "customFields": [
                {"id": "case_id", "value": "NX-123"},
                {"id": "case_program_type", "value": "Express Entry"},
            ],
        }
        mock_svc._get_ghl_client.return_value = mock_ghl
        MockSvc.return_value = mock_svc
        r = client.get("/cases/status/c1")
        assert r.status_code == 200
