"""
E-Signature Endpoints (Documenso Integration)
POST /signatures/send      — Generate retainer + send for e-signing
POST /signatures/webhook   — Documenso webhook (signature completed)
GET  /signatures/status     — Check signing status
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging

from app.services.document_service import DocumentService
from app.services.documenso_client import DocumensoClient
from app.services.ghl_client import GHLClient
from app.database import is_db_configured

router = APIRouter()
logger = logging.getLogger("neuronx.signatures")


class SendRetainerRequest(BaseModel):
    contact_id: str
    retainer_amount: float = 3500.0
    payment_schedule: str = "50% upfront, 50% on submission"


class DocumensoWebhook(BaseModel):
    event: str  # DOCUMENT_SIGNED, DOCUMENT_COMPLETED, etc.
    data: dict = Field(default_factory=dict)


@router.post("/send")
async def send_retainer_for_signing(payload: SendRetainerRequest):
    """
    Generate retainer agreement and send via Documenso for e-signing.
    Flow: Generate .docx → (convert to PDF) → Upload to Documenso → Email to client
    """
    documenso = DocumensoClient()
    if not documenso.is_configured():
        raise HTTPException(
            status_code=503,
            detail="Documenso not configured. Set DOCUMENSO_URL and DOCUMENSO_API_KEY env vars."
        )

    # Generate retainer .docx
    doc_service = DocumentService()
    docx_bytes = await doc_service.generate_retainer(
        contact_id=payload.contact_id,
        retainer_amount=payload.retainer_amount,
        payment_schedule=payload.payment_schedule,
    )

    if not docx_bytes:
        raise HTTPException(status_code=500, detail="Failed to generate retainer document")

    # Get client info for signing
    ghl = GHLClient()
    contact = await ghl.get_contact(payload.contact_id)
    client_name = f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip()
    client_email = contact.get("email", "")

    if not client_email:
        raise HTTPException(status_code=400, detail="Contact has no email address")

    # Send to Documenso
    # NOTE: For v1, we send the .docx bytes directly.
    # For production, convert to PDF first via LibreOffice headless.
    result = await documenso.create_document(
        title=f"Retainer Agreement — {client_name}",
        pdf_bytes=docx_bytes,  # Documenso accepts PDF; convert in production
        signer_email=client_email,
        signer_name=client_name,
    )

    if not result:
        raise HTTPException(status_code=502, detail="Documenso API call failed")

    # Record in database if available
    if is_db_configured():
        from app.services.sync_service import SyncService
        sync = SyncService()
        await sync.record_activity(
            contact_id=payload.contact_id,
            activity_type="retainer_sent_for_signing",
            detail=f"Sent to {client_email} via Documenso",
            metadata=result,
        )

    # Add tag in GHL
    await ghl.add_tag(payload.contact_id, "nx:retainer:sent")

    return {
        "contact_id": payload.contact_id,
        "signer_email": client_email,
        "documenso_document_id": result.get("document_id"),
        "status": "sent",
    }


@router.post("/webhook")
async def documenso_webhook(payload: DocumensoWebhook):
    """
    Handle Documenso webhook events.
    On DOCUMENT_COMPLETED: add nx:retainer:signed tag in GHL → triggers WF-10.
    """
    event = payload.event
    data = payload.data

    logger.info("Documenso webhook: %s", event)

    if event in ("DOCUMENT_SIGNED", "DOCUMENT_COMPLETED"):
        # Find the contact by signer email
        signer_email = ""
        recipients = data.get("recipients", [])
        if recipients:
            signer_email = recipients[0].get("email", "")

        if signer_email:
            ghl = GHLClient()
            # Search for contact by email
            contacts = await ghl.search_contacts(signer_email, limit=1)
            contact_list = contacts.get("contacts", [])

            if contact_list:
                contact_id = contact_list[0]["id"]
                await ghl.add_tag(contact_id, "nx:retainer:signed")
                await ghl.add_tag(contact_id, "nx:payment:received")

                logger.info("Retainer signed by %s (contact %s) — tags added", signer_email, contact_id)

                # Record in database
                if is_db_configured():
                    from app.services.sync_service import SyncService
                    sync = SyncService()
                    await sync.record_activity(
                        contact_id=contact_id,
                        activity_type="retainer_signed",
                        detail=f"Signed by {signer_email} via Documenso",
                        metadata=data,
                    )

                return {"status": "processed", "contact_id": contact_id, "action": "nx:retainer:signed added"}

        logger.warning("Could not find contact for Documenso signer: %s", signer_email)
        return {"status": "unmatched", "signer_email": signer_email}

    return {"status": "ignored", "event": event}


@router.get("/status/{document_id}")
async def check_signature_status(document_id: str):
    """Check the current signing status of a document in Documenso."""
    documenso = DocumensoClient()
    if not documenso.is_configured():
        raise HTTPException(status_code=503, detail="Documenso not configured")

    result = await documenso.get_document_status(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found in Documenso")

    return result
