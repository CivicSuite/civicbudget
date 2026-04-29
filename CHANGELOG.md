# Changelog

## [0.1.2] - 2026-04-29

### Added

- Bearer-token auth and role checks for persisted budget narrative and hearing packet retrieval routes via `CIVICBUDGET_AUTH_TOKEN_ROLES` and `civiccore.auth`.

### Changed

- Moved CivicBudget to `civiccore==0.4.0` so persisted retrieval protection consumes the published shared auth helper instead of a module-local bridge.
- Updated CI, release verification, docs, runtime tests, and public UI copy for the v0.1.2 dependency and auth boundary.

## [0.1.1] - 2026-04-28

### Added

- Optional SQLAlchemy-backed budget narrative and hearing packet workpaper records via `CIVICBUDGET_WORKPAPER_DB_URL`.
- Budget narrative and hearing packet retrieval endpoints for persisted records.

### Changed

- Dependency-alignment release: moved CivicBudget to `civiccore==0.3.0` while preserving the existing v0.1.0 runtime foundation behavior.
- Updated CI, verification gates, package metadata, docs, runtime tests, landing page, and public UI labels for the v0.1.1 release.

## [0.1.0] - 2026-04-27

### Added

- CivicBudget package, FastAPI runtime, line-item analysis, budget narrative drafts, memo drafts, hearing packet checklists, resident summaries, GFOA checklist, docs, tests, and release gates.

### Not Shipped

- ERP, budgeting system, accounting, payroll, fund accounting, budget adoption, official approvals, live LLM calls, or live finance-system connector runtime.
