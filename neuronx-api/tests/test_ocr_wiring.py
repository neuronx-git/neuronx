"""
Tests for OCR wiring (upload-and-sync to GHL) and duplicate file prevention.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestDuplicateFilePrevention:
    def test_duplicate_upload_returns_cached(self, client):
        """Same file content uploaded twice should return cached result on second call."""
        from app.routers.doc_extract import _processed_hashes
        _processed_hashes.clear()

        with patch("app.routers.doc_extract.DocOCRService") as MockService:
            mock_svc = AsyncMock()
            mock_svc.extract.return_value = {
                "doc_type": "passport", "method": "fastmrz",
                "extracted_fields": {"full_name": "John Doe"},
                "field_count": 1, "confidence": "high",
            }
            MockService.return_value = mock_svc

            # First upload
            r1 = client.post(
                "/extract/upload",
                files={"file": ("passport.jpg", b"identical_content", "image/jpeg")},
                data={"doc_type": "passport"},
            )
            assert r1.status_code == 200
            assert "duplicate" not in r1.json()

            # Second upload with same content
            r2 = client.post(
                "/extract/upload",
                files={"file": ("passport_copy.jpg", b"identical_content", "image/jpeg")},
                data={"doc_type": "passport"},
            )
            assert r2.status_code == 200
            assert r2.json().get("duplicate") is True
            # OCR service should only be called once
            assert mock_svc.extract.call_count == 1

        _processed_hashes.clear()

    def test_different_files_not_cached(self, client):
        from app.routers.doc_extract import _processed_hashes
        _processed_hashes.clear()

        with patch("app.routers.doc_extract.DocOCRService") as MockService:
            mock_svc = AsyncMock()
            mock_svc.extract.return_value = {
                "doc_type": "ielts", "method": "claude",
                "extracted_fields": {"overall_score": "7.5"},
                "field_count": 1, "confidence": "high",
            }
            MockService.return_value = mock_svc

            client.post("/extract/upload",
                        files={"file": ("doc1.pdf", b"content_a", "application/pdf")})
            client.post("/extract/upload",
                        files={"file": ("doc2.pdf", b"content_b", "application/pdf")})
            assert mock_svc.extract.call_count == 2

        _processed_hashes.clear()

    def test_cache_eviction(self, client):
        """Cache should evict when exceeding 100 entries."""
        from app.routers.doc_extract import _processed_hashes
        _processed_hashes.clear()

        # Pre-fill cache with 101 entries
        for i in range(101):
            _processed_hashes[f"hash_{i}"] = {"cached": True}

        with patch("app.routers.doc_extract.DocOCRService") as MockService:
            mock_svc = AsyncMock()
            mock_svc.extract.return_value = {
                "doc_type": "general", "method": "claude",
                "extracted_fields": {}, "field_count": 0, "confidence": "low",
            }
            MockService.return_value = mock_svc
            client.post("/extract/upload",
                        files={"file": ("new.pdf", b"new_content", "application/pdf")})
            # Should have evicted one and added one
            assert len(_processed_hashes) <= 101

        _processed_hashes.clear()


class TestOCRSyncToGHL:
    @patch("app.routers.doc_extract.DocOCRService")
    def test_upload_and_sync_passport(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.extract.return_value = {
            "doc_type": "passport", "method": "fastmrz",
            "extracted_fields": {
                "full_name": "John Doe",
                "date_of_birth": "1990-01-15",
                "passport_number": "AB123456",
                "passport_expiry": "2030-12-31",
                "nationality": "CAN",
            },
            "field_count": 5, "confidence": "high",
        }
        MockService.return_value = mock_svc

        mock_ghl = AsyncMock()
        with patch("app.routers.doc_extract.GHLClient", return_value=mock_ghl):
            r = client.post(
                "/extract/upload-and-sync",
                files={"file": ("passport.jpg", b"fake_passport", "image/jpeg")},
                data={"contact_id": "c1", "doc_type": "passport"},
            )

        assert r.status_code == 200
        data = r.json()
        assert data["ghl_sync"] == "synced"
        assert "passport_number" in data["ghl_fields_updated"]
        assert data["ghl_fields_updated"]["passport_number"] == "AB123456"
        assert data["contact_id"] == "c1"

    @patch("app.routers.doc_extract.DocOCRService")
    def test_upload_and_sync_ielts(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.extract.return_value = {
            "doc_type": "ielts", "method": "claude",
            "extracted_fields": {
                "overall_score": "7.5",
                "listening_score": "8.0",
                "reading_score": "7.0",
                "writing_score": "6.5",
                "speaking_score": "7.5",
                "test_type": "IELTS General",
            },
            "field_count": 6, "confidence": "high",
        }
        MockService.return_value = mock_svc

        mock_ghl = AsyncMock()
        with patch("app.routers.doc_extract.GHLClient", return_value=mock_ghl):
            r = client.post(
                "/extract/upload-and-sync",
                files={"file": ("ielts.pdf", b"fake_ielts", "application/pdf")},
                data={"contact_id": "c2", "doc_type": "ielts"},
            )

        assert r.status_code == 200
        data = r.json()
        assert data["ghl_sync"] == "synced"
        assert "language_overall_score" in data["ghl_fields_updated"]

    @patch("app.routers.doc_extract.DocOCRService")
    def test_upload_and_sync_no_fields(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.extract.return_value = {
            "doc_type": "general", "method": "claude",
            "extracted_fields": {},
            "field_count": 0, "confidence": "none",
        }
        MockService.return_value = mock_svc

        r = client.post(
            "/extract/upload-and-sync",
            files={"file": ("blurry.jpg", b"fake", "image/jpeg")},
            data={"contact_id": "c3"},
        )
        assert r.status_code == 200
        assert r.json()["ghl_sync"] == "skipped"

    @patch("app.routers.doc_extract.DocOCRService")
    def test_upload_and_sync_ghl_error(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.extract.return_value = {
            "doc_type": "passport", "method": "fastmrz",
            "extracted_fields": {"full_name": "Test"},
            "field_count": 1, "confidence": "high",
        }
        MockService.return_value = mock_svc

        mock_ghl = AsyncMock()
        mock_ghl.update_custom_fields.side_effect = Exception("GHL API error")

        with patch("app.routers.doc_extract.GHLClient", return_value=mock_ghl):
            r = client.post(
                "/extract/upload-and-sync",
                files={"file": ("passport.jpg", b"fake", "image/jpeg")},
                data={"contact_id": "c4"},
            )

        assert r.status_code == 200
        assert "error" in r.json()["ghl_sync"]

    def test_upload_and_sync_empty_file(self, client):
        r = client.post(
            "/extract/upload-and-sync",
            files={"file": ("empty.jpg", b"", "image/jpeg")},
            data={"contact_id": "c1"},
        )
        assert r.status_code == 400

    def test_upload_and_sync_too_large(self, client):
        r = client.post(
            "/extract/upload-and-sync",
            files={"file": ("big.jpg", b"x" * (11 * 1024 * 1024), "image/jpeg")},
            data={"contact_id": "c1"},
        )
        assert r.status_code == 413

    @patch("app.routers.doc_extract.DocOCRService")
    def test_upload_and_sync_employment(self, MockService, client):
        mock_svc = AsyncMock()
        mock_svc.extract.return_value = {
            "doc_type": "employment_letter", "method": "claude",
            "extracted_fields": {
                "employer_name": "Acme Corp",
                "job_title": "Software Engineer",
                "noc_code": "21232",
            },
            "field_count": 3, "confidence": "high",
        }
        MockService.return_value = mock_svc

        mock_ghl = AsyncMock()
        with patch("app.routers.doc_extract.GHLClient", return_value=mock_ghl):
            r = client.post(
                "/extract/upload-and-sync",
                files={"file": ("employment.pdf", b"fake", "application/pdf")},
                data={"contact_id": "c5", "doc_type": "employment_letter"},
            )
        assert r.status_code == 200
        fields = r.json()["ghl_fields_updated"]
        assert fields["employer_name"] == "Acme Corp"
        assert fields["noc_code"] == "21232"
