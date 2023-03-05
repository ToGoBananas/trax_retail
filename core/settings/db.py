import os

from core.utils import ImmutableModel


class DBConfig(ImmutableModel):
    host: str = os.getenv("DB_HOST", "localhost")
    password: str = os.getenv("DB_PASSWORD", "password")
    user: str = os.getenv("DB_USER", "root")
    database: str | None = os.getenv("DB_NAME", "trax_retail")
    port: int = os.getenv("DB_PORT", 3306)

    @classmethod
    def get_default(cls):
        return DBConfig()
