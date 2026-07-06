# FundMyDegree

Find scholarships that actually fit you.

FundMyDegree helps international students find scholarships that actually fit their profile.

I built this because scholarship discovery is not just about finding a long list of opportunities. Students often lose days on scholarships that look promising but are outdated, unclear, unofficial, or not applicable to their country, degree level, subject, or funding need. FundMyDegree focuses on a smaller but more useful question:

```text
Is this scholarship worth my time?
```

The app lets a student create a lightweight study profile, view scholarship matches, open a match, and see what fits, what needs confirmation, and what may not be worth applying for.

This is a Kaggle AI Agents capstone prototype. It uses fixture/offline data for a reproducible demo. It does not claim to find every scholarship in the world.

## Why I built this

International students do not just need more scholarship links. They need to know which scholarships fit their actual profile.

Aggregator sites and random scholarship lists can be useful starting points, but they often blur together official opportunities, outdated pages, vague eligibility rules, and listings that do not apply to a student's country, degree level, field, or funding need. That creates a lot of false hope and wasted effort.

FundMyDegree focuses on matching plus evidence. It is not trying to make blind recommendations. It tries to show why a scholarship looks relevant, what still needs to be confirmed, and when the safer answer is not to treat it as a fit yet.

## What the app does

1. The student fills a lightweight study profile.
2. FundMyDegree shows scholarship matches.
3. The student opens a scholarship.
4. The agent checks source evidence and profile fit.
5. The app groups results as Best Matches, Need to Confirm, Not for You, or Couldn't Verify Yet.
6. If something is unclear, the app can prepare an Ask to confirm draft.
7. The email is draft-only. It is never sent automatically.

## What makes it different

Most scholarship tools stop at discovery. FundMyDegree adds a fit-checking layer.

It does not just ask:

```text
Does this scholarship exist?
```

It asks:

```text
Does this scholarship look relevant for this student, based on available evidence?
```

That distinction matters. A scholarship can exist and still be the wrong use of a student's time. FundMyDegree keeps uncertainty visible instead of hiding it behind a confident-looking recommendation.

## Demo flow

1. Open the app.
2. Complete My Profile.
3. Go to My Matches.
4. Open a scholarship match.
5. Review what matches, what needs confirmation, and what may stop the student applying.
6. Save the scholarship or copy an Ask to confirm draft.

## How the agent works

```text
Student profile
  |
  v
Finder Agent finds candidate scholarships
  |
  v
Tool layer loads fixture scholarship data
  |
  v
Verifier Agent checks source, rules, and profile fit
  |
  v
Conservative verdict engine chooses the safest status
  |
  v
Frontend shows the result in student-friendly language
```

The detailed architecture lives in `docs/` for anyone who wants deeper implementation notes.

## Course concepts demonstrated

- Agent / multi-agent workflow: Root Orchestrator Agent, Finder Agent, Verifier Agent, and clarification email wrapper.
- MCP-style tool layer: tools such as `search_scholarships`, `classify_source`, `extract_rules`, `match_profile`, `generate_verdict`, and `detect_prompt_injection`.
- Agent Skills: skill folders for source checking, rule extraction, conservative verdicting, and clarification email drafting.
- Security features: no auto-send, no auto-submit, no sensitive document upload, prompt-injection detection, official-source gate, and conservative fit decisions.
- Evaluation: golden fixture cases and eval runner with `false_eligible_count = 0`.
- Deployability: FastAPI backend, React/Vite frontend, Dockerfile, Docker Compose, `/health` endpoint, and deployment smoke test.
- Antigravity: demo notes and workflow documentation in `docs/`.

## Safety decisions

FundMyDegree is intentionally limited in what it can do.

- It does not upload passports, transcripts, bank statements, offer letters, or other sensitive student documents.
- The document section is only a checklist.
- It never sends emails automatically.
- It never submits applications.
- Aggregator-style sources are treated as leads, not proof.
- If a required rule is missing or unclear, the app prefers Need to Confirm instead of guessing.
- The hard eval target is `false_eligible_count = 0`.

## Current limitations

- Fixture/offline demo mode only.
- No live global scholarship search yet.
- No account system yet.
- No persistent database yet.
- No payment or subscription system.
- No guarantee of admission, funding, eligibility, or scholarship success.
- Final decisions belong to universities, governments, or scholarship providers.

## Tech stack

- Frontend: React + Vite
- Backend: FastAPI
- Core logic: Python
- Agent layer: ADK-style orchestrator and specialist agents
- Tool layer: MCP-style Python tools
- Evaluation: Python fixture-based eval runner
- Deployment: Docker

## Run locally

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
python -m fundmydegree
```

Backend docs:

```text
http://127.0.0.1:8000/docs
```

Run the frontend:

```bash
cd fundmydegree/ui
npm install
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5173/
```

Run the tool layer:

```bash
python -m fundmydegree.mcp_server list
python -m fundmydegree.mcp_server call classify_source fixture_id=eligible_01
```

Run with Docker:

```bash
docker build -t fundmydegree-scholarship-agent .
docker run --rm -p 8080:8080 fundmydegree-scholarship-agent
```

Docker URLs:

```text
http://127.0.0.1:8080/
http://127.0.0.1:8080/docs
http://127.0.0.1:8080/health
```

## Tests

Run the verification evals:

```bash
python -B evals/run_evals.py
```

Run smoke tests:

```bash
python -B scripts/smoke_api.py
python -B scripts/smoke_tools.py
python -B scripts/smoke_agents.py
python -B scripts/smoke_deploy.py
```

Run the frontend build:

```bash
cd fundmydegree/ui
npm run build
```

Expected key result:

```text
false_eligible_count = 0
```

## Project structure

- `fundmydegree/ui/` - React/Vite student UI.
- `fundmydegree/api/` - FastAPI backend.
- `fundmydegree/agents/` - Root Orchestrator, Finder, Verifier, and clarification email wrapper.
- `fundmydegree/mcp_server/` - MCP-style tool registry and tools.
- `fundmydegree/core/` - source checking, rule matching, verdict policy, and shared models.
- `fixtures/` - offline scholarship fixtures for the demo.
- `evals/` - golden eval cases and eval runner.
- `scripts/` - smoke tests.
- `docs/` - architecture, security, deployment, evaluation, and Kaggle notes.
- `Dockerfile` and `docker-compose.yml` - containerized demo setup.

## License

MIT License.
