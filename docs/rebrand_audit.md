# Rebrand Audit

## Summary

The public product name is FundMyDegree.

Tagline: Find scholarships that actually fit you.

Short description: FundMyDegree helps international students find scholarships that match their profile, then shows what fits, what needs confirmation, and what may not be worth their time before they apply.

## Initial Occurrences Found

The final polish search looked for:

- `ScholarProof`
- `scholarproof`
- `Scholar Proof`
- `official evidence first`
- `Find scholarships that are real and right for you`

Occurrences found before the cleanup:

| Location | Occurrence | Action |
|---|---|---|
| `.dockerignore` | `scholarproof/ui/node_modules/`, `scholarproof/ui/dist/` | Changed to `fundmydegree/ui/...` |
| `.agent/skills/conservative-verdicting/SKILL.md` | Product name in skill description and prompt example | Changed to FundMyDegree |
| `.agent/skills/official-source-verification/SKILL.md` | Product name in skill description | Changed to FundMyDegree |
| `.env.example` | `DATABASE_URL=sqlite:///data/scholarproof.db` | Removed because the current demo uses an in-memory fixture store |
| `docker-compose.yml` | `scholarproof` service name | Changed to `fundmydegree` |
| `Dockerfile` | package paths, Linux user, and `python -m scholarproof` command | Changed to `fundmydegree` |
| `deploy/cloud-run.md` | old internal package note | Rewritten to use `python -m fundmydegree` |
| `docs/antigravity_demo_steps.md` | old spec path and screen names | Updated to FundMyDegree paths and current UI names |
| `docs/architecture.md` | old package note and implementation wording | Updated to FundMyDegree and in-memory fixture store |
| `docs/deployment.md` | old package note, old module command, old frontend path, old DB URL | Updated or removed |
| `docs/kaggle_rubric_mapping.md` | old package note and old code paths | Updated to `fundmydegree/...` |
| `docs/rebrand_audit.md` | old decision saying package was not renamed | Replaced with this audit |
| `docs/internal_package_rename_plan.md` | old plan saying not to rename | Replaced with a rename summary |
| `README.md` | naming note, Mermaid diagram, old package paths, old module commands | Rewritten |
| `LICENSE` | old contributor name | Changed to FundMyDegree contributors |
| `evals/run_evals.py` | import from old package | Changed to `fundmydegree` |
| `scripts/smoke_api.py` | import from old package | Changed to `fundmydegree` |
| `scripts/smoke_tools.py` | imports from old package | Changed to `fundmydegree` |
| `scripts/smoke_agents.py` | imports from old package | Changed to `fundmydegree` |
| `scripts/smoke_deploy.py` | import and old UI build path message | Changed to `fundmydegree` |
| `scholarproof/` | Python package and UI folder path | Renamed to `fundmydegree/` |
| `specs/scholarproof_system_spec.md` | old spec filename | Renamed to `specs/fundmydegree_system_spec.md` |
| Python package files | imports such as `from scholarproof...` | Changed to `from fundmydegree...` |

No occurrences were found for:

- `Scholar Proof`
- `official evidence first`
- `Find scholarships that are real and right for you`

## Package Rename Result

The internal package rename succeeded.

Current implementation paths:

- `fundmydegree/core/`
- `fundmydegree/api/`
- `fundmydegree/mcp_server/`
- `fundmydegree/agents/`
- `fundmydegree/ui/`
- `specs/fundmydegree_system_spec.md`

Current module commands:

```bash
python -m fundmydegree
python -m fundmydegree.mcp_server list
```

## Public-Facing Language

Public docs and UI now use:

- My Profile
- My Matches
- Saved
- Does this scholarship fit you?
- Why this match?
- Ask to confirm
- Best Matches
- Need to Confirm
- Not for You
- Couldn't Verify Yet

## Remaining Occurrences

There should be no remaining `ScholarProof`, `scholarproof`, or `Scholar Proof` occurrences in public-facing docs, code paths, or UI.

The only acceptable historical references are inside this audit when explaining what was searched and changed.
