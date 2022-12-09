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
        command: str = self._data['name'].split(' ')[0]
        self.db = SettingDynamoDB(
            command=command,
            target_id=self._guild_id
        )
    
    def check(self) -> bool:
        return super().check()

    def run(self) -> None:
        self.deferred_channel_message()
        super().run()
        return
    
    def response(self) -> None:
        _log.debug("dynamoDB get_item()")
        data = self.db.get_item()
        _id = data["id"]
        _log.debug("_id type: {}".format(str(type(_id))))
        _log.debug("_id: ".format(_id))
        data["id"] = int(data["id"])
        self.callback({
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "content" : "```json\n{}\n```".format(
                    json.dumps(data, ensure_ascii=False, indent=4)
                )
            }
        })
        return
    
    def clean(self) -> None:
        super().clean()
        return

