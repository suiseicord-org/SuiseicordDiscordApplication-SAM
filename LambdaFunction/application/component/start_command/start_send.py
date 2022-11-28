#!python3.9
import json
import requests
from datetime import datetime
from typing import (
    Optional
)

from .start_command import CmpStartCommand

from application.utils import isotimestamp
from application.commands import (
    SendCommand as SendCommandName,
    SendCommandOption as SendCommandOptionName
)
from application.components import CustomID
from application.discord.attachment import Attachment
from application.enums import (
    InteractionResponseType,
    ButtonStyle,
    ComponentType,
    CommandColor
)
from application.discord.channel import Channel, DmChannel, NoDmChannelError
from application.discord.message import Message
from application.mytypes.snowflake import Snowflake
from application.mytypes.embed import Embed as EmbedPayload

from logging import getLogger
_log = getLogger(__name__)

class CmpStartSend(CmpStartCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        _commands: list[str] = self.custom_id.split('-')
        self.sub_command:str = _commands[2]
        self.target_id: Snowflake = _commands[3]

    def check(self) -> bool:
        return self.check_permission(defferd_func=self.deferred_update_message)

    def run(self) -> None:
        """メッセージ送信"""
        self.deferred_update_message() # loads
        super().run()
        if self.sub_command == SendCommandName.dm:
            try:
                self.target = DmChannel(self.target_id)
            except NoDmChannelError as e:
                self.res: requests.Response = e.res
                return
        else:
            self.target = Channel(self.target_id)
        self.embed = self.message_data["embeds"][0]
        fields = dict()
        for field in self.embed["fields"]:
            fields[field["name"]] = field["value"]
        self.attachments: Optional[list[Attachment]] = []
        for key, value in fields.items():
            key: str; value: str
            if key.startswith(SendCommandOptionName.attachments):
                self.attachments.append(Attachment(
                    json.loads(value.strip('`json'))
                ))
        if len(self.attachments) < 1:
            self.attachments = None
        self.res: requests.Response = self.target.send(self.send_payload, attachments=self.attachments)
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
        if self.res.ok:
            embeds[0]["title"] = "送信成功"
            embeds[0]["color"] = CommandColor.success.value
            # message: Message = Message(self.res.json())
        else:
            embeds[0]["title"] = "送信失敗"
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