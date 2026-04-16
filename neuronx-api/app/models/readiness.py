"""
Readiness Assessment Models
Implements R1-R5 dimensions and outcome classification.
See: docs/02_operating_system/operating_spec.md for full state machine.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ProgramInterest(str, Enum):
    EXPRESS_ENTRY = "Express Entry"
    SPOUSAL = "Spousal Sponsorship"
    STUDY_PERMIT = "Study Permit"
    WORK_PERMIT = "Work Permit"
    LMIA = "LMIA"
    PR_RENEWAL = "PR Renewal"
    CITIZENSHIP = "Citizenship"
    VISITOR_VISA = "Visitor Visa"
    OTHER = "Other"


class CurrentLocation(str, Enum):
    IN_CANADA = "In Canada"
    OUTSIDE_CANADA = "Outside Canada"


class TimelineUrgency(str, Enum):
    URGENT = "Urgent"        # < 30 days
    NEAR_TERM = "Near-term"  # 1-3 months
    MEDIUM = "Medium"        # 3-6 months
    LONG_TERM = "Long-term"  # 6+ months


class PriorApplications(str, Enum):
    NONE = "None"
    APPROVED = "Approved"
    HAS_REFUSAL = "Has Refusal"
    COMPLEX = "Complex"


class BudgetAwareness(str, Enum):
    AWARE = "Aware"
    UNAWARE = "Unaware"
    UNCLEAR = "Unclear"


class ReadinessOutcome(str, Enum):
    READY_STANDARD = "ready_standard"    # R1-R5 answered, no flags → nx:assessment:complete
    READY_URGENT = "ready_urgent"        # R3 = Urgent → nx:assessment:complete + nx:urgent
    READY_COMPLEX = "ready_complex"      # Complexity flags → nx:human_escalation
    NOT_READY = "not_ready"              # Prospect not ready → nx:not_ready
    DISQUALIFIED = "disqualified"        # Unrelated inquiry → nx:disqualified


class ReadinessInput(BaseModel):
    contact_id: str = Field(..., description="GHL contact ID")
    r1_program_interest: Optional[ProgramInterest] = None
    r2_current_location: Optional[CurrentLocation] = None
    r3_timeline_urgency: Optional[TimelineUrgency] = None
    r4_prior_applications: Optional[PriorApplications] = None
    r5_budget_awareness: Optional[BudgetAwareness] = None
    transcript_excerpt: Optional[str] = Field(None, max_length=50000, description="Relevant call transcript for complexity detection")
    call_id: Optional[str] = None


class ReadinessScore(BaseModel):
    contact_id: str
    outcome: ReadinessOutcome
    score: int = Field(..., ge=0, le=100, description="0-100 readiness score (>=70 high, 40-69 med, <40 low)")
    confidence: float = Field(..., ge=0.0, le=1.0)
    flags: list[str] = Field(default_factory=list, description="Complexity or escalation flags")
    reasoning: str
    ghl_tags_to_add: list[str] = Field(default_factory=list)
    ghl_fields_to_update: dict = Field(default_factory=dict)


# GHL custom field mapping (must match fields created in GHL)
GHL_FIELD_MAP = {
    "r1_program_interest": "ai_program_interest",
    "r2_current_location": "ai_current_location",
    "r3_timeline_urgency": "ai_timeline_urgency",
    "r4_prior_applications": "ai_prior_applications",
    "r5_budget_awareness": "ai_budget_awareness",
    "readiness_outcome": "ai_readiness_outcome",
    "readiness_score": "ai_readiness_score",
    "consultation_outcome": "ai_consultation_outcome",
}

# Complexity keywords — loaded from config/scoring.yaml (single source of truth)
# Fallback list used only if YAML config unavailable.
# See: docs/04_compliance/trust_boundaries.md
def get_complexity_keywords() -> list[str]:
    """Load complexity keywords from config/scoring.yaml."""
    try:
        from app.config_loader import load_yaml_config
        cfg = load_yaml_config("scoring")
        return cfg.get("complexity_keywords", _FALLBACK_KEYWORDS)
    except Exception:
        return _FALLBACK_KEYWORDS

_FALLBACK_KEYWORDS = [
    "deport", "removal order", "inadmissib",
    "criminal", "misrepresent", "fraud", "fake", "refused",
    "refusal", "detained", "detention", "banned", "visa ban",
    "overstay", "illegal", "undocumented",
]

# For backwards compatibility — other code imports COMPLEXITY_KEYWORDS directly
COMPLEXITY_KEYWORDS = get_complexity_keywords()
