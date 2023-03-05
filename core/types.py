from datetime import datetime, timezone

import pytz
from pydantic import constr
from pydantic.datetime_parse import parse_datetime


class NaiveDatetime(datetime):
    """Convert datetime timezone-aware datetime to naive datetime."""

    @classmethod
    def __get_validators__(cls):
        yield parse_datetime
        yield cls.validate_timezone

    @classmethod
    def validate_timezone(cls, value: datetime):
        if value.tzinfo is None:
            pass
        elif value.tzinfo != timezone.utc:
            value = value.astimezone(pytz.utc)
        value = value.replace(tzinfo=None)
        return value


TINYTEXT = constr(max_length=255)
