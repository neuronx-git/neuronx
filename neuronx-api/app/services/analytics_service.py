"""
Analytics Service
Pipeline conversion metrics, stuck lead detection, daily summaries.

V1: Pulls from GHL API. Future: Local DB for historical tracking.
"""

import logging
from datetime import datetime, timedelta
from app.services.ghl_client import GHLClient

logger = logging.getLogger("neuronx.analytics")

# Pipeline stage names (must match GHL pipeline: Dtj9nQVd3QjL7bAb3Aiw)
PIPELINE_STAGES = [
    "NEW",
    "CONTACTING",
    "ASSESSMENT SCHEDULED",
    "CONSULT READY",
    "BOOKED",
    "CONSULTATION HELD",
    "RETAINER",
    "RETAINED",
    "COLD / NURTURE",
]


class AnalyticsService:
    async def get_pipeline_metrics(self, days: int = 30) -> dict:
        """
        Conversion funnel metrics for the last N days.
        Returns stage counts and conversion rates.
        """
        # TODO: Pull from GHL API opportunities endpoint
        # GET /opportunities/search?location_id={id}&date_added={start}
        return {
            "period_days": days,
            "as_of": datetime.now().isoformat(),
            "funnel": {
                "NEW": {"count": 0, "conversion_rate_to_next": None},
                "CONTACTING": {"count": 0, "conversion_rate_to_next": None},
                "ASSESSMENT SCHEDULED": {"count": 0, "conversion_rate_to_next": None},
                "CONSULT READY": {"count": 0, "conversion_rate_to_next": None},
                "BOOKED": {"count": 0, "conversion_rate_to_next": None},
                "CONSULTATION HELD": {"count": 0, "conversion_rate_to_next": None},
                "RETAINER": {"count": 0, "conversion_rate_to_next": None},
                "RETAINED": {"count": 0, "conversion_rate_to_next": None},
            },
            "north_star": {
                "consult_to_retained_rate": None,
                "speed_to_first_contact_avg_min": None,
                "contact_rate": None,
                "booking_rate": None,
                "show_rate": None,
            },
            "note": "Full implementation in Week 4. Requires GHL opportunity data ingestion.",
        }

    async def get_stuck_leads(self, threshold_days: int = 3) -> dict:
        """
        Identify contacts that have been in the same stage for > threshold_days.
        """
        # TODO: Implement via GHL opportunities API + last_stage_change_date
        return {
            "threshold_days": threshold_days,
            "stuck_count": 0,
            "stuck_leads": [],
            "note": "Full implementation in Week 4.",
        }

    async def get_daily_summary(self) -> dict:
        """Daily briefing for firm owner dashboard."""
        today = datetime.now().strftime("%Y-%m-%d")
        return {
            "date": today,
            "new_inquiries_today": 0,
            "consultations_today": 0,
            "retainers_this_week": 0,
            "stuck_leads": 0,
            "pipeline_health": "pending_data",
            "note": "Full implementation in Week 4.",
        }
