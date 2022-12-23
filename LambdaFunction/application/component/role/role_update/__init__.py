#!python3.9
from application.commands import (
    RoleCommand as RoleCommandName
)
from .role_update import CmpRoleUpdate
from .role_update_button import CmpRoleUpdateButton
from .role_update_select import CmpRoleUpdateSelect

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> CmpRoleUpdate:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    command_type: str = _commands[2].lower()
    _log.debug("command_type: {}".format(command_type))
    if command_type == RoleCommandName.button:
        _log.debug("command_type == RoleCommandName.button")
        return CmpRoleUpdateButton(rawdata)
    elif command_type == RoleCommandName.select:
        _log.debug("command_type == RoleCommandName.select")
        return CmpRoleUpdateSelect(rawdata)