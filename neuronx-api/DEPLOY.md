# NeuronX API — Deployment Guide

## Option A: Railway (Recommended — Free Tier)

1. Go to https://railway.app and sign in with GitHub
2. Click **New Project → Deploy from GitHub repo**
3. Select the `NeuronX` repo, set **Root Directory** to `neuronx-api/`
4. Railway auto-detects Python + Dockerfile
5. Add environment variables in Railway dashboard (copy from `.env.example`)
6. Deploy — Railway gives you a public URL like `https://neuronx-api-production.up.railway.app`
7. Set that URL as VAPI's `serverUrl` in VAPI dashboard

**Cost**: Free tier = 500 hours/month (enough for MVP)

## Option B: Render (Free Tier)

1. Go to https://render.com and sign in with GitHub
2. Click **New → Web Service**
3. Connect your GitHub repo, set **Root Directory** to `neuronx-api/`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables from `.env.example`

**Cost**: Free tier = 750 hours/month (spins down after 15min inactivity)

## Option C: Fly.io

```bash
# Install: brew install flyctl
cd neuronx-api
fly launch  # auto-detects Dockerfile
fly secrets set GHL_ACCESS_TOKEN=... VAPI_API_KEY=...
fly deploy
```

**Cost**: Free tier = 3 shared-cpu VMs

## Post-Deploy Checklist

- [ ] Verify `/health` returns `{"status": "ok"}`
- [ ] Verify `/docs` shows Swagger UI (dev only)
- [ ] Set VAPI assistant's `serverUrl` to deployed URL
- [ ] Set GHL webhook URL to `{deployed_url}/webhooks/ghl`
- [ ] Test: POST to `/score/lead` with sample data
- [ ] Test: POST to `/webhooks/voice` with sample VAPI payload
