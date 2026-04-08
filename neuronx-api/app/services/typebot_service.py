"""
Typebot Service — API Client + Form JSON Generator

Creates and manages Typebot conversational forms programmatically.
Generates form structure from questionnaires.yaml so all business logic
stays in YAML config files — no hardcoded form definitions.

Architecture:
  questionnaires.yaml → TypebotService.generate_form_json() → Typebot API → Published form
  Client submits form → Typebot webhook → POST /typebot/webhook → GHL custom fields
"""

import logging
import httpx
from typing import Optional
from datetime import datetime, timezone

from app.config import settings
from app.config_loader import load_yaml_config

logger = logging.getLogger("neuronx.typebot")


class TypebotService:
    """Manages Typebot forms via REST API."""

    def __init__(self):
        self.base_url = settings.typebot_url.rstrip("/") if settings.typebot_url else ""
        self.api_token = settings.typebot_api_token
        self.viewer_url = settings.typebot_viewer_url.rstrip("/") if settings.typebot_viewer_url else ""
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def is_configured(self) -> bool:
        return bool(self.base_url and self.api_token)

    def generate_form_json(self, program_type: str, firm_name: str = "Visa Master Canada",
                            webhook_url: str = "") -> dict:
        """
        Generate Typebot-compatible JSON from questionnaires.yaml.
        Creates a conversational flow with program-specific branching.
        """
        config = load_yaml_config("questionnaires")
        if not config:
            logger.error("questionnaires.yaml not found")
            return {}

        common_questions = config.get("common_questions", [])
        programs = config.get("programs", {})
        program_config = programs.get(program_type, {})
        program_questions = program_config.get("questions", [])

        # Build Typebot groups (sections of the conversation)
        groups = []
        edges = []
        group_counter = 0

        # Group 1: Welcome
        welcome_group_id = f"group_{group_counter}"
        groups.append({
            "id": welcome_group_id,
            "title": "Welcome",
            "graphCoordinates": {"x": 0, "y": 0},
            "blocks": [
                {
                    "id": f"block_welcome",
                    "type": "text",
                    "content": {
                        "richText": [
                            {"type": "p", "children": [
                                {"text": f"Hi! Welcome to {firm_name}. 👋"}
                            ]},
                            {"type": "p", "children": [
                                {"text": "I'll help you complete your onboarding questionnaire. This takes about 10 minutes."}
                            ]},
                        ]
                    }
                }
            ]
        })
        group_counter += 1

        # Group 2: Personal Info (common questions)
        personal_group_id = f"group_{group_counter}"
        personal_blocks = []
        for q in common_questions:
            if q.get("section") == "Personal Information" or q.get("section") == "Contact":
                block = self._question_to_block(q)
                if block:
                    personal_blocks.append(block)

        groups.append({
            "id": personal_group_id,
            "title": "Personal Information",
            "graphCoordinates": {"x": 0, "y": 200},
            "blocks": personal_blocks,
        })
        edges.append({"from": {"groupId": welcome_group_id}, "to": {"groupId": personal_group_id}})
        group_counter += 1

        # Group 3: Family & Background
        family_group_id = f"group_{group_counter}"
        family_blocks = []
        for q in common_questions:
            if q.get("section") in ("Family", "Background"):
                block = self._question_to_block(q)
                if block:
                    family_blocks.append(block)

        groups.append({
            "id": family_group_id,
            "title": "Family & Background",
            "graphCoordinates": {"x": 0, "y": 400},
            "blocks": family_blocks,
        })
        edges.append({"from": {"groupId": personal_group_id}, "to": {"groupId": family_group_id}})
        group_counter += 1

        # Group 4: Program-specific questions
        if program_questions:
            program_group_id = f"group_{group_counter}"
            program_blocks = [
                {
                    "id": "block_program_intro",
                    "type": "text",
                    "content": {
                        "richText": [{"type": "p", "children": [
                            {"text": f"Now let's get the details for your {program_type} application."}
                        ]}]
                    }
                }
            ]
            for q in program_questions:
                block = self._question_to_block(q)
                if block:
                    program_blocks.append(block)

            groups.append({
                "id": program_group_id,
                "title": f"{program_type} Questions",
                "graphCoordinates": {"x": 0, "y": 600},
                "blocks": program_blocks,
            })
            edges.append({"from": {"groupId": family_group_id}, "to": {"groupId": program_group_id}})
            group_counter += 1
            last_group_id = program_group_id
        else:
            last_group_id = family_group_id

        # Group 5: Document Upload
        doc_group_id = f"group_{group_counter}"
        doc_blocks = [
            {
                "id": "block_doc_intro",
                "type": "text",
                "content": {
                    "richText": [{"type": "p", "children": [
                        {"text": "Almost done! Now please upload your key documents. You can upload more later."}
                    ]}]
                }
            },
            {
                "id": "block_passport_upload",
                "type": "file input",
                "options": {
                    "labels": {"placeholder": "Upload your passport (all pages)", "button": "Upload Passport"},
                    "isRequired": True,
                }
            },
            {
                "id": "block_additional_docs",
                "type": "file input",
                "options": {
                    "labels": {"placeholder": "Upload any additional documents you have ready", "button": "Upload Documents"},
                    "isRequired": False,
                    "isMultipleAllowed": True,
                }
            },
        ]
        groups.append({
            "id": doc_group_id,
            "title": "Document Upload",
            "graphCoordinates": {"x": 0, "y": 800},
            "blocks": doc_blocks,
        })
        edges.append({"from": {"groupId": last_group_id}, "to": {"groupId": doc_group_id}})
        group_counter += 1

        # Group 6: Webhook + Thank You
        final_group_id = f"group_{group_counter}"
        final_blocks = [
            {
                "id": "block_thankyou",
                "type": "text",
                "content": {
                    "richText": [
                        {"type": "p", "children": [{"text": "Thank you! Your onboarding is complete. ✅"}]},
                        {"type": "p", "children": [{"text": "Your consultant will review your documents and reach out within 2 business days."}]},
                        {"type": "p", "children": [{"text": f"If you have questions, call us at (647) 931-5181 or reply to your welcome email."}]},
                    ]
                }
            }
        ]

        # Add webhook block if URL provided
        if webhook_url:
            final_blocks.insert(0, {
                "id": "block_webhook",
                "type": "Webhook",
                "options": {
                    "url": webhook_url,
                    "method": "POST",
                    "isAdvancedConfig": False,
                    "isExecutedOnClient": False,
                }
            })

        groups.append({
            "id": final_group_id,
            "title": "Complete",
            "graphCoordinates": {"x": 0, "y": 1000},
            "blocks": final_blocks,
        })
        edges.append({"from": {"groupId": doc_group_id}, "to": {"groupId": final_group_id}})

        # Build complete Typebot JSON
        slug = program_type.lower().replace(" ", "-")
        typebot_json = {
            "version": "6",
            "name": f"{firm_name} — {program_type} Onboarding",
            "groups": groups,
            "edges": edges,
            "variables": [
                {"id": "var_contact_id", "name": "contact_id"},
                {"id": "var_email", "name": "email"},
                {"id": "var_first_name", "name": "first_name"},
                {"id": "var_program", "name": "program_interest", "value": program_type},
            ],
            "theme": {
                "general": {
                    "font": "Inter",
                    "background": {"type": "Color", "content": "#F9FAFB"},
                },
                "chat": {
                    "hostBubbles": {"backgroundColor": "#0F172A", "color": "#FFFFFF"},
                    "guestBubbles": {"backgroundColor": "#E8380D", "color": "#FFFFFF"},
                    "buttons": {"backgroundColor": "#E8380D", "color": "#FFFFFF"},
                    "inputs": {"backgroundColor": "#FFFFFF", "color": "#0F172A"},
                }
            },
            "settings": {
                "general": {
                    "isBrandingEnabled": False,
                    "isInputPrefillEnabled": True,
                },
                "metadata": {
                    "title": f"{firm_name} — Onboarding",
                    "description": f"Complete your {program_type} immigration onboarding",
                }
            },
            "publicId": f"{slug}-onboarding",
        }

        return typebot_json

    def _question_to_block(self, question: dict) -> Optional[dict]:
        """Convert a questionnaire.yaml question to a Typebot block."""
        q_type = question.get("type", "text")
        key = question.get("key", "")
        label = question.get("label", "")

        if q_type == "text" or q_type == "email" or q_type == "phone":
            return {
                "id": f"block_{key}",
                "type": "text input",
                "options": {
                    "labels": {"placeholder": label},
                    "variableId": f"var_{key}",
                    "isRequired": question.get("required", False),
                }
            }
        elif q_type == "select":
            options = question.get("options", [])
            return {
                "id": f"block_{key}",
                "type": "choice input",
                "options": {
                    "items": [{"id": f"item_{key}_{i}", "content": opt} for i, opt in enumerate(options)],
                    "variableId": f"var_{key}",
                    "isMultipleChoice": False,
                }
            }
        elif q_type == "boolean":
            return {
                "id": f"block_{key}",
                "type": "choice input",
                "options": {
                    "items": [
                        {"id": f"item_{key}_yes", "content": "Yes"},
                        {"id": f"item_{key}_no", "content": "No"},
                    ],
                    "variableId": f"var_{key}",
                    "isMultipleChoice": False,
                }
            }
        elif q_type == "number":
            return {
                "id": f"block_{key}",
                "type": "number input",
                "options": {
                    "labels": {"placeholder": label},
                    "variableId": f"var_{key}",
                }
            }
        elif q_type == "date":
            return {
                "id": f"block_{key}",
                "type": "date input",
                "options": {
                    "labels": {"placeholder": label},
                    "variableId": f"var_{key}",
                }
            }
        elif q_type == "textarea":
            return {
                "id": f"block_{key}",
                "type": "text input",
                "options": {
                    "labels": {"placeholder": label},
                    "variableId": f"var_{key}",
                    "isLong": True,
                }
            }

        return None

    async def create_onboarding_form(self, program_type: str, firm_name: str = "Visa Master Canada",
                                       webhook_url: str = None) -> Optional[dict]:
        """Create a Typebot form via API from questionnaires.yaml."""
        if not self.is_configured():
            return None

        # Default webhook URL
        if not webhook_url:
            webhook_url = f"https://neuronx-production-62f9.up.railway.app/typebot/webhook"

        form_json = self.generate_form_json(program_type, firm_name, webhook_url)
        if not form_json:
            return None

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/api/v1/typebots/import",
                    headers=self.headers,
                    json={"typebot": form_json},
                )
                resp.raise_for_status()
                data = resp.json()
                typebot_id = data.get("typebot", {}).get("id")

                if typebot_id:
                    # Publish the form
                    await client.post(
                        f"{self.base_url}/api/v1/typebots/{typebot_id}/publish",
                        headers=self.headers,
                    )

                    slug = program_type.lower().replace(" ", "-")
                    form_url = f"{self.viewer_url}/{slug}-onboarding"

                    logger.info("Created Typebot form: %s → %s", program_type, form_url)
                    return {
                        "typebot_id": typebot_id,
                        "program_type": program_type,
                        "form_url": form_url,
                        "status": "published",
                    }

            except httpx.HTTPError as e:
                logger.error("Typebot API error: %s", e)

        return None

    async def list_forms(self) -> list:
        """List all Typebot forms."""
        if not self.is_configured():
            return []

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                resp = await client.get(
                    f"{self.base_url}/api/v1/typebots",
                    headers=self.headers,
                )
                resp.raise_for_status()
                return resp.json().get("typebots", [])
            except httpx.HTTPError as e:
                logger.error("Typebot list error: %s", e)
                return []
