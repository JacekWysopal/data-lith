# dbt Transformations

## Goal

Introduce dbt Core transformations on top of DuckDB and formalize the first local data flow:

```text
raw.source_events -> clean.events -> curated.event_counts_by_day
```

## Layers

- `raw`: source-shaped data loaded by seeds for now and later by ingestion jobs.
- `clean`: typed, normalized, deduplicated datasets.
- `curated`: business-facing aggregates and marts for BI, dashboards, and the AI assistant.

## Commands

```powershell
docker compose --profile tools run --rm dbt seed
docker compose --profile tools run --rm dbt run
docker compose --profile tools run --rm dbt test
```

## Orchestration

Dagster orchestrates dbt runs as repeatable assets/jobs.
