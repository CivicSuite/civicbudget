"""Department budget memo assembly."""
from dataclasses import dataclass


@dataclass(frozen=True)
class BudgetMemoDraft:
    department: str
    audience: str
    sections: tuple[str, ...]
    not_a_approval: bool


def draft_budget_memo(department: str, audience: str, highlights: list[str]) -> BudgetMemoDraft:
    lines = tuple(h.strip() for h in highlights if h.strip()) or (
        "Budget highlights require finance input.",
    )
    return BudgetMemoDraft(
        department.strip(),
        audience.strip(),
        (
            "Purpose and context",
            *lines,
            "Fiscal impact and source references",
            "Finance review status",
        ),
        True,
    )
