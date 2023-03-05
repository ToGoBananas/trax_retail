import os

from core.utils import ImmutableModel


class S3Config(ImmutableModel):
    host: str = os.getenv("MINIO_HOST", "localhost")
    access_key: str = os.getenv("MINIO_ACCESS_KEY", "root")
    secret_key: str = os.getenv("MINIO_SECRET_KEY", "password")
    port: int = os.getenv("MINIO_PORT", 9000)
    bucket_name: str = os.getenv("MINIO_BUCKET", "trax-retail")

    @classmethod
    def get_default(cls):
        return S3Config()
