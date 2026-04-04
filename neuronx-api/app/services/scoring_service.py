"""
Lead Readiness Scoring Service

Implements R1-R5 dimension scoring and outcome classification.
Score is 0-100 to align with WF-04B routing thresholds:
  >= 70 → nx:score:high → WF-04 (booking invite)
  40-69 → nx:score:med  → WF-12 (operator review)
  < 40  → nx:score:low  → WF-11 (nurture)

See: docs/02_operating_system/operating_spec.md
See: docs/06_execution/WORKFLOW_REFERENCE.md (WF-04B)
"""

from typing import Optional
from datetime import datetime, timezone

from app.models.readiness import (
    ReadinessScore, ReadinessOutcome,
    GHL_FIELD_MAP,
)
from app.config_loader import load_scoring_config
from app.utils.compliance_log import log_event


class ScoringService:
    """
    Scores lead readiness on a 0-100 scale from R1-R5 dimensions.

    Scoring logic:
    - Each R dimension answered: +16 points base (max 80 for R1-R5)
    - Urgency bonus: Urgent +10, Near-term +5
    - Long-term penalty: -5
    - Prior refusal: -10 (complex but still valid)
    - Budget unaware: -5
    - Budget aware: +10 bonus
    - Complexity keywords: forces ready_complex regardless of score

    WF-04B thresholds: >=70 high, 40-69 med, <40 low
    """

    def score(
        self,
        contact_id: str,
        r1_program_interest: Optional[str] = None,
        r2_current_location: Optional[str] = None,
        r3_timeline_urgency: Optional[str] = None,
        r4_prior_applications: Optional[str] = None,
        r5_budget_awareness: Optional[str] = None,
        transcript_excerpt: Optional[str] = None,
        call_id: Optional[str] = None,
    ) -> ReadinessScore:

        cfg = load_scoring_config()
        base = cfg["dimension_base_points"]
        mods = cfg["modifiers"]

        score = 0
        flags = []
        answered = 0

        # R1: Program Interest
        if r1_program_interest:
            answered += 1
            score += base

        # R2: Current Location
        if r2_current_location:
            answered += 1
            score += base

        # R3: Timeline Urgency
        if r3_timeline_urgency:
            answered += 1
            score += base
            urgency = r3_timeline_urgency.lower().replace("-", "_").replace(" ", "_")
            if urgency in ("urgent", "urgent_(30_days)", "urgent (30 days)"):
                score += mods["urgent_timeline_bonus"]
                flags.append("urgent_timeline")
            elif urgency in ("near_term", "near-term", "near_term_(1_3_months)", "near-term (1-3 months)"):
                score += mods["near_term_bonus"]
            elif urgency in ("long_term", "long-term", "long_term_(6+_months)", "long-term (6+ months)"):
                score += mods["long_term_penalty"]

        # R4: Prior Applications
        if r4_prior_applications:
            answered += 1
            score += base
            prior = r4_prior_applications.lower().replace(" ", "_")
            if prior in ("has_refusal", "has refusal"):
                score += mods["prior_refusal_penalty"]
                flags.append("prior_refusal")
            elif prior == "complex":
                score += mods["complex_history_penalty"]
                flags.append("complex_history")

        # R5: Budget Awareness
        if r5_budget_awareness:
            answered += 1
            score += base
            budget = r5_budget_awareness.lower()
            if budget == "aware":
                score += mods["budget_aware_bonus"]
            elif budget == "unaware":
                score += mods["budget_unaware_penalty"]
                flags.append("budget_education_needed")

        # Clamp score to 0-100
        score = max(0, min(100, score))
        confidence = answered / 5.0

        # Check for complexity keywords from config (requires human escalation)
        if transcript_excerpt:
            transcript_lower = transcript_excerpt.lower()
            keywords = cfg.get("complexity_keywords", [])
            complexity_found = [kw for kw in keywords if kw in transcript_lower]
            if complexity_found:
                flags.extend([f"complexity:{kw}" for kw in complexity_found])
                flags.append("requires_human_escalation")

        # Determine outcome
        outcome = self._determine_outcome(answered, score, flags)

        # Build GHL field updates
        ghl_fields = self._build_ghl_fields(
            r1_program_interest, r2_current_location, r3_timeline_urgency,
            r4_prior_applications, r5_budget_awareness, outcome, score,
        )

        # Build GHL tags (aligned with WF-04B routing)
        ghl_tags = self._outcome_to_tags(outcome, score, flags)

        result = ReadinessScore(
            contact_id=contact_id,
            outcome=outcome,
            score=score,
            confidence=confidence,
            flags=flags,
            reasoning=self._build_reasoning(answered, score, outcome, flags),
            ghl_tags_to_add=ghl_tags,
            ghl_fields_to_update=ghl_fields,
        )

        log_event("lead_scored", {
            "contact_id": contact_id,
            "call_id": call_id,
            "outcome": outcome.value,
            "score": score,
            "confidence": confidence,
            "flags": flags,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        })

        return result

    def _determine_outcome(self, answered: int, score: int, flags: list) -> ReadinessOutcome:
        cfg = load_scoring_config()
        med = cfg["thresholds"]["med"]
        min_dims = cfg.get("min_dimensions_for_ready", 2)

        # Complexity keywords ALWAYS override — human must review
        if "requires_human_escalation" in flags:
            return ReadinessOutcome.READY_COMPLEX
        if answered < min_dims:
            return ReadinessOutcome.NOT_READY
        # Urgent only if no complexity flags
        if "urgent_timeline" in flags and score >= med:
            return ReadinessOutcome.READY_URGENT
        if score >= med:
            return ReadinessOutcome.READY_STANDARD
        return ReadinessOutcome.NOT_READY

    def _outcome_to_tags(self, outcome: ReadinessOutcome, score: int, flags: list) -> list[str]:
        """Map outcome + score to GHL tags using config thresholds."""
        cfg = load_scoring_config()
        high = cfg["thresholds"]["high"]
        med = cfg["thresholds"]["med"]

        tags = []
        if score >= high:
            tags.append("nx:score:high")
        elif score >= med:
            tags.append("nx:score:med")
        else:
            tags.append("nx:score:low")

        # Outcome-specific tags
        if outcome in (ReadinessOutcome.READY_STANDARD, ReadinessOutcome.READY_URGENT):
            tags.append("nx:assessment:complete")
        if outcome == ReadinessOutcome.READY_URGENT:
            tags.append("nx:urgent")
        if outcome == ReadinessOutcome.READY_COMPLEX:
            tags.append("nx:human_escalation")
        if outcome == ReadinessOutcome.NOT_READY:
            tags.append("nx:not_ready")
        if outcome == ReadinessOutcome.DISQUALIFIED:
            tags.append("nx:disqualified")

        return tags

    def _build_ghl_fields(
        self, r1, r2, r3, r4, r5, outcome, score,
    ) -> dict:
        fields = {}
        if r1:
            fields[GHL_FIELD_MAP["r1_program_interest"]] = str(r1)
        if r2:
            fields[GHL_FIELD_MAP["r2_current_location"]] = str(r2)
        if r3:
            fields[GHL_FIELD_MAP["r3_timeline_urgency"]] = str(r3)
        if r4:
            fields[GHL_FIELD_MAP["r4_prior_applications"]] = str(r4)
        if r5:
            fields[GHL_FIELD_MAP["r5_budget_awareness"]] = str(r5)
        fields[GHL_FIELD_MAP["readiness_outcome"]] = outcome.value
        fields[GHL_FIELD_MAP["readiness_score"]] = str(score)
        fields["assessment_completed_at"] = datetime.now(tz=timezone.utc).isoformat()
        fields["assessed_by"] = "neuronx-api"
        return fields

    def _build_reasoning(self, answered: int, score: int, outcome: ReadinessOutcome, flags: list) -> str:
        tier = "HIGH" if score >= 70 else "MED" if score >= 40 else "LOW"
        parts = [
            f"Answered {answered}/5 dimensions.",
            f"Score: {score}/100 ({tier}).",
            f"Outcome: {outcome.value}.",
        ]
        if flags:
            parts.append(f"Flags: {', '.join(flags)}.")
        return " ".join(parts)
