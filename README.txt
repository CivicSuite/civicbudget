CivicBudget v0.1.1 is the CivicSuite budget narrative and transparency support module.

Shipping: line-item variance analysis, budget narrative drafts, department memo drafts, hearing packet checklists, resident plain-English summaries, optional GFOA checklist support, FastAPI runtime, docs, tests, and browser QA evidence.

Boundaries: CivicBudget is not an ERP, budgeting system, accounting system, payroll system, fund-accounting tool, budget-adoption workflow, official approval system, live LLM runtime, or live finance-system connector.

Install:
python -m pip install -e ".[dev]"
python -m uvicorn civicbudget.main:app --host 127.0.0.1 --port 8139

Dependency: civiccore==0.3.0.
