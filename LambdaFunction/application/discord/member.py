#!python3.9
from typing import Optional


from application.mytypes.snowflake import Snowflake
from application.mytypes.member import MemberNoUser
from .user import User, PartiaUser

from logging import getLogger
_log = getLogger(__name__)

class PartiaMember(PartiaUser):
    def __init__(self, payload: dict):
        super().__init__(payload["user"])
        if ava := payload.get("avatar"):
            #override
            self._avatar_hash: Optional[str] = ava

class Member(User):
    def __init__(self, payload: dict):
        self.id: Snowflake = payload['id']