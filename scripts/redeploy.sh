#!/bin/bash
# NeuronX — Force Redeploy Script
# Use when Railway auto-deploy gets stuck or doesn't trigger.
#
# Usage: ./scripts/redeploy.sh
#
# Prerequisites:
#   1. railway CLI installed: brew install railway
#   2. Logged in: railway login
#   3. Linked to project: railway link (select NeuronX API service)
#
# What this does:
#   1. Verifies you're on the right branch with latest code
#   2. Pushes to GitHub
#   3. Triggers Railway redeploy
#   4. Waits for deployment to complete
#   5. Runs health check

set -e

echo "=== NeuronX Redeploy Script ==="
echo ""

# Step 1: Verify branch and commit
BRANCH=$(git branch --show-current)
COMMIT=$(git rev-parse --short HEAD)
echo "Branch: $BRANCH"
echo "Commit: $COMMIT"
echo ""

if [ "$BRANCH" != "main" ]; then
    echo "WARNING: Not on main branch. Railway deploys from main."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

# Step 2: Push to GitHub
echo "Pushing to GitHub..."
git push origin main || echo "Push failed or nothing to push"
echo ""

# Step 3: Trigger Railway redeploy
echo "Triggering Railway redeploy..."
railway deployment redeploy 2>&1 || {
    echo ""
    echo "ERROR: Railway redeploy failed."
    echo "Try: railway login && railway link && railway deployment redeploy"
    exit 1
}
echo ""

# Step 4: Wait for deploy
echo "Waiting for deployment (checking every 10s, max 5 min)..."
for i in $(seq 1 30); do
    HEALTH=$(curl -s https://neuronx-production-62f9.up.railway.app/health 2>/dev/null)
    DEEP=$(curl -s https://neuronx-production-62f9.up.railway.app/health/deep 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','unknown'))" 2>/dev/null)

    if [ "$DEEP" = "ok" ] || [ "$DEEP" = "degraded" ]; then
        echo ""
        echo "=== DEPLOYED SUCCESSFULLY ==="
        echo "Health: $HEALTH"
        echo "Deep health: $DEEP"
        echo ""
        echo "Verify: https://neuronx-production-62f9.up.railway.app/health/deep"
        exit 0
    fi

    echo "  Check $i: still deploying..."
    sleep 10
done

echo ""
echo "Deploy timeout (5 min). Check Railway dashboard manually."
echo "Dashboard: https://railway.app/project"
