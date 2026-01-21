from pathlib import Path

import pytest

from sdt_validator import validate_template, validate_rule, load_json_file, ValidationError


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
