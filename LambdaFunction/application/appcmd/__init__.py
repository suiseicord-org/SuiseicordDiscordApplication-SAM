#!python3.9
from application.enums import ApplicationCommandType

from .application_command import ApplicationCommand
from .slash_command import from_data as sc_from_data
from .message_command import from_data as mc_from_data

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> ApplicationCommand:
    _data = rawdata['data']
    _type_int: int = _data['type']
    _type = ApplicationCommandType(_type_int)
    _log.debug("ApplicationCommandType: {}".format(_type))
    if _type == ApplicationCommandType.slash:
        _log.debug("_type == ApplicationCommandType.slash")
        return sc_from_data(rawdata)
    elif _type == ApplicationCommandType.user:
        _log.debug("_type == ApplicationCommandType.user")
        pass
    elif _type == ApplicationCommandType.message:
        _log.debug("_type == ApplicationCommandType.message")
        return mc_from_data(rawdata)
