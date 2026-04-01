"""
GHL API Client
Thin wrapper around GoHighLevel V2 API.

Token management: Reads OAuth token from tools/ghl-lab/.tokens.json.
Falls back to GHL_ACCESS_TOKEN env var if token file not found.

Rate limits (sandbox): 25 req/10s, 10K req/day
Rate limits (production): 100 req/10s, 200K req/day
Docs: https://highlevel.stoplight.io/docs/integrations/
"""

import httpx
import json
import logging
import time
from pathlib import Path
from typing import Optional
from app.config import settings

logger = logging.getLogger("neuronx.ghl")

# Token file path (relative to project root)
TOKEN_FILE = Path(__file__).parent.parent.parent.parent / "tools" / "ghl-lab" / ".tokens.json"


class GHLClient:
    _cached_token: Optional[str] = None
    _token_expires_at: float = 0

    def __init__(self, location_id: Optional[str] = None):
        self.base_url = settings.ghl_api_base_url
        self.location_id = location_id or settings.ghl_location_id

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
            "Version": "2021-07-28",
        }

    def _get_token(self) -> str:
        """Read OAuth token from .tokens.json, falling back to env var."""
        now = time.time()
        if GHLClient._cached_token and now < GHLClient._token_expires_at:
            return GHLClient._cached_token

        if TOKEN_FILE.exists():
            try:
                data = json.loads(TOKEN_FILE.read_text())
                GHLClient._cached_token = data["access_token"]
                # GHL tokens expire in ~24h; cache for 20h to be safe
                GHLClient._token_expires_at = now + (20 * 3600)
                logger.info("Loaded GHL token from %s", TOKEN_FILE)
                return GHLClient._cached_token
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning("Failed to read token file: %s", e)

        if settings.ghl_access_token:
            return settings.ghl_access_token

        raise RuntimeError("No GHL access token available. Set GHL_ACCESS_TOKEN or ensure .tokens.json exists.")

    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Make an authenticated GHL API request with error handling."""
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.request(method, url, headers=self.headers, **kwargs)
            if r.status_code == 401:
                logger.error("GHL 401 — token may be expired. Refresh via: cd tools/ghl-lab && npx tsx src/ghlProvisioner.ts refresh-token")
                GHLClient._cached_token = None
                GHLClient._token_expires_at = 0
            r.raise_for_status()
            return r

    # ── Contact Operations ──

    async def get_contact(self, contact_id: str) -> dict:
        r = await self._request("GET", f"/contacts/{contact_id}")
        return r.json().get("contact", {})

    async def update_contact(self, contact_id: str, data: dict) -> dict:
        """Update contact fields (name, email, phone, tags, etc.)."""
        r = await self._request("PUT", f"/contacts/{contact_id}", json=data)
        return r.json().get("contact", {})

    async def update_custom_fields(self, contact_id: str, fields: dict) -> bool:
        """
        Update GHL custom fields for a contact.
        fields: dict of {field_key: value} where field_key is the custom field key.
        GHL V2 API format: customFields = [{"id": key, "field_value": value}]
        """
        if not fields:
            return True
        payload = {
            "customFields": [
                {"id": k, "field_value": str(v)} for k, v in fields.items()
            ]
        }
        await self._request("PUT", f"/contacts/{contact_id}", json=payload)
        logger.info("Updated %d custom fields for contact %s", len(fields), contact_id)
        return True

    async def add_tag(self, contact_id: str, tag: str) -> bool:
        """Add a tag to a GHL contact."""
        await self._request("POST", f"/contacts/{contact_id}/tags", json={"tags": [tag]})
        logger.info("Added tag '%s' to contact %s", tag, contact_id)
        return True

    async def add_tags(self, contact_id: str, tags: list[str]) -> bool:
        """Add multiple tags to a GHL contact."""
        if not tags:
            return True
        await self._request("POST", f"/contacts/{contact_id}/tags", json={"tags": tags})
        logger.info("Added %d tags to contact %s", len(tags), contact_id)
        return True

    async def remove_tag(self, contact_id: str, tag: str) -> bool:
        """Remove a tag from a GHL contact."""
        await self._request("DELETE", f"/contacts/{contact_id}/tags", json={"tags": [tag]})
        logger.info("Removed tag '%s' from contact %s", tag, contact_id)
        return True

    # ── Notes ──

    async def add_note(self, contact_id: str, note: str) -> bool:
        """Add a note to a GHL contact."""
        await self._request("POST", f"/contacts/{contact_id}/notes", json={"body": note})
        return True

    # ── Appointments ──

    async def get_appointment(self, appointment_id: str) -> dict:
        r = await self._request("GET", f"/calendars/events/appointments/{appointment_id}")
        return r.json()

    # ── Opportunities ──

    async def get_opportunities_by_contact(self, contact_id: str) -> list:
        r = await self._request(
            "GET",
            f"/opportunities/search",
            params={"location_id": self.location_id, "contact_id": contact_id},
        )
        return r.json().get("opportunities", [])

    async def update_opportunity_stage(self, opportunity_id: str, stage_id: str) -> dict:
        """Move an opportunity to a new pipeline stage."""
        r = await self._request(
            "PUT",
            f"/opportunities/{opportunity_id}",
            json={"pipelineStageId": stage_id},
        )
        return r.json()

    # ── Conversations / Messaging ──

    async def send_email(self, contact_id: str, subject: str, body: str) -> bool:
        """Send email to a contact via GHL Conversations API."""
        await self._request(
            "POST",
            "/conversations/messages",
            json={
                "type": "Email",
                "contactId": contact_id,
                "subject": subject,
                "html": body,
            },
        )
        return True

    # ── Search ──

    async def search_contacts(self, query: str, limit: int = 20) -> list:
        """Search contacts by name, email, or phone."""
        r = await self._request(
            "POST",
            "/contacts/search",
            json={
                "locationId": self.location_id,
                "query": query,
                "limit": limit,
            },
        )
        return r.json().get("contacts", [])

    async def get_pipeline_opportunities(
        self,
        pipeline_id: str = "Dtj9nQVd3QjL7bAb3Aiw",
        limit: int = 50,
    ) -> list:
        """Get all opportunities in a pipeline."""
        r = await self._request(
            "GET",
            "/opportunities/search",
            params={
                "location_id": self.location_id,
                "pipeline_id": pipeline_id,
                "limit": limit,
            },
        )
        return r.json().get("opportunities", [])
