"""
Webhook Signature Verification
Verifies GHL Ed25519 signatures and VAPI HMAC signatures.
Required for production security — all webhook handlers MUST call these.

GHL: Ed25519 signature in X-GHL-Signature header
VAPI: HMAC-SHA256 signature in X-Vapi-Signature header
"""

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from fastapi import HTTPException
import base64
import hashlib
import hmac
import time
import logging
import os

from app.config import settings

logger = logging.getLogger("neuronx.security")

# Replay protection: reject webhooks older than 5 minutes
MAX_WEBHOOK_AGE_SECONDS = 300

# Feature flag: set VERIFY_WEBHOOKS=false to disable in development
VERIFY_WEBHOOKS = os.getenv("VERIFY_WEBHOOKS", "true").lower() != "false"


def verify_ghl_signature(
    body: bytes,
    signature: str | None,
    timestamp: str | None = None,
) -> bool:
    """
    Verify GHL webhook Ed25519 signature.
    See: https://highlevel.stoplight.io/docs/integrations/webhook-security

    In development (VERIFY_WEBHOOKS=false), skips verification with warning.
    In production, raises 401 if signature is missing or invalid.
    """
    if not VERIFY_WEBHOOKS:
        logger.debug("Webhook verification disabled (VERIFY_WEBHOOKS=false)")
        return True

    if not signature:
        logger.warning("No GHL signature header present")
        raise HTTPException(status_code=401, detail="Missing webhook signature")

    # Timestamp validation (replay protection)
    if timestamp:
        try:
            webhook_time = int(timestamp)
            age = time.time() - webhook_time
            if age > MAX_WEBHOOK_AGE_SECONDS:
                raise HTTPException(status_code=401, detail="Webhook timestamp too old (replay protection)")
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid webhook timestamp")

    public_key_pem = settings.ghl_webhook_secret
    if not public_key_pem:
        # No public key configured — log and allow (transitional)
        logger.warning("No GHL webhook public key configured — signature received but cannot verify")
        return True

    try:
        public_key = load_pem_public_key(public_key_pem.encode())
        sig_bytes = base64.b64decode(signature)
        public_key.verify(sig_bytes, body)
        return True
    except Exception as e:
        logger.error("GHL signature verification failed: %s", str(e))
        raise HTTPException(status_code=401, detail="Invalid webhook signature")


def verify_vapi_signature(
    body: bytes,
    signature: str | None,
) -> bool:
    """
    Verify VAPI webhook HMAC-SHA256 signature.
    VAPI signs payload body with the webhook secret using HMAC-SHA256.
    """
    if not VERIFY_WEBHOOKS:
        logger.debug("Webhook verification disabled (VERIFY_WEBHOOKS=false)")
        return True

    if not signature:
        logger.warning("No VAPI signature header present")
        raise HTTPException(status_code=401, detail="Missing VAPI webhook signature")

    secret = settings.vapi_webhook_secret
    if not secret:
        logger.warning("No VAPI webhook secret configured — signature received but cannot verify")
        return True

    try:
        expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected, signature):
            return True
        raise HTTPException(status_code=401, detail="Invalid VAPI webhook signature")
    except HTTPException:
        raise
    except Exception as e:
        logger.error("VAPI signature verification failed: %s", str(e))
        raise HTTPException(status_code=401, detail="VAPI signature verification error")
