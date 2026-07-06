"""Fixture-backed verification flow used by evals and offline demos."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import AuditEvent, ScholarshipCandidate, StudentProfile, VerificationResult
from .rule_extraction import extract_rules, match_profile
from .security import detect_prompt_injection
from .source_classifier import classify_source
from .verdict_engine import generate_verdict


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_fixture_case(case: dict[str, Any], root: Path | None = None) -> VerificationResult:
    """Run the core tool trajectory against one fixture case."""

    base = root or repo_root()
    audit_log: list[AuditEvent] = []

    def audit(step: str, tool: str, input_summary: str, output_summary: str, success: bool = True) -> None:
        audit_log.append(
            AuditEvent(
                step=step,
                tool=tool,
                input_summary=input_summary,
                output_summary=output_summary,
                success=success,
            )
        )

    profile = StudentProfile.from_mapping(case["profile"])
    candidate = ScholarshipCandidate.from_mapping(case["candidate"])

    fixture_path = base / "fixtures" / "scholarships" / case["fixture"]
    fixture = _read_json(fixture_path)
    page_text = str(fixture.get("page_text", ""))
    fixture_rules = list(fixture.get("rules", []))
    source_url = str(fixture.get("url", candidate.candidate_url))
    provider = str(fixture.get("provider", candidate.provider))

    audit(
        "1",
        "fetch_page",
        f"fixture={case['fixture']}",
        f"loaded url={source_url or '<missing>'}",
    )

    source = classify_source(source_url, provider=provider, config_path=base / "config" / "trusted_sources.yml")
    audit(
        "2",
        "classify_source",
        f"url={source_url or '<missing>'}",
        f"type={source.source_type}; official={source.is_official}",
    )

    security_flags = detect_prompt_injection(page_text)
    audit(
        "3",
        "detect_prompt_injection",
        f"text_chars={len(page_text)}",
        f"flags={len(security_flags)}",
    )

    rules = extract_rules(page_text, source_url=source_url, fixture_rules=fixture_rules)
    audit(
        "4",
        "extract_rules",
        f"text_chars={len(page_text)}",
        f"rules={len(rules)}",
    )

    matched_rules, blocking_rules, unclear_rules = match_profile(profile, rules)
    audit(
        "5",
        "match_profile",
        f"profile={profile.id}; rules={len(rules)}",
        f"matched={len(matched_rules)}; blocking={len(blocking_rules)}; unclear={len(unclear_rules)}",
    )

    result = generate_verdict(
        profile=profile,
        candidate=candidate,
        source=source,
        matched_rules=matched_rules,
        blocking_rules=blocking_rules,
        unclear_rules=unclear_rules,
        security_flags=security_flags,
        audit_log=audit_log,
    )
    audit(
        "6",
        "generate_verdict",
        f"candidate={candidate.id}",
        f"status={result.status}",
    )

    audit(
        "7",
        "write_audit_log",
        f"verification={result.id}",
        f"events={len(audit_log) + 1}",
    )
    return result

