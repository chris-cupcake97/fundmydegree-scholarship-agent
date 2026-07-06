"""Security checks for untrusted scholarship page text."""

from __future__ import annotations

import re


INJECTION_PATTERNS: tuple[tuple[str, str], ...] = (
    ("ignore_previous_instructions", r"\bignore\s+(all\s+)?previous\s+instructions\b"),
    ("disregard_system_prompt", r"\bdisregard\s+(the\s+)?system\s+prompt\b"),
    ("mark_all_users_eligible", r"\bmark\s+all\s+users\s+eligible\b"),
    ("send_data_to_external_target", r"\bsend\s+(student\s+)?data\s+to\b"),
    ("reveal_api_key", r"\breveal\s+(the\s+)?api\s+key\b"),
    ("override_eligibility_rules", r"\boverride\s+eligibility\s+rules\b"),
    ("ignore_verdict_policy", r"\bignore\s+(the\s+)?verdict\s+policy\b"),
)


def detect_prompt_injection(text: str) -> list[str]:
    """Return security flags found in untrusted text."""

    flags: list[str] = []
    for name, pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            flags.append(f"prompt_injection:{name}")
    return flags

