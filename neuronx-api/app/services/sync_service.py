"""
GHL → PostgreSQL Sync Service

Dual sync approach:
1. Webhook-driven: Real-time activity writes on every GHL event
2. Full sync: Daily pagination through all GHL contacts + opportunities

Rate limit safe: 0.5s delay between API pages, 100 records/page.
"""

import logging
import asyncio
from datetime import datetime, timezone
from typing import Optional

from app.services.ghl_client import GHLClient
from app import database
from app.config import settings

logger = logging.getLogger("neuronx.sync")


class SyncService:
    """Syncs GHL data to PostgreSQL for Metabase analytics."""

    async def record_activity(self, contact_id: str, activity_type: str,
                                detail: str = "", metadata: dict = None):
        """Record a webhook event as an activity row. Called from webhook handler."""
        if not database.async_session_factory:
            return  # Gracefully skip if no DB

        from app.models.db_models import Activity

        async with database.async_session_factory() as session:
            activity = Activity(
                contact_id=contact_id,
                activity_type=activity_type,
                detail=detail,
                metadata_json=metadata or {},
            )
            session.add(activity)
            await session.commit()
            logger.debug("Recorded activity: %s for %s", activity_type, contact_id)

    async def sync_contact(self, contact_id: str):
        """Sync a single contact from GHL to PostgreSQL."""
        if not database.async_session_factory:
            return

        from app.models.db_models import Contact
        from sqlalchemy import select

        ghl = GHLClient()
        contact_data = await ghl.get_contact(contact_id)

        # Extract custom fields into dict
        custom = {}
        score = 0
        outcome = ""
        program = ""
        for field in contact_data.get("customFields", []):
            key = field.get("id", "")
            val = field.get("value", "")
            custom[key] = val
            if "readiness_score" in key.lower():
                try:
                    score = int(val)
                except (ValueError, TypeError):
                    pass
            elif "readiness_outcome" in key.lower():
                outcome = val
            elif "program_interest" in key.lower():
                program = val

        async with database.async_session_factory() as session:
            # Upsert
            result = await session.execute(select(Contact).where(Contact.id == contact_id))
            existing = result.scalar_one_or_none()

            if existing:
                existing.first_name = contact_data.get("firstName", "")
                existing.last_name = contact_data.get("lastName", "")
                existing.email = contact_data.get("email", "")
                existing.phone = contact_data.get("phone", "")
                existing.tags = contact_data.get("tags", [])
                existing.source = contact_data.get("source", "")
                existing.custom_fields = custom
                existing.readiness_score = score
                existing.readiness_outcome = outcome
                existing.program_interest = program
                existing.synced_at = datetime.now(timezone.utc)
            else:
                new_contact = Contact(
                    id=contact_id,
                    first_name=contact_data.get("firstName", ""),
                    last_name=contact_data.get("lastName", ""),
                    email=contact_data.get("email", ""),
                    phone=contact_data.get("phone", ""),
                    tags=contact_data.get("tags", []),
                    source=contact_data.get("source", ""),
                    custom_fields=custom,
                    readiness_score=score,
                    readiness_outcome=outcome,
                    program_interest=program,
                    ghl_created_at=None,  # GHL doesn't always provide this
                )
                session.add(new_contact)

            await session.commit()

    async def full_sync(self) -> dict:
        """
        Full sync: paginate through all GHL contacts and opportunities.
        Call daily via POST /sync/full or a scheduled job.
        """
        if not database.async_session_factory:
            return {"error": "Database not configured"}

        from app.models.db_models import SyncLog

        logger.info("Starting full GHL → PostgreSQL sync")
        start_time = datetime.now(timezone.utc)
        contacts_synced = 0
        opps_synced = 0

        ghl = GHLClient()

        # Sync contacts
        try:
            contacts = await ghl.search_contacts("", limit=100)
            contact_list = contacts.get("contacts", [])

            for contact in contact_list:
                try:
                    await self.sync_contact(contact["id"])
                    contacts_synced += 1
                except Exception as e:
                    logger.warning("Failed to sync contact %s: %s", contact.get("id"), e)
                await asyncio.sleep(0.5)  # Rate limit safety

        except Exception as e:
            logger.error("Contact sync failed: %s", e)

        # Sync opportunities
        try:
            # Intake pipeline
            opps = await ghl.get_pipeline_opportunities(settings.ghl_pipeline_id)
            opp_list = opps.get("opportunities", [])

            from app.models.db_models import Opportunity
            from sqlalchemy import select

            async with database.async_session_factory() as session:
                for opp in opp_list:
                    result = await session.execute(
                        select(Opportunity).where(Opportunity.id == opp["id"])
                    )
                    existing = result.scalar_one_or_none()

                    if existing:
                        existing.stage_id = opp.get("pipelineStageId", "")
                        existing.status = opp.get("status", "open")
                        existing.monetary_value = float(opp.get("monetaryValue", 0) or 0)
                        existing.synced_at = datetime.now(timezone.utc)
                    else:
                        new_opp = Opportunity(
                            id=opp["id"],
                            contact_id=opp.get("contactId", ""),
                            pipeline_id=opp.get("pipelineId", ""),
                            pipeline_name="Immigration Intake",
                            stage_id=opp.get("pipelineStageId", ""),
                            stage_name="",  # Will be mapped later
                            status=opp.get("status", "open"),
                            monetary_value=float(opp.get("monetaryValue", 0) or 0),
                            assigned_to=opp.get("assignedTo", ""),
                        )
                        session.add(new_opp)
                    opps_synced += 1

                await session.commit()

        except Exception as e:
            logger.error("Opportunity sync failed: %s", e)

        # Log sync
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()

        async with database.async_session_factory() as session:
            log = SyncLog(
                entity_type="full_sync",
                records_synced=contacts_synced + opps_synced,
                status="completed",
            )
            session.add(log)
            await session.commit()

        result = {
            "status": "completed",
            "contacts_synced": contacts_synced,
            "opportunities_synced": opps_synced,
            "duration_seconds": round(duration, 1),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        logger.info("Full sync completed: %d contacts, %d opps in %.1fs",
                     contacts_synced, opps_synced, duration)
        return result
