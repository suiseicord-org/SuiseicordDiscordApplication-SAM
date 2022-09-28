#!python3.9
from typing import Optional

from application.mytypes.snowflake import Snowflake
from application.mytypes.user import (
    User as UserPayload,
    PartialUser as PartiaUserPayload
)

from . import ImageBaseUrl

from logging import getLogger
_log = getLogger(__name__)

class PartiaUser:
    def __init__(self, payload: PartiaUserPayload):
        self.id: Snowflake = payload["id"]
        self.name: str = payload["username"]
        self.discriminator: str = payload["discriminator"]
        self._avatar_hash: Optional[str] = payload.get("avatar")
    
    def __str__(self) -> str:
        return f"{self.name}#{self.discriminator}"

    @property
    def avatar_url(self) -> str:
        return ImageBaseUrl + f"avatars/{self.id}/{self._avatar_hash}.png"

class User(PartiaUser):
    def __init__(self, payload: UserPayload):
        super().__init__(payload)

