#!python3.9
import json
import requests
from .start_command import CmpStartCommand
from datetime import datetime

from application.utils import isotimestamp
from application.commands import (
    SendCommand as SendCommandName
)
from application.components import CustomID
from application.enums import (
    InteractionResponseType,
    ButtonStyle,
    ComponentType
)
from application.mytypes.snowflake import Snowflake
from application.discord.channel import Channel, DmChannel, NoDmChannelError

from logging import getLogger
_log = getLogger(__name__)

class CmpStartSend(CmpStartCommand):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
        _commands: list[str] = self.custom_id.split('-')
        self.sub_command:str = _commands[2]
        self.target_id: Snowflake = _commands[3]

    def run(self) -> None:
        """メッセージ送信"""
        self.deferred_update_message() # loads
        super().run()
        if self.sub_command == SendCommandName.dm:
            try:
                self.target = DmChannel(self._bot_token, self.target_id)
            except NoDmChannelError:
                return
        else:
            self.target = Channel(self._bot_token, self.target_id)
        self.embed = self.message_data["embeds"][0]
        fields = dict()
        for field in self.embed["fields"]:
            fields[field["name"]] = field["value"]
        if fields.get("attachments") is not None:
            self.attachments = fields["attachments"].split("\n")
        else:
            self.attachments = None
        self.res: requests.Response = self.target.send(self.send_payload)
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
    def send_payload(self) -> dict:
        payload: dict = {
            "content" : self.embed.get("description")
        }
        if self.attachments is not None:
            payload["embeds"] = []
            for url in self.attachments:
                payload["embeds"].append({
                    "image" : {
                        "url" : url
                    }
                })
        # happi announce
        if self.sub_command == SendCommandName.happi:
            #componentを追加
            payload["components"] = [
                {
                    "components": [
                        {
                            "custom_id": CustomID.happi_announce_jp,
                            "label": "日本国内の方",
                            "style": ButtonStyle.primary.value,
                            "type": ComponentType.button.value
                        },
                        {
                            "custom_id": CustomID.happi_announce_en,
                            "label": "Outside Japan or Using Tenso",
                            "style": ButtonStyle.success.value,
                            "type": ComponentType.button.value
                        }
                    ],
                    "type": 1
                }
            ]
        return payload
    
    @property
    def response_payload(self) -> dict:
        embeds = self.message_data["embeds"]
        if self.res.status_code != requests.codes.ok:
            embeds[0]["title"] = "送信失敗"
            text = json.dumps(self.res.json(), ensure_ascii=False, indent=4)
            text = text[:1000]
            embeds[0]["fields"].append({
                "name" : "詳細",
                "value" : f"```json\n{text}\n```"
            })
        else:
            embeds[0]["title"] = "送信成功"
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