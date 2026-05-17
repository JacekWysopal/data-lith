# Local Infrastructure

This folder contains the local foundation for the analytics platform:

- MinIO as the local lakehouse-compatible object store.
- Automatic creation of the `lakehouse` bucket with `raw`, `clean`, and `curated` prefixes.
- A DuckDB smoke test that writes a tiny local database under `storage/`.

## Start MinIO

```powershell
Copy-Item .env.example .env
docker compose up -d minio minio-init
```

MinIO API: <http://localhost:9000>

MinIO Console: <http://localhost:9001>

Default credentials are defined in `.env.example`.

## Run DuckDB Smoke Test

With local Python:

```powershell
py -m pip install -r requirements-dev.txt
py infrastructure/docker/duckdb_smoke.py
```

Or through Docker Compose:

```powershell
docker compose --profile tools run --rm duckdb-smoke
```
