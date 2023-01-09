#!python3.9
from application.commands import (
    SlashCommand as SlashCommandName,
    SlashChannelCommand as SlashChannelCommandName,
)

from .start_command import CmpStartCommand

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> CmpStartCommand:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    #start-command-
    command: str = _commands[1]
    _log.debug("command: {}".format(command))
    if command == SlashCommandName.send:
        _log.debug("command == SlashCommandName.send")
        from .start_send import CmpStartSend
        return CmpStartSend(rawdata)
    elif command == SlashChannelCommandName.channel_topic:
        _log.debug("command == ChannelCommandName.channel_topic")
        from .start_channel_topic import CmpStartChannelTopic
        return CmpStartChannelTopic(rawdata)
    elif command == SlashCommandName.ban:
        _log.debug("command == SlashCommandName.ban")
        from .start_ban import CmpStartBan
        return CmpStartBan(rawdata)
