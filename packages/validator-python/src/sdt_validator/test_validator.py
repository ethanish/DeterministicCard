from pathlib import Path

import pytest

from sdt_validator import validate_template, validate_rule, validate_agent, load_json_file, ValidationError


def test_validate_game_growth_template_from_presets():
    # Assumes tests run from repo root or SDT_SPEC_DIR is set
    template = load_json_file("presets/game_growth.json")
    validate_template(template)


def test_validate_oss_template_from_presets():
    template = load_json_file("presets/open_source_contrib.json")
    validate_template(template)


def test_invalid_template_missing_required_fields():
    bad = {"id": "x", "name": "Bad"}  # missing domain + fields
    with pytest.raises(ValidationError):
        validate_template(bad)


def test_invalid_rule_missing_conditions():
    bad = {"id": "r1", "template_id": "t1", "enabled": True}
    with pytest.raises(ValidationError):
        validate_rule(bad)


def test_valid_agent_minimal():
    agent = {
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic"
    }
    validate_agent(agent)


def test_valid_agent_with_capabilities():
    agent = {
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic",
        "description": "An agent that helps capture data",
        "capabilities": [
            {
                "type": "capture",
                "field": "session_length",
                "trigger": "on_session_end"
            }
        ],
        "enabled": True
    }
    validate_agent(agent)


def test_invalid_agent_missing_required_fields():
    bad = {"id": "a1", "name": "Bad"}  # missing template_id
    with pytest.raises(ValidationError):
        validate_agent(bad)
