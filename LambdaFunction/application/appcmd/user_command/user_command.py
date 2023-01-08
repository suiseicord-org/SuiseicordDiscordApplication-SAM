#!python3.9
from typing import Optional, Union

from ..application_command import ApplicationCommand

from application.discord.member import Member
from application.discord.user import User

from logging import getLogger
_log = getLogger(__name__)

class UserCommand(ApplicationCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.target_id: str = self._data['target_id']
        if 'members' in self._data['resolved']:
            member_payload = self._data['resolved']["members"][self.target_id]
            member_payload["user"] = self._data['resolved']["users"][self.target_id]
            self.target: Member = Member(member_payload, self._guild_id)
        else:
            self.target: User = User(self._data['resolved']["users"][self.target_id])
        _log.info("target type: {}".format(type(self.target)))
    
    def check(self) -> bool:
        """User Commands is always 'True'."""
        return True

    def run(self) -> None:
        super().run()
        return
    
    def response(self) -> None:
        super().response()
        return
    
    def clean(self) -> None:
        super().clean()
        return