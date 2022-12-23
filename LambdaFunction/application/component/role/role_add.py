#!python3.9
from requests import Response
from .role import CmpRole

from application.enums import (
    InteractionResponseType,
    MessageFlags
)

from logging import getLogger
_log = getLogger(__name__)

class CmpRoleAdd(CmpRole):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        _commands: list[str] = self.custom_id.split('-')
        self.add_role_id: int = int(_commands[2])
        self.has_role: bool = False
    
    def check(self) -> bool:
        return super().check()
    
    def run(self) -> None:
        super().run()
        if self.add_role_id in self.commander._role_ids:
            self.has_role = True
            return
        reason: str = "Application Command; Add Role (message id: {})".format(
            self.message_data["id"]
        )
        self.res: Response = self.commander.add_role(
            role_id=self.add_role_id,
            reason=reason
        )
        return

    def response(self) -> None:
        if self.has_role:
            content = "あなたはすでにこのロールを付与されています。\nYou already have this role."
        elif self.res.ok:
            content = "<@&{0}> ロールを付与しました！\nYou got a <@&{0}> role!".format(
                self.add_role_id
            )
        else:
            content = "ロールの追加に失敗しました。サーバー管理者に問い合わせてください。 \
                \nFailed to add role. Please contact your server administrator."
        payload = {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "flags" : MessageFlags.ephemeral.value,
                "content" : content
            }
        }
        self.callback(payload)
        return
    
    def clean(self) -> None:
        return super().clean()