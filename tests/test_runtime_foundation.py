from fastapi.testclient import TestClient

from civicbudget import __version__
from civicbudget.main import app

client = TestClient(app)


def test_root_reports_honest_current_state():
    payload = client.get("/").json()

    assert payload["name"] == "CivicBudget"
    assert payload["version"] == __version__
    assert payload["status"] == "budget narrative foundation plus workpaper persistence"
    assert "database-backed narrative and hearing packet workpapers" in payload["message"]
    assert "ERP" in payload["message"]
    assert "not implemented yet" in payload["message"]


def test_health_reports_civiccore_pin():
    assert client.get("/health").json() == {
        "status": "ok",
        "service": "civicbudget",
        "version": "0.1.2",
        "civiccore_version": "0.4.0",
    }


def test_public_ui_contains_version_boundaries_and_dependency():
    text = client.get("/civicbudget").text

    assert "CivicBudget v0.1.2" in text
    assert "No ERP" in text
    assert "civiccore==0.4.0" in text


def test_api_endpoints_return_deterministic_payloads():
    items = [{"account": "101", "current_amount": 150000, "prior_amount": 100000}]

    assert client.post("/api/v1/civicbudget/line-items", json={"items": items}).status_code == 200
    assert (
        client.post(
            "/api/v1/civicbudget/narrative",
            json={"department": "Parks", "priorities": ["Fields"], "line_items": items},
        ).json()["narrative_id"]
        is None
    )
    assert (
        client.post(
            "/api/v1/civicbudget/memo",
            json={
                "department": "Finance",
                "audience": "Council",
                "highlights": ["Balanced"],
            },
        ).json()["not_a_approval"]
        is True
    )
    assert (
        client.post(
            "/api/v1/civicbudget/hearing-packet",
            json={"hearing_name": "FY27", "required_items": ["Memo"]},
        ).json()["packet_id"]
        is None
    )
    assert (
        client.post(
            "/api/v1/civicbudget/resident-summary",
            json={"topic": "General fund", "facts": ["Revenue up"]},
        ).status_code
        == 200
    )
    assert client.post("/api/v1/civicbudget/gfoa-review", json={"pursued": True}).status_code == 200
