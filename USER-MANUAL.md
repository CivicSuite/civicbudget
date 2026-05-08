# CivicBudget User Manual

## What CivicBudget Is

CivicBudget helps municipal finance teams prepare budget-supporting text, checklists, and optional local workpaper records. It is designed for budget narrative preparation, line-item variance explanation, department memo drafting, hearing packet readiness, resident-facing budget summaries, and optional GFOA presentation checklist review.

Published version `0.1.2` is a foundation label under suite-wide release-recovery review. Do not promote it as production budget software until the recovery gates and a future v1.0.0 definition of done are complete.

CivicBudget does not make budget decisions. It does not approve numbers. It does not replace the city ERP, accounting system, payroll system, fund-accounting system, or budget adoption process.

## Non-Technical Staff Guide

### Typical Workflow

1. Start with department priorities and line-item amounts from your official finance system.
2. Use line-item analysis to identify material changes that need explanation.
3. Draft a department budget narrative and memo.
4. Build a hearing packet checklist for clerk coordination.
5. Draft a plain-English resident summary.
6. Send all outputs through normal finance and management review before publication or council use.

### What To Review Before Use

- Confirm every dollar amount against the official budget or ERP system.
- Confirm variance explanations with the department budget lead.
- Confirm public summaries with finance leadership and communications staff.
- Confirm hearing packet requirements with the clerk before agenda publication.

### What CivicBudget Will Not Do

- It will not approve a department budget.
- It will not submit budget amendments.
- It will not post official notices or packets.
- It will not certify GFOA compliance.
- It will not connect to live ERP or accounting systems in v0.1.2.

## IT / Technical Guide

### Runtime

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civicbudget.main:app --host 127.0.0.1 --port 8139
```

### Dependency

CivicBudget v0.1.2 depends on the published CivicCore v0.4.0 release wheel.

### Verification

```bash
bash scripts/verify-release.sh
```

The release gate checks documentation, placeholder imports, tests, Ruff, package build output, SHA256 sums, and the package version.

### API Endpoints

- `GET /`
- `GET /health`
- `GET /civicbudget`
- `POST /api/v1/civicbudget/line-items`
- `POST /api/v1/civicbudget/narrative`
- `GET /api/v1/civicbudget/narrative/{narrative_id}`
- `POST /api/v1/civicbudget/memo`
- `POST /api/v1/civicbudget/hearing-packet`
- `GET /api/v1/civicbudget/hearing-packet/{packet_id}`
- `POST /api/v1/civicbudget/resident-summary`
- `POST /api/v1/civicbudget/gfoa-review`

Set `CIVICBUDGET_WORKPAPER_DB_URL` to enable local SQLAlchemy-backed narrative and hearing packet workpaper records. If the variable is not set, CivicBudget keeps deterministic stateless behavior and retrieval endpoints return actionable configuration guidance.

## Supporting Architecture

![CivicBudget architecture](docs/architecture-civicbudget.svg)

The architecture is intentionally local and conservative in v0.1.2. Staff provide budget facts from official systems. CivicBudget creates reviewable drafts, checklists, and optional local workpaper records. Finance staff approve outputs. Future releases can add read-only ERP imports, CivicClerk packet handoffs, and CivicData transparency publishing without changing the boundary that official decisions remain with municipal staff.
