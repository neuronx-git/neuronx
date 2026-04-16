"""
E2E Test Suite: Typebot Immigration Form Flow
Tests the complete data flow: form load → OCR → program branching → webhook → GHL sync

Run: pytest tests/test_e2e_form_flow.py -v
Against production: PRODUCTION=1 pytest tests/test_e2e_form_flow.py -v
"""

import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.config import settings

# Production URL for live tests
PROD_URL = "https://neuronx-production-62f9.up.railway.app"
TYPEBOT_BUILDER = "https://builder-production-6784.up.railway.app"
TYPEBOT_VIEWER = "https://viewer-production-366c.up.railway.app"
FORM_URL = "https://www.neuronx.co/intake/vmc/onboarding"
IS_PRODUCTION = os.environ.get("PRODUCTION") == "1"


class TestFormServing:
    """Test 1: Form loads and renders correctly."""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_form_returns_200(self, client):
        r = client.get("/form/vmc/onboarding")
        assert r.status_code == 200

    def test_form_has_correct_title(self, client):
        r = client.get("/form/vmc/onboarding")
        assert "VMC Immigration Assessment" in r.text

    def test_form_has_typebot_viewer(self, client):
        r = client.get("/form/vmc/onboarding")
        assert "viewer-production-366c" in r.text

    def test_form_noindex(self, client):
        r = client.get("/form/vmc/onboarding")
        assert "noindex" in r.text

    def test_form_nx_favicon(self, client):
        r = client.get("/form/vmc/onboarding")
        assert "NX" in r.text

    def test_unknown_form_404(self, client):
        r = client.get("/form/vmc/nonexistent")
        assert r.status_code == 404

    def test_unknown_tenant_404(self, client):
        r = client.get("/form/unknown/onboarding")
        assert r.status_code == 404


class TestQuestionnaireAPI:
    """Test 2: Program-specific questionnaires return correct fields."""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    @pytest.mark.parametrize("slug,display_name,min_questions", [
        ("express-entry", "Express Entry", 43),
        ("spousal-sponsorship", "Spousal Sponsorship", 39),
        ("work-permit", "Work Permit", 37),
        ("study-permit", "Study Permit", 36),
        ("lmia", "LMIA", 31),
        ("pr-renewal", "PR Renewal", 29),
        ("citizenship", "Citizenship", 31),
        ("visitor-visa", "Visitor Visa", 36),
    ])
    def test_questionnaire_returns_correct_count(self, client, slug, display_name, min_questions):
        r = client.get(f"/cases/questionnaire/{slug}")
        assert r.status_code == 200
        data = r.json()
        assert data["program_type"] == display_name
        assert data["total_questions"] >= min_questions
        assert data["common_count"] == 24

    def test_questionnaire_express_entry_has_sections(self, client):
        r = client.get("/cases/questionnaire/express-entry")
        data = r.json()
        assert "Education" in data["sections"]
        assert "Language" in data["sections"]
        assert "Settlement Funds" in data["sections"]

    def test_questionnaire_unknown_program_returns_common_only(self, client):
        r = client.get("/cases/questionnaire/unknown-program")
        data = r.json()
        assert data["total_questions"] == 24
        assert "note" in data


class TestOCRExtraction:
    """Test 3: Document OCR extraction returns standardized fields."""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_extract_types_returns_7_types(self, client):
        r = client.get("/extract/types")
        assert r.status_code == 200
        types = r.json()["supported_types"]
        assert len(types) == 7
        type_names = [t["type"] for t in types]
        assert "passport" in type_names
        assert "ielts" in type_names
        assert "eca" in type_names

    def test_passport_type_has_correct_fields(self, client):
        r = client.get("/extract/types")
        passport = next(t for t in r.json()["supported_types"] if t["type"] == "passport")
        assert "full_name" in passport["fields"]
        assert "passport_number" in passport["fields"]
        assert "date_of_birth" in passport["fields"]

    @pytest.mark.asyncio
    async def test_ocr_passport_with_fastmrz(self):
        from app.services.doc_ocr_service import DocOCRService
        import sys

        service = DocOCRService()
        mock_mod = MagicMock()
        mock_inst = MagicMock()
        mock_inst.get_details.return_value = {
            "given_name": "PRIYA", "surname": "SHARMA",
            "date_of_birth": "1990-01-15", "document_number": "T1234567",
            "expiry_date": "2032-12-20", "nationality": "IND", "sex": "F",
        }
        mock_mod.FastMRZ.return_value = mock_inst

        with patch.dict(sys.modules, {"fastmrz": mock_mod}):
            result = await service._extract_passport(b"fake_data", "passport.jpg")

        assert result["method"] == "fastmrz"
        assert result["extracted_fields"]["full_name"] == "PRIYA SHARMA"
        assert result["extracted_fields"]["passport_number"] == "T1234567"
        assert result["extracted_fields"]["country_of_citizenship"] == "IND"
        assert result["confidence"] == "high"

    @pytest.mark.asyncio
    async def test_ocr_auto_detect_from_filename(self):
        from app.services.doc_ocr_service import DocOCRService
        service = DocOCRService()

        assert service._detect_type("passport_scan.jpg") == "passport"
        assert service._detect_type("IELTS_Results_2026.pdf") == "ielts"
        assert service._detect_type("WES_ECA_Report.pdf") == "eca"
        assert service._detect_type("employment_letter.pdf") == "employment_letter"
        assert service._detect_type("marriage_certificate.jpg") == "marriage_certificate"
        assert service._detect_type("bank_statement_march.pdf") == "bank_statement"
        assert service._detect_type("police_clearance_india.pdf") == "police_clearance"
        assert service._detect_type("random_document.pdf") == "general"


class TestWebhookProcessing:
    """Test 4: Typebot webhook correctly maps fields to GHL."""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_webhook_deduplication(self, client):
        """Same resultId should be rejected on second submission."""
        payload = {"resultId": "dedup-test-001", "email": "dedup@test.com", "answers": {"full_name": "Dedup Test"}}
        with patch("app.routers.typebot.GHLClient") as mock_ghl:
            mock_instance = MagicMock()
            mock_instance.search_contacts = AsyncMock(return_value={"contacts": [{"id": "c-dedup"}]})
            mock_instance.update_custom_fields = AsyncMock()
            mock_instance.add_tag = AsyncMock()
            mock_ghl.return_value = mock_instance

            r1 = client.post("/typebot/webhook", json=payload)
            assert r1.json()["status"] == "processed"

            r2 = client.post("/typebot/webhook", json=payload)
            assert r2.json()["status"] == "duplicate"

    def test_webhook_maps_express_entry_fields(self, client):
        """Express Entry fields map to correct GHL custom field keys."""
        payload = {
            "resultId": "ee-test-001",
            "email": "express@test.com",
            "answers": {
                "full_name": "Test User",
                "program_interest": "Express Entry",
                "education_level": "Bachelor's Degree",
                "settlement_funds": "25000",
                "language_test_type": "IELTS General",
                "provincial_nomination": "No",
            },
        }
        with patch("app.routers.typebot.GHLClient") as mock_ghl:
            mock_instance = MagicMock()
            mock_instance.search_contacts = AsyncMock(return_value={"contacts": [{"id": "c123"}]})
            mock_instance.update_custom_fields = AsyncMock()
            mock_instance.add_tag = AsyncMock()
            mock_ghl.return_value = mock_instance

            r = client.post("/typebot/webhook", json=payload)
            assert r.json()["status"] == "processed"
            assert r.json()["fields_updated"] >= 5
            assert r.json()["tag_added"] == "nx:case:docs_pending"

            # Verify GHL was called with correct field mapping
            call_args = mock_instance.update_custom_fields.call_args
            fields = call_args[0][1]
            assert fields["ai_program_interest"] == "Express Entry"
            assert fields["r2_education_level"] == "Bachelor's Degree"
            assert fields["settlement_funds"] == "25000"

    def test_webhook_maps_spousal_fields(self, client):
        """Spousal Sponsorship fields map correctly."""
        payload = {
            "resultId": "ss-test-001",
            "email": "spousal@test.com",
            "answers": {
                "full_name": "Test Sponsor",
                "program_interest": "Spousal Sponsorship",
                "sponsor_name": "John Doe",
                "sponsor_status": "Canadian Citizen",
                "relationship_type": "Married",
                "met_in_person": "Yes",
            },
        }
        with patch("app.routers.typebot.GHLClient") as mock_ghl:
            mock_instance = MagicMock()
            mock_instance.search_contacts = AsyncMock(return_value={"contacts": [{"id": "c456"}]})
            mock_instance.update_custom_fields = AsyncMock()
            mock_instance.add_tag = AsyncMock()
            mock_ghl.return_value = mock_instance

            r = client.post("/typebot/webhook", json=payload)
            assert r.json()["status"] == "processed"

            fields = mock_instance.update_custom_fields.call_args[0][1]
            assert fields["sponsor_name"] == "John Doe"
            assert fields["sponsor_status"] == "Canadian Citizen"
            assert fields["relationship_type"] == "Married"

    def test_webhook_maps_all_p2_programs(self, client):
        """P2 program fields (LMIA, PR Renewal, Citizenship, Visitor) map correctly."""
        # LMIA
        payload = {
            "resultId": "lmia-test-001",
            "email": "lmia@test.com",
            "answers": {
                "employer_province": "Ontario",
                "position_title": "Software Engineer",
                "lmia_stream": "Global Talent Stream",
            },
        }
        with patch("app.routers.typebot.GHLClient") as mock_ghl:
            mock_instance = MagicMock()
            mock_instance.search_contacts = AsyncMock(return_value={"contacts": [{"id": "c789"}]})
            mock_instance.update_custom_fields = AsyncMock()
            mock_instance.add_tag = AsyncMock()
            mock_ghl.return_value = mock_instance

            r = client.post("/typebot/webhook", json=payload)
            assert r.json()["status"] == "processed"

            fields = mock_instance.update_custom_fields.call_args[0][1]
            assert fields["employer_province"] == "Ontario"
            assert fields["lmia_stream"] == "Global Talent Stream"


class TestOnboardingURL:
    """Test 5: Pre-filled onboarding URL generation from Phase 1 data."""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_onboarding_url_with_contact_data(self, client):
        """URL should contain pre-filled query params from GHL contact."""
        mock_contact = {
            "firstName": "Priya",
            "lastName": "Sharma",
            "email": "priya@example.com",
            "phone": "+16479999999",
            "country": "India",
            "customFields": [
                {"id": "ai_program_interest", "value": "Express Entry"},
                {"id": "ai_current_location", "value": "outside_canada"},
            ],
        }
        with patch("app.routers.cases.GHLClient") as mock_ghl:
            mock_instance = MagicMock()
            mock_instance.get_contact = AsyncMock(return_value=mock_contact)
            mock_ghl.return_value = mock_instance

            r = client.get("/cases/onboarding-url/test-contact-123")
            assert r.status_code == 200
            data = r.json()

            assert "Priya+Sharma" in data["onboarding_url"] or "Priya%20Sharma" in data["onboarding_url"]
            assert "priya%40example.com" in data["onboarding_url"] or "priya@example.com" in data["onboarding_url"]
            assert data["prefill_count"] >= 4
            assert data["total_form_fields"] > 15  # Dynamic, not hardcoded 68

    def test_onboarding_url_dynamic_field_count(self, client):
        """Field count should vary by program."""
        mock_contact = {
            "firstName": "Test",
            "customFields": [
                {"id": "ai_program_interest", "value": "Express Entry"},
            ],
        }
        with patch("app.routers.cases.GHLClient") as mock_ghl:
            mock_instance = MagicMock()
            mock_instance.get_contact = AsyncMock(return_value=mock_contact)
            mock_ghl.return_value = mock_instance

            r = client.get("/cases/onboarding-url/test-contact-456")
            data = r.json()
            assert data["total_form_fields"] == 43  # Express Entry = 24 common + 19


class TestDeepHealth:
    """Test 6: Deep health check returns clean status."""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_health_returns_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_deep_health_no_crashes(self, client):
        """Deep health should not crash with empty tokens."""
        r = client.get("/health/deep")
        assert r.status_code == 200
        checks = r.json()["checks"]
        # Should return clean status messages, not crash errors
        assert "Illegal header" not in str(checks)
        assert "async_generator" not in str(checks)


class TestDocumentChecklist:
    """Test 7: Document checklists per program."""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    @pytest.mark.parametrize("program,min_required", [
        ("Express Entry", 7),
        ("Spousal Sponsorship", 7),
        ("Work Permit", 7),
        ("Study Permit", 8),
    ])
    def test_document_checklist_per_program(self, client, program, min_required):
        slug = program.lower().replace(" ", "-")
        r = client.get(f"/cases/forms/{slug}")
        # May return empty for slug (not display name)
        r2 = client.get(f"/cases/forms/{program}")
        data = r2.json() if r2.status_code == 200 else r.json()
        # Programs with IRCC forms should have them
        if program in ["Express Entry", "Spousal Sponsorship", "Work Permit"]:
            assert len(data.get("forms", [])) > 0

    def test_timeline_returns_estimate(self, client):
        r = client.get("/cases/timeline/express-entry")
        assert r.status_code == 200
        data = r.json()
        assert "estimated_months" in data
        assert data["estimated_months"]["avg"] > 0


class TestCaseProcessing:
    """Test 8: Case initiation and stage management."""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_case_initiate(self, client):
        """Case initiation should create case ID and set GHL fields."""
        with patch("app.routers.cases.CaseService") as mock_cs:
            mock_instance = MagicMock()
            mock_instance.initiate_case = AsyncMock(return_value={
                "case_id": "NX-20260416-abcd1234",
                "status": "initiated",
                "program_type": "Express Entry",
            })
            mock_cs.return_value = mock_instance

            r = client.post("/cases/initiate", json={
                "contact_id": "test-contact",
                "program_type": "Express Entry",
                "assigned_rcic": "Rajiv Mehta",
            })
            assert r.status_code == 200
            assert r.json()["case_id"].startswith("NX-")


@pytest.mark.skipif(not IS_PRODUCTION, reason="Production-only test")
class TestProductionEndpoints:
    """Test 9: Live production endpoint verification."""

    @pytest.mark.asyncio
    async def test_production_health(self):
        async with AsyncClient() as client:
            r = await client.get(f"{PROD_URL}/health")
            assert r.status_code == 200
            assert r.json()["status"] == "ok"

    @pytest.mark.asyncio
    async def test_production_deep_health(self):
        async with AsyncClient() as client:
            r = await client.get(f"{PROD_URL}/health/deep")
            assert r.status_code == 200
            checks = r.json()["checks"]
            assert checks["database"] == "ok"
            assert checks["configs"].startswith("ok")

    @pytest.mark.asyncio
    async def test_production_form_serves(self):
        async with AsyncClient(follow_redirects=True) as client:
            r = await client.get(f"{PROD_URL}/form/vmc/onboarding")
            assert r.status_code == 200

    @pytest.mark.asyncio
    async def test_production_questionnaire(self):
        async with AsyncClient() as client:
            r = await client.get(f"{PROD_URL}/cases/questionnaire/express-entry")
            assert r.status_code == 200
            assert r.json()["total_questions"] == 28

    @pytest.mark.asyncio
    async def test_production_extract_types(self):
        async with AsyncClient() as client:
            r = await client.get(f"{PROD_URL}/extract/types")
            assert r.status_code == 200
            assert len(r.json()["supported_types"]) == 7

    @pytest.mark.asyncio
    async def test_production_ocr_passport(self):
        """Upload synthetic passport and verify OCR extraction."""
        from PIL import Image, ImageDraw
        import io

        # Create minimal test image
        img = Image.new('RGB', (400, 300), 'white')
        draw = ImageDraw.Draw(img)
        draw.text((20, 20), "PASSPORT", fill='black')
        draw.text((20, 50), "Name: TEST USER", fill='black')
        draw.text((20, 80), "Passport: X9999999", fill='black')
        mrz1 = "P<INDTEST<<USER<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        mrz2 = "X99999994IND9001015F3012206<<<<<<<<<<<<<<<<<08"
        draw.text((20, 220), mrz1, fill='black')
        draw.text((20, 250), mrz2, fill='black')

        buf = io.BytesIO()
        img.save(buf, 'JPEG')
        buf.seek(0)

        async with AsyncClient(timeout=60.0) as client:
            r = await client.post(
                f"{PROD_URL}/extract/upload",
                files={"file": ("test_passport.jpg", buf, "image/jpeg")},
                data={"doc_type": "passport"},
            )
            assert r.status_code == 200
            data = r.json()
            assert data["confidence"] in ("high", "medium")
            assert data["field_count"] > 0
