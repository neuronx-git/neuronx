"""
GHL API Client
Thin wrapper around GoHighLevel V2 API.

Token management: Reads OAuth token from tools/ghl-lab/.tokens.json.
Falls back to GHL_ACCESS_TOKEN env var if token file not found.

Reliability:
- Retry with exponential backoff (3 attempts via tenacity)
- 429 rate limit handling with Retry-After header
- Shared httpx client for connection pooling
- Token cache with 20h TTL

Rate limits (sandbox): 25 req/10s, 10K req/day
Rate limits (production): 100 req/10s, 200K req/day
Docs: https://highlevel.stoplight.io/docs/integrations/
"""

import httpx
import json
import logging
import time
import asyncio
from pathlib import Path
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log

from app.config import settings

logger = logging.getLogger("neuronx.ghl")

# Token file path (relative to project root)
TOKEN_FILE = Path(__file__).parent.parent.parent.parent / "tools" / "ghl-lab" / ".tokens.json"

# Shared httpx client (connection pooling)
_http_client: Optional[httpx.AsyncClient] = None


def _get_http_client() -> httpx.AsyncClient:
    """Get or create shared httpx client for connection reuse."""
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        )
    return _http_client


class RateLimitError(Exception):
    """Raised when GHL returns 429 — triggers retry with backoff."""
    def __init__(self, retry_after: int = 10):
        self.retry_after = retry_after
        super().__init__(f"Rate limited. Retry after {retry_after}s")


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

    async def _refresh_token(self) -> bool:
        """Auto-refresh GHL OAuth token using refresh_token. Refresh token valid until 2057."""
        refresh_token = None

        # Get refresh token from .tokens.json
        if TOKEN_FILE.exists():
            try:
                data = json.loads(TOKEN_FILE.read_text())
                refresh_token = data.get("refresh_token")
            except (json.JSONDecodeError, KeyError):
                pass

        if not refresh_token:
            logger.error("No refresh token available for auto-refresh")
            return False

        try:
            client = _get_http_client()
            r = await client.post(
                "https://services.leadconnectorhq.com/oauth/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": settings.ghl_client_id if hasattr(settings, 'ghl_client_id') else "",
                    "client_secret": settings.ghl_client_secret if hasattr(settings, 'ghl_client_secret') else "",
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            if r.status_code == 200:
                tokens = r.json()
                GHLClient._cached_token = tokens["access_token"]
                GHLClient._token_expires_at = time.time() + (20 * 3600)
                logger.info("GHL token auto-refreshed successfully")

                # Update .tokens.json if it exists
                if TOKEN_FILE.exists():
                    try:
                        data = json.loads(TOKEN_FILE.read_text())
                        data["access_token"] = tokens["access_token"]
                        if "refresh_token" in tokens:
                            data["refresh_token"] = tokens["refresh_token"]
                        data["refreshed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                        TOKEN_FILE.write_text(json.dumps(data, indent=2))
                    except Exception as e:
                        logger.warning("Could not update token file: %s", e)
                return True
            else:
                logger.error("GHL token refresh failed: %d %s", r.status_code, r.text[:100])
                return False
        except Exception as e:
            logger.error("GHL token refresh error: %s", e)
            return False

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=30),
        retry=retry_if_exception_type((httpx.ConnectError, httpx.ReadTimeout, RateLimitError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Make an authenticated GHL API request with retry + rate limit handling."""
        url = f"{self.base_url}{path}"
        client = _get_http_client()

        r = await client.request(method, url, headers=self.headers, **kwargs)

        # Handle rate limiting
        if r.status_code == 429:
            retry_after = int(r.headers.get("Retry-After", "10"))
            logger.warning("GHL 429 rate limited — waiting %ds before retry", retry_after)
            await asyncio.sleep(retry_after)
            raise RateLimitError(retry_after)

        # Handle auth failures — auto-refresh token
        if r.status_code == 401:
            logger.warning("GHL 401 — attempting automatic token refresh")
            GHLClient._cached_token = None
            GHLClient._token_expires_at = 0
            refreshed = await self._refresh_token()
            if refreshed:
                # Retry the request with the new token
                r = await client.request(method, url, headers=self.headers, **kwargs)
                if r.status_code == 401:
                    logger.error("GHL 401 after refresh — token may be permanently invalid")
                else:
                    return r

        # Handle server errors (trigger retry)
        if r.status_code >= 500:
            logger.warning("GHL %d on %s %s — will retry", r.status_code, method, path)
            r.raise_for_status()

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

    async def search_contacts(self, query: str, limit: int = 20) -> dict:
        """Search contacts by name, email, or phone."""
        r = await self._request(
            "POST",
            "/contacts/search",
            json={
                "locationId": self.location_id,
                "query": query,
                "pageLimit": limit,
            },
        )
        return r.json()

    async def get_pipeline_opportunities(
        self,
        pipeline_id: Optional[str] = None,
        limit: int = 50,
    ) -> list:
        """Get all opportunities in a pipeline."""
        r = await self._request(
            "GET",
            "/opportunities/search",
            params={
                "location_id": self.location_id,
                "pipeline_id": pipeline_id or settings.ghl_pipeline_id,
                "limit": limit,
            },
        )
        return r.json().get("opportunities", [])
