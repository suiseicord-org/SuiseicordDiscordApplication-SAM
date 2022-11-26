#!python3.9
from application.commands import SlashCommand as SlashCommandName

from .slash_command import SlashCommand
from .slash_send import SlashSend
from .slash_user import SlashUser

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> SlashCommand:
    name: str = rawdata['data']['name'].split(' ')[0]
    name = name.lower()
    _log.debug("name: {0}".format(name))
    if name == SlashCommandName.send:
        _log.debug("name == SlashCommandName.send")
        return SlashSend(rawdata)
    elif name == SlashCommandName.user:
        _log.debug("name == SlashCommandName.user")
        return SlashUser(rawdata)