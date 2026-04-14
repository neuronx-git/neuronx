"""
Unit Tests — Config Loader

Tests YAML config loading, caching, and reload functionality.
All 7 config files must parse without error.
"""

import pytest
from app.config_loader import (
    load_scoring_config,
    load_programs_config,
    load_trust_config,
    load_yaml_config,
    reload_all,
)


@pytest.mark.unit
class TestScoringConfig:
    """Tests for load_scoring_config()."""

    def test_returns_dict(self):
        reload_all()
        config = load_scoring_config()
        assert isinstance(config, dict)

    def test_has_thresholds(self):
        reload_all()
        config = load_scoring_config()
        assert "thresholds" in config
        assert "high" in config["thresholds"]
        assert "med" in config["thresholds"]

    def test_threshold_values(self):
        reload_all()
        config = load_scoring_config()
        assert config["thresholds"]["high"] == 70
        assert config["thresholds"]["med"] == 40

    def test_has_dimension_base_points(self):
        reload_all()
        config = load_scoring_config()
        assert "dimension_base_points" in config
        assert config["dimension_base_points"] == 16

    def test_has_modifiers(self):
        reload_all()
        config = load_scoring_config()
        assert "modifiers" in config
        mods = config["modifiers"]
        assert "urgent_timeline_bonus" in mods
        assert "near_term_bonus" in mods
        assert "long_term_penalty" in mods
        assert "prior_refusal_penalty" in mods
        assert "budget_aware_bonus" in mods
        assert "budget_unaware_penalty" in mods

    def test_has_complexity_keywords(self):
        reload_all()
        config = load_scoring_config()
        assert "complexity_keywords" in config
        assert isinstance(config["complexity_keywords"], list)
        assert len(config["complexity_keywords"]) > 0

    def test_has_min_dimensions_for_ready(self):
        reload_all()
        config = load_scoring_config()
        assert "min_dimensions_for_ready" in config
        assert config["min_dimensions_for_ready"] == 2


@pytest.mark.unit
class TestProgramsConfig:
    """Tests for load_programs_config()."""

    def test_returns_dict(self):
        reload_all()
        config = load_programs_config()
        assert isinstance(config, dict)

    def test_has_programs(self):
        """Programs config contains program entries."""
        reload_all()
        config = load_programs_config()
        # programs.yaml has a "programs" key at top level,
        # load_programs_config returns the programs dict inside it
        assert isinstance(config, dict)


@pytest.mark.unit
class TestTrustConfig:
    """Tests for load_trust_config()."""

    def test_returns_dict(self):
        reload_all()
        config = load_trust_config()
        assert isinstance(config, dict)

    def test_has_escalation_triggers(self):
        reload_all()
        config = load_trust_config()
        assert "escalation_triggers" in config
        triggers = config["escalation_triggers"]
        assert isinstance(triggers, dict)
        assert len(triggers) > 0

    def test_has_ai_violations(self):
        reload_all()
        config = load_trust_config()
        assert "ai_violations" in config
        violations = config["ai_violations"]
        assert isinstance(violations, dict)
        assert len(violations) > 0

    def test_escalation_trigger_categories(self):
        """All 6 escalation categories are present."""
        reload_all()
        config = load_trust_config()
        triggers = config["escalation_triggers"]
        expected = [
            "eligibility_question",
            "deportation_removal",
            "inadmissibility",
            "fraud_misrepresentation",
            "emotional_distress",
            "explicit_human_request",
        ]
        for cat in expected:
            assert cat in triggers, f"Missing escalation category: {cat}"

    def test_ai_violation_categories(self):
        """All 3 violation categories are present."""
        reload_all()
        config = load_trust_config()
        violations = config["ai_violations"]
        expected = ["eligibility_assessment", "legal_advice", "outcome_promises"]
        for cat in expected:
            assert cat in violations, f"Missing violation category: {cat}"


@pytest.mark.unit
class TestGenericYamlLoader:
    """Tests for load_yaml_config()."""

    def test_load_scoring(self):
        config = load_yaml_config("scoring")
        assert isinstance(config, dict)
        assert "thresholds" in config

    def test_load_trust(self):
        config = load_yaml_config("trust")
        assert isinstance(config, dict)
        assert "escalation_triggers" in config

    def test_load_programs(self):
        config = load_yaml_config("programs")
        assert isinstance(config, dict)

    def test_load_tenants(self):
        config = load_yaml_config("tenants")
        assert isinstance(config, dict)
        assert "tenants" in config

    def test_load_questionnaires(self):
        config = load_yaml_config("questionnaires")
        assert isinstance(config, dict)

    def test_load_ircc_field_mappings(self):
        config = load_yaml_config("ircc_field_mappings")
        assert isinstance(config, dict)

    def test_load_case_emails(self):
        config = load_yaml_config("case_emails")
        assert isinstance(config, dict)

    def test_nonexistent_returns_empty_dict(self):
        """Loading a nonexistent config returns empty dict."""
        config = load_yaml_config("this_config_does_not_exist_xyz")
        assert config == {}


@pytest.mark.unit
class TestReloadAll:
    """Tests for reload_all() cache clearing."""

    def test_reload_clears_scoring_cache(self):
        """reload_all() clears the scoring config LRU cache."""
        # Warm the cache
        load_scoring_config()
        info_before = load_scoring_config.cache_info()
        assert info_before.currsize == 1

        reload_all()

        info_after = load_scoring_config.cache_info()
        assert info_after.currsize == 0

    def test_reload_clears_programs_cache(self):
        """reload_all() clears the programs config LRU cache."""
        load_programs_config()
        reload_all()
        info = load_programs_config.cache_info()
        assert info.currsize == 0

    def test_reload_clears_trust_cache(self):
        """reload_all() clears the trust config LRU cache."""
        load_trust_config()
        reload_all()
        info = load_trust_config.cache_info()
        assert info.currsize == 0

    def test_configs_reload_fresh_after_clear(self):
        """After reload, loading configs again works and repopulates cache."""
        reload_all()
        config = load_scoring_config()
        assert isinstance(config, dict)
        assert load_scoring_config.cache_info().currsize == 1
