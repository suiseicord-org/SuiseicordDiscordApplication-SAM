#!python3.9
from application.commands import SlashThreadCommand as SlashThreadCommandName

from .slash_thread import SlashThread
from .slash_thread_create import SlashThreadCreate

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> SlashThread:
    sub_command: str = rawdata['data']["options"][0]["name"]
    sub_command = sub_command.lower()
    _log.debug("sub_command: {0}".format(sub_command))
    if sub_command == SlashThreadCommandName.create:
        _log.debug("sub_command == ThreadCommandName.create")
        return SlashThreadCreate(rawdata)