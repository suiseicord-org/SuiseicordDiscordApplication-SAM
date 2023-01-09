#!python3.9
from application.commands import UserCommand as UserCommandName

from .user_command import UserCommand

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> UserCommand:
    name: str = rawdata['data']['name']
    name = name.lower()
    _log.debug("name: {0}".format(name))
    if name == UserCommandName.info:
        _log.debug('name == UserCommandName.info')
        from .user_info import UserInfo
        return UserInfo(rawdata)
