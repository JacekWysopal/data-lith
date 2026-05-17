# Ingestion API

## Goal

Create a small FastAPI service that accepts JSON payloads and writes them to the raw lakehouse layer in MinIO.

## Flow

```text
Client -> FastAPI /ingest/{source} -> MinIO lakehouse/raw/{source}/YYYY/MM/DD/{uuid}.json
```

## Raw Payload Envelope

Each ingested object is stored as JSON with a small metadata envelope:

```json
{
  "source": "demo",
  "received_at": "2026-05-17T18:00:00+00:00",
  "payload": {
    "event": "signup"
  }
}
```

## Downstream Use

The dbt layer can read from `raw/` and produce typed, normalized tables in `clean/`.
