from core.db import SingleStoreClient
from core.s3 import S3Client

db_client = SingleStoreClient()
db_client.connect()


class BaseManager:
    db_client = db_client
    s3_client = S3Client()


class BaseValidator(BaseManager):
    pass