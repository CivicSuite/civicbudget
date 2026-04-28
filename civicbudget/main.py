"""FastAPI runtime foundation for CivicBudget."""
from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicbudget import __version__
from civicbudget.gfoa_review import review_gfoa_alignment
from civicbudget.hearing_packet import build_hearing_packet_checklist
from civicbudget.line_item_analysis import analyze_line_items
from civicbudget.memo import draft_budget_memo
from civicbudget.narrative import draft_budget_narrative
from civicbudget.public_ui import render_public_lookup_page
from civicbudget.resident_summary import draft_resident_summary

app = FastAPI(
    title="CivicBudget",
    version=__version__,
    description=(
        "Budget narratives, line-item analysis, hearing packet prep, and transparency "
        "summaries for CivicSuite."
    ),
)


class LineItemsRequest(BaseModel):
    items: list[dict[str, float | str]]


class NarrativeRequest(BaseModel):
    department: str
    priorities: list[str]
    line_items: list[dict[str, float | str]]


class MemoRequest(BaseModel):
    department: str
    audience: str
    highlights: list[str]


class HearingPacketRequest(BaseModel):
    hearing_name: str
    required_items: list[str]


class ResidentSummaryRequest(BaseModel):
    topic: str
    facts: list[str]


class GFOARequest(BaseModel):
    pursued: bool


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "CivicBudget",
        "version": __version__,
        "status": "budget narrative foundation",
        "message": (
            "CivicBudget package, API foundation, line-item analysis, budget narratives, "
            "department memos, hearing packet checklists, resident summaries, GFOA checklist, "
            "and public UI foundation are online; ERP, budgeting system, accounting, payroll, "
            "budget adoption, official approvals, live LLM calls, and live finance-system "
            "connectors are not implemented yet."
        ),
        "next_step": (
            "Post-v0.1.0 roadmap: finance approval queues, ERP read-only imports, and "
            "CivicClerk/CivicData handoffs"
        ),
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "civicbudget",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civicbudget", response_class=HTMLResponse)
def public_civicbudget_page() -> str:
    return render_public_lookup_page()


@app.post("/api/v1/civicbudget/line-items")
def line_items(request: LineItemsRequest) -> dict[str, object]:
    return {"variances": [v.__dict__ for v in analyze_line_items(request.items)]}


@app.post("/api/v1/civicbudget/narrative")
def narrative(request: NarrativeRequest) -> dict[str, object]:
    draft = draft_budget_narrative(
        request.department,
        request.priorities,
        request.line_items,
    )
    return {**draft.__dict__, "variances": [v.__dict__ for v in draft.variances]}


@app.post("/api/v1/civicbudget/memo")
def memo(request: MemoRequest) -> dict[str, object]:
    return draft_budget_memo(
        request.department,
        request.audience,
        request.highlights,
    ).__dict__


@app.post("/api/v1/civicbudget/hearing-packet")
def hearing_packet(request: HearingPacketRequest) -> dict[str, object]:
    return build_hearing_packet_checklist(
        request.hearing_name,
        request.required_items,
    ).__dict__


@app.post("/api/v1/civicbudget/resident-summary")
def resident_summary(request: ResidentSummaryRequest) -> dict[str, object]:
    return draft_resident_summary(request.topic, request.facts).__dict__


@app.post("/api/v1/civicbudget/gfoa-review")
def gfoa_review(request: GFOARequest) -> dict[str, object]:
    return review_gfoa_alignment(request.pursued).__dict__
