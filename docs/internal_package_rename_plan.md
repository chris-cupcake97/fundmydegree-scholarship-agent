# Internal Package Rename Summary

## Decision

The internal Python package was renamed from the original working package name to `fundmydegree`.

## What Changed

- Python package path: `fundmydegree/`
- Backend entrypoint: `python -m fundmydegree`
- MCP-style tool entrypoint: `python -m fundmydegree.mcp_server`
- Frontend path: `fundmydegree/ui`
- Spec path: `specs/fundmydegree_system_spec.md`
- Docker build paths and runtime command now use `fundmydegree`
- Eval and smoke scripts import `fundmydegree`

## Why This Matters

The public repo now matches the FundMyDegree brand in both user-facing docs and implementation paths. This avoids the half-renamed appearance that can distract reviewers.

## Validation Required After Rename

```bash
python -B evals/run_evals.py
python -B scripts/smoke_api.py
python -B scripts/smoke_tools.py
python -B scripts/smoke_agents.py
python -B scripts/smoke_deploy.py
cd fundmydegree/ui
npm run build
docker build -t fundmydegree-scholarship-agent .
```
