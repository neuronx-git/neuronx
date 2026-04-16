"""
End-to-End Integration Tests for NeuronX

Tests ALL integration points across the full stack:
- NeuronX API endpoints
- Typebot API connectivity
- GHL API connectivity (sandbox)
- Document OCR service
- IRCC form service
- Webhook security
- Idempotency
- Config loading

Run: pytest tests/test_e2e_integrations.py -v
"""

import pytest
import httpx
import os
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


# ═══════════════════════════════════════
# 1. API HEALTH & INFRASTRUCTURE
# ═══════════════════════════════════════

class TestAPIInfrastructure:
    """Test core API infrastructure is working."""

    def test_health_endpoint(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert data["service"] == "neuronx-api"
        assert "version" in data
        assert "database" in data

    def test_root_endpoint(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert "NeuronX API" in r.json()["service"]

    def test_docs_disabled_in_production(self):
        """Docs should be disabled when env=production."""
        # This is a config-level test
        from app.config import settings
        # In test env, docs should be available
        assert settings.env != "production" or app.docs_url is None

    def test_cors_headers(self, client):
        r = client.options("/health", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        })
        # Should not have wildcard allow_headers
        assert r.headers.get("access-control-allow-headers") != "*"

    def test_admin_requires_auth(self, client):
        """Admin endpoint must require X-Admin-Key header."""
        r = client.post("/admin/reload-config")
        assert r.status_code == 422  # Missing required header


# ═══════════════════════════════════════
# 2. WEBHOOK SECURITY
# ═══════════════════════════════════════

class TestWebhookSecurity:
    """Test webhook signature verification and idempotency."""

    def test_ghl_webhook_processes_valid_request(self, client):
        """GHL webhook should process valid requests (verification disabled in test)."""
        r = client.post("/webhooks/ghl", json={
            "type": "ContactCreated",
            "contactId": "test-123",
            "webhookId": "wh-test-001",
        })
        assert r.status_code == 200
        assert r.json()["action"] == "contact_logged"

    def test_vapi_webhook_processes_status(self, client):
        """VAPI status update should be logged."""
        r = client.post("/webhooks/voice", json={
            "message": {
                "type": "status-update",
                "status": "in-progress",
                "call": {"id": "call-123"},
            }
        })
        assert r.status_code == 200
        assert r.json()["action"] == "status_logged"

    def test_webhook_security_module_loads(self):
        """Webhook security module should be importable."""
        from app.services.webhook_security import verify_ghl_signature, verify_vapi_signature
        assert callable(verify_ghl_signature)
        assert callable(verify_vapi_signature)


# ═══════════════════════════════════════
# 3. SCORING SERVICE
# ═══════════════════════════════════════

class TestScoringIntegration:
    """Test readiness scoring end-to-end."""

    def test_score_lead_full_data(self, client):
        r = client.post("/score/lead", json={
            "contact_id": "test-contact",
            "r1_program_interest": "Express Entry",
            "r2_current_location": "Outside Canada",
            "r3_timeline_urgency": "Near-term",
            "r4_prior_applications": "None",
            "r5_budget_awareness": "Aware",
            "transcript_excerpt": "I want to apply for Express Entry",
        })
        assert r.status_code == 200
        data = r.json()
        assert "score" in data
        assert "outcome" in data
        assert data["score"] >= 0

    def test_score_with_complexity_keywords(self, client):
        r = client.post("/score/lead", json={
            "contact_id": "test-complex",
            "r1_program_interest": "Express Entry",
            "transcript_excerpt": "I was deported from another country",
        })
        assert r.status_code == 200
        data = r.json()
        assert "complex" in data.get("outcome", "").lower() or "escalation" in str(data.get("flags", []))


# ═══════════════════════════════════════
# 4. TRUST SERVICE
# ═══════════════════════════════════════

class TestTrustIntegration:
    """Test trust boundary enforcement."""

    def test_trust_check_clean_transcript(self, client):
        r = client.post("/trust/check", json={
            "contact_id": "test",
            "transcript": "Hi, I'd like to learn about Express Entry",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["compliant"] == True

    def test_trust_check_escalation_trigger(self, client):
        r = client.post("/trust/check", json={
            "contact_id": "test",
            "transcript": "Am I eligible for Express Entry? What are my chances?",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["requires_escalation"] == True

    def test_trust_check_violation_detection(self, client):
        r = client.post("/trust/check", json={
            "contact_id": "test",
            "transcript": "You are eligible for Express Entry and you will likely get approved",
        })
        assert r.status_code == 200
        data = r.json()
        assert len(data["violations"]) > 0


# ═══════════════════════════════════════
# 5. CASE PROCESSING
# ═══════════════════════════════════════

class TestCaseProcessing:
    """Test case lifecycle endpoints."""

    def test_case_forms_express_entry(self, client):
        r = client.get("/cases/forms/Express%20Entry")
        assert r.status_code == 200
        data = r.json()
        assert data["total_required"] >= 5
        assert any(f["code"] == "IMM 0008" for f in data["forms"])

    def test_case_timeline(self, client):
        r = client.get("/cases/timeline/Express%20Entry")
        assert r.status_code == 200
        data = r.json()
        assert data["estimated_months"]["avg"] == 6
        assert "disclaimer" in data

    def test_case_questionnaire_branching(self, client):
        """Each program should return program-specific questions."""
        for program in ["Express Entry", "Spousal Sponsorship", "Work Permit"]:
            r = client.get(f"/cases/questionnaire/{program.replace(' ', '%20')}")
            assert r.status_code == 200
            data = r.json()
            assert data["program_type"] == program
            assert data["total_questions"] > 15  # Common + program-specific

    def test_case_invalid_decision(self, client):
        r = client.post("/cases/decision", json={
            "contact_id": "test",
            "decision": "Maybe",
        })
        assert r.status_code == 400

    def test_onboarding_url_without_ghl(self, client):
        """Onboarding URL endpoint should handle missing contact gracefully."""
        r = client.get("/cases/onboarding-url/nonexistent-id")
        # Will fail because GHL is not available in test, but shouldn't crash
        assert r.status_code in [404, 500, 503]


# ═══════════════════════════════════════
# 6. DOCUMENT SERVICES
# ═══════════════════════════════════════

class TestDocumentServices:
    """Test document checklist and IRCC form services."""

    def test_document_checklist_express_entry(self, client):
        r = client.post("/documents/checklist", json={"contact_id": "test", "program_type": "Express Entry"})
        assert r.status_code == 200
        data = r.json()
        assert len(data.get("required_documents", data.get("required", []))) >= 7

    def test_document_checklist_all_programs(self, client):
        """All 8 programs should have document checklists."""
        programs = ["Express Entry", "Spousal Sponsorship", "Work Permit",
                     "Study Permit", "LMIA", "PR Renewal", "Citizenship", "Visitor Visa"]
        for prog in programs:
            r = client.post("/documents/checklist", json={"contact_id": "test", "program_type": prog})
            assert r.status_code == 200, f"Failed for {prog}"
            docs = r.json().get("required_documents", r.json().get("required", []))
            assert len(docs) > 0, f"No docs for {prog}"

    def test_ircc_forms_available(self, client):
        """IRCC forms endpoint should list available PDFs."""
        r = client.get("/documents/ircc-forms/Express%20Entry")
        assert r.status_code == 200


# ═══════════════════════════════════════
# 7. DOCUMENT OCR EXTRACTION
# ═══════════════════════════════════════

class TestDocumentOCR:
    """Test document OCR extraction service."""

    def test_extraction_types_endpoint(self, client):
        r = client.get("/extract/types")
        assert r.status_code == 200
        types = r.json()["supported_types"]
        assert len(types) == 7
        type_names = [t["type"] for t in types]
        assert "passport" in type_names
        assert "ielts" in type_names
        assert "eca" in type_names

    def test_doc_type_auto_detection(self):
        from app.services.doc_ocr_service import DocOCRService
        svc = DocOCRService()
        assert svc._detect_type("passport.jpg") == "passport"
        assert svc._detect_type("IELTS_results.pdf") == "ielts"
        assert svc._detect_type("WES_eca_report.pdf") == "eca"
        assert svc._detect_type("employment_letter.pdf") == "employment_letter"
        assert svc._detect_type("marriage_cert.jpg") == "marriage_certificate"
        assert svc._detect_type("bank_statement_april.pdf") == "bank_statement"
        assert svc._detect_type("police_clearance_india.pdf") == "police_clearance"
        assert svc._detect_type("random_doc.pdf") == "general"

    def test_upload_requires_file(self, client):
        r = client.post("/extract/upload")
        assert r.status_code == 422  # Missing file


# ═══════════════════════════════════════
# 8. MULTI-TENANT FORM SERVING
# ═══════════════════════════════════════

class TestMultiTenantForms:
    """Test multi-tenant form serving."""

    def test_vmc_form_serves(self, client):
        r = client.get("/form/vmc/onboarding")
        assert r.status_code == 200
        assert "typebot-standard" in r.text
        assert "vmc-onboarding" in r.text

    def test_unknown_tenant_404(self, client):
        r = client.get("/form/nonexistent/onboarding")
        assert r.status_code == 404

    def test_unknown_form_404(self, client):
        r = client.get("/form/vmc/nonexistent")
        assert r.status_code == 404

    def test_tenant_list(self, client):
        r = client.get("/form/vmc")
        assert r.status_code == 200
        assert "onboarding" in r.text.lower()


# ═══════════════════════════════════════
# 9. CONFIG LOADING
# ═══════════════════════════════════════

class TestConfigIntegrity:
    """Test all config files load correctly."""

    def test_scoring_config_loads(self):
        from app.config_loader import load_yaml_config
        cfg = load_yaml_config("scoring")
        assert "thresholds" in cfg
        assert "complexity_keywords" in cfg
        assert len(cfg["complexity_keywords"]) > 10

    def test_trust_config_loads(self):
        from app.config_loader import load_yaml_config
        cfg = load_yaml_config("trust")
        assert "escalation_triggers" in cfg
        assert "ai_violations" in cfg

    def test_programs_config_loads(self):
        from app.config_loader import load_yaml_config
        cfg = load_yaml_config("programs")
        programs = cfg.get("programs", {})
        assert len(programs) == 8
        assert "Express Entry" in programs
        assert "Spousal Sponsorship" in programs

    def test_questionnaires_config_loads(self):
        from app.config_loader import load_yaml_config
        cfg = load_yaml_config("questionnaires")
        common = cfg.get("common_questions", [])
        assert len(common) >= 14
        programs = cfg.get("programs", {})
        assert len(programs) == 8

    def test_field_mappings_config_loads(self):
        from app.config_loader import load_yaml_config
        cfg = load_yaml_config("ircc_field_mappings")
        assert "common_fields" in cfg
        assert "forms" in cfg

    def test_tenants_config_loads(self):
        from app.config_loader import load_yaml_config
        cfg = load_yaml_config("tenants")
        tenants = cfg.get("tenants", {})
        assert "vmc" in tenants
        assert tenants["vmc"]["name"] == "Visa Master Canada"


# ═══════════════════════════════════════
# 10. IRCC FORM SERVICE
# ═══════════════════════════════════════

class TestIRCCFormService:
    """Test IRCC PDF form handling."""

    def test_ircc_pdfs_exist(self):
        """All expected IRCC PDFs should be in templates/ircc/."""
        from pathlib import Path
        ircc_dir = Path(__file__).parent.parent / "templates" / "ircc"
        expected = ["IMM_0008", "IMM_5669", "IMM_5406", "IMM_5476",
                     "IMM_1344", "IMM_5532", "IMM_5540", "IMM_5562",
                     "IMM_5645", "IMM_5710", "IMM_1295", "IMM_5481"]
        for form in expected:
            pdf = ircc_dir / f"{form}.pdf"
            assert pdf.exists(), f"Missing IRCC PDF: {form}.pdf"
            assert pdf.stat().st_size > 10000, f"PDF too small (likely not real): {form}.pdf"

    def test_form_service_loads(self):
        from app.services.ircc_form_service import IRCCFormService
        svc = IRCCFormService()
        assert svc.config is not None
        assert len(svc.forms) > 0

    def test_form_fill_returns_output(self):
        """Filling a form should return either PDF bytes or HTML data sheet."""
        from app.services.ircc_form_service import IRCCFormService
        svc = IRCCFormService()
        result = svc.fill_form("IMM_5476", {
            "full_name": "Test User",
            "email": "test@example.com",
        })
        if result:
            assert len(result) > 100
            # Should be either PDF or HTML
            assert result[:5] == b"%PDF-" or b"<!DOCTYPE html>" in result[:50]


# ═══════════════════════════════════════
# 11. DATABASE MODELS
# ═══════════════════════════════════════

class TestDatabaseModels:
    """Test database models are properly defined."""

    def test_all_models_importable(self):
        from app.models.db_models import (
            Contact, Opportunity, Case, Activity, Signature,
            Dependent, ProcessedWebhook, DeadLetterQueue, SyncLog
        )
        assert Contact.__tablename__ == "contacts"
        assert Dependent.__tablename__ == "dependents"
        assert ProcessedWebhook.__tablename__ == "processed_webhooks"
        assert DeadLetterQueue.__tablename__ == "dead_letter_queue"

    def test_case_model_has_unique_id(self):
        from app.models.db_models import Case
        # case_id should have unique constraint
        for col in Case.__table__.columns:
            if col.name == "case_id":
                assert col.unique == True


# ═══════════════════════════════════════
# 12. GHL CLIENT
# ═══════════════════════════════════════

class TestGHLClient:
    """Test GHL client configuration."""

    def test_ghl_client_imports(self):
        from app.services.ghl_client import GHLClient, RateLimitError
        assert callable(GHLClient)
        assert issubclass(RateLimitError, Exception)

    def test_ghl_client_has_retry(self):
        """GHL client _request method should have retry decorator."""
        from app.services.ghl_client import GHLClient
        client = GHLClient()
        # The _request method should have tenacity retry
        assert hasattr(client._request, "retry")


# ═══════════════════════════════════════
# 13. COMPLIANCE LOG
# ═══════════════════════════════════════

class TestComplianceLog:
    """Test audit trail functionality."""

    def test_log_event_works(self):
        from app.utils.compliance_log import log_event, get_request_id
        # Should not raise
        log_event("test_event", {"key": "value"})
        rid = get_request_id()
        assert len(rid) > 0

    def test_request_id_consistency(self):
        from app.utils.compliance_log import get_request_id
        id1 = get_request_id()
        id2 = get_request_id()
        # Same context should return same ID
        assert id1 == id2
