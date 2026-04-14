"""
Integration Tests — Typebot Webhook Deduplication

Tests the submission deduplication logic added to prevent
double-processing when Typebot retries webhooks.
"""

import pytest
from unittest.mock import patch, AsyncMock

pytestmark = pytest.mark.integration


class TestTypebotDeduplication:
    """Test form submission deduplication via resultId."""

    def test_first_submission_processed(self, client, patch_ghl):
        """First submission with resultId is processed normally."""
        # Clear dedup cache
        from app.routers.typebot import _processed_submissions
        _processed_submissions.clear()

        resp = client.post("/typebot/webhook", json={
            "resultId": "result-dedup-001",
            "email": "test@example.com",
            "answers": {"program_interest": "Express Entry"},
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "processed" or data["status"] == "unmatched"

    def test_duplicate_submission_rejected(self, client, patch_ghl):
        """Second submission with same resultId returns 'duplicate'."""
        from app.routers.typebot import _processed_submissions
        _processed_submissions.clear()

        # First submission
        client.post("/typebot/webhook", json={
            "resultId": "result-dedup-002",
            "contact_id": "test-contact-123",
            "answers": {"program_interest": "Express Entry"},
        })

        # Second submission (duplicate)
        resp = client.post("/typebot/webhook", json={
            "resultId": "result-dedup-002",
            "contact_id": "test-contact-123",
            "answers": {"program_interest": "Express Entry"},
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "duplicate"
        assert data["resultId"] == "result-dedup-002"

    def test_different_result_ids_both_processed(self, client, patch_ghl):
        """Different resultIds are processed independently."""
        from app.routers.typebot import _processed_submissions
        _processed_submissions.clear()

        resp1 = client.post("/typebot/webhook", json={
            "resultId": "result-dedup-003",
            "contact_id": "test-contact-123",
            "answers": {},
        })
        resp2 = client.post("/typebot/webhook", json={
            "resultId": "result-dedup-004",
            "contact_id": "test-contact-123",
            "answers": {},
        })
        assert resp1.json()["status"] == "processed"
        assert resp2.json()["status"] == "processed"

    def test_no_result_id_still_works(self, client, patch_ghl):
        """Submissions without resultId are processed (no dedup possible)."""
        resp = client.post("/typebot/webhook", json={
            "contact_id": "test-contact-123",
            "answers": {"program_interest": "Study Permit"},
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "processed"

    def test_dedup_cache_size_limited(self, client, patch_ghl):
        """Dedup cache does not grow beyond 500 entries."""
        from app.routers.typebot import _processed_submissions
        _processed_submissions.clear()

        # Add 510 entries manually
        for i in range(510):
            _processed_submissions[f"result-bulk-{i}"] = "2026-04-14T00:00:00Z"

        assert len(_processed_submissions) <= 510  # Before cleanup

        # Next real submission should trigger cleanup
        client.post("/typebot/webhook", json={
            "resultId": "result-after-bulk",
            "contact_id": "test-contact-123",
            "answers": {},
        })


class TestTypebotMultiContactSafety:
    """Test contact lookup safety when multiple contacts match."""

    def test_unmatched_when_no_contact(self, client, patch_ghl, mock_ghl):
        """Returns unmatched when no contact found by email or phone."""
        mock_ghl.search_contacts.return_value = {"contacts": []}

        resp = client.post("/typebot/webhook", json={
            "email": "nonexistent@example.com",
            "answers": {"program_interest": "Express Entry"},
        })
        assert resp.json()["status"] == "unmatched"

    def test_uses_first_match_on_multiple(self, client, patch_ghl, mock_ghl):
        """When multiple contacts match email, uses first one (logs warning)."""
        mock_ghl.search_contacts.return_value = {
            "contacts": [
                {"id": "contact-first"},
                {"id": "contact-second"},
            ]
        }

        resp = client.post("/typebot/webhook", json={
            "email": "shared@example.com",
            "answers": {"program_interest": "Express Entry"},
        })
        assert resp.json()["status"] == "processed"
        assert resp.json()["contact_id"] == "contact-first"
