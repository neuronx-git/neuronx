"""
Dependents API
CRUD operations for case dependents (spouse, children, parents).

PostgreSQL is authoritative for dependent data — GHL has no relational model
for multi-dependent management.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
import logging

from app.database import is_db_configured, get_session
from app.utils.compliance_log import log_event

router = APIRouter()
logger = logging.getLogger("neuronx.dependents")

RelationshipType = Literal["spouse", "child", "parent", "sibling", "other"]
DocsStatusType = Literal["pending", "partial", "complete"]

# Allowed columns for dynamic UPDATE (prevents SQL injection via keys)
ALLOWED_UPDATE_COLUMNS = {
    "full_name", "relationship", "date_of_birth",
    "passport_number", "passport_expiry", "docs_status", "notes",
}


class DependentCreate(BaseModel):
    case_id: str = Field(..., min_length=1, max_length=50)
    contact_id: str = Field(..., min_length=1, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=200)
    relationship: RelationshipType
    date_of_birth: Optional[str] = Field(None, max_length=20)
    passport_number: Optional[str] = Field("", max_length=50)
    passport_expiry: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = Field("", max_length=2000)


class DependentUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    relationship: Optional[RelationshipType] = None
    date_of_birth: Optional[str] = Field(None, max_length=20)
    passport_number: Optional[str] = Field(None, max_length=50)
    passport_expiry: Optional[str] = Field(None, max_length=20)
    docs_status: Optional[DocsStatusType] = None
    notes: Optional[str] = Field(None, max_length=2000)


@router.post("/")
async def create_dependent(data: DependentCreate):
    """Add a dependent to a case."""
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    # Verify case exists before inserting (prevents orphan FK errors returning 500)
    from sqlalchemy import text
    try:
        async for session in get_session():
            check = await session.execute(
                text("SELECT 1 FROM cases WHERE case_id = :cid"),
                {"cid": data.case_id},
            )
            if check.scalar() is None:
                raise HTTPException(status_code=404, detail=f"Case '{data.case_id}' not found")

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
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to add dependent to case %s: %s", data.case_id, e)
        raise HTTPException(status_code=500, detail="Failed to add dependent")

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

    raw_updates = {k: v for k, v in data.model_dump().items() if v is not None}
    # Whitelist: only allow known columns (defense-in-depth vs SQL injection)
    updates = {k: v for k, v in raw_updates.items() if k in ALLOWED_UPDATE_COLUMNS}
    if not updates:
        return {"status": "ok", "message": "No fields to update"}

    from sqlalchemy import text
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    params = {**updates, "dep_id": dependent_id}

    try:
        async for session in get_session():
            check = await session.execute(
                text("SELECT 1 FROM dependents WHERE id = :dep_id"),
                {"dep_id": dependent_id},
            )
            if check.scalar() is None:
                raise HTTPException(status_code=404, detail=f"Dependent {dependent_id} not found")

            await session.execute(
                text(f"UPDATE dependents SET {set_clause} WHERE id = :dep_id"),
                params,
            )
            await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update dependent %s: %s", dependent_id, e)
        raise HTTPException(status_code=500, detail="Failed to update dependent")

    return {"status": "ok", "message": f"Dependent {dependent_id} updated", "fields_updated": list(updates.keys())}


@router.delete("/{dependent_id}")
async def delete_dependent(dependent_id: int):
    """Remove a dependent from a case."""
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    from sqlalchemy import text
    try:
        async for session in get_session():
            result = await session.execute(
                text("DELETE FROM dependents WHERE id = :dep_id"),
                {"dep_id": dependent_id},
            )
            await session.commit()
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Dependent {dependent_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete dependent %s: %s", dependent_id, e)
        raise HTTPException(status_code=500, detail="Failed to delete dependent")

    return {"status": "ok", "message": f"Dependent {dependent_id} deleted"}
