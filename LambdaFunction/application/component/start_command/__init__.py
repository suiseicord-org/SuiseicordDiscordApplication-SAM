#!python3.9

from .start_command import CmpStartCommand
from .start_send import CmpStartSend
from .start_channel_topic import CmpStartChannelTopic

from application.commands import (
    SlashCommand as SlashCommandName,
    ChannelCommand as ChannelCommandName,
)

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> CmpStartCommand:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    #start-command-
    command: str = _commands[1]
    _log.debug("command: {}".format(command))
    if command == SlashCommandName.send:
        _log.debug("command == SlashCommandName.send")
        return CmpStartSend(rawdata)
    elif command == ChannelCommandName.channel_topic:
        _log.debug("command == ChannelCommandName.channel_topic")
        return CmpStartChannelTopic(rawdata)