"""
Tests for webhook endpoints.
Uses FastAPI TestClient — no real GHL/VAPI calls.
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ghl_webhook_contact_created(client):
    r = client.post("/webhooks/ghl", json={
        "type": "ContactCreated",
        "contactId": "test-contact-123",
    })
    assert r.status_code == 200
    assert r.json()["action"] == "contact_logged"


def test_ghl_webhook_appointment_booked(client):
    r = client.post("/webhooks/ghl", json={
        "type": "AppointmentBooked",
        "contactId": "test-contact-123",
        "appointmentId": "appt-456",
    })
    assert r.status_code == 200
    assert r.json()["action"] == "appointment_logged"


def test_ghl_webhook_unknown_type(client):
    r = client.post("/webhooks/ghl", json={
        "type": "SomethingElse",
        "contactId": "test-contact-123",
    })
    assert r.status_code == 200
    assert r.json()["action"] == "no_handler"


def test_vapi_status_update(client):
    r = client.post("/webhooks/voice", json={
        "message": {
            "type": "status-update",
            "status": "in-progress",
            "call": {"id": "call-789"},
        }
    })
    assert r.status_code == 200
    assert r.json()["action"] == "status_logged"


def test_vapi_function_call_readiness(client):
    r = client.post("/webhooks/voice", json={
        "message": {
            "type": "function-call",
            "functionCall": {
                "name": "collect_readiness_data",
                "parameters": {
                    "program_interest": "Express Entry",
                    "current_location": "In Canada",
                },
            },
        }
    })
    assert r.status_code == 200
    assert "result" in r.json()


def test_vapi_function_call_unknown(client):
    r = client.post("/webhooks/voice", json={
        "message": {
            "type": "function-call",
            "functionCall": {
                "name": "unknown_function",
                "parameters": {},
            },
        }
    })
    assert r.status_code == 200
    assert "result" in r.json()


@patch("app.routers.webhooks.GHLClient")
def test_vapi_end_of_call_no_contact(mock_ghl_class, client):
    """End-of-call without ghl_contact_id returns warning."""
    r = client.post("/webhooks/voice", json={
        "message": {
            "type": "end-of-call-report",
            "call": {"id": "call-999", "metadata": {}},
            "transcript": "Hello, thanks for calling.",
            "analysis": {
                "summary": "Test call",
                "structuredData": {},
            },
        }
    })
    assert r.status_code == 200
    assert r.json()["status"] == "warning"
    assert r.json()["message"] == "no_contact_id"


def test_score_lead_endpoint(client):
    """POST /score/lead returns valid scoring result."""
    r = client.post("/score/lead", json={
        "contact_id": "test-e2e-001",
        "r1_program_interest": "Express Entry",
        "r2_current_location": "In Canada",
        "r3_timeline_urgency": "Urgent",
        "r4_prior_applications": "None",
        "r5_budget_awareness": "Aware",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["contact_id"] == "test-e2e-001"
    assert data["score"] >= 70
    assert "nx:score:high" in data["ghl_tags_to_add"]


def test_score_form_endpoint(client):
    """POST /score/form returns preliminary form-based score."""
    r = client.post("/score/form", json={
        "contact_id": "test-form-001",
        "program_interest": "Express Entry",
        "current_location": "In Canada",
        "timeline": "Urgent",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["contact_id"] == "test-form-001"
    assert data["score_source"] == "form"
    assert data["preliminary_score"] <= 48  # Capped at form max
    assert data["dimensions_captured"] == 3
    assert data["can_upgrade"] is True
    assert "nx:form_scored" in data["ghl_tags_to_add"]
    assert "nx:form_qualified" in data["ghl_tags_to_add"]


def test_score_form_partial(client):
    """POST /score/form with 1 dimension — still works."""
    r = client.post("/score/form", json={
        "contact_id": "test-form-002",
        "program_interest": "Study Permit",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["dimensions_captured"] == 1
    assert data["preliminary_score"] > 0
    assert "nx:form_scored" in data["ghl_tags_to_add"]


def test_score_form_empty(client):
    """POST /score/form with no dimensions — score 0."""
    r = client.post("/score/form", json={
        "contact_id": "test-form-003",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["preliminary_score"] == 0
    assert data["dimensions_captured"] == 0
