#!python3.9

from application.commands import Commands as CommandsName

from .modal_submit import ModalSubmit

from .textinput import from_data as mti_from_data

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> ModalSubmit:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    command: str = _commands[0].lower()
    _log.debug("command: {}".format(command))
    if command == CommandsName.textinput:
        _log.debug("command == CommandsName.textinput")
        return mti_from_data(rawdata)