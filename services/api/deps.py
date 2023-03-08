from fastapi import Header

from core.utils import ImmutableModel


class User(ImmutableModel):
    username: str


def get_user(
    username: str = Header(),
) -> User:
    return User(username=username)
