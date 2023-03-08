from db.queries.base import QueriesBase


class QASessionQueries(QueriesBase):
    def create_session(self, username, remaining_snapshots_quantity):
        return self.db_client.execute(
            "INSERT INTO qa_snapshot_session (username, remaining_snapshots_quantity)"
            f"VALUES ('{username}', {remaining_snapshots_quantity})",
        )

    def get_current_session_id(self, username):
        session = self.db_client.fetch_one(
            f"SELECT id from qa_snapshot_session WHERE username = '{username}' and remaining_snapshots_quantity <> 0;"
        )
        if session:
            return session["id"]

    def create_session_snapshots(self, snapshots: list[dict]):
        return self.db_client.executemany(
            "INSERT INTO qa_snapshot_session_result (session_id, snapshot_id)"
            "VALUES (%(session_id)s, %(snapshot_id)s)",
            snapshots,
        )

    def get_current_session(self, username):
        q = f"""
            SELECT qa_snapshot_session.id as session_id, product.id as product_id, 
                product.name as product_name, product_snapshot.id as snapshot_id, 
                product_snapshot.filename from qa_snapshot_session 
            JOIN qa_snapshot_session_result ON qa_snapshot_session_result.session_id = qa_snapshot_session.id 
                                            and qa_snapshot_session.username = '{username}' 
            JOIN product_snapshot ON product_snapshot.id = qa_snapshot_session_result.snapshot_id 
            JOIN product ON product.id = product_snapshot.product_id 
            WHERE remaining_snapshots_quantity > 0 and qa_snapshot_session_result.is_match is NULL;
        """
        return self.db_client.fetchall(q)
