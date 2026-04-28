"""Plain-English resident budget summary support."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ResidentBudgetSummary:
    topic: str
    bullets: tuple[str,...]
    requires_publication_review: bool

def draft_resident_summary(topic: str, facts: list[str]) -> ResidentBudgetSummary:
    bullets=tuple(f.strip() for f in facts if f.strip()) or ("Finance-approved facts required before summary.",)
    return ResidentBudgetSummary(topic.strip(), bullets, True)
