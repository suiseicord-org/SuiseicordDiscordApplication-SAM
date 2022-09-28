#!python3.9
from ..interaction import Interaction

from logging import getLogger
_log = getLogger(__name__)

class ApplicationCommand(Interaction):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)

    def run(self) -> None:
        super().run()
        return
    
    def response(self) -> None:
        super().response()
        return
    
    def clean(self) -> None:
        super().clean()
        return