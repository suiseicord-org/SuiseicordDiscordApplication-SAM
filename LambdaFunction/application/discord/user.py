#!python3.9
from typing import Optional
import datetime

from application.utils import snowflake_time

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
        _log.debug(payload)
        self.id: Snowflake = payload["id"]
        self.name: str = payload["username"]
        self.discriminator: str = payload["discriminator"]
        self._avatar_hash: Optional[str] = payload.get("avatar")
    
    def __str__(self) -> str:
        return f"{self.name}#{self.discriminator}"

    @property
    def avatar_url(self) -> str:
        return ImageBaseUrl + f"avatars/{self.id}/{self._avatar_hash}.png"
    
    @property
    def created_at(self) -> datetime.datetime:
        return snowflake_time(self.id)

class User(PartiaUser):
    def __init__(self, payload: UserPayload):
        _log.debug(payload)
        super().__init__(payload)
        self.bot: Optional[bool] = payload.get("bot")
        self.system: Optional[bool] = payload.get("system")
        self.mfa_enabled: Optional[bool] = payload.get("mfa_enabled")
        self.local: Optional[str] = payload.get("local")
        self.verified: Optional[bool] = payload.get("verified")
        self.email: Optional[str] = payload.get("email")
        self.flags: Optional[int] = payload.get("flags")
        self.premium_type: Optional[int] = payload.get("premium_type")
        self.public_flags: Optional[int] = payload.get("public_flags")
