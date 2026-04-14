"""
NeuronX API — Shared Test Infrastructure

Provides:
- Shared FastAPI TestClient
- Mock factories for external services (GHL, VAPI, Claude, Typebot, Documenso)
- JSON fixture loader
- Environment setup (webhook verification disabled, test mode)
"""

import os
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# ── Environment setup (before any app imports) ──────────────────────
os.environ["VERIFY_WEBHOOKS"] = "false"
os.environ["ENV"] = "test"
os.environ["ADMIN_API_KEY"] = "neuronx-admin-dev"
os.environ["GHL_LOCATION_ID"] = "test-location-id"
os.environ["GHL_COMPANY_ID"] = "test-company-id"
os.environ["GHL_API_BASE_URL"] = "https://services.leadconnectorhq.com"
os.environ["GHL_ACCESS_TOKEN"] = "test-ghl-token"
os.environ["GHL_WEBHOOK_SECRET"] = "test-webhook-secret"
os.environ["GHL_CALENDAR_ID"] = "test-calendar-id"
os.environ["GHL_PIPELINE_ID"] = "test-pipeline-id"
os.environ["VAPI_API_KEY"] = "test-vapi-key"
os.environ["VAPI_WEBHOOK_SECRET"] = "test-vapi-secret"
os.environ["ANTHROPIC_API_KEY"] = "test-anthropic-key"
os.environ["TYPEBOT_URL"] = "https://test-typebot.example.com"
os.environ["TYPEBOT_API_TOKEN"] = "test-typebot-token"
os.environ["TYPEBOT_VIEWER_URL"] = "https://test-viewer.example.com"
os.environ["DOCUMENSO_URL"] = "https://test-documenso.example.com"
os.environ["DOCUMENSO_API_KEY"] = "test-documenso-key"
os.environ["CORS_ORIGINS"] = '["http://localhost:3000"]'
os.environ["COMPLIANCE_LOG_PATH"] = "/tmp/neuronx-test-compliance.jsonl"


# ── Fixtures directory ──────────────────────────────────────────────
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    """Load a JSON fixture file by name (without .json extension)."""
    path = FIXTURES_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Fixture not found: {path}")
    with open(path) as f:
        return json.load(f)


@pytest.fixture
def fixture_loader():
    """Provides fixture loading function to tests."""
    return load_fixture


# ── FastAPI TestClient ──────────────────────────────────────────────
@pytest.fixture
def client():
    """Shared FastAPI test client. Fresh per test function."""
    from main import app
    with TestClient(app) as c:
        yield c


# ── Mock GHL Client ─────────────────────────────────────────────────
@pytest.fixture
def mock_ghl():
    """Pre-configured GHL client mock with all methods."""
    mock = AsyncMock()
    mock.get_contact.return_value = {
        "contact": {
            "id": "test-contact-123",
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "phone": "+14165551234",
            "tags": [],
            "customFields": [],
        }
    }
    mock.update_contact.return_value = {"contact": {"id": "test-contact-123"}}
    mock.update_custom_fields.return_value = {"contact": {"id": "test-contact-123"}}
    mock.add_tag.return_value = {"tags": ["nx:score:high"]}
    mock.add_tags.return_value = {"tags": ["nx:score:high", "nx:assessment:complete"]}
    mock.remove_tag.return_value = {}
    mock.add_note.return_value = {"note": {"id": "note-123"}}
    mock.get_appointment.return_value = {
        "id": "appt-123",
        "calendarId": "test-calendar-id",
        "contactId": "test-contact-123",
        "status": "confirmed",
        "startTime": "2026-04-20T09:00:00Z",
        "endTime": "2026-04-20T09:30:00Z",
    }
    mock.get_opportunities_by_contact.return_value = {
        "opportunities": []
    }
    mock.update_opportunity_stage.return_value = {"opportunity": {"id": "opp-123"}}
    mock.send_email.return_value = {"messageId": "msg-123"}
    mock.search_contacts.return_value = {"contacts": []}
    mock.get_pipeline_opportunities.return_value = {"opportunities": []}
    return mock


@pytest.fixture
def patch_ghl(mock_ghl):
    """Patches GHLClient across all routers that import it."""
    with patch("app.routers.webhooks.GHLClient", return_value=mock_ghl), \
         patch("app.routers.doc_extract.GHLClient", return_value=mock_ghl), \
         patch("app.routers.cases.GHLClient", return_value=mock_ghl), \
         patch("app.routers.documents.GHLClient", return_value=mock_ghl), \
         patch("app.routers.typebot.GHLClient", return_value=mock_ghl), \
         patch("app.routers.signatures.GHLClient", return_value=mock_ghl), \
         patch("app.routers.clients.GHLClient", return_value=mock_ghl), \
         patch("app.services.ghl_client.GHLClient", return_value=mock_ghl), \
         patch("app.services.case_service.GHLClient", return_value=mock_ghl):
        yield mock_ghl


# ── Mock Compliance Logger ──────────────────────────────────────────
@pytest.fixture(autouse=True)
def mock_compliance_log():
    """Suppress compliance logging in tests (file I/O)."""
    with patch("app.utils.compliance_log.log_event"):
        yield


# ── Sample Payloads ─────────────────────────────────────────────────
@pytest.fixture
def ghl_contact_payload():
    """Minimal GHL ContactCreated webhook payload."""
    return {
        "type": "ContactCreate",
        "locationId": "test-location-id",
        "id": "contact-001",
        "firstName": "Maria",
        "lastName": "Santos",
        "email": "maria@example.com",
        "phone": "+14165559999",
        "source": "Landing Page",
        "tags": [],
        "customFields": [],
    }


@pytest.fixture
def vapi_end_of_call_payload():
    """VAPI end-of-call-report webhook payload with R1-R5 structured data."""
    return {
        "message": {
            "type": "end-of-call-report",
            "call": {
                "id": "call-001",
                "status": "ended",
                "type": "outboundPhoneCall",
            },
            "analysis": {
                "structuredData": {
                    "program_interest": "Express Entry",
                    "current_location": "Outside Canada",
                    "timeline_urgency": "Urgent (30 days)",
                    "prior_applications": "None",
                    "budget_awareness": "Aware",
                },
                "summary": "Prospect interested in Express Entry, located outside Canada, urgent timeline."
            },
            "artifact": {
                "transcript": "AI: Welcome to NeuronX. How can I help?\nProspect: I want to apply for Express Entry.\nAI: Great. Where are you currently located?\nProspect: I'm in India.\nAI: What's your timeline?\nProspect: I need to apply within 30 days."
            },
            "customer": {
                "number": "+14165559999"
            }
        }
    }


@pytest.fixture
def typebot_submission_payload():
    """Typebot form submission webhook payload."""
    return {
        "resultId": "result-001",
        "typebot": {
            "id": "typebot-001",
        },
        "answers": [
            {"blockId": "block-1", "variableId": "var-1", "content": "Express Entry"},
            {"blockId": "block-2", "variableId": "var-2", "content": "maria@example.com"},
            {"blockId": "block-3", "variableId": "var-3", "content": "+14165559999"},
            {"blockId": "block-4", "variableId": "var-4", "content": "Maria Santos"},
        ],
        "variables": [
            {"id": "var-1", "name": "program_interest", "value": "Express Entry"},
            {"id": "var-2", "name": "email", "value": "maria@example.com"},
            {"id": "var-3", "name": "phone", "value": "+14165559999"},
            {"id": "var-4", "name": "full_name", "value": "Maria Santos"},
        ],
    }


@pytest.fixture
def readiness_input_standard():
    """Standard readiness scoring input — all 5 dimensions, no complexity."""
    return {
        "contact_id": "test-contact-123",
        "r1_program_interest": "Express Entry",
        "r2_current_location": "Outside Canada",
        "r3_timeline_urgency": "Near-term (1-3 months)",
        "r4_prior_applications": "None",
        "r5_budget_awareness": "Aware",
    }


@pytest.fixture
def readiness_input_urgent():
    """Urgent readiness input — triggers urgent timeline bonus."""
    return {
        "contact_id": "test-contact-urgent",
        "r1_program_interest": "Spousal Sponsorship",
        "r2_current_location": "In Canada",
        "r3_timeline_urgency": "Urgent (30 days)",
        "r4_prior_applications": "None",
        "r5_budget_awareness": "Aware",
    }


@pytest.fixture
def readiness_input_complex():
    """Complex readiness input — transcript contains complexity keywords."""
    return {
        "contact_id": "test-contact-complex",
        "r1_program_interest": "Express Entry",
        "r2_current_location": "Outside Canada",
        "r3_timeline_urgency": "Near-term (1-3 months)",
        "r4_prior_applications": "Has Refusal",
        "r5_budget_awareness": "Aware",
        "transcript_excerpt": "I was previously deported from Canada and had a removal order.",
    }


@pytest.fixture
def readiness_input_minimal():
    """Minimal input — only 1 dimension (below min_dimensions_for_ready)."""
    return {
        "contact_id": "test-contact-minimal",
        "r1_program_interest": "Express Entry",
    }
