#!python3.9
from requests import Response

from .create_modal import CmpCreateModal

from application.enums import (
    InteractionResponseType,
    ComponentType,
    TextInputStyle
)
from application.components import CustomID

from logging import getLogger
_log = getLogger(__name__)

class CreateModalSend(CmpCreateModal):

    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
    
    def check(self) -> bool:
        _log.debug("check()")
        return self.check_permission(self.deferred_channel_message)

    def run(self) -> None:
        super().run()
        return

    def response(self) -> None:
        r: Response = self.callback(self._payload)
        if self.response_error(r):
            pass
        else:
            pass
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    @property
    def _payload(self) -> dict:
        text = self.message_data["embeds"][0].get("description", "")
        payload: dict = {
            "type" : InteractionResponseType.modal.value,
            "data" : {
                "title" : "【送信コマンド】メッセージ登録フォーム",
                "custom_id" : CustomID.textinput_send,
                "components" : [
                    {
                        "type" : ComponentType.action_row.value,
                        "components" : [{
                            "type" : ComponentType.text_input.value,
                            "custom_id" : CustomID.text,
                            "label" : "送信メッセージ本文",
                            "style" : TextInputStyle.long.value,
                            "max_length" : 2000,
                            "value" : text,
                            "required" : True
                        }]
                    }
                ]
            }
        }
        return payload