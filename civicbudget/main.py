"""FastAPI runtime foundation for CivicBudget."""
import os

from civiccore import __version__ as CIVICCORE_VERSION
from civiccore.auth import AuthenticatedPrincipal, authorize_bearer_roles
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicbudget import __version__
from civicbudget.gfoa_review import review_gfoa_alignment
from civicbudget.hearing_packet import build_hearing_packet_checklist
from civicbudget.line_item_analysis import analyze_line_items
from civicbudget.memo import draft_budget_memo
from civicbudget.narrative import draft_budget_narrative
from civicbudget.persistence import BudgetWorkpaperRepository, StoredBudgetNarrative, StoredHearingPacket
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

_workpaper_repository: BudgetWorkpaperRepository | None = None
_workpaper_db_url: str | None = None
_workpaper_bearer = HTTPBearer(auto_error=False)


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Return an empty favicon response so browser QA has a clean console."""

    return Response(status_code=204)


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
        "status": "budget narrative foundation plus workpaper persistence",
        "message": (
            "CivicBudget package, API foundation, line-item analysis, budget narratives, "
            "department memos, hearing packet checklists, resident summaries, GFOA checklist, "
            "optional database-backed narrative and hearing packet workpapers, and public UI foundation "
            "are online; ERP, budgeting system, accounting, payroll, budget adoption, official approvals, "
            "live LLM calls, and live finance-system connectors are not implemented yet."
        ),
        "next_step": (
            "Post-v0.1.2 roadmap: finance approval queues, ERP read-only imports, and "
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


def _require_workpaper_reader(
    credentials: HTTPAuthorizationCredentials | None = Depends(_workpaper_bearer),
) -> AuthenticatedPrincipal:
    return authorize_bearer_roles(
        credentials,
        service_name="CivicBudget",
        feature_name="persisted workpaper retrieval",
        token_roles_env_var="CIVICBUDGET_AUTH_TOKEN_ROLES",
        allowed_roles={"workpaper_reader", "budget_admin"},
    )


@app.post("/api/v1/civicbudget/narrative")
def narrative(request: NarrativeRequest) -> dict[str, object]:
    if _workpaper_database_url() is not None:
        stored = _get_workpaper_repository().create_narrative(
            department=request.department,
            priorities=request.priorities,
            line_items=request.line_items,
        )
        return _stored_narrative_response(stored)

    draft = draft_budget_narrative(
        request.department,
        request.priorities,
        request.line_items,
    )
    return {
        **draft.__dict__,
        "narrative_id": None,
        "variances": [v.__dict__ for v in draft.variances],
    }


@app.get("/api/v1/civicbudget/narrative/{narrative_id}")
def get_narrative(
    narrative_id: str,
    _principal: AuthenticatedPrincipal = Depends(_require_workpaper_reader),
) -> dict[str, object]:
    if _workpaper_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicBudget workpaper persistence is not configured.",
                "fix": "Set CIVICBUDGET_WORKPAPER_DB_URL to retrieve persisted budget narrative records.",
            },
        )
    stored = _get_workpaper_repository().get_narrative(narrative_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Budget narrative record not found.",
                "fix": "Use a narrative_id returned by POST /api/v1/civicbudget/narrative.",
            },
        )
    return _stored_narrative_response(stored)


@app.post("/api/v1/civicbudget/memo")
def memo(request: MemoRequest) -> dict[str, object]:
    return draft_budget_memo(
        request.department,
        request.audience,
        request.highlights,
    ).__dict__


@app.post("/api/v1/civicbudget/hearing-packet")
def hearing_packet(request: HearingPacketRequest) -> dict[str, object]:
    if _workpaper_database_url() is not None:
        stored = _get_workpaper_repository().create_hearing_packet(
            hearing_name=request.hearing_name,
            required_items=request.required_items,
        )
        return _stored_hearing_packet_response(stored)

    packet = build_hearing_packet_checklist(
        request.hearing_name,
        request.required_items,
    )
    payload = packet.__dict__
    payload["packet_id"] = None
    return payload


@app.get("/api/v1/civicbudget/hearing-packet/{packet_id}")
def get_hearing_packet(
    packet_id: str,
    _principal: AuthenticatedPrincipal = Depends(_require_workpaper_reader),
) -> dict[str, object]:
    if _workpaper_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicBudget workpaper persistence is not configured.",
                "fix": "Set CIVICBUDGET_WORKPAPER_DB_URL to retrieve persisted hearing packet records.",
            },
        )
    stored = _get_workpaper_repository().get_hearing_packet(packet_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Hearing packet record not found.",
                "fix": "Use a packet_id returned by POST /api/v1/civicbudget/hearing-packet.",
            },
        )
    return _stored_hearing_packet_response(stored)


@app.post("/api/v1/civicbudget/resident-summary")
def resident_summary(request: ResidentSummaryRequest) -> dict[str, object]:
    return draft_resident_summary(request.topic, request.facts).__dict__


@app.post("/api/v1/civicbudget/gfoa-review")
def gfoa_review(request: GFOARequest) -> dict[str, object]:
    return review_gfoa_alignment(request.pursued).__dict__


def _workpaper_database_url() -> str | None:
    return os.environ.get("CIVICBUDGET_WORKPAPER_DB_URL")


def _get_workpaper_repository() -> BudgetWorkpaperRepository:
    global _workpaper_db_url, _workpaper_repository
    db_url = _workpaper_database_url()
    if db_url is None:
        raise RuntimeError("CIVICBUDGET_WORKPAPER_DB_URL is not configured.")
    if _workpaper_repository is None or db_url != _workpaper_db_url:
        _dispose_workpaper_repository()
        _workpaper_db_url = db_url
        _workpaper_repository = BudgetWorkpaperRepository(db_url=db_url)
    return _workpaper_repository


def _dispose_workpaper_repository() -> None:
    global _workpaper_repository
    if _workpaper_repository is not None:
        _workpaper_repository.engine.dispose()
        _workpaper_repository = None


def _stored_narrative_response(stored: StoredBudgetNarrative) -> dict[str, object]:
    return {
        "narrative_id": stored.narrative_id,
        "department": stored.department,
        "priorities": list(stored.priorities),
        "line_items": list(stored.line_items),
        "sections": list(stored.sections),
        "variances": [variance.__dict__ for variance in stored.variances],
        "requires_finance_review": stored.requires_finance_review,
        "created_at": stored.created_at.isoformat(),
    }


def _stored_hearing_packet_response(stored: StoredHearingPacket) -> dict[str, object]:
    return {
        "packet_id": stored.packet_id,
        "hearing_name": stored.hearing_name,
        "required_items": list(stored.required_items),
        "checklist": list(stored.checklist),
        "clerk_handoff_required": stored.clerk_handoff_required,
        "created_at": stored.created_at.isoformat(),
    }
