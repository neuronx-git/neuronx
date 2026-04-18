"""
User Sync Service — GHL users → PostgreSQL `users` table.

GHL is authoritative for who the team is (admin creates users there). This
service mirrors that roster so we can:
  * attach cases via FK instead of typo-prone strings
  * compute reliable per-user analytics / leaderboards
  * (future) implement access control and per-user portals

Data source order of preference:
  1. GHL REST:  GET /users/?locationId=<loc>   (requires oauth access token)
  2. Local fallback file: tools/ghl-lab/.team-users.json (for dev / offline)

Also exposes `resolve_by_name()` — fuzzy matches a legacy "First Last" string
to a User row. Used by the one-off `migrate_rcic_strings_to_fks` script.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional

from app import database
from app.services.ghl_client import GHLClient

logger = logging.getLogger("neuronx.user_sync")


# ── Role normalisation ───────────────────────────────────────────────────────
# GHL has a free-text "title" + coarse "role" (admin/user). We map both to
# NeuronX canonical roles used for analytics + access control.
_TITLE_TO_ROLE = {
    "managing partner / head rcic": "managing_partner",
    "managing partner": "managing_partner",
    "head rcic": "managing_partner",
    "senior rcic consultant": "senior_rcic",
    "senior rcic": "senior_rcic",
    "junior rcic consultant": "junior_rcic",
    "junior rcic": "junior_rcic",
    "client success manager": "csm",
    "sales development rep": "sdr",
    "sales development representative": "sdr",
    "operations manager": "ops",
    "intake coordinator": "intake",
}


def _normalise_role(title: str, perms: str = "", ghl_role: str = "") -> str:
    """Collapse GHL title + perms into one of our canonical role codes."""
    t = (title or "").strip().lower()
    if t in _TITLE_TO_ROLE:
        return _TITLE_TO_ROLE[t]
    p = (perms or "").strip().lower()
    if p in {
        "managing_partner", "senior_rcic", "junior_rcic",
        "csm", "sdr", "ops", "intake", "admin",
    }:
        return p
    return (ghl_role or "user").lower()


def _fallback_team_file() -> Path:
    """Return the repo-local .team-users.json path (GHL-lab snapshot)."""
    return Path(__file__).parent.parent.parent.parent / "tools" / "ghl-lab" / ".team-users.json"


def _name_similarity(a: str, b: str) -> float:
    """0.0–1.0 token-insensitive similarity score."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


class UserSyncService:
    """Sync GHL users → PostgreSQL users table."""

    def __init__(self, ghl_client: Optional[GHLClient] = None):
        self._ghl = ghl_client

    # ── Public API ──────────────────────────────────────────────────────────

    async def sync_all_from_ghl(self) -> dict:
        """
        Fetch all GHL users for the configured location and upsert them.

        Returns a summary dict: {fetched, created, updated, source}.
        Never raises for empty results — logs and returns zeros.
        """
        records = await self._fetch_users()
        if not records:
            logger.warning("No users found in GHL or fallback file — nothing to sync")
            return {"fetched": 0, "created": 0, "updated": 0, "source": "none"}

        created, updated = await self._upsert_users(records)
        return {
            "fetched": len(records),
            "created": created,
            "updated": updated,
            "source": records[0].get("_source", "unknown"),
        }

    async def resolve_by_name(self, name: str, threshold: float = 0.78) -> Optional[dict]:
        """
        Best-effort fuzzy match of a "First Last" string to a User row.

        Drops common display prefixes ("DEMO -", "Dr.", trailing ", RCIC" etc.)
        before comparing. Returns the dict `{id, email, full_name}` of the
        best match above `threshold`, else None.
        """
        if not name or not database.async_session_factory:
            return None

        cleaned = _clean_name_for_match(name)
        if not cleaned:
            return None

        from app.models.db_models import User
        from sqlalchemy import select

        async with database.async_session_factory() as session:
            result = await session.execute(select(User).where(User.is_active == True))  # noqa: E712
            users = result.scalars().all()

        best = None
        best_score = 0.0
        for u in users:
            candidates = [
                u.full_name,
                f"{u.first_name} {u.last_name}".strip(),
                _clean_name_for_match(u.full_name),
                _clean_name_for_match(f"{u.first_name} {u.last_name}"),
            ]
            for cand in candidates:
                s = _name_similarity(cleaned, cand)
                if s > best_score:
                    best_score = s
                    best = u

        if best and best_score >= threshold:
            return {
                "id": best.id,
                "email": best.email,
                "full_name": best.full_name,
                "match_score": round(best_score, 3),
            }
        logger.debug("No user match for %r (best score %.2f)", name, best_score)
        return None

    # ── Internals ───────────────────────────────────────────────────────────

    async def _fetch_users(self) -> list[dict]:
        """Try the GHL API first, fall back to the repo team-users snapshot."""
        # 1. GHL API
        try:
            ghl = self._ghl or GHLClient()
            r = await ghl._request(  # noqa: SLF001 — reuses auth/backoff
                "GET", f"/users/?locationId={ghl.location_id}",
            )
            payload = r.json()
            users = payload.get("users") or payload.get("data") or []
            if users:
                return [{**u, "_source": "ghl_api"} for u in users]
            logger.info("GHL /users returned empty list — trying fallback file")
        except Exception as e:  # pragma: no cover — network failure path
            logger.warning("GHL /users fetch failed (%s) — falling back to local file", e)

        # 2. Local snapshot
        path = _fallback_team_file()
        if path.exists():
            try:
                raw = json.loads(path.read_text())
                users = raw.get("users", [])
                # Remap snapshot keys → canonical keys (id/email/...)
                return [
                    {
                        "id": u.get("ghl_id") or u.get("id"),
                        "email": u.get("email", ""),
                        "firstName": u.get("firstName", ""),
                        "lastName": u.get("lastName", ""),
                        "phone": u.get("phone", ""),
                        "title": u.get("title", ""),
                        "role": u.get("role", "user"),
                        "perms": u.get("perms", ""),
                        "license": u.get("license", ""),
                        "_source": "team_users_file",
                    }
                    for u in users
                    if u.get("ghl_id") or u.get("id")
                ]
            except Exception as e:  # pragma: no cover
                logger.error("Failed to parse %s: %s", path, e)

        return []

    async def _upsert_users(self, records: list[dict]) -> tuple[int, int]:
        """Upsert a list of GHL user dicts; returns (created, updated)."""
        from app.models.db_models import User
        from sqlalchemy import select

        created = 0
        updated = 0
        now = datetime.now(timezone.utc)

        if not database.async_session_factory:
            logger.warning("Database not configured — skipping user upsert")
            return 0, 0

        async with database.async_session_factory() as session:
            for raw in records:
                uid = raw.get("id") or raw.get("userId") or raw.get("_id")
                if not uid:
                    continue

                first = raw.get("firstName", "") or raw.get("first_name", "")
                last = raw.get("lastName", "") or raw.get("last_name", "")
                full = f"{first} {last}".strip()
                email = (raw.get("email") or "").strip()
                role = _normalise_role(
                    raw.get("title", ""),
                    raw.get("perms", ""),
                    raw.get("role", ""),
                )

                result = await session.execute(select(User).where(User.id == uid))
                existing = result.scalar_one_or_none()

                if existing:
                    existing.email = email or existing.email
                    existing.first_name = first
                    existing.last_name = last
                    existing.full_name = full
                    existing.phone = raw.get("phone", "") or existing.phone
                    existing.role = role
                    existing.rcic_license = raw.get("license", "") or existing.rcic_license
                    existing.ghl_user_id = uid
                    existing.synced_at = now
                    updated += 1
                else:
                    session.add(User(
                        id=uid,
                        email=email or f"{uid}@unknown.local",
                        first_name=first,
                        last_name=last,
                        full_name=full,
                        phone=raw.get("phone", ""),
                        role=role,
                        rcic_license=raw.get("license", ""),
                        is_active=True,
                        ghl_user_id=uid,
                        synced_at=now,
                    ))
                    created += 1

            await session.commit()

        logger.info("User sync: created=%d updated=%d", created, updated)
        return created, updated


# ── Helpers ──────────────────────────────────────────────────────────────────

_PREFIXES = ("demo -", "demo-", "dr.", "dr ")
_SUFFIXES = (", rcic", ", r.c.i.c.", " rcic", ", esq", ", jd")


def _clean_name_for_match(name: str) -> str:
    """Strip display prefixes/suffixes that legacy strings often include."""
    if not name:
        return ""
    s = name.strip().lower()
    for p in _PREFIXES:
        if s.startswith(p):
            s = s[len(p):].strip()
            break
    for suf in _SUFFIXES:
        if s.endswith(suf):
            s = s[: -len(suf)].strip()
            break
    return s
