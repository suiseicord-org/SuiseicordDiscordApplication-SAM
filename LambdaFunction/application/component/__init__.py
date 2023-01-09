#!python3.9
from application.commands import (
    Commands as CommandsName
)

from .component import Component

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> Component:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    command: str = _commands[0].lower()
    _log.debug("command: {}".format(command))
    if command == CommandsName.cancel:
        _log.debug("command == CommandsName.cancel")
        from .cancel import from_data as cc_from_data
        return cc_from_data(rawdata)
    elif command == CommandsName.start:
        _log.debug("command == CommandsName.start")
        from .start_command import from_data as csc_from_data
        return csc_from_data(rawdata)
    elif command == CommandsName.modal:
        _log.debug("command == CommandsName.modal")
        from .create_modal import from_data as ccm_from_data
        return ccm_from_data(rawdata)
    elif command == CommandsName.form:
        _log.debug(command == CommandsName.form)
        from .form import from_data as cf_from_data
        return cf_from_data(rawdata)
    elif command == CommandsName.role:
        _log.debug("command == CommandsName.role")
        from .role import from_data as cr_from_data
        return cr_from_data(rawdata)
    # elif command == CommandsName.happi:
    #     _log.debug("command == CommandsName.happi")
    #     from .suiseicord_happi import from_data as csh_from_data
    #     return csh_from_data(rawdata)
