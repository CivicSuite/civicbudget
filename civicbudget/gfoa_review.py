"""Optional GFOA presentation alignment checklist."""
from dataclasses import dataclass

@dataclass(frozen=True)
class GFOAAlignmentReview:
    pursued: bool
    checklist: tuple[str,...]
    boundary: str

def review_gfoa_alignment(pursued: bool) -> GFOAAlignmentReview:
    return GFOAAlignmentReview(pursued, ("Reader guide", "Financial summaries", "Capital/debt context", "Policy and fund descriptions") if pursued else ("GFOA award alignment not pursued for this packet.",), "Checklist only; CivicBudget does not certify GFOA compliance.")
