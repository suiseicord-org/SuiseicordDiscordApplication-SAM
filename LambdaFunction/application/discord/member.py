#!python3.9
import datetime
from typing import Optional

from application.mytypes.member import (
    PartialMember as PartialMemberPayload,
    MemberWithUser as MemberWithUserPayload
)
from application.mytypes.snowflake import Snowflake
from application.mytypes.user import (
    User as UserPayload
)
from application.utils import parse_time
from .user import User, PartiaUser

from . import ImageBaseUrl

from logging import getLogger
_log = getLogger(__name__)

class PartiaMember(PartiaUser):
    def __init__(self, payload: PartialMemberPayload):
        super().__init__(payload["user"])
        self._role_ids: list[Snowflake] = payload["roles"]
        self.joind_at: datetime.datetime = parse_time(payload["joined_at"])
        self.deaf: bool = payload["deaf"]
        self.mute: bool = payload["mute"]

class Member(PartiaMember, User):
    def __init__(
        self, 
        payload: MemberWithUserPayload, 
        guild_id: Snowflake,
        *,
        user: Optional[UserPayload] = None
    ):
        User.__init__(self, payload["user"])
        PartiaMember.__init__(self, payload)

        self._guild_avatar_hash: Optional[str] = payload.get("avatar")
        self.nick: Optional[str] = payload.get("nick")
        self.premium_since: Optional[datetime.datetime] = parse_time(payload.get("premium_since"))
        self.pending: Optional[bool] = payload.get("pending")
        self.permissions: Optional[str] = payload.get("permissions")

        self.guild_id: Snowflake = guild_id
    
    @property
    def avatar_url(self) -> str:
        if self._guild_avatar_hash:
            return ImageBaseUrl + f"guilds/{self.guild_id}/users/{self.id}/avatars/{self._avatar_hash}.png"
        return super().avatar_url