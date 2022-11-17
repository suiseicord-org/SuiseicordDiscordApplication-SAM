#!python3.9
import datetime
from typing import (
    overload,
    Optional
)

from .mytypes.snowflake import Snowflake

DISCORD_EPOCH = 1420070400000


@overload
def parse_time(timestamp: None) -> None:
    ...

@overload
def parse_time(timestamp: str) -> datetime.datetime:
    ...

@overload
def parse_time(timestamp: Optional[str]) -> Optional[datetime.datetime]:
    ...

def parse_time(timestamp: Optional[str]) -> Optional[datetime.datetime]:
    if timestamp:
        return datetime.datetime.fromisoformat(timestamp)
    return None


def snowflake_time(id: Snowflake) -> datetime.datetime:
    """
    Parameters
    -----------
    id: :class:`Snowflake`
        The snowflake ID.

    Returns
    --------
    :class:`datetime.datetime`
        An aware datetime in UTC representing the creation time of the snowflake.
    """
    _id = int(id)
    timestamp = ((_id >> 22) + DISCORD_EPOCH) / 1000
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)

def isotimestamp(timestamp: datetime.datetime) -> str:

    if timestamp.tzinfo:
        return timestamp.astimezone(tz=datetime.timezone.utc).isoformat()
    else:
        return timestamp.replace(tzinfo=datetime.timezone.utc).isoformat()