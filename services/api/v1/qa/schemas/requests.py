from core.utils import ImmutableModel


class QASnapshotResultSchema(ImmutableModel):
    is_match: bool
