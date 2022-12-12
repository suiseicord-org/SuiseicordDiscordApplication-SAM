#!python3.9
from .command_cancel import CmpCommandCancel

from application.commands import (
    BanCommandOption as BanCommandOptionName
)
from application.mytypes.components import (
    Component as ComponentPayload
)
from application.enums import (
    InteractionResponseType,
    ComponentType,
    MessageFlags
)

from logging import getLogger
_log = getLogger(__name__)

class CmpCommandCancelBan(CmpCommandCancel):

    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.commands: list[str] = self.custom_id.split('-')
        self.count: int = int(self.commands[2])
        _log.info("BAN cancel count: {}".format(self.count))
    
    def check(self) -> bool:
        return self.check_permission(defferd_func=self.deferred_update_message)

    def run(self) -> None:
        return super().run()
    
    def response(self) -> None:
        for field in self.message_data["embeds"][0]["fields"]:
            if field["name"].startswith(BanCommandOptionName.cancel_title):
                cancel_members_text: str = field["value"]
                break
        else:
            cancel_members_text: str = ""
        if str(self.commander.id) in cancel_members_text:
            payload: dict = {
                "type" : InteractionResponseType.channel_message.value,
                "data" : {
                    "flags" : MessageFlags.ephemeral.value,
                    "content" : "既にこのボタンを押しています。"
                }
            }
        else:
            embeds = self.message_data["embeds"]
            for field in embeds[0]["fields"]:
                if field["name"].startswith(BanCommandOptionName.cancel_title):
                    field["value"] += "\n<@{0}> (ID: {0})".format(
                        self.commander.id
                    )
            self.count -= 1
            self.commands[2] = str(self.count)
            custom_id = '-'.join(self.commands)
            components = self.message_data["components"]
            components[0]["components"][1]["custom_id"] = custom_id
            if self.count > 0:
                pass
            else:
                self.disable_components(components)
            payload: dict = {
                "type" : InteractionResponseType.message_update.value,
                "data" : {
                    "embeds" : embeds,
                    "components" : components
                }
            }
        r= self.callback(payload)
        if self.response_error(r):
            pass
        else:
            pass
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    def disable_components(self, payload: list[ComponentPayload]) -> None:
        for component in payload:
            if component.get('type') is None:
                continue
            _type = ComponentType(component["type"])
            if _type == ComponentType.action_row:
                self.disable_components(component["components"])
            elif _type == ComponentType.button or \
                 _type == ComponentType.select or \
                 _type == ComponentType.user_select or \
                 _type == ComponentType.role_select or \
                 _type == ComponentType.mentionable_select or \
                 _type == ComponentType.channel_select:
                component["disabled"] = True