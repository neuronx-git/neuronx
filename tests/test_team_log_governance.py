"""
Test suite for TEAM_LOG governance and structure validation.

This test suite validates that the single collaboration surface (TEAM_LOG.md)
exists and has the required structure for CEO/CTO Takeover Mode.
"""

import os
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TEAM_LOG_PATH = REPO_ROOT / "COCKPIT" / "WORKSPACE" / "TEAM_LOG.md"


def test_team_log_exists():
    """TEAM_LOG.md must exist as the single collaboration surface."""
    assert TEAM_LOG_PATH.exists(), (
        f"TEAM_LOG.md not found at {TEAM_LOG_PATH}. "
        "This is the mandatory collaboration surface."
    )


def test_team_log_has_cto_scoreboard():
    """TEAM_LOG.md must contain CTO Scoreboard section."""
    content = TEAM_LOG_PATH.read_text()
    assert "## CTO Scoreboard" in content, (
        "TEAM_LOG.md must have '## CTO Scoreboard' section"
    )


def test_team_log_has_required_sections():
    """TEAM_LOG.md must have all required sections."""
    content = TEAM_LOG_PATH.read_text()
    
    required_sections = [
        "## CTO Scoreboard",
        "### Roadmap Completion",
        "### Test Health",
        "### CI Stability",
        "### Delivery Throughput",
        "### Defect Rate",
        "### Risk Ledger",
        "### Top 3 Priorities",
        "### Blockers",
    ]
    
    for section in required_sections:
        assert section in content, (
            f"TEAM_LOG.md missing required section: {section}"
        )


def test_workspace_directory_exists():
    """COCKPIT/WORKSPACE/ directory must exist."""
    workspace_dir = REPO_ROOT / "COCKPIT" / "WORKSPACE"
    assert workspace_dir.exists(), (
        f"COCKPIT/WORKSPACE/ directory not found at {workspace_dir}"
    )
    assert workspace_dir.is_dir(), (
        f"{workspace_dir} exists but is not a directory"
    )


def test_team_log_has_collaboration_sections():
    """TEAM_LOG.md must have sections for active discussions and reviews."""
    content = TEAM_LOG_PATH.read_text()
    
    collaboration_sections = [
        "## Active Discussions",
        "## Review Notes",
        "## Archive",
    ]
    
    for section in collaboration_sections:
        assert section in content, (
            f"TEAM_LOG.md missing collaboration section: {section}"
        )
