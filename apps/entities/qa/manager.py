from apps.entities.base import BaseManager
from apps.entities.qa.schemas.session import QASnapshotSessionCreateSchema, QASnapshotSessionResponse
from apps.entities.qa.validators import QASessionValidator
from core.exceptions import NotFoundException
from core.redis import RedisLockClient


class QASessionManager(BaseManager):
    validator = QASessionValidator()

    def create(self, entity: QASnapshotSessionCreateSchema):
        with RedisLockClient.get(f"qa_session:{entity.username}"):
            snapshots_ids = self.validator.validate_create(entity.username)
            # TODO: add transaction
            session_id = self.db_client.executemany(
                'INSERT INTO qa_snapshot_session (username, remaining_snapshots_quantity) VALUES (%(username)s, %(remaining_snapshots_quantity)s)',
                [entity.dict()]
            )
            self.db_client.executemany(
                'INSERT INTO qa_snapshot_session_result (session_id, snapshot_id) VALUES (%(session_id)s, %(snapshot_id)s)',
                [{"session_id": session_id, "snapshot_id": snapshot_id} for snapshot_id in snapshots_ids]
            )
        return QASnapshotSessionResponse(session_id=session_id, remaining_snapshots_quantity=entity.remaining_snapshots_quantity)

    def retrieve(self, username):
        session = self.db_client.execute(f"SELECT session_id, remaining_snapshots_quantity WHERE username = '{username}")
        if not session:
            raise NotFoundException()
        return QASnapshotSessionResponse(**session)


class QASessionSnapshotManager(BaseManager):

    def retrieve(self, session_id):
        pass
