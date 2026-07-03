"""Smoke test the ScholarProof FastAPI routes in fixture mode."""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

warnings.filterwarnings(
    "ignore",
    message="Using `httpx` with `starlette.testclient` is deprecated.*",
    category=Warning,
)

from fastapi.testclient import TestClient  # noqa: E402

from scholarproof.api.app import app  # noqa: E402


def _load_case(case_id: str) -> dict:
    cases = json.loads((ROOT / "evals" / "eval_cases.json").read_text(encoding="utf-8"))
    for case in cases:
        if case["id"] == case_id:
            return case
    raise AssertionError(f"Missing smoke fixture case: {case_id}")


def _assert_ok(response, label: str) -> dict:
    assert response.status_code == 200, f"{label} failed: {response.status_code} {response.text}"
    return response.json()


def main() -> int:
    client = TestClient(app)
    unclear_case = _load_case("unclear_01")
    eligible_case = _load_case("eligible_01")

    health = _assert_ok(client.get("/health"), "health")
    assert health["status"] == "ok"

    profile_response = _assert_ok(
        client.post("/api/profile", json=unclear_case["profile"]),
        "create profile",
    )
    profile_id = profile_response["profile"]["id"]

    loaded_profile = _assert_ok(client.get(f"/api/profile/{profile_id}"), "get profile")
    assert loaded_profile["profile"]["id"] == profile_id

    search = _assert_ok(
        client.post("/api/search-scholarships", json={"profile_id": profile_id, "query": "Bristol"}),
        "search scholarships",
    )
    assert search["count"] >= 1

    unclear_verification = _assert_ok(
        client.post(
            "/api/verify-scholarship",
            json={"profile_id": profile_id, "fixture_id": unclear_case["id"]},
        ),
        "verify unclear scholarship",
    )["verification"]
    assert unclear_verification["status"] == "unclear"
    unclear_verification_id = unclear_verification["id"]

    evidence = _assert_ok(
        client.get(f"/api/evidence/{unclear_verification_id}"),
        "get evidence",
    )
    assert evidence["status"] == "unclear"
    assert evidence["source"]["official"] is True

    draft = _assert_ok(
        client.post(
            "/api/draft-email",
            json={"verification_id": unclear_verification_id, "student_name": "Demo Student"},
        ),
        "draft clarification email",
    )
    assert draft["send_allowed"] is False
    assert "Could you please clarify" in draft["body"]

    eligible_verification = _assert_ok(
        client.post(
            "/api/verify-scholarship",
            json={"profile_id": profile_id, "fixture_id": eligible_case["id"]},
        ),
        "verify eligible scholarship",
    )["verification"]
    assert eligible_verification["status"] == "eligible"

    blocked_draft = client.post(
        "/api/draft-email",
        json={"verification_id": eligible_verification["id"], "student_name": "Demo Student"},
    )
    assert blocked_draft.status_code == 400

    saved = _assert_ok(
        client.post(
            "/api/save-result",
            json={"verification_id": unclear_verification_id, "notes": "Needs country clarification."},
        ),
        "save result",
    )
    assert saved["saved_result"]["verification_id"] == unclear_verification_id

    saved_results = _assert_ok(
        client.get(f"/api/saved-results/{profile_id}"),
        "get saved results",
    )
    assert saved_results["count"] == 1

    audit = _assert_ok(
        client.get(f"/api/audit/{unclear_verification_id}"),
        "get audit",
    )
    assert [event["tool"] for event in audit["audit_log"]][-1] == "write_audit_log"

    print("ScholarProof API smoke")
    print("health: ok")
    print(f"profile_id: {profile_id}")
    print(f"unclear_verification_id: {unclear_verification_id}")
    print(f"eligible_verification_id: {eligible_verification['id']}")
    print("draft_email_unclear_only: ok")
    print("saved_results: ok")
    print("audit: ok")
    print("passed: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
