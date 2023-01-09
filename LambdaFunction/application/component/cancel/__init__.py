#!python3.9
from application.commands import (
    SlashCommand as SlashCommandName
)

from ..component import Component

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> Component:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    if len(_commands) > 1:
        command: str  = _commands[1]
        _log.debug("command: {}".format(command))
        if command == SlashCommandName.ban:
            _log.debug("command == SlashCommandName.ban")
            from .command_cancel_ban import CmpCommandCancelBan
            return CmpCommandCancelBan(rawdata)
    from .command_cancel import CmpCommandCancel
    return CmpCommandCancel(rawdata)
