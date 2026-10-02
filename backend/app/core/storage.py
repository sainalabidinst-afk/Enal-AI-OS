"""
MinIO Object Storage Service.

Provides S3-compatible object storage operations using MinIO.
Used for artifact storage, workspace files, and large binary objects.

ADR-003: This is a thin adapter — delegates to MinIO SDK.
ADR-004: Business logic (bucket policies, lifecycle) resides in domain services.
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Any

from minio import Minio
from minio.error import S3Error
from starlette.concurrency import run_in_threadpool

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class StorageError(Exception):
    """Raised when a storage operation fails."""


class MinioStorage:
    """
    MinIO-backed object storage service.

    Public API::

        storage = MinioStorage()
        storage.ensure_bucket("artifacts")
        storage.put("artifacts", "report.pdf", file_bytes)
        data = storage.get("artifacts", "report.pdf")
        storage.delete("artifacts", "report.pdf")
    """

    def __init__(self) -> None:
        self._client: Minio | None = None
        self._endpoint = settings.MINIO_ENDPOINT
        self._access_key = settings.MINIO_ACCESS_KEY
        self._secret_key = settings.MINIO_SECRET_KEY
        self._secure = settings.MINIO_SECURE
        self._default_bucket = settings.MINIO_BUCKET

    @property
    def client(self) -> Minio:
        if self._client is None:
            if not self._access_key or not self._secret_key:
                raise StorageError("MinIO credentials not configured")
            self._client = Minio(
                self._endpoint,
                access_key=self._access_key,
                secret_key=self._secret_key,
                secure=self._secure,
            )
        return self._client

    def ensure_bucket(self, bucket_name: str | None = None) -> str:
        """Create bucket if it does not exist. Returns bucket name."""
        bucket = bucket_name or self._default_bucket
        try:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)
                logger.info(f"Created bucket: {bucket}")
        except S3Error as e:
            raise StorageError(f"Failed to ensure bucket '{bucket}': {e}") from e
        return bucket

    async def put_object(
        self,
        bucket: str,
        object_name: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Upload bytes to object storage. Returns the object path."""
        try:
            from io import BytesIO

            stream = BytesIO(data)
            await run_in_threadpool(
                self.client.put_object,
                bucket,
                object_name,
                stream,
                length=len(data),
                content_type=content_type,
            )
            return f"{bucket}/{object_name}"
        except S3Error as e:
            raise StorageError(f"Failed to put object '{object_name}': {e}") from e

    async def get_object(self, bucket: str, object_name: str) -> bytes:
        """Download an object as bytes."""
        try:
            response = await run_in_threadpool(self.client.get_object, bucket, object_name)
            try:
                return response.read()
            finally:
                response.close()
                response.release_conn()
        except S3Error as e:
            raise StorageError(f"Failed to get object '{object_name}': {e}") from e

    async def delete_object(self, bucket: str, object_name: str) -> None:
        """Delete an object from storage."""
        try:
            await run_in_threadpool(self.client.remove_object, bucket, object_name)
        except S3Error as e:
            raise StorageError(f"Failed to delete object '{object_name}': {e}") from e

    async def list_objects(self, bucket: str, prefix: str = "") -> list[dict[str, Any]]:
        """List objects in a bucket with optional prefix."""
        try:
            objects = await run_in_threadpool(
                lambda: list(self.client.list_objects(bucket, prefix=prefix, recursive=True))
            )
            return [
                {
                    "name": o.object_name,
                    "size": o.size,
                    "etag": o.etag,
                    "last_modified": o.last_modified.isoformat() if o.last_modified else None,
                }
                for o in objects
            ]
        except S3Error as e:
            raise StorageError(f"Failed to list objects in '{bucket}': {e}") from e

    async def upload_file(self, bucket: str, object_name: str, file_path: str) -> str:
        """Upload a local file to object storage."""
        try:
            path = Path(file_path)
            if not path.exists():
                raise StorageError(f"Local file not found: {file_path}")
            await run_in_threadpool(
                self.client.fput_object,
                bucket,
                object_name,
                file_path,
            )
            return f"{bucket}/{object_name}"
        except S3Error as e:
            raise StorageError(f"Failed to upload file '{file_path}': {e}") from e

    async def download_file(self, bucket: str, object_name: str, dest_path: str) -> str:
        """Download an object from storage to a local file."""
        try:
            await run_in_threadpool(
                self.client.fget_object,
                bucket,
                object_name,
                dest_path,
            )
            return dest_path
        except S3Error as e:
            raise StorageError(f"Failed to download object '{object_name}': {e}") from e

    def get_presigned_url(self, bucket: str, object_name: str, expires: int = 3600) -> str:
        """Generate a presigned URL for downloading an object."""
        try:
            return self.client.presigned_get_object(bucket, object_name, expires=expires)
        except S3Error as e:
            raise StorageError(f"Failed to generate presigned URL: {e}") from e


storage = MinioStorage()
