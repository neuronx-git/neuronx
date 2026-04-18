"""
User (Team / RCIC) Endpoints

GET  /users/                    — List all users (filter by role / active)
GET  /users/{user_id}           — Get one user
GET  /users/{user_id}/cases     — Cases assigned to this user
POST /users/sync-from-ghl       — Admin: re-sync roster from GHL (X-Admin-Key)

The users table is a mirror of the GHL team; use `sync-from-ghl` after GHL
roster changes to pull the latest.
"""

import logging
import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Header, Query

from app import database
from app.services.user_sync_service import UserSyncService

router = APIRouter()
logger = logging.getLogger("neuronx.users")


def _serialize_user(u) -> dict:
    return {
        "id": u.id,
        "email": u.email,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "full_name": u.full_name,
        "phone": u.phone,
        "role": u.role,
        "rcic_license": u.rcic_license,
        "is_active": u.is_active,
        "max_concurrent_cases": u.max_concurrent_cases,
        "ghl_user_id": u.ghl_user_id,
        "hire_date": u.hire_date.isoformat() if u.hire_date else None,
        "synced_at": u.synced_at.isoformat() if u.synced_at else None,
    }


@router.get("/")
async def list_users(
    role: Optional[str] = Query(None, description="Filter by role code"),
    active_only: bool = Query(True),
    limit: int = Query(100, ge=1, le=500),
):
    """List users, optionally filtered by role and active flag."""
    if not database.async_session_factory:
        return {"database": "not configured", "users": []}

    from app.models.db_models import User
    from sqlalchemy import select

    async with database.async_session_factory() as session:
        q = select(User).order_by(User.full_name).limit(limit)
        if role:
            q = q.where(User.role == role)
        if active_only:
            q = q.where(User.is_active == True)  # noqa: E712
        result = await session.execute(q)
        users = result.scalars().all()

    return {"count": len(users), "users": [_serialize_user(u) for u in users]}


@router.get("/{user_id}")
async def get_user(user_id: str):
    """Get a single user by GHL user ID."""
    if not database.async_session_factory:
        raise HTTPException(status_code=503, detail="Database not configured")

    from app.models.db_models import User
    from sqlalchemy import select

    async with database.async_session_factory() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    return _serialize_user(user)


@router.get("/{user_id}/cases")
async def list_cases_for_user(
    user_id: str,
    include_closed: bool = Query(False),
    limit: int = Query(100, ge=1, le=500),
):
    """List cases assigned to a given user."""
    if not database.async_session_factory:
        raise HTTPException(status_code=503, detail="Database not configured")

    from app.models.db_models import Case, User
    from sqlalchemy import select

    async with database.async_session_factory() as session:
        # Confirm user exists so callers get a clean 404 vs an empty list
        user = (await session.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")

        q = select(Case).where(Case.assigned_rcic_id == user_id).order_by(Case.created_at.desc()).limit(limit)
        if not include_closed:
            q = q.where(Case.stage != "closed")
        result = await session.execute(q)
        cases = result.scalars().all()

    return {
        "user": _serialize_user(user),
        "count": len(cases),
        "cases": [
            {
                "case_id": c.case_id,
                "contact_id": c.contact_id,
                "program_type": c.program_type,
                "stage": c.stage,
                "complexity": c.complexity,
                "ircc_decision": c.ircc_decision,
                "retainer_value": c.retainer_value,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "closed_at": c.closed_at.isoformat() if c.closed_at else None,
            }
            for c in cases
        ],
    }


@router.post("/sync-from-ghl")
async def sync_users_from_ghl(x_admin_key: str = Header(...)):
    """Re-sync the users table from GHL. Requires X-Admin-Key."""
    admin_key = os.getenv("ADMIN_API_KEY", "neuronx-admin-dev")
    if x_admin_key != admin_key:
        raise HTTPException(status_code=401, detail="Invalid admin key")

    svc = UserSyncService()
    summary = await svc.sync_all_from_ghl()
    return {"status": "ok", **summary}
