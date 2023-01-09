#!python3.9
from ..component import Component

from application.mytypes.components import (
    Component as ComponentPayload
)
from application.enums import (
    InteractionResponseType,
    ComponentType
)

from logging import getLogger
_log = getLogger(__name__)

class CmpCommandCancel(Component):

    def __init__(self, rawdata: dict):
        _log.debug("make instance")
        super().__init__(rawdata)
    
    def check(self) -> bool:
        return self.check_permission(defferd_func=self.deferred_update_message)

    def run(self) -> None:
        return super().run()
    
    def response(self) -> None:
        components = self.message_data["components"]
        self.disable_components(components)
        payload: dict = {
            "type" : InteractionResponseType.message_update.value,
            "data" : {
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
