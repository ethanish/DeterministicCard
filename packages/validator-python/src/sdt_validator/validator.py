from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


@dataclass
class ValidationError(Exception):
    """Raised when JSON does not conform to the SDT schema."""
    message: str
    errors: Optional[list[str]] = None

    def __str__(self) -> str:
        if not self.errors:
            return self.message
        details = "\n".join(f"- {e}" for e in self.errors)
        return f"{self.message}\n{details}"


def _default_spec_dir() -> Path:
    """
    Locate schema directory.

    Priority:
      1) SDT_SPEC_DIR environment variable
      2) ./spec relative to current working directory
    """
    env = os.getenv("SDT_SPEC_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return (Path.cwd() / "spec").resolve()


def _build_registry(spec_dir: Path) -> Registry:
    resources: dict[str, Resource] = {}
    for schema_path in spec_dir.glob("*.json"):
        with schema_path.open("r", encoding="utf-8") as f:
            schema = json.load(f)
        schema_id = schema.get("$id") or schema_path.name
        resources[schema_id] = Resource.from_contents(schema)
    return Registry().with_resources(resources.items())


def _load_schema(
    schema_filename: str, spec_dir: Optional[Path] = None
) -> tuple[Dict[str, Any], Registry]:
    spec_dir = spec_dir or _default_spec_dir()
    schema_path = spec_dir / schema_filename
    if not schema_path.exists():
        raise FileNotFoundError(
            f"Schema file not found: {schema_path}. "
            f"Set SDT_SPEC_DIR or run from repo root so ./spec exists."
        )
    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)
    registry = _build_registry(spec_dir)
    return schema, registry


def load_json_file(path: str | Path) -> Any:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def _validate(obj: Any, schema: Dict[str, Any], label: str, registry: Registry) -> None:
    validator = Draft202012Validator(schema, registry=registry)
    errors = sorted(validator.iter_errors(obj), key=lambda e: list(e.path))

    if errors:
        rendered: list[str] = []
        for e in errors:
            # Build a readable path like fields[0].key
            path = ""
            for part in e.path:
                if isinstance(part, int):
                    path += f"[{part}]"
                else:
                    path += f".{part}" if path else str(part)
            where = f" at '{path}'" if path else ""
            rendered.append(f"{e.message}{where}")
        raise ValidationError(f"{label} failed schema validation.", rendered)


def validate_template(template_obj: Any, *, spec_dir: Optional[str | Path] = None) -> None:
    schema, registry = _load_schema("template.schema.json", Path(spec_dir) if spec_dir else None)
    _validate(template_obj, schema, "Template", registry)


def validate_rule(rule_obj: Any, *, spec_dir: Optional[str | Path] = None) -> None:
    schema, registry = _load_schema("rule.schema.json", Path(spec_dir) if spec_dir else None)
    _validate(rule_obj, schema, "Rule", registry)


def validate_agent(
    agent_obj: Any,
    *,
    template_obj: Optional[Any] = None,
    spec_dir: Optional[str | Path] = None
) -> None:
    """
    Validate an agent object against the agent schema.
    
    Args:
        agent_obj: The agent object to validate
        template_obj: Optional template object for cross-reference validation.
                     If provided, validates that template_id exists and
                     capabilities reference valid fields.
        spec_dir: Optional path to spec directory containing schemas
    """
    schema, registry = _load_schema("agent.schema.json", Path(spec_dir) if spec_dir else None)
    _validate(agent_obj, schema, "Agent", registry)
    
    # Cross-reference validation if template is provided
    if template_obj is not None:
        _validate_agent_references(agent_obj, template_obj)


def _validate_agent_references(agent_obj: Any, template_obj: Any) -> None:
    """
    Validate cross-references between agent and template.
    
    - Validates that agent.template_id matches template.id
    - Validates that capabilities[].field exists in template.fields[].key
    """
    errors: list[str] = []
    
    # Validate template_id reference
    agent_template_id = agent_obj.get("template_id")
    template_id = template_obj.get("id")
    
    if agent_template_id != template_id:
        errors.append(
            f"Agent references template_id '{agent_template_id}', "
            f"but provided template has id '{template_id}'"
        )
    
    # Build set of valid field keys from template
    template_fields = template_obj.get("fields", [])
    valid_field_keys = {field.get("key") for field in template_fields if field.get("key")}
    
    # Validate capabilities field references
    capabilities = agent_obj.get("capabilities", [])
    for idx, capability in enumerate(capabilities):
        field = capability.get("field")
        if field is not None:
            if field not in valid_field_keys:
                errors.append(
                    f"Capability[{idx}].field '{field}' does not exist in template. "
                    f"Available fields: {sorted(valid_field_keys) if valid_field_keys else 'none'}"
                )
    
    # Validate SDT support consistency (optional check)
    agent_sdt = agent_obj.get("sdt_support")
    template_sdt = template_obj.get("sdt_support")
    
    if agent_sdt and template_sdt:
        # Check if agent defines SDT support but template doesn't have corresponding values
        # This is a warning-level check, but we'll include it as an error for consistency
        for key in ["autonomy", "competence", "relatedness"]:
            if key in agent_sdt and key not in template_sdt:
                # This is informational - agent can extend template's SDT support
                pass
    
    if errors:
        raise ValidationError("Agent failed cross-reference validation.", errors)
