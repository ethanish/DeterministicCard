# Backend Update Notes

Last updated: 2026-02-03

This file records backend MVP progress related to the DeterministicCard schemas.
The backend code lives outside this repo at:
- /Users/ish/PROJECTS/DeterministicCard-backend

## Implemented MVP scope
- FastAPI skeleton with routes for projects, events, executions, billing, and paid queries.
- JSON Schema validation (optional) via SDT_SPEC_DIR.
- Domain validations: workflow DAG checks and event_type field checks.
- Pydantic request models for API consistency.
- Basic JWT auth toggle + CORS settings.
- Alembic config for DB migrations.

## Next steps (backend)
- Add orchestration/worker execution engine.
- Add role-based access control and API key management.
- Harden billing: idempotency, pricing rules, audit trail.
