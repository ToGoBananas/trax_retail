from core.utils import ImmutableModel


class QASnapshotSessionCreateSchema(ImmutableModel):
    remaining_snapshots_quantity: int = 100
    username: str


class QASnapshotSessionResponse(ImmutableModel):
    remaining_snapshots_quantity: int = 100
    session_id: int

