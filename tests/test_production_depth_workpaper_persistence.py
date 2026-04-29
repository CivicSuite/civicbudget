from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civicbudget.main import app, _dispose_workpaper_repository
from civicbudget.persistence import BudgetWorkpaperRepository


client = TestClient(app)


def _sample_items() -> list[dict[str, float | str]]:
    return [{"account": "101", "current_amount": 150000, "prior_amount": 100000}]


def _auth_headers(token: str = "reader-token") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_repository_persists_narrative_and_hearing_packet(tmp_path: Path) -> None:
    db_path = tmp_path / "civicbudget.db"
    db_url = f"sqlite+pysqlite:///{db_path.as_posix()}"

    repository = BudgetWorkpaperRepository(db_url=db_url)
    narrative = repository.create_narrative(
        department="Parks",
        priorities=["Fields"],
        line_items=_sample_items(),
    )
    packet = repository.create_hearing_packet(
        hearing_name="FY27 budget hearing",
        required_items=["Memo"],
    )
    repository.engine.dispose()

    reloaded = BudgetWorkpaperRepository(db_url=db_url)
    stored_narrative = reloaded.get_narrative(narrative.narrative_id)
    stored_packet = reloaded.get_hearing_packet(packet.packet_id)
    reloaded.engine.dispose()

    assert stored_narrative is not None
    assert stored_narrative.department == "Parks"
    assert stored_narrative.requires_finance_review is True
    assert stored_narrative.variances[0].account == "101"
    assert stored_packet is not None
    assert stored_packet.hearing_name == "FY27 budget hearing"
    assert stored_packet.clerk_handoff_required is True
    db_path.unlink()


def test_workpaper_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicbudget-api.db"
    monkeypatch.setenv("CIVICBUDGET_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    monkeypatch.setenv(
        "CIVICBUDGET_AUTH_TOKEN_ROLES",
        '{"reader-token": ["workpaper_reader"], "admin-token": ["budget_admin"]}',
    )
    _dispose_workpaper_repository()

    created_narrative = client.post(
        "/api/v1/civicbudget/narrative",
        json={"department": "Parks", "priorities": ["Fields"], "line_items": _sample_items()},
    )
    narrative_id = created_narrative.json()["narrative_id"]
    fetched_narrative = client.get(
        f"/api/v1/civicbudget/narrative/{narrative_id}",
        headers=_auth_headers(),
    )
    created_packet = client.post(
        "/api/v1/civicbudget/hearing-packet",
        json={"hearing_name": "FY27 budget hearing", "required_items": ["Memo"]},
    )
    packet_id = created_packet.json()["packet_id"]
    fetched_packet = client.get(
        f"/api/v1/civicbudget/hearing-packet/{packet_id}",
        headers=_auth_headers("admin-token"),
    )

    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICBUDGET_WORKPAPER_DB_URL")
    monkeypatch.delenv("CIVICBUDGET_AUTH_TOKEN_ROLES")

    assert created_narrative.status_code == 200
    assert narrative_id
    assert fetched_narrative.status_code == 200
    assert fetched_narrative.json()["department"] == "Parks"
    assert created_packet.status_code == 200
    assert packet_id
    assert fetched_packet.status_code == 200
    assert fetched_packet.json()["hearing_name"] == "FY27 budget hearing"
    db_path.unlink()


def test_get_narrative_without_auth_config_returns_actionable_503(monkeypatch) -> None:
    monkeypatch.delenv("CIVICBUDGET_WORKPAPER_DB_URL", raising=False)
    monkeypatch.delenv("CIVICBUDGET_AUTH_TOKEN_ROLES", raising=False)
    _dispose_workpaper_repository()

    response = client.get("/api/v1/civicbudget/narrative/example")

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["message"] == "CivicBudget persisted workpaper retrieval auth is not configured."
    assert "Set CIVICBUDGET_AUTH_TOKEN_ROLES" in detail["fix"]


def test_get_narrative_requires_bearer_token(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicbudget-auth.db"
    monkeypatch.setenv("CIVICBUDGET_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    monkeypatch.setenv("CIVICBUDGET_AUTH_TOKEN_ROLES", '{"reader-token": ["workpaper_reader"]}')
    _dispose_workpaper_repository()

    created_narrative = client.post(
        "/api/v1/civicbudget/narrative",
        json={"department": "Parks", "priorities": ["Fields"], "line_items": _sample_items()},
    )
    narrative_id = created_narrative.json()["narrative_id"]
    response = client.get(f"/api/v1/civicbudget/narrative/{narrative_id}")

    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICBUDGET_WORKPAPER_DB_URL")
    monkeypatch.delenv("CIVICBUDGET_AUTH_TOKEN_ROLES")

    assert response.status_code == 401
    detail = response.json()["detail"]
    assert detail["message"] == "Bearer token required."
    assert "Authorization header" in detail["fix"]
    db_path.unlink()


def test_get_hearing_packet_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicbudget-missing.db"
    monkeypatch.setenv("CIVICBUDGET_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    monkeypatch.setenv("CIVICBUDGET_AUTH_TOKEN_ROLES", '{"reader-token": ["workpaper_reader"]}')
    _dispose_workpaper_repository()

    response = client.get("/api/v1/civicbudget/hearing-packet/missing", headers=_auth_headers())

    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICBUDGET_WORKPAPER_DB_URL")
    monkeypatch.delenv("CIVICBUDGET_AUTH_TOKEN_ROLES")

    assert response.status_code == 404
    detail = response.json()["detail"]
    assert detail["message"] == "Hearing packet record not found."
    assert "POST /api/v1/civicbudget/hearing-packet" in detail["fix"]
    db_path.unlink()
