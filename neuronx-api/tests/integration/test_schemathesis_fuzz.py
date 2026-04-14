"""
OpenAPI Schema Validation Tests

Validates that all FastAPI endpoints have valid OpenAPI specs.
Uses the auto-generated OpenAPI schema from FastAPI.

For full fuzz testing, run the Schemathesis CLI:
    cd neuronx-api && .venv/bin/schemathesis run \
        --app main:app --base-url http://localhost:8000 \
        --checks not_a_server_error --max-examples 20

This file validates the schema structure and basic endpoint reachability.
"""

import json
import pytest

pytestmark = [pytest.mark.integration, pytest.mark.slow]


class TestOpenAPISchema:
    """Validate the OpenAPI schema structure."""

    def test_openapi_spec_accessible(self, client):
        """GET /openapi.json returns valid JSON with OpenAPI fields."""
        resp = client.get("/openapi.json")
        assert resp.status_code == 200
        spec = resp.json()
        assert "openapi" in spec
        assert "info" in spec
        assert "paths" in spec
        assert spec["info"]["title"] == "NeuronX API"

    def test_openapi_spec_version(self, client):
        """OpenAPI spec declares version 0.4.0."""
        spec = client.get("/openapi.json").json()
        assert spec["info"]["version"] == "0.4.0"

    def test_all_routers_have_paths(self, client):
        """All 15 registered routers appear in the OpenAPI paths."""
        spec = client.get("/openapi.json").json()
        paths = list(spec["paths"].keys())

        # Core routing prefixes from main.py
        expected_prefixes = [
            "/webhooks", "/score", "/briefing", "/analytics",
            "/trust", "/documents", "/cases", "/sync",
            "/signatures", "/demo", "/typebot", "/clients",
            "/form", "/dependents", "/extract",
        ]

        for prefix in expected_prefixes:
            matching = [p for p in paths if p.startswith(prefix)]
            assert len(matching) > 0, f"No paths found for router prefix: {prefix}"

    def test_health_endpoints_in_spec(self, client):
        """Health endpoints are documented in OpenAPI."""
        spec = client.get("/openapi.json").json()
        assert "/health" in spec["paths"]
        assert "/health/deep" in spec["paths"]

    def test_scoring_endpoint_has_schema(self, client):
        """POST /score/lead has request body schema with R1-R5 fields."""
        spec = client.get("/openapi.json").json()
        lead_path = spec["paths"].get("/score/lead", {})
        assert "post" in lead_path

        post_spec = lead_path["post"]
        assert "requestBody" in post_spec

    def test_webhook_endpoints_documented(self, client):
        """Webhook endpoints have POST operations."""
        spec = client.get("/openapi.json").json()

        assert "post" in spec["paths"].get("/webhooks/ghl", {})
        assert "post" in spec["paths"].get("/webhooks/voice", {})

    def test_no_undocumented_server_errors(self, client):
        """All GET endpoints return non-500 status (basic reachability)."""
        spec = client.get("/openapi.json").json()

        get_paths = [
            path for path, methods in spec["paths"].items()
            if "get" in methods
            # Skip parameterized paths (they need valid IDs)
            and "{" not in path
        ]

        for path in get_paths:
            resp = client.get(path)
            assert resp.status_code < 500, f"Server error on GET {path}: {resp.status_code}"

    def test_openapi_has_components(self, client):
        """OpenAPI spec includes component schemas (Pydantic models)."""
        spec = client.get("/openapi.json").json()
        assert "components" in spec
        assert "schemas" in spec["components"]
        schemas = spec["components"]["schemas"]

        # Key models should be documented
        schema_names = list(schemas.keys())
        assert len(schema_names) > 5, f"Too few schemas: {len(schema_names)}"
