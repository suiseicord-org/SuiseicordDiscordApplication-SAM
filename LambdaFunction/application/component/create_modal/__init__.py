#!python3.9

from .create_modal import CmpCreateModal
from .create_modal_send import CreateModalSend

from application.commands import (
    SlashCommand as SlashCommandName
)

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict, bot_token: str) -> CmpCreateModal:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    command: str  = _commands[1]
    _log.debug("command: {}".format(command))
    if command == SlashCommandName.send:
        _log.debug("command == SlashCommandName.send")
        return CreateModalSend(rawdata, bot_token)