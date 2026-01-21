# SDT Template Validator (Python)

Validates SDT templates and rules against the JSON Schemas in `spec/`.

This package checks **structure only**.
- No coin logic
- No enforcement
- No auth

## Install (editable)
From repo root:
```bash
pip install -e packages/validator-python
```
CLI
```bash
sdt-validate template presets/game_growth.json
sdt-validate rule examples/minimal_rule.json
```
Python API
```
from sdt_validator import validate_template, validate_rule

validate_template(template_obj)
validate_rule(rule_obj)
```
Environment

The validator looks for schemas at:

SDT_SPEC_DIR (if set), otherwise

repo default ./spec/ (relative to current working directory)
