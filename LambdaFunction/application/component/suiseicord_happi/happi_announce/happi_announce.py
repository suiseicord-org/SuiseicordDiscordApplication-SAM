#!python3.9
from urllib.parse import urlencode
from typing import (
    overload
)

from ..suiseicord_happi import CmpSuiseicordHappi
from application.enums import (
    ButtonStyle,
    ComponentType,
    InteractionResponseType,
    MessageFlags
)
from application.commands import (
    Commands as CommandName,
    HappiCommand as HappiCommandName
)

from logging import getLogger
_log = getLogger(__name__)

class CmpHappiAnnounce(CmpSuiseicordHappi):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
    
    def run(self) -> None:
        super().run()
        return
    
    def response(self) -> None:
        _log.debug("response()")
        with open(self.fp, "r", encoding="utf-8") as f:
            content = f.read()
        payload = {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "content" : content,
                "flags" : MessageFlags.ephemeral.value,
                "components" : [{
                    "components" : [{
                        "type" : ComponentType.button.value,
                        "style" : ButtonStyle.url.value,
                        "label" : self.label,
                        "url" : self.form_url
                    }],
                    "type" : ComponentType.action_row.value
                }]
            }
        }
        r = self.callback(payload)
        self.response_error(r)
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    @overload
    @property
    def fp(self) -> str:
        ...
    
    @overload
    @property
    def form_url(self) -> str:
        ...
    
    @overload
    @property
    def label(self) -> str:
        ...

    def _create_url(self, form_data: dict) -> str:
        entrys = form_data["entrys"]
        query = {
            f"entry.{entrys['user_id']}" : self.commander.id,
            f"entry.{entrys['name']}"    : str(self.commander)
        }
        return '%s?%s' % (form_data["url"], urlencode(query))