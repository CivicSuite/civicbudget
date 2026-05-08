CivicBudget published v0.1.2 is the CivicSuite budget narrative and transparency support module and is a foundation label under suite-wide release-recovery review. Do not promote it as production budget software until the recovery gates and a future v1.0.0 definition of done are complete.

Available: line-item variance analysis, budget narrative drafts, department memo drafts, hearing packet checklists, resident plain-English summaries, optional GFOA checklist support, optional database-backed narrative and hearing packet workpaper records, FastAPI runtime, docs, tests, and browser QA evidence.

Boundaries: CivicBudget is not an ERP, budgeting system, accounting system, payroll system, fund-accounting tool, budget-adoption workflow, official approval system, live LLM runtime, or live finance-system connector.

Install:
python -m pip install -e ".[dev]"
python -m uvicorn civicbudget.main:app --host 127.0.0.1 --port 8139

Dependency: published CivicCore v0.4.0 release wheel.

Optional persistence: set CIVICBUDGET_WORKPAPER_DB_URL to enable SQLAlchemy-backed narrative and hearing packet workpaper records. Without it, CivicBudget remains deterministic and stateless.
