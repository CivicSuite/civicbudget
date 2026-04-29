# CivicBudget

CivicBudget is the CivicSuite budget narrative and transparency support module. Version 0.1.2 helps finance staff prepare line-item variance notes, department budget narratives, council-facing budget memos, hearing packet checklists, plain-English resident summaries, optional GFOA presentation checklist reviews, and optional local workpaper records.

It is intentionally not an ERP, budgeting system, accounting system, payroll system, fund-accounting tool, budget-adoption workflow, or official approval system. CivicBudget prepares reviewable staff work products; finance staff remain responsible for every number, narrative, and public-facing statement.

## Shipping in v0.1.2

- Line-item variance analysis with finance-review notes.
- Budget narrative draft assembly from department priorities and line-item inputs.
- Department budget memo draft scaffolding.
- Budget hearing packet checklist support for CivicClerk handoff.
- Optional database-backed narrative and hearing packet workpaper records via `CIVICBUDGET_WORKPAPER_DB_URL`.
- Bearer-token protection for persisted narrative and hearing packet retrieval via `CIVICBUDGET_AUTH_TOKEN_ROLES`.
- Plain-English resident budget summary drafts.
- Optional GFOA presentation checklist support.
- FastAPI runtime with health, public landing page, and deterministic API endpoints.
- Release gates, docs, browser QA evidence, and package build artifacts.

## Not shipped yet

- ERP, budgeting, accounting, payroll, fund accounting, budget adoption, official approvals, live LLM calls, or live finance-system connector runtime.
- Live CivicClerk packet submission and live CivicData publishing handoffs. v0.1.2 prepares the handoff checklist; later releases will wire the cross-module workflow.
- Finance approval queues, role-based workflow, and signed publication records.

## Install

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civicbudget.main:app --host 127.0.0.1 --port 8139
```

CivicBudget v0.1.2 is pinned to `civiccore==0.4.0`.

## Operator Path

1. Finance or department staff collect line-item inputs from the city budget or ERP system.
2. CivicBudget identifies material variances and drafts review notes.
3. Staff draft department narratives, memos, hearing packet checklists, and resident summaries.
4. Finance reviews and approves the output outside CivicBudget.
5. Future releases will hand approved packet materials to CivicClerk and public transparency summaries to CivicData.

## API Surface

- `GET /` returns honest current-state metadata and roadmap boundary.
- `GET /health` returns runtime and CivicCore version status.
- `GET /civicbudget` renders the public module overview.
- `POST /api/v1/civicbudget/line-items` returns variance analysis.
- `POST /api/v1/civicbudget/narrative` returns a finance-review-required narrative draft and a `narrative_id` when persistence is configured.
- `GET /api/v1/civicbudget/narrative/{narrative_id}` retrieves a persisted narrative when both `CIVICBUDGET_WORKPAPER_DB_URL` and `CIVICBUDGET_AUTH_TOKEN_ROLES` are configured.
- `POST /api/v1/civicbudget/memo` returns a non-approval budget memo draft.
- `POST /api/v1/civicbudget/hearing-packet` returns a CivicClerk-ready checklist and a `packet_id` when persistence is configured.
- `GET /api/v1/civicbudget/hearing-packet/{packet_id}` retrieves a persisted hearing packet when both `CIVICBUDGET_WORKPAPER_DB_URL` and `CIVICBUDGET_AUTH_TOKEN_ROLES` are configured.
- `POST /api/v1/civicbudget/resident-summary` returns a publication-review-required public summary draft.
- `POST /api/v1/civicbudget/gfoa-review` returns a checklist, not certification.

## Optional Persistence

Set `CIVICBUDGET_WORKPAPER_DB_URL` to enable local SQLAlchemy-backed narrative and hearing packet workpaper records:

```bash
export CIVICBUDGET_WORKPAPER_DB_URL="sqlite+pysqlite:///./civicbudget.db"
```

Set `CIVICBUDGET_AUTH_TOKEN_ROLES` to a JSON object that maps bearer tokens to roles before exposing persisted retrieval:

```json
{
  "demo-reader-token": ["workpaper_reader"],
  "budget-admin-token": "workpaper_reader,budget_admin"
}
```

Without the database variable, CivicBudget remains deterministic and stateless. Without the auth variable, persisted retrieval endpoints return actionable `503` responses that name the missing auth configuration. With auth configured, anonymous callers receive `401` and callers without an allowed role receive `403`.

## Documentation

- [User Manual](USER-MANUAL.md)
- [Architecture](docs/architecture.md)
- [Landing Page](docs/index.html)
- [Release Notes](CHANGELOG.md)

Apache 2.0 code. CC BY 4.0 docs.
