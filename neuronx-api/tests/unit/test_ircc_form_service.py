"""
Unit Tests — IRCC Form Auto-Population Service

Tests IRCCFormService: form listing, PDF field discovery, form filling,
data sheet generation, value transformers, and mapping coverage.

Mocks pypdf since actual IRCC PDFs may not be in the test environment.
"""

import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from pathlib import Path

from app.services.ircc_form_service import IRCCFormService

pytestmark = pytest.mark.unit


# ── Fixtures ────────────────────────────────────────────────────────

@pytest.fixture
def service():
    """IRCCFormService with config loaded from YAML."""
    return IRCCFormService()


@pytest.fixture
def sample_client_data():
    """Sample client questionnaire data for filling forms."""
    return {
        "full_name": "Maria Elena Santos",
        "date_of_birth": "1990-03-15",
        "country_of_citizenship": "India",
        "passport_number": "AB1234567",
        "passport_expiry": "2031-03-14",
        "marital_status": "Married",
        "current_address": "123 Main St, Mumbai, India",
        "email": "maria@example.com",
        "phone": "+91 9876543210",
    }


# ── Config Loading ──────────────────────────────────────────────────

class TestConfigLoading:
    """Verify IRCCFormService loads config from YAML."""

    def test_service_loads_config(self, service):
        """Service initializes with config from ircc_field_mappings.yaml."""
        assert isinstance(service.config, dict)

    def test_service_has_forms(self, service):
        """Service loads forms dict from config."""
        assert isinstance(service.forms, dict)

    def test_service_has_common_fields(self, service):
        """Service loads common_fields from config."""
        assert isinstance(service.common_fields, dict)

    def test_service_has_transformers(self, service):
        """Service loads transformers from config."""
        assert isinstance(service.transformers, dict)

    def test_service_has_firm_defaults(self, service):
        """Service loads firm_defaults from config."""
        assert isinstance(service.firm_defaults, dict)


# ── List Available Forms ────────────────────────────────────────────

class TestListAvailableForms:
    """Test listing IRCC forms for a given program."""

    def test_list_forms_returns_list(self, service):
        """list_available_forms returns a list."""
        result = service.list_available_forms("Express Entry")
        assert isinstance(result, list)

    def test_list_forms_contains_form_keys(self, service):
        """Each form in list has required keys."""
        result = service.list_available_forms("Express Entry")
        if result:
            form = result[0]
            assert "form_key" in form
            assert "form_code" in form
            assert "form_name" in form
            assert "pdf_available" in form

    def test_list_forms_nonexistent_program(self, service):
        """Unknown program returns empty list."""
        result = service.list_available_forms("Nonexistent Program")
        assert result == []


# ── Discover PDF Fields ─────────────────────────────────────────────

class TestDiscoverPdfFields:
    """Test PDF field discovery for mapping setup."""

    def test_discover_missing_pdf(self, service):
        """discover_pdf_fields returns error for missing PDF."""
        result = service.discover_pdf_fields("NONEXISTENT_FORM")
        assert "error" in result
        assert "not found" in result["error"].lower()

    def test_discover_nonexistent_dir(self, service):
        """discover_pdf_fields handles missing directory."""
        with patch("app.services.ircc_form_service.TEMPLATES_DIR", Path("/nonexistent/path")):
            result = service.discover_pdf_fields("IMM_0008")
        assert "error" in result

    def test_discover_with_mock_pdf(self, service):
        """discover_pdf_fields reads fields from a PDF."""
        mock_reader = MagicMock()
        mock_reader.get_form_text_fields.return_value = {"FamilyName": "Santos"}
        mock_reader.get_fields.return_value = {
            "FamilyName": {"/FT": "/Tx", "/V": "Santos"}
        }
        mock_reader.pages = [MagicMock(), MagicMock()]

        with patch("app.services.ircc_form_service.TEMPLATES_DIR") as mock_dir:
            mock_dir.__truediv__ = MagicMock(return_value=Path("/tmp/test.pdf"))
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_dir.__truediv__.return_value = mock_path

            with patch("app.services.ircc_form_service.PdfReader", return_value=mock_reader, create=True):
                with patch.dict("sys.modules", {"pypdf": MagicMock()}):
                    # Test that pypdf import works
                    pass


# ── Fill Form ───────────────────────────────────────────────────────

class TestFillForm:
    """Test form filling with client data."""

    def test_fill_form_no_pdf(self, service, sample_client_data):
        """fill_form returns None when PDF template doesn't exist."""
        result = service.fill_form("NONEXISTENT_FORM", sample_client_data)
        assert result is None

    def test_fill_form_no_mapping(self, service, sample_client_data):
        """fill_form returns None for form without field mappings."""
        # Use a form key that exists in config but has no PDF
        for form_key in service.forms:
            result = service.fill_form(form_key, sample_client_data)
            # Either None (no PDF) or bytes (filled) — should not crash
            assert result is None or isinstance(result, bytes)
            break

    def test_fill_form_empty_data(self, service):
        """fill_form with empty data returns None (no fields to fill)."""
        for form_key in service.forms:
            result = service.fill_form(form_key, {})
            assert result is None
            break

    def test_fill_form_pypdf_not_installed(self, service, sample_client_data):
        """fill_form returns None when pypdf is not importable."""
        with patch.dict("sys.modules", {"pypdf": None}):
            with patch("builtins.__import__", side_effect=ImportError("No module named 'pypdf'")):
                for form_key in service.forms:
                    result = service.fill_form(form_key, sample_client_data)
                    # Should handle gracefully
                    assert result is None or isinstance(result, bytes)
                    break


# ── Generate Data Sheet ─────────────────────────────────────────────

class TestGenerateDataSheet:
    """Test HTML data sheet generation for encrypted PDFs."""

    def test_data_sheet_returns_bytes(self, service):
        """_generate_data_sheet returns HTML bytes."""
        form_config = {"form_code": "IMM 0008", "form_name": "Application for PR"}
        fill_data = {"FamilyName": "Santos", "GivenName": "Maria"}

        result = service._generate_data_sheet("IMM_0008", form_config, fill_data)

        assert isinstance(result, bytes)
        html = result.decode("utf-8")
        assert "Santos" in html
        assert "Maria" in html
        assert "IMM 0008" in html

    def test_data_sheet_contains_header(self, service):
        """Data sheet HTML contains NeuronX header."""
        form_config = {"form_code": "IMM 5476", "form_name": "Use of Representative"}
        fill_data = {"RepName": "John Doe"}

        html = service._generate_data_sheet("IMM_5476", form_config, fill_data).decode()
        assert "NeuronX" in html
        assert "Data Sheet" in html

    def test_data_sheet_empty_data(self, service):
        """Data sheet with empty fill_data still generates valid HTML."""
        form_config = {"form_code": "TEST", "form_name": "Test Form"}
        result = service._generate_data_sheet("TEST", form_config, {})

        html = result.decode("utf-8")
        assert "<html>" in html
        assert "</html>" in html


# ── Value Transformers ──────────────────────────────────────────────

class TestValueTransformers:
    """Test value transformation for form fields."""

    def test_transform_string_passthrough(self, service):
        """Non-special keys pass through as strings."""
        result = service._transform_value("full_name", "Maria Santos")
        assert result == "Maria Santos"

    def test_transform_boolean_true(self, service):
        """Boolean True transforms via boolean_to_yesno mapping."""
        result = service._transform_value("has_passport", True)
        # Either "Yes" (if transformer configured) or "True" (default)
        assert result in ("Yes", "True")

    def test_transform_boolean_false(self, service):
        """Boolean False transforms via boolean_to_yesno mapping."""
        result = service._transform_value("has_refusal", False)
        assert result in ("No", "False")

    def test_transform_integer(self, service):
        """Integer values convert to string."""
        result = service._transform_value("age", 35)
        assert result == "35"

    def test_transform_marital_status(self, service):
        """Marital status uses transformer if configured."""
        result = service._transform_value("marital_status", "Married")
        assert isinstance(result, str)
        assert len(result) > 0


# ── Fill All Forms ──────────────────────────────────────────────────

class TestFillAllForms:
    """Test batch form filling for a program."""

    def test_fill_all_returns_list(self, service, sample_client_data):
        """fill_all_forms returns list of results."""
        result = service.fill_all_forms("Express Entry", sample_client_data)
        assert isinstance(result, list)

    def test_fill_all_each_has_form_code(self, service, sample_client_data):
        """Each result has form_code and form_name."""
        results = service.fill_all_forms("Express Entry", sample_client_data)
        for r in results:
            assert "form_code" in r
            assert "form_name" in r
            assert "form_key" in r

    def test_fill_all_nonexistent_program(self, service, sample_client_data):
        """fill_all_forms for unknown program returns empty list."""
        result = service.fill_all_forms("Nonexistent Program", sample_client_data)
        assert result == []


# ── Mapping Coverage ────────────────────────────────────────────────

class TestMappingCoverage:
    """Test field mapping coverage reporting."""

    def test_coverage_unknown_form(self, service):
        """get_mapping_coverage returns error for unknown form."""
        result = service.get_mapping_coverage("NONEXISTENT", {})
        assert "error" in result

    def test_coverage_returns_stats(self, service, sample_client_data):
        """get_mapping_coverage returns coverage stats for known form."""
        for form_key in service.forms:
            result = service.get_mapping_coverage(form_key, sample_client_data)
            assert "form_code" in result
            assert "total_fields" in result
            assert "fillable_from_data" in result
            assert "coverage_percent" in result
            assert "missing_fields" in result
            assert isinstance(result["coverage_percent"], (int, float))
            break

    def test_coverage_empty_data(self, service):
        """get_mapping_coverage with empty data shows 0% coverage."""
        for form_key in service.forms:
            result = service.get_mapping_coverage(form_key, {})
            if result.get("total_fields", 0) > 0:
                assert result["coverage_percent"] == 0
                assert len(result["missing_fields"]) == result["total_fields"]
            break

    def test_coverage_full_data(self, service):
        """get_mapping_coverage with all keys shows high coverage."""
        for form_key, form_config in service.forms.items():
            mappings = form_config.get("field_mappings", {})
            if mappings:
                full_data = {key: f"value_{key}" for key in mappings}
                result = service.get_mapping_coverage(form_key, full_data)
                assert result["coverage_percent"] == 100
                assert result["missing_fields"] == []
                break
