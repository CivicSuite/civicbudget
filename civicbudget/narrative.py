"""Budget narrative drafting support."""
from dataclasses import dataclass

from civicbudget.line_item_analysis import LineItemVariance, analyze_line_items


@dataclass(frozen=True)
class BudgetNarrativeDraft:
    department: str
    sections: tuple[str, ...]
    variances: tuple[LineItemVariance, ...]
    requires_finance_review: bool


def draft_budget_narrative(
    department: str,
    priorities: list[str],
    line_items: list[dict[str, float | str]],
) -> BudgetNarrativeDraft:
    variances = tuple(analyze_line_items(line_items))
    priority_lines = tuple(f"Priority: {p.strip()}" for p in priorities if p.strip()) or (
        "Department priorities require budget lead input.",
    )
    return BudgetNarrativeDraft(
        department.strip(),
        (
            "Narrative must be reviewed by Finance before use.",
            *priority_lines,
            "Explain material line-item changes with source references.",
        ),
        variances,
        True,
    )
