#!python3.9
from typing import Optional
from requests import Response

from .slash_command import SlashCommand

from application.discord.channel import InteractionPartialChannel
from application.discord.member import Member
from application.discord.user import PartiaUser

from application.commands import (
    SlashCommand as SlashCommandName,
    SendCommand as SendCommandName,
    SendCommandOption as SendCommandOptionName
)
from application.components import Button, CustomID
from application.enums import (
    InteractionResponseType,
    ComponentType,
    ButtonStyle
)
from application.interaction import get_options, get_resolved_data
from application.mytypes.snowflake import Snowflake

from logging import getLogger
_log = getLogger(__name__)

class SlashUser(SlashCommand):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
        self.sub_command: dict = self._data['options'][0]
        self.resolved: dict = self._data['resolved']
        self.sub_command_name: str = self.sub_command['name']
        _targets = get_options(
            self.sub_command['options'],
            name = SendCommandOptionName.target
        )
        self.target_id: Snowflake = _targets[0]['value']

    
    def run(self) -> None:
        super().run()
        return

    
    def response(self) -> None:
        self.payload: dict = {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "embeds" : [
                    self._create_embed()
                ]
            }
        }
        r: Response = self.callback(self.payload)
        if self.response_error(r):
            pass
        else:
            pass
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    def _create_embed(self) -> dict:
        embed: dict = {"title" : "ユーザー情報取得結果"} # set title
        return embed

