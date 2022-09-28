#!python3.9

from application.commands import (
    TextinputSubCommand as TextinputSubCommandName
)

from .textinput import ModalTextInput
from .textinput_send import TextInputSend

from .suiseicord_happi import from_data as tsh_from_data

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict, bot_token: str) -> ModalTextInput:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    sub_command: str = _commands[1].lower()
    _log.debug("sub_command: {}".format(sub_command))
    if sub_command == TextinputSubCommandName.send:
        _log.debug("sub_command == TextinputSubCommandName.send")
        return TextInputSend(rawdata, bot_token)
    elif sub_command == TextinputSubCommandName.happi:
        _log.debug("sub_command == TextinputSubCommandName.happi")
        return tsh_from_data(rawdata, bot_token)