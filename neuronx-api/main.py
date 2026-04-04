"""
NeuronX API — Thin Orchestration Brain
Immigration Consulting SaaS — FastAPI Service

Architecture: GHL (system of record) + NeuronX API (intelligence layer)
See: docs/03_infrastructure/product_boundary.md for what belongs here vs GHL
See: docs/04_compliance/trust_boundaries.md for AI behavioral constraints
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routers import webhooks, scoring, briefings, analytics, trust, documents, cases
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("neuronx")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("NeuronX API starting up — GHL location: %s", settings.ghl_location_id)
    yield
    logger.info("NeuronX API shutting down")


app = FastAPI(
    title="NeuronX API",
    description="AI orchestration layer for immigration consulting intake. Handles webhooks, readiness scoring, consultation prep, and analytics.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.env != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Routers
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(scoring.router, prefix="/score", tags=["Lead Scoring"])
app.include_router(briefings.router, prefix="/briefing", tags=["Consultation Prep"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(trust.router, prefix="/trust", tags=["Trust Boundary"])
app.include_router(documents.router, prefix="/documents", tags=["Document Generation"])
app.include_router(cases.router, prefix="/cases", tags=["Case Processing"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": "neuronx-api", "version": "0.2.0"}


@app.post("/admin/reload-config")
async def reload_config():
    """Reload YAML config files without redeploying. For hot config changes."""
    from app.config_loader import reload_all
    reload_all()
    return {"status": "ok", "message": "All configs reloaded from YAML"}


@app.get("/")
async def root():
    return {
        "service": "NeuronX API",
        "docs": "/docs",
        "health": "/health",
    }
