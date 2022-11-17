#!python3.9
from .enums import (
    InteractionType,
)

from .interaction import Interaction

from .appcmd import from_data as ap_from_data
from .component import from_data as c_from_data
from .modalsubmit import from_data as m_from_data

import os, json
from logging import getLogger, config

# Logger
LOGGING_MODE: str = os.getenv('LOGGING_MODE')

if (LOGGING_MODE is not None) and (LOGGING_MODE.lower() == 'debug'):
    fp = 'logging_format/debug.json'
else:
    fp = 'logging_format/info.json'
with open(fp, 'r') as f:
    _config = json.load(f)
config.dictConfig(_config)
_log = getLogger(__name__)

def from_data(rawdata: dict, bot_token: str) -> Interaction:
    _type_int: int = rawdata['type']
    _type: InteractionType = InteractionType(_type_int)
    if _type == InteractionType.application_command:
        _log.debug("_type == InteractionType.application_command")
        return ap_from_data(rawdata, bot_token)
    elif _type == InteractionType.component:
        _log.debug("_type == InteractionType.component")
        return c_from_data(rawdata, bot_token)
    elif _type == InteractionType.application_command_autocomplete:
        _log.debug("_type == InteractionType.application_command_autocomplete")
        pass
    elif _type == InteractionType.model_submit:
        _log.debug("_type == InteractionType.model_submit")
        return m_from_data(rawdata, bot_token)
    else:
        _log.debug("not match")
        return Interaction(rawdata, bot_token)