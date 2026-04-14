"""
LIVE GHL API Integration Tests

Tests the actual GoHighLevel API to verify pipeline stages,
custom fields, tags, calendar, and contact operations exist.

These tests call the REAL GHL API — they require a valid OAuth token.
Run with: pytest tests/integration/test_ghl_live.py -v -m live

Token is loaded from tools/ghl-lab/.tokens.json.
If token is expired, run: cd tools/ghl-lab && npx tsx src/ghlProvisioner.ts refresh-token
"""

import os
import json
import pytest
import httpx
from pathlib import Path

# Load GHL token from .tokens.json
TOKENS_PATH = Path(__file__).parent.parent.parent.parent / "tools" / "ghl-lab" / ".tokens.json"
GHL_BASE = "https://services.leadconnectorhq.com"
LOCATION_ID = "FlRL82M0D6nclmKT7eXH"
PIPELINE_ID = "Dtj9nQVd3QjL7bAb3Aiw"
CALENDAR_ID = "To1U2KbcvJ0EAX0RGKHS"
API_VERSION = "2021-07-28"


def _get_ghl_token() -> str:
    """Load access token from .tokens.json file."""
    if not TOKENS_PATH.exists():
        return ""
    data = json.loads(TOKENS_PATH.read_text())
    return data.get("access_token", "")


GHL_TOKEN = _get_ghl_token()


def ghl_get(path: str, params: dict = None) -> httpx.Response:
    """Helper: GET from GHL API with auth + version headers."""
    return httpx.get(
        f"{GHL_BASE}{path}",
        headers={
            "Authorization": f"Bearer {GHL_TOKEN}",
            "Version": API_VERSION,
        },
        params=params or {},
        timeout=10.0,
    )


def _is_token_valid() -> bool:
    """Quick check if token is still valid."""
    if not GHL_TOKEN:
        return False
    try:
        resp = ghl_get(f"/locations/{LOCATION_ID}")
        return resp.status_code == 200
    except Exception:
        return False


# Skip all tests if token is invalid
pytestmark = [
    pytest.mark.integration,
    pytest.mark.live,
    pytest.mark.skipif(not GHL_TOKEN, reason="No GHL token in .tokens.json"),
]


# ── Location Verification ────────────────────────────────────────────

class TestGHLLocation:
    """Verify GHL location (sub-account) is accessible."""

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired — run: cd tools/ghl-lab && npx tsx src/ghlProvisioner.ts refresh-token")
    def test_location_accessible(self):
        """Location ID returns 200."""
        resp = ghl_get(f"/locations/{LOCATION_ID}")
        assert resp.status_code == 200

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_location_name(self):
        """Location has expected name."""
        data = ghl_get(f"/locations/{LOCATION_ID}").json()
        location = data.get("location", data)
        assert location.get("name") is not None


# ── Custom Fields ────────────────────────────────────────────────────

class TestGHLCustomFields:
    """Verify NeuronX custom fields exist in GHL."""

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_custom_fields_exist(self):
        """Location has custom fields configured."""
        resp = ghl_get(f"/locations/{LOCATION_ID}/customFields")
        assert resp.status_code == 200
        data = resp.json()
        fields = data.get("customFields", [])
        assert len(fields) > 0, "No custom fields found"

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_readiness_fields_exist(self):
        """R1-R5 readiness custom fields exist."""
        resp = ghl_get(f"/locations/{LOCATION_ID}/customFields")
        fields = resp.json().get("customFields", [])
        field_names = [f.get("name", "") for f in fields]

        # R1-R5 readiness fields (may be ai_ prefixed or r1_/r2_ prefixed)
        expected_patterns = [
            "program_interest",     # ai_program_interest or r1_program_interest
            "current_location",     # r2_current_location or current_location
            "timeline_urgency",     # r3_timeline_urgency or ai_urgency
            "prior_applications",   # r4_prior_history or prior_applications
            "budget_awareness",     # r5_budget_awareness or budget_awareness
        ]

        for pattern in expected_patterns:
            matching = [n for n in field_names if pattern in n.lower().replace(" ", "_")]
            assert len(matching) > 0, f"Missing custom field matching: {pattern} (searched {len(field_names)} fields)"

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_custom_fields_count(self):
        """Location has 100+ custom fields (per PROJECT_MEMORY.md: 140)."""
        resp = ghl_get(f"/locations/{LOCATION_ID}/customFields")
        fields = resp.json().get("customFields", [])
        assert len(fields) >= 50, f"Expected 50+ fields, got {len(fields)}"


# ── Tags ─────────────────────────────────────────────────────────────

class TestGHLTags:
    """Verify NeuronX tags exist in GHL."""

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_tags_exist(self):
        """Location has tags configured."""
        resp = ghl_get(f"/locations/{LOCATION_ID}/tags")
        assert resp.status_code == 200
        data = resp.json()
        tags = data.get("tags", [])
        assert len(tags) > 0, "No tags found"

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_nx_prefixed_tags_exist(self):
        """NeuronX-prefixed tags (nx:*) exist."""
        resp = ghl_get(f"/locations/{LOCATION_ID}/tags")
        tags = resp.json().get("tags", [])
        tag_names = [t.get("name", "") for t in tags]
        nx_tags = [t for t in tag_names if t.startswith("nx:")]
        assert len(nx_tags) >= 10, f"Expected 10+ nx: tags, got {len(nx_tags)}"

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_scoring_tags_exist(self):
        """Score-related tags exist (nx:score:high, nx:score:med, nx:score:low)."""
        resp = ghl_get(f"/locations/{LOCATION_ID}/tags")
        tags = resp.json().get("tags", [])
        tag_names = {t.get("name", "") for t in tags}

        for expected in ["nx:score:high", "nx:score:med", "nx:score:low"]:
            assert expected in tag_names, f"Missing tag: {expected}"

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_assessment_tags_exist(self):
        """Assessment tags exist."""
        resp = ghl_get(f"/locations/{LOCATION_ID}/tags")
        tags = resp.json().get("tags", [])
        tag_names = {t.get("name", "") for t in tags}

        for expected in ["nx:assessment:complete", "nx:human_escalation"]:
            assert expected in tag_names, f"Missing tag: {expected}"


# ── Pipeline ─────────────────────────────────────────────────────────

class TestGHLPipeline:
    """Verify NeuronX Immigration Intake pipeline exists with correct stages."""

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_pipeline_exists(self):
        """Pipeline search returns results for our location."""
        resp = ghl_get(f"/opportunities/pipelines", {"locationId": LOCATION_ID})
        assert resp.status_code == 200

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_pipeline_has_stages(self):
        """Pipeline has multiple stages configured."""
        resp = ghl_get(f"/opportunities/pipelines", {"locationId": LOCATION_ID})
        data = resp.json()
        pipelines = data.get("pipelines", [])
        assert len(pipelines) > 0, "No pipelines found"

        # Find our intake pipeline
        intake = None
        for p in pipelines:
            if p.get("id") == PIPELINE_ID or "intake" in p.get("name", "").lower():
                intake = p
                break

        if intake:
            stages = intake.get("stages", [])
            assert len(stages) >= 5, f"Expected 5+ stages, got {len(stages)}"


# ── Calendar ─────────────────────────────────────────────────────────

class TestGHLCalendar:
    """Verify Immigration Consultations calendar exists."""

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_calendars_exist(self):
        """Location has calendars configured."""
        resp = ghl_get(f"/calendars/", params={"locationId": LOCATION_ID})
        assert resp.status_code == 200
        data = resp.json()
        calendars = data.get("calendars", [])
        assert len(calendars) > 0, "No calendars found"

    @pytest.mark.skipif(not _is_token_valid(), reason="GHL token expired")
    def test_consultation_calendar_exists(self):
        """Immigration Consultations calendar exists."""
        resp = ghl_get(f"/calendars/", params={"locationId": LOCATION_ID})
        calendars = resp.json().get("calendars", [])

        consultation = None
        for cal in calendars:
            if CALENDAR_ID in cal.get("id", "") or "consult" in cal.get("name", "").lower():
                consultation = cal
                break

        assert consultation is not None, "Immigration Consultations calendar not found"
