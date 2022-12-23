#!python3.9
from requests import Response
from .role_update import CmpRoleUpdate

from application.enums import (
    InteractionResponseType,
    MessageFlags
)

from logging import getLogger
_log = getLogger(__name__)

class CmpRoleUpdateSelect(CmpRoleUpdate):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.add_roles: list[int] = [int(r) for r in self._data['values']]
        _log.debug("add_roles: {}".format(self.add_roles))
        all_roles: set[int] = self.all_menue_roles()
        _log.debug("all_roles: {}".format(all_roles))
        self.remove_roles: list[int] = list(all_roles.difference(self.add_roles))
        _log.debug("remove_roles: {}".format(self.remove_roles))
    
    def check(self) -> bool:
        return super().check()
    
    def run(self) -> None:
        reason: str = "Application Command; Add Role (message id: {})".format(
            self.message_data["id"]
        )
        self.res: Response = self.commander.update_roles(
            self.add_roles,
            self.remove_roles,
            reason=reason
        )

    def response(self) -> None:
        if self.res.ok:
            content = "ロールを更新しました！ Your role has been updated!"
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
    
    def all_menue_roles(self) -> set[int]:
        for compnents in self.message_data['components'][0]['components']:
            if compnents['custom_id'] == self.custom_id:
                return {
                    int(opt['value']) for opt in compnents['options']
                }
        return set()
            