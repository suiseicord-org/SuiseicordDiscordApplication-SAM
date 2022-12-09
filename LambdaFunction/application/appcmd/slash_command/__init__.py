#!python3.9
from application.commands import SlashCommand as SlashCommandName

from .slash_command import SlashCommand
from .slash_send import SlashSend
from .slash_user import SlashUser
from .thread import from_data as sct_from_data
from .channel import from_data as scc_from_data

from .slash_test import SlashTest

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
    elif name == SlashCommandName.thread:
        _log.debug("name == SlashCommandName.thread")
        return sct_from_data(rawdata)
    elif name == SlashCommandName.channel:
        _log.debug("name == SlashCommandName.channel")
        return scc_from_data(rawdata)
    
    elif name == SlashCommandName.test:
        _log.debug("name == SlashCommandName.test")
        return SlashTest(rawdata)