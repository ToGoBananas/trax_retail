from decimal import Decimal

from core.utils import ImmutableModel


class QALeaderBoardDBSchema(ImmutableModel):
    username: str
    activity_points: Decimal
    accuracy_points: Decimal
