#!python3.9
from typing import Optional

from application.mytypes.snowflake import Snowflake
from application.mytypes.emoji import (
    PartialEmoji as PartialEmojiPayload
)

from logging import getLogger
_log = getLogger(__name__)

class PartialEmoji:
    def __init__(self, payload: PartialEmojiPayload) -> None:
        self.id: Optional[Snowflake] = payload['id']
        self.name: Optional[str]     = payload['name']
        self.animated: bool          = payload.get('animated', False)
    
    def __str__(self) -> str:
        if self.id is None:
            return self.name
        return '<{animated}:{name}:{id}>'.format(
            animated = 'a' if self.animated else '',
            name = self.name,
            id = self.id
        )
