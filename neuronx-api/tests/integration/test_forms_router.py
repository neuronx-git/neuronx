"""
Integration Tests — Forms Router

Tests the multi-tenant form serving endpoints:
  GET /form/{tenant_slug}/{form_slug}
  GET /form/{tenant_slug}
"""

import pytest


@pytest.mark.integration
class TestServeForm:
    """Tests for GET /form/{tenant}/{form_slug}."""

    def test_valid_tenant_and_form_returns_200(self, client):
        """GET /form/vmc/onboarding returns 200."""
        response = client.get("/form/vmc/onboarding")
        assert response.status_code == 200

    def test_response_is_html(self, client):
        """Response Content-Type is text/html."""
        response = client.get("/form/vmc/onboarding")
        assert "text/html" in response.headers["content-type"]

    def test_html_contains_typebot_id(self, client):
        """HTML body contains the typebot_id from config."""
        response = client.get("/form/vmc/onboarding")
        assert "vmc-onboarding" in response.text

    def test_html_contains_tenant_name(self, client):
        """HTML body contains the tenant display name."""
        response = client.get("/form/vmc/onboarding")
        assert "Visa Master Canada" in response.text

    def test_html_contains_iframe(self, client):
        """HTML body contains an iframe pointing to the Typebot viewer."""
        response = client.get("/form/vmc/onboarding")
        assert "typebot-standard" in response.text

    def test_html_contains_typebot_api_url(self, client):
        """HTML embed contains the typebot builder API URL."""
        response = client.get("/form/vmc/onboarding")
        assert "builder-production-6784.up.railway.app" in response.text

    def test_invalid_tenant_returns_404(self, client):
        """GET /form/nonexistent-tenant/onboarding returns 404."""
        response = client.get("/form/nonexistent-tenant/onboarding")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_invalid_form_slug_returns_404_with_available(self, client):
        """GET /form/vmc/nonexistent-form returns 404 with available forms."""
        response = client.get("/form/vmc/nonexistent-form")
        assert response.status_code == 404
        detail = response.json()["detail"]
        assert "nonexistent-form" in detail
        assert "onboarding" in detail  # lists available forms


@pytest.mark.integration
class TestListForms:
    """Tests for GET /form/{tenant_slug}."""

    def test_list_forms_returns_200(self, client):
        """GET /form/vmc returns 200 with HTML listing."""
        response = client.get("/form/vmc")
        assert response.status_code == 200

    def test_list_forms_is_html(self, client):
        """Response Content-Type is text/html."""
        response = client.get("/form/vmc")
        assert "text/html" in response.headers["content-type"]

    def test_list_forms_contains_links(self, client):
        """HTML listing contains links to available forms."""
        response = client.get("/form/vmc")
        assert "/form/vmc/onboarding" in response.text

    def test_list_forms_contains_tenant_name(self, client):
        """HTML listing contains tenant name."""
        response = client.get("/form/vmc")
        assert "Visa Master Canada" in response.text

    def test_list_forms_invalid_tenant_returns_404(self, client):
        """GET /form/invalid-tenant returns 404."""
        response = client.get("/form/invalid-tenant")
        assert response.status_code == 404
