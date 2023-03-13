from core.exceptions import BadRequestException
from apps.entities.base import BaseValidator


class QASessionValidator(BaseValidator):
    def validate_create(self, username, session_size: int, max_reviews):
        if self.db_client.fetch_one(
            f'SELECT 1 FROM qa_snapshot_session WHERE username = "{username}" and remaining_snapshots_quantity > 0'
        ):
            raise BadRequestException("Session already exists")
        q = f"""
            SELECT DISTINCT product_snapshot.id FROM product_snapshot
            left join qa_snapshot_session_result on qa_snapshot_session_result.snapshot_id = product_snapshot.id
            where product_snapshot.id not in (
                select distinct snapshot_id from qa_snapshot_session_result 
                join qa_snapshot_session on qa_snapshot_session.id = qa_snapshot_session_result.session_id
                where qa_snapshot_session.username = '{username}'  
            ) and product_snapshot.approved_count + product_snapshot.disapproved_count < {max_reviews}
            LIMIT {session_size};
        """  # TODO: check performance on large tables
        data = self.db_client.fetchall(q)
        if len(data) != session_size:
            raise BadRequestException("Not enough snapshots to validate")
        return [x["id"] for x in data]
