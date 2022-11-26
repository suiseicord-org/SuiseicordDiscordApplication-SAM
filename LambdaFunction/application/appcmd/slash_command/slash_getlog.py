#!python3.9
from .slash_command import SlashCommand
from application.commands import (
    GetlogCommand as GetlogCommandName,
    GetlogCommandOption as GetlogCommandOptionName
)
from application.interaction import parse_to_dict
from application.mytypes.snowflake import Snowflake

from application.discord.channel import (
    Channel,
    DmChannel
)

from logging import getLogger
_log = getLogger(__name__)

class SlashGetlog(SlashCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.sub_command: dict = self._data['options'][0]
        self.resolved: dict = self._data['resolved']
        self.sub_command_name: str = self.sub_command['name']
        self.options: dict = parse_to_dict(self.sub_command['options'])
        self.target_id: Snowflake = self.options[GetlogCommandOptionName.target]
    
    def run(self) -> None:
        super().run()
        self.deferred_channel_message()
        if self.sub_command_name == GetlogCommandName.dm:
            self.target = DmChannel(self.target_id)
        else:
            self.target = Channel(self.target_id)
        self.logfile: str = self.target.logs(**self.options)
        return
    
    def response(self) -> None:
        super().response()
        return
    
    def clean(self) -> None:
        super().clean()
        return
