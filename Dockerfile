FROM node:20-slim AS ui-build

WORKDIR /app/fundmydegree/ui

COPY fundmydegree/ui/package*.json ./
RUN npm ci

COPY fundmydegree/ui/ ./
RUN npm run build

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    FIXTURE_MODE=true \
    HOST=0.0.0.0 \
    PORT=8080

WORKDIR /app

RUN addgroup --system fundmydegree && adduser --system --ingroup fundmydegree fundmydegree

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY .env.example README.md AGENTS.md ./
COPY config/ ./config/
COPY docs/ ./docs/
COPY evals/ ./evals/
COPY fixtures/ ./fixtures/
COPY scripts/ ./scripts/
COPY specs/ ./specs/
COPY fundmydegree/ ./fundmydegree/
COPY --from=ui-build /app/fundmydegree/ui/dist ./fundmydegree/ui/dist

USER fundmydegree

EXPOSE 8080

CMD ["python", "-m", "fundmydegree"]
