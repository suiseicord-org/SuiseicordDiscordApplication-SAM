#!python3.9
from .emoji import PartialEmoji

from application.mytypes.message import (
    Reaction as ReactionPayload
)

from logging import getLogger
_log = getLogger(__name__)

class Reaction:
    def __init__(self, payload: ReactionPayload) -> None:
        self.count: int = payload['count']
        self.me: bool = payload['me']
        self.emoji: PartialEmoji = PartialEmoji(payload['emoji'])
