from enum import Enum
from enum import unique

import singlestoredb as s2

from core.settings.db import DBConfig


@unique
class SingleStoreResultType(Enum):
    DICT = "dict"
    TUPLE = "tuple"
    NAMEDTUPLE = "namedtuple"


class SingleStoreClient:
    def __init__(
        self,
        db_config: DBConfig = DBConfig.get_default(),
        results_type: SingleStoreResultType = SingleStoreResultType.DICT,
    ):
        self.db_config = db_config
        self.results_type = results_type
        self._conn = None

    def connect(self):
        if self._conn is None:
            self._conn = s2.connect(**self.db_config.dict(), results_type=self.results_type.value)
        return self._conn

    def close(self):
        if self._conn and self._conn.is_connected():
            self._conn.close()
            self._conn = None

    def fetch_one(self, query: str, args=None):
        with self._conn.cursor() as cur:
            cur.execute(query, args=args)
            return cur.fetchone()

    def execute(self, query: str, args=None):
        with self._conn.cursor() as cur:
            return cur.execute(query, args=args)

    def executemany(self, query: str, data: list):
        with self._conn.cursor() as cur:
            return cur.executemany(query, data)

    def fetchall(self, query: str, **kwargs):
        with self._conn.cursor() as cur:
            cur.execute(query, kwargs)
            return cur.fetchall()
