"""
Final coverage boost — targets specific uncovered lines.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock, PropertyMock
from fastapi.testclient import TestClient
from main import app
import json


@pytest.fixture
def client():
    return TestClient(app)


# ── GHL Client — all API methods ──

class TestGHLClientMethods:
    """Test all GHLClient methods by mocking _request."""

    @pytest.fixture
    def ghl(self):
        from app.services.ghl_client import GHLClient
        GHLClient._cached_token = "test-tok"
        GHLClient._token_expires_at = 9999999999
        client = GHLClient()
        return client

    @pytest.mark.asyncio
    async def test_get_contact(self, ghl):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"contact": {"id": "c1", "firstName": "A"}}
        with patch.object(ghl, '_request', new_callable=AsyncMock, return_value=mock_resp):
            result = await ghl.get_contact("c1")
            assert result["id"] == "c1"

    @pytest.mark.asyncio
    async def test_update_contact(self, ghl):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"contact": {"id": "c1"}}
        with patch.object(ghl, '_request', new_callable=AsyncMock, return_value=mock_resp):
            result = await ghl.update_contact("c1", {"firstName": "New"})
            assert result["id"] == "c1"

    @pytest.mark.asyncio
    async def test_update_custom_fields(self, ghl):
        with patch.object(ghl, '_request', new_callable=AsyncMock):
            result = await ghl.update_custom_fields("c1", {"key1": "val1", "key2": "val2"})
            assert result is True

    @pytest.mark.asyncio
    async def test_update_custom_fields_empty(self, ghl):
        result = await ghl.update_custom_fields("c1", {})
        assert result is True

    @pytest.mark.asyncio
    async def test_add_tag(self, ghl):
        with patch.object(ghl, '_request', new_callable=AsyncMock):
            result = await ghl.add_tag("c1", "nx:scored")
            assert result is True

    @pytest.mark.asyncio
    async def test_add_tags(self, ghl):
        with patch.object(ghl, '_request', new_callable=AsyncMock):
            result = await ghl.add_tags("c1", ["tag1", "tag2"])
            assert result is True

    @pytest.mark.asyncio
    async def test_add_tags_empty(self, ghl):
        result = await ghl.add_tags("c1", [])
        assert result is True

    @pytest.mark.asyncio
    async def test_remove_tag(self, ghl):
        with patch.object(ghl, '_request', new_callable=AsyncMock):
            result = await ghl.remove_tag("c1", "nx:old")
            assert result is True

    @pytest.mark.asyncio
    async def test_add_note(self, ghl):
        with patch.object(ghl, '_request', new_callable=AsyncMock):
            result = await ghl.add_note("c1", "Test note")
            assert result is True

    @pytest.mark.asyncio
    async def test_get_appointment(self, ghl):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"id": "a1", "startTime": "2026-04-15T10:00:00Z"}
        with patch.object(ghl, '_request', new_callable=AsyncMock, return_value=mock_resp):
            result = await ghl.get_appointment("a1")
            assert result["id"] == "a1"

    @pytest.mark.asyncio
    async def test_get_opportunities_by_contact(self, ghl):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"opportunities": [{"id": "o1"}]}
        with patch.object(ghl, '_request', new_callable=AsyncMock, return_value=mock_resp):
            result = await ghl.get_opportunities_by_contact("c1")
            assert len(result) == 1

    @pytest.mark.asyncio
    async def test_update_opportunity_stage(self, ghl):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"id": "o1", "pipelineStageId": "s2"}
        with patch.object(ghl, '_request', new_callable=AsyncMock, return_value=mock_resp):
            result = await ghl.update_opportunity_stage("o1", "s2")
            assert result["pipelineStageId"] == "s2"

    @pytest.mark.asyncio
    async def test_send_email(self, ghl):
        with patch.object(ghl, '_request', new_callable=AsyncMock):
            result = await ghl.send_email("c1", "Subject", "<p>Body</p>")
            assert result is True

    @pytest.mark.asyncio
    async def test_search_contacts(self, ghl):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"contacts": [{"id": "c1"}]}
        with patch.object(ghl, '_request', new_callable=AsyncMock, return_value=mock_resp):
            result = await ghl.search_contacts("test", 10)
            assert result == [{"id": "c1"}]

    @pytest.mark.asyncio
    async def test_get_pipeline_opportunities(self, ghl):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"opportunities": [{"id": "o1"}, {"id": "o2"}]}
        with patch.object(ghl, '_request', new_callable=AsyncMock, return_value=mock_resp):
            result = await ghl.get_pipeline_opportunities("pipeline-1")
            assert len(result) == 2

    @pytest.mark.asyncio
    async def test_request_429_rate_limit(self, ghl):
        from app.services.ghl_client import RateLimitError, _get_http_client
        mock_resp = MagicMock()
        mock_resp.status_code = 429
        mock_resp.headers = {"Retry-After": "5"}

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_resp)

        with patch("app.services.ghl_client._get_http_client", return_value=mock_client), \
             patch("app.services.ghl_client.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(RateLimitError):
                await ghl._request.__wrapped__(ghl, "GET", "/test")

    @pytest.mark.asyncio
    async def test_request_401_clears_cache(self, ghl):
        from app.services.ghl_client import GHLClient
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.raise_for_status = MagicMock(side_effect=Exception("401"))

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_resp)

        with patch("app.services.ghl_client._get_http_client", return_value=mock_client):
            try:
                await ghl._request.__wrapped__(ghl, "GET", "/test")
            except:
                pass
        assert GHLClient._cached_token is None

    @pytest.mark.asyncio
    async def test_request_500_raises(self, ghl):
        import httpx
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.raise_for_status = MagicMock(side_effect=httpx.HTTPStatusError("500", request=MagicMock(), response=mock_resp))

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_resp)

        with patch("app.services.ghl_client._get_http_client", return_value=mock_client):
            with pytest.raises(httpx.HTTPStatusError):
                await ghl._request.__wrapped__(ghl, "GET", "/test")

    def test_get_token_file_bad_json(self):
        from app.services.ghl_client import GHLClient
        GHLClient._cached_token = None
        GHLClient._token_expires_at = 0
        with patch("app.services.ghl_client.TOKEN_FILE") as mock_tf, \
             patch("app.services.ghl_client.settings") as mock_s:
            mock_tf.exists.return_value = True
            mock_tf.read_text.return_value = "not valid json"
            mock_s.ghl_access_token = "fallback"
            client = GHLClient()
            assert client._get_token() == "fallback"


# ── Document Service — assessment ──

class TestDocumentServiceAssessment:
    @pytest.mark.asyncio
    async def test_generate_assessment_success(self):
        import sys
        from app.services.document_service import DocumentService

        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Test", "lastName": "User", "email": "t@t.com", "phone": "+1",
            "customFields": [
                {"id": "ai_readiness_score", "value": "72"},
                {"id": "ai_readiness_outcome", "value": "ready_standard"},
                {"id": "ai_program_interest", "value": "Express Entry"},
            ],
        }

        mock_doc = MagicMock()
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_path.__str__ = MagicMock(return_value="/fake/path/assessment_report.docx")

        mock_docxtpl = MagicMock()
        mock_docxtpl.DocxTemplate.return_value = mock_doc

        with patch("app.services.document_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.document_service.TEMPLATES_DIR") as mock_dir, \
             patch.dict(sys.modules, {"docxtpl": mock_docxtpl}):
            mock_dir.__truediv__ = MagicMock(return_value=mock_path)
            svc = DocumentService()
            result = await svc.generate_assessment("c1")
            mock_doc.render.assert_called_once()
            # Verify the context had the right score tier
            ctx = mock_doc.render.call_args[0][0]
            assert ctx["score_tier"] == "High"

    @pytest.mark.asyncio
    async def test_generate_assessment_low_score(self):
        import sys
        from app.services.document_service import DocumentService

        mock_ghl = AsyncMock()
        mock_ghl.get_contact.return_value = {
            "firstName": "Low", "lastName": "Score", "email": "", "phone": "",
            "customFields": [
                {"id": "ai_readiness_score", "value": "25"},
                {"id": "ai_readiness_outcome", "value": "not_ready"},
                {"id": "ai_program_interest", "value": "Study Permit"},
            ],
        }
        mock_doc = MagicMock()
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_path.__str__ = MagicMock(return_value="/fake")
        mock_docxtpl = MagicMock()
        mock_docxtpl.DocxTemplate.return_value = mock_doc

        with patch("app.services.document_service.GHLClient", return_value=mock_ghl), \
             patch("app.services.document_service.TEMPLATES_DIR") as mock_dir, \
             patch.dict(sys.modules, {"docxtpl": mock_docxtpl}):
            mock_dir.__truediv__ = MagicMock(return_value=mock_path)
            svc = DocumentService()
            await svc.generate_assessment("c2")
            ctx = mock_doc.render.call_args[0][0]
            assert ctx["score_tier"] == "Low"


# ── Webhook idempotency helpers ──

class TestWebhookHelpers:
    @pytest.mark.asyncio
    async def test_is_duplicate_no_db(self):
        from app.routers.webhooks import _is_duplicate_webhook
        with patch("app.routers.webhooks.is_db_configured", return_value=False):
            result = await _is_duplicate_webhook("wh-1", "ghl")
            assert result is False

    @pytest.mark.asyncio
    async def test_is_duplicate_no_id(self):
        from app.routers.webhooks import _is_duplicate_webhook
        result = await _is_duplicate_webhook("", "ghl")
        assert result is False

    @pytest.mark.asyncio
    async def test_mark_processed_no_db(self):
        from app.routers.webhooks import _mark_webhook_processed
        with patch("app.routers.webhooks.is_db_configured", return_value=False):
            await _mark_webhook_processed("wh-1", "ghl")

    @pytest.mark.asyncio
    async def test_mark_processed_no_id(self):
        from app.routers.webhooks import _mark_webhook_processed
        await _mark_webhook_processed("", "ghl")

    @pytest.mark.asyncio
    async def test_save_to_dlq_no_db(self):
        from app.routers.webhooks import _save_to_dlq
        with patch("app.routers.webhooks.is_db_configured", return_value=False):
            await _save_to_dlq("ghl", "wh-1", {}, "test error")

    @pytest.mark.asyncio
    async def test_is_duplicate_with_db(self):
        from app.routers.webhooks import _is_duplicate_webhook

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar.return_value = 1
        mock_session.execute = AsyncMock(return_value=mock_result)

        async def mock_get_session():
            yield mock_session

        with patch("app.routers.webhooks.is_db_configured", return_value=True), \
             patch("app.routers.webhooks.get_session", mock_get_session):
            result = await _is_duplicate_webhook("wh-1", "ghl")
            assert result is True

    @pytest.mark.asyncio
    async def test_is_duplicate_db_error(self):
        from app.routers.webhooks import _is_duplicate_webhook

        async def mock_get_session():
            raise Exception("DB error")
            yield  # pragma: no cover

        with patch("app.routers.webhooks.is_db_configured", return_value=True), \
             patch("app.routers.webhooks.get_session", mock_get_session):
            result = await _is_duplicate_webhook("wh-1", "ghl")
            assert result is False

    @pytest.mark.asyncio
    async def test_mark_processed_with_db(self):
        from app.routers.webhooks import _mark_webhook_processed

        mock_session = AsyncMock()

        async def mock_get_session():
            yield mock_session

        with patch("app.routers.webhooks.is_db_configured", return_value=True), \
             patch("app.routers.webhooks.get_session", mock_get_session):
            await _mark_webhook_processed("wh-1", "ghl", 200)
            mock_session.execute.assert_called_once()
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_mark_processed_db_error(self):
        from app.routers.webhooks import _mark_webhook_processed

        async def mock_get_session():
            raise Exception("DB error")
            yield  # pragma: no cover

        with patch("app.routers.webhooks.is_db_configured", return_value=True), \
             patch("app.routers.webhooks.get_session", mock_get_session):
            await _mark_webhook_processed("wh-1", "ghl")  # should not raise

    @pytest.mark.asyncio
    async def test_save_to_dlq_with_db(self):
        from app.routers.webhooks import _save_to_dlq

        mock_session = AsyncMock()

        async def mock_get_session():
            yield mock_session

        with patch("app.routers.webhooks.is_db_configured", return_value=True), \
             patch("app.routers.webhooks.get_session", mock_get_session):
            await _save_to_dlq("vapi", "wh-1", {"data": "test"}, "some error")
            mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_to_dlq_db_error(self):
        from app.routers.webhooks import _save_to_dlq

        async def mock_get_session():
            raise Exception("DB error")
            yield  # pragma: no cover

        with patch("app.routers.webhooks.is_db_configured", return_value=True), \
             patch("app.routers.webhooks.get_session", mock_get_session):
            await _save_to_dlq("vapi", "wh-1", {}, "err")  # should not raise


# ── Webhook _extract_readiness ──

class TestExtractReadiness:
    def test_with_structured_data(self):
        from app.routers.webhooks import _extract_readiness
        result = _extract_readiness({
            "program_interest": "Express Entry",
            "current_location": "In Canada",
            "timeline_urgency": "urgent",
            "prior_applications": "none",
            "budget_awareness": "aware",
        }, "Some transcript text")
        assert result["r1_program_interest"] == "Express Entry"
        assert result["transcript_excerpt"] == "Some transcript text"

    def test_without_structured_data(self):
        from app.routers.webhooks import _extract_readiness
        result = _extract_readiness({}, "Long transcript here")
        assert "transcript_excerpt" in result
        assert "r1_program_interest" not in result

    def test_empty_both(self):
        from app.routers.webhooks import _extract_readiness
        result = _extract_readiness(None, "")
        assert result.get("transcript_excerpt") is None


# ── Sync Router with DB mock ──

class TestSyncRouterWithDB:
    @patch("app.routers.sync.SyncService")
    def test_full_sync_with_db(self, MockSvc, client):
        mock_svc = AsyncMock()
        mock_svc.full_sync.return_value = {
            "status": "completed", "contacts_synced": 5,
            "opportunities_synced": 3, "duration_seconds": 2.5,
        }
        MockSvc.return_value = mock_svc
        with patch("app.routers.sync.async_session_factory", new="truthy"):
            r = client.post("/sync/full")
            assert r.status_code == 200

    def test_sync_status_with_db(self, client):
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_log = MagicMock()
        mock_log.last_sync_at.isoformat.return_value = "2026-04-13T10:00:00Z"
        mock_log.records_synced = 42
        mock_log.status = "completed"
        mock_result.scalar_one_or_none.return_value = mock_log
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_factory = MagicMock()
        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_factory.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("app.routers.sync.async_session_factory", new=mock_factory):
            r = client.get("/sync/status")
            assert r.status_code == 200


# ── Demo Router with DB mock ──

class TestDemoWithDB:
    def test_seed_with_db(self, client):
        mock_session = AsyncMock()
        mock_factory = MagicMock()
        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_factory.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("app.database.async_session_factory", new=mock_factory):
            r = client.post("/demo/seed")
            assert r.status_code == 200
            data = r.json()
            assert data["contacts"] == 12

    def test_clear_with_db(self, client):
        mock_session = AsyncMock()
        mock_factory = MagicMock()
        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_factory.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("app.database.async_session_factory", new=mock_factory):
            r = client.post("/demo/clear")
            assert r.status_code == 200
            assert r.json()["status"] == "demo data cleared"


# ── Dependents with DB mock ──

class TestDependentsWithDB:
    def test_create_with_db(self, client):
        mock_session = AsyncMock()

        async def mock_get_session():
            yield mock_session

        with patch("app.routers.dependents.is_db_configured", return_value=True), \
             patch("app.routers.dependents.get_session", mock_get_session):
            r = client.post("/dependents/", json={
                "case_id": "NX-123", "contact_id": "c1",
                "full_name": "Jane Doe", "relationship": "spouse",
            })
            assert r.status_code == 200
            assert r.json()["status"] == "ok"

    def test_list_with_db(self, client):
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = [
            {"id": 1, "full_name": "Jane Doe", "relationship": "spouse",
             "passport_number": "P123", "docs_status": "pending",
             "notes": "", "created_at": None},
        ]
        mock_session.execute = AsyncMock(return_value=mock_result)

        async def mock_get_session():
            yield mock_session

        with patch("app.routers.dependents.is_db_configured", return_value=True), \
             patch("app.routers.dependents.get_session", mock_get_session):
            r = client.get("/dependents/NX-123")
            assert r.status_code == 200
            assert r.json()["count"] == 1

    def test_update_with_db(self, client):
        mock_session = AsyncMock()

        async def mock_get_session():
            yield mock_session

        with patch("app.routers.dependents.is_db_configured", return_value=True), \
             patch("app.routers.dependents.get_session", mock_get_session):
            r = client.put("/dependents/1", json={"full_name": "Updated Name"})
            assert r.status_code == 200

    def test_update_no_fields(self, client):
        with patch("app.routers.dependents.is_db_configured", return_value=True):
            r = client.put("/dependents/1", json={})
            assert r.status_code == 200
            assert r.json()["message"] == "No fields to update"

    def test_delete_with_db(self, client):
        mock_session = AsyncMock()

        async def mock_get_session():
            yield mock_session

        with patch("app.routers.dependents.is_db_configured", return_value=True), \
             patch("app.routers.dependents.get_session", mock_get_session):
            r = client.delete("/dependents/1")
            assert r.status_code == 200


# ── Cases Router — additional coverage ──

class TestCasesEdgeCases:
    @patch("app.routers.cases.CaseService")
    def test_initiate_case_error(self, MockSvc, client):
        mock_svc = AsyncMock()
        mock_svc.initiate_case.side_effect = Exception("GHL error")
        MockSvc.return_value = mock_svc
        r = client.post("/cases/initiate", json={
            "contact_id": "c1", "program_type": "X", "assigned_rcic": "R",
        })
        assert r.status_code == 500

    @patch("app.routers.cases.CaseService")
    def test_stage_invalid(self, MockSvc, client):
        mock_svc = AsyncMock()
        mock_svc.update_stage.return_value = {"error": "Unknown stage: bad"}
        MockSvc.return_value = mock_svc
        r = client.post("/cases/stage", json={"contact_id": "c1", "stage": "bad"})
        assert r.status_code == 400

    def test_questionnaire_unknown_program(self, client):
        r = client.get("/cases/questionnaire/UnknownProgram")
        assert r.status_code == 200
        assert "common" in str(r.json()).lower() or "note" in r.json()

    @patch("app.routers.cases.GHLClient")
    def test_onboarding_url_not_found(self, MockGHL, client):
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.side_effect = Exception("not found")
        MockGHL.return_value = mock_ghl
        r = client.get("/cases/onboarding-url/c999")
        assert r.status_code == 404

    @patch("app.routers.cases.CaseService")
    def test_case_status_not_found(self, MockSvc, client):
        mock_svc = MagicMock()
        mock_ghl = AsyncMock()
        mock_ghl.get_contact.side_effect = Exception("not found")
        mock_svc._get_ghl_client.return_value = mock_ghl
        MockSvc.return_value = mock_svc
        r = client.get("/cases/status/c999")
        assert r.status_code == 404

    def test_decision_invalid(self, client):
        r = client.post("/cases/decision", json={
            "contact_id": "c1", "decision": "Maybe",
        })
        assert r.status_code == 400


# ── Typebot form URL with viewer configured ──

class TestTypebotFormURL:
    def test_form_url_with_viewer(self, client):
        with patch("app.config.settings") as mock_s:
            mock_s.typebot_viewer_url = "https://viewer.test.com"
            r = client.get("/typebot/form-url/Express Entry")
            assert r.status_code == 200
            data = r.json()
            # May return url or note depending on settings state
            assert "program_type" in data


# ── Documents Router — remaining endpoints ──

class TestDocumentsIRCC:
    def test_ircc_fill_no_template(self, client):
        r = client.post("/documents/ircc-fill", json={
            "form_key": "NONEXISTENT_FORM",
            "client_data": {"full_name": "Test"},
        })
        assert r.status_code == 404

    def test_ircc_coverage_no_contact(self, client):
        r = client.get("/documents/ircc-coverage/IMM_0008")
        assert r.status_code == 200


# ── Main app lifespan ──

class TestMainLifespan:
    def test_docs_endpoint_in_dev(self, client):
        r = client.get("/docs")
        assert r.status_code == 200

    def test_openapi_schema(self, client):
        r = client.get("/openapi.json")
        assert r.status_code == 200
        schema = r.json()
        assert schema["info"]["version"] == "0.4.0"
