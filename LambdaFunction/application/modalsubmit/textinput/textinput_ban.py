#!python3.9
from .textinput import ModalTextInput

from application.components import CustomID
from application.enums import (
    InteractionResponseType
)

from logging import getLogger
_log = getLogger(__name__)

class TextInputBan(ModalTextInput):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)

    def check(self) -> bool:
        return super().check()

    def run(self) -> None:
        super().run()
        return

    def response(self) -> None:
        data = self.parse_values()
        embeds = self.message_data["embeds"]
        embeds[-1]["description"] = data[CustomID.text]
        payload: dict = {
            "type" : InteractionResponseType.message_update.value,
            "data" : {
                "embeds" : embeds
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