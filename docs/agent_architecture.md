# Agent Architecture

FundMyDegree uses an ADK-style multi-agent workflow in Python. It does not currently import or depend on the official Google ADK package.

The goal is to keep the agent design understandable and safe:

```text
Student profile
-> Root Orchestrator Agent
-> Finder Agent
-> Verifier Agent
-> Clarification Email Skill
-> Student-facing grouped results
```

## Root Orchestrator Agent

Location: `fundmydegree/agents/orchestrator.py`

Responsibilities:

- Accept a student profile and search query.
- Create or reuse a profile through the API service layer.
- Call the Finder Agent for candidates.
- Call the Verifier Agent for each candidate.
- Group results by conservative verdict.
- Never produce its own eligibility verdict.

## Finder Agent

Location: `fundmydegree/agents/finder.py`

Responsibilities:

- Call `search_scholarships`.
- Return structured scholarship candidates.
- Remove any status fields from candidate data.
- Never decide eligibility.
- Never label a candidate as a strong match.

## Verifier Agent

Location: `fundmydegree/agents/verifier.py`

Responsibilities:

- Execute the required tool sequence:
  1. `fetch_page`
  2. `classify_source`
  3. `detect_prompt_injection`
  4. `extract_rules`
  5. `match_profile`
  6. `generate_verdict`
  7. `write_audit_log`
- Return a `VerificationResult`.
- Preserve the conservative verdict policy.
- Reject false eligible outcomes.

## Clarification Email Skill

Location: `fundmydegree/agents/clarification_email.py`

Responsibilities:

- Draft a clarification email only for `unclear` verification results.
- Return `send_allowed: false`.
- Reject `eligible`, `not_eligible`, and `unverified` cases.
- Never send email.

## Smoke Test

```bash
python -B scripts/smoke_agents.py
```

The smoke test verifies orchestrator search, finder candidate output, verifier tool sequence, unclear-only email drafting, aggregator-unverified behavior, blocking-rule behavior, and false-eligible protection.
