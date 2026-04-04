"""Tests for document generation endpoints."""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_checklist_express_entry(client):
    r = client.post("/documents/checklist", json={
        "contact_id": "test-doc-001",
        "program_type": "Express Entry",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["program_type"] == "Express Entry"
    assert data["total_required"] >= 8
    assert "Valid passport" in data["required_documents"][0]


def test_checklist_spousal(client):
    r = client.post("/documents/checklist", json={
        "contact_id": "test-doc-002",
        "program_type": "Spousal Sponsorship",
    })
    assert r.status_code == 200
    assert r.json()["total_required"] >= 8


def test_checklist_all_programs(client):
    """Every program returns a valid checklist."""
    programs = [
        "Express Entry", "Spousal Sponsorship", "Work Permit",
        "Study Permit", "LMIA", "PR Renewal", "Citizenship", "Visitor Visa",
    ]
    for p in programs:
        r = client.post("/documents/checklist", json={
            "contact_id": "test-doc-all",
            "program_type": p,
        })
        assert r.status_code == 200, f"Failed for {p}"
        assert r.json()["total_required"] > 0, f"Empty checklist for {p}"


def test_checklist_unknown_program(client):
    r = client.post("/documents/checklist", json={
        "contact_id": "test-doc-003",
        "program_type": "Martian Visa",
    })
    assert r.status_code == 400


def test_checklist_fuzzy_match(client):
    r = client.post("/documents/checklist", json={
        "contact_id": "test-doc-004",
        "program_type": "express entry",  # lowercase
    })
    assert r.status_code == 200
    assert r.json()["program_type"] == "Express Entry"
