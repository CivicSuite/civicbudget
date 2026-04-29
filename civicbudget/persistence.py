from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civicbudget.hearing_packet import build_hearing_packet_checklist
from civicbudget.line_item_analysis import LineItemVariance
from civicbudget.narrative import draft_budget_narrative


metadata = sa.MetaData()

budget_narrative_records = sa.Table(
    "budget_narrative_records",
    metadata,
    sa.Column("narrative_id", sa.String(36), primary_key=True),
    sa.Column("department", sa.String(255), nullable=False),
    sa.Column("priorities", sa.JSON(), nullable=False),
    sa.Column("line_items", sa.JSON(), nullable=False),
    sa.Column("sections", sa.JSON(), nullable=False),
    sa.Column("variances", sa.JSON(), nullable=False),
    sa.Column("requires_finance_review", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicbudget",
)

hearing_packet_records = sa.Table(
    "hearing_packet_records",
    metadata,
    sa.Column("packet_id", sa.String(36), primary_key=True),
    sa.Column("hearing_name", sa.String(500), nullable=False),
    sa.Column("required_items", sa.JSON(), nullable=False),
    sa.Column("checklist", sa.JSON(), nullable=False),
    sa.Column("clerk_handoff_required", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicbudget",
)


@dataclass(frozen=True)
class StoredBudgetNarrative:
    narrative_id: str
    department: str
    priorities: tuple[str, ...]
    line_items: tuple[dict[str, float | str], ...]
    sections: tuple[str, ...]
    variances: tuple[LineItemVariance, ...]
    requires_finance_review: bool
    created_at: datetime


@dataclass(frozen=True)
class StoredHearingPacket:
    packet_id: str
    hearing_name: str
    required_items: tuple[str, ...]
    checklist: tuple[str, ...]
    clerk_handoff_required: bool
    created_at: datetime


class BudgetWorkpaperRepository:
    """SQLAlchemy-backed budget narrative and hearing-packet workpaper records."""

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civicbudget": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civicbudget"))
        metadata.create_all(self.engine)

    def create_narrative(
        self,
        *,
        department: str,
        priorities: list[str],
        line_items: list[dict[str, float | str]],
    ) -> StoredBudgetNarrative:
        draft = draft_budget_narrative(department, priorities, line_items)
        stored = StoredBudgetNarrative(
            narrative_id=str(uuid4()),
            department=draft.department,
            priorities=tuple(priorities),
            line_items=tuple(dict(item) for item in line_items),
            sections=draft.sections,
            variances=draft.variances,
            requires_finance_review=draft.requires_finance_review,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                budget_narrative_records.insert().values(
                    narrative_id=stored.narrative_id,
                    department=stored.department,
                    priorities=list(stored.priorities),
                    line_items=list(stored.line_items),
                    sections=list(stored.sections),
                    variances=[variance.__dict__ for variance in stored.variances],
                    requires_finance_review=stored.requires_finance_review,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_narrative(self, narrative_id: str) -> StoredBudgetNarrative | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(budget_narrative_records).where(
                    budget_narrative_records.c.narrative_id == narrative_id
                )
            ).mappings().first()
        if row is None:
            return None
        return _row_to_narrative(row)

    def create_hearing_packet(
        self, *, hearing_name: str, required_items: list[str]
    ) -> StoredHearingPacket:
        packet = build_hearing_packet_checklist(hearing_name, required_items)
        stored = StoredHearingPacket(
            packet_id=str(uuid4()),
            hearing_name=packet.hearing_name,
            required_items=tuple(required_items),
            checklist=packet.checklist,
            clerk_handoff_required=packet.clerk_handoff_required,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                hearing_packet_records.insert().values(
                    packet_id=stored.packet_id,
                    hearing_name=stored.hearing_name,
                    required_items=list(stored.required_items),
                    checklist=list(stored.checklist),
                    clerk_handoff_required=stored.clerk_handoff_required,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_hearing_packet(self, packet_id: str) -> StoredHearingPacket | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(hearing_packet_records).where(hearing_packet_records.c.packet_id == packet_id)
            ).mappings().first()
        if row is None:
            return None
        return _row_to_hearing_packet(row)


def _row_to_narrative(row: object) -> StoredBudgetNarrative:
    data = dict(row)
    return StoredBudgetNarrative(
        narrative_id=data["narrative_id"],
        department=data["department"],
        priorities=tuple(data["priorities"]),
        line_items=tuple(dict(item) for item in data["line_items"]),
        sections=tuple(data["sections"]),
        variances=tuple(LineItemVariance(**variance) for variance in data["variances"]),
        requires_finance_review=data["requires_finance_review"],
        created_at=data["created_at"],
    )


def _row_to_hearing_packet(row: object) -> StoredHearingPacket:
    data = dict(row)
    return StoredHearingPacket(
        packet_id=data["packet_id"],
        hearing_name=data["hearing_name"],
        required_items=tuple(data["required_items"]),
        checklist=tuple(data["checklist"]),
        clerk_handoff_required=data["clerk_handoff_required"],
        created_at=data["created_at"],
    )
