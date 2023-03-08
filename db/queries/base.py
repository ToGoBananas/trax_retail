from core.db import SingleStoreClient


class QueriesBase:
    def __init__(self, db_client: SingleStoreClient):
        self.db_client = db_client
