---
name: eligibility-rule-extraction
description: Extract structured scholarship eligibility rules from official source text.
version: 0.1.0
---

# Eligibility Rule Extraction

## When To Use

- Official source text needs normalized eligibility rules.
- A verifier needs nationality, residence, fee status, degree, field, funding, deadline, or application-process rules.
- Evidence snippets need to be attached to extracted rules.

## When Not To Use

- Do not use on unverified aggregator pages as proof.
- Do not decide final status.
- Do not draft clarification emails.

## Inputs

- Sanitized official page text.
- Source URL.
- Scholarship candidate.

## Outputs

List of `EligibilityRule` objects.

## Workflow

1. Identify rule-bearing text.
2. Extract rule type and requirement text.
3. Attach evidence text.
4. Mark rule status as pending for profile matching.
5. Return structured JSON.

## Rules

- Preserve evidence text.
- Do not infer missing rules.
- Mark vague or missing rules as unclear.

## Positive Trigger Examples

- "Extract eligibility rules from this source."
- "Find nationality and degree-level requirements."
- "Turn this scholarship page into structured rules."

## Negative Trigger Examples

- "Is this student eligible?"
- "Search for more scholarships."
- "Send a clarification email."

## Expected Output Format

```json
[
  {
    "rule_type": "degree_level",
    "requirement_text": "Applicants must apply for a Master's programme.",
    "evidence_text": "Open to Master's applicants...",
    "status": "pending",
    "confidence": 0.8
  }
]
```
