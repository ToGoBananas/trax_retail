from db.queries.base import QueriesBase


class ProductSnapshotQueries(QueriesBase):
    def create_snapshots(self, snapshots: list[dict]):
        return self.db_client.executemany(
            "INSERT INTO product_snapshot (product_id, filename) VALUES (%(product_id)s, %(filename)s)",
            snapshots,
        )
