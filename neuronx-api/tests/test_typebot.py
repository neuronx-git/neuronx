"""Tests for Typebot webhook and form generation."""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.services.typebot_service import TypebotService


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def service():
    return TypebotService()


def test_generate_form_json_express_entry(service):
    """Generate Typebot JSON for Express Entry program."""
    json = service.generate_form_json("Express Entry")
    assert json["name"] == "Visa Master Canada — Express Entry Onboarding"
    assert len(json["groups"]) >= 5  # Welcome, Personal, Family, Program, Docs, Complete
    assert len(json["edges"]) >= 4
    assert json["publicId"] == "express-entry-onboarding"
    assert json["settings"]["general"]["isBrandingEnabled"] is False


def test_generate_form_json_spousal(service):
    json = service.generate_form_json("Spousal Sponsorship")
    assert "Spousal Sponsorship" in json["name"]
    assert json["publicId"] == "spousal-sponsorship-onboarding"


def test_generate_form_json_unknown_program(service):
    """Unknown program should still generate a form with common questions."""
    json = service.generate_form_json("Martian Visa")
    assert len(json["groups"]) >= 4  # Welcome, Personal, Family, Docs, Complete (no program group)


def test_generate_form_json_with_webhook(service):
    json = service.generate_form_json("Express Entry", webhook_url="https://example.com/webhook")
    # Last group should contain a webhook block
    last_group = json["groups"][-1]
    webhook_blocks = [b for b in last_group["blocks"] if b.get("type") == "Webhook"]
    assert len(webhook_blocks) == 1
    assert webhook_blocks[0]["options"]["url"] == "https://example.com/webhook"


def test_generate_form_json_custom_firm_name(service):
    json = service.generate_form_json("Express Entry", firm_name="ABC Immigration")
    assert "ABC Immigration" in json["name"]


def test_generate_form_json_theme(service):
    json = service.generate_form_json("Express Entry")
    theme = json["theme"]
    assert theme["general"]["font"] == "Inter"
    assert theme["chat"]["buttons"]["backgroundColor"] == "#E8380D"


def test_webhook_endpoint_no_contact(client):
    """Webhook should return unmatched if no contact found."""
    r = client.post("/typebot/webhook", json={
        "answers": {"program_interest": "Express Entry", "education_level": "Master's"},
    })
    assert r.status_code == 200
    assert r.json()["status"] == "unmatched"


def test_form_url_no_typebot(client):
    """Form URL should indicate Typebot not deployed."""
    r = client.get("/typebot/form-url/Express Entry")
    assert r.status_code == 200
    data = r.json()
    assert data["url"] is None
    assert "not deployed" in data["note"]


def test_create_form_no_typebot(client):
    """Create form should return 503 when Typebot not configured."""
    r = client.post("/typebot/create-form", json={
        "program_type": "Express Entry",
    })
    assert r.status_code == 503


def test_question_to_block_text(service):
    block = service._question_to_block({"key": "name", "label": "Full Name", "type": "text", "required": True})
    assert block["type"] == "text input"
    assert block["options"]["isRequired"] is True


def test_question_to_block_select(service):
    block = service._question_to_block({
        "key": "edu", "label": "Education", "type": "select",
        "options": ["High School", "Bachelor", "Master"]
    })
    assert block["type"] == "choice input"
    assert len(block["options"]["items"]) == 3


def test_question_to_block_boolean(service):
    block = service._question_to_block({"key": "criminal", "label": "Criminal history?", "type": "boolean"})
    assert block["type"] == "choice input"
    assert len(block["options"]["items"]) == 2
