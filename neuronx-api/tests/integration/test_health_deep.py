"""
Integration Tests — Deep Health Endpoint

Tests GET /health/deep which probes all external dependencies.
All external calls are mocked for test isolation.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import httpx

pytestmark = pytest.mark.integration


def _make_httpx_mock(status_code=200):
    """Create a mock httpx.AsyncClient context manager."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_client = AsyncMock()
    mock_client.get.return_value = mock_resp
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    return mock_client


class TestDeepHealth:
    """Tests for GET /health/deep."""

    def test_deep_health_returns_structure(self, client):
        """Deep health returns status, service, version, and checks dict."""
        with patch("httpx.AsyncClient", return_value=_make_httpx_mock()):
            resp = client.get("/health/deep")

        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data
        assert "checks" in data
        assert "service" in data
        assert data["service"] == "neuronx-api"
        assert data["version"] == "0.5.0"

    def test_deep_health_checks_keys(self, client):
        """Deep health checks include all expected dependency probes."""
        with patch("httpx.AsyncClient", return_value=_make_httpx_mock()):
            resp = client.get("/health/deep")

        checks = resp.json()["checks"]
        assert "database" in checks
        assert "ghl_api" in checks
        assert "configs" in checks

    def test_deep_health_configs_ok(self, client):
        """Deep health reports configs as loaded successfully."""
        with patch("httpx.AsyncClient", return_value=_make_httpx_mock()):
            resp = client.get("/health/deep")

        checks = resp.json()["checks"]
        assert "ok" in checks["configs"]

    def test_deep_health_ghl_reachable(self, client):
        """Deep health reports GHL as reachable when API returns 200."""
        with patch("httpx.AsyncClient", return_value=_make_httpx_mock(200)):
            resp = client.get("/health/deep")

        checks = resp.json()["checks"]
        assert checks["ghl_api"] == "ok"

    def test_deep_health_ghl_unreachable(self, client):
        """Deep health reports GHL as unreachable on connection error."""
        mock_client = AsyncMock()
        mock_client.get.side_effect = httpx.ConnectError("Connection refused")
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            resp = client.get("/health/deep")

        checks = resp.json()["checks"]
        assert "unreachable" in checks["ghl_api"]

    def test_deep_health_overall_status_ok(self, client):
        """Overall status is 'ok' when all checks pass."""
        with patch("httpx.AsyncClient", return_value=_make_httpx_mock()):
            resp = client.get("/health/deep")

        assert resp.json()["status"] == "ok"
