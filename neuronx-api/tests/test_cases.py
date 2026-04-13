"""Tests for case processing endpoints."""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_ircc_forms_express_entry(client):
    r = client.get("/cases/forms/Express Entry")
    assert r.status_code == 200
    data = r.json()
    assert data["program_type"] == "Express Entry"
    assert data["total_required"] >= 5
    assert any(f["code"] == "IMM 0008" for f in data["forms"])


def test_get_ircc_forms_spousal(client):
    r = client.get("/cases/forms/Spousal Sponsorship")
    assert r.status_code == 200
    data = r.json()
    assert data["total_required"] >= 7
    assert any(f["code"] == "IMM 1344" for f in data["forms"])


def test_get_ircc_forms_work_permit(client):
    r = client.get("/cases/forms/Work Permit")
    assert r.status_code == 200
    assert r.json()["total_required"] >= 4


def test_get_ircc_forms_unknown(client):
    r = client.get("/cases/forms/Martian Visa")
    assert r.status_code == 200
    assert r.json()["forms"] == []


def test_processing_timeline(client):
    r = client.get("/cases/timeline/Express Entry")
    assert r.status_code == 200
    data = r.json()
    assert data["estimated_months"]["avg"] == 6
    assert "disclaimer" in data


def test_processing_timeline_spousal(client):
    r = client.get("/cases/timeline/Spousal Sponsorship")
    assert r.status_code == 200
    assert r.json()["estimated_months"]["avg"] == 18  # Updated April 2026: 15mo outland, 24mo inland, avg 18


def test_invalid_decision(client):
    r = client.post("/cases/decision", json={
        "contact_id": "test",
        "decision": "Maybe",
    })
    assert r.status_code == 400


def test_questionnaire_express_entry(client):
    r = client.get("/cases/questionnaire/Express Entry")
    assert r.status_code == 200
    data = r.json()
    assert data["program_type"] == "Express Entry"
    assert data["common_count"] > 0
    assert data["program_specific_count"] > 0
    assert data["total_questions"] == data["common_count"] + data["program_specific_count"]
    # Must have program-specific sections
    assert "Education" in data["sections"]
    assert "Language" in data["sections"]


def test_questionnaire_spousal(client):
    r = client.get("/cases/questionnaire/Spousal Sponsorship")
    assert r.status_code == 200
    data = r.json()
    assert "Sponsor Information" in data["sections"]
    assert "Relationship" in data["sections"]
    assert data["program_specific_count"] > 0


def test_questionnaire_unknown_program(client):
    r = client.get("/cases/questionnaire/Martian Visa")
    assert r.status_code == 200
    data = r.json()
    assert data["total_questions"] > 0  # Still returns common questions
    assert "note" in data  # Has a note about using common questions only


def test_questionnaire_has_conditional_fields(client):
    r = client.get("/cases/questionnaire/Express Entry")
    data = r.json()
    # ECA question should have show_if conditional
    eca_q = next((q for q in data["questions"] if q.get("key") == "eca_organization"), None)
    assert eca_q is not None
    assert "show_if" in eca_q
