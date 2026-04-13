"""
NeuronX API — Thin Orchestration Brain
Immigration Consulting SaaS — FastAPI Service

Architecture: GHL (system of record) + NeuronX API (intelligence layer)
See: docs/03_infrastructure/product_boundary.md for what belongs here vs GHL
See: docs/04_compliance/trust_boundaries.md for AI behavioral constraints
"""

from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from app.routers import webhooks, scoring, briefings, analytics, trust, documents, cases, sync, signatures, demo, typebot, clients, forms, dependents, doc_extract
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("neuronx")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("NeuronX API starting up — GHL location: %s", settings.ghl_location_id)
    # Initialize database if configured
    from app.database import init_db, close_db, is_db_configured
    if is_db_configured():
        await init_db()
        logger.info("Database connected")
    else:
        logger.info("No DATABASE_URL — running without database persistence")
    yield
    if is_db_configured():
        await close_db()
    logger.info("NeuronX API shutting down")


app = FastAPI(
    title="NeuronX API",
    description="AI orchestration layer for immigration consulting intake. Handles webhooks, readiness scoring, consultation prep, and analytics.",
    version="0.4.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.env != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-GHL-Signature", "X-GHL-Timestamp", "X-Vapi-Signature"],
)

# Routers
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(scoring.router, prefix="/score", tags=["Lead Scoring"])
app.include_router(briefings.router, prefix="/briefing", tags=["Consultation Prep"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(trust.router, prefix="/trust", tags=["Trust Boundary"])
app.include_router(documents.router, prefix="/documents", tags=["Document Generation"])
app.include_router(cases.router, prefix="/cases", tags=["Case Processing"])
app.include_router(sync.router, prefix="/sync", tags=["Data Sync"])
app.include_router(signatures.router, prefix="/signatures", tags=["E-Signatures"])
app.include_router(demo.router, prefix="/demo", tags=["Demo Data"])
app.include_router(typebot.router, prefix="/typebot", tags=["Smart Forms (Typebot)"])
app.include_router(clients.router, prefix="/clients", tags=["Client Data (Chrome Extension)"])
app.include_router(forms.router, prefix="/form", tags=["Multi-Tenant Forms"])  # forms.neuronx.co/form/vmc/onboarding
app.include_router(dependents.router, prefix="/dependents", tags=["Case Dependents"])
app.include_router(doc_extract.router, prefix="/extract", tags=["Document OCR Extraction"])


@app.get("/health")
async def health():
    from app.database import is_db_configured
    return {
        "status": "ok",
        "service": "neuronx-api",
        "version": "0.4.0",
        "database": "connected" if is_db_configured() else "not configured",
    }


@app.post("/admin/reload-config")
async def reload_config(x_admin_key: str = Header(...)):
    """Reload YAML config files without redeploying. Requires X-Admin-Key header."""
    admin_key = os.getenv("ADMIN_API_KEY", "neuronx-admin-dev")
    if x_admin_key != admin_key:
        raise HTTPException(status_code=401, detail="Invalid admin key")
    from app.config_loader import reload_all
    reload_all()
    return {"status": "ok", "message": "All configs reloaded from YAML"}


# Serve static assets (avatar, favicon, images)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    return {
        "service": "NeuronX API",
        "docs": "/docs",
        "health": "/health",
    }
