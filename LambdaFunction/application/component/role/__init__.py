#!python3.9
from application.commands import (
    RoleCommand as RoleCommandName
)
from .role import CmpRole

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> CmpRole:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    sub_command: str = _commands[1].lower()
    _log.debug("sub_command: {}".format(sub_command))
    if sub_command == RoleCommandName.add:
        _log.debug("sub_command == RoleCommandName.add")
        from .role_add import CmpRoleAdd
        return CmpRoleAdd(rawdata)
    elif sub_command == RoleCommandName.update:
        _log.debug("sub_command == RoleCommandName.update")
        from .role_update import from_data as cru_from_data
        return cru_from_data(rawdata)
