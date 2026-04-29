# Production Depth: Budget Workpaper Persistence

## Summary

CivicBudget now supports optional SQLAlchemy-backed budget narrative and hearing packet workpaper records through `CIVICBUDGET_WORKPAPER_DB_URL`.

## Shipped

- `BudgetWorkpaperRepository` with schema-aware SQLAlchemy tables.
- Persisted budget narrative records with `narrative_id`.
- Persisted hearing packet records with `packet_id`.
- Retrieval endpoints:
  - `GET /api/v1/civicbudget/narrative/{narrative_id}`
  - `GET /api/v1/civicbudget/hearing-packet/{packet_id}`
- Actionable `503` guidance when persistence is not configured.
- Regression tests for repository reload, API round trip, missing-record `404`, no-config `503`, and stateless fallback behavior.

## Still Not Shipped

- ERP, budgeting system, accounting, payroll, or fund-accounting runtime.
- Budget adoption or official approvals.
- Live LLM calls.
- Live finance-system connectors.
- Live CivicClerk packet submission or CivicData publishing handoffs.

## Verification

Run before merge:

```bash
python -m pytest --collect-only -q
python -m pytest -q
bash scripts/verify-docs.sh
python scripts/check-civiccore-placeholder-imports.py
python -m ruff check .
bash scripts/verify-release.sh
git diff --check
```
