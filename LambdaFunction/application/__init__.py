#!python3.9
from .enums import (
    InteractionType,
)

from .interaction import Interaction

from logging import getLogger

_log = getLogger(__name__)

def from_data(rawdata: dict) -> Interaction:
    _type_int: int = rawdata['type']
    _type: InteractionType = InteractionType(_type_int)
    if _type == InteractionType.application_command:
        _log.debug("_type == InteractionType.application_command")
        from .appcmd import from_data as ap_from_data
        return ap_from_data(rawdata)
    elif _type == InteractionType.component:
        _log.debug("_type == InteractionType.component")
        from .component import from_data as c_from_data
        return c_from_data(rawdata)
    elif _type == InteractionType.application_command_autocomplete:
        _log.debug("_type == InteractionType.application_command_autocomplete")
        pass
    elif _type == InteractionType.model_submit:
        _log.debug("_type == InteractionType.model_submit")
        from .modalsubmit import from_data as m_from_data
        return m_from_data(rawdata)
    else:
        _log.debug("not match")
        return Interaction(rawdata)
