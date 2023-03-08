from core.db import SingleStoreClient
from core.s3 import S3Client
from db.queries.base import QueriesBase


class BaseManager:
    db_client = SingleStoreClient()
    s3_client = S3Client()
    queries = QueriesBase

    def __init__(self):
        self.queries = self.queries(self.db_client)


class BaseValidator(BaseManager):
    pass
