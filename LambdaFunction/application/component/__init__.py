#!python3.9

from application.commands import (
    Commands as CommandsName
)

from .component import Component
from .command_cancel import CmpCommandCancel
from .start_command import from_data as csc_from_data
from .create_modal import from_data as ccm_from_data
from .suiseicord_happi import from_data as csh_from_data

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict, bot_token: str) -> Component:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    command: str = _commands[0].lower()
    _log.debug("command: {}".format(command))
    if command == CommandsName.cancel:
        _log.debug("command == CommandsName.cancel")
        return CmpCommandCancel(rawdata, bot_token)
    elif command == CommandsName.start:
        _log.debug("command == CommandsName.start")
        return csc_from_data(rawdata, bot_token)
    elif command == CommandsName.modal:
        _log.debug("command == CommandsName.modal")
        return ccm_from_data(rawdata, bot_token)
    # elif command == CommandsName.happi:
    #     _log.debug("command == CommandsName.happi")
    #     return csh_from_data(rawdata, bot_token)