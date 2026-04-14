"""
Integration Tests — Admin Router

Tests the /admin/reload-config endpoint.
Requires X-Admin-Key header matching ADMIN_API_KEY env var.
"""

import pytest
from unittest.mock import patch


@pytest.mark.integration
class TestReloadConfig:
    """Tests for POST /admin/reload-config."""

    def test_correct_key_returns_200(self, client):
        """POST /admin/reload-config with correct key returns 200."""
        response = client.post(
            "/admin/reload-config",
            headers={"X-Admin-Key": "neuronx-admin-dev"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert "reloaded" in body["message"].lower()

    def test_wrong_key_returns_401(self, client):
        """POST /admin/reload-config with wrong key returns 401."""
        response = client.post(
            "/admin/reload-config",
            headers={"X-Admin-Key": "wrong-key-abc"},
        )
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_missing_header_returns_422(self, client):
        """POST /admin/reload-config without X-Admin-Key header returns 422."""
        response = client.post("/admin/reload-config")
        assert response.status_code == 422

    def test_reload_calls_reload_all(self, client):
        """Successful reload calls config_loader.reload_all()."""
        with patch("app.config_loader.reload_all") as mock_reload:
            response = client.post(
                "/admin/reload-config",
                headers={"X-Admin-Key": "neuronx-admin-dev"},
            )
            assert response.status_code == 200
            mock_reload.assert_called_once()

    def test_empty_key_returns_401(self, client):
        """POST /admin/reload-config with empty key returns 401."""
        response = client.post(
            "/admin/reload-config",
            headers={"X-Admin-Key": ""},
        )
        assert response.status_code == 401
