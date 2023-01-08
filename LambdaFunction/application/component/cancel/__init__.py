#!python3.9
from ..component import Component
from .command_cancel import CmpCommandCancel
from .command_cancel_ban import CmpCommandCancelBan

from application.commands import (
    SlashCommand as SlashCommandName
)

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> Component:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    if len(_commands) > 1:
        command: str  = _commands[1]
        _log.debug("command: {}".format(command))
        if command == SlashCommandName.ban:
            _log.debug("command == SlashCommandName.ban")
            return CmpCommandCancelBan(rawdata)
    return CmpCommandCancel(rawdata)