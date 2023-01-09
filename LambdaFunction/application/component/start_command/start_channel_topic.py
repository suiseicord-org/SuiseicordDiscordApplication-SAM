#!python3.9
import json
import requests
from datetime import datetime

from .start_command import CmpStartCommand

from application.utils import isotimestamp
from application.enums import (
    InteractionResponseType,
    CommandColor
)
from application.discord.channel import Channel
from application.mytypes.snowflake import Snowflake

from logging import getLogger
_log = getLogger(__name__)

class CmpStartChannelTopic(CmpStartCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        _commands: list[str] = self.custom_id.split('-')
        self.target_id: Snowflake = _commands[2]
        self.target: Channel = Channel(_id=self.target_id)

    def check(self) -> bool:
        return self.check_permission(defferd_func=self.deferred_update_message)

    def run(self) -> None:
        """チェンネルトピック編集"""
        self.deferred_update_message() # loads
        super().run()

        embed = self.message_data["embeds"][0]
        topic: str = embed.get("description", "")
        payload = {
            "topic" : topic
        }
        reason = "Edit channel topic using command. Started by {0} (ID: {1})".format(
            str(self.commander),
            self.commander.id
        )
        self.res: requests.Response = self.target.modify(
            payload,
            reason = reason
        )
        if self.run_error(self.res):
            pass
        else:
            pass
        return

    def response(self) -> None:
        """result送信"""
        r = self.callback(self.response_payload)
        if self.response_error(r):
            pass
        else:
            pass
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    @property
    def response_payload(self) -> dict:
        embeds = self.message_data["embeds"]
        if self.res.ok:
            embeds[0]["title"] = "編集成功"
            embeds[0]["color"] = CommandColor.success.value
        else:
            embeds[0]["title"] = "編集失敗"
            text = json.dumps(self.res.json(), ensure_ascii=False, indent=4)
            text = text[:1000]
            if not embeds[0].get("fields", False):
                embeds[0]["fields"] = []
            embeds[0]["fields"].append({
                "name" : "詳細",
                "value" : f"```json\n{text}\n```"
            })
            embeds[0]["color"] = CommandColor.fail.value
        embeds[0]["footer"] = {
            "text" : f"started by {str(self.commander)}",
            "icon_url" : self.commander.avatar_url
        }
        embeds[0]["timestamp"] = isotimestamp(datetime.now())
        components = self.message_data["components"]
        for comp in components[0]["components"]:
            comp["disabled"] = True
        payload: dict = {
            "type" : InteractionResponseType.message_update.value,
            "data" : {
                "embeds" : embeds,
                "components" : components
            }
        }
        return payload
