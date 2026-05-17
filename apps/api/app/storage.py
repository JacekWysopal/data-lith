import json
import os
import re
from datetime import datetime
from uuid import uuid4

import boto3
from botocore.exceptions import BotoCoreError, ClientError


SOURCE_NAME_PATTERN = re.compile(r"[^a-zA-Z0-9_-]+")


class StorageError(RuntimeError):
    pass


def normalize_source_name(source: str) -> str:
    normalized = SOURCE_NAME_PATTERN.sub("-", source.strip()).strip("-").lower()
    return normalized or "unknown"


class MinioRawStorage:
    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        raw_prefix: str,
    ) -> None:
        self.bucket = bucket
        self.raw_prefix = raw_prefix.strip("/")
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="us-east-1",
        )

    @classmethod
    def from_env(cls) -> "MinioRawStorage":
        return cls(
            endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
            access_key=os.getenv("MINIO_ROOT_USER", "minioadmin"),
            secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123"),
            bucket=os.getenv("LAKEHOUSE_BUCKET", "lakehouse"),
            raw_prefix=os.getenv("RAW_PREFIX", "raw"),
        )

    def write_json(
        self,
        source: str,
        received_at: datetime,
        payload: dict,
    ) -> str:
        key = self._build_key(source, received_at)
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode(
            "utf-8"
        )

        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=body,
                ContentType="application/json",
            )
        except (BotoCoreError, ClientError) as exc:
            raise StorageError(f"Could not write object to MinIO: {exc}") from exc

        return key

    def _build_key(self, source: str, received_at: datetime) -> str:
        date_path = received_at.strftime("%Y/%m/%d")
        return f"{self.raw_prefix}/{source}/{date_path}/{uuid4()}.json"

