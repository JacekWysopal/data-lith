# Dagster Orchestration

Dagster orchestrates the local analytics pipeline:

```text
dbt seed -> dbt run -> dbt test
```

## Run The Pipeline Once

From the repository root:

```powershell
docker compose --profile tools run --rm dagster `
  dagster job execute `
  -f /workspace/pipelines/dagster/definitions.py `
  -j analytics_pipeline
```

## Start The Dagster UI

```powershell
docker compose --profile orchestration up -d dagster
```

Open <http://localhost:3000>.

