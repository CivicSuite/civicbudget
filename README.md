# CivicBudget

CivicBudget is the CivicSuite budget narrative and transparency support module. Version 0.1.1 helps finance staff prepare line-item variance notes, department budget narratives, council-facing budget memos, hearing packet checklists, plain-English resident summaries, and optional GFOA presentation checklist reviews.

It is intentionally not an ERP, budgeting system, accounting system, payroll system, fund-accounting tool, budget-adoption workflow, or official approval system. CivicBudget prepares reviewable staff work products; finance staff remain responsible for every number, narrative, and public-facing statement.

## Shipping in v0.1.1

- Line-item variance analysis with finance-review notes.
- Budget narrative draft assembly from department priorities and line-item inputs.
- Department budget memo draft scaffolding.
- Budget hearing packet checklist support for CivicClerk handoff.
- Plain-English resident budget summary drafts.
- Optional GFOA presentation checklist support.
- FastAPI runtime with health, public landing page, and deterministic API endpoints.
- Release gates, docs, browser QA evidence, and package build artifacts.

## Not shipped yet

- ERP, budgeting, accounting, payroll, fund accounting, budget adoption, official approvals, live LLM calls, or live finance-system connector runtime.
- Live CivicClerk packet submission and live CivicData publishing handoffs. v0.1.1 prepares the handoff checklist; later releases will wire the cross-module workflow.
- Finance approval queues, role-based workflow, and signed publication records.

## Install

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civicbudget.main:app --host 127.0.0.1 --port 8139
```

CivicBudget v0.1.1 is pinned to `civiccore==0.3.0`.

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
- `POST /api/v1/civicbudget/narrative` returns a finance-review-required narrative draft.
- `POST /api/v1/civicbudget/memo` returns a non-approval budget memo draft.
- `POST /api/v1/civicbudget/hearing-packet` returns a CivicClerk-ready checklist.
- `POST /api/v1/civicbudget/resident-summary` returns a publication-review-required public summary draft.
- `POST /api/v1/civicbudget/gfoa-review` returns a checklist, not certification.

## Documentation

- [User Manual](USER-MANUAL.md)
- [Architecture](docs/architecture.md)
- [Landing Page](docs/index.html)
- [Release Notes](CHANGELOG.md)

Apache 2.0 code. CC BY 4.0 docs.
