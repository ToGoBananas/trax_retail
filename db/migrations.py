from time import sleep

from core.db import SingleStoreClient
from core.s3 import S3Client
from core.settings.db import DBConfig
from db.models.product import product_snapshot_table
from db.models.product import product_table
from db.models.qa import qa_leaderboard_table
from db.models.qa import qa_snapshot_session_result_table
from db.models.qa import qa_snapshot_session_table


if __name__ == "__main__":
    S3Client().create_bucket()
    sleep(20)  # HACK do not repeat in production: wait for singlestore to set up

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
