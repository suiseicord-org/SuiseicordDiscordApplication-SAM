#!python3.9
from application.enums import ApplicationCommandType

from .application_command import ApplicationCommand
from .slash_command import from_data as sc_from_data

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict, bot_token: str) -> ApplicationCommand:
    _data = rawdata['data']
    _type_int: int = _data['type']
    _type = ApplicationCommandType(_type_int)
    if _type == ApplicationCommandType.slash:
        _log.debug("_type == ApplicationCommandType.slash")
        return sc_from_data(rawdata, bot_token)
    elif _type == ApplicationCommandType.user:
        _log.debug("_type == ApplicationCommandType.user")
        pass
    elif _type == ApplicationCommandType.message:
        _log.debug("_type == ApplicationCommandType.message")
        pass