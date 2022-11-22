#!python3.9
import datetime
from typing import Optional, Union
import requests

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
from .role import Role

from . import ApiBaseUrl, ImageBaseUrl

from logging import getLogger
_log = getLogger(__name__)

class PartiaMember(PartiaUser):
    def __init__(self, payload: PartialMemberPayload, guild_id: Snowflake):
        _log.debug(payload)
        super().__init__(payload["user"])
        self.joind_at: datetime.datetime = parse_time(payload["joined_at"])
        self.deaf: bool = payload.get("deaf", False)
        self.mute: bool = payload.get("mute", False)

        self.guild_id: Snowflake = guild_id

        role_ids = set([int(i) for i in payload["roles"]])
        role_ids.add(int(guild_id))
        self._role_ids: list[int] = list(role_ids)

class Member(PartiaMember, User):
    def __init__(
        self, 
        payload: MemberWithUserPayload, 
        guild_id: Snowflake
    ):
        _log.debug(payload)
        User.__init__(self, payload["user"])
        PartiaMember.__init__(self, payload, guild_id)

        self._guild_avatar_hash: Optional[str] = payload.get("avatar")
        self.nick: Optional[str] = payload.get("nick")
        self.premium_since: Optional[datetime.datetime] = parse_time(payload.get("premium_since"))
        self.pending: Optional[bool] = payload.get("pending")
        self.permissions: Optional[str] = payload.get("permissions")

        self.roles: list[Role] = []
    
    @property
    def avatar_url(self) -> str:
        if self._guild_avatar_hash:
            return ImageBaseUrl + f"guilds/{self.guild_id}/users/{self.id}/avatars/{self._guild_avatar_hash}.png"
        return super().avatar_url
    
    def set_guild_roles(self, headers: dict):
        url = ApiBaseUrl + f'/guilds/{self.guild_id}/roles'
        r: requests.Response = requests.get(
            url,
            headers = headers
        )
        _log.debug("status code: {}".format(r.status_code))
        _log.debug("response: {}".format(r.text))
        if r.ok:
            self.roles: list[Role] = []
            role_dict: dict[Role] = dict()
            for r in r.json():
                role_dict[int(r["id"])] = Role(r, self.guild_id)
            for r in self._role_ids:
                self.roles.append(role_dict[r])
        self.roles.sort(reverse=True, key=lambda x:x.position)
        _log.debug(self.roles)
    
def get_member_or_user(user_id: Snowflake, guild_id: Snowflake, headers: dict):
    url = ApiBaseUrl + f'/guilds/{guild_id}/members/{user_id}'
    r: requests.Response = requests.get(
        url,
        headers = headers
    )
    _log.debug("status code: {}".format(r.status_code))
    _log.debug("response: {}".format(r.text))
    if r.ok:
        return Member(r.json(), guild_id)
    
    if r.status_code == requests.codes.not_found:
        if r.json()["code"] == 10013:
            return None
    
    url = ApiBaseUrl + f'/users/{user_id}'
    r: requests.Response = requests.get(
        url,
        headers = headers
    )
    _log.debug("status code: {}".format(r.status_code))
    _log.debug("response: {}".format(r.text))
    if r.ok:
        return User(r.json())
    
    return None
