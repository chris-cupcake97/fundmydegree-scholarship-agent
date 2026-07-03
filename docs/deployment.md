# Deployment Plan

## Goals

ScholarProof must be easy to run locally, easy to evaluate, and clear enough to deploy to Cloud Run or an equivalent service.

## Required Deployment Artifacts

- `Dockerfile`
- Optional `docker-compose.yml`
- `.env.example`
- `/health` endpoint
- README setup instructions
- Cloud Run or equivalent deployment instructions

## Environment Variables

Use `.env.example` for names only. Do not commit real values.

Planned variables:

```text
APP_ENV=development
FIXTURE_MODE=true
DATABASE_URL=sqlite:///data/scholarproof.db
LOG_LEVEL=info
```

If live APIs are added later, add only placeholder names:

```text
SEARCH_API_KEY=
MODEL_API_KEY=
```

## Local Run Plan

Planned commands:

```bash
python -m scholarproof
python evals/run_evals.py
```

## Docker Run Plan

Planned commands:

```bash
docker build -t scholarproof .
docker run --env-file .env -p 8080:8080 scholarproof
```

## Health Check

The backend must expose:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok",
  "fixture_mode": true
}
```

## Demo Reliability

The app must run in fixture mode without live web search.

Live search can be optional, but it must not be required for Kaggle demo.
