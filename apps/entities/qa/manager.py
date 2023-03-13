from contextlib import nullcontext

from apps.entities.product.manager import ProductManager
from apps.entities.product.manager import ProductSnapshotManager
from apps.entities.qa.schemas.leaderboard import QALeaderBoardDBSchema
from apps.entities.qa.schemas.session import QASnapshotSessionResponse
from apps.entities.qa.schemas.session import SnapshotForQa
from apps.entities.qa.validators import QASessionValidator
from core.exceptions import ConflictException
from core.exceptions import NotFoundException
from core.redis import RedisLockClient
from apps.entities.base import BaseManager
from db.queries.qa.leaderboard import QALeaderboardQueries
from db.queries.qa.session import QASessionQueries
from db.queries.qa.session_result import QASessionResultQueries


class _SessionLockMixin:
    def _get_lock(self, username: str):
        return RedisLockClient.get(f"qa_session:{username}")


class QASessionManager(BaseManager, _SessionLockMixin):
    SESSION_SNAPSHOTS_SIZE = 100
    MAX_REVIEWS_COUNT = 3
    validator = QASessionValidator()
    queries: QASessionQueries = QASessionQueries

    def create(self, username: str):
        with self._get_lock(username):
            snapshots_ids = self.validator.validate_create(
                username, self.SESSION_SNAPSHOTS_SIZE, self.MAX_REVIEWS_COUNT
            )
            # TODO: add transaction
            self.queries.create_session(username, self.SESSION_SNAPSHOTS_SIZE)
            session_id = self.queries.get_current_session_id(username)
            self.queries.create_session_snapshots(
                [{"session_id": session_id, "snapshot_id": snapshot_id} for snapshot_id in snapshots_ids]
            )
            return self.retrieve(username, is_has_lock=True)  # TODO: (remove redundant queries to the database)

    def retrieve(self, username: str, is_has_lock: bool = False) -> QASnapshotSessionResponse:
        with self._get_lock(username) if not is_has_lock else nullcontext():
            data = self.queries.get_current_session(username)
            if not data:
                raise NotFoundException()
            snapshots = self._prepare_snapshots_session_data(data)
            return QASnapshotSessionResponse(
                remaining_snapshots_quantity=len(snapshots), session_id=data[0]["session_id"], snapshots=snapshots
            )

    @classmethod
    def _prepare_snapshots_session_data(cls, data):
        snapshots = []
        for snapshot in data:
            snapshots.append(
                SnapshotForQa(
                    snapshot_id=snapshot["snapshot_id"],
                    snapshot_image_url=ProductSnapshotManager.build_snapshot_image_url(
                        snapshot["product_id"], snapshot["filename"]
                    ),
                    product_name=snapshot["product_name"],
                    product_image_url=ProductManager.build_product_image_url(snapshot["product_id"]),
                    product_id=snapshot["product_id"],
                )
            )
        return snapshots


class QASessionResultManager(BaseManager, _SessionLockMixin):
    queries: QASessionResultQueries = QASessionResultQueries

    def update(self, username: str, session_id: int, snapshot_id: int, is_match: bool):
        with self._get_lock(username):
            result = self.queries.get_session_result(username, session_id, snapshot_id)
            if not result:
                raise NotFoundException()
            if result["is_match"] is not None:
                raise ConflictException()
            # TODO: add transaction
            self.queries.set_is_match(session_id, snapshot_id, is_match)
            self.queries.decrease_remaining_snapshots_quantity(session_id)
            self.queries.update_product(is_match, snapshot_id)

            remaining_snapshots_quantity = result["remaining_snapshots_quantity"] - 1
            if remaining_snapshots_quantity == 0:
                QALeaderBoardManager().update_leaderboard(username)  # TODO: execute asynchronously
            return remaining_snapshots_quantity


class QALeaderBoardManager(BaseManager):
    POINTS_FOR_ACCURACY = 0.1
    POINTS_PER_SESSION = 10
    queries: QALeaderboardQueries = QALeaderboardQueries

    def _get_lock(self):
        return RedisLockClient.get(f"leaderboard")

    def update_leaderboard(self, username: str):  # should be improved to calculate all users data
        with self._get_lock():
            matches = self.queries.get_accuracy_matches(username, QASessionManager.MAX_REVIEWS_COUNT)
            if matches is not None:
                points_for_accuracy = int(matches) * self.POINTS_FOR_ACCURACY
                points_for_activity = self.queries.get_finished_sessions_count(username) * self.POINTS_PER_SESSION
                self.queries.update_leaderboard(username, points_for_activity, points_for_accuracy)

    def retrieve(self):
        results = self.queries.get_leaderboard()
        return [QALeaderBoardDBSchema(**result) for result in results]
