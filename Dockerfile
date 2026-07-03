FROM node:20-slim AS ui-build

WORKDIR /app/scholarproof/ui

COPY scholarproof/ui/package*.json ./
RUN npm ci

COPY scholarproof/ui/ ./
RUN npm run build

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    FIXTURE_MODE=true \
    HOST=0.0.0.0 \
    PORT=8080

WORKDIR /app

RUN addgroup --system scholarproof && adduser --system --ingroup scholarproof scholarproof

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY .env.example README.md AGENTS.md ./
COPY config/ ./config/
COPY docs/ ./docs/
COPY evals/ ./evals/
COPY fixtures/ ./fixtures/
COPY scripts/ ./scripts/
COPY specs/ ./specs/
COPY scholarproof/ ./scholarproof/
COPY --from=ui-build /app/scholarproof/ui/dist ./scholarproof/ui/dist

USER scholarproof

EXPOSE 8080

CMD ["python", "-m", "scholarproof"]
