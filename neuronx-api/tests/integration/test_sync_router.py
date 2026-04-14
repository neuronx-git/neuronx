"""
Integration Tests — Sync Router

Tests POST /sync/full and GET /sync/status.
Mocks database and GHL to test routing logic.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock

pytestmark = pytest.mark.integration


class TestSyncStatus:
    """Tests for GET /sync/status."""

    def test_status_no_db(self, client):
        """Returns 'not configured' when no database session factory."""
        # The sync router imports async_session_factory at call time
        with patch("app.database.async_session_factory", None):
            resp = client.get("/sync/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["database"] in ("not configured", "not initialized")

    def test_status_endpoint_returns_200(self, client):
        """Sync status endpoint is reachable and returns 200."""
        resp = client.get("/sync/status")
        assert resp.status_code == 200


class TestFullSync:
    """Tests for POST /sync/full."""

    def test_full_sync_no_db(self, client):
        """Full sync returns error when no database."""
        with patch("app.database.async_session_factory", None):
            resp = client.post("/sync/full")
        assert resp.status_code == 200
        data = resp.json()
        assert "error" in data or "database" in str(data).lower()

    def test_full_sync_endpoint_reachable(self, client):
        """Full sync endpoint is reachable."""
        resp = client.post("/sync/full")
        assert resp.status_code == 200

    def test_full_sync_mocked_service(self, client, patch_ghl):
        """Full sync with mocked sync service returns results."""
        mock_service = AsyncMock()
        mock_service.full_sync.return_value = {
            "contacts_synced": 25,
            "opportunities_synced": 10,
            "status": "completed",
        }

        # Need to mock both the session factory check AND the service
        mock_sf = MagicMock()
        with patch("app.database.async_session_factory", mock_sf):
            with patch("app.routers.sync.SyncService", return_value=mock_service):
                resp = client.post("/sync/full")

        assert resp.status_code == 200
