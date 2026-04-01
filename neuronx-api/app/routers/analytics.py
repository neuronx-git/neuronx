"""
Analytics Endpoints
GET /analytics/pipeline  — Conversion funnel metrics
GET /analytics/stuck     — Stuck leads detection
"""

from fastapi import APIRouter, Query
from typing import Optional
import logging

from app.services.analytics_service import AnalyticsService

router = APIRouter()
logger = logging.getLogger("neuronx.analytics")


@router.get("/pipeline")
async def pipeline_analytics(
    days: int = Query(30, description="Look-back window in days"),
    location_id: Optional[str] = Query(None, description="GHL location ID"),
):
    """
    Pipeline conversion funnel metrics.
    NEW → CONTACTING → ASSESSMENT → CONSULT READY → BOOKED → RETAINED

    Returns conversion rates, velocity, and bottleneck identification.
    """
    service = AnalyticsService()
    return await service.get_pipeline_metrics(days=days)


@router.get("/stuck")
async def stuck_leads(
    threshold_days: int = Query(3, description="Days without activity to flag as stuck"),
):
    """
    Identify leads stuck in a pipeline stage without activity.
    Returns list of stuck contacts with last activity and owner.
    """
    service = AnalyticsService()
    return await service.get_stuck_leads(threshold_days=threshold_days)


@router.get("/dashboard")
async def dashboard_summary():
    """
    Daily briefing data for firm owner.
    Returns: today's new leads, contacts scheduled, conversions, stuck count.
    """
    service = AnalyticsService()
    return await service.get_daily_summary()
