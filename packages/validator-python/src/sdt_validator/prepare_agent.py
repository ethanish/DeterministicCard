"""
Agent Creation Helper: Pre-Preparation Phase Assistant

This script helps users complete the pre-preparation phase checklist
for creating a new SDT agent.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .validator import load_json_file, validate_template


def find_template_files(search_dirs: list[Path]) -> list[Path]:
    """Find all template JSON files in the given directories."""
    templates = []
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for template_file in search_dir.glob("*.json"):
            try:
                obj = load_json_file(template_file)
                # Quick check if it looks like a template
                if isinstance(obj, dict) and "id" in obj and "fields" in obj:
                    templates.append(template_file)
            except Exception:
                continue
    return templates


def display_template_info(template_path: Path) -> dict[str, Any]:
    """Load and display template information."""
    template = load_json_file(template_path)
    
    print(f"\n📋 Template: {template.get('name', 'Unknown')}")
    print(f"   ID: {template.get('id', 'N/A')}")
    print(f"   Domain: {template.get('domain', 'N/A')}")
    if description := template.get('description'):
        print(f"   Description: {description}")
    
    print(f"\n   Fields:")
    for field in template.get('fields', []):
        optional = " (optional)" if field.get('optional', False) else ""
        print(f"     - {field.get('key')}: {field.get('type')}{optional}")
        if label := field.get('label'):
            print(f"       Label: {label}")
    
    if metrics := template.get('metrics'):
        print(f"\n   Metrics:")
        for metric in metrics:
            print(f"     - {metric.get('key')}: {metric.get('formula', 'N/A')}")
    
    if sdt := template.get('sdt_support'):
        print(f"\n   SDT Support:")
        for key in ['autonomy', 'competence', 'relatedness']:
            if value := sdt.get(key):
                print(f"     - {key.capitalize()}: {value}")
    
    return template


def interactive_template_selection(templates: list[Path]) -> Path | None:
    """Interactively select a template."""
    if not templates:
        print("❌ No template files found.")
        return None
    
    print("\n📚 Available Templates:")
    print("=" * 60)
    for idx, template_path in enumerate(templates, 1):
        try:
            template = load_json_file(template_path)
            name = template.get('name', 'Unknown')
            template_id = template.get('id', 'N/A')
            print(f"{idx}. {name} (ID: {template_id})")
            print(f"   Path: {template_path}")
        except Exception:
            print(f"{idx}. {template_path.name} (could not load)")
    
    print("\n" + "=" * 60)
    
    while True:
        try:
            choice = input(f"\nSelect template (1-{len(templates)}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(templates):
                return templates[idx]
            print(f"❌ Please enter a number between 1 and {len(templates)}")
        except ValueError:
            print("❌ Please enter a valid number or 'q'")
        except KeyboardInterrupt:
            print("\n\nCancelled.")
            return None


def collect_agent_info(template: dict[str, Any]) -> dict[str, Any]:
    """Collect agent information interactively."""
    info = {}
    
    print("\n" + "=" * 60)
    print("📝 Agent Information")
    print("=" * 60)
    
    # Agent ID
    while True:
        agent_id = input("\nAgent ID (e.g., 'my-agent-001'): ").strip()
        if agent_id:
            info['id'] = agent_id
            break
        print("❌ Agent ID is required")
    
    # Agent Name
    while True:
        agent_name = input("Agent Name: ").strip()
        if agent_name:
            info['name'] = agent_name
            break
        print("❌ Agent Name is required")
    
    # Description (optional)
    description = input("Description (optional, press Enter to skip): ").strip()
    if description:
        info['description'] = description
    
    # Template ID
    info['template_id'] = template.get('id', '')
    
    return info


def collect_sdt_elements() -> dict[str, str]:
    """Collect SDT support elements."""
    sdt_support = {}
    
    print("\n" + "=" * 60)
    print("🎯 SDT Elements Support")
    print("=" * 60)
    print("\nWhich SDT elements will this agent support?")
    print("(You can describe how the agent supports each element)")
    
    for element in ['autonomy', 'competence', 'relatedness']:
        print(f"\n{element.capitalize()}:")
        desc = input(f"  How does this agent support {element}? (optional, press Enter to skip): ").strip()
        if desc:
            sdt_support[element] = desc
    
    return sdt_support


def collect_capability_types() -> list[str]:
    """Collect desired capability types."""
    capability_types = ['capture', 'suggest', 'remind', 'analyze', 'custom']
    
    print("\n" + "=" * 60)
    print("⚙️  Capability Types")
    print("=" * 60)
    print("\nAvailable capability types:")
    print("  1. capture - Data collection")
    print("  2. suggest - Suggestion provision")
    print("  3. remind - Notification provision")
    print("  4. analyze - Analysis performance")
    print("  5. custom - User-defined functionality")
    
    selected = []
    print("\nSelect capability types (enter numbers separated by commas, e.g., '1,3,4'):")
    while True:
        choice = input("Capabilities: ").strip()
        if not choice:
            print("❌ Please select at least one capability type")
            continue
        
        try:
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            for idx in indices:
                if 0 <= idx < len(capability_types):
                    if capability_types[idx] not in selected:
                        selected.append(capability_types[idx])
                else:
                    print(f"❌ Invalid index: {idx + 1}")
                    break
            else:
                break
        except ValueError:
            print("❌ Please enter valid numbers separated by commas")
    
    return selected


def plan_field_mappings(template: dict[str, Any], capabilities: list[str]) -> list[dict[str, Any]]:
    """Help plan field mappings for capabilities."""
    fields = template.get('fields', [])
    field_keys = [f.get('key') for f in fields if f.get('key')]
    
    print("\n" + "=" * 60)
    print("🗺️  Field Mapping Plan")
    print("=" * 60)
    print("\nAvailable template fields:")
    for idx, field_key in enumerate(field_keys, 1):
        field_info = next((f for f in fields if f.get('key') == field_key), {})
        optional = " (optional)" if field_info.get('optional', False) else ""
        print(f"  {idx}. {field_key} ({field_info.get('type', 'unknown')}){optional}")
    
    mappings = []
    print(f"\nPlan field mappings for each capability:")
    
    for cap_type in capabilities:
        print(f"\n{cap_type.upper()} capability:")
        print("  Which field(s) should this capability work with?")
        print("  (Enter field numbers separated by commas, or press Enter to skip)")
        
        choice = input(f"  Fields for {cap_type}: ").strip()
        if not choice:
            continue
        
        try:
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            for idx in indices:
                if 0 <= idx < len(field_keys):
                    field_key = field_keys[idx]
                    mappings.append({
                        'capability_type': cap_type,
                        'field': field_key,
                        'field_index': idx
                    })
        except ValueError:
            print(f"  ⚠️  Skipping invalid input for {cap_type}")
    
    return mappings


def generate_summary(info: dict[str, Any], sdt_support: dict[str, str], 
                     capabilities: list[str], mappings: list[dict[str, Any]]) -> None:
    """Generate and display a summary."""
    print("\n" + "=" * 60)
    print("📊 Pre-Preparation Summary")
    print("=" * 60)
    
    print(f"\n✅ Agent ID: {info.get('id')}")
    print(f"✅ Agent Name: {info.get('name')}")
    print(f"✅ Template ID: {info.get('template_id')}")
    if desc := info.get('description'):
        print(f"✅ Description: {desc}")
    
    print(f"\n✅ SDT Elements:")
    for key, value in sdt_support.items():
        print(f"   - {key}: {value}")
    if not sdt_support:
        print("   (None specified)")
    
    print(f"\n✅ Capability Types: {', '.join(capabilities)}")
    
    print(f"\n✅ Field Mappings:")
    if mappings:
        for mapping in mappings:
            print(f"   - {mapping['capability_type']} -> {mapping['field']}")
    else:
        print("   (None planned)")
    
    print("\n" + "=" * 60)
    print("✅ Pre-preparation phase complete!")
    print("\nNext steps:")
    print("  1. Use this information to create your agent JSON file")
    print("  2. Run: sdt-validate agent <your_agent.json> --template <template_file.json>")


def main(argv: list[str] | None = None) -> None:
    """Main entry point for the agent preparation helper."""
    parser = argparse.ArgumentParser(
        prog="sdt-prepare-agent",
        description="Interactive helper for agent pre-preparation phase",
    )
    parser.add_argument(
        "--template-dir",
        type=Path,
        default=None,
        help="Directory to search for templates (default: ./presets and current directory)",
    )
    parser.add_argument(
        "--spec-dir",
        type=Path,
        default=None,
        help="Path to spec directory for template validation",
    )
    
    args = parser.parse_args(argv)
    
    # Find templates
    search_dirs = []
    if args.template_dir:
        search_dirs.append(args.template_dir)
    else:
        # Default search locations
        repo_root = Path(__file__).parent.parent.parent.parent
        search_dirs.extend([
            repo_root / "presets",
            Path.cwd() / "presets",
            Path.cwd(),
        ])
    
    print("🔍 Searching for templates...")
    templates = find_template_files(search_dirs)
    
    # Select template
    selected_template_path = interactive_template_selection(templates)
    if not selected_template_path:
        print("\n❌ No template selected. Exiting.")
        sys.exit(1)
    
    # Validate template
    try:
        template_obj = load_json_file(selected_template_path)
        validate_template(template_obj, spec_dir=args.spec_dir)
        print("\n✅ Template validation passed!")
    except Exception as e:
        print(f"\n⚠️  Template validation warning: {e}")
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
        template_obj = load_json_file(selected_template_path)
    
    # Display template info
    display_template_info(selected_template_path)
    
    # Collect information
    agent_info = collect_agent_info(template_obj)
    sdt_elements = collect_sdt_elements()
    capability_types = collect_capability_types()
    field_mappings = plan_field_mappings(template_obj, capability_types)
    
    # Generate summary
    generate_summary(agent_info, sdt_elements, capability_types, field_mappings)
    
    # Optionally save to file
    save = input("\n💾 Save preparation summary to file? (y/n): ").strip().lower()
    if save == 'y':
        output_file = Path(f"{agent_info['id']}_preparation.json")
        summary = {
            'agent_info': agent_info,
            'sdt_support': sdt_elements,
            'capability_types': capability_types,
            'field_mappings': field_mappings,
            'template_path': str(selected_template_path),
        }
        with output_file.open('w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"✅ Summary saved to: {output_file}")


if __name__ == "__main__":
    main()
