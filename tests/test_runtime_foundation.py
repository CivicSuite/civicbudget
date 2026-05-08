from pathlib import Path
import re
import tomllib

from fastapi.testclient import TestClient

from civicbudget import __version__
from civicbudget.main import app

client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_root_reports_honest_current_state():
    payload = client.get("/").json()

    assert payload["name"] == "CivicBudget"
    assert payload["version"] == __version__
    assert payload["status"] == "budget narrative foundation plus workpaper persistence"
    assert "database-backed narrative and hearing packet workpapers" in payload["message"]
    assert "ERP" in payload["message"]
    assert "not implemented yet" in payload["message"]


def test_health_reports_civiccore_pin():
    payload = client.get("/health").json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civicbudget"
    assert payload["version"] == "0.1.2"
    assert re.fullmatch(r"\d+\.\d+\.\d+", payload["civiccore_version"])


def test_public_ui_contains_version_boundaries_and_dependency():
    text = client.get("/civicbudget").text

    assert "CivicBudget v0.1.2" in text
    assert "No ERP" in text
    assert "published foundation label under suite-wide release-recovery review" in text
    assert "CivicCore v0.4.0 release wheel" in text
    assert "Shipping v0.1.2" not in text


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


def test_release_script_prefers_python3_and_avoids_windowsapps_fallback() -> None:
    lines = (ROOT / "scripts" / "verify-release.sh").read_text(encoding="utf-8").splitlines()
    candidate_line = next(line for line in lines if line.startswith("PYTHON_CANDIDATES+="))

    assert "python3 python py" in candidate_line
    assert "WindowsApps" not in candidate_line


def test_pyproject_uses_published_civiccore_release_wheel() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    dependencies = pyproject["project"]["dependencies"]
    assert any(
        dependency
        == "civiccore @ https://github.com/CivicSuite/civiccore/releases/download/v0.4.0/civiccore-0.4.0-py3-none-any.whl"
        for dependency in dependencies
    )
    assert pyproject["tool"]["hatch"]["metadata"]["allow-direct-references"] is True


def test_docs_gate_rejects_stale_shipping_product_ready_and_mojibake_markers() -> None:
    text = (ROOT / "scripts" / "verify-docs.sh").read_text(encoding="utf-8")

    assert '"Shipping v0.1.2"' in text
    assert '"Ships Today"' in text
    assert '"product-ready"' in text
    assert '"production-ready"' in text


def test_current_docs_are_version_and_dependency_current() -> None:
    current_docs = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in ["README.md", "README.txt", "USER-MANUAL.md", "USER-MANUAL.txt"]
    )

    assert "published CivicCore v0.4.0 release wheel" in current_docs
    assert "civiccore==0.3.0" not in current_docs
    assert "v0.1.1" not in current_docs


def test_docs_index_marks_foundation_label_provisional() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "published foundation label under suite-wide release-recovery review" in text
    assert "v0.1.2 foundation under recovery review" in text
    assert "release-recovery-status.md" in text
    assert "Shipping v0.1.2" not in text
    assert "Ships Today" not in text


def test_recovery_status_blocks_product_promotion() -> None:
    text = (ROOT / "docs" / "release-recovery-status.md").read_text(encoding="utf-8")

    assert "not product-ready" in text
    assert "must not be promoted as production municipal budget software" in text
