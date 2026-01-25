# DeterministicCard
Self-Deterministic based Template Spec Developer

# SDT Template & Rule Specification

Self-Determination Theory (SDT)-friendly template and rule specification
for hybrid systems (web, mobile, smart glasses, games, APIs).

This project provides:
- A **neutral structure (not control)** for defining growth, contribution, and reflection
- User-modifiable templates and rules
- A foundation usable across databases, games, wearable devices, and APIs

## Why SDT?
SDT emphasizes:
- **Autonomy**: users choose what matters
- **Competence**: users see growth they define
- **Relatedness**: optional, non-coercive connection

This spec provides *structure without coercion*.
## Non-coercive use requirements (SDT guardrails)
To stay aligned with SDT's "structure, not control" philosophy, any implementation **must** include:
- **Informed choice**: explain why a rule or template exists, and allow users to opt out or modify it.
- **Transparent feedback**: show how progress is calculated and what data is used.
- **Data minimization**: collect only what is needed for user-defined goals.
- **No forced incentives**: avoid penalties, locks, or pressure tactics that reduce autonomy.
- **Human override**: provide a clear path to pause or reset rules without punishment.

## Schema version
All template, rule, and agent JSON files must include `schema_version` (SemVer, e.g. `0.1.0`).

## Data & privacy scope (implementation requirements)
Implementations **must** clearly document the following, in user-facing language:
- **Data categories**: what inputs are collected (e.g., task events, timestamps), and what is explicitly *not* collected.
- **Purpose binding**: each data category must be tied to a user-defined goal or rule.
- **Default posture**: no telemetry/analytics by default; opt-in only with a clear toggle.
- **Retention & deletion**: how long data is kept and how users can delete or export it.
- **Local vs. remote**: where data is stored/processed (on-device, local file, or server) and the tradeoffs.
- **Third parties**: any external services or SDKs that receive data, with a short rationale.

## What this repo is
✅ Specification (JSON Schema)  
✅ Preset templates (game, OSS, learning, habit)  
✅ Rule definition format (goals, nudges, reward candidates)  
✅ Validators (client-side / tooling only)

## What this repo is NOT
❌ Coin ledger or economy logic  
❌ Authentication / authorization  
❌ Backend / production server code  
❌ Pricing or billing logic  

> This repo is safe to use as open source.

## Domains supported
- Web / Mobile apps
- Smart glasses (voice / button capture)
- Games
- Open-source contribution tracking
- Personal growth systems

## License
MIT
