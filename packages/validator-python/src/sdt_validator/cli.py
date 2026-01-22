from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .validator import (
    ValidationError,
    load_json_file,
    validate_rule,
    validate_template,
    validate_agent,
)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sdt-validate",
        description="Validate SDT template/rule/agent JSON files against the spec schemas.",
    )
    p.add_argument(
        "kind",
        choices=["template", "rule", "agent"],
        help="Type of JSON to validate.",
    )
    p.add_argument(
        "json_path",
        help="Path to JSON file to validate.",
    )
    p.add_argument(
        "--spec-dir",
        default=None,
        help="Path to spec directory containing template.schema.json, rule.schema.json, and agent.schema.json. "
             "Overrides SDT_SPEC_DIR if provided.",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    json_path = Path(args.json_path)
    if not json_path.exists():
        print(f"File not found: {json_path}", file=sys.stderr)
        raise SystemExit(2)

    try:
        obj = load_json_file(json_path)
        if args.kind == "template":
            validate_template(obj, spec_dir=args.spec_dir)
        elif args.kind == "rule":
            validate_rule(obj, spec_dir=args.spec_dir)
        else:  # agent
            validate_agent(obj, spec_dir=args.spec_dir)

        print("OK")
    except ValidationError as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        raise SystemExit(3)


if __name__ == "__main__":
    main()
