#!python3.9
from requests import Response
from .role_update import CmpRoleUpdate

from application.enums import (
    InteractionResponseType,
    MessageFlags
)

class CmpRoleUpdateButton(CmpRoleUpdate):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        _commands: list[str] = self.custom_id.split('-')
        self.update_role_id: int = int(_commands[3])
    
    def check(self) -> bool:
        return super().check()
    
    def run(self) -> None:
        super().run()
        if self.update_role_id in self.commander._role_ids:
            reason: str = "Application Command; Remove Role (message id: {})".format(
                self.message_data["id"]
            )
            self.res: Response = self.commander.remove_role(
                role_id=self.update_role_id,
                reason=reason
            )
            return
        else:
            reason: str = "Application Command; Add Role (message id: {})".format(
                self.message_data["id"]
            )
            self.res: Response = self.commander.add_role(
                role_id=self.update_role_id,
                reason=reason
            )
            return

    def response(self) -> None:
        if self.res.ok:
            if self.update_role_id in self.commander._role_ids:
                content = "<@&{0}> ロールを付与しました！\nYou got a <@&{0}> role!".format(
                    self.update_role_id
                )
            else:
                content = "<@&{0}> ロールを削除しました！\nYou lost a <@&{0}> role!".format(
                    self.update_role_id
                )
        else:
            content = "ロールの更新に失敗しました。サーバー管理者に問い合わせてください。 \
                \nFailed to update role. Please contact your server administrator."
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