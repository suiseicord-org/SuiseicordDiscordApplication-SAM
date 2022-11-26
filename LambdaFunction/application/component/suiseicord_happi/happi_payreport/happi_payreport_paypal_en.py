#!python3.9
from requests import Response

from .happi_payreport import CmpHappiPayreport
from application.enums import (
    InteractionResponseType,
    ComponentType,
    TextInputStyle
)

from application.mytypes.snowflake import Snowflake

from logging import getLogger
_log = getLogger(__name__)

class CmpHappiPayreportPaypalEn(CmpHappiPayreport):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        _commands: list[str] = self.custom_id.split("-")
        way = _commands[2]
        amount = _commands[3]
    
    def run(self) -> None:
        return super().run()
    
    def response(self) -> None:
        r: Response = self.callback(self._payload)
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    @property
    def _payload(self) -> dict:
        payload: dict = {
            "type" : InteractionResponseType.modal.value,
            "data" : {
                "title" : "【PayPal】Payment Report Form",
                "custom_id" : "textinput-happi-payreport-paypal",
                "components" : [
                    {
                        "type" : ComponentType.action_row.value,
                        "components" : [{
                            "type" : ComponentType.text_input.value,
                            "custom_id" : "amount",
                            "label" : "amount",
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
                            "label" : "Your PayPal E-mail address",
                            "style" : TextInputStyle.short.value,
                            "min_length" : 1,
                            "max_length" : 300, # 256
                            "required" : True
                        }]
                    }
                ]
            }
        }
        return payload