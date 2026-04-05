#!/bin/bash
PORT="${1:-9222}"
echo "Launching Chrome with remote debugging on port $PORT..."
echo "After Chrome opens, log into GHL if not already logged in."
echo "Then Playwright MCP can connect via: --cdp-endpoint http://127.0.0.1:$PORT"
echo ""

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port="$PORT" \
  --no-first-run \
  --no-default-browser-check \
  "https://app.gohighlevel.com/v2/location/FlRL82M0D6nclmKT7eXH/dashboard" &

echo "Chrome PID: $!"
echo "Verify at: http://127.0.0.1:$PORT/json/version"
