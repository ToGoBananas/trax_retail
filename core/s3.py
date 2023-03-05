import json
import os
import uuid
from datetime import datetime

import orjson
from minio import Minio

from core.settings.s3 import S3Config


class S3Client:
    def __init__(self, config: S3Config = S3Config.get_default()):
        self.config = config
        self.client = Minio(
            f"{self.config.host}:{self.config.port}",
            access_key=self.config.access_key,
            secret_key=self.config.secret_key,
            secure=False,
        )

    def create_bucket(self, bucket_name: str | None = None, is_check_exists=True):
        bucket_name = bucket_name or self.config.bucket_name
        if is_check_exists and self.client.bucket_exists(bucket_name):
            return
        self.client.make_bucket(bucket_name)
        self.client.set_bucket_policy(bucket_name, self._get_public_policy(bucket_name))

    def put_object(self, file_path, save_dir=None, bucket_name=None, content_type=None):
        bucket_name = bucket_name or self.config.bucket_name
        filename = file_path.split("/")[-1]
        if save_dir:
            filename = os.path.join(save_dir, filename)
        return self.client.fput_object(
            bucket_name,
            filename,
            file_path,
            content_type=content_type
        )

    @classmethod
    def _get_public_policy(cls, bucket_name):
        return orjson.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                    "Resource": f"arn:aws:s3:::{bucket_name}",
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                },
            ],
        })