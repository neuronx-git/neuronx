"""
NeuronX API Configuration
All settings from environment variables. See .env.example at project root.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    env: str = "development"

    # GHL
    ghl_location_id: str = "FlRL82M0D6nclmKT7eXH"
    ghl_company_id: str = "1H22jRUQWbxzaCaacZjO"
    ghl_api_base_url: str = "https://services.leadconnectorhq.com"
    ghl_access_token: str = ""
    ghl_webhook_secret: str = ""  # Ed25519 public key for GHL webhook verification
    ghl_calendar_id: str = "To1U2KbcvJ0EAX0RGKHS"  # Immigration Consultations calendar
    ghl_pipeline_id: str = "Dtj9nQVd3QjL7bAb3Aiw"  # NeuronX — Immigration Intake

    # VAPI
    vapi_api_key: str = ""
    vapi_base_url: str = "https://api.vapi.ai"
    vapi_webhook_secret: str = ""

    # Anthropic (for consultation briefing generation)
    anthropic_api_key: str = ""
    briefing_model: str = "claude-sonnet-4-6"

    # Database
    database_url: str = ""  # postgresql+asyncpg://user:pass@host:5432/dbname (Railway provides this)

    # Documenso (Block 2)
    documenso_url: str = ""  # https://documenso.your-railway.app
    documenso_api_key: str = ""

    # Service config
    cors_origins: List[str] = ["http://localhost:3000"]
    compliance_log_path: str = "logs/compliance.jsonl"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
