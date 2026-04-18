"""
Case Documents Viewer — Server-Rendered HTML UI
==================================================
Serves the RCIC-facing case viewer pages. This is what RCICs see when
they click the `case_documents_url` link from GHL.

Routes:
  GET  /cases/{case_id}/viewer                         — full case view
  GET  /cases/{case_id}/documents/viewer               — document gallery only
  GET  /cases/{case_id}/documents/{doc_id}/download    — presigned download
  GET  /cases/{case_id}/viewer/data                    — JSON (for JS / testing)

Design:
  • Brand colors: navy #0F172A, orange #E8380D
  • Inter font (system fallback)
  • Server-rendered Jinja2 — no SPA
  • Tailwind via CDN (inline), ~50 lines JS total

Auth (placeholder — harden later):
  • Case must exist in DB → 404 if not found
  • Presigned download URLs expire in 15 min (HMAC signed)

Data sources (graceful fallback to placeholder data):
  • app.services.case_service.CaseService.get_case_by_id
  • /cases/{case_id}/documents + /checklist (from blocker #1)
  • /activities?contact_id=...
"""

from __future__ import annotations

import hmac
import hashlib
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

logger = logging.getLogger("neuronx.case_viewer")

router = APIRouter()

# Templates dir is neuronx-api/templates (same level as main.py)
_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
templates = Jinja2Templates(directory=_TEMPLATES_DIR)


# ── Helpers ────────────────────────────────────────────────────────────

def _sign_download(case_id: str, doc_id: str, expires: int) -> str:
    """HMAC-sign a download token. Expires is unix timestamp."""
    secret = os.getenv("ADMIN_API_KEY", "neuronx-admin-dev")
    msg = f"{case_id}|{doc_id}|{expires}".encode()
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()[:32]


def _verify_download(case_id: str, doc_id: str, expires: int, sig: str) -> bool:
    if expires < int(time.time()):
        return False
    expected = _sign_download(case_id, doc_id, expires)
    return hmac.compare_digest(expected, sig)


def _presigned_url(case_id: str, doc_id: str, ttl_sec: int = 900) -> str:
    """Returns a 15-min presigned download URL."""
    expires = int(time.time()) + ttl_sec
    sig = _sign_download(case_id, doc_id, expires)
    return f"/cases/{case_id}/documents/{doc_id}/download?expires={expires}&sig={sig}"


def _stage_color(stage: str) -> str:
    """Map case stage → Tailwind color classes."""
    mapping = {
        "onboarding":      ("bg-slate-100", "text-slate-700"),
        "doc_collection":  ("bg-amber-100", "text-amber-800"),
        "docs_complete":   ("bg-emerald-100", "text-emerald-800"),
        "form_prep":       ("bg-blue-100", "text-blue-800"),
        "under_review":    ("bg-indigo-100", "text-indigo-800"),
        "submitted":       ("bg-violet-100", "text-violet-800"),
        "processing":      ("bg-cyan-100", "text-cyan-800"),
        "rfi":             ("bg-orange-100", "text-orange-800"),
        "decision":        ("bg-fuchsia-100", "text-fuchsia-800"),
        "closed":          ("bg-gray-100", "text-gray-700"),
    }
    bg, fg = mapping.get(stage, ("bg-slate-100", "text-slate-700"))
    return f"{bg} {fg}"


def _days_between(a: Optional[datetime], b: Optional[datetime]) -> int:
    if not a or not b:
        return 0
    try:
        return max(0, (b - a).days)
    except Exception:
        return 0


async def _load_case_context(case_id: str) -> dict[str, Any]:
    """
    Load full context for the viewer. Gracefully falls back to placeholder
    data when underlying services are unavailable (dev / no-DB mode).
    Raises HTTPException(404) only when we can positively determine the
    case does not exist.
    """
    case: Optional[dict] = None
    try:
        from app.services.case_service import CaseService
        service = CaseService()
        case = await service.get_case_by_id(case_id)
    except Exception as e:
        logger.info("CaseService unavailable, using placeholder (%s): %s", case_id, e)
        case = None

    # Placeholder / demo fallback — lets the viewer render for screenshots + UAT
    if not case:
        if case_id.startswith("NX-"):
            case = _demo_case(case_id)
        else:
            raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found")

    documents = case.get("documents") or _demo_documents(case_id)
    checklist = case.get("checklist") or _demo_checklist()
    activities = case.get("activities") or _demo_activities(case)

    # Attach presigned URLs to each doc
    for doc in documents:
        doc["download_url"] = _presigned_url(case_id, doc.get("id", "unknown"))

    received = sum(1 for c in checklist if c.get("received"))
    required_total = sum(1 for c in checklist if c.get("required"))
    required_received = sum(1 for c in checklist if c.get("required") and c.get("received"))
    progress_pct = int((required_received / required_total) * 100) if required_total else 0

    now = datetime.now(timezone.utc)
    stage_entered = _parse_ts(case.get("stage_entered_at"))
    deadline = _parse_ts(case.get("submission_deadline"))

    days_in_stage = _days_between(stage_entered, now) if stage_entered else 0
    days_to_deadline = _days_between(now, deadline) if deadline else None

    if days_to_deadline is not None and days_to_deadline < 0:
        sla_status = {"label": f"{abs(days_to_deadline)} days overdue", "ok": False}
    elif days_to_deadline is not None and days_to_deadline <= 2:
        sla_status = {"label": f"{days_to_deadline}d — at risk", "ok": False}
    else:
        sla_status = {"label": "On track", "ok": True}

    stage = case.get("current_stage") or case.get("stage") or "onboarding"
    rcic_name = case.get("assigned_rcic") or "Unassigned"
    rcic_initial = (rcic_name[0] if rcic_name else "?").upper()

    ghl_location = os.getenv("GHL_LOCATION_ID", "")
    contact_id = case.get("contact_id", "")
    ghl_deeplink = (
        f"https://app.gohighlevel.com/v2/location/{ghl_location}/contacts/detail/{contact_id}"
        if ghl_location and contact_id else ""
    )

    return {
        "case": case,
        "case_id": case_id,
        "stage": stage,
        "stage_label": stage.replace("_", " ").title(),
        "stage_color": _stage_color(stage),
        "rcic_name": rcic_name,
        "rcic_initial": rcic_initial,
        "ghl_deeplink": ghl_deeplink,
        "documents": documents,
        "checklist": checklist,
        "activities": activities,
        "stats": {
            "received": received,
            "required_total": required_total,
            "required_received": required_received,
            "progress_pct": progress_pct,
            "days_in_stage": days_in_stage,
            "days_to_deadline": days_to_deadline,
            "sla": sla_status,
        },
    }


def _parse_ts(v: Any) -> Optional[datetime]:
    if not v:
        return None
    if isinstance(v, datetime):
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)
    try:
        return datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except Exception:
        return None


# ── Demo / placeholder data ────────────────────────────────────────────

def _demo_case(case_id: str) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "case_id": case_id,
        "contact_id": "demo-contact-id",
        "client_name": "Priya Sharma",
        "program_type": "Express Entry",
        "current_stage": "doc_collection",
        "assigned_rcic": "Ranjan Singh",
        "stage_entered_at": (now.replace(microsecond=0)).isoformat(),
        "submission_deadline": now.replace(microsecond=0).isoformat(),
        "created_at": now.isoformat(),
    }


def _demo_documents(case_id: str) -> list[dict]:
    return [
        {"id": "doc-001", "name": "Passport.pdf", "type": "Passport", "mime": "application/pdf",
         "size_bytes": 1_200_000, "uploaded_at": "2026-04-10T14:22:00Z", "uploaded_by": "Priya Sharma",
         "status": "received"},
        {"id": "doc-002", "name": "IELTS_Results.pdf", "type": "Language Test", "mime": "application/pdf",
         "size_bytes": 420_000, "uploaded_at": "2026-04-11T09:01:00Z", "uploaded_by": "Priya Sharma",
         "status": "received"},
        {"id": "doc-003", "name": "ECA_WES.pdf", "type": "ECA", "mime": "application/pdf",
         "size_bytes": 800_000, "uploaded_at": "2026-04-12T18:40:00Z", "uploaded_by": "Priya Sharma",
         "status": "received"},
    ]


def _demo_checklist() -> list[dict]:
    return [
        {"name": "Valid passport (all pages)", "required": True, "received": True, "filename": "Passport.pdf"},
        {"name": "IELTS / CELPIP language results", "required": True, "received": True, "filename": "IELTS_Results.pdf"},
        {"name": "ECA (WES or equivalent)", "required": True, "received": True, "filename": "ECA_WES.pdf"},
        {"name": "Reference letters (last 10 years)", "required": True, "received": False},
        {"name": "Police clearance certificates", "required": True, "received": False},
        {"name": "Proof of funds (6 months statements)", "required": True, "received": False},
        {"name": "Marriage certificate (if applicable)", "required": False, "received": False},
        {"name": "Birth certificates of dependents", "required": False, "received": False},
    ]


def _demo_activities(case: dict) -> list[dict]:
    return [
        {"ts": "2026-04-09T12:00:00Z", "icon": "play", "description": "Case initiated after retainer signed", "actor": "system"},
        {"ts": "2026-04-09T12:05:00Z", "icon": "mail", "description": "Welcome email sent to client", "actor": "WF-CP-01"},
        {"ts": "2026-04-10T14:22:00Z", "icon": "upload", "description": "Client uploaded Passport.pdf", "actor": case.get("client_name", "Client")},
        {"ts": "2026-04-11T09:01:00Z", "icon": "upload", "description": "Client uploaded IELTS_Results.pdf", "actor": case.get("client_name", "Client")},
        {"ts": "2026-04-12T18:40:00Z", "icon": "upload", "description": "Client uploaded ECA_WES.pdf", "actor": case.get("client_name", "Client")},
        {"ts": "2026-04-13T10:00:00Z", "icon": "note", "description": "RCIC reviewed uploads, flagged 3 missing items", "actor": case.get("assigned_rcic", "RCIC")},
    ]


# ── Routes ─────────────────────────────────────────────────────────────

@router.get("/{case_id}/viewer", response_class=HTMLResponse)
async def case_viewer(request: Request, case_id: str):
    """Full case viewer — header, timeline, documents, checklist, stats."""
    ctx = await _load_case_context(case_id)
    ctx["request"] = request
    ctx["view_mode"] = "full"
    return templates.TemplateResponse("case_viewer.html", ctx)


@router.get("/{case_id}/documents/viewer", response_class=HTMLResponse)
async def documents_viewer(request: Request, case_id: str):
    """Document-gallery-only view (embedded in modals etc.)."""
    ctx = await _load_case_context(case_id)
    ctx["request"] = request
    ctx["view_mode"] = "documents"
    return templates.TemplateResponse("case_viewer.html", ctx)


@router.get("/{case_id}/viewer/data")
async def case_viewer_data(case_id: str):
    """JSON payload of viewer data — used by tests and small JS refresh calls."""
    ctx = await _load_case_context(case_id)
    ctx.pop("request", None)

    # Recursively coerce datetimes to ISO strings for safe JSON serialization
    def _coerce(v):
        if isinstance(v, datetime):
            return v.isoformat()
        if isinstance(v, dict):
            return {k: _coerce(x) for k, x in v.items()}
        if isinstance(v, list):
            return [_coerce(x) for x in v]
        return v

    return JSONResponse(_coerce(ctx))


@router.get("/{case_id}/documents/{doc_id}/download")
async def download_document(case_id: str, doc_id: str, expires: int, sig: str):
    """
    Presigned download endpoint. Verifies HMAC signature + expiry,
    then redirects to the underlying storage URL (or returns 404/410).
    """
    if not _verify_download(case_id, doc_id, expires, sig):
        raise HTTPException(status_code=410, detail="Download link expired or invalid")

    # Attempt to resolve underlying storage URL via document service.
    storage_url: Optional[str] = None
    try:
        from app.services.document_service import DocumentService  # type: ignore
        svc = DocumentService()
        if hasattr(svc, "get_download_url"):
            storage_url = await svc.get_download_url(case_id=case_id, doc_id=doc_id)  # type: ignore
    except Exception as e:
        logger.info("DocumentService.get_download_url unavailable (%s)", e)

    if storage_url:
        return RedirectResponse(url=storage_url, status_code=302)

    # Fallback for dev: return a JSON stub so link isn't broken
    return JSONResponse(
        {"case_id": case_id, "doc_id": doc_id, "note": "Storage backend not configured — link valid, no file served."},
        status_code=200,
    )
