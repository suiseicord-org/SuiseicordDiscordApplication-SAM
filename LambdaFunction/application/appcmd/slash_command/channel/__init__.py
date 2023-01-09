#!python3.9
from application.commands import SlashChannelCommand as SlashChannelCommandName

from .slash_channel import SlashChannel
from .slash_channel_topic import SlashChannelTopic

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> SlashChannel:
    sub_command: str = rawdata['data']["options"][0]["name"]
    sub_command = sub_command.lower()
    _log.debug("sub_command: {0}".format(sub_command))
    if sub_command == SlashChannelCommandName.topic:
        _log.debug("sub_command == ChannelCommandName.create")
        return SlashChannelTopic(rawdata)
