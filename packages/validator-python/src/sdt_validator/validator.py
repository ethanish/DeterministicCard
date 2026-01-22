from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from jsonschema import Draft7Validator


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


def _load_schema(schema_filename: str, spec_dir: Optional[Path] = None) -> Dict[str, Any]:
    spec_dir = spec_dir or _default_spec_dir()
    schema_path = spec_dir / schema_filename
    if not schema_path.exists():
        raise FileNotFoundError(
            f"Schema file not found: {schema_path}. "
            f"Set SDT_SPEC_DIR or run from repo root so ./spec exists."
        )
    with schema_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_json_file(path: str | Path) -> Any:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def _validate(obj: Any, schema: Dict[str, Any], label: str) -> None:
    validator = Draft7Validator(schema)
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
    schema = _load_schema("template.schema.json", Path(spec_dir) if spec_dir else None)
    _validate(template_obj, schema, "Template")


def validate_rule(rule_obj: Any, *, spec_dir: Optional[str | Path] = None) -> None:
    schema = _load_schema("rule.schema.json", Path(spec_dir) if spec_dir else None)
    _validate(rule_obj, schema, "Rule")


def validate_agent(agent_obj: Any, *, spec_dir: Optional[str | Path] = None) -> None:
    schema = _load_schema("agent.schema.json", Path(spec_dir) if spec_dir else None)
    _validate(agent_obj, schema, "Agent")