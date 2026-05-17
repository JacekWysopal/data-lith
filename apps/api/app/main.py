from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel

from app.storage import MinioRawStorage, StorageError, normalize_source_name


app = FastAPI(
    title="Data Lith Ingestion API",
    version="0.1.0",
    description="Accepts source payloads and stores them in the raw lakehouse layer.",
)
storage = MinioRawStorage.from_env()


class IngestResponse(BaseModel):
    bucket: str
    key: str
    source: str
    received_at: datetime


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/ingest/{source}",
    response_model=IngestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ingest(source: str, request: Request) -> IngestResponse:
    try:
        payload: Any = await request.json()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must be valid JSON.",
        ) from exc

    received_at = datetime.now(UTC)
    normalized_source = normalize_source_name(source)
    envelope = {
        "source": normalized_source,
        "received_at": received_at.isoformat(),
        "payload": payload,
    }

    try:
        key = storage.write_json(normalized_source, received_at, envelope)
    except StorageError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return IngestResponse(
        bucket=storage.bucket,
        key=key,
        source=normalized_source,
        received_at=received_at,
    )

