"""
Configuration Loader
Reads YAML config files from /config directory.
All business rules live in YAML — edit config, push, auto-deploy.
No code changes needed to adjust scoring, programs, or trust rules.
"""

import yaml
import logging
from pathlib import Path
from functools import lru_cache

logger = logging.getLogger("neuronx.config")

CONFIG_DIR = Path(__file__).parent.parent / "config"


@lru_cache(maxsize=1)
def load_scoring_config() -> dict:
    path = CONFIG_DIR / "scoring.yaml"
    with open(path) as f:
        config = yaml.safe_load(f)
    logger.info("Loaded scoring config: thresholds high=%d med=%d", config["thresholds"]["high"], config["thresholds"]["med"])
    return config


@lru_cache(maxsize=1)
def load_programs_config() -> dict:
    path = CONFIG_DIR / "programs.yaml"
    with open(path) as f:
        config = yaml.safe_load(f)
    programs = config.get("programs", {})
    logger.info("Loaded %d programs from config", len(programs))
    return programs


@lru_cache(maxsize=1)
def load_trust_config() -> dict:
    path = CONFIG_DIR / "trust.yaml"
    with open(path) as f:
        config = yaml.safe_load(f)
    triggers = config.get("escalation_triggers", {})
    logger.info("Loaded trust config: %d escalation categories", len(triggers))
    return config


def reload_all():
    """Clear cached configs. Call after config file changes."""
    load_scoring_config.cache_clear()
    load_programs_config.cache_clear()
    load_trust_config.cache_clear()
    logger.info("All configs reloaded")
