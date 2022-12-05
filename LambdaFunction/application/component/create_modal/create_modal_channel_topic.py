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

class CreateModalChannelTopic(CmpCreateModal):

    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
    
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
                "title" : "【チャンネルトピック編集コマンド】トピック入力フォーム",
                "custom_id" : CustomID.textinput_channel_topic,
                "components" : [
                    {
                        "type" : ComponentType.action_row.value,
                        "components" : [{
                            "type" : ComponentType.text_input.value,
                            "custom_id" : CustomID.text,
                            "label" : "チャンネルトピック",
                            "style" : TextInputStyle.long.value,
                            "max_length" : 1024,
                            "value" : text,
                            "required" : True
                        }]
                    }
                ]
            }
        }
        return payload