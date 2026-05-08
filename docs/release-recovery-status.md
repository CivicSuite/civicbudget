# CivicBudget Release-Recovery Status

Date: 2026-05-07

## Status

CivicBudget `0.1.2` is a published foundation label under suite-wide release-recovery review. It is not product-ready and must not be promoted as production municipal budget software.

## Current Runtime Boundary

The current package provides line-item variance analysis, budget narrative drafts, memo drafts, hearing packet checklists, resident summaries, optional GFOA checklist review, optional local budget workpaper persistence, bearer-role protection for persisted retrieval, and a public sample UI at `/civicbudget`.

It does not replace an ERP, budgeting system, accounting system, payroll system, fund-accounting tool, budget-adoption workflow, official approval system, live LLM runtime, or live finance-system connector.

## Recovery Evidence

- WSL-native release verification passed through `scripts/verify-release.sh`: `22 passed`, docs gate passed, placeholder import check passed, Ruff passed, and build artifacts/checksums were created.
- Fresh install proof resolved CivicCore from the published v0.4.0 release wheel without a hidden CI preinstall: `CivicCore: 0.4.0`, `CivicBudget: 0.1.2`, `WSL platform: linux`.
- Browser QA covered `docs/index.html` at desktop 1440 x 1000 and mobile 390 x 844 with console, overflow, and keyboard-focus checks.
- Documentation gates reject stale product-ready language, shipping badges, stale version pins, and browser mojibake.

## Promotion Rule

Do not call CivicBudget finished, shippable, production-ready, or product-ready until a later active-module sprint implements the full CivicBudget v1.0.0 definition of done and passes the release gate.
