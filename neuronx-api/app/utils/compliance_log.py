"""
Compliance Audit Log
Append-only JSONL log of all AI interactions and trust checks.
Required for regulatory compliance and incident investigation.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from app.config import settings

logger = logging.getLogger("neuronx.compliance")


def log_event(event_type: str, data: dict) -> None:
    """Append an event to the compliance audit log."""
    entry = {
        "timestamp": datetime.now(tz=__import__('datetime').timezone.utc).isoformat(),
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
