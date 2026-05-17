# Ingestion API

FastAPI service for writing incoming JSON payloads to the raw lakehouse layer in MinIO.

## Endpoints

- `GET /health`: service health check.
- `POST /ingest/{source}`: stores a JSON payload under `lakehouse/raw/{source}/YYYY/MM/DD/{uuid}.json`.

## Example

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/ingest/demo `
  -ContentType application/json `
  -Body '{"event":"signup","user_id":123}'
```

