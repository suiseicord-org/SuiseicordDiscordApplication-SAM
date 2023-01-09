#!python3.9
from application.commands import (
    TextinputSubCommand as TextinputSubCommandName
)

from .textinput import ModalTextInput

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> ModalTextInput:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    sub_command: str = _commands[1].lower()
    _log.debug("sub_command: {}".format(sub_command))
    if sub_command == TextinputSubCommandName.send:
        _log.debug("sub_command == TextinputSubCommandName.send")
        from .textinput_send import TextInputSend
        return TextInputSend(rawdata)
    elif sub_command == TextinputSubCommandName.channel_topic:
        _log.debug("sub_command == TextinputSubCommandName.channel_topic")
        from .textinput_channel_topic import TextInputChannelTopic
        return TextInputChannelTopic(rawdata)
    elif sub_command == TextinputSubCommandName.ban:
        _log.debug("sub_command == TextinputSubCommandName.ban")
        from .textinput_ban import TextInputBan
        return TextInputBan(rawdata)
    # elif sub_command == TextinputSubCommandName.happi:
    #     _log.debug("sub_command == TextinputSubCommandName.happi")
    #     from .suiseicord_happi import from_data as tsh_from_data
    #     return tsh_from_data(rawdata)