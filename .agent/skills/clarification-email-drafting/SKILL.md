---
name: clarification-email-drafting
description: Draft a safe clarification email for scholarships with unclear official rules.
version: 0.1.0
---

# Clarification Email Drafting

## When To Use

- Verification status is `unclear`.
- One or more key rules need clarification.
- The student wants a draft to copy manually.

## When Not To Use

- Do not use for `eligible`, `not_eligible`, or `unverified` cases.
- Do not send email.
- Do not create a Send button.

## Inputs

- Scholarship name.
- Scholarship office or provider if known.
- Unclear rules.
- Student profile summary.

## Outputs

Structured draft:

- `to`
- `subject`
- `body`
- `questions_included`

## Workflow

1. Read unclear rules.
2. Draft concise polite questions.
3. Avoid sensitive personal details.
4. Return draft only.

## Rules

- Never send email.
- Ask only about unclear rules.
- Do not include passport, bank, transcript, or sensitive data.

## Safety Notes

- Return draft-only output with `send_allowed: false`.
- Do not invent eligibility advice inside the email.
- Do not include sensitive student documents or private financial details.

## Positive Trigger Examples

- "Draft a clarification email for this unclear scholarship."
- "Ask whether Sri Lankan citizens are eligible."
- "Ask if a separate scholarship application is required."

## Negative Trigger Examples

- "Send this email."
- "Apply for this scholarship."
- "Upload my passport."

## Expected Output Format

```json
{
  "to": "",
  "subject": "Clarification about scholarship eligibility",
  "body": "Dear Scholarship Office...",
  "questions_included": []
}
```
