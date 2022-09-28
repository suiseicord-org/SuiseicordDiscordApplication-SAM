#!python3.9

from .start_command import CmpStartCommand
from .start_send import CmpStartSend

from application.commands import (
    SlashCommand as SlashCommandName
)

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict, bot_token: str) -> CmpStartCommand:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    #start-command-
    command: str = _commands[1]
    _log.debug("command: {}".format(command))
    if command == SlashCommandName.send:
        _log.debug("command == SlashCommandName.send")
        return CmpStartSend(rawdata, bot_token)