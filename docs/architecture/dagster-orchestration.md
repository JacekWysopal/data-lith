# Dagster Orchestration

## Goal

Use Dagster to run the local transformation pipeline as a repeatable job.

## Job

```text
analytics_pipeline
  dbt_seed
    -> dbt_run
      -> dbt_test
```

## Commands

Run the job once:

```powershell
docker compose --profile tools run --rm dagster `
  dagster job execute `
  -f /workspace/pipelines/dagster/definitions.py `
  -j analytics_pipeline
```

Start the Dagster UI:

```powershell
docker compose --profile orchestration up -d dagster
```

Dagster UI: <http://localhost:3000>

## Downstream Use

Streamlit dashboards read from the curated DuckDB models.
