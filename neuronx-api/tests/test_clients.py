"""Tests for client data endpoints (Chrome extension + data sheets)."""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_search_requires_query(client):
    r = client.get("/clients/search")
    assert r.status_code == 422  # Missing required q param


def test_search_min_length(client):
    r = client.get("/clients/search?q=a")
    assert r.status_code == 422  # Too short


def test_form_data_not_found(client):
    """Should return 404 for non-existent contact."""
    r = client.get("/clients/nonexistent123/form-data")
    assert r.status_code == 404


def test_data_sheet_not_found(client):
    r = client.get("/clients/nonexistent123/data-sheet")
    assert r.status_code == 404


def test_validate_not_found(client):
    r = client.get("/clients/nonexistent123/validate")
    assert r.status_code == 404


def test_copy_paste_not_found(client):
    r = client.get("/clients/nonexistent123/copy-paste")
    assert r.status_code == 404
