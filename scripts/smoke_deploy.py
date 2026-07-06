"""Smoke test deployment-facing app behavior."""

from __future__ import annotations

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

from fundmydegree.api.app import UI_DIST, app  # noqa: E402


def main() -> int:
    client = TestClient(app)

    health = client.get("/health")
    assert health.status_code == 200, health.text
    assert health.json()["status"] == "ok"

    docs = client.get("/docs")
    assert docs.status_code == 200, docs.text

    assert UI_DIST.exists(), "Frontend dist is missing. Run `npm run build` in fundmydegree/ui first."
    index = client.get("/")
    assert index.status_code == 200, index.text[:200]
    assert "FundMyDegree" in index.text

    print("FundMyDegree deployment smoke")
    print("health: ok")
    print("docs: ok")
    print("frontend_static: ok")
    print("passed: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
