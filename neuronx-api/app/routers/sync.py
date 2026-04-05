"""
Data Sync Endpoints
POST /sync/full    — Full GHL → PostgreSQL sync (contacts + opportunities)
GET  /sync/status  — Last sync status
"""

from fastapi import APIRouter
import logging

from app.services.sync_service import SyncService
from app.database import async_session_factory

router = APIRouter()
logger = logging.getLogger("neuronx.sync")


@router.post("/full")
async def full_sync():
    """
    Run a full GHL → PostgreSQL sync.
    Paginates through all contacts and opportunities.
    Call daily or on-demand.
    """
    from app.database import async_session_factory as sf
    if not sf:
        return {"error": "Database not configured. Set DATABASE_URL env var."}

    service = SyncService()
    return await service.full_sync()


@router.get("/status")
async def sync_status():
    """Get the last sync timestamp and record count."""
    from app.database import async_session_factory
    if not async_session_factory:
        return {"database": "not configured", "last_sync": None}
    from app.models.db_models import SyncLog
    from sqlalchemy import select

    if not async_session_factory:
        return {"database": "not initialized", "last_sync": None}

    async with async_session_factory() as session:
        result = await session.execute(
            select(SyncLog).order_by(SyncLog.last_sync_at.desc()).limit(1)
        )
        last = result.scalar_one_or_none()

        if last:
            return {
                "database": "connected",
                "last_sync": last.last_sync_at.isoformat(),
                "records_synced": last.records_synced,
                "status": last.status,
            }
        return {"database": "connected", "last_sync": None, "note": "No sync has been run yet"}
