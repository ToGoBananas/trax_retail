from db.queries.base import QueriesBase


class QASessionResultQueries(QueriesBase):
    def get_session_result(self, username, session_id, snapshot_id):
        return self.db_client.fetch_one(
            f"SELECT is_match, remaining_snapshots_quantity FROM qa_snapshot_session_result "
            f"JOIN qa_snapshot_session ON qa_snapshot_session.id = qa_snapshot_session_result.session_id "
            f'WHERE qa_snapshot_session.username = "{username}" '
            f"and qa_snapshot_session_result.session_id = {session_id} "
            f"and qa_snapshot_session_result.snapshot_id = {snapshot_id};"
        )

    def set_is_match(self, session_id, snapshot_id, is_match: bool):
        return self.db_client.execute(
            f"UPDATE qa_snapshot_session_result "
            f"SET is_match = {is_match} "
            f"WHERE session_id = {session_id} and snapshot_id = {snapshot_id};"
        )

    def decrease_remaining_snapshots_quantity(self, session_id):
        return self.db_client.execute(
            f"UPDATE qa_snapshot_session "
            f"SET remaining_snapshots_quantity = remaining_snapshots_quantity - 1 "
            f"WHERE id = {session_id}"
        )

    def update_product(self, is_match: bool, snapshot_id):
        if is_match:
            self.db_client.execute(
                f"UPDATE product_snapshot SET approved_count = approved_count + 1 WHERE id = {snapshot_id}"
            )
        else:
            self.db_client.execute(
                f"UPDATE product_snapshot SET disapproved_count = disapproved_count + 1 WHERE id = {snapshot_id}"
            )
