#!python3.9
from requests import Response

from .happi_payreport import CmpHappiPayreport
from application.enums import (
    InteractionResponseType,
    ComponentType,
    TextInputStyle
)

from logging import getLogger
_log = getLogger(__name__)

class CmpHappiPayreportBank(CmpHappiPayreport):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
    
    def run(self) -> None:
        return super().run()
    
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
        payload: dict = {
            "type" : InteractionResponseType.modal.value,
            "data" : {
                "title" : "【銀行口座振込】入金報告フォーム",
                "custom_id" : "textinput-happi-payreport-bank",
                "components" : [
                    {
                        "type" : ComponentType.action_row.value,
                        "components" : [{
                            "type" : ComponentType.text_input.value,
                            "custom_id" : "amount",
                            "label" : "入金金額",
                            "style" : TextInputStyle.short.value,
                            "min_length" : 1,
                            "max_length" : 10,
                            "value" : str(self.amount),
                            "required" : True
                        }]
                    },
                    {
                        "type" : ComponentType.action_row.value,
                        "components" : [{
                            "type" : ComponentType.text_input.value,
                            "custom_id" : "name",
                            "label" : "入金名義",
                            "style" : TextInputStyle.short.value,
                            "min_length" : 1,
                            "max_length" : 100,
                            "required" : True
                        }]
                    }
                ]
            }
        }
        return payload
