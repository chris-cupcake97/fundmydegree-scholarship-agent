# Agent Skills

FundMyDegree includes four focused agent skills. Each skill has one job and supports the conservative scholarship verification workflow.

## Official Source Verification

- Location: `.agent/skills/official-source-verification/SKILL.md`
- Purpose: classify whether a scholarship source can count as official evidence.
- Supports: source classification, aggregator rejection, official-source gate.
- Covered by: `scripts/smoke_tools.py`, `evals/run_evals.py`.

## Eligibility Rule Extraction

- Location: `.agent/skills/eligibility-rule-extraction/SKILL.md`
- Purpose: extract structured scholarship rules from official source text or fixture rule data.
- Supports: nationality, residence, degree, field, funding, deadline, and application-process checks.
- Covered by: `scripts/smoke_tools.py`, `evals/run_evals.py`.

## Conservative Verdicting

- Location: `.agent/skills/conservative-verdicting/SKILL.md`
- Purpose: apply the unclear-beats-wrong policy to matched, blocking, and unclear rules.
- Supports: `eligible`, `unclear`, `not_eligible`, and `unverified` verdicts.
- Covered by: `scripts/smoke_agents.py`, `scripts/smoke_tools.py`, `evals/run_evals.py`.

## Clarification Email Drafting

- Location: `.agent/skills/clarification-email-drafting/SKILL.md`
- Purpose: draft a safe clarification email only for unclear cases.
- Supports: Ask to confirm workflow.
- Covered by: `scripts/smoke_api.py`, `scripts/smoke_agents.py`.

## Skill Quality Check

Each skill includes:

- Specific description for routing.
- When to use.
- When not to use.
- Inputs and outputs.
- Expected output shape.
- Safety notes.
- Positive trigger examples.
- Negative trigger examples.

These skills guide the agent workflow; they do not add live web search, automatic email sending, application submission, or document upload.
