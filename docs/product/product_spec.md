# ScholarProof Product Spec

## Product

ScholarProof helps international students find scholarships that are real, current, and actually applicable to their profile.

Tagline: Find scholarships that are real - and right for you.

Track: Agents for Good

## Main User

An international student from a country like Sri Lanka looking for Master's or PhD funding abroad.

## Pain Point

Students do not want random scholarship lists. They need to know whether each opportunity is official, current, open to their country/residence/fee status, aligned with their degree and field, funded enough, still open, and worth their time.

## Core Rule

Unclear beats wrong.

Never mark a scholarship as `eligible` unless official evidence proves the key eligibility rules.

## MVP Features

- Student Profile Wizard.
- Find Scholarships screen.
- Eligibility Checker screen.
- Evidence Panel screen.
- Draft Clarification Email screen.
- Simple Saved Results screen.
- Evaluation runner.
- Security/audit logging.
- Deployability setup.
- Agent Skills folder.
- MCP/tool server layer.
- Kaggle documentation and video script.

## Out Of Scope

- Auto-filling university portals.
- Auto-submitting applications.
- Automatic email sending.
- Real passport, bank statement, or transcript upload.
- Full SOP/essay writer.
- Full student CRM.
- Claiming the system finds every scholarship globally.

## Status Mapping

| Backend status | UI label |
|---|---|
| `eligible` | Strong Fit |
| `unclear` | Needs Clarification |
| `not_eligible` | Not for You |
| `unverified` | Unverified Lead |

## Product Principle

ScholarProof is a source and eligibility verification assistant, not a scholarship application submitter.
