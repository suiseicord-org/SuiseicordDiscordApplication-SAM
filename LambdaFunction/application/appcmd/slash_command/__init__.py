#!python3.9
from application.commands import SlashCommand as SlashCommandName

from .slash_command import SlashCommand

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> SlashCommand:
    name: str = rawdata['data']['name'].split(' ')[0]
    name = name.lower()
    _log.debug("name: {0}".format(name))
    if name == SlashCommandName.send:
        _log.debug("name == SlashCommandName.send")
        from .slash_send import SlashSend
        return SlashSend(rawdata)
    elif name == SlashCommandName.user:
        _log.debug("name == SlashCommandName.user")
        from .slash_user import SlashUser
        return SlashUser(rawdata)
    elif name == SlashCommandName.thread:
        _log.debug("name == SlashCommandName.thread")
        from .thread import from_data as sct_from_data
        return sct_from_data(rawdata)
    elif name == SlashCommandName.channel:
        _log.debug("name == SlashCommandName.channel")
        from .channel import from_data as scc_from_data
        return scc_from_data(rawdata)
    elif name == SlashCommandName.ban:
        _log.debug("name == SlashCommandName.ban")
        from .slash_ban import SlashBan
        return SlashBan(rawdata)
    elif name == SlashCommandName.unixtimestamp:
        _log.debug("name == SlashCommandName.unixtimestamp")
        from .slash_unixtimestamp import SlashUnixtimestamp
        return SlashUnixtimestamp(rawdata)

    elif name == SlashCommandName.test:
        _log.debug("name == SlashCommandName.test")
        from .slash_test import SlashTest
        return SlashTest(rawdata)