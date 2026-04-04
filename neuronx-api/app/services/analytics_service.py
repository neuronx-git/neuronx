"""
Analytics Service
Pipeline conversion metrics, stuck lead detection, daily summaries.
Pulls real data from GHL API.
"""

import logging
from datetime import datetime, timezone, timedelta
from app.services.ghl_client import GHLClient
from app.config import settings

logger = logging.getLogger("neuronx.analytics")

# Pipeline stage order (must match GHL pipeline)
INTAKE_STAGES = [
    "NEW", "CONTACTING", "ASSESSMENT SCHEDULED", "CONSULT READY",
    "BOOKED", "CONSULTATION HELD", "PROPOSAL SENT", "RETAINER",
    "RETAINED", "COLD / NURTURE",
]


class AnalyticsService:
    async def get_pipeline_metrics(self, days: int = 30) -> dict:
        """
        Conversion funnel metrics for the last N days.
        Pulls real opportunity data from GHL.
        """
        ghl = GHLClient()
        try:
            opportunities = await ghl.get_pipeline_opportunities(
                pipeline_id=settings.ghl_pipeline_id,
                limit=100,
            )
        except Exception as e:
            logger.warning("Failed to fetch GHL opportunities: %s", e)
            opportunities = []

        # Count by stage
        stage_counts = {}
        for opp in opportunities:
            stage_name = opp.get("pipelineStageId", "unknown")
            # GHL returns stage IDs, not names. Map if possible.
            stage_counts[stage_name] = stage_counts.get(stage_name, 0) + 1

        total = len(opportunities)

        # Calculate basic metrics
        return {
            "period_days": days,
            "as_of": datetime.now(tz=timezone.utc).isoformat(),
            "total_opportunities": total,
            "stage_distribution": stage_counts,
            "north_star": {
                "total_in_pipeline": total,
                "note": "Stage-level conversion rates require stage name mapping. Pipeline ID: " + settings.ghl_pipeline_id,
            },
        }

    async def get_stuck_leads(self, threshold_days: int = 3) -> dict:
        """
        Identify contacts stuck in the same stage for > threshold_days.
        """
        ghl = GHLClient()
        try:
            opportunities = await ghl.get_pipeline_opportunities(limit=100)
        except Exception as e:
            logger.warning("Failed to fetch opportunities: %s", e)
            return {"stuck_count": 0, "stuck_leads": [], "error": str(e)}

        threshold = datetime.now(tz=timezone.utc) - timedelta(days=threshold_days)
        stuck = []

        for opp in opportunities:
            last_update = opp.get("updatedAt") or opp.get("lastStageChangeAt")
            if last_update:
                try:
                    update_time = datetime.fromisoformat(last_update.replace("Z", "+00:00"))
                    if update_time < threshold:
                        stuck.append({
                            "id": opp.get("id"),
                            "contact_id": opp.get("contactId"),
                            "name": opp.get("name", "Unknown"),
                            "stage": opp.get("pipelineStageId"),
                            "last_updated": last_update,
                            "days_stuck": (datetime.now(tz=timezone.utc) - update_time).days,
                        })
                except (ValueError, TypeError):
                    pass

        stuck.sort(key=lambda x: x.get("days_stuck", 0), reverse=True)

        return {
            "threshold_days": threshold_days,
            "stuck_count": len(stuck),
            "stuck_leads": stuck[:20],
        }

    async def get_daily_summary(self) -> dict:
        """Daily briefing for firm owner dashboard."""
        ghl = GHLClient()
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

        try:
            opportunities = await ghl.get_pipeline_opportunities(limit=100)
        except Exception as e:
            return {"date": today, "error": str(e)}

        total = len(opportunities)

        return {
            "date": today,
            "total_pipeline_opportunities": total,
            "pipeline_id": settings.ghl_pipeline_id,
        }
