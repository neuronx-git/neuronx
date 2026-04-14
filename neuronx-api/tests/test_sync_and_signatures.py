"""Tests for sync and signature endpoints (without database)."""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_sync_status_no_db(client):
    """Sync status should gracefully handle no database."""
    r = client.get("/sync/status")
    assert r.status_code == 200
    data = r.json()
    assert data["database"] in ("not configured", "not initialized")


def test_full_sync_no_db(client):
    """Full sync should return error when no database configured."""
    r = client.post("/sync/full")
    assert r.status_code == 200
    data = r.json()
    assert "error" in data or "database" in str(data)


def test_signature_send_no_documenso(client):
    """Signature send should return 503 when Documenso not configured."""
    with patch("app.routers.signatures.DocumensoClient") as MockDocumenso:
        mock = MagicMock()
        mock.is_configured.return_value = False
        MockDocumenso.return_value = mock
        r = client.post("/signatures/send", json={
            "contact_id": "test123",
            "retainer_amount": 3500,
        })
    assert r.status_code == 503
    assert "Documenso not configured" in r.json()["detail"]


def test_signature_status_no_documenso(client):
    """Signature status check should return 503 when not configured."""
    with patch("app.routers.signatures.DocumensoClient") as MockDocumenso:
        mock = MagicMock()
        mock.is_configured.return_value = False
        MockDocumenso.return_value = mock
        r = client.get("/signatures/status/doc123")
    assert r.status_code == 503


def test_signature_webhook_ignored(client):
    """Webhook with unknown event should be ignored gracefully."""
    r = client.post("/signatures/webhook", json={
        "event": "UNKNOWN_EVENT",
        "data": {},
    })
    assert r.status_code == 200
    assert r.json()["status"] == "ignored"


def test_health_shows_db_status(client):
    """Health endpoint should show database status."""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert "database" in data
    assert data["version"] == "0.4.0"
