#!python3.9
from .create_modal import CmpCreateModal
from .create_modal_send import CreateModalSend
from .create_modal_channel_topic import CreateModalChannelTopic
from .create_modal_ban import CreateModalBan

from application.commands import (
    SlashCommand as SlashCommandName,
    SlashChannelCommand as SlashChannelCommandName,
)

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> CmpCreateModal:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    command: str  = _commands[1]
    _log.debug("command: {}".format(command))
    if command == SlashCommandName.send:
        _log.debug("command == SlashCommandName.send")
        return CreateModalSend(rawdata)
    elif command == SlashChannelCommandName.channel_topic:
        _log.debug("command == ChannelCommandName.channel_topic")
        return CreateModalChannelTopic(rawdata)
    elif command == SlashCommandName.ban:
        _log.debug("command == SlashCommandName.ban")
        return CreateModalBan(rawdata)