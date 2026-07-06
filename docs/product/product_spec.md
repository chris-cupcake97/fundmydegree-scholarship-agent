# FundMyDegree Product Spec

## Product

FundMyDegree helps international students find scholarships that match their profile, then shows what fits, what needs confirmation, and what may not be worth their time before they apply.

Tagline: Find scholarships that actually fit you.

Track: Agents for Good

## Main User

An international student from a country like Sri Lanka looking for Master's or PhD funding abroad.

## Pain Point

Students do not want random scholarship lists. They need to know whether each opportunity is official, current, open to their country/residence/fee status, aligned with their degree and field, funded enough, still open, and worth their time.

## Core Rule

Unclear beats wrong.

Never mark a scholarship as `eligible` unless official evidence proves the key eligibility rules.

## MVP Features

- My Profile screen.
- My Matches screen.
- Does this scholarship fit you? screen.
- Why this match?? view.
- Ask to confirm action.
- Saved screen.
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
| `eligible` | Strong Match |
| `unclear` | Need to Confirm |
| `not_eligible` | Not for You |
| `unverified` | Couldn't Verify Yet |

## Product Principle

FundMyDegree is a scholarship matching and fit guidance assistant, not a scholarship application submitter.
