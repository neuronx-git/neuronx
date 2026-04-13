"""
Test configuration — disables webhook signature verification for tests.
"""
import os

# Disable webhook signature verification in tests
os.environ["VERIFY_WEBHOOKS"] = "false"
