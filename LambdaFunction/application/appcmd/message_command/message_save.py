#!python3.9
from requests import Response
from typing import Optional

from .message_command import MessageCommand

from application.dynamodb import SettingDynamoDB

from application.discord.channel import Channel

from application.enums import (
    InteractionResponseType,
    MessageFlags
)

from logging import getLogger
_log = getLogger(__name__)

class MessageSave(MessageCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)

    def run(self) -> None:
        self.callback({
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "flags" : MessageFlags.ephemeral.value,
                "content" : "保存中です..."
            }
        })
        super().run()

        self.result = self.message_save()

        return
    
    def response(self) -> None:
        if self.result is None:
            content = 'メッセージ保存機能が有効になっていません。管理者に問い合わせてください。'
        elif self.result.ok:
            content = f'メッセージを {self.send_channel.mention} に保存しました。'
        else:
            content = 'メッセージの保存に失敗しました。BOT権限が不足している可能性があります。管理者に問い合わせてください。'
        payload: dict = {
            "content" : content
        }
        self.update_callback(payload)
        return
    
    def clean(self) -> None:
        super().clean()
        return

    def message_save(self) -> Optional[Response]:
        db = SettingDynamoDB()
        _log.debug("dynamoDB get_item()")
        db_data: dict = db.get_item(
            command='message-save',
            target_id=int(self._guild_id)
        )

        _send_channel_id: Optional[int] = db_data.get('channel')

        if _send_channel_id is None:
            return None
        
        self.send_channel: Channel = Channel(_send_channel_id)

        save_embeds, attachments = self.target_message.to_embeds(detail=True, transfer_files=True)
        save_embeds[0]["footer"] = {
            "text" : f"saved by {str(self.commander)}",
            "icon_url" : self.commander.avatar_url
        }

        payload: dict = {"embeds" : save_embeds[:10]}

        return self.send_channel.send(json_payload=payload, attachments=attachments)
