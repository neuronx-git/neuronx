"""
Comprehensive service-level tests for coverage boost.
Covers: sync_service, briefing_service, document_service, analytics_service,
        doc_ocr_service, webhook_security, case_service, documenso_client, ghl_client
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock, PropertyMock
from datetime import datetime, timezone, timedelta
import json


# ── SyncService ──

class TestSyncService:
    @pytest.fixture
    def service(self):
        from app.services.sync_service import SyncService
        return SyncService()

    @pytest.mark.asyncio
    async def test_record_activity_no_db(self, service):
        """record_activity skips gracefully when no DB."""
        with patch("app.services.sync_service.database") as mock_db:
            mock_db.async_session_factory = None
            await service.record_activity("c1", "form_submitted", "test")

    @pytest.mark.asyncio
    async def test_record_activity_with_db(self, service):
        mock_session = AsyncMock()
        mock_factory = MagicMock()
        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_factory.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("app.services.sync_service.database") as mock_db:
            mock_db.async_session_factory = mock_factory
            await service.record_activity("c1", "form_submitted", "test", {"key": "val"})
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_sync_contact_no_db(self, service):
        with patch("app.services.sync_service.database") as mock_db:
            mock_db.async_session_factory = None
            await service.sync_contact("c1")

    @pytest.mark.asyncio
    async def test_sync_contact_new(self, service):
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_factory = MagicMock()
        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_factory.return_value.__aexit__ = AsyncMock(return_value=False)

        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Priya", "lastName": "Sharma",
            "email": "p@test.com", "phone": "+1234",
            "tags": ["nx:scored"], "source": "web",
            "customFields": [
                {"id": "ai_readiness_score", "value": "80"},
                {"id": "ai_readiness_outcome", "value": "ready_standard"},
                {"id": "ai_program_interest", "value": "Express Entry"},
            ],
        }

        with patch("app.services.sync_service.database") as mock_db, \
             patch("app.services.sync_service.GHLClient", return_value=mock_ghl):
            mock_db.async_session_factory = mock_factory
            await service.sync_contact("c1")
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_sync_contact_existing(self, service):
        existing = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_factory = MagicMock()
        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_factory.return_value.__aexit__ = AsyncMock(return_value=False)

        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Priya", "lastName": "Sharma",
            "email": "p@test.com", "phone": "+1234",
            "tags": [], "source": "web",
            "customFields": [],
        }

        with patch("app.services.sync_service.database") as mock_db, \
             patch("app.services.sync_service.GHLClient", return_value=mock_ghl):
            mock_db.async_session_factory = mock_factory
            await service.sync_contact("c1")
            assert existing.first_name == "Priya"

    @pytest.mark.asyncio
    async def test_full_sync_no_db(self, service):
        with patch("app.services.sync_service.database") as mock_db:
            mock_db.async_session_factory = None
            result = await service.full_sync()
            assert result["error"] == "Database not configured"

    @pytest.mark.asyncio
    async def test_full_sync_with_data(self, service):
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_factory = MagicMock()
        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_factory.return_value.__aexit__ = AsyncMock(return_value=False)

        mock_ghl = AsyncMock()
        mock_ghl.search_contacts.return_value = {"contacts": [{"id": "c1"}]}
        mock_ghl.get_contact.return_value = {
            "firstName": "A", "lastName": "B", "email": "", "phone": "",
            "tags": [], "source": "", "customFields": [],
        }
        mock_ghl.get_pipeline_opportunities.return_value = {
            "opportunities": [{"id": "o1", "contactId": "c1", "pipelineId": "p1",
                               "pipelineStageId": "s1", "status": "open",
                               "monetaryValue": 3500, "assignedTo": ""}]
        }

        with patch("app.services.sync_service.database") as mock_db, \
             patch("app.services.sync_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.sync_service.asyncio.sleep", new_callable=AsyncMock):
            mock_db.async_session_factory = mock_factory
            result = await service.full_sync()
            assert result["status"] == "completed"
            assert result["contacts_synced"] == 1

    @pytest.mark.asyncio
    async def test_full_sync_contact_error(self, service):
        mock_session = AsyncMock()
        mock_factory = MagicMock()
        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_factory.return_value.__aexit__ = AsyncMock(return_value=False)

        mock_ghl = AsyncMock()
        mock_ghl.search_contacts.side_effect = Exception("API down")
        mock_ghl.get_pipeline_opportunities.return_value = {"opportunities": []}

        with patch("app.services.sync_service.database") as mock_db, \
             patch("app.services.sync_service.GHLClient", return_value=mock_ghl):
            mock_db.async_session_factory = mock_factory
            result = await service.full_sync()
            assert result["status"] == "completed"
            assert result["contacts_synced"] == 0


# ── BriefingService ──

class TestBriefingService:
    @pytest.fixture
    def service(self):
        from app.services.briefing_service import BriefingService
        return BriefingService()

    @pytest.mark.asyncio
    async def test_generate_and_deliver_email_and_note(self, service):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Priya", "lastName": "Sharma",
            "email": "priya@test.com", "phone": "+1234",
            "source": "Website",
            "tags": ["nx:score:high", "nx:urgent"],
            "notes": [{"body": "Called in. Very interested."}],
            "customFields": [
                {"id": "ai_program_interest", "value": "Express Entry"},
                {"id": "ai_current_location", "value": "Outside Canada"},
                {"id": "ai_timeline_urgency", "value": "Urgent (30 days)"},
                {"id": "ai_prior_applications", "value": "None"},
                {"id": "ai_budget_awareness", "value": "Aware"},
                {"id": "ai_readiness_outcome", "value": "ready_urgent"},
                {"id": "ai_readiness_score", "value": "85"},
            ],
        }
        mock_ghl.get_appointment.return_value = {"startTime": "2026-04-15T10:00:00Z"}
        mock_ghl.get_opportunities_by_contact.return_value = []
        mock_ghl.send_email = AsyncMock()
        mock_ghl.add_note = AsyncMock()

        with patch("app.services.briefing_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.briefing_service.log_event"):
            result = await service.generate_and_deliver("c1", "a1", "rcic@test.com")

        assert result["status"] == "delivered"
        assert "priya" in result["briefing_summary"].lower() or "Priya" in result["briefing_summary"]
        mock_ghl.send_email.assert_called_once()
        mock_ghl.add_note.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_note_only(self, service):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Wei", "lastName": "Chen", "email": "", "phone": "",
            "source": "", "tags": [], "notes": [],
            "customFields": [],
        }
        mock_ghl.get_appointment.return_value = {"start_time": "TBD"}
        mock_ghl.get_opportunities_by_contact.return_value = []

        with patch("app.services.briefing_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.briefing_service.log_event"):
            result = await service.generate_and_deliver("c2", "a2", "rcic@test.com", "note_only")

        assert "ghl_note" in result["delivered_to"][0]

    @pytest.mark.asyncio
    async def test_generate_email_only_failure(self, service):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "X", "lastName": "Y", "email": "", "phone": "",
            "source": "", "tags": ["nx:human_escalation", "nx:score:low"],
            "notes": [],
            "customFields": [{"id": "ai_readiness_score", "value": "invalid"}],
        }
        mock_ghl.get_appointment.return_value = {}
        mock_ghl.get_opportunities_by_contact.return_value = []
        mock_ghl.send_email.side_effect = Exception("Email blocked in sandbox")

        with patch("app.services.briefing_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.briefing_service.log_event"):
            result = await service.generate_and_deliver("c3", "a3", "rcic@test.com", "email_only")
        assert result["status"] == "delivered"

    def test_assemble_briefing_all_flags(self, service):
        briefing = service._assemble_briefing(
            contact={"firstName": "A", "lastName": "B", "phone": "123",
                     "email": "a@b.com", "source": "Web",
                     "tags": ["nx:human_escalation", "nx:urgent", "nx:score:low"],
                     "notes": [{"body": "Note 1"}, {"body": "Note 2"}]},
            appointment={"startTime": "2026-04-15T10:00:00Z"},
            custom_fields={
                "ai_program_interest": "Express Entry",
                "ai_current_location": "In Canada",
                "ai_timeline_urgency": "Urgent",
                "ai_prior_applications": "Has Refusal",
                "ai_budget_awareness": "Unaware",
                "ai_readiness_outcome": "ready_complex",
                "ai_readiness_score": "35",
            },
            opportunities=[],
        )
        assert "plain_text" in briefing
        assert "html" in briefing
        assert "summary" in briefing
        assert "COMPLEX CASE" in briefing["plain_text"]
        assert "URGENT" in briefing["plain_text"]
        assert "LOW SCORE" in briefing["plain_text"]

    def test_assemble_briefing_no_flags(self, service):
        briefing = service._assemble_briefing(
            contact={"firstName": "C", "lastName": "D", "phone": "",
                     "email": "", "source": "", "tags": [], "notes": []},
            appointment={},
            custom_fields={"ai_readiness_score": "90"},
            opportunities=[],
        )
        assert "No escalation flags" in briefing["plain_text"]


# ── DocumentService ──

class TestDocumentService:
    @pytest.mark.asyncio
    async def test_generate_retainer_no_docxtpl(self):
        from app.services.document_service import DocumentService
        svc = DocumentService()
        with patch.dict("sys.modules", {"docxtpl": None}):
            with patch("builtins.__import__", side_effect=ImportError("no docxtpl")):
                result = await svc.generate_retainer("c1")
                assert result is None

    @pytest.mark.asyncio
    async def test_generate_retainer_no_template(self):
        from app.services.document_service import DocumentService
        svc = DocumentService()
        with patch("app.services.document_service.TEMPLATES_DIR", MagicMock()) as mock_dir:
            mock_path = MagicMock()
            mock_path.exists.return_value = False
            mock_dir.__truediv__ = MagicMock(return_value=mock_path)
            result = await svc.generate_retainer("c1")
            assert result is None

    @pytest.mark.asyncio
    async def test_generate_retainer_success(self):
        from app.services.document_service import DocumentService

        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Test", "lastName": "User",
            "email": "t@t.com", "phone": "+1",
            "customFields": [{"id": "ai_program_interest", "value": "Express Entry"}],
        }

        mock_doc = MagicMock()
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_path.__str__ = MagicMock(return_value="/fake/path/retainer_agreement.docx")

        with patch("app.services.document_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.document_service.TEMPLATES_DIR") as mock_dir:
            mock_dir.__truediv__ = MagicMock(return_value=mock_path)
            # Patch the import of DocxTemplate inside the function
            import sys
            mock_docxtpl = MagicMock()
            mock_docxtpl.DocxTemplate.return_value = mock_doc
            with patch.dict(sys.modules, {"docxtpl": mock_docxtpl}):
                svc = DocumentService()
                result = await svc.generate_retainer("c1", 5000.0, "Full upfront", 400.0)
                mock_doc.render.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_assessment_no_template(self):
        from app.services.document_service import DocumentService
        svc = DocumentService()
        with patch("app.services.document_service.TEMPLATES_DIR", MagicMock()) as mock_dir:
            mock_path = MagicMock()
            mock_path.exists.return_value = False
            mock_dir.__truediv__ = MagicMock(return_value=mock_path)
            result = await svc.generate_assessment("c1")
            assert result is None


# ── AnalyticsService ──

class TestAnalyticsService:
    @pytest.fixture
    def service(self):
        from app.services.analytics_service import AnalyticsService
        return AnalyticsService()

    @pytest.mark.asyncio
    async def test_pipeline_metrics(self, service):
        mock_ghl = AsyncMock()
        mock_ghl.get_pipeline_opportunities.return_value = [
            {"pipelineStageId": "s1"}, {"pipelineStageId": "s1"}, {"pipelineStageId": "s2"},
        ]
        with patch("app.services.analytics_service.GHLClient", return_value=mock_ghl):
            result = await service.get_pipeline_metrics(30)
        assert result["total_opportunities"] == 3
        assert "s1" in result["stage_distribution"]

    @pytest.mark.asyncio
    async def test_pipeline_metrics_error(self, service):
        mock_ghl = AsyncMock()
        mock_ghl.get_pipeline_opportunities.side_effect = Exception("fail")
        with patch("app.services.analytics_service.GHLClient", return_value=mock_ghl):
            result = await service.get_pipeline_metrics()
        assert result["total_opportunities"] == 0

    @pytest.mark.asyncio
    async def test_stuck_leads(self, service):
        old_date = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
        mock_ghl = AsyncMock()
        mock_ghl.get_pipeline_opportunities.return_value = [
            {"id": "o1", "contactId": "c1", "name": "Test",
             "pipelineStageId": "s1", "updatedAt": old_date},
            {"id": "o2", "contactId": "c2", "name": "Recent",
             "pipelineStageId": "s2", "updatedAt": datetime.now(timezone.utc).isoformat()},
        ]
        with patch("app.services.analytics_service.GHLClient", return_value=mock_ghl):
            result = await service.get_stuck_leads(3)
        assert result["stuck_count"] == 1
        assert result["stuck_leads"][0]["id"] == "o1"

    @pytest.mark.asyncio
    async def test_stuck_leads_error(self, service):
        mock_ghl = AsyncMock()
        mock_ghl.get_pipeline_opportunities.side_effect = Exception("fail")
        with patch("app.services.analytics_service.GHLClient", return_value=mock_ghl):
            result = await service.get_stuck_leads()
        assert result["stuck_count"] == 0

    @pytest.mark.asyncio
    async def test_daily_summary(self, service):
        mock_ghl = AsyncMock()
        mock_ghl.get_pipeline_opportunities.return_value = [{"id": "o1"}, {"id": "o2"}]
        with patch("app.services.analytics_service.GHLClient", return_value=mock_ghl):
            result = await service.get_daily_summary()
        assert result["total_pipeline_opportunities"] == 2

    @pytest.mark.asyncio
    async def test_daily_summary_error(self, service):
        mock_ghl = AsyncMock()
        mock_ghl.get_pipeline_opportunities.side_effect = Exception("down")
        with patch("app.services.analytics_service.GHLClient", return_value=mock_ghl):
            result = await service.get_daily_summary()
        assert "error" in result


# ── DocOCRService ──

class TestDocOCRService:
    @pytest.fixture
    def service(self):
        from app.services.doc_ocr_service import DocOCRService
        return DocOCRService()

    def test_detect_type(self, service):
        assert service._detect_type("my_passport.jpg") == "passport"
        assert service._detect_type("ielts_result.pdf") == "ielts"
        assert service._detect_type("wes_eca.pdf") == "eca"
        assert service._detect_type("employment_letter.pdf") == "employment_letter"
        assert service._detect_type("marriage_cert.jpg") == "marriage_certificate"
        assert service._detect_type("bank_statement.pdf") == "bank_statement"
        assert service._detect_type("police_clearance.pdf") == "police_clearance"
        assert service._detect_type("random_doc.pdf") == "general"
        assert service._detect_type("PASSPORT_SCAN.PNG") == "passport"
        assert service._detect_type("celpip_scores.pdf") == "ielts"

    def test_parse_json_direct(self, service):
        result = service._parse_json_from_response('{"name": "John"}')
        assert result == {"name": "John"}

    def test_parse_json_markdown(self, service):
        result = service._parse_json_from_response('Here is data:\n```json\n{"name": "John"}\n```\nDone.')
        assert result == {"name": "John"}

    def test_parse_json_embedded(self, service):
        result = service._parse_json_from_response('Some text {"name": "John"} more text')
        assert result == {"name": "John"}

    def test_parse_json_invalid(self, service):
        result = service._parse_json_from_response('No JSON here at all')
        assert result == {}

    def test_get_supported_types(self, service):
        types = service.get_supported_types()
        assert len(types) >= 6
        labels = [t["label"] for t in types]
        assert "Passport" in labels

    @pytest.mark.asyncio
    async def test_extract_auto_detect(self, service):
        with patch.object(service, '_extract_passport', new_callable=AsyncMock) as mock_p:
            mock_p.return_value = {"method": "fastmrz", "extracted_fields": {"full_name": "John"}, "field_count": 1, "confidence": "high"}
            result = await service.extract(b"fake", "passport_scan.jpg", "auto")
            assert result["doc_type"] == "passport"
            mock_p.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_claude_type(self, service):
        with patch.object(service, '_extract_with_claude', new_callable=AsyncMock) as mock_c:
            mock_c.return_value = {"method": "claude", "extracted_fields": {"score": "7.5"}, "field_count": 1, "confidence": "medium"}
            result = await service.extract(b"fake", "ielts.pdf", "ielts")
            assert result["doc_type"] == "ielts"
            mock_c.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_passport_fastmrz(self, service):
        mock_mrz = MagicMock()
        mock_mrz_instance = MagicMock()
        mock_mrz_instance.get_mrz.return_value = {
            "given_name": "JOHN", "surname": "DOE",
            "date_of_birth": "1990-01-15", "document_number": "AB123456",
            "expiry_date": "2030-12-31", "nationality": "CAN", "sex": "M",
        }
        mock_mrz.return_value = mock_mrz_instance

        with patch("app.services.doc_ocr_service.FastMRZ", mock_mrz, create=True), \
             patch("builtins.__import__", wraps=__builtins__.__import__ if hasattr(__builtins__, '__import__') else __import__):
            # Use a mock for the import
            import sys
            mock_fastmrz_mod = MagicMock()
            mock_fastmrz_mod.FastMRZ = mock_mrz
            with patch.dict(sys.modules, {"fastmrz": mock_fastmrz_mod}):
                result = await service._extract_passport(b"fake_image_data", "passport.jpg")
                assert result["method"] == "fastmrz"
                assert result["extracted_fields"]["full_name"] == "JOHN DOE"

    @pytest.mark.asyncio
    async def test_extract_passport_no_mrz_fallback(self, service):
        import sys
        mock_mod = MagicMock()
        mock_inst = MagicMock()
        mock_inst.get_mrz.return_value = None
        mock_mod.FastMRZ.return_value = mock_inst

        with patch.dict(sys.modules, {"fastmrz": mock_mod}), \
             patch.object(service, '_extract_with_claude', new_callable=AsyncMock) as mock_claude:
            mock_claude.return_value = {"method": "claude", "extracted_fields": {}, "field_count": 0, "confidence": "low"}
            result = await service._extract_passport(b"fake", "passport.jpg")
            mock_claude.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_with_claude_no_key(self, service):
        with patch("app.services.doc_ocr_service.settings") as mock_s:
            mock_s.anthropic_api_key = ""
            mock_s.ollama_cloud_api_key = ""
            result = await service._extract_with_claude(b"fake", "doc.pdf", {"prompt": "test"})
            assert "not configured" in result.get("error", "").lower() or "no llm" in result.get("error", "").lower()

    @pytest.mark.asyncio
    async def test_extract_with_claude_success(self, service):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{"text": '{"candidate_name": "John Doe", "overall_score": "7.5"}'}]
        }

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_response)

        with patch("app.services.doc_ocr_service.settings") as mock_s, \
             patch("app.services.doc_ocr_service.httpx.AsyncClient", return_value=mock_client):
            mock_s.anthropic_api_key = "test-key"
            mock_s.ollama_cloud_api_key = ""
            mock_s.briefing_model = "claude-sonnet-4-6"
            result = await service._extract_with_claude(b"fake", "ielts.pdf", {"prompt": "Extract"})
            assert "anthropic" in result["method"]
            assert result["extracted_fields"]["candidate_name"] == "John Doe"

    @pytest.mark.asyncio
    async def test_extract_with_claude_api_error(self, service):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_response)

        with patch("app.services.doc_ocr_service.settings") as mock_s, \
             patch("app.services.doc_ocr_service.httpx.AsyncClient", return_value=mock_client):
            mock_s.anthropic_api_key = "key"
            mock_s.briefing_model = "m"
            result = await service._extract_with_claude(b"fake", "doc.pdf", {"prompt": "x"})
            assert "error" in result

    @pytest.mark.asyncio
    async def test_extract_with_claude_exception(self, service):
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(side_effect=Exception("network error"))

        with patch("app.services.doc_ocr_service.settings") as mock_s, \
             patch("app.services.doc_ocr_service.httpx.AsyncClient", return_value=mock_client):
            mock_s.anthropic_api_key = "key"
            mock_s.briefing_model = "m"
            result = await service._extract_with_claude(b"fake", "doc.pdf", {"prompt": "x"})
            assert result["confidence"] == "none"


# ── WebhookSecurity ──

class TestWebhookSecurity:
    def test_ghl_verification_disabled(self):
        from app.services.webhook_security import verify_ghl_signature, VERIFY_WEBHOOKS
        # In tests, VERIFY_WEBHOOKS is false via conftest
        result = verify_ghl_signature(b"body", None)
        assert result is True

    def test_vapi_verification_disabled(self):
        from app.services.webhook_security import verify_vapi_signature
        result = verify_vapi_signature(b"body", None)
        assert result is True

    def test_ghl_verification_enabled_no_sig(self):
        import os
        from importlib import reload
        old = os.environ.get("VERIFY_WEBHOOKS")
        os.environ["VERIFY_WEBHOOKS"] = "true"
        try:
            import app.services.webhook_security as ws
            reload(ws)
            if ws.VERIFY_WEBHOOKS:
                from fastapi import HTTPException
                with pytest.raises(HTTPException) as exc_info:
                    ws.verify_ghl_signature(b"body", None)
                assert exc_info.value.status_code == 401
        finally:
            os.environ["VERIFY_WEBHOOKS"] = "false"
            reload(ws)

    def test_ghl_timestamp_too_old(self):
        import os
        from importlib import reload
        os.environ["VERIFY_WEBHOOKS"] = "true"
        try:
            import app.services.webhook_security as ws
            reload(ws)
            if ws.VERIFY_WEBHOOKS:
                from fastapi import HTTPException
                old_ts = str(int(datetime.now().timestamp()) - 600)
                with pytest.raises(HTTPException):
                    ws.verify_ghl_signature(b"body", "fakesig", old_ts)
        finally:
            os.environ["VERIFY_WEBHOOKS"] = "false"
            reload(ws)

    def test_ghl_invalid_timestamp(self):
        import os
        from importlib import reload
        os.environ["VERIFY_WEBHOOKS"] = "true"
        try:
            import app.services.webhook_security as ws
            reload(ws)
            if ws.VERIFY_WEBHOOKS:
                from fastapi import HTTPException
                with pytest.raises(HTTPException):
                    ws.verify_ghl_signature(b"body", "sig", "not-a-number")
        finally:
            os.environ["VERIFY_WEBHOOKS"] = "false"
            reload(ws)

    def test_ghl_no_public_key_configured(self):
        import os
        from importlib import reload
        os.environ["VERIFY_WEBHOOKS"] = "true"
        try:
            import app.services.webhook_security as ws
            reload(ws)
            if ws.VERIFY_WEBHOOKS:
                with patch("app.services.webhook_security.settings") as mock_s:
                    mock_s.ghl_webhook_secret = ""
                    ts = str(int(datetime.now().timestamp()))
                    result = ws.verify_ghl_signature(b"body", "sig", ts)
                    assert result is True
        finally:
            os.environ["VERIFY_WEBHOOKS"] = "false"
            reload(ws)

    def test_vapi_no_secret_configured(self):
        import os
        from importlib import reload
        os.environ["VERIFY_WEBHOOKS"] = "true"
        try:
            import app.services.webhook_security as ws
            reload(ws)
            if ws.VERIFY_WEBHOOKS:
                with patch("app.services.webhook_security.settings") as mock_s:
                    mock_s.vapi_webhook_secret = ""
                    result = ws.verify_vapi_signature(b"body", "sig")
                    assert result is True
        finally:
            os.environ["VERIFY_WEBHOOKS"] = "false"
            reload(ws)

    def test_vapi_valid_hmac(self):
        import os, hmac, hashlib
        from importlib import reload
        os.environ["VERIFY_WEBHOOKS"] = "true"
        try:
            import app.services.webhook_security as ws
            reload(ws)
            if ws.VERIFY_WEBHOOKS:
                secret = "test-secret"
                body = b"test body"
                sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
                with patch("app.services.webhook_security.settings") as mock_s:
                    mock_s.vapi_webhook_secret = secret
                    result = ws.verify_vapi_signature(body, sig)
                    assert result is True
        finally:
            os.environ["VERIFY_WEBHOOKS"] = "false"
            reload(ws)

    def test_vapi_invalid_hmac(self):
        import os
        from importlib import reload
        os.environ["VERIFY_WEBHOOKS"] = "true"
        try:
            import app.services.webhook_security as ws
            reload(ws)
            if ws.VERIFY_WEBHOOKS:
                from fastapi import HTTPException
                with patch("app.services.webhook_security.settings") as mock_s:
                    mock_s.vapi_webhook_secret = "secret"
                    with pytest.raises(HTTPException):
                        ws.verify_vapi_signature(b"body", "wrong-sig")
        finally:
            os.environ["VERIFY_WEBHOOKS"] = "false"
            reload(ws)


# ── CaseService ──

class TestCaseService:
    @pytest.fixture
    def service(self):
        from app.services.case_service import CaseService
        return CaseService()

    def test_get_ircc_forms(self, service):
        forms = service.get_ircc_forms("Express Entry")
        assert isinstance(forms, list)

    def test_get_processing_estimate(self, service):
        est = service.get_processing_estimate("Express Entry")
        assert "min" in est

    @pytest.mark.asyncio
    async def test_initiate_case(self, service):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {"firstName": "Test", "lastName": "User"}
        with patch("app.services.case_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.case_service.log_event"):
            result = await service.initiate_case("c1", "Express Entry", "Rajiv Mehta")
            assert result["status"] == "onboarding"
            assert result["case_id"].startswith("NX-")
            mock_ghl.update_custom_fields.assert_called_once()
            mock_ghl.add_tags.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_stage_valid(self, service):
        mock_ghl = AsyncMock()
        with patch("app.services.case_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.case_service.log_event"):
            result = await service.update_stage("c1", "doc_collection", "Collecting docs")
            assert result["stage"] == "doc_collection"
            mock_ghl.add_tag.assert_called_once()
            mock_ghl.add_note.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_stage_invalid(self, service):
        result = await service.update_stage("c1", "nonexistent_stage")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_update_stage_no_notes(self, service):
        mock_ghl = AsyncMock()
        with patch("app.services.case_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.case_service.log_event"):
            result = await service.update_stage("c1", "submitted")
            assert result["tag_added"] == "nx:case:submitted"
            mock_ghl.update_custom_fields.assert_not_called()

    @pytest.mark.asyncio
    async def test_record_submission(self, service):
        mock_ghl = AsyncMock()
        with patch("app.services.case_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.case_service.log_event"):
            result = await service.record_submission("c1", "E000123", "2026-04-01")
            assert result["status"] == "submitted"
            assert result["receipt_number"] == "E000123"

    @pytest.mark.asyncio
    async def test_record_decision_approved(self, service):
        mock_ghl = AsyncMock()
        with patch("app.services.case_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.case_service.log_event"):
            result = await service.record_decision("c1", "Approved", "2026-04-10", "Congrats!")
            assert result["decision"] == "Approved"

    @pytest.mark.asyncio
    async def test_record_decision_invalid(self, service):
        result = await service.record_decision("c1", "InvalidDecision")
        assert "error" in result


# ── DocumensoClient ──

class TestDocumensoClient:
    def test_not_configured(self):
        from app.services.documenso_client import DocumensoClient
        with patch("app.services.documenso_client.settings") as mock_s:
            mock_s.documenso_url = ""
            mock_s.documenso_api_key = ""
            client = DocumensoClient()
            assert not client.is_configured()

    def test_is_configured(self):
        from app.services.documenso_client import DocumensoClient
        with patch("app.services.documenso_client.settings") as mock_s:
            mock_s.documenso_url = "https://sign.example.com"
            mock_s.documenso_api_key = "key123"
            client = DocumensoClient()
            assert client.is_configured()

    @pytest.mark.asyncio
    async def test_create_document_not_configured(self):
        from app.services.documenso_client import DocumensoClient
        with patch("app.services.documenso_client.settings") as mock_s:
            mock_s.documenso_url = ""
            mock_s.documenso_api_key = ""
            client = DocumensoClient()
            result = await client.create_document("Test", b"pdf", "a@b.com", "A B")
            assert result is None

    @pytest.mark.asyncio
    async def test_create_document_success(self):
        from app.services.documenso_client import DocumensoClient

        mock_http = AsyncMock()
        mock_http.__aenter__ = AsyncMock(return_value=mock_http)
        mock_http.__aexit__ = AsyncMock(return_value=False)

        mock_resp1 = MagicMock()
        mock_resp1.json.return_value = {"id": "doc-123"}
        mock_resp1.raise_for_status = MagicMock()

        mock_resp2 = MagicMock()
        mock_resp2.raise_for_status = MagicMock()

        mock_resp3 = MagicMock()
        mock_resp3.raise_for_status = MagicMock()

        mock_http.post = AsyncMock(side_effect=[mock_resp1, mock_resp2, mock_resp3])

        with patch("app.services.documenso_client.settings") as mock_s, \
             patch("app.services.documenso_client.httpx.AsyncClient", return_value=mock_http):
            mock_s.documenso_url = "https://sign.example.com"
            mock_s.documenso_api_key = "key"
            client = DocumensoClient()
            result = await client.create_document("Retainer", b"pdf", "a@b.com", "A B")
            assert result["document_id"] == "doc-123"
            assert result["status"] == "sent"

    @pytest.mark.asyncio
    async def test_create_document_no_id(self):
        from app.services.documenso_client import DocumensoClient

        mock_http = AsyncMock()
        mock_http.__aenter__ = AsyncMock(return_value=mock_http)
        mock_http.__aexit__ = AsyncMock(return_value=False)
        mock_resp = MagicMock()
        mock_resp.json.return_value = {}
        mock_resp.raise_for_status = MagicMock()
        mock_http.post = AsyncMock(return_value=mock_resp)

        with patch("app.services.documenso_client.settings") as mock_s, \
             patch("app.services.documenso_client.httpx.AsyncClient", return_value=mock_http):
            mock_s.documenso_url = "https://sign.example.com"
            mock_s.documenso_api_key = "key"
            client = DocumensoClient()
            result = await client.create_document("R", b"p", "a@b.com", "A")
            assert result is None

    @pytest.mark.asyncio
    async def test_create_document_http_error(self):
        from app.services.documenso_client import DocumensoClient
        import httpx

        mock_http = AsyncMock()
        mock_http.__aenter__ = AsyncMock(return_value=mock_http)
        mock_http.__aexit__ = AsyncMock(return_value=False)
        mock_http.post = AsyncMock(side_effect=httpx.HTTPError("fail"))

        with patch("app.services.documenso_client.settings") as mock_s, \
             patch("app.services.documenso_client.httpx.AsyncClient", return_value=mock_http):
            mock_s.documenso_url = "https://sign.example.com"
            mock_s.documenso_api_key = "key"
            client = DocumensoClient()
            result = await client.create_document("R", b"p", "a@b.com", "A")
            assert result is None

    @pytest.mark.asyncio
    async def test_get_document_status_not_configured(self):
        from app.services.documenso_client import DocumensoClient
        with patch("app.services.documenso_client.settings") as mock_s:
            mock_s.documenso_url = ""
            mock_s.documenso_api_key = ""
            client = DocumensoClient()
            result = await client.get_document_status("doc-1")
            assert result is None

    @pytest.mark.asyncio
    async def test_get_document_status_success(self):
        from app.services.documenso_client import DocumensoClient

        mock_http = AsyncMock()
        mock_http.__aenter__ = AsyncMock(return_value=mock_http)
        mock_http.__aexit__ = AsyncMock(return_value=False)
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"status": "COMPLETED"}
        mock_resp.raise_for_status = MagicMock()
        mock_http.get = AsyncMock(return_value=mock_resp)

        with patch("app.services.documenso_client.settings") as mock_s, \
             patch("app.services.documenso_client.httpx.AsyncClient", return_value=mock_http):
            mock_s.documenso_url = "https://sign.example.com"
            mock_s.documenso_api_key = "key"
            client = DocumensoClient()
            result = await client.get_document_status("doc-1")
            assert result["status"] == "COMPLETED"


# ── GHLClient ──

class TestGHLClient:
    def test_init_default(self):
        from app.services.ghl_client import GHLClient
        client = GHLClient()
        assert client.base_url is not None

    def test_init_custom_location(self):
        from app.services.ghl_client import GHLClient
        client = GHLClient(location_id="custom-loc")
        assert client.location_id == "custom-loc"

    def test_get_token_from_env(self):
        from app.services.ghl_client import GHLClient
        GHLClient._cached_token = None
        GHLClient._token_expires_at = 0
        with patch("app.services.ghl_client.TOKEN_FILE") as mock_tf, \
             patch("app.services.ghl_client.settings") as mock_s:
            mock_tf.exists.return_value = False
            mock_s.ghl_access_token = "env-token"
            client = GHLClient()
            assert client._get_token() == "env-token"

    def test_get_token_from_file(self):
        import time
        from app.services.ghl_client import GHLClient
        GHLClient._cached_token = None
        GHLClient._token_expires_at = 0
        with patch("app.services.ghl_client.TOKEN_FILE") as mock_tf:
            mock_tf.exists.return_value = True
            mock_tf.read_text.return_value = '{"access_token": "file-token"}'
            client = GHLClient()
            assert client._get_token() == "file-token"
            assert GHLClient._cached_token == "file-token"

    def test_get_token_cached(self):
        import time
        from app.services.ghl_client import GHLClient
        GHLClient._cached_token = "cached-token"
        GHLClient._token_expires_at = time.time() + 3600
        client = GHLClient()
        assert client._get_token() == "cached-token"
        GHLClient._cached_token = None
        GHLClient._token_expires_at = 0

    def test_get_token_no_source(self):
        from app.services.ghl_client import GHLClient
        GHLClient._cached_token = None
        GHLClient._token_expires_at = 0
        with patch("app.services.ghl_client.TOKEN_FILE") as mock_tf, \
             patch("app.services.ghl_client.settings") as mock_s:
            mock_tf.exists.return_value = False
            mock_s.ghl_access_token = ""
            client = GHLClient()
            with pytest.raises(RuntimeError):
                client._get_token()

    def test_headers_property(self):
        from app.services.ghl_client import GHLClient
        GHLClient._cached_token = "test-token"
        GHLClient._token_expires_at = 9999999999
        client = GHLClient()
        h = client.headers
        assert h["Authorization"] == "Bearer test-token"
        assert "Version" in h
        GHLClient._cached_token = None
        GHLClient._token_expires_at = 0
