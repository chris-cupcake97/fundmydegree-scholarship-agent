# Deployment Plan

## Goals

FundMyDegree must be easy to run locally, easy to evaluate, and clear enough to deploy to Cloud Run or an equivalent container service.

## Current Deployment Readiness

- Dockerfile.
- Optional Docker Compose file.
- `.env.example`.
- `/health` endpoint.
- README setup instructions.
- Fixture/offline demo mode.
- Backend, tool, agent, eval, frontend, and deployment smoke checks.
- MCP-compatible protocol smoke check.
- Single-container serving for backend API and built frontend UI.

## Runtime Shape

The deployment container serves:

- React/Vite frontend from `/`.
- FastAPI docs from `/docs`.
- API routes from `/api/*`.
- Health check from `/health`.

The frontend uses same-origin API calls in deployed builds. During local Vite development, it calls `http://127.0.0.1:8000`.

## Environment Variables

Use `.env.example` for names only. Do not commit real values.

```text
APP_ENV=production
FIXTURE_MODE=true
LOG_LEVEL=info
HOST=0.0.0.0
PORT=8080
```

If live APIs are added later, add only placeholder names:

```text
SEARCH_API_KEY=
MODEL_API_KEY=
```

## Local Backend Run

```bash
python -m fundmydegree
```

Default local backend:

```text
http://127.0.0.1:8000
```

## Local Frontend Run

```bash
cd fundmydegree/ui
npm install
npm run dev
```

Default local frontend:

```text
http://127.0.0.1:5173/
```

## Container Build

```bash
docker build -t fundmydegree-scholarship-agent .
```

## Container Run

```bash
docker run --rm -p 8080:8080 fundmydegree-scholarship-agent
```

Open:

```text
http://127.0.0.1:8080/
http://127.0.0.1:8080/docs
http://127.0.0.1:8080/health
```

## Docker Compose

```bash
docker compose up --build
```

## Cloud Run

Cloud Run commands are documented in `deploy/cloud-run.md`.

## Health Check

The backend exposes:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok",
  "service": "fundmydegree-api",
  "mode": "fixture",
  "verdict_policy": "conservative"
}
```

## Pre-Deployment Checks

```bash
python -B evals/run_evals.py
python -B scripts/smoke_api.py
python -B scripts/smoke_tools.py
python -B scripts/smoke_mcp_protocol.py
python -B scripts/smoke_agents.py
python -B scripts/smoke_deploy.py
cd fundmydegree/ui
npm run build
```

If Docker is available locally:

```bash
docker build -t fundmydegree-scholarship-agent .
docker run --rm -p 8080:8080 fundmydegree-scholarship-agent
```

Then check:

```text
http://127.0.0.1:8080/health
http://127.0.0.1:8080/
```

Do not treat the Docker run as complete unless those local endpoints respond.

## Demo Reliability

The app runs in fixture mode without live web search. Live search can be optional later, but it must not be required for the current demo.
