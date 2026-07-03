"""Trusted source classification for scholarship evidence."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from .models import SourceClassification


AGGREGATOR_KEYWORDS: tuple[str, ...] = (
    "scholarshipportal",
    "scholars4dev",
    "wemakescholars",
    "scholarshiproar",
    "scholarship-positions",
    "mastersportal",
    "findamasters",
    "hotcourses",
    "educations.com",
    "studyabroad",
    "opportunities",
    "listicle",
    "blog",
)


PUBLIC_AUTHORITY_HINTS: tuple[str, ...] = (
    ".gov",
    "gov.",
    "europa.eu",
    "daad.de",
    "studyinsweden.se",
    "universityadmissions.se",
)


UNIVERSITY_HINTS: tuple[str, ...] = (
    ".ac.uk",
    ".edu",
    ".edu.",
    ".edu/",
    ".fi",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def domain_from_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url if "://" in url else f"https://{url}")
    domain = parsed.netloc.lower().strip()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def load_trusted_domains(config_path: str | Path | None = None) -> set[str]:
    """Load trusted domains from the small YAML policy without adding a dependency."""

    path = Path(config_path) if config_path else repo_root() / "config" / "trusted_sources.yml"
    trusted: set[str] = set()
    if not path.exists():
        return trusted

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("- "):
            continue
        value = line[2:].strip().strip("'\"")
        if "." in value and " " not in value:
            trusted.add(value.lower())
    return trusted


def _matches_domain(domain: str, trusted_domain: str) -> bool:
    return domain == trusted_domain or domain.endswith(f".{trusted_domain}")


def _provider_domain_hint(provider: str) -> str:
    return "".join(char for char in provider.lower() if char.isalnum())


def _source_type_for_official_domain(domain: str) -> str:
    if any(hint in domain for hint in PUBLIC_AUTHORITY_HINTS):
        return "official_government"
    if any(hint in domain for hint in UNIVERSITY_HINTS):
        return "official_university"
    return "official_provider"


def classify_source(
    url: str,
    provider: str = "",
    config_path: str | Path | None = None,
) -> SourceClassification:
    """Classify a URL before eligibility matching is allowed."""

    domain = domain_from_url(url)
    if not domain:
        return SourceClassification(
            url=url,
            domain="",
            source_type="missing_url",
            is_official=False,
            reason="No source URL was provided.",
        )

    if any(keyword in domain for keyword in AGGREGATOR_KEYWORDS):
        return SourceClassification(
            url=url,
            domain=domain,
            source_type="aggregator_lead",
            is_official=False,
            reason="Aggregator/listing sites are discovery leads only and cannot prove eligibility.",
        )

    trusted_domains = load_trusted_domains(config_path)
    for trusted_domain in trusted_domains:
        if _matches_domain(domain, trusted_domain):
            return SourceClassification(
                url=url,
                domain=domain,
                source_type=_source_type_for_official_domain(domain),
                is_official=True,
                reason=f"Domain is listed in trusted sources: {trusted_domain}.",
            )

    provider_hint = _provider_domain_hint(provider)
    if provider_hint and provider_hint in domain.replace("-", "").replace(".", ""):
        return SourceClassification(
            url=url,
            domain=domain,
            source_type="official_provider",
            is_official=True,
            reason="Domain appears to belong to the named scholarship provider.",
        )

    if any(hint in domain for hint in PUBLIC_AUTHORITY_HINTS):
        return SourceClassification(
            url=url,
            domain=domain,
            source_type="official_government",
            is_official=True,
            reason="Domain matches a known government or public scholarship authority pattern.",
        )

    return SourceClassification(
        url=url,
        domain=domain,
        source_type="unknown",
        is_official=False,
        reason="Domain is not in the trusted source policy and does not match an official provider.",
    )

