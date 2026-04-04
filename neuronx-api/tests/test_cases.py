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
    assert r.json()["estimated_months"]["avg"] == 15


def test_invalid_decision(client):
    r = client.post("/cases/decision", json={
        "contact_id": "test",
        "decision": "Maybe",
    })
    assert r.status_code == 400
