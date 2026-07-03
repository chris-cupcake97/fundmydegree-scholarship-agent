"""Run the ScholarProof API with `python -m scholarproof`."""

from __future__ import annotations


def main() -> None:
    try:
        import uvicorn
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "uvicorn is not installed. Run `python -m pip install -r requirements.txt` first."
        ) from exc

    uvicorn.run("scholarproof.api.app:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()

