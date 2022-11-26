#!python3.9

from ..suiseicord_happi import CmpSuiseicordHappi

from logging import getLogger
_log = getLogger(__name__)

class CmpHappiPayreport(CmpSuiseicordHappi):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        _commands: list[str] = self.custom_id.split("-")
        self.way = _commands[2]
        self.amount = _commands[3]
    
    def run(self) -> None:
        return super().run()
    
    def response(self) -> None:
        return super().response()
    
    def clean(self) -> None:
        return super().clean()


        