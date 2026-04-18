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
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import os

from app.routers import webhooks, scoring, briefings, analytics, trust, documents, cases, sync, signatures, demo, typebot, clients, forms, dependents, doc_extract, users, case_viewer
from app.config import settings

limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])

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
    version="0.5.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.env != "production" else None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Adds OWASP-recommended security headers to every response."""
    response = await call_next(request)
    response.headers.setdefault("strict-transport-security", "max-age=31536000; includeSubDomains")
    response.headers.setdefault("x-content-type-options", "nosniff")
    response.headers.setdefault("x-frame-options", "DENY")
    response.headers.setdefault("referrer-policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("permissions-policy", "geolocation=(), microphone=(), camera=()")
    # CSP only for HTML responses (forms) to avoid breaking API JSON consumers
    ct = response.headers.get("content-type", "")
    if "text/html" in ct:
        response.headers.setdefault(
            "content-security-policy",
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://*.railway.app https://cdn.tailwindcss.com; "
            "style-src 'self' 'unsafe-inline' https://rsms.me; "
            "font-src 'self' https://rsms.me data:; "
            "frame-src https://*.railway.app 'self'; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://*.railway.app"
        )
    return response


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Simple per-IP rate limiter. 200 req/min default; webhooks exempted."""
    # Exempt health checks and webhooks (webhooks have their own signature verification)
    path = request.url.path
    if path.startswith("/health") or path.startswith("/webhooks/") or path == "/":
        return await call_next(request)

    from collections import defaultdict
    import time
    if not hasattr(app.state, "_rate_buckets"):
        app.state._rate_buckets = defaultdict(list)

    ip = request.client.host if request.client else "unknown"
    now = time.time()
    bucket = app.state._rate_buckets[ip]
    # Keep only requests within the last 60 seconds
    bucket[:] = [t for t in bucket if now - t < 60]

    if len(bucket) >= 200:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded: 200 requests/minute"},
            headers={"retry-after": "60"},
        )
    bucket.append(now)
    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-GHL-Signature", "X-GHL-Timestamp", "X-Vapi-Signature", "X-Admin-Key"],
)

# Routers
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(scoring.router, prefix="/score", tags=["Lead Scoring"])
app.include_router(briefings.router, prefix="/briefing", tags=["Consultation Prep"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(trust.router, prefix="/trust", tags=["Trust Boundary"])
app.include_router(documents.router, prefix="/documents", tags=["Document Generation"])
app.include_router(cases.router, prefix="/cases", tags=["Case Processing"])
app.include_router(case_viewer.router, prefix="/cases", tags=["Case Viewer (UI)"])
app.include_router(sync.router, prefix="/sync", tags=["Data Sync"])
app.include_router(signatures.router, prefix="/signatures", tags=["E-Signatures"])
app.include_router(demo.router, prefix="/demo", tags=["Demo Data"])
app.include_router(typebot.router, prefix="/typebot", tags=["Smart Forms (Typebot)"])
app.include_router(clients.router, prefix="/clients", tags=["Client Data (Chrome Extension)"])
app.include_router(forms.router, prefix="/form", tags=["Multi-Tenant Forms"])  # forms.neuronx.co/form/vmc/onboarding
app.include_router(dependents.router, prefix="/dependents", tags=["Case Dependents"])
app.include_router(doc_extract.router, prefix="/extract", tags=["Document OCR Extraction"])
app.include_router(users.router, prefix="/users", tags=["Users / Team"])


@app.get("/health")
async def health():
    from app.database import is_db_configured
    return {
        "status": "ok",
        "service": "neuronx-api",
        "version": "0.5.0",
        "database": "connected" if is_db_configured() else "not configured",
    }


@app.get("/health/deep")
async def health_deep():
    """
    Deep health check — probes all external dependencies.
    Use for production monitoring and pre-deploy validation.
    """
    import httpx
    from app.database import is_db_configured, get_session
    from app.config_loader import load_scoring_config, load_programs_config, load_trust_config

    checks = {}

    # Database connectivity
    if is_db_configured():
        try:
            from app.database import async_session_factory
            if async_session_factory:
                async with async_session_factory() as session:
                    from sqlalchemy import text
                    await session.execute(text("SELECT 1"))
                checks["database"] = "ok"
            else:
                checks["database"] = "engine not initialized"
        except Exception as e:
            checks["database"] = f"error: {str(e)[:100]}"
    else:
        checks["database"] = "not configured"

    # GHL API reachability
    if not settings.ghl_access_token:
        checks["ghl_api"] = "token not configured"
    else:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(
                    f"{settings.ghl_api_base_url}/locations/{settings.ghl_location_id}",
                    headers={"Authorization": f"Bearer {settings.ghl_access_token}"},
                )
                checks["ghl_api"] = "ok" if r.status_code in (200, 401) else f"status: {r.status_code}"
        except Exception as e:
            checks["ghl_api"] = f"unreachable: {str(e)[:80]}"

    # YAML config parsing
    try:
        load_scoring_config()
        load_programs_config()
        load_trust_config()
        checks["configs"] = "ok (3/3 loaded)"
    except Exception as e:
        checks["configs"] = f"error: {str(e)[:100]}"

    # Typebot reachability
    if not settings.typebot_url or not settings.typebot_api_token:
        checks["typebot"] = "not configured"
    else:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(
                    f"{settings.typebot_url}/api/v1/typebots",
                    headers={"Authorization": f"Bearer {settings.typebot_api_token}"},
                    params={"workspaceId": "cmnrfqc6z000034qx46joy6hf"},
                )
                checks["typebot"] = "ok" if r.status_code in (200, 401, 403) else f"status: {r.status_code}"
        except Exception as e:
            checks["typebot"] = f"unreachable: {str(e)[:80]}"

    all_ok = all(v in ("ok", "configured", "not configured") or v.startswith("ok") for v in checks.values())

    return {
        "status": "ok" if all_ok else "degraded",
        "service": "neuronx-api",
        "version": "0.5.0",
        "checks": checks,
    }


@app.get("/health/smoke")
async def smoke_test():
    """
    Production smoke test — verifies end-to-end data flow.
    Checks: DB read, case listing, config load, GHL reachability.
    Use for daily automated monitoring.
    """
    import httpx
    from app.database import async_session_factory
    from app.config_loader import load_scoring_config, load_programs_config
    from sqlalchemy import text

    results = {}
    passed = 0
    total = 0

    # Test 1: DB read
    total += 1
    try:
        if async_session_factory:
            async with async_session_factory() as session:
                row = await session.execute(text("SELECT COUNT(*) as cnt FROM cases"))
                count = row.scalar()
                results["db_cases"] = {"status": "ok", "count": count}
                passed += 1
        else:
            results["db_cases"] = {"status": "skip", "reason": "no DB"}
    except Exception as e:
        results["db_cases"] = {"status": "fail", "error": str(e)[:100]}

    # Test 2: Config load
    total += 1
    try:
        programs = load_programs_config()
        scoring = load_scoring_config()
        results["configs"] = {"status": "ok", "programs": len(programs.get("programs", {})), "scoring_loaded": bool(scoring)}
        passed += 1
    except Exception as e:
        results["configs"] = {"status": "fail", "error": str(e)[:100]}

    # Test 3: Case lifecycle API
    total += 1
    try:
        from app.services.case_service import VALID_TRANSITIONS, ALL_STAGES
        assert len(ALL_STAGES) == 10
        assert len(VALID_TRANSITIONS) == 10
        results["case_lifecycle"] = {"status": "ok", "stages": len(ALL_STAGES)}
        passed += 1
    except Exception as e:
        results["case_lifecycle"] = {"status": "fail", "error": str(e)[:100]}

    # Test 4: GHL API reachability
    total += 1
    if settings.ghl_access_token:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(
                    f"{settings.ghl_api_base_url}/locations/{settings.ghl_location_id}",
                    headers={"Authorization": f"Bearer {settings.ghl_access_token}"},
                )
                results["ghl_api"] = {"status": "ok" if r.status_code in (200, 401) else "degraded", "http_status": r.status_code}
                if r.status_code in (200, 401):
                    passed += 1
        except Exception as e:
            results["ghl_api"] = {"status": "fail", "error": str(e)[:100]}
    else:
        results["ghl_api"] = {"status": "skip", "reason": "no token"}

    return {
        "status": "pass" if passed == total else "partial" if passed > 0 else "fail",
        "passed": passed,
        "total": total,
        "checks": results,
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


@app.post("/admin/install-views")
async def install_views(x_admin_key: str = Header(...)):
    """Install Metabase SQL views for dashboards. Requires X-Admin-Key header."""
    admin_key = os.getenv("ADMIN_API_KEY", "neuronx-admin-dev")
    if x_admin_key != admin_key:
        raise HTTPException(status_code=401, detail="Invalid admin key")

    from app.database import async_session_factory
    from sqlalchemy import text

    if not async_session_factory:
        raise HTTPException(status_code=500, detail="Database not configured")

    sql_path = os.path.join(os.path.dirname(__file__), "scripts", "metabase_views.sql")
    if not os.path.exists(sql_path):
        raise HTTPException(status_code=500, detail="metabase_views.sql not found")

    with open(sql_path) as f:
        sql = f.read()

    # Execute each CREATE VIEW statement in its own transaction
    views_created = 0
    errors = []
    for stmt in sql.split(";"):
        lines = [l for l in stmt.strip().splitlines() if l.strip() and not l.strip().startswith("--")]
        clean = "\n".join(lines).strip()
        if clean:
            try:
                async with async_session_factory() as session:
                    await session.execute(text(clean))
                    await session.commit()
                    if "CREATE" in clean.upper():
                        views_created += 1
            except Exception as e:
                errors.append({"sql": clean[:80], "error": str(e)[:200]})

    result = {"status": "ok", "views_created": views_created}
    if errors:
        result["errors"] = errors
    return result


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

# Railway deploy — GitHub repo reconnected 2026-04-16
