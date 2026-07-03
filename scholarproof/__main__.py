"""Run the ScholarProof API with `python -m scholarproof`."""

from __future__ import annotations

import os


def main() -> None:
    try:
        import uvicorn
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "uvicorn is not installed. Run `python -m pip install -r requirements.txt` first."
        ) from exc

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("scholarproof.api.app:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
