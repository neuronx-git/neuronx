"""
Multi-Tenant Form Serving Router

GET /form/{tenant_slug}/{form_slug} → Renders branded Typebot form per tenant
Each tenant's branding, bot name, avatar, and Typebot ID come from config/tenants.yaml

Adding a new client: add YAML block to tenants.yaml → push → form live at /form/{slug}/onboarding
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from urllib.parse import urlencode, quote_plus
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


def _render_form(tenant: dict, form_config: dict, tenant_slug: str, prefill_params: str = "") -> str:
    """Render the form HTML with tenant branding and optional prefill params."""
    branding = tenant.get("branding", {})
    template = jinja_env.get_template("form.html")
    return template.render(
        tenant_name=tenant.get("name", tenant_slug),
        bot_name=tenant.get("bot_name", "Immigration Assistant"),
        bot_status=tenant.get("bot_status", "Online"),
        avatar_url=tenant.get("avatar_url", "/static/favicon.png"),
        favicon_url=tenant.get("favicon_url", "/static/favicon.png"),
        title=form_config.get("title", "Immigration Assessment"),
        description=form_config.get("description", ""),
        typebot_id=form_config.get("typebot_id"),
        typebot_viewer_url=tenant.get("typebot_viewer_url", "https://viewer-production-366c.up.railway.app"),
        typebot_api_url=tenant.get("typebot_api_url", "https://builder-production-6784.up.railway.app"),
        prefill_params=prefill_params,
        primary=branding.get("primary", "#1E3A5F"),
        accent=branding.get("accent", "#E8380D"),
        background=branding.get("background", "#F8FAFC"),
        text_on_primary=branding.get("text_on_primary", "#FFFFFF"),
        text_on_accent=branding.get("text_on_accent", "#FFFFFF"),
        input_border=branding.get("input_border", "#E2E8F0"),
        input_focus=branding.get("input_focus", "#1E3A5F"),
        font=branding.get("font", "Inter, -apple-system, sans-serif"),
    )


def _get_form_config(tenant: dict, form_slug: str, tenant_slug: str) -> dict:
    """Get form config or raise 404."""
    forms = tenant.get("forms", {})
    form_config = forms.get(form_slug)
    if not form_config:
        available = list(forms.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Form '{form_slug}' not found for tenant '{tenant_slug}'. Available: {available}",
        )
    return form_config


@router.get("/{tenant_slug}/{form_slug}", response_class=HTMLResponse)
async def serve_form(tenant_slug: str, form_slug: str):
    """
    Serve a branded conversational form for a specific tenant.

    Shared URL: /form/vmc/onboarding
    With prefill: /form/vmc/onboarding?full_name=Priya&program_interest=Express+Entry
    """
    tenant = get_tenant(tenant_slug)
    form_config = _get_form_config(tenant, form_slug, tenant_slug)
    html = _render_form(tenant, form_config, tenant_slug)
    logger.info("Served form: /form/%s/%s", tenant_slug, form_slug)
    return HTMLResponse(content=html)


@router.get("/{tenant_slug}/{form_slug}/{contact_id}", response_class=HTMLResponse)
async def serve_form_for_client(tenant_slug: str, form_slug: str, contact_id: str):
    """
    Serve a client-specific form pre-filled with GHL contact data.

    URL: /form/vmc/onboarding/abc123
    Flow:
      1. Fetch contact from GHL by contact_id
      2. Map known fields to Typebot prefill params
      3. Render form with pre-populated fields
      4. Client sees their data already filled in
      5. On submit, webhook uses contact_id to sync back to GHL
    """
    from app.services.ghl_client import GHLClient

    tenant = get_tenant(tenant_slug)
    form_config = _get_form_config(tenant, form_slug, tenant_slug)

    # Fetch existing data from GHL
    prefill = {"contact_id": contact_id}
    try:
        ghl = GHLClient(location_id=tenant.get("ghl_location_id"))
        contact = await ghl.get_contact(contact_id)

        # Standard fields
        first = contact.get("firstName", "")
        last = contact.get("lastName", "")
        if first or last:
            prefill["full_name"] = f"{first} {last}".strip()
        if contact.get("email"):
            prefill["email"] = contact["email"]
        if contact.get("phone"):
            prefill["phone"] = contact["phone"]
        if contact.get("country"):
            prefill["country_of_citizenship"] = contact["country"]

        # Custom fields (Phase 1 VAPI data + previous form submissions)
        for field in contact.get("customFields", []):
            key = field.get("id", "")
            val = field.get("value", "")
            if val:
                # Map GHL custom field keys to Typebot variable names
                ghl_to_form = {
                    "ai_program_interest": "program_interest",
                    "ai_current_location": "current_country",
                    "full_name": "full_name",
                    "date_of_birth": "date_of_birth",
                    "passport_number": "passport_number",
                    "passport_expiry": "passport_expiry",
                    "country_of_citizenship": "country_of_citizenship",
                    "marital_status": "marital_status",
                    "r2_education_level": "education_level",
                    "settlement_funds": "settlement_funds",
                    "language_test_type": "language_test_type",
                    "sponsor_name": "sponsor_name",
                    "employer_name": "employer_name",
                    "job_title": "job_title",
                    "dli_name": "dli_name",
                    "program_name": "program_name",
                }
                form_key = ghl_to_form.get(key)
                if form_key and form_key not in prefill:
                    prefill[form_key] = val

        logger.info("Pre-filled %d fields for contact %s", len(prefill), contact_id)

    except Exception as e:
        logger.warning("Could not fetch GHL contact %s: %s — serving empty form", contact_id, e)

    # Build query string for Typebot prefill
    prefill_qs = "?" + urlencode(prefill, quote_via=quote_plus) if prefill else ""
    html = _render_form(tenant, form_config, tenant_slug, prefill_params=prefill_qs)
    logger.info("Served client form: /form/%s/%s/%s (%d prefilled)", tenant_slug, form_slug, contact_id, len(prefill))
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
