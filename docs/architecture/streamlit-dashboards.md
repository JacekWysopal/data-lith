# Streamlit Dashboards

## Goal

Provide a lightweight BI surface for curated DuckDB models.

## Data Source

The dashboard reads from:

```text
curated.event_counts_by_day
```

## Command

```powershell
docker compose --profile dashboards up -d streamlit
```

Streamlit UI: <http://localhost:8501>

