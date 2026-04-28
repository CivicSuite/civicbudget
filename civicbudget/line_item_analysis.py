"""Line-item comparison helpers."""
from dataclasses import dataclass


@dataclass(frozen=True)
class LineItemVariance:
    account: str
    current_amount: float
    prior_amount: float
    variance: float
    percent_change: float
    review_note: str


def analyze_line_items(items: list[dict[str, float | str]]) -> list[LineItemVariance]:
    results = []
    for item in items:
        current = float(item.get("current_amount", 0))
        prior = float(item.get("prior_amount", 0))
        variance = current - prior
        pct = 0.0 if prior == 0 else (variance / prior) * 100
        note = (
            "Finance review required for material variance."
            if abs(pct) >= 10 or abs(variance) >= 50000
            else "Routine variance; finance review still required before publication."
        )
        results.append(
            LineItemVariance(
                str(item.get("account", "account")),
                current,
                prior,
                variance,
                pct,
                note,
            )
        )
    return results
