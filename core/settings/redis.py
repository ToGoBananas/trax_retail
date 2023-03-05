import os

from core.utils import ImmutableModel


class RedisConfig(ImmutableModel):
    host: str = os.getenv("REDIS_HOST", "localhost")
    db: int = os.getenv("REDIS_DB", 1)
    port: int = os.getenv("DB_PORT", 6380)

    @classmethod
    def get_default(cls):
        return RedisConfig()
