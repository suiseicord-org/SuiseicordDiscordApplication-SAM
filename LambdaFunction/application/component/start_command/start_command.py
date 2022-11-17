#!python3.9

from ..component import Component

from logging import getLogger
_log = getLogger(__name__)

class CmpStartCommand(Component):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
        pass

    def check(self) -> bool:
        return super().check()

    def run(self) -> None:
        super().run()
        return

    def response(self) -> None:
        super().response()
        return 
    
    def clean(self) -> None:
        return super().clean()