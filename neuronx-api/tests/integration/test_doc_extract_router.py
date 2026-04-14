"""
Integration Tests — Document OCR Extraction Router

Tests the /extract/* endpoints:
  GET  /extract/types
  POST /extract/upload
  POST /extract/upload-and-sync
"""

import pytest
from unittest.mock import patch, AsyncMock
from io import BytesIO


def _make_upload_file(content: bytes = b"fake-pdf-content", filename: str = "passport.jpg"):
    """Create a file-like tuple for TestClient file upload."""
    return {"file": (filename, BytesIO(content), "image/jpeg")}


@pytest.mark.integration
class TestListDocumentTypes:
    """Tests for GET /extract/types."""

    def test_returns_200(self, client):
        """GET /extract/types returns 200."""
        response = client.get("/extract/types")
        assert response.status_code == 200

    def test_returns_supported_types(self, client):
        """Response contains supported_types list."""
        response = client.get("/extract/types")
        body = response.json()
        assert "supported_types" in body
        assert isinstance(body["supported_types"], list)
        assert len(body["supported_types"]) > 0

    def test_types_include_passport(self, client):
        """Supported types include passport."""
        response = client.get("/extract/types")
        types = [t["type"] for t in response.json()["supported_types"]]
        assert "passport" in types

    def test_types_include_ielts(self, client):
        """Supported types include ielts."""
        response = client.get("/extract/types")
        types = [t["type"] for t in response.json()["supported_types"]]
        assert "ielts" in types

    def test_each_type_has_label_and_fields(self, client):
        """Each supported type has label and fields keys."""
        response = client.get("/extract/types")
        for doc_type in response.json()["supported_types"]:
            assert "label" in doc_type
            assert "fields" in doc_type
            assert "type" in doc_type


@pytest.mark.integration
class TestUploadDocument:
    """Tests for POST /extract/upload."""

    def test_upload_with_mock_ocr_returns_result(self, client):
        """Upload with mocked OCR service returns extraction result."""
        mock_result = {
            "method": "fastmrz",
            "extracted_fields": {"full_name": "John Doe", "passport_number": "AB1234567"},
            "field_count": 2,
            "confidence": "high",
            "doc_type": "passport",
            "doc_type_label": "Passport",
            "filename": "passport.jpg",
        }
        with patch("app.routers.doc_extract.DocOCRService") as MockService:
            instance = MockService.return_value
            instance.extract = AsyncMock(return_value=mock_result)
            response = client.post(
                "/extract/upload",
                files=_make_upload_file(),
                data={"doc_type": "passport"},
            )
        assert response.status_code == 200
        body = response.json()
        assert body["method"] == "fastmrz"
        assert body["field_count"] == 2
        assert body["extracted_fields"]["full_name"] == "John Doe"

    def test_upload_duplicate_returns_cached(self, client):
        """Uploading the same file content twice returns cached result with duplicate=True."""
        # Clear the module-level dedup cache first
        import app.routers.doc_extract as doc_mod
        doc_mod._processed_hashes.clear()

        content = b"unique-test-content-for-dedup"
        mock_result = {
            "method": "claude",
            "extracted_fields": {"test_field": "value"},
            "field_count": 1,
            "confidence": "medium",
            "doc_type": "general",
            "doc_type_label": "General Document",
            "filename": "test.jpg",
        }
        with patch("app.routers.doc_extract.DocOCRService") as MockService:
            instance = MockService.return_value
            instance.extract = AsyncMock(return_value=mock_result)

            # First upload
            resp1 = client.post(
                "/extract/upload",
                files={"file": ("test.jpg", BytesIO(content), "image/jpeg")},
                data={"doc_type": "general"},
            )
            assert resp1.status_code == 200

            # Second upload with same content
            resp2 = client.post(
                "/extract/upload",
                files={"file": ("test.jpg", BytesIO(content), "image/jpeg")},
                data={"doc_type": "general"},
            )
            assert resp2.status_code == 200
            assert resp2.json().get("duplicate") is True

        # Clean up
        doc_mod._processed_hashes.clear()

    def test_upload_empty_file_returns_400(self, client):
        """Uploading an empty file returns 400."""
        response = client.post(
            "/extract/upload",
            files={"file": ("empty.jpg", BytesIO(b""), "image/jpeg")},
            data={"doc_type": "passport"},
        )
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

    def test_upload_oversized_file_returns_413(self, client):
        """Uploading a file > 10MB returns 413."""
        big_content = b"x" * (11 * 1024 * 1024)  # 11MB
        with patch("app.routers.doc_extract.DocOCRService"):
            response = client.post(
                "/extract/upload",
                files={"file": ("big.jpg", BytesIO(big_content), "image/jpeg")},
                data={"doc_type": "passport"},
            )
        assert response.status_code == 413


@pytest.mark.integration
class TestUploadAndSync:
    """Tests for POST /extract/upload-and-sync."""

    def test_upload_and_sync_success(self, client):
        """Upload + sync with mocked OCR and GHL returns synced result."""
        mock_ghl = AsyncMock()
        mock_ghl.update_custom_fields.return_value = {"contact": {"id": "test-contact-123"}}
        mock_result = {
            "method": "fastmrz",
            "extracted_fields": {
                "full_name": "Jane Smith",
                "passport_number": "CD9876543",
                "date_of_birth": "1990-05-15",
            },
            "field_count": 3,
            "confidence": "high",
            "doc_type": "passport",
            "doc_type_label": "Passport",
            "filename": "passport.jpg",
        }
        with patch("app.routers.doc_extract.DocOCRService") as MockService, \
             patch("app.routers.doc_extract.GHLClient", return_value=mock_ghl):
            instance = MockService.return_value
            instance.extract = AsyncMock(return_value=mock_result)

            response = client.post(
                "/extract/upload-and-sync",
                files=_make_upload_file(),
                data={"contact_id": "test-contact-123", "doc_type": "passport"},
            )
        assert response.status_code == 200
        body = response.json()
        assert body["ghl_sync"] == "synced"
        assert "ghl_fields_updated" in body
        assert body["contact_id"] == "test-contact-123"

    def test_upload_and_sync_no_fields_extracted(self, client):
        """When OCR extracts no fields, sync is skipped."""
        mock_result = {
            "method": "claude",
            "extracted_fields": {},
            "field_count": 0,
            "confidence": "none",
            "doc_type": "general",
            "doc_type_label": "General Document",
            "filename": "unclear.jpg",
        }
        with patch("app.routers.doc_extract.DocOCRService") as MockService:
            instance = MockService.return_value
            instance.extract = AsyncMock(return_value=mock_result)

            response = client.post(
                "/extract/upload-and-sync",
                files=_make_upload_file(filename="unclear.jpg"),
                data={"contact_id": "test-contact-123", "doc_type": "general"},
            )
        assert response.status_code == 200
        body = response.json()
        assert body["ghl_sync"] == "skipped"

    def test_upload_and_sync_empty_file_returns_400(self, client):
        """Empty file returns 400 even on sync endpoint."""
        response = client.post(
            "/extract/upload-and-sync",
            files={"file": ("empty.jpg", BytesIO(b""), "image/jpeg")},
            data={"contact_id": "test-contact-123", "doc_type": "passport"},
        )
        assert response.status_code == 400
