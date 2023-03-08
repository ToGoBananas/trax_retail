from pydantic import AnyUrl

from core.utils import ImmutableModel


class SnapshotForQa(ImmutableModel):
    snapshot_image_url: AnyUrl
    snapshot_id: int
    product_name: str
    product_image_url: AnyUrl
    product_id: int


class QASnapshotSessionResponse(ImmutableModel):
    remaining_snapshots_quantity: int
    snapshots: list[SnapshotForQa]
    session_id: int
