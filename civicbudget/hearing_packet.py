"""Budget hearing packet checklist support."""
from dataclasses import dataclass

@dataclass(frozen=True)
class HearingPacketChecklist:
    hearing_name: str
    checklist: tuple[str,...]
    clerk_handoff_required: bool

def build_hearing_packet_checklist(hearing_name: str, required_items: list[str]) -> HearingPacketChecklist:
    items=tuple(i.strip() for i in required_items if i.strip())
    return HearingPacketChecklist(hearing_name.strip(), ("Confirm notice and agenda deadline.", *items, "Attach finance-approved memo and exhibits.", "Coordinate CivicClerk packet handoff."), True)
