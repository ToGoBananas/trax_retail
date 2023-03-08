from fastapi import Depends
from starlette import status

from apps.entities.qa.manager import QALeaderBoardManager
from apps.entities.qa.manager import QASessionManager
from apps.entities.qa.manager import QASessionResultManager
from apps.entities.qa.schemas.leaderboard import QALeaderBoardDBSchema
from apps.entities.qa.schemas.session import QASnapshotSessionResponse
from services.api import deps
from services.api.deps import User
from services.api.utils import get_router
from services.api.v1.qa.schemas.requests import QASnapshotResultSchema
from services.api.v1.qa.schemas.responses import QASnapshotResultResponseSchema

router = get_router()


@router.post(
    path="/session",
    operation_id="authorized_qa_session_create",
    response_model=QASnapshotSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def authorized_qa_session_create(
    user: User = Depends(deps.get_user),
):
    return QASessionManager().create(user.username)


@router.get(
    path="/session",
    operation_id="authorized_qa_session_retrieve",
    response_model=QASnapshotSessionResponse,
    status_code=status.HTTP_200_OK,
)
def authorized_qa_session_retrieve(
    user: User = Depends(deps.get_user),
):
    return QASessionManager().retrieve(user.username)


@router.patch(
    path="/session/{session_id}/snapshot/{snapshot_id}",
    operation_id="authorized_qa_snapshot_update",
    response_model=QASnapshotResultResponseSchema,
    status_code=status.HTTP_200_OK,
)
def authorized_qa_snapshot_update(
    session_id: int,
    snapshot_id: int,
    body: QASnapshotResultSchema,
    user: User = Depends(deps.get_user),
):
    return QASnapshotResultResponseSchema(
        remaining_snapshots_quantity=QASessionResultManager().update(
            user.username, session_id, snapshot_id, body.is_match
        )
    )


@router.get(
    path="/leaderboard",
    operation_id="authorized_qa_leaderboard_retrieve",
    response_model=list[QALeaderBoardDBSchema],
    status_code=status.HTTP_200_OK,
)
def authorized_qa_leaderboard_retrieve():
    return QALeaderBoardManager().retrieve()
