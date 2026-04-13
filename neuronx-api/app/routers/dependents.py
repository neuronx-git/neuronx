"""
Dependents API
CRUD operations for case dependents (spouse, children, parents).

PostgreSQL is authoritative for dependent data — GHL has no relational model
for multi-dependent management.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging

from app.database import is_db_configured, get_session
from app.utils.compliance_log import log_event

router = APIRouter()
logger = logging.getLogger("neuronx.dependents")


class DependentCreate(BaseModel):
    case_id: str
    contact_id: str
    full_name: str
    relationship: str  # spouse, child, parent
    date_of_birth: Optional[str] = None
    passport_number: Optional[str] = ""
    passport_expiry: Optional[str] = None
    notes: Optional[str] = ""


class DependentUpdate(BaseModel):
    full_name: Optional[str] = None
    relationship: Optional[str] = None
    date_of_birth: Optional[str] = None
    passport_number: Optional[str] = None
    passport_expiry: Optional[str] = None
    docs_status: Optional[str] = None  # pending, partial, complete
    notes: Optional[str] = None


@router.post("/")
async def create_dependent(data: DependentCreate):
    """Add a dependent to a case."""
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    from sqlalchemy import text
    async for session in get_session():
        await session.execute(
            text(
                "INSERT INTO dependents (case_id, contact_id, full_name, relationship, "
                "passport_number, notes) "
                "VALUES (:case_id, :contact_id, :name, :rel, :passport, :notes)"
            ),
            {
                "case_id": data.case_id,
                "contact_id": data.contact_id,
                "name": data.full_name,
                "rel": data.relationship,
                "passport": data.passport_number or "",
                "notes": data.notes or "",
            },
        )
        await session.commit()

    log_event("dependent_added", {
        "case_id": data.case_id,
        "contact_id": data.contact_id,
        "name": data.full_name,
        "relationship": data.relationship,
    })

    return {"status": "ok", "message": f"Dependent '{data.full_name}' added to case {data.case_id}"}


@router.get("/{case_id}")
async def list_dependents(case_id: str):
    """List all dependents for a case."""
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    from sqlalchemy import text
    async for session in get_session():
        result = await session.execute(
            text("SELECT id, full_name, relationship, passport_number, docs_status, notes, created_at "
                 "FROM dependents WHERE case_id = :case_id ORDER BY created_at"),
            {"case_id": case_id},
        )
        rows = result.mappings().all()

    dependents = [
        {
            "id": r["id"],
            "full_name": r["full_name"],
            "relationship": r["relationship"],
            "passport_number": r["passport_number"],
            "docs_status": r["docs_status"],
            "notes": r["notes"],
            "created_at": r["created_at"].isoformat() if r["created_at"] else None,
        }
        for r in rows
    ]

    return {"case_id": case_id, "dependents": dependents, "count": len(dependents)}


@router.put("/{dependent_id}")
async def update_dependent(dependent_id: int, data: DependentUpdate):
    """Update a dependent's information."""
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    if not updates:
        return {"status": "ok", "message": "No fields to update"}

    from sqlalchemy import text
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    updates["dep_id"] = dependent_id

    async for session in get_session():
        await session.execute(
            text(f"UPDATE dependents SET {set_clause} WHERE id = :dep_id"),
            updates,
        )
        await session.commit()

    return {"status": "ok", "message": f"Dependent {dependent_id} updated", "fields_updated": list(updates.keys())}


@router.delete("/{dependent_id}")
async def delete_dependent(dependent_id: int):
    """Remove a dependent from a case."""
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    from sqlalchemy import text
    async for session in get_session():
        await session.execute(
            text("DELETE FROM dependents WHERE id = :dep_id"),
            {"dep_id": dependent_id},
        )
        await session.commit()

    return {"status": "ok", "message": f"Dependent {dependent_id} deleted"}
