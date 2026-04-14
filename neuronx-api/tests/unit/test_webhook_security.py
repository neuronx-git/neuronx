"""
Unit Tests — Webhook Signature Verification

Tests GHL Ed25519 and VAPI HMAC-SHA256 signature verification.
Both with verification enabled and disabled (VERIFY_WEBHOOKS flag).
"""

import pytest
import hmac
import hashlib
import time
import os
from unittest.mock import patch
from fastapi import HTTPException

pytestmark = pytest.mark.unit


class TestGHLSignatureVerification:
    """Test verify_ghl_signature with Ed25519."""

    def test_verification_disabled_returns_true(self):
        """When VERIFY_WEBHOOKS=false, all signatures pass."""
        with patch.dict(os.environ, {"VERIFY_WEBHOOKS": "false"}):
            # Need to reimport since VERIFY_WEBHOOKS is read at module load
            import importlib
            from app.services import webhook_security
            importlib.reload(webhook_security)

            result = webhook_security.verify_ghl_signature(
                body=b"test body",
                signature=None,
                timestamp=None,
            )
            assert result is True

            # Restore
            os.environ["VERIFY_WEBHOOKS"] = "false"
            importlib.reload(webhook_security)

    def test_missing_signature_raises_401_when_enabled(self):
        """Missing signature raises 401 when verification is enabled."""
        with patch.dict(os.environ, {"VERIFY_WEBHOOKS": "true"}):
            import importlib
            from app.services import webhook_security
            importlib.reload(webhook_security)

            try:
                with pytest.raises(HTTPException) as exc_info:
                    webhook_security.verify_ghl_signature(
                        body=b"test body",
                        signature=None,
                    )
                assert exc_info.value.status_code == 401
            finally:
                os.environ["VERIFY_WEBHOOKS"] = "false"
                importlib.reload(webhook_security)

    def test_expired_timestamp_raises_401(self):
        """Timestamp older than 5 minutes raises 401."""
        with patch.dict(os.environ, {"VERIFY_WEBHOOKS": "true"}):
            import importlib
            from app.services import webhook_security
            importlib.reload(webhook_security)

            old_timestamp = str(int(time.time()) - 600)  # 10 minutes ago
            try:
                with pytest.raises(HTTPException) as exc_info:
                    webhook_security.verify_ghl_signature(
                        body=b"test body",
                        signature="some-sig",
                        timestamp=old_timestamp,
                    )
                assert exc_info.value.status_code == 401
                assert "replay" in exc_info.value.detail.lower() or "old" in exc_info.value.detail.lower()
            finally:
                os.environ["VERIFY_WEBHOOKS"] = "false"
                importlib.reload(webhook_security)

    def test_invalid_timestamp_raises_401(self):
        """Non-numeric timestamp raises 401."""
        with patch.dict(os.environ, {"VERIFY_WEBHOOKS": "true"}):
            import importlib
            from app.services import webhook_security
            importlib.reload(webhook_security)

            try:
                with pytest.raises(HTTPException) as exc_info:
                    webhook_security.verify_ghl_signature(
                        body=b"test body",
                        signature="some-sig",
                        timestamp="not-a-number",
                    )
                assert exc_info.value.status_code == 401
            finally:
                os.environ["VERIFY_WEBHOOKS"] = "false"
                importlib.reload(webhook_security)

    def test_no_public_key_allows_through(self):
        """When no public key is configured, signature is allowed (transitional)."""
        with patch.dict(os.environ, {"VERIFY_WEBHOOKS": "true"}):
            import importlib
            from app.services import webhook_security
            importlib.reload(webhook_security)

            try:
                with patch("app.services.webhook_security.settings") as mock_settings:
                    mock_settings.ghl_webhook_secret = ""
                    result = webhook_security.verify_ghl_signature(
                        body=b"test body",
                        signature="some-sig",
                        timestamp=str(int(time.time())),
                    )
                    assert result is True
            finally:
                os.environ["VERIFY_WEBHOOKS"] = "false"
                importlib.reload(webhook_security)

    def test_invalid_signature_raises_401(self):
        """Invalid Ed25519 signature raises 401."""
        with patch.dict(os.environ, {"VERIFY_WEBHOOKS": "true"}):
            import importlib
            from app.services import webhook_security
            importlib.reload(webhook_security)

            try:
                with patch("app.services.webhook_security.settings") as mock_settings:
                    # Use a real PEM key format (but wrong key for the signature)
                    mock_settings.ghl_webhook_secret = "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAtest1234567890abcdefghijklmnopqrst=\n-----END PUBLIC KEY-----"
                    with pytest.raises(HTTPException) as exc_info:
                        webhook_security.verify_ghl_signature(
                            body=b"test body",
                            signature="aW52YWxpZA==",  # base64 "invalid"
                            timestamp=str(int(time.time())),
                        )
                    assert exc_info.value.status_code == 401
            finally:
                os.environ["VERIFY_WEBHOOKS"] = "false"
                importlib.reload(webhook_security)


class TestVAPISignatureVerification:
    """Test verify_vapi_signature with HMAC-SHA256."""

    def test_verification_disabled_returns_true(self):
        """When VERIFY_WEBHOOKS=false, all signatures pass."""
        from app.services.webhook_security import verify_vapi_signature
        result = verify_vapi_signature(body=b"test", signature=None)
        assert result is True

    def test_missing_signature_raises_401_when_enabled(self):
        """Missing VAPI signature raises 401."""
        with patch.dict(os.environ, {"VERIFY_WEBHOOKS": "true"}):
            import importlib
            from app.services import webhook_security
            importlib.reload(webhook_security)

            try:
                with pytest.raises(HTTPException) as exc_info:
                    webhook_security.verify_vapi_signature(
                        body=b"test",
                        signature=None,
                    )
                assert exc_info.value.status_code == 401
            finally:
                os.environ["VERIFY_WEBHOOKS"] = "false"
                importlib.reload(webhook_security)

    def test_no_secret_allows_through(self):
        """When no VAPI secret is configured, signature is allowed."""
        with patch.dict(os.environ, {"VERIFY_WEBHOOKS": "true"}):
            import importlib
            from app.services import webhook_security
            importlib.reload(webhook_security)

            try:
                with patch("app.services.webhook_security.settings") as mock_settings:
                    mock_settings.vapi_webhook_secret = ""
                    result = webhook_security.verify_vapi_signature(
                        body=b"test",
                        signature="some-sig",
                    )
                    assert result is True
            finally:
                os.environ["VERIFY_WEBHOOKS"] = "false"
                importlib.reload(webhook_security)

    def test_valid_hmac_passes(self):
        """Valid HMAC-SHA256 signature passes verification."""
        with patch.dict(os.environ, {"VERIFY_WEBHOOKS": "true"}):
            import importlib
            from app.services import webhook_security
            importlib.reload(webhook_security)

            secret = "test-secret-key"
            body = b'{"message":{"type":"end-of-call-report"}}'
            valid_sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

            try:
                with patch("app.services.webhook_security.settings") as mock_settings:
                    mock_settings.vapi_webhook_secret = secret
                    result = webhook_security.verify_vapi_signature(
                        body=body,
                        signature=valid_sig,
                    )
                    assert result is True
            finally:
                os.environ["VERIFY_WEBHOOKS"] = "false"
                importlib.reload(webhook_security)

    def test_invalid_hmac_raises_401(self):
        """Invalid HMAC signature raises 401."""
        with patch.dict(os.environ, {"VERIFY_WEBHOOKS": "true"}):
            import importlib
            from app.services import webhook_security
            importlib.reload(webhook_security)

            try:
                with patch("app.services.webhook_security.settings") as mock_settings:
                    mock_settings.vapi_webhook_secret = "real-secret"
                    with pytest.raises(HTTPException) as exc_info:
                        webhook_security.verify_vapi_signature(
                            body=b"test body",
                            signature="wrong-signature-value",
                        )
                    assert exc_info.value.status_code == 401
            finally:
                os.environ["VERIFY_WEBHOOKS"] = "false"
                importlib.reload(webhook_security)
