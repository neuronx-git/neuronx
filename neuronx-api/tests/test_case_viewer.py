"""Tests for the Case Documents Viewer UI routes."""

import time

import pytest
from fastapi.testclient import TestClient

from main import app
from app.routers.case_viewer import _sign_download, _verify_download, _presigned_url


@pytest.fixture
def client():
    return TestClient(app)


# ── Rendering ──────────────────────────────────────────────────────────

def test_viewer_renders_for_demo_case(client):
    """NX-prefixed case_ids get placeholder data when DB absent — must render."""
    r = client.get("/cases/NX-20260301-DEMO01/viewer")
    assert r.status_code == 200, r.text
    assert "text/html" in r.headers["content-type"]
    body = r.text
    assert "NX-20260301-DEMO01" in body
    assert "Priya Sharma" in body              # placeholder client
    assert "Express Entry" in body             # placeholder program
    assert "Timeline" in body
    assert "Checklist" in body
    assert "Documents" in body


def test_documents_only_viewer_renders(client):
    r = client.get("/cases/NX-20260301-DEMO01/documents/viewer")
    assert r.status_code == 200
    assert "Documents" in r.text


def test_viewer_404_for_unknown_non_nx_case(client):
    """Non-NX- prefixed IDs with no DB match must 404."""
    r = client.get("/cases/not-a-real-case/viewer")
    assert r.status_code == 404


def test_viewer_data_returns_json(client):
    r = client.get("/cases/NX-20260301-DEMO01/viewer/data")
    assert r.status_code == 200
    data = r.json()
    assert data["case_id"] == "NX-20260301-DEMO01"
    assert "documents" in data
    assert "checklist" in data
    assert "activities" in data
    assert "stats" in data
    assert data["stats"]["required_total"] > 0
    assert 0 <= data["stats"]["progress_pct"] <= 100


# ── Brand / structural assertions ──────────────────────────────────────

def test_viewer_contains_brand_colors(client):
    r = client.get("/cases/NX-20260301-DEMO01/viewer")
    # Navy (header) + orange (accent) + Inter font
    assert "#0F172A" in r.text or "brand-navy" in r.text
    assert "#E8380D" in r.text or "brand-orange" in r.text
    assert "Inter" in r.text


def test_viewer_contains_timeline_events(client):
    r = client.get("/cases/NX-20260301-DEMO01/viewer")
    assert "Case initiated" in r.text
    assert "uploaded" in r.text.lower()


# ── Presigned downloads ────────────────────────────────────────────────

def test_presigned_url_round_trip():
    url = _presigned_url("NX-1", "doc-1", ttl_sec=60)
    assert "expires=" in url and "sig=" in url
    # Extract and verify
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    qs = dict(urllib.parse.parse_qsl(parsed.query))
    assert _verify_download("NX-1", "doc-1", int(qs["expires"]), qs["sig"])


def test_download_rejects_expired_link(client):
    expired = int(time.time()) - 10
    sig = _sign_download("NX-1", "doc-1", expired)
    r = client.get(f"/cases/NX-1/documents/doc-1/download?expires={expired}&sig={sig}")
    assert r.status_code == 410


def test_download_rejects_bad_signature(client):
    future = int(time.time()) + 60
    r = client.get(f"/cases/NX-1/documents/doc-1/download?expires={future}&sig=bogus")
    assert r.status_code == 410


def test_download_accepts_valid_signature(client):
    future = int(time.time()) + 60
    sig = _sign_download("NX-X", "doc-X", future)
    # follow_redirects=False so we see the 200/302 from our handler, not storage
    r = client.get(
        f"/cases/NX-X/documents/doc-X/download?expires={future}&sig={sig}",
        follow_redirects=False,
    )
    # When storage backend is absent we return 200 stub; when present 302.
    assert r.status_code in (200, 302)


# ── case_viewer_url in case response ───────────────────────────────────

def test_case_viewer_url_not_in_unknown_case(client):
    """Unknown case still 404s without leaking viewer URL."""
    r = client.get("/cases/by-id/does-not-exist")
    assert r.status_code == 404
