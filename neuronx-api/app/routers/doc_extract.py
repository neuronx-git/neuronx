"""
Document OCR Extraction API

POST /extract/upload    — Upload document, extract fields via OCR
GET  /extract/types     — List supported document types
POST /extract/passport  — Passport-specific extraction (FastMRZ)

Hybrid approach:
- Passport: FastMRZ (free, unlimited, ~85-90% accuracy)
- All other docs: Claude API vision (pay per use, 95%+ accuracy)
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import logging

from app.services.doc_ocr_service import DocOCRService
from app.utils.compliance_log import log_event

router = APIRouter()
logger = logging.getLogger("neuronx.doc_extract")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


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
    """
    # Validate file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large. Max {MAX_FILE_SIZE // (1024*1024)}MB")

    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    service = DocOCRService()
    result = await service.extract(contents, file.filename or "document", doc_type)

    log_event("document_extracted", {
        "filename": file.filename,
        "doc_type": result.get("doc_type"),
        "method": result.get("method"),
        "field_count": result.get("field_count", 0),
        "confidence": result.get("confidence"),
    })

    return result


@router.get("/types")
async def list_document_types():
    """List all supported document types for extraction."""
    service = DocOCRService()
    return {
        "supported_types": service.get_supported_types(),
        "note": "Use doc_type='auto' to auto-detect from filename, or specify explicitly.",
    }
