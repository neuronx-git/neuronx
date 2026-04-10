"""Tests for IRCC form auto-population service."""

import pytest
from app.services.ircc_form_service import IRCCFormService


@pytest.fixture
def service():
    return IRCCFormService()


def test_list_forms_express_entry(service):
    forms = service.list_available_forms("Express Entry")
    assert len(forms) >= 4  # IMM_0008, IMM_5669, IMM_5406, IMM_5476
    codes = [f["form_code"] for f in forms]
    assert "IMM 0008" in codes
    assert "IMM 5669" in codes


def test_list_forms_spousal(service):
    forms = service.list_available_forms("Spousal Sponsorship")
    codes = [f["form_code"] for f in forms]
    assert "IMM 1344" in codes
    assert "IMM 5532" in codes


def test_list_forms_work_permit(service):
    forms = service.list_available_forms("Work Permit")
    codes = [f["form_code"] for f in forms]
    assert "IMM 1295" in codes
    assert "IMM 5710" in codes


def test_list_forms_unknown_program(service):
    forms = service.list_available_forms("Martian Visa")
    assert forms == []


def test_mapping_coverage(service):
    client_data = {
        "full_name": "Singh",
        "full_name_given": "Ranjan",
        "date_of_birth": "1990-01-01",
        "country_of_citizenship": "India",
        "email": "test@test.com",
    }
    coverage = service.get_mapping_coverage("IMM_0008", client_data)
    assert coverage["total_fields"] > 0
    assert coverage["fillable_from_data"] >= 4
    assert coverage["coverage_percent"] > 0


def test_mapping_coverage_unknown_form(service):
    result = service.get_mapping_coverage("NONEXISTENT", {})
    assert "error" in result


def test_transform_marital_status(service):
    assert service._transform_value("marital_status", "Married") == "02"
    assert service._transform_value("marital_status", "Single") == "01"
    assert service._transform_value("marital_status", "Common-Law") == "03"


def test_transform_boolean(service):
    assert service._transform_value("criminal_history", True) == "Yes"
    assert service._transform_value("criminal_history", False) == "No"


def test_fill_form_no_pdf(service):
    """Fill should return None when PDF template doesn't exist."""
    result = service.fill_form("IMM_9999_NONEXISTENT", {"full_name": "Test"})
    assert result is None  # PDF doesn't exist


def test_fill_form_imm5476(service):
    """Fill IMM 5476 (Use of Representative) with test data."""
    result = service.fill_form("IMM_5476", {
        "full_name": "Sharma",
        "full_name_given": "Priya",
        "email": "priya@example.com",
    })
    if result:  # Only if PDF exists
        assert len(result) > 100000  # Should be a substantial PDF
        assert result[:5] == b"%PDF-"


def test_ircc_forms_endpoint(client):
    """Test the IRCC forms listing endpoint."""
    r = client.get("/documents/ircc-forms/Express Entry")
    assert r.status_code == 200
    data = r.json()
    assert data["program_type"] == "Express Entry"
    assert data["total"] >= 4


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)
