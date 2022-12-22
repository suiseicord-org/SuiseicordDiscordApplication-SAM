#!python3.9
import json

from .slash_command import SlashCommand

from application.dynamodb import SettingDynamoDB

from application.enums import (
    InteractionResponseType,
    ComponentType,
    ButtonStyle,
    CommandColor,
    SuiseiCordColor
)

from logging import getLogger
_log = getLogger(__name__)

class SlashTest(SlashCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
    
    def check(self) -> bool:
        return super().check()

    def run(self) -> None:
        # self.deferred_channel_message()
        super().run()
        return
    
    def response(self) -> None:
        self.callback({
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "content" : '<@&1048945486700216370>',
                "allowed_mentions" : {
                    "parse" : ["everyone", "roles", "users"],
                }
            }
        })
        return
    
    def clean(self) -> None:
        super().clean()
        return

