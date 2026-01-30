from pathlib import Path

import pytest

from sdt_validator import (
    validate_template,
    validate_rule,
    validate_agent,
    validate_project,
    validate_execution,
    validate_event,
    validate_billing,
    load_json_file,
    ValidationError,
)


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


def test_invalid_template_metric_unknown_field():
    template = load_json_file("presets/game_growth.json")
    template["metrics"].append(
        {
            "key": "unknown_metric",
            "formula": "sum(unknown_field)",
            "display": "Unknown metric",
        }
    )
    with pytest.raises(ValidationError) as exc_info:
        validate_template(template)
    assert "unknown field" in str(exc_info.value).lower()


def test_invalid_rule_missing_conditions():
    bad = {"id": "r1", "template_id": "t1", "enabled": True}
    with pytest.raises(ValidationError):
        validate_rule(bad)


def test_valid_rule_cross_reference():
    template = load_json_file("presets/game_growth.json")
    rule = {
        "schema_version": "0.1.0",
        "id": "r1",
        "template_id": template["id"],
        "enabled": True,
        "conditions": [
            {"type": "count", "field": "session_length", "value": 1}
        ],
        "effects": [
            {"type": "nudge", "message": "Nice progress."}
        ],
    }
    validate_rule(rule, template_obj=template)


def test_invalid_rule_field_not_in_template():
    template = load_json_file("presets/game_growth.json")
    rule = {
        "schema_version": "0.1.0",
        "id": "r2",
        "template_id": template["id"],
        "enabled": True,
        "conditions": [
            {"type": "count", "field": "unknown_field", "value": 1}
        ],
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_rule(rule, template_obj=template)
    assert "condition[0].field" in str(exc_info.value).lower()


def test_valid_agent_minimal():
    agent = {
        "schema_version": "0.1.0",
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic"
    }
    validate_agent(agent)


def test_valid_agent_with_capabilities():
    agent = {
        "schema_version": "0.1.0",
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
    bad = {"schema_version": "0.1.0", "id": "a1", "name": "Bad"}  # missing template_id
    with pytest.raises(ValidationError):
        validate_agent(bad)


def test_valid_agent_cross_reference():
    """Test cross-reference validation with valid template"""
    template = load_json_file("presets/game_growth.json")
    agent = {
        "schema_version": "0.1.0",
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic",
        "capabilities": [
            {
                "type": "capture",
                "field": "session_length",
                "trigger": "on_session_end"
            },
            {
                "type": "suggest",
                "field": "difficulty",
                "trigger": "on_field_change"
            }
        ]
    }
    validate_agent(agent, template_obj=template)


def test_invalid_agent_template_id_mismatch():
    """Test that agent with wrong template_id fails validation"""
    template = load_json_file("presets/game_growth.json")
    agent = {
        "schema_version": "0.1.0",
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "wrong-template-id",
        "capabilities": []
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_agent(agent, template_obj=template)
    assert "template_id" in str(exc_info.value).lower()


def test_invalid_agent_field_not_in_template():
    """Test that agent with invalid field reference fails validation"""
    template = load_json_file("presets/game_growth.json")
    agent = {
        "schema_version": "0.1.0",
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic",
        "capabilities": [
            {
                "type": "capture",
                "field": "nonexistent_field",
                "trigger": "on_session_end"
            }
        ]
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_agent(agent, template_obj=template)
    assert "nonexistent_field" in str(exc_info.value)


def test_valid_agent_capability_types():
    """Test all capability types with proper configs"""
    agent = {
        "schema_version": "0.1.0",
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic",
        "capabilities": [
            {
                "type": "capture",
                "field": "session_length",
                "trigger": "on_session_end",
                "config": {
                    "source": "game_api",
                    "format": "auto"
                }
            },
            {
                "type": "suggest",
                "field": "difficulty",
                "trigger": "on_field_change",
                "config": {
                    "context": ["session_length"],
                    "max_suggestions": 3
                }
            },
            {
                "type": "remind",
                "field": "reflection",
                "trigger": "on_time_interval",
                "config": {
                    "interval": "daily",
                    "message": "Don't forget to reflect!"
                }
            },
            {
                "type": "analyze",
                "field": "session_length",
                "trigger": "manual",
                "config": {
                    "model": "trend_analysis",
                    "parameters": {}
                }
            },
            {
                "type": "custom",
                "field": "difficulty",
                "trigger": "on_condition_met",
                "config": {
                    "custom_param": "value"
                }
            }
        ]
    }
    validate_agent(agent)


def test_invalid_agent_invalid_trigger():
    """Test that invalid trigger enum value fails validation"""
    agent = {
        "schema_version": "0.1.0",
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic",
        "capabilities": [
            {
                "type": "capture",
                "field": "session_length",
                "trigger": "invalid_trigger"  # Not in enum
            }
        ]
    }
    with pytest.raises(ValidationError):
        validate_agent(agent)


def test_invalid_agent_capture_missing_field():
    """Test that capture capability requires field"""
    agent = {
        "schema_version": "0.1.0",
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic",
        "capabilities": [
            {
                "type": "capture",
                # missing required field
                "trigger": "on_session_end"
            }
        ]
    }
    with pytest.raises(ValidationError):
        validate_agent(agent)


def test_invalid_agent_remind_missing_trigger():
    """Test that remind capability requires trigger"""
    agent = {
        "schema_version": "0.1.0",
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic",
        "capabilities": [
            {
                "type": "remind",
                "field": "reflection"
                # missing required trigger
            }
        ]
    }
    with pytest.raises(ValidationError):
        validate_agent(agent)


def test_valid_agent_sdt_support():
    """Test agent with SDT support values"""
    agent = {
        "schema_version": "0.1.0",
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic",
        "sdt_support": {
            "autonomy": "Users can customize agent behavior",
            "competence": "Agent provides insights on user progress",
            "relatedness": "Optional sharing features"
        }
    }
    validate_agent(agent)


def test_valid_agent_with_template_sdt_consistency():
    """Test agent SDT support with template (should not error)"""
    template = load_json_file("presets/game_growth.json")
    agent = {
        "schema_version": "0.1.0",
        "id": "agent1",
        "name": "Test Agent",
        "template_id": "game-growth-basic",
        "sdt_support": {
            "autonomy": "Extended autonomy support",
            "competence": "Extended competence support"
        }
    }
    # Should pass - agent can extend template's SDT support
    validate_agent(agent, template_obj=template)


def test_valid_project_minimal():
    project = {
        "schema_version": "0.1.0",
        "project_id": "proj_1",
        "name": "Test Project",
        "owner_id": "user_1",
        "agents": ["agent_a"],
        "workflows": [
            {
                "workflow_id": "wf_1",
                "trigger": {"type": "manual"},
                "steps": [
                    {"step_id": "s1", "agent_id": "agent_a", "action": "capture"}
                ],
            }
        ],
    }
    validate_project(project)


def test_invalid_project_missing_agents():
    bad = {
        "schema_version": "0.1.0",
        "project_id": "proj_1",
        "name": "Test Project",
        "owner_id": "user_1",
        "workflows": [],
    }
    with pytest.raises(ValidationError):
        validate_project(bad)


def test_valid_execution_minimal():
    execution = {
        "schema_version": "0.1.0",
        "execution_id": "exec_1",
        "project_id": "proj_1",
        "workflow_id": "wf_1",
        "status": "queued",
    }
    validate_execution(execution)


def test_valid_event_minimal():
    event = {
        "schema_version": "0.1.0",
        "event_id": "evt_1",
        "event_type": "choice_made",
        "user_id": "user_1",
        "project_id": "proj_1",
        "timestamp": "2026-01-30T08:00:00Z",
        "choice": {"screen": "q1", "value": "option_a"},
        "privacy": {"consent": True},
    }
    validate_event(event)


def test_valid_billing_minimal():
    billing = {
        "schema_version": "0.1.0",
        "transaction_id": "txn_1",
        "user_id": "user_1",
        "type": "credit_spend",
        "balance_delta": -5,
        "timestamp": "2026-01-30T08:00:00Z",
    }
    validate_billing(billing)
