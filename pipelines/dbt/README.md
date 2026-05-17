# dbt Transformations

This dbt project transforms local DuckDB data through the platform layers:

```text
raw -> clean -> curated
```

## Commands

From the repository root:

```powershell
docker compose --profile tools run --rm dbt seed
docker compose --profile tools run --rm dbt run
docker compose --profile tools run --rm dbt test
```

## Models

- `raw.source_events`: seeded sample source data.
- `clean.events`: typed and normalized event rows.
- `curated.event_counts_by_day`: daily event counts by event name.

