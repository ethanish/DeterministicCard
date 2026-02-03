# DeterministicCard Roadmap

Last updated: 2026-02-01

This roadmap focuses on the SDT-aligned spec, presets, validators, and documentation.
It does not cover production servers, enforcement logic, or monetization systems.

## Guiding principles
- SDT-aligned structure without coercion.
- Transparent data and privacy scope for any implementation.
- Schema-first portability across platforms.

## Milestones

### Now -> 2026-03 (v0.1: Foundation hardening)
- Document the new automation/transport/billing schemas in README and usage docs.
- Add full examples for project/execution/event/billing alongside existing full examples.
- Add validator tests for the new schemas (JS + Python).
- Add non-schema validation (e.g., workflow DAG checks, event-type-specific fields).
- Expand presets to include learning and habit domains alongside existing ones.
- Update a minimal usage flow (including new schemas).

### Backend (out of scope for this repo)
- Track MVP backend progress in /Users/ish/PROJECTS/DeterministicCard-backend (separate repo).

### 2026-04 -> 2026-06 (v0.2: Interop & tooling)
- Define schema versioning and deprecation policy (SemVer for specs).
- Add validator test suites and CI to validate all examples and presets.
- Provide a bundled schema output for easier consumption by tools.
- Package and publish validators (npm/pypi) with consistent CLI flags.
- Add optional schema for progress/metrics output to standardize reporting.

### 2026-07+ (v1.0: Stability)
- Stabilize the spec and publish compatibility guarantees.
- Add contribution governance (CONTRIBUTING, decision log, release process).
- Expand reference docs for non-enforcing implementations.
- Localize core docs where needed.

## Backlog ideas
- Additional condition types (e.g., rolling windows, weighted streaks).
- Expanded `sdt_support` guidance with examples.
- Implementation checklist for privacy-by-default patterns.
