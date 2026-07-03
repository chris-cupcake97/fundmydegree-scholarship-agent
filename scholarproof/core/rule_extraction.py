"""Deterministic fixture rule extraction and profile matching."""

from __future__ import annotations

from .models import EligibilityRule, StudentProfile


def extract_rules(
    page_text: str,
    source_url: str,
    fixture_rules: list[dict] | None = None,
) -> list[EligibilityRule]:
    """Extract eligibility rules.

    The MVP eval harness uses curated JSON fixtures, so this function accepts
    fixture rules directly. Later agent/tool implementations can replace this
    with model-assisted extraction while keeping the same output shape.
    """

    del page_text
    return [
        EligibilityRule.from_mapping(rule_data, source_url=source_url)
        for rule_data in fixture_rules or []
    ]


def match_profile(
    profile: StudentProfile,
    rules: list[EligibilityRule],
) -> tuple[list[EligibilityRule], list[EligibilityRule], list[EligibilityRule]]:
    """Partition extracted rules into matched, blocking, and unclear buckets."""

    del profile
    matched: list[EligibilityRule] = []
    blocking: list[EligibilityRule] = []
    unclear: list[EligibilityRule] = []

    for rule in rules:
        if rule.status == "blocking":
            blocking.append(rule)
        elif rule.status == "matched" and rule.has_evidence:
            matched.append(rule)
        else:
            unclear.append(rule)

    return matched, blocking, unclear

