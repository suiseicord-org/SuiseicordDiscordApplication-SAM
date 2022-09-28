#!python3.9
from datetime import datetime

from .suiseicord_happi import CmpSuiseicordHappi

from application.messages.message import MessageFile, filepath
from application.utils import isotimestamp
from application.enums import (
    InteractionResponseType
)

from application.discord.channel import Channel
from application.discord.message import Message

from logging import getLogger
_log = getLogger(__name__)

class CmpHappiPaycheck(CmpSuiseicordHappi):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
        _commands: list[str] = self.custom_id.split("-")
        # happi-paycheck-{channel_id}-{message_id}-{amount}
        self.target_ch: Channel = Channel(bot_token, _commands[2])
        self.target_msg: Message = Message(bot_token, _commands[2], _commands[3])
    
    def run(self) -> None:
        """報告者に対して確認したことを送信する。"""
        #deferred
        self.deferred_update_message()
        super().run()

        fp = filepath(MessageFile.SuiseiCordHappi.paycheck_complete)
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        payload: dict = {
            "content" : content,
            "message_reference" : {
                "message_id" : self.target_msg.id,
                "channel_id" : self.target_ch.id
            }
        }
        r = self.target_ch.send(payload)
        if self.run_error(r):
            pass
        else:
            pass
    
    def response(self) -> None:
        """確認済みに変更する"""
        # embedsに確認者をマークする
        embeds = self.message_data["embeds"]
        embeds[0]["footer"] = {
            "text" : f"checked by {str(self.commander)}",
            "icon_url" : self.commander.avatar_url
        }
        embeds[0]["timestamp"] = isotimestamp(datetime.now())
        # ボタンを無効化する。
        components = self.message_data["components"]
        components[0]["components"][0]["disabled"] = True
        payload = {
            "type" : InteractionResponseType.message_update.value,
            "data" : {
                "embeds" : embeds,
                "components" : components
            }
        }
        r = self.callback(payload)
        if self.response_error(r):
            pass
        else:
            pass
        return
    
    def clean(self) -> None:
        return super().clean()