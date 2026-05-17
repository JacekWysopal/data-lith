# Local Foundation

## Goal

Create a local analytics foundation with Docker Compose, MinIO, and DuckDB.

## Components

- `docker-compose.yml` starts MinIO and creates the initial lakehouse bucket and layer prefixes.
- `infrastructure/docker/duckdb_smoke.py` verifies that DuckDB can create schemas for the raw, clean, and curated layers.
- `storage/` remains the local filesystem mirror for development artifacts.

## Lakehouse Layers

- `raw`: source data preserved as close to the original shape as possible.
- `clean`: validated, typed, deduplicated, and normalized data.
- `curated`: analytics-ready marts, aggregates, and business-facing datasets.

## Commands

```powershell
Copy-Item .env.example .env
docker compose up -d minio minio-init
docker compose --profile tools run --rm duckdb-smoke
```
