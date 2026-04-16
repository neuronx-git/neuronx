"""
Multi-Tenant Form Serving Router

GET /form/{tenant_slug}/{form_slug} → Renders branded Typebot form per tenant
Each tenant's branding, bot name, avatar, and Typebot ID come from config/tenants.yaml

Adding a new client: add YAML block to tenants.yaml → push → form live at /form/{slug}/onboarding
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
import os
import logging

from app.config_loader import load_yaml_config

router = APIRouter()
logger = logging.getLogger("neuronx.forms")

# Jinja2 template engine
templates_dir = os.path.join(os.path.dirname(__file__), "..", "..", "templates")
jinja_env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)


def get_tenant(slug: str) -> dict:
    """Load tenant config from tenants.yaml."""
    config = load_yaml_config("tenants")
    tenants = config.get("tenants", {})
    tenant = tenants.get(slug)
    if not tenant:
        raise HTTPException(status_code=404, detail=f"Tenant '{slug}' not found")
    return tenant


@router.get("/{tenant_slug}/{form_slug}", response_class=HTMLResponse)
async def serve_form(tenant_slug: str, form_slug: str):
    """
    Serve a branded conversational form for a specific tenant.

    URL: /form/vmc/onboarding
    Renders: VMC-branded Typebot form with custom colors, avatar, bot name
    """
    tenant = get_tenant(tenant_slug)
    forms = tenant.get("forms", {})
    form_config = forms.get(form_slug)

    if not form_config:
        available = list(forms.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Form '{form_slug}' not found for tenant '{tenant_slug}'. Available: {available}",
        )

    branding = tenant.get("branding", {})

    template = jinja_env.get_template("form.html")
    html = template.render(
        # Tenant info
        tenant_name=tenant.get("name", tenant_slug),
        bot_name=tenant.get("bot_name", "Immigration Assistant"),
        bot_status=tenant.get("bot_status", "Online"),
        avatar_url=tenant.get("avatar_url", "/static/favicon.png"),
        favicon_url=tenant.get("favicon_url", "/static/favicon.png"),

        # Form info
        title=form_config.get("title", "Immigration Assessment"),
        description=form_config.get("description", ""),
        typebot_id=form_config.get("typebot_id"),
        typebot_viewer_url=tenant.get("typebot_viewer_url", "https://viewer-production-366c.up.railway.app"),
        typebot_api_url=tenant.get("typebot_api_url", "https://builder-production-6784.up.railway.app"),

        # Branding
        primary=branding.get("primary", "#1E3A5F"),
        accent=branding.get("accent", "#E8380D"),
        background=branding.get("background", "#F8FAFC"),
        text_on_primary=branding.get("text_on_primary", "#FFFFFF"),
        text_on_accent=branding.get("text_on_accent", "#FFFFFF"),
        input_border=branding.get("input_border", "#E2E8F0"),
        input_focus=branding.get("input_focus", "#1E3A5F"),
        font=branding.get("font", "Inter, -apple-system, sans-serif"),
    )

    logger.info("Served form: /form/%s/%s", tenant_slug, form_slug)
    return HTMLResponse(content=html)


@router.get("/{tenant_slug}", response_class=HTMLResponse)
async def list_forms(tenant_slug: str):
    """List available forms for a tenant (for debugging/testing)."""
    tenant = get_tenant(tenant_slug)
    forms = tenant.get("forms", {})
    links = "".join(
        f'<li><a href="/form/{tenant_slug}/{slug}">{cfg.get("title", slug)}</a></li>'
        for slug, cfg in forms.items()
    )
    return HTMLResponse(
        content=f"<h2>{tenant.get('name')} Forms</h2><ul>{links}</ul>",
    )
