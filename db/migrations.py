from core.s3 import S3Client
from core.settings.db import DBConfig
from core.db import SingleStoreClient
from db.models.product import product_table, product_snapshot_table
from db.models.qa import (
    qa_snapshot_session_result_table,
    qa_snapshot_session_table,
    qa_leaderboard_table,
)

S3Client().create_bucket()

client = SingleStoreClient(DBConfig(database=None))
client.connect()
client.execute(f"CREATE DATABASE {DBConfig().database};")
client.close()

client = SingleStoreClient()
client.connect()
client.execute(product_table)
client.execute(product_snapshot_table)
client.execute(qa_snapshot_session_result_table)
client.execute(qa_snapshot_session_table)
client.execute(qa_leaderboard_table)
client.close()
