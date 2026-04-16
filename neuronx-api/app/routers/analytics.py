"""
Analytics Endpoints
GET /analytics/pipeline  — Conversion funnel metrics
GET /analytics/stuck     — Stuck leads detection
GET /analytics/dashboard — Daily briefing
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import logging

from app.services.analytics_service import AnalyticsService

router = APIRouter()
logger = logging.getLogger("neuronx.analytics")


@router.get("/pipeline")
async def pipeline_analytics(
    days: int = Query(30, ge=1, le=365, description="Look-back window in days"),
    location_id: Optional[str] = Query(None, description="GHL location ID"),
):
    """
    Pipeline conversion funnel metrics.
    Returns conversion rates, velocity, and bottleneck identification.
    """
    service = AnalyticsService()
    try:
        return await service.get_pipeline_metrics(days=days)
    except Exception as e:
        logger.error("Pipeline analytics failed: %s", e)
        raise HTTPException(status_code=500, detail="Analytics unavailable")


@router.get("/stuck")
async def stuck_leads(
    threshold_days: int = Query(3, ge=1, le=90, description="Days without activity to flag as stuck"),
    limit: int = Query(50, ge=1, le=200, description="Max results"),
):
    """
    Identify leads stuck in a pipeline stage without activity.
    Returns list of stuck contacts with last activity and owner.
    """
    service = AnalyticsService()
    try:
        result = await service.get_stuck_leads(threshold_days=threshold_days)
        # Apply limit to prevent unbounded responses
        if isinstance(result, dict) and "stuck_leads" in result:
            result["stuck_leads"] = result["stuck_leads"][:limit]
        elif isinstance(result, list):
            result = result[:limit]
        return result
    except Exception as e:
        logger.error("Stuck leads query failed: %s", e)
        raise HTTPException(status_code=500, detail="Analytics unavailable")


@router.get("/dashboard")
async def dashboard_summary():
    """
    Daily briefing data for firm owner.
    Returns: today's new leads, contacts scheduled, conversions, stuck count.
    """
    service = AnalyticsService()
    try:
        return await service.get_daily_summary()
    except Exception as e:
        logger.error("Dashboard summary failed: %s", e)
        raise HTTPException(status_code=500, detail="Analytics unavailable")
