# DeterministicCard Roadmap

Last updated: 2026-01-25

This roadmap focuses on the SDT-aligned spec, presets, validators, and documentation.
It does not cover production servers, enforcement logic, or monetization systems.

## Guiding principles
- SDT-aligned structure without coercion.
- Transparent data and privacy scope for any implementation.
- Schema-first portability across platforms.

## Milestones

### Now -> 2026-03 (v0.1: Foundation hardening)
- Finalize JSON Schemas (`spec/`) with shared definitions and a clear version field.
- Add minimal examples in `examples/` (template, rule, agent, and a full set).
- Expand presets to include learning and habit domains alongside existing ones.
- Align validator behavior in `packages/validator-js` and `packages/validator-python`.
- Update a minimal usage flow.

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
