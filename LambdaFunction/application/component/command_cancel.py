#!python3.9

from .component import Component

from application.enums import (
    InteractionResponseType
)

from logging import getLogger
_log = getLogger(__name__)

class CmpCommandCancel(Component):

    def __init__(self, rawdata: dict, bot_token: str):
        _log.debug("make instance")
        super().__init__(rawdata, bot_token)
    
    def check(self) -> bool:
        return self.check_permission(defferd_func=self.deferred_update_message)

    def run(self) -> None:
        return super().run()
    
    def response(self) -> None:
        components = self.message_data["components"]
        for comp in components[0]["components"]:
            comp["disabled"] = True
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