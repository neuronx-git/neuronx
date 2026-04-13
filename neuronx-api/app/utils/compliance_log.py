"""
Compliance & Audit Log
Writes structured events to JSONL file with request correlation IDs.

Every webhook, scoring decision, trust check, and case stage change is logged.
Required for regulatory compliance and incident investigation.

Architecture: JSONL file is the primary audit log. PostgreSQL activities table
is populated by webhook handlers directly (async context).
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from contextvars import ContextVar

from app.config import settings

logger = logging.getLogger("neuronx.audit")

# Request correlation ID — set per request, used in all log entries
request_id: ContextVar[str] = ContextVar("request_id", default="")


def get_request_id() -> str:
    """Get or create request correlation ID for log tracing."""
    rid = request_id.get()
    if not rid:
        rid = uuid.uuid4().hex[:12]
        request_id.set(rid)
    return rid


def log_event(event_type: str, data: dict) -> None:
    """
    Append a structured audit event to the compliance log.

    Each entry includes:
    - timestamp (UTC ISO 8601)
    - request_id (correlation across services)
    - event_type (ghl_webhook, vapi_end_of_call, call_processed, trust_check, etc.)
    - event-specific data fields
    """
    entry = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "request_id": get_request_id(),
        "event_type": event_type,
        **data,
    }

    log_path = Path(settings.compliance_log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logger.error("Failed to write compliance log: %s", str(e))
