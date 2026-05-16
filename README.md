# Open Source Modern Analytics Platform

## Architecture

```mermaid
graph TD
    A[Data Sources] --> B[FastAPI Collectors]
    A --> C[Redpanda Streaming]

    B --> D[MinIO Lakehouse]
    C --> D

    D --> E[DuckDB / ClickHouse]

    E --> F[dbt Core]
    F --> G[Dagster Pipelines]

    G --> H[Streamlit Apps]
    G --> I[Apache Superset]
    G --> J[AI Analytics Assistant]

    K[Prometheus] --> L[Grafana]
```

## Repository Structure

```text
apps/
  streamlit/
  ai-assistant/
  api/
pipelines/
  dagster/
  dbt/
  ingestion/
infrastructure/
  docker/
  monitoring/
  configs/
storage/
  bronze/
  silver/
  gold/
docs/
  architecture/
  adr/
  diagrams/
```

