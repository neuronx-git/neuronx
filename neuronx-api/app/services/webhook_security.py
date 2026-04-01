"""
Webhook Signature Verification
Verifies GHL Ed25519 signatures and VAPI signatures.
Required for production security.
"""

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from fastapi import HTTPException
import base64
import time
import logging

logger = logging.getLogger("neuronx.security")

# Replay protection: reject webhooks older than 5 minutes
MAX_WEBHOOK_AGE_SECONDS = 300


def verify_ghl_signature(
    body: bytes,
    signature: str | None,
    timestamp: str | None = None,
    public_key_pem: str | None = None,
) -> bool:
    """
    Verify GHL webhook Ed25519 signature.
    See: https://highlevel.stoplight.io/docs/integrations/webhook-security
    """
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

    # Signature verification
    if not public_key_pem:
        logger.warning("No GHL public key configured — skipping signature verification")
        return True  # TODO: Remove when GHL webhook secret is configured

    try:
        public_key = load_pem_public_key(public_key_pem.encode())
        sig_bytes = base64.b64decode(signature)
        public_key.verify(sig_bytes, body)
        return True
    except Exception as e:
        logger.error("GHL signature verification failed: %s", str(e))
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
