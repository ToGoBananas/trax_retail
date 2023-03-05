from apps.entities.base import BaseValidator
from core.exceptions import BadRequestException


class QASessionValidator(BaseValidator):

    MAX_REVIEWS_COUNT = 3

    def validate_create(self, username):
        if self.db_client.fetch_one(
            f'SELECT 1 FROM qa_snapshot_session WHERE username = "{username}" and remaining_snapshots_quantity > 0'
        ):
            raise BadRequestException("Session already exists")
        data = self.db_client.fetchall(f"SELECT id FROM product_snapshot LEFT JOIN qa_snapshot_session_result on qa_snapshot_session_result.snapshot_id = product_snapshot.id where qa_snapshot_session_result.session_id is null and product_snapshot.approved_count + product_snapshot.disapproved_count <{self.MAX_REVIEWS_COUNT} LIMIT 100")
        if len(data) != 100:
            raise BadRequestException("Not enough snapshots to validate")
        return [x['id'] for x in data]
