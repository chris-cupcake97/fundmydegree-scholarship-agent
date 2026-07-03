---
name: conservative-verdicting
description: Apply ScholarProof's unclear-beats-wrong verdict policy to matched scholarship rules.
version: 0.1.0
---

# Conservative Verdicting

## When To Use

- Source classification and eligibility rules are available.
- Matched, blocking, and unclear rules need final status.
- A verifier needs to prevent false eligible results.

## When Not To Use

- Do not use before source classification.
- Do not use without evidence.
- Do not use for email drafting.

## Inputs

- Student profile.
- Official source classification.
- Extracted rules.
- Matched rules.
- Blocking rules.
- Unclear rules.

## Outputs

`VerificationResult` status:

- `eligible`
- `unclear`
- `not_eligible`
- `unverified`

## Workflow

1. Reject `eligible` if source is missing or not official.
2. Return `not_eligible` when an official source has a blocking rule.
3. Return `unclear` when official evidence is incomplete, vague, missing, or contradictory.
4. Return `eligible` only when every required claim has official evidence.

## Rules

- False eligible count must be 0.
- Aggregators are never proof.
- Missing evidence means unclear.

## Positive Trigger Examples

- "Generate the final verdict from these matched rules."
- "Apply the ScholarProof verdict policy."
- "Check whether this can be Strong Fit."

## Negative Trigger Examples

- "Find scholarships."
- "Classify this URL."
- "Write the student email."

## Expected Output Format

```json
{
  "status": "unclear",
  "student_facing_status": "Needs Clarification",
  "verdict_reason": "Funding amount is not explicit on the official source.",
  "matched_rules": [],
  "blocking_rules": [],
  "unclear_rules": []
}
```
