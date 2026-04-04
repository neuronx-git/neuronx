"""
Documenso E-Signature Client

Integrates with self-hosted Documenso (Railway) for retainer signing.

Flow:
1. FastAPI generates retainer.docx via docxtpl
2. Convert .docx → PDF (LibreOffice headless or python-docx2pdf)
3. Upload PDF to Documenso API
4. Documenso emails client with signing link
5. Client signs digitally
6. Documenso webhook → FastAPI → adds nx:retainer:signed tag in GHL
7. WF-10 triggers → contact moves to RETAINED

API docs: https://docs.documenso.com/developers/public-api
"""

import logging
import httpx
from typing import Optional
from datetime import datetime, timezone

from app.config import settings

logger = logging.getLogger("neuronx.documenso")


class DocumensoClient:
    """REST client for Documenso e-signature API."""

    def __init__(self):
        self.base_url = settings.documenso_url.rstrip("/") if settings.documenso_url else ""
        self.api_key = settings.documenso_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def is_configured(self) -> bool:
        return bool(self.base_url and self.api_key)

    async def create_document(self, title: str, pdf_bytes: bytes,
                                signer_email: str, signer_name: str) -> Optional[dict]:
        """
        Upload a PDF to Documenso and create a signing request.

        Returns dict with document_id and signing_url, or None on failure.
        """
        if not self.is_configured():
            logger.warning("Documenso not configured. Set DOCUMENSO_URL and DOCUMENSO_API_KEY.")
            return None

        async with httpx.AsyncClient(timeout=30.0) as client:
            # Step 1: Create document
            import base64
            create_payload = {
                "title": title,
                "recipients": [
                    {
                        "email": signer_email,
                        "name": signer_name,
                        "role": "SIGNER",
                    }
                ],
                "meta": {
                    "message": f"Please review and sign the attached {title}.",
                    "subject": f"{title} — Ready for Your Signature",
                },
            }

            try:
                # Create the document envelope
                resp = await client.post(
                    f"{self.base_url}/api/v1/documents",
                    headers=self.headers,
                    json=create_payload,
                )
                resp.raise_for_status()
                doc_data = resp.json()
                document_id = doc_data.get("id")

                if not document_id:
                    logger.error("Documenso returned no document ID")
                    return None

                # Step 2: Upload the PDF file
                upload_resp = await client.post(
                    f"{self.base_url}/api/v1/documents/{document_id}/fields",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files={"file": (f"{title}.pdf", pdf_bytes, "application/pdf")},
                )

                # Step 3: Send for signing
                send_resp = await client.post(
                    f"{self.base_url}/api/v1/documents/{document_id}/send",
                    headers=self.headers,
                )

                logger.info("Documenso document created: %s for %s", document_id, signer_email)

                return {
                    "document_id": str(document_id),
                    "signer_email": signer_email,
                    "status": "sent",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }

            except httpx.HTTPError as e:
                logger.error("Documenso API error: %s", e)
                return None

    async def get_document_status(self, document_id: str) -> Optional[dict]:
        """Check the signing status of a document."""
        if not self.is_configured():
            return None

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                resp = await client.get(
                    f"{self.base_url}/api/v1/documents/{document_id}",
                    headers=self.headers,
                )
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError as e:
                logger.error("Documenso status check failed: %s", e)
                return None
