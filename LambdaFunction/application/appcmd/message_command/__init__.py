#!python3.9
from application.commands import MessageCommand as MessageCommandName

from .message_command import MessageCommand
from .message_save import MessageSave

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> MessageCommand:
    name: str = rawdata['data']['name']
    name = name.lower()
    _log.debug("name: {0}".format(name))
    if name == MessageCommandName.save:
        _log.debug('name == MessageCommandName.save')
        return MessageSave(rawdata)
