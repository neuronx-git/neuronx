"""
Document OCR Extraction API

POST /extract/upload            — Upload document, extract fields via OCR
POST /extract/upload-and-sync   — Upload, extract, and sync fields to GHL contact
GET  /extract/types             — List supported document types

Hybrid approach:
- Passport: FastMRZ (free, unlimited, ~85-90% accuracy)
- All other docs: Claude API vision (pay per use, 95%+ accuracy)
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import hashlib
import logging

from app.services.doc_ocr_service import DocOCRService
from app.services.ghl_client import GHLClient
from app.utils.compliance_log import log_event

router = APIRouter()
logger = logging.getLogger("neuronx.doc_extract")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# In-memory dedup cache for file hashes (prevents re-processing identical uploads)
# Note: This cache is lost on Railway restart. For durability, check database
# processed_webhooks table with source="doc_extract" before OCR.
_processed_hashes: dict[str, dict] = {}


def _file_hash(contents: bytes) -> str:
    """SHA-256 hash for duplicate file detection."""
    return hashlib.sha256(contents).hexdigest()


@router.post("/upload")
async def extract_from_document(
    file: UploadFile = File(...),
    doc_type: Optional[str] = Form("auto"),
):
    """
    Upload a document and extract structured data.

    Supported types: passport, ielts, eca, employment_letter,
    marriage_certificate, bank_statement, police_clearance, general

    Set doc_type="auto" to auto-detect from filename.
    Duplicate files (same content hash) return cached results.
    """
    # Validate file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large. Max {MAX_FILE_SIZE // (1024*1024)}MB")

    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    # Duplicate file detection
    content_hash = _file_hash(contents)
    if content_hash in _processed_hashes:
        logger.info("Duplicate file detected (hash=%s), returning cached result", content_hash[:12])
        cached = _processed_hashes[content_hash].copy()
        cached["duplicate"] = True
        return cached

    service = DocOCRService()
    result = await service.extract(contents, file.filename or "document", doc_type)

    log_event("document_extracted", {
        "filename": file.filename,
        "doc_type": result.get("doc_type"),
        "method": result.get("method"),
        "field_count": result.get("field_count", 0),
        "confidence": result.get("confidence"),
    })

    # Cache for dedup (keep last 100 hashes)
    if len(_processed_hashes) > 100:
        oldest = next(iter(_processed_hashes))
        del _processed_hashes[oldest]
    _processed_hashes[content_hash] = result

    return result


@router.post("/upload-and-sync")
async def extract_and_sync_to_ghl(
    file: UploadFile = File(...),
    contact_id: str = Form(...),
    doc_type: Optional[str] = Form("auto"),
):
    """
    Upload document, extract fields via OCR, and sync extracted data to GHL contact.

    This wires OCR extraction into the GHL pipeline:
    1. Extract structured fields from document
    2. Map extracted fields to GHL custom field keys
    3. Update GHL contact with extracted data
    4. Return extraction result + sync status

    Used by: Typebot form file upload → auto-populate contact fields
    """
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large. Max {MAX_FILE_SIZE // (1024*1024)}MB")
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    # Extract
    service = DocOCRService()
    result = await service.extract(contents, file.filename or "document", doc_type)

    extracted = result.get("extracted_fields", {})
    if not extracted:
        return {**result, "ghl_sync": "skipped", "reason": "no fields extracted"}

    # Map OCR fields → GHL custom field keys
    ocr_to_ghl = {
        # Passport
        "full_name": "full_name",
        "date_of_birth": "date_of_birth",
        "passport_number": "passport_number",
        "passport_expiry": "passport_expiry",
        "country_of_citizenship": "country_of_citizenship",
        "nationality": "country_of_citizenship",
        "sex": "sex",
        # IELTS
        "overall_score": "language_overall_score",
        "listening_score": "language_listening",
        "reading_score": "language_reading",
        "writing_score": "language_writing",
        "speaking_score": "language_speaking",
        "test_type": "language_test_type",
        # ECA
        "credential_level": "education_level",
        "canadian_equivalent": "eca_canadian_equivalent",
        "reference_number": "eca_reference_number",
        # Employment
        "employer_name": "employer_name",
        "job_title": "job_title",
        "noc_code": "noc_code",
        # Marriage
        "marriage_date": "marriage_date",
        # Bank
        "balance": "settlement_funds",
    }

    ghl_fields = {}
    for ocr_key, ghl_key in ocr_to_ghl.items():
        value = extracted.get(ocr_key)
        if value is not None and value != "" and value != "null":
            ghl_fields[ghl_key] = str(value)

    sync_status = "no_fields_mapped"
    if ghl_fields:
        try:
            ghl = GHLClient()
            await ghl.update_custom_fields(contact_id, ghl_fields)
            sync_status = "synced"
            logger.info("OCR→GHL sync: %d fields for contact %s", len(ghl_fields), contact_id)
        except Exception as e:
            logger.warning("OCR→GHL sync failed for %s: %s", contact_id, e)
            sync_status = f"error: {e}"

    log_event("document_extracted_and_synced", {
        "contact_id": contact_id,
        "filename": file.filename,
        "doc_type": result.get("doc_type"),
        "fields_extracted": result.get("field_count", 0),
        "fields_synced": len(ghl_fields),
        "sync_status": sync_status,
    })

    return {
        **result,
        "ghl_sync": sync_status,
        "ghl_fields_updated": ghl_fields,
        "contact_id": contact_id,
    }


@router.post("/from-url")
async def extract_from_url(
    file_url: str = Form(...),
    doc_type: Optional[str] = Form("passport"),
    contact_id: Optional[str] = Form(None),
):
    """
    Download a document from a URL (e.g. MinIO) and extract fields via OCR.
    Used by Typebot webhook after passport upload — the file is stored in MinIO,
    and this endpoint fetches it, runs OCR, and returns extracted data.

    If contact_id is provided, also syncs extracted fields to GHL.
    """
    import httpx as hx

    try:
        async with hx.AsyncClient(timeout=30.0) as http:
            resp = await http.get(file_url)
            if resp.status_code != 200:
                return {"error": f"Could not download file: HTTP {resp.status_code}", "url": file_url}
            contents = resp.content
    except Exception as e:
        return {"error": f"Download failed: {str(e)}", "url": file_url}

    if not contents or len(contents) < 100:
        return {"error": "File is empty or too small", "url": file_url}

    # Extract filename from URL
    filename = file_url.split("/")[-1] if "/" in file_url else "document"

    service = DocOCRService()
    result = await service.extract(contents, filename, doc_type)

    log_event("document_extracted_from_url", {
        "url": file_url[:100],
        "doc_type": result.get("doc_type"),
        "field_count": result.get("field_count", 0),
        "contact_id": contact_id,
    })

    # Optionally sync to GHL
    if contact_id and result.get("extracted_fields"):
        from app.services.ghl_client import GHLClient
        ocr_to_ghl = {
            "full_name": "full_name", "date_of_birth": "date_of_birth",
            "passport_number": "passport_number", "passport_expiry": "passport_expiry",
            "country_of_citizenship": "country_of_citizenship", "sex": "sex",
            "overall_score": "language_overall_score",
            "employer_name": "employer_name", "job_title": "job_title",
            "noc_code": "noc_code", "balance": "settlement_funds",
            "credential_level": "education_level", "marriage_date": "marriage_date",
        }
        ghl_fields = {}
        for ocr_key, ghl_key in ocr_to_ghl.items():
            val = result["extracted_fields"].get(ocr_key)
            if val:
                ghl_fields[ghl_key] = str(val)
        if ghl_fields:
            try:
                ghl = GHLClient()
                await ghl.update_custom_fields(contact_id, ghl_fields)
                result["ghl_sync"] = "synced"
                result["ghl_fields_updated"] = ghl_fields
            except Exception as e:
                result["ghl_sync"] = f"error: {e}"

    # Flatten extracted_fields to top level for Typebot variable auto-mapping.
    # Typebot maps response JSON keys matching variable names automatically.
    # Variable names: full_name, date_of_birth, passport_number, passport_expiry,
    # country_of_citizenship, ocr_listening_score, ocr_employer_name, etc.
    extracted = result.get("extracted_fields", {})
    response = {**result}
    # Passport fields → direct variable names
    for key in ("full_name", "date_of_birth", "passport_number", "passport_expiry",
                "country_of_citizenship", "nationality", "sex"):
        if extracted.get(key):
            response[key] = str(extracted[key])
    # IELTS → prefixed variables
    for key in ("listening_score", "reading_score", "writing_score", "speaking_score", "overall_score"):
        if extracted.get(key):
            response[f"ocr_{key}"] = str(extracted[key])
    # ECA
    for key in ("credential_level", "canadian_equivalent", "reference_number"):
        if extracted.get(key):
            response[f"ocr_{key}" if key != "credential_level" else "ocr_credential_level"] = str(extracted[key])
    # Employment
    for key in ("employer_name", "job_title", "noc_code"):
        if extracted.get(key):
            response[f"ocr_{key}"] = str(extracted[key])
    # Bank
    if extracted.get("balance"):
        response["ocr_settlement_funds"] = str(extracted["balance"])

    return response


@router.get("/types")
async def list_document_types():
    """List all supported document types for extraction."""
    service = DocOCRService()
    return {
        "supported_types": service.get_supported_types(),
        "note": "Use doc_type='auto' to auto-detect from filename, or specify explicitly.",
    }
