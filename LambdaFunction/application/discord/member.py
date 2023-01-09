#!python3.9
import datetime
from typing import Optional
import requests
from copy import deepcopy

from application.mytypes.member import (
    PartialMember as PartialMemberPayload,
    MemberWithUser as MemberWithUserPayload
)
from application.mytypes.snowflake import Snowflake
from application.utils import parse_time
from .user import User, PartiaUser
from .role import Role

from . import ImageBaseUrl
from .http import Route

from logging import getLogger
_log = getLogger(__name__)

class BaseMember:
    def __init__(self, _id: Snowflake, guild_id: Snowflake) -> None:
        self.id: Snowflake = _id
        self.guild_id: Snowflake = guild_id
    
    def ban(self, delete_message_days: int = 1, reason: Optional[str] = None) -> requests.Response:
        kwargs = {}
        kwargs["json_payload"] = {
            "delete_message_days" : delete_message_days
        }
        kwargs["reason"] = reason
        route = Route(
            'PUT',
            f'/guilds/{self.guild_id}/bans/{self.id}',
            **kwargs
        )
        r = route.requets()
        return r

class PartiaMember(PartiaUser, BaseMember):
    def __init__(self, payload: PartialMemberPayload, guild_id: Snowflake):
        _log.debug(payload)
        PartiaUser.__init__(self, payload["user"])
        BaseMember.__init__(self, payload["user"]["id"], guild_id)
        self.joind_at: datetime.datetime = parse_time(payload["joined_at"])
        self.deaf: bool = payload.get("deaf", False)
        self.mute: bool = payload.get("mute", False)

        role_ids = set([int(i) for i in payload["roles"]])
        role_ids.add(int(guild_id))
        self._role_ids: list[int] = list(role_ids)
    
    def _update_role(self, new_roles: list[int], reason: Optional[str] = None) -> requests.Response:
        kwargs = {}
        kwargs["json_payload"] = {
            "roles" : new_roles
        }
        kwargs["reason"] = reason
        route: Route = Route(
            'PATCH',
            f'/guilds/{self.guild_id}/members/{self.id}',
            **kwargs
        )
        r = route.requets()
        if r.ok:
            self._role_ids = new_roles
        return r

    def add_role(self, role_id: int, reason: Optional[str] = None) -> requests.Response:
        _log.info("Add Role ID; {}".format(role_id))
        new_roles = deepcopy(self._role_ids)
        new_roles.append(role_id)
        _log.debug("New Role IDs: {}".format(new_roles))
        return self._update_role(
            new_roles=new_roles,
            reason=reason
        )

    def remove_role(self, role_id: int, reason: Optional[str] = None) -> requests.Response:
        _log.info("Add Role ID; {}".format(role_id))
        new_roles = deepcopy(self._role_ids)
        new_roles.remove(role_id)
        _log.debug("New Role IDs: {}".format(new_roles))
        return self._update_role(
            new_roles=new_roles,
            reason=reason
        )
    
    def update_roles(
        self,
        add_roles: list[int] = [],
        remove_roles: list[int] = [],
        reason: Optional[str] = None
    ) -> requests.Response:
        _log.info("Add Role IDs: {}".format(add_roles))
        _log.info("Remove Role IDs: {}".format(remove_roles))
        current_roles = set(self._role_ids)
        new_roles = list(current_roles.union(add_roles).difference(remove_roles))
        _log.debug("New Role IDs: {}".format(new_roles))
        return self._update_role(
            new_roles=new_roles,
            reason=reason
        )


        

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

        self.__owner: Optional[bool] = None
    
    @property
    def avatar_url(self) -> str:
        if self.guild_avatar_url is not None:
            return self.guild_avatar_url
        return super().avatar_url

    @property
    def guild_avatar_url(self) -> Optional[str]:
        if self._guild_avatar_hash:
            return ImageBaseUrl + f"guilds/{self.guild_id}/users/{self.id}/avatars/{self._guild_avatar_hash}.png?size=512"
        return None
    
    @property
    def is_owner(self) -> Optional[bool]:
        if self.__owner is None:
            route = Route('GET', f'/guilds/{self.guild_id}')
            r = route.requets()
            if r.ok:
                _data = r.json()
                _owner_id = _data['owner_id']
                if int(self.id) == int(_owner_id):
                    self.__owner = True
                else:
                    self.__owner = False
        return self.__owner
    
    @property
    def color(self) -> int:
        if len(self.roles) < 1:
            _log.info("Loadding guild roles.")
            self.set_guild_roles()
        
        for role in self.roles:
            if role.color > 0:
                return role.color
        
        return 0

    def set_guild_roles(self):
        route = Route('GET', f'/guilds/{self.guild_id}/roles')
        r = route.requets()
        if r.ok:
            self.roles: list[Role] = []
            role_dict: dict[Role] = dict()
            for r in r.json():
                role_dict[int(r["id"])] = Role(r, self.guild_id)
            for r in self._role_ids:
                self.roles.append(role_dict[r])
        self.roles.sort(reverse=True, key=lambda x:x.position)
        _log.debug(self.roles)
    
def get_member_or_user(user_id: Snowflake, guild_id: Snowflake):
    route = Route('GET', f'/guilds/{guild_id}/members/{user_id}')
    r = route.requets()
    if r.ok:
        return Member(r.json(), guild_id)
    
    if r.status_code == requests.codes.not_found:
        if r.json()["code"] == 10013:
            return None
    
    route = Route('GET', f'/users/{user_id}')
    r = route.requets()
    if r.ok:
        return User(r.json())
    
    return None
