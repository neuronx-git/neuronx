"""
Auto-refresh GHL sandbox OAuth token.

Reads: client_id + client_secret from tools/ghl-lab/.env
Updates: tools/ghl-lab/.tokens.json in place

Usage: python3 tools/ghl-lab/src/refresh_oauth.py
"""
import httpx
import json
import os
import sys
import time
from pathlib import Path


def load_env(env_path):
    """Parse simple KEY=value .env file."""
    d = {}
    if not env_path.exists():
        return d
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip().strip('"').strip("'")
    return d


def main():
    root = Path(__file__).parent.parent
    env_path = root / ".env"
    tokens_path = root / ".tokens.json"

    env = load_env(env_path)
    client_id = env.get("GHL_OAUTH_CLIENT_ID") or os.getenv("GHL_OAUTH_CLIENT_ID")
    client_secret = env.get("GHL_OAUTH_CLIENT_SECRET") or os.getenv("GHL_OAUTH_CLIENT_SECRET")
    if not (client_id and client_secret):
        print("ERROR: GHL_OAUTH_CLIENT_ID + GHL_OAUTH_CLIENT_SECRET not in tools/ghl-lab/.env", file=sys.stderr)
        sys.exit(1)

    with open(tokens_path) as f:
        tokens = json.load(f)

    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        print("ERROR: No refresh_token in .tokens.json", file=sys.stderr)
        sys.exit(1)

    r = httpx.post(
        "https://services.leadconnectorhq.com/oauth/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "user_type": "Location",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    if r.status_code != 200:
        print(f"Refresh failed: {r.status_code} {r.text[:300]}", file=sys.stderr)
        sys.exit(1)

    new = r.json()
    tokens.update(new)
    tokens["refreshed_at"] = int(time.time())
    tokens_path.write_text(json.dumps(tokens, indent=2))

    # Verify
    r2 = httpx.get(
        f"https://services.leadconnectorhq.com/locations/{tokens['locationId']}",
        headers={"Authorization": f"Bearer {new['access_token']}", "Version": "2021-07-28"},
        timeout=10,
    )
    print(f"✓ Sandbox OAuth refreshed (expires in {new.get('expires_in', '?')}s)")
    print(f"  Verify: GET /locations/{tokens['locationId']} → {r2.status_code}")


if __name__ == "__main__":
    main()
