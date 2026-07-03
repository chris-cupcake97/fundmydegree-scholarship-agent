"""Simple in-memory persistence for the fixture-mode API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class InMemoryStore:
    profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    verifications: dict[str, dict[str, Any]] = field(default_factory=dict)
    verification_context: dict[str, dict[str, Any]] = field(default_factory=dict)
    saved_results: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    def reset(self) -> None:
        self.profiles.clear()
        self.verifications.clear()
        self.verification_context.clear()
        self.saved_results.clear()


store = InMemoryStore()

