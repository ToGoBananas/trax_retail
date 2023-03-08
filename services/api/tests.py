from multiprocessing.pool import ThreadPool

from starlette import status

from apps.entities.qa.manager import BaseManager
from apps.entities.qa.schemas.session import QASnapshotSessionResponse
from services.api.main import app
from services.api.v1.qa.schemas.requests import QASnapshotResultSchema


def _create_session_and_approve_all(client, username):
    response = client.post(app.url_path_for("authorized_qa_session_create"), headers={"username": username})
    assert response.status_code == status.HTTP_201_CREATED
    response = response.json()
    response = QASnapshotSessionResponse(**response)
    session_id = response.session_id
    for snapshot_data in response.snapshots:
        response = client.patch(
            app.url_path_for(
                "authorized_qa_snapshot_update",
                session_id=session_id,
                snapshot_id=snapshot_data.snapshot_id,
            ),
            json=QASnapshotResultSchema(is_match=True).dict(),
            headers={"username": username},
        )
        assert response.status_code == status.HTTP_200_OK


def test_quick(client):
    BaseManager.db_client.connect()
    users = ["test1", "test2", "test3"]

    with ThreadPool(processes=3) as pool:
        result = pool.starmap_async(_create_session_and_approve_all, [(client, username) for username in users])
        result.wait()

    _create_session_and_approve_all(client, users[0])
    response = client.post(app.url_path_for("authorized_qa_session_create"), headers={"username": users[0]})
    assert response.status_code == status.HTTP_400_BAD_REQUEST  # not enough snapshots

    response = client.get(app.url_path_for("authorized_qa_leaderboard_retrieve"), headers={"username": users[0]})
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response
    assert response[0]["activity_points"]
    assert response[0]["accuracy_points"]
