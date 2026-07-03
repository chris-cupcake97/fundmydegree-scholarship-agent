# Cloud Run Deployment

ScholarProof is packaged as one container for the capstone demo. The container serves:

- React/Vite frontend from `/`
- FastAPI docs from `/docs`
- API routes from `/api/*`
- Health check from `/health`

## Build Locally

```bash
docker build -t scholarproof .
```

## Run Locally

```bash
docker run --rm -p 8080:8080 scholarproof
```

Open:

```text
http://127.0.0.1:8080/
http://127.0.0.1:8080/docs
http://127.0.0.1:8080/health
```

## Deploy To Cloud Run

Replace `PROJECT_ID` and `REGION` before running.

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/scholarproof
gcloud run deploy scholarproof \
  --image gcr.io/PROJECT_ID/scholarproof \
  --region REGION \
  --allow-unauthenticated \
  --set-env-vars APP_ENV=production,FIXTURE_MODE=true
```

## Runtime Notes

- The app listens on the `PORT` environment variable, defaulting to `8080` in Docker.
- Fixture/offline mode is used for reproducible demo behavior.
- Do not set real API keys for the MVP.
- Do not deploy sensitive documents or private student datasets.
